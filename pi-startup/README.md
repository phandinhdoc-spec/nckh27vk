# Pi startup: network time → Tailscale → /root/pi/app.py

Dành cho Pi hiện tại: DietPi/Debian 13, user root, app `/root/pi/app.py`.
Không dùng `timedatectl` hoặc system D-Bus để chỉnh giờ. Không apt update, không cài lại hệ điều hành, không reboot trong installer.

## Trình tự mỗi lần boot

1. Drop-in của `tailscaled.service` chạy `clock_sync.py` **trước daemon**. Script hỏi giờ SNTP qua UDP 123; chưa có mạng thì thử lại sau 15 giây. Vì chưa có đồng hồ đúng, bước này không dùng HTTPS.
2. Khi hai endpoint trả giờ khớp trong 3 giây, script gọi `/usr/bin/date -u -s @UNIX_TIMESTAMP`. Chỉ khi `date` thành công, systemd mới tiếp tục khởi động `tailscaled`.
3. `pi-app.service` chờ job khởi động tailscaled hoàn tất, chạy `tailscale up --timeout=30s`; thử lại nếu thất bại. Kiểm tra JSON có `BackendState=Running`, có Tailscale IP và `Self.Online=true` trước khi mở app. Đây là trạng thái client, không đảm bảo mọi peer/ACL đều truy cập được.
4. Chạy `/usr/bin/python3 -u /root/pi/app.py` với working directory `/root/pi`. Đọc thêm `/root/pi/.env` nếu có (cú pháp EnvironmentFile systemd, không phải shell script). App thoát sẽ được khởi động lại sau 5 giây và kiểm tra Tailscale lại.

Không dùng ngày giờ hard-code. Không tắt kiểm tra TLS. Không lưu auth key. `~/pi` được đổi thành `/root/pi` vì service chạy với root, systemd không tự mở rộng dấu `~` như shell.

## Cài đặt

Từ bản clone repo trên **Pi**, chạy:

```sh
bash pi-startup/install.sh
```

Hoặc dùng `install-bundle.sh` (chứa cùng 5 file cài đặt) để chuyển từ Termux sang Pi. Cách này tải qua điện thoại có giờ đúng, nên không phụ thuộc HTTPS trên Pi đang sai giờ.

Trong **Termux**, không phải shell `root@hieunga`:

```sh
curl -fL https://raw.githubusercontent.com/phandinhdoc-spec/nckh27vk/main/pi-startup/install-bundle.sh -o ~/pi-startup-install.sh
scp ~/pi-startup-install.sh pi:/root/pi-startup-install.sh
ssh pi
```

Nếu alias `pi` còn trỏ IP hotspot cũ, dùng `root@IP_HIEN_TAI` thay `pi` trong `scp`/`ssh`.

Sau đó, trên **Pi**:

```sh
bash /root/pi-startup-install.sh
python3 -u /usr/local/lib/pi-startup/clock_sync.py
systemctl start --no-block tailscaled
```

Nếu lệnh clock liên tục báo timeout: mạng có thể chặn UDP 123; app/Tailscale theo chuỗi này sẽ tiếp tục chờ. Ctrl+C chỉ dừng lần kiểm tra bằng tay. Gửi log để đổi nguồn thời gian/phương thức có xác thực phù hợp, không bỏ kiểm tra chứng chỉ.

Chờ clock/daemon sẵn sàng rồi chạy `tailscale up`. Lần đăng nhập đầu hoặc key hết hạn phải mở link xác thực trên điện thoại. Không thể bỏ qua yêu cầu đăng nhập bằng một service. Sau đó:

```sh
tailscale status
tailscale ip -4
```

**Trước khi bật app service lần đầu:** bảo đảm app này không đang được chạy thủ công hoặc được một service/cron khác tự mở. Installer không tự tắt service lạ. Có thể xem:

```sh
pgrep -af 'python.*app.py'
systemctl list-unit-files --type=service | grep -E 'pi|thien|green'
```

Khi đã tránh chạy trùng:

```sh
systemctl start --no-block pi-app.service
journalctl -u tailscaled -u pi-app -n 80 --no-pager
```

Installer chỉ enable cho các lần boot sau, không restart Tailscale đang hoạt động để tránh cắt phiên SSH hiện tại. Drop-in mới áp dụng ở lần daemon khởi động kế tiếp. Có thể kiểm thử hiện tại bằng clock script trực tiếp như trên. Không cần reboot ngay.

## Quản lý

```sh
systemctl status tailscaled pi-app --no-pager -l
journalctl -u tailscaled -u pi-app -f
systemctl restart pi-app
systemctl stop pi-app
```

Trong khi đang chờ giờ, tailscaled có thể hiện `activating (start-pre)`; app đang chờ Tailscale cũng hiện `activating (start-pre)`. Điều này là có chủ đích, không phải app đã chạy. SSH LAN vẫn dùng được nếu hệ thống mạng/SSH đã sẵn sàng.

Nếu app dùng virtualenv, tạo override:

```sh
systemctl edit pi-app
```

Nội dung, thay bằng đường dẫn Python thực:

```ini
[Service]
ExecStart=
ExecStart=/root/pi/.venv/bin/python -u /root/pi/app.py
```

## Giới hạn cần biết

- Chưa thử trên Pi thật; đã kiểm thử logic bằng mô phỏng, cú pháp shell và unit systemd.
- Cần systemd đang hoạt động, Python 3, GNU date, Tailscale đã cài, mạng ra UDP 123. Installer kiểm tra các điều kiện cơ bản; không tự cài dependency.
- SNTP thường không có xác thực mật mã. Script kiểm tra origin token, mode, stratum, leap status, độ trễ, khoảng năm và so sánh hai endpoint; điều đó không thay thế NTS. Hai endpoint Cloudflare có cùng nhà cung cấp. Nguồn IP trực tiếp tránh vòng phụ thuộc DNS Tailscale trong bước lấy giờ. DNS của Tailscale vẫn cần hoạt động sau đó.
- Đây là **đồng bộ khi khởi động tailscaled**, không phải daemon hiệu chỉnh đồng hồ liên tục. Không tắt/chỉnh các dịch vụ đồng bộ giờ có sẵn của DietPi. App đang chạy không bị dừng chỉ vì mạng mất tạm thời.
- Nếu toàn bộ mạng chặn NTP, chuỗi chờ thay vì khởi động với giờ sai. Không chỉ kiểm tra ping hay `network-online.target` vì các dấu hiệu đó không chứng minh Internet hoặc nguồn giờ hoạt động.
- Không sửa file app.py của bạn. App thiếu module, sai Python hoặc thiếu tài nguyên sẽ báo trong journal và thử khởi động lại.

## Gỡ chuỗi khởi động này

```sh
systemctl disable --now pi-app.service
rm /etc/systemd/system/tailscaled.service.d/20-pi-clock.conf
systemctl daemon-reload
```

Không stop/restart tailscaled khi đang SSH qua Tailscale. File unit/drop-in cũ nếu bị thay được lưu trong `/root/pi-startup-backup-*`; phục hồi từ bản backup đúng nếu cần. Script Python chưa bị xóa để tiện chẩn đoán.

## Kiểm thử

```sh
python3 -m unittest discover -s pi-startup/tests -v
bash -n pi-startup/install.sh
bash -n pi-startup/install-bundle.sh
```

Nguồn: [SNTP RFC 4330](https://www.rfc-editor.org/rfc/rfc4330.html), [Cloudflare NTP](https://developers.cloudflare.com/time-services/ntp/usage/), [tailscale up](https://tailscale.com/docs/reference/tailscale-cli/up).
