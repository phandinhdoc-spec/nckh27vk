"""OpenSSH transport and validated remote operations; no third-party packages."""
from dataclasses import dataclass
from pathlib import Path
import json
import re
import shlex
import subprocess

PROBE = Path(__file__).with_name('remote_probe.py')
PROTECTED = {'ssh.service', 'sshd.service', 'tailscaled.service', 'NetworkManager.service',
             'systemd-networkd.service', 'networking.service', 'wpa_supplicant.service', 'dbus.service'}


def service_command(action, unit):
    if action not in {'start', 'stop', 'restart', 'enable', 'disable', 'logs'}:
        raise ValueError('Thao tác service không hợp lệ')
    if not re.fullmatch(r'[A-Za-z0-9_@.:\\-]+\.service', unit) or unit.startswith('-'):
        raise ValueError('Tên service không hợp lệ')
    if action in {'stop', 'restart', 'disable'} and (unit in PROTECTED or unit.startswith(('ssh@', 'wpa_supplicant@'))):
        raise ValueError('Service giữ kết nối bị khóa trong nút điều khiển để tránh mất SSH/Tailscale.')
    if action == 'logs':
        return shlex.join(['journalctl', '-u', unit, '-n', '150', '--no-pager', '--output=short-iso'])
    return shlex.join(['sudo', '-n', 'systemctl', action, unit])


@dataclass(frozen=True)
class SSH:
    host: str
    user: str
    port: int = 22
    key: str = ''

    def argv(self):
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9.:-]*', self.host):
            raise ValueError('Nhập IP Tailscale hoặc hostname, không có khoảng trắng')
        if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_-]*', self.user):
            raise ValueError('Tên user SSH không hợp lệ')
        if not 1 <= self.port <= 65535:
            raise ValueError('Port phải từ 1 đến 65535')
        args = ['ssh', '-T', '-o', 'BatchMode=yes', '-o', 'StrictHostKeyChecking=yes',
                '-o', 'ConnectTimeout=8', '-o', 'ServerAliveInterval=5',
                '-o', 'ServerAliveCountMax=2', '-p', str(self.port)]
        if self.key:
            args += ['-i', str(Path(self.key).expanduser())]
        return args + [f'{self.user}@{self.host}']

    def execute(self, command, stdin=None, timeout=40):
        p = subprocess.run(self.argv() + [command], input=stdin, capture_output=True,
                           timeout=timeout)
        if p.returncode:
            raise RuntimeError(p.stderr.decode(errors='replace').strip() or
                               p.stdout.decode(errors='replace').strip() or f'Exit {p.returncode}')
        return p.stdout

    def probe(self, mode, telemetry_path):
        return json.loads(self.execute(shlex.join(['python3', '-', mode, telemetry_path]),
                                      PROBE.read_bytes(), timeout=55))

    def record(self, device, seconds, rate):
        if not 1 <= seconds <= 120 or rate not in {16000, 44100, 48000}:
            raise ValueError('Thu 1–120 giây, tần số 16000/44100/48000 Hz')
        if not device or len(device) > 200:
            raise ValueError('Thiết bị ALSA không hợp lệ')
        # Finite duration + remote timeout; no persistent files or background recorder.
        return self.execute(shlex.join(['timeout', '--signal=TERM', '--kill-after=2',
            str(seconds + 5), 'arecord', '-q', '-D', device, '-f', 'S16_LE', '-c', '1',
            '-r', str(rate), '-d', str(seconds), '-t', 'wav', '-']), timeout=seconds + 20)
