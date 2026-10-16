import http.client
import importlib.util
import json
from pathlib import Path
import sys
import threading
import unittest
from unittest.mock import Mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('web_server', ROOT / 'web_server.py')
web = importlib.util.module_from_spec(spec)
spec.loader.exec_module(web)


class WebTest(unittest.TestCase):
    def setUp(self):
        self.server = web.make_server({'origin': 'https://pi.example.ts.net',
            'allowed_users': ['owner@example.com'], 'key': '/tmp/key', 'telemetry': '/tmp/data.json'}, 0)
        self.server.state.client = Mock()
        self.server.state.client.probe.return_value = {'hostname': 'test-pi'}
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()

    def request(self, path='/', method='GET', body=None, headers=None):
        h = {'X-Forwarded-Host': 'pi.example.ts.net', 'X-Forwarded-Proto': 'https',
             'Tailscale-User-Login': 'owner@example.com', 'X-Pi-Control': '1',
             'Origin': self.server.origin}
        h.update(headers or {})
        c = http.client.HTTPConnection('127.0.0.1', self.server.server_port, timeout=3)
        c.request(method, path, json.dumps(body or {}) if method == 'POST' else None, h)
        r = c.getresponse()
        result = r.status, r.read()
        c.close()
        return result

    def test_shell_and_manifest(self):
        status, body = self.request()
        self.assertEqual(status, 200)
        self.assertIn(b'manifest.webmanifest', body)
        self.assertEqual(self.request('/manifest.webmanifest')[0], 200)
        self.assertTrue(self.request('/icon.png')[1].startswith(b'\x89PNG'))

    def test_identity_required_for_everything(self):
        for path in ('/', '/app.js', '/recording.wav', '/api/config', '/manifest.webmanifest'):
            self.assertEqual(self.request(path, headers={'Tailscale-User-Login': ''})[0], 403)
            self.assertEqual(self.request(path, headers={'Tailscale-User-Login': 'other@example.com'})[0], 403)
        self.assertEqual(self.request(headers={'Tailscale-Funnel-Request': '?1'})[0], 403)
        self.assertEqual(self.request(headers={'X-Forwarded-Host': 'evil.test'})[0], 403)

    def test_no_key_or_token_in_config(self):
        status, body = self.request('/api/config')
        self.assertEqual(status, 200)
        data = json.loads(body)
        self.assertTrue(data['hosted'])
        self.assertNotIn('key', data['config'])
        self.assertEqual(self.request('/unlock?token=' + self.server.state.token)[0], 404)

    def test_post_origin_and_identity(self):
        for headers in ({'Origin': 'https://evil.test'}, {'X-Pi-Control': ''},
                        {'Tailscale-User-Login': 'intruder'}):
            self.assertEqual(self.request('/api/command', 'POST', {'command': 'id'}, headers)[0], 403)
        self.server.state.client.execute.assert_not_called()

    def test_fixed_ssh_and_existing_dispatch(self):
        original = self.server.state.client
        self.assertEqual(self.request('/api/connect', 'POST', {'host': 'evil.test', 'key': '/etc/shadow'})[0], 200)
        self.assertIs(self.server.state.client, original)
        self.assertEqual(self.server.state.config['host'], '127.0.0.1')
        original.execute.return_value = b'{"entries": []}'
        self.assertEqual(self.request('/api/files', 'POST', {'action': 'list', 'path': '/root'})[0], 200)
        self.assertIn('python3', original.execute.call_args.args[0])
        self.assertEqual(self.request('/api/disconnect', 'POST')[0], 400)

    def test_pinned_ssh(self):
        argv = web.LocalSSH('127.0.0.1', 'root', 22, '/data/key').argv()
        self.assertIn('StrictHostKeyChecking=yes', argv)
        self.assertIn('UserKnownHostsFile=/data/known_hosts', argv)
        self.assertEqual(argv[-1], 'root@127.0.0.1')


if __name__ == '__main__':
    unittest.main()
