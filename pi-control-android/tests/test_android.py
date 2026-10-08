import http.client
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('android_server', ROOT / 'server.py')
server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(server)


class AndroidTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.web = server.make_server(0, True, Path(cls.temp.name)/'config.json')
        cls.thread = threading.Thread(target=cls.web.serve_forever, daemon=True)
        cls.thread.start()
        cls.cookie = 'pi_session=' + cls.web.state.token

    @classmethod
    def tearDownClass(cls):
        cls.web.shutdown()
        cls.web.server_close()
        cls.thread.join()
        cls.temp.cleanup()

    def request(self, method, path, data=None, auth=True, headers=None):
        connection = http.client.HTTPConnection('127.0.0.1', self.web.server_port)
        request_headers = {'X-Pi-Control': '1'}
        if auth:
            request_headers['Cookie'] = self.cookie
        request_headers.update(headers or {})
        connection.request(method, path, json.dumps(data or {}) if method == 'POST' else None, request_headers)
        response = connection.getresponse()
        result = response.status, dict(response.getheaders()), response.read()
        connection.close()
        return result

    def test_local_auth_and_unlock(self):
        self.assertEqual(self.request('GET', '/', auth=False)[0], 401)
        code, headers, _ = self.request('GET', '/unlock?token='+self.web.state.token, auth=False)
        self.assertEqual(code, 303)
        self.assertIn('HttpOnly', headers['Set-Cookie'])
        self.assertEqual(self.request('GET', '/')[0], 200)

    def test_rebinding_and_cross_origin_rejected(self):
        self.assertEqual(self.request('GET', '/', headers={'Host': 'evil.test'})[0], 403)
        self.assertEqual(self.request('POST', '/api/snapshot', headers={'Origin': 'https://evil.test'})[0], 403)
        self.assertEqual(self.request('POST', '/api/snapshot', auth=False)[0], 403)
        self.assertEqual(self.request('POST', '/api/snapshot', headers={'X-Pi-Control': ''})[0], 403)

    def test_demo_no_network_and_no_fake_recording(self):
        with patch.object(server.SSH, 'execute', side_effect=AssertionError('Network called')):
            self.assertEqual(self.request('POST', '/api/snapshot')[0], 200)
            self.assertEqual(self.request('POST', '/api/command', {'command': 'uptime'})[0], 200)
            self.assertEqual(self.request('POST', '/api/record', {'device': 'default', 'seconds': 5, 'rate': 16000})[0], 400)

    def test_protect_connectivity_and_quote_validation(self):
        self.assertEqual(self.request('POST', '/api/service', {'action': 'stop', 'unit': 'tailscaled.service'})[0], 400)
        self.assertEqual(self.request('POST', '/api/service', {'action': 'start', 'unit': 'x.service; reboot'})[0], 400)

    def test_busy_requests_rejected(self):
        self.web.state.lock.acquire()
        try:
            self.assertEqual(self.request('POST', '/api/snapshot')[0], 409)
        finally:
            self.web.state.lock.release()

    def test_static_paths_are_allowlisted(self):
        self.assertEqual(self.request('GET', '/../server.py')[0], 404)
        self.assertEqual(self.request('GET', '/recording.wav')[0], 404)

    def test_root_service_without_sudo(self):
        state = server.State(config_path=Path(self.temp.name)/'another.json')
        state.client = server.SSH('pi', 'root')
        with patch.object(server.SSH, 'execute', return_value=b'') as execute:
            state.dispatch('/api/service', {'action': 'start', 'unit': 'pi-app.service'})
            self.assertEqual(execute.call_args.args[0], 'systemctl start pi-app.service')

    def test_file_api_roundtrip_and_auth(self):
        import subprocess
        import shlex
        path = Path(self.temp.name) / 'settings.env'
        path.write_text('old value')
        def execute(command, stdin=None, timeout=40):
            return subprocess.run(shlex.split(command), input=stdin, capture_output=True,
                                  timeout=timeout, check=True).stdout
        with patch.object(self.web.state, 'demo', False), patch.object(self.web.state, 'client', server.SSH('pi', 'root')), patch.object(server.SSH, 'execute', side_effect=execute):
            request = {'action': 'read', 'path': str(path)}
            self.assertEqual(self.request('POST', '/api/files', request, auth=False)[0], 403)
            code, _, body = self.request('POST', '/api/files', request)
            self.assertEqual(code, 200)
            content = 'Tiếng Việt\n' * 5000
            write = {'action': 'write', 'path': str(path), 'revision': json.loads(body)['revision'], 'content': content}
            code, _, body = self.request('POST', '/api/files', write)
            self.assertEqual(code, 200, body)
            self.assertEqual(path.read_text(), content)
            self.assertEqual(Path(json.loads(body)['backup']).read_text(), 'old value')

    def test_disconnect_removes_audio_and_connection(self):
        state = server.State(config_path=Path(self.temp.name)/'another.json')
        state.client = server.SSH('pi', 'root')
        state.recording = b'private recording'
        state.dispatch('/api/disconnect', {})
        self.assertIsNone(state.client)
        self.assertIsNone(state.recording)


if __name__ == '__main__':
    unittest.main()
