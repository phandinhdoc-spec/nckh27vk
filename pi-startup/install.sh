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
