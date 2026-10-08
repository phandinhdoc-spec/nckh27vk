import importlib.util
import pathlib
import struct
import subprocess
import unittest
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]

def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

clock = load('clock_sync')
ready = load('tailscale_ready')


class StartupTests(unittest.TestCase):
    def packet(self):
        packet = bytearray(48)
        packet[0], packet[1] = 0x24, 2
        packet[24:32] = b'12345678'
        packet[40:48] = struct.pack('!II', 1791432000 + clock.EPOCH, 0)
        return packet

    def test_valid_reply(self):
        self.assertAlmostEqual(clock.decode_reply(self.packet(), b'12345678', .2), 1791432000.1)

    def test_reject_bad_origin_unsynced_kod_and_short_reply(self):
        for offset, value in [(0, 0xe4), (0, 0x23), (1, 0), (24, 0)]:
            packet = self.packet()
            packet[offset] = value
            with self.assertRaises(ValueError):
                clock.decode_reply(packet, b'12345678', .2)
        with self.assertRaises(ValueError):
            clock.decode_reply(b'', b'12345678', .2)

    def test_consensus_adjusts_elapsed_time(self):
        self.assertEqual(clock.consensus([(100, 10), (104, 14)], 20), 110)
        with self.assertRaises(ValueError):
            clock.consensus([(100, 10), (200, 10)], 20)
        with self.assertRaises(ValueError):
            clock.consensus([(100, 10)], 20)

    def test_date_not_run_without_agreement(self):
        with patch.object(clock, 'query', side_effect=OSError('offline')), patch.object(clock.subprocess, 'run') as run:
            with self.assertRaises(ValueError):
                clock.attempt()
            run.assert_not_called()

    def test_sets_date_only_after_samples_and_propagates_error(self):
        with patch.object(clock, 'query', return_value=(1791432000, 10)), patch.object(clock.time, 'monotonic', return_value=11), patch.object(clock.subprocess, 'run') as run:
            clock.attempt()
            self.assertEqual(run.call_args.args[0], ['/usr/bin/date', '-u', '-s', '@1791432001.000'])
            run.side_effect = subprocess.CalledProcessError(1, 'date')
            with self.assertRaises(subprocess.CalledProcessError):
                clock.attempt()

    def test_tailscale_requires_running_ip_and_online(self):
        state = {'BackendState': 'Running', 'TailscaleIPs': ['100.1.2.3'], 'Self': {'Online': True}}
        self.assertTrue(ready.ready(state))
        for key, value in [('BackendState', 'NeedsLogin'), ('TailscaleIPs', []), ('Self', {'Online': False})]:
            self.assertFalse(ready.ready({**state, key: value}))

    def test_boot_order_and_retry(self):
        app = (ROOT / 'pi-app.service').read_text()
        self.assertIn('After=network-online.target tailscaled.service', app)
        self.assertIn('ExecStartPre=/usr/bin/python3 -u /usr/local/lib/pi-startup/tailscale_ready.py', app)
        self.assertIn('Restart=always', app)
        self.assertIn('clock_sync.py', (ROOT / '20-pi-clock.conf').read_text())


if __name__ == '__main__':
    unittest.main()
