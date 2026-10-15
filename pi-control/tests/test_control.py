import io
import json
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from core import SSH, service_command
import remote_probe
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'Pi 3'))
import sensors


class ControlTests(unittest.TestCase):
    def test_reject_injection_and_unknown_action(self):
        for unit in ['foo.service; reboot', '$(id).service', '-foo.service', 'foo.service\nreboot']:
            with self.assertRaises(ValueError):
                service_command('start', unit)
        with self.assertRaises(ValueError):
            service_command('kill', 'foo.service')

    def test_protect_connectivity(self):
        for unit in ['ssh.service', 'tailscaled.service', 'NetworkManager.service', 'ssh@session.service']:
            for action in ['stop', 'restart', 'disable']:
                with self.assertRaises(ValueError):
                    service_command(action, unit)
        self.assertIn('journalctl', service_command('logs', 'ssh.service'))

    def test_transport_rejects_host_options(self):
        with self.assertRaises(ValueError):
            SSH('-oProxyCommand=x', 'pi').argv()
        args = SSH('100.100.10.10', 'pi').argv()
        self.assertIn('StrictHostKeyChecking=yes', args)
        self.assertIn('BatchMode=yes', args)

    def test_disabled_units_not_missing(self):
        replies = [{'ok': True, 'text': 'live.service loaded active running Live'},
                   {'ok': True, 'text': 'live.service enabled enabled\nstopped.service disabled enabled'}]
        with patch.object(remote_probe, 'run', side_effect=replies):
            rows = remote_probe.services()['rows']
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[1][1], 'not-loaded')
        self.assertEqual(rows[1][3], 'disabled')

    def test_failed_service_inventory_is_not_empty_success(self):
        with patch.object(remote_probe, 'run', return_value={'ok': False, 'text': 'denied'}):
            self.assertEqual(len(remote_probe.services()['errors']), 2)

    def test_missing_stale_and_malformed_telemetry(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / 'data.json'
            self.assertEqual(remote_probe.telemetry(str(p))['state'], 'unavailable')
            p.write_text('{')
            self.assertEqual(remote_probe.telemetry(str(p))['state'], 'unavailable')
            p.write_text(json.dumps({'timestamp': time.time()-60, 'devices': {}}))
            self.assertEqual(remote_probe.telemetry(str(p))['state'], 'stale')
            p.write_text(json.dumps({'timestamp': time.time(), 'devices': {}}))
            self.assertEqual(remote_probe.telemetry(str(p))['state'], 'fresh')

    def test_publisher_uses_real_sample_and_does_not_break_on_io_error(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / 'telemetry.json'
            with patch.dict('os.environ', {'PI_CONTROL_TELEMETRY_PATH': str(p)}):
                sensors._publish_telemetry({'imu': None, 'pressure': {'pressure_pa': 101325}})
            data = json.loads(p.read_text())
            self.assertIsNone(data['devices']['imu'])
            self.assertEqual(data['devices']['pressure']['pressure_pa'], 101325)
            self.assertEqual(p.stat().st_mode & 0o777, 0o640)
            self.assertFalse(list(Path(directory).glob('.telemetry-*')))
            with patch.dict('os.environ', {'PI_CONTROL_TELEMETRY_PATH': str(p / 'missing')}):
                sensors._publish_telemetry({})

    def test_record_quotes_device_and_limits_duration(self):
        with patch.object(SSH, 'execute', return_value=b'wav') as execute:
            SSH('pi', 'pi').record('default; reboot', 5, 16000)
            self.assertIn("'default; reboot'", execute.call_args.args[0])
            self.assertIn('timeout', execute.call_args.args[0])
        with self.assertRaises(ValueError):
            SSH('pi', 'pi').record('default', 500, 16000)

    def test_ssh_reports_failure_and_timeout(self):
        import subprocess
        result = subprocess.CompletedProcess([], 255, b'', b'Permission denied')
        with patch('core.subprocess.run', return_value=result):
            with self.assertRaisesRegex(RuntimeError, 'Permission denied'):
                SSH('pi', 'pi').execute('uptime')
        with patch('core.subprocess.run', side_effect=subprocess.TimeoutExpired('ssh', 1)):
            with self.assertRaises(subprocess.TimeoutExpired):
                SSH('pi', 'pi').execute('uptime')


if __name__ == '__main__':
    unittest.main()
