#!/usr/bin/env python3
"""Install from this checked-out repository. No apt, networking restart or reboot."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


def run(*args, **kwargs):
    return subprocess.run(args, check=True, text=True, capture_output=True, timeout=45, **kwargs).stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--allow-user', action='append', required=True, help='Tailscale login; repeat for multiple administrators')
    parser.add_argument('--telemetry', default='/opt/thiennhan/history/telemetry.json')
    args = parser.parse_args()
    if os.geteuid() != 0:
        raise SystemExit('Chạy bằng root trên Pi.')
    for cmd in ('ssh', 'ssh-keygen', 'tailscale', 'systemctl'):
        if not shutil.which(cmd):
            raise SystemExit('Thiếu công cụ: ' + cmd)
    status = json.loads(run('tailscale', 'status', '--json'))
    if status.get('BackendState') != 'Running':
        raise SystemExit('Đăng nhập Tailscale trên Pi trước: tailscale up')
    dns = status['Self']['DNSName'].rstrip('.')
    origin = 'https://' + dns
    # Never overwrite an unrelated Serve route or enable public Funnel.
    serve = json.loads(run('tailscale', 'serve', 'status', '--json') or '{}')
    web = serve.get('Web', {})
    handler = web.get(dns + ':443', {}).get('Handlers', {}).get('/')
    if handler and handler != {'Proxy': 'http://127.0.0.1:8766'}:
        raise SystemExit('Tailscale Serve / đã có ứng dụng khác. Giữ nguyên, chưa cài đặt.')
    if serve.get('AllowFunnel'):
        raise SystemExit('Pi có cấu hình Funnel. Tắt Funnel trước khi triển khai công cụ root.')
    tcp = serve.get('TCP', {}).get('443')
    if tcp and not tcp.get('HTTPS'):
        raise SystemExit('Cổng Serve 443 đang dùng TCP khác; chưa thay đổi.')
    data = Path('/var/lib/pi-control-web')
    data.mkdir(mode=0o700, exist_ok=True)
    data.chmod(0o700)
    key = data / 'id_ed25519'
    if not key.exists():
        run('ssh-keygen', '-t', 'ed25519', '-N', '', '-C', 'pi-control-web-local', '-f', str(key))
    key.chmod(0o600)
    sshdir = Path('/root/.ssh')
    sshdir.mkdir(mode=0o700, exist_ok=True)
    auth = sshdir / 'authorized_keys'
    public = key.with_suffix('.pub').read_text().strip()
    entry = 'from="127.0.0.1",restrict ' + public
    old = auth.read_text() if auth.exists() else ''
    if entry not in old.splitlines():
        with auth.open('a') as stream:
            stream.write(('\n' if old and not old.endswith('\n') else '') + entry + '\n')
    auth.chmod(0o600)
    hostkey = Path('/etc/ssh/ssh_host_ed25519_key.pub').read_text().strip()
    known = data / 'known_hosts'
    known.write_text('127.0.0.1 ' + hostkey + '\n')
    known.chmod(0o600)
    run('ssh', '-T', '-o', 'BatchMode=yes', '-o', 'StrictHostKeyChecking=yes',
        '-o', 'IdentitiesOnly=yes', '-o', 'ConnectTimeout=8', '-o',
        'UserKnownHostsFile=' + str(known), '-o', 'GlobalKnownHostsFile=/dev/null',
        '-i', str(key), 'root@127.0.0.1', 'true')
    root = Path(__file__).resolve().parent.parent
    releases = Path('/opt/pi-control-web-releases')
    releases.mkdir(exist_ok=True)
    release = Path(tempfile.mkdtemp(prefix='release-', dir=releases))
    release.chmod(0o755)
    for folder in ('pi-control', 'pi-control-android', 'pi-control-web'):
        shutil.copytree(root / folder, release / folder, ignore=shutil.ignore_patterns('__pycache__', 'tests', '.git'))
    configpath = Path('/etc/pi-control-web.json')
    if configpath.exists():
        shutil.copy2(configpath, release / 'previous-config.json')
        (release / 'previous-config.json').chmod(0o600)
    config = {'origin': origin, 'allowed_users': args.allow_user, 'key': str(key), 'telemetry': args.telemetry}
    fd = os.open(configpath, os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0o600)
    with os.fdopen(fd, 'w') as stream:
        json.dump(config, stream, indent=2)
    configpath.chmod(0o600)
    unit = Path('/etc/systemd/system/pi-control-web.service')
    if unit.exists():
        shutil.copy2(unit, release / 'previous-service.txt')
    unit.write_text('[Unit]\nDescription=Pi Control private web app\nAfter=network.target tailscaled.service ssh.service\n\n[Service]\nType=simple\nUser=root\nExecStart=/usr/bin/python3 ' + str(release / 'pi-control-web/web_server.py') + '\nRestart=on-failure\nRestartSec=5\nUMask=0077\n\n[Install]\nWantedBy=multi-user.target\n')
    run('systemctl', 'daemon-reload')
    run('systemctl', 'enable', 'pi-control-web.service')
    run('systemctl', 'restart', 'pi-control-web.service')
    run('systemctl', 'is-active', 'pi-control-web.service')
    print('Backend đã chạy. Thiết lập HTTPS Tailscale Serve…', flush=True)
    # Output must stay visible: Tailscale may print the owner's HTTPS enable link.
    try:
        subprocess.run(['tailscale', 'serve', '--bg', '--https=443', 'http://127.0.0.1:8766'], check=True, timeout=60)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        print('Backend đã cài. Hoàn tất bật HTTPS theo link Tailscale rồi chạy lại:\n tailscale serve --bg --https=443 http://127.0.0.1:8766')
        raise SystemExit(1)
    print('\nMở trên điện thoại đã kết nối Tailscale: ' + origin)
    print('Android: menu → Thêm vào màn hình chính. iPhone: Safari → Chia sẻ → Thêm vào MH chính.')
    print('Quản trị được phép: ' + ', '.join(args.allow_user))


if __name__ == '__main__':
    try:
        main()
    except subprocess.CalledProcessError as exc:
        raise SystemExit('Lệnh cài đặt thất bại: ' + str(exc.cmd) + '\n' + (exc.stderr or ''))
