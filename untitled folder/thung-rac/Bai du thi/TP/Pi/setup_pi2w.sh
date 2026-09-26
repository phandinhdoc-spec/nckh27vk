#!/usr/bin/env bash
set -Eeuo pipefail

[[ $(uname -m) == aarch64 ]] || { echo "Cần aarch64" >&2; exit 1; }
[[ $(dpkg --print-architecture) == arm64 ]] || { echo "Cần arm64" >&2; exit 1; }
[[ $EUID == 0 ]] || { echo "Chạy: sudo bash setup_pi2w.sh" >&2; exit 1; }

apt-get update
apt-get install -y python3-gpiozero mpg123 rpicam-apps
install -d -o greeneye -g greeneye /opt/green-eye 2>/dev/null || {
  useradd --system --home /opt/green-eye --shell /usr/sbin/nologin greeneye
  install -d -o greeneye -g greeneye /opt/green-eye
}
usermod -aG gpio,video,audio greeneye
install -m 0755 app.py /opt/green-eye/app.py
install -d -m 0755 /opt/green-eye/audio
install -m 0644 audio/*.mp3 /opt/green-eye/audio/
[[ -e /etc/green-eye.env ]] || install -m 0644 green-eye.env.example /etc/green-eye.env
install -m 0644 green-eye.service /etc/systemd/system/green-eye.service
systemctl daemon-reload

echo "Sửa /etc/green-eye.env, kiểm tra camera/loa, rồi chạy:"
echo "  sudo systemctl enable --now green-eye.service"
