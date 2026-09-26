# Thiết kế kiến trúc Python

## 1. Phạm vi và nguyên tắc

Tài liệu này là đặc tả thiết kế, không phải mã triển khai. Coder sẽ hiện thực hệ thống nhận diện rác trên Raspberry Pi theo chu trình: chờ nhấn công tắc, chụp JPEG, gửi ảnh đến Gemini, kiểm tra câu trả lời, phát MP3, xóa ảnh tạm và chờ nhả công tắc.

Các nguyên tắc bắt buộc:

- GPIO dùng chế độ BCM: `GPIO25`, tương ứng physical pin 22; công tắc nối về GND physical pin 20; dùng pull-up nội bộ.
- Trạng thái nhấn là LOW, trạng thái nhả là HIGH; debounce trong khoảng 50–150 ms.
- Model Gemini là `gemini-2.5-flash-lite`.
- API key để trống trong thiết kế, chỉ nhận từ biến môi trường khi triển khai; tuyệt đối không ghi key vào mã nguồn hoặc log.
- Chỉ phát MP3 khi câu trả lời khớp chính xác một trong 36 câu đã quy định.
- Không dùng suy đoán gần đúng để chọn MP3.
- Ảnh tạm phải được xóa trong nhánh dọn dẹp, kể cả khi xử lý thất bại.

## 2. Các file Python cần có

| File | Trách nhiệm |
|---|---|
| `main.py` | Khởi tạo ứng dụng, kiểm tra cấu hình, điều phối vòng lặp xử lý một lượt nhấn. |
| `config.py` | Tập trung hằng số, đọc cấu hình môi trường và tạo cấu hình bất biến cho các module. |
| `button.py` | Khởi tạo GPIO25, phát hiện nhấn/nhả, debounce và giải phóng GPIO. |
| `camera.py` | Gọi `rpicam-jpeg`, tạo ảnh JPEG ở thư mục tạm và báo lỗi chụp. |
| `gemini_client.py` | Tạo request multipart nội dung JSON/ảnh, gọi Gemini, timeout, retry và trích text. |
| `messages.py` | Danh sách 36 câu hợp lệ, ánh xạ cố định câu–MP3, chuẩn hóa tối thiểu và fallback. |
| `audio.py` | Kiểm tra đường dẫn MP3 và phát âm thanh qua trình phát hệ thống đã chọn. |
| `requirements.txt` | Khai báo thư viện bên ngoài cần cho triển khai; không chứa API key. |

Không tạo `*.py` chạy được trong phạm vi tài liệu này.

## 3. Import cần dùng theo module

Danh sách dưới đây là định hướng import, không phải mã triển khai hoàn chỉnh.

| Module | Import cần dùng |
|---|---|
| `main.py` | `logging`, `pathlib.Path`, `typing`; các interface từ `audio`, `button`, `camera`, `config`, `gemini_client`, `messages`. |
| `config.py` | `os`, `dataclasses`, `pathlib.Path`, `typing`. |
| `button.py` | `time`, `logging`, `typing`; thư viện GPIO đã chọn, ví dụ `RPi.GPIO`. |
| `camera.py` | `subprocess`, ` tempfile` hoặc `pathlib`, `logging`, `uuid`, `typing`. |
| `gemini_client.py` | `base64`, `json`, `logging`, `time`, `pathlib.Path`, `typing`; HTTP client chuẩn như `urllib.request` hoặc thư viện HTTP được chấp thuận. |
| `messages.py` | `typing`, `pathlib.Path`. |
| `audio.py` | `subprocess`, `logging`, `pathlib.Path`, `typing`. |

Coder phải chọn một HTTP client duy nhất, đặt timeout rõ ràng và không trộn nhiều thư viện cho cùng một việc.

## 4. Hằng số và biến cấu hình

`config.py` cần quản lý tối thiểu các giá trị sau:

- `BUTTON_GPIO_BCM = 25`.
- `BUTTON_PHYSICAL_PIN = 22` và `GROUND_PHYSICAL_PIN = 20` chỉ để tài liệu hóa/kiểm tra cấu hình.
- `GEMINI_MODEL = "gemini-2.5-flash-lite"`.
- `GEMINI_API_KEY`: đọc từ `GEMINI_API_KEY`, giá trị mặc định để trống.
- Endpoint Gemini v1beta `generateContent` được dựng từ model và key, không hard-code key.
- `CAPTURE_PATH = /dev/shm/green-eye-capture.jpg` hoặc đường dẫn tạm tương đương có thể cấu hình.
- `CAPTURE_COMMAND = rpicam-jpeg`.
- MIME ảnh `image/jpeg`.
- `TEMPERATURE = 0`, `CANDIDATE_COUNT = 1`, `MAX_OUTPUT_TOKENS = 40`.
- HTTP timeout; số lần retry tối đa là 1 cho lỗi tạm thời.
- Debounce mặc định trong khoảng 50–150 ms.
- Thư mục MP3 mặc định là `../X/mp3/` tính tương đối từ `source/`, nhưng nên cho phép cấu hình bằng biến môi trường.
- Trình phát audio và timeout phát, nếu cần.
- Mức logging; không bao giờ log giá trị API key.

Hàm đọc cấu hình phải thất bại sớm khi thiếu API key, nhưng chỉ ghi hướng dẫn cấu hình, không in secret.

## 5. Giao diện module và các hàm cần có

### `config.py`

- `load_config() -> AppConfig`: đọc biến môi trường, áp dụng mặc định, xác thực đường dẫn/model/GPIO và trả về cấu hình ứng dụng.
- `validate_config(config: AppConfig) -> None`: ném lỗi cấu hình nếu API key rỗng hoặc giá trị không hợp lệ.
- `build_gemini_endpoint(config: AppConfig) -> str`: tạo endpoint từ model và API key; không ghi endpoint có key vào log.

`AppConfig` là cấu trúc dữ liệu cấu hình, không chứa logic nghiệp vụ.

### `button.py`

- `setup_button(gpio_number: int, debounce_seconds: float) -> ButtonController`: cấu hình BCM, input pull-up và trả về controller.
- `wait_for_press(controller: ButtonController) -> None`: chặn đến khi GPIO chuyển LOW và debounce xác nhận đó là nhấn thật.
- `wait_for_release(controller: ButtonController) -> None`: chặn đến khi GPIO trở HIGH để một lần nhấn chỉ tạo một lượt.
- `close_button(controller: ButtonController) -> None`: gỡ callback/giải phóng GPIO an toàn, có thể gọi nhiều lần.

### `camera.py`

- `capture_jpeg(config: AppConfig) -> Path`: gọi `rpicam-jpeg`, ghi JPEG vào đường dẫn tạm và chỉ trả về sau khi file tồn tại, không rỗng.
- `delete_file_if_exists(path: Path | None) -> None`: xóa đúng file tạm đã tạo; không xóa đường dẫn ngoài phạm vi được cấp.

Lỗi tiến trình, timeout, file rỗng hoặc camera không có phải được chuyển thành lỗi camera có ngữ cảnh.

### `gemini_client.py`

- `classify(image_path: Path, config: AppConfig) -> str`: đọc ảnh, mã hóa base64, gửi prompt đầy đủ cùng `inline_data` MIME `image/jpeg`, retry tối đa một lần cho lỗi tạm thời và trả text thô.
- `build_prompt() -> str`: tạo prompt đầy đủ với luật phân loại và toàn bộ 36 câu; danh sách trong prompt phải lấy từ nguồn hợp lệ thống nhất.
- `build_payload(prompt: str, image_base64: str, config: AppConfig) -> dict`: tạo payload theo `contents.parts` và `generationConfig` đã quy định.
- `extract_response_text(response: dict) -> str`: lấy text từ response Gemini; lỗi thiếu trường hoặc response bị chặn phải được báo rõ.

### `messages.py`

- `VALID_MESSAGES: tuple[str, ...]`: đúng 36 câu, giữ nguyên dấu câu và Unicode.
- `MESSAGE_TO_MP3: Mapping[str, str]`: ánh xạ một-một từ từng câu sang tên file MP3.
- `FALLBACK_MESSAGE = "Đây là rác khác."`.
- `normalize_and_validate(raw_text: str) -> str`: chỉ `strip()` khoảng trắng đầu/cuối rồi kiểm tra exact match; text không hợp lệ trả fallback.
- `mp3_filename_for(message: str) -> str`: tra cứu exact match; câu không hợp lệ không được tự suy đoán và phải dùng fallback.
- `validate_message_catalog(mp3_dir: Path) -> None`: xác nhận có đủ 36 khóa, 36 file ánh xạ và file fallback tồn tại.

### `audio.py`

- `resolve_mp3_path(mp3_dir: Path, filename: str) -> Path`: tạo đường dẫn và kiểm tra file tồn tại, là file thường, đúng thư mục MP3.
- `play_mp3(path: Path, config: AppConfig) -> None`: phát đồng bộ file MP3; lỗi trình phát phải được ghi log và chuyển thành lỗi audio.
- `play_fallback(config: AppConfig) -> None`: phát MP3 của `FALLBACK_MESSAGE` nếu có thể.

### `main.py`

- `process_one_press(config: AppConfig, services: Services) -> None`: điều phối một lượt từ chụp ảnh đến phát âm thanh; luôn dọn ảnh.
- `run() -> None`: khởi tạo logging, config, catalog, GPIO và service; chạy vòng lặp chờ nhấn; xử lý shutdown.
- `handle_error(error: Exception, services: Services) -> None`: log lỗi không chứa secret và thử phát fallback cục bộ.

## 6. Cấu trúc ánh xạ 36 câu sang MP3

`MESSAGE_TO_MP3` phải là mapping tĩnh, viết rõ từng mục, không suy ra tên file bằng bỏ dấu. Thứ tự và tên file chuẩn:

| # | Câu hợp lệ | MP3 |
|---:|---|---|
| 1–10 | 10 câu tiền: năm trăm, một ngàn, hai ngàn, năm ngàn, mười ngàn, hai mươi ngàn, năm mươi ngàn, một trăm ngàn, hai trăm ngàn, năm trăm ngàn đồng | `01-ay-la-to-nam-tram-ong.mp3` đến `10-ay-la-to-nam-tram-ngan-ong.mp3` theo catalog thực tế |
| 11 | Đây là cây bút. | `11-ay-la-cay-but.mp3` |
| 12 | Đây là cái chăn. | `12-ay-la-cai-chan.mp3` |
| 13 | Đây là chậu rửa. | `13-ay-la-chau-rua.mp3` |
| 14 | Đây là giẻ lau. | `14-ay-la-gie-lau.mp3` |
| 15 | Đây là đồng hồ. | `15-ay-la-dong-ho.mp3` |
| 16 | Đây là cái cốc. | `16-ay-la-cai-coc.mp3` |
| 17 | Đây là cái bát. | `17-ay-la-cai-bat.mp3` |
| 18 | Đây là cái ấm. | `18-ay-la-cai-am.mp3` |
| 19 | Đây là chìa khóa. | `19-ay-la-chia-khoa.mp3` |
| 20 | Đây là dao nhà bếp. | `20-ay-la-dao-nha-bep.mp3` |
| 21–35 | 15 câu vật thể/rác còn lại theo đúng thứ tự trong `design.md` | `21-...mp3` đến `35-...mp3`, đối chiếu từng tên file trong thư mục `../X/mp3/` |
| 36 | Đây là rác khác. | `36-ay-la-rac-khac.mp3` |

Do tên 10 MP3 tiền trong nguồn có thể chứa quy ước đánh vần riêng, Coder phải đối chiếu tên file thật và ghi đủ từng cặp cụ thể trong `messages.py`; không được dùng dải tên sinh tự động. Catalog phải bảo đảm đủ 36 câu, trong đó câu thứ 36 là fallback.

## 7. Luồng gọi hàm

1. `run()` gọi `load_config()`, `validate_message_catalog()`, khởi tạo client, camera, audio và `setup_button()`.
2. Vòng lặp gọi `wait_for_press()`.
3. `process_one_press()` đặt `image_path = None`, gọi `capture_jpeg()`.
4. Gọi `gemini_client.classify()`; nhận text thô.
5. Gọi `normalize_and_validate()`; nếu sai định dạng, chuyển sang fallback.
6. Gọi `mp3_filename_for()`, `resolve_mp3_path()` và `play_mp3()`.
7. Trong mọi trường hợp, `finally` gọi `delete_file_if_exists(image_path)`.
8. Vòng lặp gọi `wait_for_release()` rồi quay lại chờ nhấn.
9. Khi shutdown, gọi `close_button()` và giải phóng tài nguyên.

## 8. Xử lý lỗi

- GPIO không khởi tạo được: log lỗi, không khởi động vòng nhận diện.
- Camera lỗi, timeout hoặc JPEG rỗng: không gọi Gemini; dọn file và phát fallback nếu audio còn hoạt động.
- Thiếu API key: báo lỗi cấu hình lúc khởi động, không gửi request.
- HTTP timeout, lỗi mạng hoặc lỗi 5xx: retry tối đa một lần; sau đó fallback.
- Lỗi xác thực/4xx: không retry mù; fallback và log mã lỗi, không log key.
- Response Gemini thiếu text, bị chặn hoặc text ngoài catalog: fallback exact `Đây là rác khác.`.
- MP3 thiếu/hỏng: log đường dẫn; thử fallback; nếu fallback cũng lỗi thì chỉ ghi log, không làm treo vòng lặp.
- Lỗi bất kỳ trong một lượt không được làm mất khả năng chờ lượt nhấn tiếp theo, trừ lỗi khởi tạo phần cứng nghiêm trọng.
- `finally` luôn được thực hiện để xóa ảnh; cleanup phải an toàn cả khi đường dẫn là `None`.

## 9. Tiêu chí bàn giao cho Coder

- Có đủ các file Python nêu ở mục 2 và không có logic trùng lặp giữa các module.
- Không sửa `design.md`, không hard-code API key, giữ đúng model `gemini-2.5-flash-lite`.
- GPIO25 BCM, physical pin 22 và GND physical pin 20 được ghi rõ trong cấu hình và README triển khai.
- Prompt, payload, timeout, retry và `inline_data` JPEG đúng đặc tả.
- Catalog có đúng 36 câu; mọi câu có đúng một MP3; fallback là mục 36.
- Kiểm tra exact match trước khi phát; không TTS, không fuzzy matching, không phát text chưa xác thực.
- Có kiểm tra tồn tại 36 MP3, đặc biệt 10 mệnh giá tiền và fallback.
- Có cleanup ảnh khi thành công, lỗi camera, lỗi mạng, lỗi Gemini và lỗi audio.
- Nhấn giữ chỉ xử lý một lượt; phải chờ nhả công tắc trước lượt kế tiếp.
- Có test cho GPIO LOW/HIGH, camera, response hợp lệ/không hợp lệ, fallback, mapping 36 mục, retry và cleanup.
- Log đủ để chẩn đoán nhưng không làm lộ API key hay dữ liệu nhạy cảm.
- Coder chỉ bàn giao mã sau khi chạy kiểm thử độc lập bằng ảnh tiền, bút, lon kim loại, lá cây, vật sắc nhọn và vật không xác định.
