#!/usr/bin/env python3
"""Private Pi-hosted controller behind Tailscale Serve; Python standard library."""
import argparse
from email.header import decode_header, make_header
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / 'pi-control-android'))
import server as android


class LocalSSH(android.SSH):
    def argv(self):
        args = super().argv()
        return args[:-1] + ['-o', 'IdentitiesOnly=yes', '-o',
            'UserKnownHostsFile=' + str(Path(self.key).parent / 'known_hosts'),
            '-o', 'GlobalKnownHostsFile=/dev/null'] + args[-1:]


class HostedState(android.State):
    def __init__(self, config):
        super().__init__(config_path=Path('/dev/null'))
        self.config.update(host='127.0.0.1', user='root', port=22,
                           key=config['key'], telemetry=config['telemetry'])
        self.client = LocalSSH('127.0.0.1', 'root', 22, config['key'])

    def configure(self, data):
        # The browser must never select a different SSH destination or key.
        return self.snapshot()

    def dispatch(self, route, data):
        if route == '/api/disconnect':
            raise ValueError('Kết nối được quản lý trên Pi. Đóng ứng dụng để thoát.')
        return super().dispatch(route, data)


class Handler(android.Handler):
    def valid_host(self):
        return (self.headers.get('X-Forwarded-Host') == urlsplit(self.server.origin).netloc
                and self.headers.get('X-Forwarded-Proto') == 'https')

    def authorized(self):
        try:
            identity = str(make_header(decode_header(self.headers.get('Tailscale-User-Login', ''))))
        except (ValueError, UnicodeError, LookupError):
            return False
        return (self.client_address[0] == '127.0.0.1'
                and not self.headers.get('Tailscale-Funnel-Request')
                and identity in self.server.allowed_users)

    def do_GET(self):
        if not self.valid_host() or not self.authorized():
            return self.send(403, {'error': 'Bật Tailscale và dùng tài khoản được chủ Pi cấp quyền. Mở đúng địa chỉ HTTPS của Pi.'})
        path = urlsplit(self.path).path
        if path == '/api/config':
            return self.send(200, {'config': {'telemetry': self.server.state.config['telemetry']},
                                   'demo': False, 'hosted': True})
        if path == '/unlock':
            return self.send(404, {'error': 'Không dùng token trong chế độ web.'})
        if path == '/':
            html = (android.ROOT / 'static/index.html').read_text()
            html = html.replace('</head>', '<link rel="manifest" href="/manifest.webmanifest"><link rel="apple-touch-icon" href="/icon.png"><meta name="apple-mobile-web-app-capable" content="yes"></head>')
            html = html.replace('</header>', '</header><p class="hint">Dùng như ứng dụng: mở menu trình duyệt (iPhone: Chia sẻ) → Thêm vào màn hình chính. Giữ Tailscale bật khi điều khiển Pi.</p>')
            return self.send(200, html.encode(), 'text/html; charset=utf-8')
        if path == '/manifest.webmanifest':
            return self.send(200, {'name': 'Pi Control', 'short_name': 'Pi Control',
                'id': '/', 'start_url': '/', 'scope': '/', 'display': 'standalone',
                'background_color': '#f3f6f2', 'theme_color': '#102c29',
                'icons': [{'src': '/icon.png', 'sizes': '512x512', 'type': 'image/png'}]},
                'application/manifest+json')
        if path == '/icon.png':
            return self.send(200, icon_png(), 'image/png')
        return super().do_GET()


def icon_png():
    # Generate a small PNG without image dependencies or binary source files.
    import struct
    import zlib
    def chunk(kind, data):
        return struct.pack('!I', len(data)) + kind + data + struct.pack('!I', zlib.crc32(kind + data))
    rows = []
    for y in range(512):
        row = bytearray(b'\x00')
        for x in range(512):
            mark = (110 <= x < 402 and 130 <= y < 175) or (155 <= x < 200 and 175 <= y < 382) or (312 <= x < 357 and 175 <= y < 382)
            row.extend((218, 245, 148) if mark else (16, 44, 41))
        rows.append(row)
    return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('!2I5B', 512, 512, 8, 2, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(b''.join(rows))) + chunk(b'IEND', b'')


def make_server(config, port=8766):
    origin = config['origin']
    if not re.fullmatch(r'https://[a-zA-Z0-9-]+\.[a-zA-Z0-9.-]+\.ts\.net', origin):
        raise ValueError('origin phải là HTTPS MagicDNS .ts.net, không có dấu / cuối')
    users = config['allowed_users']
    if not isinstance(users, list) or not users or any(not isinstance(u, str) or not u.strip() for u in users):
        raise ValueError('Cần ít nhất một tài khoản Tailscale được phép')
    server = android.Server(('127.0.0.1', port), Handler)
    server.origin = origin
    server.allowed_users = set(users)
    server.state = HostedState(config)
    return server


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='/etc/pi-control-web.json')
    args = parser.parse_args()
    with open(args.config) as stream:
        config = json.load(stream)
    server = make_server(config)
    print('Pi Control: ' + server.origin, flush=True)
    try:
        server.serve_forever()
    finally:
        server.server_close()
