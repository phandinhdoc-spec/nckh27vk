"""Read-only, stdlib-only Linux probe. Executed over SSH via stdin."""
import glob
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time


def run(args, timeout=4):
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=timeout,
                           env={**os.environ, 'LC_ALL': 'C', 'SYSTEMD_COLORS': '0'})
        return {'ok': p.returncode == 0, 'text': (p.stdout + p.stderr).strip()}
    except (OSError, subprocess.TimeoutExpired) as e:
        return {'ok': False, 'text': str(e)}


def services():
    units = run(['systemctl', 'list-units', '--all', '--type=service', '--plain', '--no-legend', '--no-pager'])
    files = run(['systemctl', 'list-unit-files', '--type=service', '--no-legend', '--no-pager'])
    rows = {}
    for line in files['text'].splitlines() if files['ok'] else []:
        parts = line.split()
        if len(parts) >= 2 and parts[0].endswith('.service'):
            rows[parts[0]] = [parts[0], 'not-loaded', '—', parts[1], '']
    for line in units['text'].splitlines() if units['ok'] else []:
        parts = line.split(None, 4)
        if len(parts) >= 4 and parts[0].endswith('.service'):
            name, load, active, sub = parts[:4]
            enabled = rows.get(name, ['', '', '', 'unknown'])[3]
            rows[name] = [name, active, sub, enabled, parts[4] if len(parts) > 4 else load]
    return {'rows': sorted(rows.values()), 'errors': [v['text'] for v in (units, files) if not v['ok']]}


def telemetry(path):
    try:
        p = Path(path).expanduser()
        if p.stat().st_size > 1024 * 1024:
            raise ValueError('Telemetry vượt 1 MiB')
        value = json.loads(p.read_text())
        if not isinstance(value, dict) or not isinstance(value.get('devices'), dict):
            raise ValueError('Telemetry cần object devices')
        stamp = float(value['timestamp'])
        if not math.isfinite(stamp):
            raise ValueError('Timestamp không hợp lệ')
        age = time.time() - stamp
        return {'state': 'fresh' if 0 <= age <= 15 else 'stale', 'age_seconds': round(age, 1), 'data': value}
    except (OSError, ValueError, KeyError, TypeError) as e:
        return {'state': 'unavailable', 'error': str(e)}


def snapshot(path):
    def cpu():
        values = list(map(int, Path('/proc/stat').read_text().splitlines()[0].split()[1:9]))
        return sum(values), values[3] + values[4]
    first = cpu()
    time.sleep(.15)
    second = cpu()
    delta = second[0] - first[0]
    memory = {line.split(':')[0]: int(line.split()[1]) for line in Path('/proc/meminfo').read_text().splitlines()}
    disk = shutil.disk_usage('/')
    try:
        temperature = float(Path('/sys/class/thermal/thermal_zone0/temp').read_text()) / 1000
    except (OSError, ValueError):
        temperature = None
    return {'timestamp': time.time(), 'hostname': os.uname().nodename,
            'cpu_percent': round(100 * (1 - (second[1] - first[1]) / delta), 1) if delta else 0,
            'ram_percent': round(100 * (1 - memory['MemAvailable'] / memory['MemTotal']), 1),
            'disk_percent': round(100 * disk.used / disk.total, 1), 'temperature_c': temperature,
            'uptime_seconds': float(Path('/proc/uptime').read_text().split()[0]),
            'load': os.getloadavg(), 'services': services(), 'telemetry': telemetry(path)}


def devices():
    commands = {'USB': ['lsusb'], 'Microphone': ['arecord', '-l'], 'Audio outputs': ['aplay', '-l'],
                'Bluetooth connected': ['bluetoothctl', 'devices', 'Connected'],
                'Network': ['ip', '-brief', 'address'], 'Tailscale': ['tailscale', 'status'],
                'I2C adapters (not sensor detection)': ['i2cdetect', '-l']}
    result = {name: run(command) for name, command in commands.items()}
    result['Device nodes'] = {'ok': True, 'text': '\n'.join(sorted(set(
        glob.glob('/dev/i2c-*') + glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*') +
        glob.glob('/dev/serial*') + glob.glob('/dev/gpiochip*')))) or 'Không có node phù hợp'}
    return result


if __name__ == '__main__':
    mode = sys.argv[1]
    print(json.dumps(devices() if mode == 'devices' else snapshot(sys.argv[2]), ensure_ascii=False))
