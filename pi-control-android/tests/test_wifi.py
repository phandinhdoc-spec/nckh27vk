import importlib.util
import json
import os
from pathlib import Path
import stat
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('remote_wifi', ROOT / 'remote_wifi.py')
wifi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wifi)


class WiFiTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.adapter = wifi.DietPiWiFi(self.root)
        for path in (self.adapter.db, self.adapter.wpa, self.adapter.settings, self.adapter.helper):
            path.parent.mkdir(parents=True, exist_ok=True)
        self.adapter.settings.write_text('AUTO_SETUP_NET_WIFI_COUNTRY_CODE=VN\n')
        # A minimal native-format generator; executes the actual adapter's bash
        # subprocess and sources the generated DB, exercising shell quoting.
        self.adapter.helper.write_text('''#!/bin/bash
set -e
readonly MAX_SSID_SLOTS=5
Wifi_Db_Apply() { :; }
. "''' + str(self.adapter.db) + '''"
{
 echo country=VN
 echo 'ctrl_interface=DIR=/run/wpa_supplicant GROUP=netdev'
 echo update_config=1
 for i in 0 1 2 3 4; do
   if [[ -n "${aWIFI_SSID[$i]}" ]]; then
     echo 'network={'
     printf 'ssid="%s"\\nscan_ssid=1\\nkey_mgmt=%s\\n' "${aWIFI_SSID[$i]}" "${aWIFI_KEYMGR[$i]}"
     if [[ ${aWIFI_KEYMGR[$i]} == WPA-PSK ]]; then printf 'psk=%s\\n' "${aWIFI_KEY[$i]}"; fi
     echo '}'
   fi
 done
} > "''' + str(self.adapter.wpa) + '''"
chmod 600 "''' + str(self.adapter.db) + '" "' + str(self.adapter.wpa) + '"\n')
        self.slots = [wifi.empty_slot() for _ in range(5)]
        self.slots[0].update(SSID='Home', KEY='a'*64)
        self.set_slots(self.slots)

    def tearDown(self):
        self.temp.cleanup()

    def set_slots(self, slots):
        self.adapter.db.write_bytes(wifi.serialize(slots))
        self.adapter.generate()

    def save(self, **overrides):
        request = {'ssid': 'Second WiFi', 'password': '12345678', 'security': 'WPA-PSK',
                   'revision': self.adapter.status()['revision']}
        request.update(overrides)
        return self.adapter.save(request)

    def test_save_persistent_keeps_existing_masks_password_and_does_not_reload(self):
        before = self.adapter.db.read_bytes()
        with patch.object(self.adapter, 'reload', side_effect=AssertionError('must not reload')):
            result = self.save()
        self.assertEqual([n['ssid'] for n in result['networks']], ['Home', 'Second WiFi'])
        self.assertNotIn('12345678', self.adapter.db.read_text())
        self.assertNotIn('12345678', json.dumps(result))
        self.assertNotIn('a'*64, json.dumps(result))
        self.assertEqual((Path(result['backup']) / 'dietpi-wifi.db').read_bytes(), before)
        self.assertEqual(stat.S_IMODE(self.adapter.db.stat().st_mode), 0o600)
        self.assertEqual(stat.S_IMODE(Path(result['backup']).stat().st_mode), 0o700)
        # A new adapter simulates reading after restart.
        self.assertEqual(len(wifi.DietPiWiFi(self.root).status()['networks']), 2)

    def test_psk_known_vector(self):
        self.assertEqual(wifi.psk('IEEE', 'password'), 'f42c6fc52df0ebef9ebb4b90b38a5f902e83fe1b135a70e23aed762e9710a12e')

    def test_open_and_explicit_update(self):
        with self.assertRaisesRegex(ValueError, 'SSID đã lưu'):
            self.save(ssid='Home')
        result = self.save(ssid='Home', replace=True, password='newpassword')
        self.assertEqual(len(result['networks']), 1)
        self.save(ssid='Guest', security='NONE', password='')
        self.assertEqual(self.adapter.status()['networks'][1]['security'], 'NONE')

    def test_full_does_not_evict(self):
        for i in range(5):
            self.slots[i].update(SSID=f'Network{i}', KEY='b'*64)
        self.set_slots(self.slots)
        before = self.adapter.db.read_bytes()
        with self.assertRaisesRegex(ValueError, 'Đã đầy'):
            self.save()
        self.assertEqual(self.adapter.db.read_bytes(), before)

    def test_revision_conflict(self):
        old = self.adapter.status()['revision']
        self.adapter.db.write_bytes(self.adapter.db.read_bytes() + b'# changed\n')
        with self.assertRaisesRegex(ValueError, 'đã đổi'):
            self.save(revision=old)

    def test_rollback_on_generator_failure(self):
        before = (self.adapter.db.read_bytes(), self.adapter.wpa.read_bytes())
        def failure():
            self.adapter.wpa.write_text('broken')
            raise RuntimeError('synthetic-secret')
        with patch.object(self.adapter, 'generate', side_effect=failure):
            with self.assertRaisesRegex(ValueError, 'khôi phục') as caught:
                self.save()
        self.assertNotIn('synthetic-secret', str(caught.exception))
        self.assertEqual((self.adapter.db.read_bytes(), self.adapter.wpa.read_bytes()), before)

    def test_custom_config_and_unfinished_boot_refused(self):
        original = self.adapter.wpa.read_bytes()
        self.adapter.wpa.write_bytes(original + b'ap_scan=2\n')
        with self.assertRaisesRegex(ValueError, 'không khớp'):
            self.save()
        self.adapter.wpa.write_bytes(original)
        (self.root / 'boot/dietpi-wifi.txt').write_text('pending')
        with self.assertRaisesRegex(ValueError, 'khởi tạo'):
            self.save()

    def test_literal_shell_characters_and_quotes_never_execute(self):
        ssid = "O'Brien $(id);#"
        self.save(ssid=ssid, password="a'$(id);#bc")
        self.assertEqual(self.adapter.status()['networks'][1]['ssid'], ssid)
        parsed = wifi.parse_db(self.adapter.db.read_bytes())
        self.assertEqual(parsed[1]['KEY'], wifi.psk(ssid, "a'$(id);#bc"))

    def test_invalid_ssid_and_password_do_not_write(self):
        before = self.adapter.db.read_bytes()
        for ssid in ('', 'x'*33, 'a\nb', 'a"b', 'a\\b', 'ế'*12):
            with self.assertRaises(ValueError):
                self.save(ssid=ssid)
        for password in ('short', 'x'*64, 'password\n'):
            with self.assertRaises(ValueError):
                self.save(password=password)
        self.assertEqual(self.adapter.db.read_bytes(), before)

    def test_db_unknown_commands_not_executed(self):
        self.adapter.db.write_text('touch /tmp/should-not-execute\n')
        with self.assertRaisesRegex(ValueError, 'định dạng'):
            self.adapter.status()

    def test_reload_separate_confirmed_and_delayed(self):
        (self.root / 'sys/class/net/wlan0/wireless').mkdir(parents=True)
        with self.assertRaisesRegex(ValueError, 'xác nhận'):
            self.adapter.reload({})
        with patch.object(wifi.shutil, 'which', return_value='/sbin/wpa_cli'), patch.object(wifi.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, b'PONG\n')), patch.object(wifi.subprocess, 'Popen') as popen:
            result = self.adapter.reload({'confirm': True, 'revision': self.adapter.status()['revision']})
        self.assertIn('3 giây', result['message'])
        self.assertIn('time.sleep(3)', popen.call_args.args[0][2])
        self.assertTrue(popen.call_args.kwargs['start_new_session'])
        self.assertNotIn('12345678', repr(popen.call_args))


if __name__ == '__main__':
    unittest.main()
