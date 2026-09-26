"""Lightweight sensor readers for the Thien Nhan Pi device.

Two sensors added to the hardware (2026-09-25):
- GY25 (MPU6050 module in UART angle-output mode): yaw/pitch/roll over a TTL
  serial port (/dev/serial0, 115200 baud). Each frame is 8 bytes:
      Byte0 = 0xAA (preamble)
      Byte1..2 = yaw   (high, low)   signed 16-bit
      Byte3..4 = pitch (high, low)   signed 16-bit
      Byte5..6 = roll  (high, low)   signed 16-bit
      Byte7 = 0x55 (frame end)
    Angle value = raw * 0.01 degrees. There is NO checksum, so framing relies on
    the 0xAA preamble + 0x55 terminator.
- GY63 (MS5611-01BA03 barometer): pressure/temperature/altitude over I2C
  (bus 1, address 0x76). Uses the standard MS5611 PROM + OSR conversion
  protocol with first- and second-order temperature compensation per the
  datasheet, plus PROM CRC-4 verification.

The device NEVER runs heavy AI. These readers are lightweight, fail-tolerantly
return None (graceful Degrade) when hardware is missing, and never raise into
the application loop. Sensor payloads ride along with requests to the Mac
server so the server can reason about fall/altitude.
"""

from __future__ import annotations

import time
from typing import Any, Optional


# ---------------------------------------------------------------------------
# GY25 (MPU6050 in UART angle mode)
# ---------------------------------------------------------------------------

_GY25_PREAMBLE = 0xAA
_GY25_TERMINATOR = 0x55
_GY25_FRAME_LEN = 8
_GY25_ANGLE_SCALE = 0.01  # raw int16 units are hundredths of a degree
_GY25_READ_TIMEOUT = 0.05  # seconds to block per read while waiting for a byte
_GY25_MAX_FRAMES_WAIT = 0.3  # total seconds to wait for one full frame


def _gy25_parse_frame(frame: bytes) -> Optional[dict[str, float]]:
    """Parse one 8-byte GY25 frame into {yaw, pitch, roll} degrees.

    Returns None if the frame does not carry the expected preamble/terminator.
    """
    if len(frame) != _GY25_FRAME_LEN:
        return None
    if frame[0] != _GY25_PREAMBLE or frame[-1] != _GY25_TERMINATOR:
        return None
    values: dict[str, float] = {}
    for index, name in enumerate(("yaw", "pitch", "roll")):
        offset = 1 + index * 2
        raw = (frame[offset] << 8) | frame[offset + 1]
        if raw >= 0x8000:
            raw -= 0x10000
        values[name] = raw * _GY25_ANGLE_SCALE
    return values


def _gy25_next_frame(buffer: bytearray) -> Optional[dict[str, float]]:
    """Extract and parse the first complete GY25 frame in ``buffer``.

    Consumes bytes up to and including the frame when one is accepted; drops
    garbage before a preamble and false (bad-terminator) frames. Returns None
    and keeps the remainder when no complete valid frame is available yet.
    """
    while True:
        start = buffer.find(_GY25_PREAMBLE)
        if start < 0:
            del buffer[:]
            return None
        if start > 0:
            del buffer[:start]
        if len(buffer) < _GY25_FRAME_LEN:
            return None  # partial frame; wait for more bytes
        frame = bytes(buffer[:_GY25_FRAME_LEN])
        parsed = _gy25_parse_frame(frame)
        del buffer[:_GY25_FRAME_LEN]
        if parsed is not None:
            return parsed
        # False preamble; keep scanning the remaining bytes.


def read_gy25(device: str, baud: int) -> Optional[dict[str, float]]:
    """Read one GY25 attitude sample, or None if the sensor is unavailable.

    device may be "" to disable the sensor entirely (returns None without
    importing serial). Reads are bounded: each blocking read waits at most
    _GY25_READ_TIMEOUT and the whole attempt is capped at _GY25_MAX_FRAMES_WAIT
    so a missing sensor never stalls the device loop.
    """
    if not device:
        return None
    try:
        import serial
    except ImportError:
        return None

    try:
        port = serial.Serial(device, baud, timeout=_GY25_READ_TIMEOUT)
    except (OSError, ValueError):
        return None

    try:
        deadline = time.monotonic() + _GY25_MAX_FRAMES_WAIT
        buffer = bytearray()
        while time.monotonic() < deadline:
            chunk = port.read(1)
            if chunk:
                buffer.extend(chunk)
            parsed = _gy25_next_frame(buffer)
            if parsed is not None:
                return parsed
    finally:
        try:
            port.close()
        except Exception:
            pass
    return None


# ---------------------------------------------------------------------------
# GY63 (MS5611-01BA03) barometer
# ---------------------------------------------------------------------------

_MS5611_CMD_RESET = 0x1E
_MS5611_CMD_ADC_READ = 0x00
_MS5611_CMD_D1_4096 = 0x48  # pressure, OSR 4096
_MS5611_CMD_D2_4096 = 0x58  # temperature, OSR 4096
_MS5611_PROM_BASE = 0xA0
_MS5611_PROM_COUNT = 8
_MS5611_RESET_SLEEP = 0.003  # datasheet: >= 2.8 ms after reset
_MS5611_CONVERSION_SLEEP = 0.01  # datasheet: <= 9.04 ms for OSR 4096
_MS5611_REFERENCE_PRESSURE = 101325.0  # Pa at sea level


def _ms5611_crc4(prom: list[int]) -> int:
    """Compute the MS5611 PROM CRC-4 nibble (AN520 datasheet algorithm).

    The CRC covers the 16 PROM bytes with the CRC nibble (C0 bits 15:12) and
    the dummy C7 word both zeroed. Returns a 4-bit value (0..15).
    """
    words = list(prom)
    words[0] &= 0x0FFF  # zero the CRC nibble
    words[7] = 0  # C7 is a dummy word, excluded from the CRC
    remainder = 0
    for cnt in range(16):
        if cnt % 2 == 1:
            remainder ^= words[cnt >> 1] & 0x00FF
        else:
            remainder ^= words[cnt >> 1] >> 8
        for _ in range(8):
            if remainder & 0x8000:
                remainder = ((remainder << 1) ^ 0x3000) & 0xFFFF
            else:
                remainder = (remainder << 1) & 0xFFFF
    return (remainder >> 12) & 0x000F


class _MS5611:
    """MS5611 driver over smbus2. Raises OSError on hardware problems."""

    def __init__(self, bus: int, address: int) -> None:
        from smbus2 import SMBus

        self.address = address
        self._bus = SMBus(bus)
        self._prom: list[int] = [0] * _MS5611_PROM_COUNT
        try:
            self._read_prom()
        except Exception:
            self.close()
            raise

    def _read_prom(self) -> None:
        self._bus.write_byte(self.address, _MS5611_CMD_RESET)
        time.sleep(_MS5611_RESET_SLEEP)
        for index in range(_MS5611_PROM_COUNT):
            register = _MS5611_PROM_BASE + index * 2
            word = self._bus.read_word_data(self.address, register)
            # smbus2 read_word_data returns the device's two bytes little-endian;
            # the MS5611 PROM is big-endian, so swap back.
            self._prom[index] = ((word & 0xFF) << 8) | ((word >> 8) & 0xFF)
        stored_crc = (self._prom[0] >> 12) & 0x0F
        if _ms5611_crc4(self._prom) != stored_crc:
            raise OSError("MS5611 PROM CRC-4 không khớp; cảm biến lỗi hoặc dây hỏng.")

    def _read_adc_24(self) -> int:
        data = self._bus.read_i2c_block_data(self.address, _MS5611_CMD_ADC_READ, 3)
        return (data[0] << 16) | (data[1] << 8) | data[2]

    def sample(self) -> dict[str, float]:
        self._bus.write_byte(self.address, _MS5611_CMD_D1_4096)
        time.sleep(_MS5611_CONVERSION_SLEEP)
        d1 = self._read_adc_24()
        self._bus.write_byte(self.address, _MS5611_CMD_D2_4096)
        time.sleep(_MS5611_CONVERSION_SLEEP)
        d2 = self._read_adc_24()

        c1, c2, c3, c4, c5, c6 = self._prom[1:7]

        d_t = d2 - (c5 << 8)
        temp = 2000 + ((d_t * c6) >> 23)
        off = (c2 << 16) + ((c4 * d_t) >> 7)
        sens = (c1 << 15) + ((c3 * d_t) >> 8)

        # Second-order compensation below 20 degC (datasheet).
        if temp < 2000:
            t2 = (d_t * d_t) >> 31
            off2 = (5 * (temp - 2000) * (temp - 2000)) >> 1
            sens2 = (5 * (temp - 2000) * (temp - 2000)) >> 2
            if temp < -1500:  # very low temperature (< -15 degC)
                off2 += 7 * (temp + 1500) * (temp + 1500)
                sens2 += (11 * (temp + 1500) * (temp + 1500)) >> 1
            temp -= t2
            off -= off2
            sens -= sens2

        # Result is in 0.01 mbar units, which equals Pa (1 mbar = 100 Pa).
        pressure_pa = (((d1 * sens) >> 21) - off) >> 15
        temperature_c = temp / 100.0

        altitude_m = (
            44330.0 * (1.0 - (pressure_pa / _MS5611_REFERENCE_PRESSURE) ** (1.0 / 5.255))
            if pressure_pa > 0
            else 0.0
        )
        return {
            "pressure_pa": round(float(pressure_pa), 1),
            "temperature_c": round(temperature_c, 2),
            "altitude_m": round(altitude_m, 1),
        }

    def close(self) -> None:
        try:
            self._bus.close()
        except Exception:
            pass


def read_ms5611(bus: int, address: int, enabled: bool = True) -> Optional[dict[str, float]]:
    """Read pressure/temperature/altitude, or None when unavailable."""
    if not enabled:
        return None
    try:
        sensor = _MS5611(bus, address)
    except (OSError, ImportError):
        return None
    try:
        return sensor.sample()
    except OSError:
        return None
    finally:
        sensor.close()


# ---------------------------------------------------------------------------
# Combined payload helper
# ---------------------------------------------------------------------------


def read_sensors(
    gy25_device: str,
    gy25_baud: int,
    ms5611_bus: int,
    ms5611_addr: int,
    ms5611_enabled: bool,
) -> dict[str, Any]:
    """Build a compact sensor payload. Missing hardware becomes None values.

    Never raises: any sensor failure degrades to None so the device loop and the
    HTTP payload stay alive even when a sensor is unplugged or the bus is down.
    """
    payload: dict[str, Any] = {
        "imu": None,
        "pressure": None,
    }
    try:
        payload["imu"] = read_gy25(gy25_device, gy25_baud)
    except Exception:
        payload["imu"] = None
    try:
        payload["pressure"] = read_ms5611(ms5611_bus, ms5611_addr, ms5611_enabled)
    except Exception:
        payload["pressure"] = None
    return payload
