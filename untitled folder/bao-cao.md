# Báo cáo rà soát cấu trúc project NCKH27VK

## 1. Tổng quan

Đây không phải một project đơn lẻ theo nghĩa thông thường mà là một workspace gồm:

- Mã nguồn hệ thống Thiên Nhãn hiện tại.
- Một phiên bản Green Eye/Thiên Nhãn cũ hoặc song song.
- Hồ sơ dự thi, tài liệu, video, hình ảnh, PDF và dữ liệu OCR.
- Hai client Raspberry Pi khác nhau.
- Hai server Swift khác nhau.

Thống kê filesystem:

- 338 file sau khi loại `.git`, `__pycache__`, `.build`, `tmp`.
- 17 file Swift.
- 11 file Python.
- 4 script shell.
- 23 file Markdown.
- 7 file Typst.
- Nhiều tài liệu nhị phân: PNG, JPG, MP3, WAV, PDF, DOCX, MP4.
- Thư mục gốc hiện không phải Git repository.
- `Server/` có Git repository riêng và đang chứa nhiều file chưa được commit.

## 2. Cây cấu trúc chính

```text
NCKH27VK/
├── Pi 2/
│   ├── app.py
│   ├── config.py
│   ├── devices.py
│   ├── history.py
│   ├── mac_client.py
│   ├── test_camera.py
│   ├── setup_pi2w.sh
│   ├── play-audio
│   ├── thiennhan.service
│   ├── sounds/
│   └── tests/
│       ├── test_runtime.py
│       └── test_deployment.py
│
├── Server/
│   ├── Package.swift
│   ├── README.md
│   ├── .env.example
│   ├── Sources/
│   │   └── ThienNhanServer/
│   │       ├── main.swift
│   │       ├── Config.swift
│   │       ├── Server.swift
│   │       ├── Command/
│   │       │   └── CommandRoutes.swift
│   │       ├── Gemini/
│   │       │   ├── GeminiEngine.swift
│   │       │   └── GeminiRoutes.swift
│   │       ├── STT/
│   │       │   ├── SpeechEngine.swift
│   │       │   ├── STTRoutes.swift
│   │       │   └── AudioArchive.swift
│   │       ├── TTS/
│   │       │   └── TTSRoutes.swift
│   │       └── Vision/
│   │           └── VisionRoutes.swift
│   ├── Tests/
│   │   └── ThienNhanServerTests/
│   │       ├── AudioArchiveTests.swift
│   │       └── CommandPlanTests.swift
│   ├── Docs/
│   │   ├── 00_PROJECT.md
│   │   ├── 01_PRODUCT_TASKS.md
│   │   ├── 02_ARCHITECTURE.md
│   │   ├── 03_PI_RESPONSIBILITIES.md
│   │   ├── 04_MAC_SERVER.md
│   │   ├── 05_API.md
│   │   ├── 06_GEMINI_ROUTING.md
│   │   ├── 07_RUNTIME_FLOW.md
│   │   ├── 08_SECURITY.md
│   │   ├── 09_TEST_PLAN.md
│   │   ├── 10_ROADMAP.md
│   │   └── các tài liệu thiết kế/nhật ký/đánh giá
│   ├── dictation_fixed.swift
│   ├── setup_pi2w.sh
│   ├── play-audio.sh
│   └── nhan-xet.md
│
├── Bai du thi/
│   ├── thien-nhan.typ
│   ├── thien-nhan.pdf
│   ├── temp.typ
│   ├── Van ban/
│   ├── images/
│   └── TP/
│       ├── README.md
│       ├── bao-cao-du-thi-toan-quoc.typ
│       ├── green-eye.typ
│       ├── green-eye.pdf
│       ├── references.bib
│       ├── image/
│       ├── video quay toan quoc/
│       ├── ocr_national/
│       ├── code/
│       ├── Pi/
│       │   ├── app.py
│       │   ├── setup_pi2w.sh
│       │   ├── green-eye.service
│       │   └── audio/
│       └── Mac/
│           ├── Package.swift
│           ├── Package.resolved
│           ├── README.md
│           └── Sources/
│               └── GreenEyeServer/
│                   └── main.swift
│
└── van ban/
```

## 3. Nhánh `Server/`: hệ thống Thiên Nhãn hiện tại

Đây là server Swift chạy trên MacBook, sử dụng:

- Swift 6.4.
- macOS 26 trở lên theo `Package.swift`.
- Hummingbird 2.x.
- Bearer Token.
- Groq Whisper/STT.
- Gemini.
- Apple Vision OCR.
- Apple Speech/TTS.
- LAME để mã hóa MP3.

Package đã được kiểm tra bằng `swift package dump-package`:

```text
Package: ThienNhanServer
Product: ThienNhanServer
Targets:
- ThienNhanServer
- ThienNhanServerTests
```

Entry point:

```text
Server/Sources/ThienNhanServer/main.swift
```

Luồng khởi động:

```text
main.swift
  → AppConfig.load()
  → Server.run()
  → khởi tạo Router, SpeechEngine, GeminiEngine, AudioArchive
  → đăng ký các route
  → chạy Hummingbird
```

Các endpoint được tài liệu hóa:

```text
GET  /health
POST /stt
POST /gemini
POST /vision/ocr
POST /tts
POST /command
```

Luồng chính:

```text
Pi thu WAV
  → POST /stt
  → server trả text, mode, command, needsImage
  → nếu cần ảnh, Pi chụp JPEG
  → POST /command
  → Vision/Gemini xử lý
  → TTS tạo MP3
  → trả MP3 về Pi
```

Các module có ranh giới tương đối rõ:

- `STT`: nhận dạng giọng nói, phân tích lệnh và lưu audio.
- `Gemini`: gọi Gemini và xử lý nội dung hình ảnh/ngôn ngữ.
- `Vision`: OCR bằng Apple Vision.
- `TTS`: chuyển văn bản thành MP3.
- `Command`: điều phối các chức năng trên.
- `Config`: đọc cấu hình và biến môi trường.
- `Server`: lắp ráp router, engine và middleware xác thực.

## 4. Nhánh `Pi 2/`: client Raspberry Pi hiện tại

`Pi 2` là client Python tương đối hoàn chỉnh cho Raspberry Pi Zero 2 W.

Các trách nhiệm chính:

```text
app.py
  → đọc Config
  → kiểm tra Wi-Fi
  → kiểm tra camera
  → kết nối Bluetooth
  → chờ button GPIO25
  → ghi WAV qua Bluetooth SCO
  → gọi MacClient.transcribe()
  → chụp ảnh nếu server yêu cầu
  → gọi MacClient.command()
  → phát MP3
  → lưu history
```

Các module:

- `config.py`: cấu hình từ `.env`.
- `devices.py`: Wi-Fi, camera, Bluetooth, GPIO, ghi âm và phát audio.
- `mac_client.py`: HTTP client giao tiếp với server Mac.
- `history.py`: lưu trữ lịch sử ảnh và âm thanh, có cơ chế dọn dữ liệu.
- `test_camera.py`: kiểm tra camera và môi trường thiết bị.
- `setup_pi2w.sh`: cài đặt hệ thống, BlueALSA, camera, MAX98357A và service.
- `thiennhan.service`: systemd service.
- `sounds/`: các âm thanh hướng dẫn và trạng thái.
- `tests/`: test runtime và deployment.

Kiến trúc phần cứng được tài liệu hóa:

- Button: GPIO25.
- Micro: Bluetooth SCO, CVSD mono 8 kHz.
- Loa: MAX98357A qua I2S.
- Phát MP3: `mpg123`.
- Phát WAV thủ công: `aplay`.
- Giao tiếp Mac: HTTP qua Tailscale.
- WAV chỉ giữ trong RAM.
- JPEG và MP3 được lưu vào `history/` theo chính sách thời gian.

## 5. Nhánh `Bai du thi/TP/`: phiên bản Green Eye/song song

Đây là một line triển khai đơn giản hơn:

```text
Bai du thi/TP/Pi/app.py
  → chờ button GPIO17
  → chụp ảnh bằng rpicam-jpeg
  → POST /classify
  → nhận một trong các mã:
      RHC, RVC, RNH, RKH, RK
  → phát file MP3 tương ứng
```

Server tương ứng:

```text
Bai du thi/TP/Mac/
├── Package.swift
├── README.md
└── Sources/GreenEyeServer/main.swift
```

Package đã được kiểm tra:

```text
Package: GreenEyeServer
Targets:
- GreenEyeServer
```

Line này khác đáng kể với `Server/` hiện tại:

- Chỉ có endpoint `/health` và `/classify`.
- Không có STT.
- Không có TTS động.
- Không có Gemini route.
- Không có OCR route.
- Server nhận ảnh rồi phân loại thành mã cố định.
- Pi phát các file MP3 dựng sẵn.
- Dùng Apple Intelligence/`FoundationModels` theo tài liệu.
- Button mặc định là GPIO17, trong khi `Pi 2` dùng GPIO25.

## 6. Khu vực tài liệu và dữ liệu

`Bai du thi/` chủ yếu là hồ sơ và tài sản truyền thông:

- Báo cáo Typst.
- PDF đã biên dịch.
- DOC/DOCX biểu mẫu và thuyết minh.
- Hình ảnh sản phẩm, sơ đồ, kết quả thực nghiệm.
- Video giới thiệu và hướng dẫn.
- Dữ liệu OCR.
- `references.bib`.
- Các file text trích xuất từ DOCX/PDF.

Khu vực này chứa phần lớn số lượng file của project nhưng không phải phần runtime chính.

## 7. Quan hệ giữa các thành phần

Có thể mô tả kiến trúc hiện tại như sau:

```text
Người dùng
  ↓
Button + microphone + camera
  ↓
Raspberry Pi Zero 2 W
  ├─ devices.py
  ├─ app.py
  ├─ mac_client.py
  └─ history.py
        ↓ HTTP/Tailscale + Bearer Token
MacBook
  ├─ Hummingbird
  ├─ SpeechEngine
  ├─ GeminiEngine
  ├─ Apple Vision OCR
  ├─ TTS
  └─ CommandRoutes
        ↓
MP3/JSON response
        ↓
Raspberry Pi phát âm thanh
```

Bên cạnh đó tồn tại một luồng cũ/đơn giản hơn:

```text
Pi/Green Eye
  → chụp JPEG
  → GreenEyeServer /classify
  → mã RHC/RVC/RNH/RKH/RK
  → MP3 cố định
```

## 8. Kết quả lập chỉ mục cấu trúc

Codebase Memory đã lập chỉ mục project với:

- 962 node.
- 2.310 quan hệ.
- 117 function.
- 94 method.
- 39 class.
- 39 struct.
- 70 file mã nguồn/tài liệu có cấu trúc.
- Ngôn ngữ chính được phát hiện:
  - Swift.
  - Python.
  - Bash.

Các cụm cấu trúc nổi bật:

- Cụm `Pi 2`: runtime audio, camera, button và client.
- Cụm `Server`: route, engine và xử lý request.
- Cụm `Bai du thi/TP`: Green Eye và tài liệu cuộc thi.
- Cụm test riêng cho `Pi 2` và `Server`.

## 9. Điểm cần lưu ý

- Project gốc không có Git repository; lịch sử phiên bản không được quản lý ở cấp root.
- `Server/` là Git repository riêng và hiện có nhiều file chưa commit.
- Có hai kiến trúc server khác nhau:
  - `Server/ThienNhanServer`: pipeline STT → command → Vision/Gemini → TTS.
  - `Bai du thi/TP/Mac/GreenEyeServer`: image classification → mã cố định → MP3.
- Có hai client Pi khác nhau:
  - `Pi 2/`: GPIO25, Bluetooth audio, STT và command.
  - `Bai du thi/TP/Pi/`: GPIO17, chụp ảnh trực tiếp và `/classify`.
- Tên gọi “Thiên Nhãn” và “Green Eye” đang cùng tồn tại.
- Có nhiều bản PDF, video, ảnh và thư mục build/OCR nằm chung với mã nguồn, khiến root project khá khó phân biệt giữa source, artifact và tài liệu.
- Codebase Memory ghi nhận hai vùng parse partial:
  - `Server/Sources/ThienNhanServer/STT/SpeechEngine.swift`, dòng 277–279.
  - `Server/nhan-xet.md`, dòng 638–639.
  Đã đọc trực tiếp các vùng này; chúng không làm thay đổi kết luận kiến trúc.
- Các file `.env`, `.build`, `.git`, cache và nhiều ảnh đã bị loại khỏi graph theo chủ ý; chúng vẫn tồn tại trên filesystem.

## Kết luận

Phần runtime có tổ chức tốt nhất hiện nay là cặp `Pi 2/` + `Server/`. `Bai du thi/TP/` nên được xem là khu vực hồ sơ dự thi chứa một implementation Green Eye riêng, không nên mặc định coi là cùng một pipeline với `Server/`.
