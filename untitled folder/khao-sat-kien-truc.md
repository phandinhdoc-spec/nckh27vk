# Khảo sát kiến trúc NCKH27VK — trạng thái tiến độ

Ngày: 2026-09-23. Phiên Hermes. KHÔNG sửa code, KHÔNG copy sang PiEnd/ServerEnd (cả hai
hiện rỗng). Tài liệu này là kết quả trung gian để tiếp tục nếu phiên bị ngắt.

## Mục tiêu kiến trúc chính thức (từ 2026-09-23)
- Server xử lý toàn bộ tác vụ nặng AI.
- Pi CHỈ: nhận lệnh/ngữ liệu; gửi lên Server; bật camera/chụp ảnh khi cần; gửi ảnh; nhận MP3; phát MP3.
- Pi KHÔNG tự chạy model AI nặng.
- Server: hiểu yêu cầu; điều phối AI/model/API; xử lý ảnh; tạo nội dung; TTS→MP3; trả MP3.

## Cặp runtime CHÍNH = `Pi 2/` + `Server/` (khớp 100% mục tiêu)

### Server (Mac) — `Server/Sources/ThienNhanServer/`
| File | Vai trò | Bằng chứng |
|---|---|---|
| main.swift (13) | Entry `@main` → `Server.run(config: AppConfig.load())` | dòng 7 |
| Config.swift | Đọc .env: host/port/token, Groq key+model, Gemini keys+4 model, timeout | dòng 30-68 |
| Server.swift | Lắp router+engines, đăng ký route, `validateBearerToken` | dòng 45-95 |
| STT/SpeechEngine.swift | Groq Whisper STT multipart, chống hallucination, timeout | dòng 50-149 |
| STT/STTRoutes.swift | POST /stt; lưu audio; gọi plan() Gemini định mode/needsImage | dòng 39-59 |
| STT/AudioArchive.swift | Lưu WAV vào `wavpi/`, giữ 30 ngày | dòng 8-35 |
| Gemini/GeminiEngine.swift | Gọi Gemini generateContent; 4 model (fast/vision/reasoning/fallback); image inline | dòng 74-302 |
| Gemini/GeminiRoutes.swift | POST /gemini (classification) | dòng 37-87 |
| Vision/VisionRoutes.swift | POST /vision/ocr; Apple Vision OCR (vi-VN/en-US) | dòng 34-131 |
| TTS/TTSRoutes.swift | POST /tts; `/usr/bin/say` + `lame` → MP3; header text base64 | dòng 60-140 |
| Command/CommandRoutes.swift | POST /command; mode local/chat/ocr/observe; routing camera; à TTS MP3 | dòng 42-176 |

### Pi Zero 2 W — `Pi 2/`
| File | Vai trò | Bằng chứng |
|---|---|---|
| app.py | Main loop: button GPIO25 → record WAV → transcribe → capture nếu needsImage → command → play MP3 → history | dòng 53-113 |
| devices.py | wait_for_button(25), record_wav (arecord SCO 8k), capture_jpeg (rpicam-jpeg /dev/shm), play_mp3 (mpg123), bluetooth | dòng 26-310 |
| mac_client.py | HTTP POST /stt + /command, Bearer, gửi ảnh base64, nhận MP3+text | dòng 30-69 |
| config.py | Đọc .env: server_url, token, MAC, các ngưỡng | dòng 31-60 |
| history.py | Lưu ảnh/mp3, dọn theo CPU/RAM | dòng 35-120 |
| play-audio | Route .mp3→MAX98357A (mpg123), .wav→bluetooth A2DP (aplay) | dòng 40-51 |
| setup_pi2w.sh | Cài hệ thống: bluealsa, camera, MAX98357A, service | toàn file |
| thiennhan.service | systemd: ExecStart app.py, Restart=on-failure | dòng 14-15 |
| tests/test_runtime.py, test_deployment.py | Unit test runtime + deployment | toàn file |

## CODE CŨ / TRÙNG / KHÔNG DÙNG TRONG KIẾN TRÚC MỚI
- `Bai du thi/TP/` = Green Eye (phân loại rác), pipeline KHÁC, không thuộc mục tiêu:
  - `TP/Pi/app.py`: button GPIO17 → chụp → POST /classify → phát MP3 cố định (RHC/RVC/RNH/RKH/RK).
  - `TP/Mac/Sources/GreenEyeServer/main.swift`: dùng Apple FoundationModels, chỉ /classify, không STT/TTS/Gemini.
- `Server/dictation_fixed.swift`: prototype độc lập dùng DictationTranscriber; KHÔNG nằm trong Package.swift target → không được build. Thử nghiệm STT Apple, thay thế bằng Groq trong SpeechEngine.
- `Server/root@192.168.2.21` ≡ `Server/setup_pi2w.sh` (giống hệt, MD5 khác nhau) — snapshot deploy; chỉ khác HEADSET_MAC (41:42 vs E0:1A).
- `Server/setup_pi2w.sh` + `Server/play-audio.sh` = bản cũ của script Pi (bản hợp lệ nằm ở `Pi 2/`, test_deployment xác nhận HEADSET_MAC=04:60:61:EF:78:22, không có 41:42/E0:1A).
- `Server/play-audio.sh` = 1 byte rỗng, file rác/trùng (bản thật: `Pi 2/play-audio`).
- `Server/wavpi/` = thư mục runtime của AudioArchive (nhiều file .wav thu). Data, không phải code.
- `Server/extracted_text.txt`, `Server/nhan-xet.md` = dữ liệu/tài liệu, không phải runtime.

## GỢI Ý CHO BƯỚC TIẾP (chưa thực hiện, cần user xác nhận)
Toàn bộ năng lực mục tiêu ĐÃ tồn tại trong `Pi 2/` + `Server/`. Bước tiếp hợp lý:
1. Xác định bộ chuyển/bản sao vào PiEnd/ServerEnd theo thứ tự phụ thuộc (không được copy khi chưa được phép).
2. Loại rác: file play-audio.sh rỗng, snapshot root@..., wavpi cũ, dictation_fixed.swift, TP/ Green Eye.
3. Xác định chỗ trống so với mục tiêu chính thức trước khi viết mới.

## E2E TEST SERVER (Mac host, 2026-09-23) — ĐÃ VERIFY
Server chạy thật trên Mac này (0.0.0.0:8765, binary .build/debug/ThienNhanServer).
- swift build: OK (exit 0). swift test: KHÔNG chạy được — máy chỉ có CommandLineTools, thiếu Xcode/XCTest. Chấp nhận, dựa vào build+e2e.
- /tts: OK — MP3 64kbps 22kHz mono, HTTP 200 (say Linh + lame).
- /gemini chat: OK sau khi sửa model (trước: 404 vì gemini-2.5-flash deprecated).
- /vision/ocr: OK — HTTP 200, nhận text + confidence 1.0 (Apple Vision, không cần API).
- /stt: OK — Groq Whisper nhận dạng đúng tiếng Việt, mode=chat, needsImage=false.
- /command chat: OK — Gemini ra text + TTS MP3, header X-ThienNhan-Text-Base64 đúng.
- /command observe (có ảnh): OK — Gemini vision mô tả vật thể + TTS MP3.

QUAN TRỌNG — .env Server đang dùng model deprecated:
- .env có 4 dòng GEMINI_MODEL_* đều = gemini-2.5-flash → Google trả 404 (model hết hạn).
- Key vẫn sống. Đã sửa (theo user duyệt) cả 4 dòng sang 'gemini-3.6-flash' để test chạy.
- Backup .env trước khi sửa: /tmp/tn_env_backup_*.env (CHỈ tồn tại trong phiên; nếu cần giữ lâu phải copy an toàn).
- Chưa move code sang PiEnd/ServerEnd (đúng quy trình: chỉ move sau khi test phần cứng Pi ổn định).
- Pi phần cứng (GPIO25/SCO/camera/MAX98357A) do USER tự test bằng tay; tôi chỉ chuẩn bị file/thư mục.

## File đã đọc (bằng chứng)
Pi 2: app.py, config.py, devices.py, mac_client.py, history.py, test_camera.py, play-audio,
setup_pi2w.sh, thiennhan.service, tests/*.py
Server: main.swift, Config.swift, Server.swift, STT/{SpeechEngine,STTRoutes,AudioArchive}.swift,
Gemini/{GeminiEngine,GeminiRoutes}.swift, TTS/TTSRoutes.swift, Vision/VisionRoutes.swift,
Command/CommandRoutes.swift, Package.swift, dictation_fixed.swift, .hermes.md
TP: Pi/app.py, Mac/Sources/GreenEyeServer/main.swift
Index coverage 13 file chính: đều no_recorded_issue.