from __future__ import annotations

import sys
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import sensors


# ---------------------------------------------------------------------------
# Fake smbus2 / serial plumbing
# ---------------------------------------------------------------------------


class FakeMS5611Bus:
    """Mimics smbus2.SMBus: read_word_data returns the two received bytes in
    the kernel's little-endian word layout (first byte -> low), matching what
    smbus2 hands back for a big-endian device."""

    def __init__(self, prom: list[int], d1: int, d2: int) -> None:
        self._prom = list(prom)
        self._d1 = d1
        self._d2 = d2
        self._adc_calls = 0
        self.commands: list[object] = []

    def write_byte(self, address: int, command: int) -> None:
        self.commands.append(command)

    def read_word_data(self, address: int, register: int) -> int:
        index = (register - sensors._MS5611_PROM_BASE) // 2
        word = self._prom[index]
        return ((word & 0xFF) << 8) | ((word >> 8) & 0xFF)

    def read_i2c_block_data(self, address: int, command: int, length: int) -> list[int]:
        self._adc_calls += 1
        value = self._d1 if self._adc_calls == 1 else self._d2
        return [(value >> 16) & 0xFF, (value >> 8) & 0xFF, value & 0xFF]

    def close(self) -> None:
        self.commands.append("close")


def patch_smbus(fake_bus: FakeMS5611Bus):
    return patch.dict(
        sys.modules, {"smbus2": SimpleNamespace(SMBus=lambda bus: fake_bus)}
    )


class FakeSerialPort:
    def __init__(self, chunks: list[bytes]) -> None:
        self._chunks = iter(chunks)
        self.closed = False

    def read(self, size: int) -> bytes:
        try:
            return next(self._chunks)
        except StopIteration:
            return b""

    def close(self) -> None:
        self.closed = True


def patch_serial(port: FakeSerialPort):
    return patch.dict(
        sys.modules, {"serial": SimpleNamespace(Serial=lambda *a, **k: port)}
    )


# ---------------------------------------------------------------------------
# MS5611 compensation (datasheet vectors)
# ---------------------------------------------------------------------------

_C1, _C2, _C3, _C4, _C5, _C6 = 40127, 36924, 23317, 23282, 33464, 28312
# CRC-4 of this PROM (with C0 data nibble 0) is 0, so C0=0x0000 is valid.
_DATASHEET_PROM = [0x0000, _C1, _C2, _C3, _C4, _C5, _C6, 0x0000]


class MS5611CompensationTests(unittest.TestCase):
    def _sample(self, d1: int, d2: int) -> dict[str, float]:
        fake = FakeMS5611Bus(_DATASHEET_PROM, d1, d2)
        with patch_smbus(fake):
            sensor = sensors._MS5611(1, 0x76)
            try:
                return sensor.sample()
            finally:
                sensor.close()

    def test_datasheet_warm_vector(self) -> None:
        result = self._sample(9085466, 8569150)
        self.assertEqual(result["pressure_pa"], 100009.0)
        self.assertEqual(result["temperature_c"], 20.07)

    def test_cold_vector_uses_second_order(self) -> None:
        result = self._sample(9085466, 8388608)
        self.assertEqual(result["pressure_pa"], 98804.0)
        self.assertEqual(result["temperature_c"], 13.84)

    def test_very_cold_vector(self) -> None:
        result = self._sample(9085466, 7000000)
        self.assertEqual(result["pressure_pa"], 85693.0)
        self.assertEqual(result["temperature_c"], -44.31)


class MS5611PromTests(unittest.TestCase):
    def test_read_prom_decodes_big_endian_words(self) -> None:
        fake = FakeMS5611Bus(_DATASHEET_PROM, 0, 0)
        with patch_smbus(fake):
            sensor = sensors._MS5611(1, 0x76)
            try:
                self.assertEqual(sensor._prom, _DATASHEET_PROM)
            finally:
                sensor.close()
        # reset command is issued before reading the 8 PROM words
        self.assertEqual(fake.commands[0], sensors._MS5611_CMD_RESET)

    def test_crc4_matches_stored_nibble(self) -> None:
        prom = [0x5ABC, 40127, 36924, 23317, 23282, 33464, 28312, 0x0000]
        self.assertEqual(sensors._ms5611_crc4(prom), 0x5)
        self.assertEqual((prom[0] >> 12) & 0x0F, 0x5)

    def test_crc_mismatch_raises(self) -> None:
        bad_prom = list(_DATASHEET_PROM)
        bad_prom[0] = 0x6000  # wrong CRC nibble (computed 0x0)
        fake = FakeMS5611Bus(bad_prom, 0, 0)
        with patch_smbus(fake):
            with self.assertRaises(OSError):
                sensors._MS5611(1, 0x76)

    def test_read_ms5611_returns_none_on_crc_mismatch(self) -> None:
        bad_prom = list(_DATASHEET_PROM)
        bad_prom[0] = 0x6000
        fake = FakeMS5611Bus(bad_prom, 0, 0)
        with patch_smbus(fake):
            self.assertIsNone(sensors.read_ms5611(1, 0x76, enabled=True))

    def test_read_ms5611_disabled_returns_none(self) -> None:
        self.assertIsNone(sensors.read_ms5611(1, 0x76, enabled=False))


# ---------------------------------------------------------------------------
# GY25 parser / framing
# ---------------------------------------------------------------------------


class GY25ParserTests(unittest.TestCase):
    def test_parses_positive_and_negative_angles(self) -> None:
        frame = bytes([0xAA, 0x00, 0x64, 0x00, 0xC8, 0xFF, 0x38, 0x55])
        self.assertEqual(
            sensors._gy25_parse_frame(frame),
            {"yaw": 1.0, "pitch": 2.0, "roll": -2.0},
        )

    def test_rejects_bad_length(self) -> None:
        self.assertIsNone(sensors._gy25_parse_frame(bytes([0xAA, 0x00, 0x00, 0x55])))

    def test_rejects_bad_preamble_or_terminator(self) -> None:
        self.assertIsNone(
            sensors._gy25_parse_frame(bytes([0x00, 0x00, 0x64, 0x00, 0xC8, 0xFF, 0x38, 0x55]))
        )
        self.assertIsNone(
            sensors._gy25_parse_frame(bytes([0xAA, 0x00, 0x64, 0x00, 0xC8, 0xFF, 0x38, 0x00]))
        )

    def test_next_frame_skips_garbage_and_false_preamble(self) -> None:
        buffer = bytearray(b"\x00\x01\xAA\x00\x64\x00\xC8\xFF\x38\x00\xAA\x00\x01\x00\x02\x00\x03\x55")
        result = sensors._gy25_next_frame(buffer)
        self.assertEqual(result, {"yaw": 0.01, "pitch": 0.02, "roll": 0.03})

    def test_next_frame_waits_for_partial_frame(self) -> None:
        buffer = bytearray(b"\x00\xAA\x00\x64")
        self.assertIsNone(sensors._gy25_next_frame(buffer))
        self.assertEqual(bytes(buffer), b"\xAA\x00\x64")


class GY25ReadTests(unittest.TestCase):
    def test_disabled_device_returns_none(self) -> None:
        self.assertIsNone(sensors.read_gy25("", 115200))

    def test_reads_a_full_frame(self) -> None:
        port = FakeSerialPort(
            [b"\xaa", b"\x00", b"\x64", b"\x00", b"\xc8", b"\xff", b"\x38", b"\x55"]
        )
        with patch_serial(port):
            result = sensors.read_gy25("/dev/serial0", 115200)
        self.assertEqual(result, {"yaw": 1.0, "pitch": 2.0, "roll": -2.0})
        self.assertTrue(port.closed)

    def test_returns_none_without_full_frame(self) -> None:
        port = FakeSerialPort([b"\xaa", b"\x00"])
        step = {"t": 0.0}

        def clock() -> float:
            step["t"] += 0.1
            return step["t"]

        with patch_serial(port), patch.object(sensors.time, "monotonic", side_effect=clock):
            result = sensors.read_gy25("/dev/serial0", 115200)
        self.assertIsNone(result)
        self.assertTrue(port.closed)


class SensorPayloadTests(unittest.TestCase):
    def test_read_sensors_degrades_when_hardware_missing(self) -> None:
        with patch.object(sensors, "read_gy25", return_value=None), patch.object(
            sensors, "read_ms5611", return_value=None
        ):
            payload = sensors.read_sensors("/dev/serial0", 115200, 1, 0x76, False)
        self.assertEqual(payload, {"imu": None, "pressure": None})

    def test_read_sensors_never_raises_on_exception(self) -> None:
        with patch.object(sensors, "read_gy25", side_effect=RuntimeError("boom")), patch.object(
            sensors, "read_ms5611", side_effect=RuntimeError("boom")
        ):
            payload = sensors.read_sensors("/dev/serial0", 115200, 1, 0x76, True)
        self.assertEqual(payload, {"imu": None, "pressure": None})


if __name__ == "__main__":
    unittest.main()
