#!/usr/bin/env python3
"""Phone-local UI for the existing Pi Control OpenSSH backend (stdlib only)."""
import argparse
from http.cookies import SimpleCookie, CookieError
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import secrets
import shlex
import subprocess
import sys
import threading
import time
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / 'pi-control'))
from core import SSH, service_command

CONFIG = Path.home() / '.pi-control-android.json'
DEFAULTS = {'host': 'pi', 'user': 'root', 'port': 22, 'key': '',
            'telemetry': '/opt/thiennhan/history/telemetry.json'}


def demo_snapshot():
    return {'hostname': 'hieunga · DEMO', 'cpu_percent': 18.4, 'ram_percent': 42.1,
            'disk_percent': 28.6, 'temperature_c': 46.2, 'uptime_seconds': 7200,
            'services': {'rows': [['tailscaled.service', 'active', 'running', 'enabled', 'Tailscale'],
             ['pi-app.service', 'active', 'running', 'enabled', 'Ứng dụng Pi'],
             ['example.service', 'inactive', 'dead', 'disabled', 'Service minh họa']], 'errors': []},
            'telemetry': {'state': 'fresh', 'age_seconds': 0, 'data': {'devices': {
                'imu': {'roll_deg': 1.2, 'pitch_deg': -2.4},
                'distance': {'distance_mm': 530}, 'pressure': None}}}}


class State:
    def __init__(self, demo=False, config_path=CONFIG):
        self.config_path = config_path
        self.config = dict(DEFAULTS)
        try:
            saved = json.loads(config_path.read_text())
            if isinstance(saved, dict):
                self.config.update({k: saved[k] for k in DEFAULTS if k in saved})
        except (OSError, ValueError):
            pass
        self.token = secrets.token_urlsafe(32)
        self.client = None
        self.lock = threading.Lock()
        self.demo = demo
        self.recording = None

    def configure(self, data):
        config = {k: str(data.get(k, DEFAULTS[k])).strip() for k in DEFAULTS}
        config['port'] = int(config['port'])
        if not config['telemetry'] or len(config['telemetry']) > 512:
            raise ValueError('Đường dẫn telemetry không hợp lệ')
        client = SSH(config['host'], config['user'], config['port'], config['key'])
        client.argv()
        self.config, self.client, self.recording = config, client, None
        # No passwords or private key bytes are stored.
        fd = os.open(self.config_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, 'w') as stream:
            json.dump(config, stream)
        os.chmod(self.config_path, 0o600)
        return self.snapshot()

    def snapshot(self):
        if self.demo:
            return demo_snapshot()
        if self.client is None:
            raise ValueError('Chưa kết nối. Mở Cài đặt và nhập IP Tailscale hoặc alias SSH.')
        return self.client.probe('snapshot', self.config['telemetry'])

    def dispatch(self, route, data):
        if route == '/api/connect':
            return self.configure(data)
        if route == '/api/disconnect':
            self.client = None
            self.recording = None
            return {'message': 'Đã ngắt kết nối'}
        if route == '/api/snapshot':
            return self.snapshot()
        if not self.demo and self.client is None:
            raise ValueError('Chưa kết nối Pi')
        if route == '/api/files':
            if self.demo:
                raise ValueError('DEMO không truy cập file. Kết nối Pi để dùng.')
            script = (ROOT / 'remote_files.py').read_text()
            result = json.loads(self.client.execute(shlex.join(['python3', '-c', script]),
                stdin=json.dumps(data, ensure_ascii=False).encode(), timeout=40))
            if 'error' in result:
                raise ValueError(result['error'])
            return result
        if route == '/api/devices':
            if self.demo:
                return {'DEMO — không phải dữ liệu thật': {'ok': True, 'text': 'USB microphone\nI²C bus 1\nBluetooth: headphones'}}
            return self.client.probe('devices', self.config['telemetry'])
        if route == '/api/service':
            action, unit = data['action'], data['unit']
            command = service_command(action, unit)
            if self.demo:
                return {'message': f'DEMO: {action} {unit}; không gửi lệnh'}
            if self.config['user'] == 'root' and action != 'logs':
                command = shlex.join(shlex.split(command)[2:])  # root needs no sudo binary
            return {'message': self.client.execute(command).decode(errors='replace') or f'{action} {unit}: thành công'}
        if route == '/api/command':
            command = str(data['command']).strip()
            if not command or len(command) > 4000:
                raise ValueError('Lệnh trống hoặc vượt 4000 ký tự')
            if self.demo:
                return {'message': 'DEMO: lệnh chưa được thực thi'}
            wrapped = shlex.join(['timeout', '--signal=TERM', '--kill-after=2', '30', 'sh', '-lc', command])
            return {'message': self.client.execute(wrapped).decode(errors='replace') or '(không có output)'}
        if route == '/api/record':
            if self.demo:
                raise ValueError('DEMO không thu âm. Kết nối Pi bằng chế độ thật để dùng.')
            self.recording = None
            raw = self.client.record(str(data['device']), int(data['seconds']), int(data['rate']))
            if raw[:4] != b'RIFF' or raw[8:12] != b'WAVE':
                raise ValueError('Pi không trả về WAV hợp lệ')
            self.recording = raw
            return {'message': 'Đã thu xong', 'url': '/recording.wav', 'bytes': len(raw)}
        raise ValueError('Thao tác không tồn tại')


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass  # Never log the one-time browser access token.

    def send(self, code, content, content_type='application/json; charset=utf-8', extra=None):
        if not isinstance(content, bytes):
            content = json.dumps(content, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(content)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'no-referrer')
        self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; media-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'")
        for key, value in (extra or {}).items():
            self.send_header(key, value)
        self.end_headers()
        try:
            self.wfile.write(content)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def valid_host(self):
        return self.headers.get('Host') == self.server.origin.removeprefix('http://')

    def authorized(self):
        try:
            cookie = SimpleCookie(self.headers.get('Cookie', ''))
            token = cookie['pi_session'].value
            return secrets.compare_digest(token, self.server.state.token)
        except (KeyError, ValueError, CookieError):
            return False

    def do_GET(self):
        if not self.valid_host():
            return self.send(403, {'error': 'Host không hợp lệ'})
        url = urlsplit(self.path)
        if url.path == '/unlock':
            token = parse_qs(url.query).get('token', [''])[0]
            if not secrets.compare_digest(token, self.server.state.token):
                return self.send(403, {'error': 'Link truy cập không hợp lệ'})
            return self.send(303, b'', extra={'Location': '/', 'Set-Cookie':
                f'pi_session={self.server.state.token}; HttpOnly; SameSite=Strict; Path=/'})
        if not self.authorized():
            return self.send(401, {'error': 'Mở link có token được in trong Termux để truy cập.'})
        if url.path == '/api/config':
            return self.send(200, {'config': self.server.state.config, 'demo': self.server.state.demo})
        if url.path == '/recording.wav':
            raw = self.server.state.recording
            if raw is None:
                return self.send(404, {'error': 'Chưa có bản thu'})
            return self.send(200, raw, 'audio/wav', {'Content-Disposition': 'attachment; filename="pi-recording.wav"'})
        files = {'/': ('index.html', 'text/html; charset=utf-8'), '/style.css': ('style.css', 'text/css'),
                 '/app.js': ('app.js', 'application/javascript')}
        if url.path not in files:
            return self.send(404, {'error': 'Không tìm thấy'})
        name, kind = files[url.path]
        self.send(200, (ROOT / 'static' / name).read_bytes(), kind)

    def do_POST(self):
        if (not self.valid_host() or not self.authorized()
            or self.headers.get('X-Pi-Control') != '1'
            or self.headers.get('Origin', self.server.origin) != self.server.origin):
            return self.send(403, {'error': 'Yêu cầu không được phép'})
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 <= length <= (4 * 1024 * 1024 if urlsplit(self.path).path == '/api/files' else 16384):
                raise ValueError('Yêu cầu quá lớn')
            data = json.loads(self.rfile.read(length) or b'{}')
            if not isinstance(data, dict):
                raise ValueError('Yêu cầu JSON không hợp lệ')
        except (ValueError, UnicodeDecodeError) as exc:
            return self.send(400, {'error': str(exc)})
        state = self.server.state
        if not state.lock.acquire(blocking=False):
            return self.send(409, {'error': 'Đang có thao tác khác. Đợi hoàn tất rồi thử lại.'})
        try:
            result = state.dispatch(urlsplit(self.path).path, data)
            self.send(200, result)
        except Exception as exc:
            self.send(400, {'error': str(exc)})
        finally:
            state.lock.release()


class Server(ThreadingHTTPServer):
    daemon_threads = True

    def get_request(self):
        sock, address = super().get_request()
        sock.settimeout(10)  # Bound local HTTP headers/body reads.
        return sock, address


def make_server(port=8765, demo=False, config_path=CONFIG):
    server = Server(('127.0.0.1', port), Handler)
    server.origin = f'http://127.0.0.1:{server.server_port}'
    server.state = State(demo, config_path)
    return server


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--demo', action='store_true')
    parser.add_argument('--no-open', action='store_true')
    args = parser.parse_args()
    server = make_server(args.port, args.demo)
    url = server.origin + '/unlock?token=' + server.state.token
    print('Pi Control Android — giữ Termux chạy. Ctrl+C để dừng.', flush=True)
    print(url, flush=True)
    if not args.no_open:
        try:
            subprocess.run(['termux-open-url', url], timeout=5, check=False)
        except (OSError, subprocess.TimeoutExpired):
            pass
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
