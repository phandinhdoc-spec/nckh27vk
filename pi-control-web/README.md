# Pi Control Web — Android và iPhone

Python chạy thường trực **trên Pi**, điện thoại chỉ cần Tailscale và trình duyệt.
SSH được thực thi trên backend bằng OpenSSH, khóa riêng nằm trên Pi. Có tổng quan,
services, cảm biến/telemetry, thiết bị, thu âm, lệnh SSH, đọc/sửa/upload file root,
và thêm WiFi vào cơ sở dữ liệu DietPi. Tab Lệnh là lệnh có giới hạn 30 giây,
không phải terminal tương tác cho nano/top/sudo hỏi mật khẩu.

## Cài một lần trên Pi (root)

Pi phải có Python 3.9+, OpenSSH server chạy và cho phép root đăng nhập bằng key,
Tailscale đã đăng nhập, đồng hồ đúng. Installer không chạy apt, không đổi WiFi,
không reboot, không sửa sshd_config. Nó chỉ kiểm tra SSH localhost.

Tải mã nguồn main vào một thư mục mới, rồi cài (thay EMAIL bằng login Tailscale thực):

```sh
workdir=$(mktemp -d)
curl -fL https://github.com/phandinhdoc-spec/nckh27vk/archive/refs/heads/main.tar.gz -o "$workdir/source.tar.gz"
tar -xzf "$workdir/source.tar.gz" -C "$workdir"
python3 "$workdir/nckh27vk-main/pi-control-web/install.py" --allow-user EMAIL
```

Có thể thêm nhiều `--allow-user EMAIL_KHAC`. Chạy lại installer thay toàn bộ danh sách
cho phép bằng danh sách truyền vào. Có thể thêm `--telemetry /duong/dan/telemetry.json`.
Các bản cài cũ và bản sao config/service nằm trong `/opt/pi-control-web-releases`.

Nếu Tailscale yêu cầu bật HTTPS, chủ tailnet mở link mà lệnh in ra, bật HTTPS,
rồi chạy lại `tailscale serve --bg --https=443 http://127.0.0.1:8766`.
Installer từ chối ghi đè route `/` của ứng dụng khác hoặc cấu hình Funnel.
Serve chạy nền và giữ cấu hình qua lần khởi động; backend có systemd tự khởi động.
Không cần chạy `tailscale up` mỗi lần người dùng mở app.

## Dùng trên điện thoại

1. Cài/đăng nhập Tailscale; tài khoản được cấp quyền vào Pi qua tailnet và nằm trong
   `allowed_users`. Chính sách tailnet phải cho kết nối HTTPS cổng 443 đến Pi.
2. Mở URL HTTPS installer in ra, ví dụ `https://hieunga-1.tailf860e1.ts.net`.
3. Android: menu trình duyệt → Thêm vào màn hình chính/Cài ứng dụng.
   iPhone: Safari → Chia sẻ → Thêm vào màn hình chính.

Không nhập IP WiFi, không Termux, không token URL, không nhập SSH key trên điện thoại.
Khi đổi WiFi/4G, bật lại Tailscale nếu cần; trang tự thử đọc lại sau khi kết nối phục hồi.
Pi vẫn cần nguồn và Internet. Đây là web app trực tuyến có manifest và biểu tượng;
không cache dữ liệu điều khiển/file để dùng offline. Màn hình chính phụ thuộc hỗ trợ
trình duyệt; luôn có thể mở bằng URL.

Giao diện dùng JavaScript hiện đại (Safari 14+ hoặc Chrome 86+ làm mốc tối thiểu mã
nguồn), nhưng thiết bị còn phải chạy được phiên bản Tailscale được hỗ trợ. Không cam kết
mọi Android/iPhone cũ; kiểm tra yêu cầu Tailscale hiện hành trên App Store/Google Play.
Chưa thử trực tiếp trên các mẫu điện thoại cũ.

## Quyền và bảo trì

- Backend chỉ lắng nghe `127.0.0.1:8766`; không mở 0.0.0.0, không dùng Funnel.
- Tailscale Serve đặt identity header. Backend kiểm tra login chính xác, HTTPS hostname,
  nguồn loopback và Origin cho POST; không dùng cookie/token của bản Termux.
- **Mọi tài khoản được cho phép có quyền điều khiển root**, kể cả file và lệnh. Các quản trị
  viên dùng chung Pi, telemetry và bản thu gần nhất; đây không phải hệ thống phân quyền nhiều vai trò.
- Tin cậy tiến trình/người dùng cục bộ trên Pi: localhost có thể giả header Serve.
  Không triển khai kiểu này trên máy nhiều người dùng không tin cậy.
- Máy Tailscale gắn tag không có user identity header sẽ bị từ chối.
- Chỉnh `/etc/pi-control-web.json`, rồi `systemctl restart pi-control-web` để đổi quyền/path.
- Kiểm tra: `systemctl status pi-control-web --no-pager`, `journalctl -u pi-control-web -n 50`,
  `tailscale serve status`. Dừng: `systemctl disable --now pi-control-web`.
- Gỡ route riêng ứng dụng: `tailscale serve --https=443 off` (chỉ nếu cổng này dành riêng app).
  SSH key và dòng `pi-control-web-local` trong authorized_keys có thể xóa sau khi dừng.

Bản Android chạy trong Termux vẫn giữ nguyên. Cảm biến chỉ có giá trị khi ứng dụng Pi
đang ghi telemetry; danh sách bus không chứng minh cảm biến hoạt động. WiFi dùng helper
DietPi hiện có; thu âm cần ALSA microphone. Không tự cài driver hoặc khởi động Pi app khác.

## Kiểm thử

```sh
python3 -m unittest discover -s pi-control-web/tests
python3 -m unittest discover -s pi-control-android/tests
```
