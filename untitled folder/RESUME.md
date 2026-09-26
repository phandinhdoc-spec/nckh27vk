# RESUME — NCKH27VK (cập nhật 2026-09-25)

## ĐÃ HOÀN TẤT (kiểm chứng 2026-09-25)
Toàn bộ "VIỆC ĐANG LÀM" và "Next actions" liên quan tới `Pi 3/` đã xử lý xong và có bằng chứng kiểm chứng cục bộ (chưa xác minh trên phần cứng thật).

- **MS5611 (sensors.py)**: sửa công thức bù theo datasheet — `dT=D2-(C5<<8)`, `TEMP=2000+((dT*C6)>>23)`, `OFF=(C2<<16)+((C4*dT)>>7)`, `SENS=(C1<<15)+((C3*dT)>>8)`, bù bậc 2 khi `TEMP<2000` (và nhánh `TEMP<-1500`), `P=(((D1*SENS)>>21)-OFF)>>15` (đơn vị 0.01 mbar = Pa). Vector datasheet khớp: D1=9085466, D2=8569150 → `pressure_pa=100009.0`, `temperature_c=20.07`.
- **MS5611 PROM**: thêm CRC-4 (thuật toán AN520), kiểm tra byte-order `read_word_data` (smbus2 trả little-endian → driver swap lại đúng). CRC sai → `OSError` → `read_ms5611` trả `None`.
- **GY25 (sensors.py)**: đọc bị chặn thời gian (`_GY25_READ_TIMEOUT=0.05`, tổng `_GY25_MAX_FRAMES_WAIT=0.3`), tách `_gy25_next_frame` để bỏ nhiễu/đồng bộ lại frame.
- **config.py**: giữ nguyên; bổ sung test defaults/override/invalid (hex, bool, int, khoảng giá trị).
- **app.py / test**: `_read_sensor_payload` + `command(..., sensor=...)` (4 args); test `SimpleNamespace` đã thêm 5 field sensor; test startup không block khi tai nghe lỗi; test payload.
- **setup_pi2w.sh**: thêm `configure_sensor_boot` (`enable_uart=1`, `dtparam=i2c_arm=on`), cài `python3-serial`/`python3-smbus2`, thêm group `dialout`/`i2c`, deploy `sensors.py`; WiFi fallback idempotent + `chmod 0600` + chỉ khi `wpa_supplicant` active + `priority=-5` (không khẳng định auto-failover).
- **README.md**: chỉ nêu điều thực sự triển khai.
- **Bluetooth retries (cập nhật tiếp)**: `setup_pi2w.sh` tối đa 2 lượt pairing/connect; nếu thất bại thì bỏ qua A2DP test và tiếp tục cài bằng loa MAX98357A. `app.py` khi startup cũng chỉ thử 2 lần. README/test_deployment cập nhật tương ứng.
- **Kiểm chứng**: `python3.11 -m unittest discover -s tests` → **41 tests, OK**; `py_compile` cho các module + `bash -n setup_pi2w.sh` → OK.
- **Git**: `Pi 3/` và thư mục cha `NCKH27VK` đều **không phải Git repo** (không có `.git`; chỉ có `.gitignore`), nên không có `git diff` để báo.

## Cách tiếp tục
Đọc file này rồi tiếp tục công việc đang dở ở “VIỆC ĐANG LÀM”. Người dùng đã duyệt kế hoạch grilled và yêu cầu Hermes tự làm tiếp toàn bộ sau duyệt; không cần hỏi lại kế hoạch.

## Mục tiêu kiến trúc (đã chốt)
- Server làm mọi tác vụ AI nặng; Pi không chạy AI nặng.
- Runtime hiện tại: `Pi 3/` + `Server/`. Không move sang PiEnd/ServerEnd khi chưa được cho phép.
- Không sửa Server/Mac trong tác vụ này; chủ yếu cập nhật Pi 3.
- Quy trình `Server/.hermes.md`: test, kiểm diff/status, không commit secret; commit/push `main` chỉ sau khi hoàn thành/verify. Chú ý `Pi 3/` hiện không phải Git repo.

## Hiện trạng đã xác minh trước khi sửa
- `Pi 3/` đã có mic USB 16 kHz, output A2DP + loa MAX fallback trong runtime, timeout tách riêng.
- Baseline: `/opt/homebrew/bin/python3.11 -m unittest discover -s tests` → 11 tests, OK.
- Chưa có GY25/GY63 sensor code, wifi dự phòng; `app._startup()` trước đó retry Bluetooth trong `while True`.
- `Pi 3/.env.example` được dùng; không sửa `.env` chứa cấu hình/secret qua file tool.
- GY25 frame từ tài liệu tìm được: 8 bytes, 0xAA, yaw/pitch/roll từng signed 16-bit big-endian, kết thúc 0x55; scale 0.01 degree.

## CMD orchestration
- run_id: `run_20260925_102816_f7aa7e`
- Prompt được chọn: grilled.
- Kế hoạch task→work_unit→step đã capture (9 WU), người dùng đã duyệt “Duyệt, thực thi toàn bộ với deepseek-v4-pro/flash như trên”.
- CMD plan: T1 sensors, T2 BT fallback + WiFi Pdmq, T3 README/tests/verification. Không cần hỏi duyệt lại.
- Live CommandCode models lúc capture: deepseek-v4-flash, deepseek-v4-pro, mimo-v2.5-pro, GLM-5.1 (Muse v1.3/MiMo 2.6/GLM 5.3 chưa xuất hiện trong live list).

## VIỆC ĐANG LÀM — chưa hoàn tất / chưa verify
Đã sửa các file sau trong `/Users/phananh/TEMP/NCKH27VK/Pi 3/`:
1. `sensors.py` (mới): GY25 UART parser/reader, MS5611 I2C reader, combined `read_sensors`.
2. `config.py`: fields `gy25_device`, `gy25_baud`, `ms5611_bus`, `ms5611_addr`, `ms5611_enabled`; helpers `_hex`, `_bool`.
3. `.env.example`: GY25/MS5611 config keys.
4. `mac_client.py`: `command(..., sensor=...)` adds `sensor` to JSON.
5. `app.py`: import `read_sensors`; add `_read_sensor_payload`; attach sensor to command; startup Bluetooth no longer loops forever (attempts twice, continues to speaker fallback).
6. `setup_pi2w.sh`: `configure_wifi_fallback()` appends Pdmq/12345678 to `/etc/wpa_supplicant/wpa_supplicant.conf`; called from main. This implementation may need reconsideration: Pi setup is DietPi and primary WiFi may not use wpa_supplicant; check actual DietPi network manager and avoid claiming guaranteed auto-failover. Also UART/I2C boot config and dependencies (pyserial, smbus2) are NOT yet wired into setup script.
7. `README.md`: replaced stale SCO/CVSD mic docs with USB mic, BT fallback, GY25/GY63 and WiFi notes. README currently has potentially inaccurate claims that setup enables UART/I2C and that Pdmq auto-failover works; reconcile with actual script before finalizing.

## Important correctness concerns to resolve next
- MS5611 implementation needs verification against datasheet/reference driver. Current compensation code in `sensors.py` is likely wrong: `off` and `sens` are computed but not used in pressure calculation; standard formula uses D1, OFF, SENS, pressure = (((D1*SENS)>>21)-OFF)>>15, with second-order compensation below 20°C. Fix and unit-test using known/reference vectors.
- `_MS5611._read_prom()` uses `read_word_data`; verify byte order and CRC handling. Add PROM CRC-4 check if feasible.
- `read_gy25()` currently reads `serial.Serial` with timeout 0.4s in loop up to ~0.6s; this may stall per sensor request. Avoid slow repeated opens; bounded reads and optional disable config.
- `config.py` field additions mean all `SimpleNamespace` configs in `tests/test_runtime.py` need new fields or tests fail. Add tests for defaults/override/invalid config.
- Existing test expecting `client.command.assert_called_once_with(text, None, "auto")` will fail because app now passes sensor as 4th positional arg; update test expectation.
- `_startup` currently successful headset startup emits ready tone on MAX; final runtime must ensure audio routing/fallback semantics make sense.
- WiFi fallback security: password is explicitly user-provided, but test/source docs should avoid printing beyond required setup. Implement idempotently, protect wpa_supplicant file permissions, use correct network stack, handle configuration without overwriting existing networks.
- Setup script does NOT yet configure UART/I2C, install `python3-serial`/`python3-smbus2`, or grant serial group permissions.
- `README.md` describes `Pi 3/` but only claims verified facts.
- No sensor data is consumed by Server yet (user asked attach payload; backend changes were excluded). Clearly state this only adds payload, not server-side fall/altitude behavior.

## Next actions
1. (Còn lại) Xác minh trên phần cứng thật (Pi Zero 2 W + GY25/GY63): chưa thể làm từ máy này; chỉ có unit test mock.
2. (Còn lại) Xác định phạm vi Git trước khi push: `Pi 3/` và `NCKH27VK` đều không có `.git`; không commit/push `Server/` ngoài phạm vi.
3. (Còn lại) Cập nhật tiến độ CMD work-unit (`cmd_unit_update`) bằng bằng chứng thật (41 tests OK, py_compile, bash -n).
4. (Còn lại) Cập nhật skill `thien-nhan-device` sau khi có quy trình cuối đáng tin; đồng bộ tham chiếu Pi 2 ↔ Pi 3.

