# AI Green — Pi Control

Ứng dụng desktop Python điều khiển Raspberry Pi bằng OpenSSH qua Tailscale. Chạy trên **máy tính**, không cần màn hình hay bàn phím cho Pi. Bản cơ bản, chưa xác minh với Pi thật. Không mở cổng web, không triển khai cloud, không cần API key.

## Chức năng

| Tab | Chức năng |
| --- | --- |
| Tổng quan | CPU, RAM, ổ đĩa gốc, nhiệt độ, uptime, load; đọc lại mỗi 5 giây khi không có thao tác khác |
| Services | Service systemd hệ thống: đang chạy, inactive, failed và unit chưa được load; tìm kiếm; start/stop/restart; enable/disable; 150 dòng journal |
| Thiết bị | USB, mic ALSA, đầu ra âm thanh, Bluetooth đang kết nối, mạng, Tailscale, các bus I²C và node UART/GPIO; bấm Quét lại để cập nhật |
| Cảm biến | Đọc snapshot JSON từ chương trình sở hữu cảm biến; hiển thị từng trường, null và tuổi dữ liệu; quá 15 giây đánh dấu cũ |
| Thu âm | Chọn thiết bị ALSA, thu 1–120 giây, mono S16_LE, lưu WAV trực tiếp trên máy tính |
| Lệnh & log | Chạy lệnh shell không tương tác trên Pi, tối đa 30 giây, hiển thị kết quả/lỗi |

Không thu/chụp/stream camera. Danh sách USB có thể chứa tên camera USB như một thiết bị được hệ điều hành nhận diện. Không tự quét địa chỉ I²C, reset cảm biến hoặc mở UART đang do app khác sử dụng. GPIO không có cơ chế nhận diện tự động mọi linh kiện gắn dây; chỉ giá trị do driver cung cấp mới xác nhận được hoạt động.

`not-loaded` nghĩa là unit có trên đĩa nhưng chưa được systemd load, không phải kết luận thiết bị hỏng. `enabled` nghĩa là được cấu hình khởi động, không đồng nghĩa đang chạy. Bản này chưa có trang riêng cho `systemctl --user` (có thể chạy lệnh này ở tab Lệnh).

## Chạy ngay khi chưa có Pi

Yêu cầu Python 3.10+ có Tkinter. Không có thư viện pip bắt buộc.

```sh
cd pi-control
python3 app.py --demo
```

Demo được đánh dấu rõ và không gửi lệnh đến Pi. Mở bản thật:

```sh
python3 app.py
```

Trên Windows dùng `py app.py`; cần OpenSSH Client trong PATH. macOS/Linux dùng `python3`. Kiểm tra GUI bằng `python3 -m tkinter`; nếu bản Python hiện tại thiếu Tkinter, dùng bản Python có Tk hỗ trợ. Linux Debian/Ubuntu chỉ khi thiếu mới cài `python3-tk`; không cần cài GUI trên Pi.

## Kết nối khi có Tailscale

1. Máy tính và Pi đăng nhập Tailscale, được ACL cho phép kết nối cổng SSH của Pi.
2. Pi đã chạy SSH server; chọn đúng user hiện hữu (ví dụ `dietpi` hoặc user bạn tự tạo).
3. Đăng nhập thử một lần từ Terminal, đối chiếu fingerprint máy Pi trước khi chấp nhận:

   ```sh
   ssh USER@TAILSCALE_IP
   ```

4. Thiết lập SSH key hoặc ssh-agent, rồi kiểm tra đăng nhập **không hỏi mật khẩu**:

   ```sh
   ssh -o BatchMode=yes USER@TAILSCALE_IP uptime
   ```

5. Trong ứng dụng nhập IP/hostname Tailscale, user, port (thường 22), đường dẫn private key nếu không dùng key mặc định/agent. Bấm Kết nối.

Giao diện sử dụng OpenSSH với `StrictHostKeyChecking=yes`: host chưa tin cậy, host đổi key hoặc xác thực thất bại sẽ báo lỗi trong tab Lệnh & log. Không tự chấp nhận host key; không lưu mật khẩu/private key. Chỉ lưu địa chỉ, user, port, **đường dẫn** key và telemetry trong `~/.pi-control.json`. Với Tailscale SSH cần hoàn tất xác thực/chính sách check trong Terminal trước nếu tailnet yêu cầu.

Không cần cung cấp auth key Tailscale cho ứng dụng. Tailscale chỉ lo kết nối mạng; SSH đảm nhiệm xác thực và thực thi.

## Quyền điều khiển service

Nút điều khiển dùng `sudo -n systemctl …`. Nếu user thiếu quyền hoặc sudo yêu cầu mật khẩu, ứng dụng báo lỗi; không tự sửa sudoers. Chỉ cấp các service và hành động thực sự cần. Ví dụ quản trị viên có thể dùng `sudo visudo -f /etc/sudoers.d/pi-control` để cấp **user thực của bạn** các lệnh tương ứng cho `thiennhan.service`. Không cấp `NOPASSWD: ALL` chỉ để dùng UI.

Nút stop/restart/disable khóa SSH, Tailscale và một số service mạng để tránh tự cắt kết nối. Tab chạy lệnh vẫn là shell thực, có thể thay đổi hệ thống theo quyền user; đọc lệnh và xác nhận trước khi chạy. Đây không phải sandbox. Không có nút tự reboot hay chạy apt update.

Nhật ký có thể thiếu nội dung nếu user không có quyền đọc journal. Nhóm `systemd-journal`/`adm` tùy hệ điều hành; quản trị viên quyết định quyền phù hợp.

## Dữ liệu cảm biến của dự án hiện tại

Repo `Pi 3/sensors.py` hiện cung cấp GY25 UART và MS5611 I²C. Pi Control không đổi driver, sơ đồ chân, bus, địa chỉ hoặc thuật toán của chúng. Đã thêm một bước **xuất telemetry tùy chọn** sau khi `read_sensors()` đọc xong; mặc định tắt nếu không đặt biến môi trường.

Trên Pi đang chạy app hiện tại, sau khi cập nhật đúng `sensors.py` vào `/opt/thiennhan`, thêm vào `/opt/thiennhan/.env`:

```dotenv
PI_CONTROL_TELEMETRY_PATH=/opt/thiennhan/history/telemetry.json
```

Chỉ cần restart `thiennhan.service` để nhận cấu hình; không cần reboot/cài lại toàn hệ thống. Có thể cập nhật có chọn lọc từ root repo (xác nhận đây đúng là bản app đang dùng trước):

```sh
sudo install -o thiennhan -g thiennhan -m 0644 'Pi 3/sensors.py' /opt/thiennhan/sensors.py
sudo systemctl restart thiennhan.service
```

Đường dẫn telemetry trên UI mặc định khớp ở trên. User SSH phải đọc được thư mục `/opt/thiennhan`, thư mục `history` và file telemetry (0640, owner/group là user chạy app). Với triển khai hiện có dùng nhóm `thiennhan`, quản trị viên có thể thêm user SSH vào nhóm đó rồi đăng nhập lại. Không đổi quyền `.env` hoặc cấp quyền đọc secret để giải quyết telemetry; nếu cần tách quyền hoàn toàn, đặt telemetry vào thư mục riêng có nhóm chỉ đọc riêng.

**Tần suất mẫu thật:** app hiện đọc cảm biến mỗi lần gửi lệnh giọng nói, chưa có vòng lấy mẫu cảm biến liên tục. UI đọc lại mỗi 5 giây không làm xuất hiện mẫu mới. Khi không có mẫu mới quá 15 giây, UI báo dữ liệu cũ. Muốn xem liên tục cần thêm publisher vào vòng lấy mẫu hiện tại sau khi xác minh cấu hình Pi; không chạy một driver thứ hai tranh chấp bus.

Dữ liệu có dạng:

```json
{
  "timestamp": 1791432000.0,
  "devices": {
    "imu": {"yaw": 0.0, "pitch": 1.2, "roll": -0.8},
    "pressure": {"pressure_pa": 101325.0, "temperature_c": 26.0, "altitude_m": 0.0}
  }
}
```

Đây là **ví dụ**, timestamp phải là thời gian Unix thực lúc lấy mẫu. Góc từ driver hiện tại là độ; áp suất Pa; nhiệt độ °C; độ cao m. `null` nghĩa là không đọc được mẫu, không khẳng định chắc chắn cảm biến bị tháo. File ghi bằng thay thế nguyên tử để UI không đọc nửa JSON; lỗi ghi không ngắt app chính.

Với MPU6050 I²C, VL53L1X, GPIO hoặc cảm biến mới, chương trình đang sở hữu driver cần xuất thêm trường vào `devices`, nên đặt đơn vị trong tên (`distance_mm`, `accel_x_ms2`, `button_pressed`). UI tự hiển thị cấu trúc này. Chưa giả định các thiết bị đó đang có trên Pi, chưa bổ sung driver phần cứng chưa xác minh.

## Thu âm và chạy lệnh

- Xem `arecord -l` tại tab Thiết bị, chọn ALSA `default` hoặc `plughw:CARD=...,DEV=0` phù hợp.
- App Thiên Nhãn giữ mic mở liên tục. Nếu mic báo busy, chủ động dừng `thiennhan.service`, thu thử, rồi chạy lại service. Pi Control không tự dừng service để giành mic.
- Bấm Thu âm, chọn nơi lưu WAV, đợi hết thời lượng. Dữ liệu đi trong SSH; không lưu bản ghi tạm trên Pi.
- Pi cần `arecord` (ALSA) và `timeout` (coreutils), user SSH có quyền audio. Bản cơ bản thu mono, không chọn số kênh khác và không có nút hủy giữa chừng; chọn thời lượng ngắn để thử trước.
- Lệnh không tương tác: dùng `sudo -n` nếu đã có quyền, tránh `sudo` hỏi mật khẩu. Không chạy tác vụ daemon/background qua ô lệnh nếu cần quản lý vòng đời; dùng service.

## Kiểm thử và giới hạn

```sh
python3 -m unittest discover -s pi-control/tests -v
cd 'Pi 3'
python3 -m unittest discover -s tests -v
```

Kiểm thử mới bao gồm chống chèn lệnh ở trường service/host, bảo vệ service kết nối, unit chưa load, lỗi systemctl/SSH/timeout, ghi telemetry nguyên tử và dữ liệu cũ/lỗi, giới hạn thu âm và quoting thiết bị.

Chưa kiểm thử end-to-end trên Pi thật, SSH/Tailscale thật, âm thanh thật; môi trường xây dựng không có display để kiểm tra trực quan Tkinter. Mã đã được compile và test logic. Sau khi có IP Tailscale + user SSH + cách xác thực, cần xác nhận bus/cảm biến, quyền systemd và thiết bị audio đang dùng trước khi kết luận vận hành hoàn chỉnh.

Tham khảo: [OpenSSH ssh_config](https://man.openbsd.org/ssh_config.5), [systemctl](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html).
