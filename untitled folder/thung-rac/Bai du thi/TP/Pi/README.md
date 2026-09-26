# Green Eye — Raspberry Pi Zero 2 W

Luồng: bấm nút GPIO → chụp JPEG → gửi Mac → nhận mã → phát MP3 bằng `mpg123` → xóa ảnh tạm.

Không dùng Bluetooth hoặc microphone.

## Nối nút

- Một chân nút vào GPIO17 (pin vật lý 11).
- Chân còn lại vào GND.
- `gpiozero` dùng pull-up nội nên không cần điện trở ngoài.

## Cài DietPi ARM64

Sao chép toàn bộ thư mục `Pi` lên Pi rồi chạy:

```sh
cd Pi
sudo bash setup_pi2w.sh
sudo nano /etc/green-eye.env
```

Điền IP/Tailscale IP của Mac, ví dụ:

```text
SERVER_URL=http://192.168.1.10:8765
BUTTON_PIN=17
MP3_DIR=/opt/green-eye/audio
```

Kiểm tra trước khi bật service:

```sh
curl -fsS http://192.168.1.10:8765/health
rpicam-jpeg -n -t 1 -o /dev/shm/test.jpg
mpg123 /opt/green-eye/audio/RHC.mp3
sudo -u greeneye /usr/bin/python3 /opt/green-eye/app.py --self-test
```

Sau khi camera, mạng và loa đều đạt:

```sh
sudo systemctl enable --now green-eye.service
systemctl status green-eye.service
journalctl -u green-eye.service -f
```

## Mã và âm thanh

| Mã | File | Nội dung |
|---|---|---|
| `RHC` | `audio/RHC.mp3` | Đây là rác hữu cơ. |
| `RVC` | `audio/RVC.mp3` | Đây là rác vô cơ. |
| `RNH` | `audio/RNH.mp3` | Đây là vật sắc nhọn nguy hiểm. |
| `RKH` | `audio/RKH.mp3` | Đây là vật có ký hiệu hóa chất độc hại. |
| `RK` | `audio/RK.mp3` | Đây là loại rác khác. |

## Cấu trúc tối thiểu

```text
app.py
setup_pi2w.sh
green-eye.service
green-eye.env.example
audio/*.mp3
```