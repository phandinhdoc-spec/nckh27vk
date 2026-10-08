#!/bin/bash
# Generated bundle of pi-startup sources. Run on the Pi as root.
set -euo pipefail
[[ $EUID -eq 0 ]] || { echo 'Run on the Pi as root'; exit 1; }
staging=$(mktemp -d)
trap 'rm -rf -- "$staging"' EXIT
cat > "$staging/clock_sync.py" <<'PI_STARTUP_FILE_EOF'
#!/usr/bin/env python3
"""Boot-time SNTP bootstrap, independent of D-Bus and TLS clock validation."""
import itertools
import os
import socket
import struct
import subprocess
import sys
import time

EPOCH = 2208988800
# Public Cloudflare addresses let bootstrap work before DNS/Tailscale is up.
SERVERS = ('162.159.200.1', '162.159.200.123', '0.pool.ntp.org', '1.pool.ntp.org')


def decode_reply(packet, token, elapsed):
    if len(packet) < 48:
        raise ValueError('Short NTP reply')
    if packet[0] >> 6 == 3 or (packet[0] & 7) != 4 or ((packet[0] >> 3) & 7) not in (3, 4):
        raise ValueError('Unsynchronized server or invalid NTP mode/version')
    if not 1 <= packet[1] <= 15 or packet[24:32] != token:
        raise ValueError('NTP stratum/origin mismatch')
    seconds, fraction = struct.unpack('!II', packet[40:48])
    if seconds == 0 and fraction == 0:
        raise ValueError('Missing server timestamp')
    epoch = seconds - EPOCH + fraction / 2**32
    # Support the 2036 era rollover without trusting the Pi's broken clock.
    if epoch < 1704067200:
        epoch += 2**32
    if not 1704067200 <= epoch < 4102444800 or not 0 <= elapsed <= 4:
        raise ValueError('Implausible time or excessive latency')
    return epoch + elapsed / 2


def query(server):
    # The first address is sufficient; retry other providers on failure.
    family, kind, proto, _, address = socket.getaddrinfo(server, 123, type=socket.SOCK_DGRAM)[0]
    with socket.socket(family, kind, proto) as sock:
        sock.settimeout(4)
        sock.connect(address)  # Filter replies to the selected endpoint.
        packet = bytearray(48)
        packet[0] = 0x23  # Version 4, client mode.
        token = struct.pack('!I', (int(time.time()) + EPOCH) & 0xffffffff) + os.urandom(4)
        packet[40:48] = token
        start = time.monotonic()
        sock.send(packet)
        reply = sock.recv(512)
        received = time.monotonic()
        return decode_reply(reply, token, received - start), received


def consensus(samples, now):
    adjusted = [stamp + now - received for stamp, received in samples]
    for a, b in itertools.combinations(adjusted, 2):
        if abs(a - b) <= 3:
            return (a + b) / 2
    raise ValueError('Need two NTP servers agreeing within 3 seconds')


def attempt():
    samples = []
    for server in SERVERS:
        try:
            samples.append(query(server))
            try:
                consensus(samples, time.monotonic())
                break
            except ValueError:
                pass
        except (OSError, ValueError) as exc:
            print(f'[clock] {server}: {exc}', flush=True)
    stamp = consensus(samples, time.monotonic())
    subprocess.run(['/usr/bin/date', '-u', '-s', f'@{stamp:.3f}'], check=True, timeout=10)
    print('[clock] Network time set using date; allowing tailscaled to start.', flush=True)


def main():
    if os.geteuid() != 0:
        sys.exit('Run as root to set the system clock')
    while True:
        try:
            attempt()
            return
        except (OSError, ValueError, subprocess.SubprocessError) as exc:
            print(f'[clock] Waiting for network time: {exc}; retry in 15 seconds', flush=True)
            time.sleep(15)


if __name__ == '__main__':
    main()
PI_STARTUP_FILE_EOF
cat > "$staging/tailscale_ready.py" <<'PI_STARTUP_FILE_EOF'
#!/usr/bin/env python3
"""Wait for an authenticated Tailscale connection before launching the app."""
import json
import subprocess
import time


def ready(status):
    return (status.get('BackendState') == 'Running'
            and bool(status.get('TailscaleIPs'))
            and status.get('Self', {}).get('Online') is True)


def main():
    while True:
        try:
            print('[tailscale] Running tailscale up (30 second limit)', flush=True)
            subprocess.run(['tailscale', 'up', '--timeout=30s'], check=True, timeout=40)
            result = subprocess.run(['tailscale', 'status', '--json'], check=True,
                                    capture_output=True, text=True, timeout=10)
            status = json.loads(result.stdout)
            if ready(status):
                print('[tailscale] Ready; starting /root/pi/app.py', flush=True)
                return
            print(f'[tailscale] Not ready: {status.get("BackendState")}; waiting', flush=True)
        except (OSError, ValueError, subprocess.SubprocessError) as exc:
            print(f'[tailscale] {exc}. If login is required, run tailscale up via local SSH and open its link.', flush=True)
        time.sleep(15)


if __name__ == '__main__':
    main()
PI_STARTUP_FILE_EOF
cat > "$staging/20-pi-clock.conf" <<'PI_STARTUP_FILE_EOF'
# Appended to the existing tailscaled service, without replacing its ExecStart.
[Service]
ExecStartPre=/usr/bin/python3 -u /usr/local/lib/pi-startup/clock_sync.py
TimeoutStartSec=infinity
PI_STARTUP_FILE_EOF
cat > "$staging/pi-app.service" <<'PI_STARTUP_FILE_EOF'
[Unit]
Description=Pi app after network clock bootstrap and Tailscale login
Wants=network-online.target tailscaled.service
After=network-online.target tailscaled.service
StartLimitIntervalSec=0

[Service]
Type=simple
User=root
WorkingDirectory=/root/pi
Environment=PYTHONUNBUFFERED=1
EnvironmentFile=-/root/pi/.env
ExecStartPre=/usr/bin/python3 -u /usr/local/lib/pi-startup/tailscale_ready.py
ExecStart=/usr/bin/python3 -u /root/pi/app.py
Restart=always
RestartSec=5
TimeoutStartSec=infinity
TimeoutStopSec=20
KillMode=control-group

[Install]
WantedBy=multi-user.target
PI_STARTUP_FILE_EOF
cat > "$staging/install.sh" <<'PI_STARTUP_FILE_EOF'
#!/bin/bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
[[ $EUID -eq 0 ]] || { echo 'Run as root on the Pi'; exit 1; }
[[ -f /root/pi/app.py ]] || { echo 'Missing /root/pi/app.py; no changes made'; exit 1; }
[[ -x /usr/bin/python3 && -x /usr/bin/date ]] || { echo 'Missing python3/date'; exit 1; }
command -v tailscale >/dev/null
systemctl cat tailscaled.service >/dev/null
# A reload must already work; do not install around an inaccessible system manager.
systemctl daemon-reload
if [[ -f /etc/systemd/system/pi-app.service ]] && ! grep -q 'Pi app after network clock bootstrap' /etc/systemd/system/pi-app.service; then
    echo 'Existing unrelated pi-app.service found. Review it before installing.'
    exit 1
fi
backup="/root/pi-startup-backup-$(date +%s)-$$"
install -d -m 0700 "$backup"
for target in /etc/systemd/system/pi-app.service /etc/systemd/system/tailscaled.service.d/20-pi-clock.conf; do
    if [[ -f "$target" ]]; then cp -a --parents "$target" "$backup/"; fi
done
install -d -m 0755 /usr/local/lib/pi-startup /etc/systemd/system/tailscaled.service.d
install -m 0644 clock_sync.py tailscale_ready.py /usr/local/lib/pi-startup/
install -m 0644 20-pi-clock.conf /etc/systemd/system/tailscaled.service.d/
install -m 0644 pi-app.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable tailscaled.service pi-app.service
printf '\nInstalled. Backup: %s\n' "$backup"
echo 'No service was restarted and no reboot was performed.'
echo 'First validate clock using: python3 -u /usr/local/lib/pi-startup/clock_sync.py'
echo 'Then: systemctl start tailscaled; tailscale up'
echo 'After resolving any old app autostart, run: systemctl start --no-block pi-app'
PI_STARTUP_FILE_EOF
bash "$staging/install.sh"
