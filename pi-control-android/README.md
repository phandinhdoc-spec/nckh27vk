# Pi Control Android

Bản Python chạy trong **Termux trên điện thoại Android**, giao diện cảm ứng mở bằng Chrome/Firefox trên chính điện thoại. Không phải APK độc lập. Pi chỉ cần SSH và Python 3; không cần cài web server trên Pi, không phụ thuộc máy tính hay hotspot.

## Chức năng

- CPU, RAM, nhiệt độ, ổ đĩa, uptime; refresh nền mỗi 5 giây khi trang đang mở. Không khóa tab, nút cài đặt hoặc ô nhập khi đọc dữ liệu. Lệnh người dùng được xếp sau lần đọc đang chạy; chỉ các nút gửi lệnh tạm khóa trong lúc xử lý lệnh để tránh gửi trùng.
- Danh sách systemd service, tìm kiếm, start/stop/restart, enable/disable và journal.
- Thiết bị USB, ALSA, Bluetooth, mạng, I²C/UART/GPIO do hệ điều hành nhận diện.
- Telemetry JSON của driver cảm biến, ghi rõ mẫu cũ/mất dữ liệu. Không lấy ảnh camera.
- Thu WAV từ mic Pi (mono, 1–120 giây), nghe và tải về Android.
- Lệnh shell không tương tác với timeout 30 giây.
- Nhập IP Tailscale, LAN hoặc alias `pi` từ `~/.ssh/config` của Termux.

Backend tái sử dụng `pi-control/core.py` và `remote_probe.py`. Giữ hai thư mục cạnh nhau như repo. Đường dẫn telemetry mặc định là `/opt/thiennhan/history/telemetry.json`; app `/root/pi/app.py` cần tự xuất theo schema đó hoặc nhập đúng file telemetry của app. Bản Android không tự thêm driver vào app bất kỳ.

## Cài trên Android

Trong **Termux**, không phải shell `root@hieunga`:

```sh
pkg install python openssh curl
```

Tải gói nhỏ gồm bản Android và hai file backend, không tải toàn bộ repo:

```sh
curl -fL https://raw.githubusercontent.com/phandinhdoc-spec/nckh27vk/main/pi-control-android/install-termux.sh -o ~/install-pi-control.sh
bash ~/install-pi-control.sh
```

Installer tải file về thư mục phiên bản mới trong `~/pi-control-android-releases/`, rồi cập nhật launcher `~/pi-control-android-start.sh` khi mọi file đã tải đủ. Không xóa phiên bản cũ và không ghi đè SSH key/config của bạn. Gói nguồn đã có trong repo; nếu đã clone, chạy thẳng `python pi-control-android/server.py`.

Chạy:

```sh
bash ~/pi-control-android-start.sh
```

Trình duyệt sẽ được mở nếu có `termux-open-url`; nếu chưa mở, chép **đúng link được in trong Termux** (có token) sang trình duyệt. Link đổi khi server khởi động lại. Có thể dùng `--demo` để xem giao diện trước khi kết nối Pi:

```sh
bash ~/pi-control-android-start.sh --demo
```

## Thiết lập SSH một lần

Nếu dùng từ xa, bật Tailscale trên điện thoại và Pi, ACL cho phép SSH. Nếu ở cùng Wi-Fi nhà, có thể dùng IP LAN. Alias `pi` đang trỏ địa chỉ hotspot cũ cần sửa HostName trong `~/.ssh/config` thành IP Tailscale thật của Pi; ứng dụng không tự suy đoán giữa `hieunga` và `hieunga-1`.

Trước hết SSH bằng Terminal để xác nhận host key đúng máy và đăng nhập:

```sh
ssh root@IP_CUA_PI
```

Thoát về Termux. Nếu chưa có key, tạo một key riêng, không ghi đè key đang dùng:

```sh
ssh-keygen -t ed25519 -f ~/.ssh/pi_control_ed25519
ssh-copy-id -i ~/.ssh/pi_control_ed25519.pub root@IP_CUA_PI
```

Đặt passphrase nếu muốn bảo vệ key; nếu có passphrase, nạp key vào ssh-agent trước khi mở app. Với shell bash:

```sh
bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/pi_control_ed25519
```

Sau đó **từ cùng shell** chạy app để nó kế thừa agent. Không đặt passphrase/mật khẩu trong JSON hay source. Xác nhận đăng nhập không tương tác:

```sh
ssh -o BatchMode=yes -i ~/.ssh/pi_control_ed25519 root@IP_CUA_PI uptime
```

Trong UI → ⚙ Kết nối:

- Host: IP Tailscale của Pi (hoặc alias `pi` đã sửa).
- User: `root`, port `22`.
- SSH key: `~/.ssh/pi_control_ed25519` (hoặc để trống nếu dùng key mặc định/agent).
- Telemetry: file JSON trên Pi.

Bấm Lưu & kết nối. Lỗi xác thực/host key hiển thị nguyên nhân; không tự bỏ kiểm tra host key. User root quản lý systemctl trực tiếp; user khác cần quyền sudo không tương tác đã được cấp trên Pi. Không cấp `NOPASSWD: ALL` chỉ để dùng UI.

## Android và chạy nền

Giữ tiến trình Termux hoạt động khi dùng UI. Android có thể dừng Termux khi hạn chế pin hoặc thiếu RAM. Nếu cần phiên làm việc dài, cho phép Termux chạy nền trong cài đặt pin; có thể dùng `termux-wake-lock` khi cần, và `termux-wake-unlock` sau khi dùng (tốn pin hơn). Bản này chưa tự chạy sau khi khởi động điện thoại.

Ctrl+C trong Termux để dừng server. Web UI chỉ lắng nghe `127.0.0.1`, không mở cho thiết bị khác trên Wi-Fi. Server kiểm tra Host, token cookie HttpOnly, Origin và header riêng cho thao tác; không dùng tài nguyên CDN bên ngoài. Root SSH vẫn có toàn quyền Pi, ô lệnh yêu cầu xác nhận trước khi thực thi.

## Thu âm

Chọn ALSA device sau khi xem tab Thiết bị. Nếu service đang giữ mic, chủ động dừng service đó rồi thu và chạy lại sau. Không tự giành mic. WAV giữ tạm trong RAM của Termux, bản mới thay bản cũ; ngắt kết nối/xóa tiến trình sẽ bỏ bản giữ trong RAM. Bấm Tải WAV để lưu lâu dài bằng trình duyệt. Không có nút hủy thu giữa chừng; chọn thời lượng ngắn để thử.

## Kiểm thử

```sh
python3 -m unittest discover -s pi-control-android/tests -v
python3 -m unittest discover -s pi-control/tests -v
```

Test HTTP thực trên loopback: xác thực token, chống Host/Origin khác, từ chối thao tác đồng thời, bảo vệ service kết nối, demo không gửi SSH, ngắt kết nối xóa bản thu, không dùng sudo khi user root. Chưa kiểm tra trực quan bằng trình duyệt hoặc end-to-end với Pi/điện thoại thật; các giá trị demo được gắn nhãn rõ.

## Cảm biến có tên và kết quả

Tab **Cảm biến** hiển thị tên model từ `sensor_info`, kết nối, trạng thái bật/tắt,
đơn vị và tuổi mẫu. Dữ liệu quá 15 giây được đánh dấu cũ. Không suy đoán tên model
chỉ từ việc có cổng I²C/UART. File schema cũ vẫn đọc được, với tên nhóm chung.
Code `Pi 3` hiện có **GY25 UART + GY63/MS5611**, chưa có driver GY53.
Không bật MS5611 nếu phần cứng thực tế là GY53.

Bản mới `Pi 3` đọc `.env` và xuất mẫu khoảng 2 giây/lần khi có
`PI_CONTROL_TELEMETRY_PATH`. Luồng nền nằm trong chính app, dùng chung khóa đọc
cảm biến với luồng gửi lệnh giọng nói. Không mở camera/mic trong luồng này.
Thư mục cha của telemetry phải tồn tại và user chạy app phải ghi được.

Trên Pi, cập nhật bản đã cài ở `/root/pi` bằng công cụ có kiểm tra phiên bản:

```sh
curl -fL https://raw.githubusercontent.com/phandinhdoc-spec/nckh27vk/main/pi-control-android/update-pi-telemetry.py -o /tmp/update-pi-telemetry.py
python3 /tmp/update-pi-telemetry.py /root/pi
```

Công cụ chỉ chấp nhận 3 file `app.py`, `config.py`, `sensors.py` khớp bản nguồn
đã kiểm tra, tải và kiểm tra hash trước khi thay, có bản sao trong thư mục ẩn
`.pi-control-backup-*`. Nếu file trên Pi đã chỉnh riêng, công cụ dừng và báo rõ;
không ghi đè mù. Không sửa `.env`, không tự restart. Nếu dùng vị trí khác, truyền
đường dẫn đó thay `/root/pi`.

Trong UI tab File mở `/root/pi/.env`, thêm hoặc chỉnh (không tạo hai dòng trùng):

```dotenv
PI_CONTROL_TELEMETRY_PATH=/root/pi/telemetry.json
```

Giữ nguyên cấu hình cảm biến thực tế. Qua tab Services restart **service chạy
ứng dụng này** (ví dụ `pi-app.service`), rồi ở Cài đặt đổi file telemetry thành
`/root/pi/telemetry.json`, bấm Lưu & kết nối. Nếu service không chạy được, xem Log.
Bật xuất telemetry không sửa driver hoặc khẳng định cảm biến đang nối đúng.

## Xem và sửa file bằng quyền root

Tab **File**: nhập `/root/pi`, `/etc` hoặc đường dẫn khác → Xem thư mục.
Có hiển thị file ẩn; bấm file để mở, chỉnh nội dung rồi Lưu file. Có thể nhập
thẳng `/root/pi/.env` và bấm Mở file. Symlink hiển thị dấu ↗; bấm để đưa đường dẫn
vào ô rồi chọn Mở file hoặc Xem thư mục. Khi mở, UI hiển thị đường dẫn đích thực.

- Dùng quyền user SSH hiện tại; đăng nhập root thì đọc/ghi bằng root, không cần sudo.
- Chỉ sửa file văn bản UTF-8 hiện có, tối đa 512 KiB. Không tạo/xóa file, không sửa file nhị phân hoặc device node.
- Lưu giữ owner, mode, extended attributes; tạo bản sao nội dung cũ `tên-file.pi-control-backup-*` quyền 0600 trước khi thay thế file.
- Kiểm tra SHA-256 khi lưu; nếu có thay đổi từ tiến trình khác, báo xung đột thay vì cố ghi đè. Đây không phải khóa bắt buộc đối với các tiến trình bên ngoài.
- Có cảnh báo khi bỏ phần chưa lưu; polling nền không ghi đè nội dung editor.
- Service không tự restart khi lưu cấu hình. Chủ động restart qua tab Services nếu cần.
- Muốn khôi phục, mở bản sao bằng UI, chép nội dung, mở lại file gốc rồi lưu.
- Nội dung nhạy cảm như `.env` chỉ nên xem trên điện thoại của bạn; không cần gửi ảnh nội dung hay khóa API để được hỗ trợ.
