# Green Eye — Mac server

Server Swift nhận JPEG từ Pi, dùng mô hình Apple Intelligence trên thiết bị qua framework `FoundationModels` để phân loại ảnh và trả một mã JSON.

Không dùng Siri, Vision heuristic hoặc dịch vụ AI bên ngoài. Ảnh chỉ được giữ trong bộ nhớ để xử lý request, không được server ghi ra đĩa.

## Chạy

Yêu cầu:

- macOS 27 trở lên và Swift 6.4;
- máy Mac hỗ trợ Apple Intelligence;
- Apple Intelligence đã được bật và mô hình đã tải xong.

```sh
swift build
swift run GreenEyeServer
```

Mặc định server nghe tại `0.0.0.0:8765`. Có thể đổi bằng:

```sh
GREEN_EYE_HOST=127.0.0.1 GREEN_EYE_PORT=8765 swift run GreenEyeServer
```

## API

```sh
curl http://127.0.0.1:8765/health
curl -X POST -H 'Content-Type: image/jpeg' \
  --data-binary @anh.jpg http://127.0.0.1:8765/classify
```

Response:

```json
{"code":"RHC"}
```

`/health` phải chứa `apple_intelligence=available`.

Mã hợp lệ: `RHC`, `RVC`, `RNH`, `RKH`, `RK`. Ảnh lỗi, Apple Intelligence không khả dụng, model trả nhiều mã hoặc kết quả không chắc chắn đều được chuẩn hóa an toàn thành `RK`.

Thứ tự ưu tiên an toàn trong prompt là `RKH` → `RNH` → `RHC`/`RVC` → `RK`.

## Kiểm tra

```sh
swift build
swift run GreenEyeServer --self-test
```

Kết quả mong đợi:

```text
self-test: ok; Apple Intelligence: available
```

## Cấu trúc tối thiểu

```text
Package.swift
Sources/GreenEyeServer/main.swift
```