from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DeploymentArtifactTests(unittest.TestCase):
    def test_setup_contains_required_bluealsa__a2dp_and_mic(self) -> None:
        script = (ROOT / "setup_pi2w.sh").read_text(encoding="utf-8")
        self.assertIn("bluez-alsa-utils", script)
        self.assertIn("libasound2-plugin-bluez", script)
        # Button/GPIO da bo: mic USB mo lien tuc + VAD cuc bo, can lame de ma hoa MP3.
        self.assertNotIn("python3-rpi.gpio", script)
        self.assertIn("lame", script)
        # Chi giu A2DP playback cho loa tai nghe; khong bat SCO capture.
        self.assertIn('options="-p a2dp-source"', script)
        self.assertIn("/etc/systemd/system/bluealsa.service.d/override.conf", script)
        self.assertIn("ExecStart=/usr/bin/bluealsa -S %s", script)
        self.assertNotIn('--codec=-mSBC', script)
        self.assertNotIn('--codec=-LC3-SWB', script)
        self.assertNotIn("PROFILE=sco", script)
        self.assertNotIn('>/etc/default/bluez-alsa', script)
        self.assertNotIn('"E0:1A:03:08:A9:7C"', script)
        self.assertIn("04:60:61:EF:78:22", script)
        self.assertIn("thu toi da 2 lan", script)
        self.assertIn("for attempt in 1 2; do", script)
        self.assertIn("tiep tuc cai dat, runtime se dung loa MAX98357A", script)
        self.assertIn('Tai nghe chua ket noi; bo qua A2DP test.', script)
        self.assertNotIn("for attempt in 1 2 3 4 5; do", script)
        self.assertNotIn('"41:42:1B:2D:3E:26"', script)
        main = script[script.index("main() {") :]
        self.assertLess(main.index("configure_camera_boot"), main.index("configure_max98357a"))
        self.assertLess(main.index("configure_max98357a"), main.index("check_camera"))
        self.assertIn("bo qua camera test trong lan nay", script)
        self.assertIn('fail "Camera chup that bai', script)

    def test_setup_configures_sensors_dependencies_and_wifi_fallback(self) -> None:
        script = (ROOT / "setup_pi2w.sh").read_text(encoding="utf-8")
        # UART/I2C boot config for GY25/MS5611.
        self.assertIn("enable_uart=1", script)
        self.assertIn("dtparam=i2c_arm=on", script)
        self.assertIn("configure_sensor_boot", script)
        # Python sensor dependencies.
        self.assertIn("python3-serial", script)
        self.assertIn("python3-smbus2", script)
        # sensors.py must be deployed or the service cannot import it.
        self.assertIn('"${SCRIPT_DIR}/sensors.py"', script)
        # Serial + I2C group access for the service user.
        self.assertIn("dialout", script)
        self.assertIn("i2c", script)
        # WiFi fallback must be idempotent, permission-safe, and only touch
        # wpa_supplicant when it is the active network manager.
        self.assertIn("systemctl is-active --quiet wpa_supplicant", script)
        self.assertIn("chmod 0600", script)
        self.assertIn('priority=-5', script)
        main = script[script.index("main() {") :]
        self.assertLess(main.index("configure_max98357a"), main.index("configure_sensor_boot"))
        self.assertLess(main.index("configure_sensor_boot"), main.index("check_camera"))

    def test_systemd_unit_has_production_basics(self) -> None:
        unit = (ROOT / "thiennhan.service").read_text(encoding="utf-8")
        for setting in (
            "User=thiennhan",
            "WorkingDirectory=/opt/thiennhan",
            "EnvironmentFile=/opt/thiennhan/.env",
            "Restart=on-failure",
            "Requires=bluetooth.service bluealsa.service",
        ):
            self.assertIn(setting, unit)

    def test_play_audio_routes_mp3_and_wav(self) -> None:
        script = ROOT / "play-audio"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            log = root / "args.log"
            for command in ("mpg123", "aplay"):
                executable = bin_dir / command
                executable.write_text(
                    '#!/usr/bin/env bash\nprintf "%s\\n" "$0" "$@" > "$PLAY_AUDIO_LOG"\n',
                    encoding="utf-8",
                )
                executable.chmod(0o755)

            environment = os.environ.copy()
            environment["PATH"] = f"{bin_dir}:{environment['PATH']}"
            environment["PLAY_AUDIO_LOG"] = str(log)
            environment["MAX98357A_DEVICE"] = "hw:MAX,0"

            mp3 = root / "response.mp3"
            mp3.write_bytes(b"ID3")
            subprocess.run([str(script), str(mp3)], check=True, env=environment)
            mp3_args = log.read_text(encoding="utf-8")
            self.assertIn("mpg123", mp3_args)
            self.assertIn("-a\nhw:MAX,0", mp3_args)

            wav = root / "sample.wav"
            wav.write_bytes(b"RIFF")
            subprocess.run([str(script), str(wav)], check=True, env=environment)
            wav_args = log.read_text(encoding="utf-8")
            self.assertIn("aplay", wav_args)
            self.assertIn("bluealsa:DEV=04:60:61:EF:78:22,PROFILE=a2dp", wav_args)


if __name__ == "__main__":
    unittest.main()
