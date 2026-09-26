# Thiết kế chương trình Python nhận diện rác bằng Gemini

## 1. Mục tiêu

Khi người dùng nhấn công tắc, Raspberry Pi sẽ:

1. Nhận sự kiện nhấn công tắc.
2. Bật camera và chụp một ảnh.
3. Gửi ảnh đến Gemini API bằng model `gemini-2.5-flash-lite`.
4. Yêu cầu Gemini trả về đúng một câu thông báo đã được định nghĩa trước.
5. Dựa vào câu Gemini trả về, chọn file MP3 tương ứng trong thư mục `../X/mp3/`.
6. Phát file MP3 cho người dùng.
7. Xóa ảnh tạm sau khi xử lý.
8. Quay lại trạng thái chờ nhấn công tắc.

API key Gemini để trống trong bản thiết kế; khi triển khai sẽ điền vào biến môi trường, không ghi trực tiếp vào mã nguồn.

## 2. Phần cứng

### Công tắc

Công tắc nối giữa:

- Chân vật lý 22 — `GPIO25` theo chế độ BCM.
- Chân vật lý 20 — `GND`.

Sơ đồ:

```text
Công tắc
  ├── Physical pin 22 / GPIO25
  └── Physical pin 20 / GND
```

GPIO dùng pull-up nội bộ. Trạng thái bình thường là HIGH; khi nhấn công tắc, GPIO25 chuyển xuống LOW.

### Camera

Dùng camera Raspberry Pi và lệnh:

```text
rpicam-jpeg
```

Ảnh nên được chụp vào thư mục tạm, ví dụ:

```text
/dev/shm/green-eye-capture.jpg
```

Sau khi Gemini xử lý xong, ảnh phải được xóa bằng `finally`, kể cả khi xảy ra lỗi.

## 3. Cấu trúc thư mục dự kiến

```text
source/
├── design.md
├── main.py
├── config.py
├── gemini_client.py
├── camera.py
├── button.py
├── audio.py
├── messages.py
└── requirements.txt

../X/
├── thong-bao.md
├── vat-the.md
└── mp3/
    ├── 01-ay-la-to-nam-tram-ong.mp3
    ├── ...
    └── 36-ay-la-rac-khac.mp3
```

Nên tạo một file ánh xạ cố định giữa câu thông báo và file MP3. Không nên suy ra tên file bằng cách tự bỏ dấu vì có thể tạo tên sai, ví dụ chữ `Đ` có thể bị biến thành `D` hoặc bị mất.

Ví dụ `messages.py`:

```python
MESSAGE_TO_MP3 = {
    "Đây là tờ năm trăm đồng.": "01-ay-la-to-nam-tram-ong.mp3",
    "Đây là tờ một ngàn đồng.": "02-ay-la-to-mot-ngan-ong.mp3",
    # ... đủ 36 câu ...
    "Đây là rác khác.": "36-ay-la-rac-khac.mp3",
}
```

Sau khi Gemini trả về câu, chương trình chỉ được phát MP3 nếu câu đó có trong `MESSAGE_TO_MP3`.

## 4. Danh sách câu trả lời hợp lệ

Gemini chỉ được phép trả về đúng một trong 36 câu sau:

```text
Đây là tờ năm trăm đồng.
Đây là tờ một ngàn đồng.
Đây là tờ hai ngàn đồng.
Đây là tờ năm ngàn đồng.
Đây là tờ mười ngàn đồng.
Đây là tờ hai mươi ngàn đồng.
Đây là tờ năm mươi ngàn đồng.
Đây là tờ một trăm ngàn đồng.
Đây là tờ hai trăm ngàn đồng.
Đây là tờ năm trăm ngàn đồng.
Đây là cây bút.
Đây là cái chăn.
Đây là chậu rửa.
Đây là giẻ lau.
Đây là đồng hồ.
Đây là cái cốc.
Đây là cái bát.
Đây là cái ấm.
Đây là chìa khóa.
Đây là dao nhà bếp.
Đây là lá cây.
Đây là bóng đèn.
Đây là cái áo.
Đây là lon kim loại.
Đây là quả cam hoặc quả quất.
Đây là giấy.
Đây là túi nhựa.
Cảnh báo, đây là vật sắc nhọn nguy hiểm.
Đây là cái thìa.
Đây là cái thước.
Đây là bàn chải đánh răng.
Đây là chai nước.
Đây là đôi đũa.
Đây là rác vô cơ.
Đây là rác hữu cơ.
Đây là rác khác.
```

## 5. Prompt gửi cho Gemini

Model được dùng:

```text
gemini-2.5-flash-lite
```

Prompt cần lặp lại đầy đủ luật vì model nhẹ dễ trả lời dài, tự giải thích hoặc dùng nhãn không đúng. Ảnh được gửi cùng prompt ở dạng `inline_data` với MIME type `image/jpeg`.

Prompt đề xuất:

```text
Bạn là bộ phân loại hình ảnh cho thiết bị hỗ trợ người khiếm thị.

Nhiệm vụ duy nhất của bạn là nhìn vào ảnh và chọn một câu trả lời trong DANH SÁCH CÂU TRẢ LỜI HỢP LỆ ở cuối prompt.

QUY TẮC BẮT BUỘC:
1. Chỉ được trả về đúng một câu duy nhất.
2. Không được trả về JSON.
3. Không được dùng Markdown.
4. Không được thêm lời giải thích, độ tin cậy, dấu ngoặc kép, dấu gạch đầu dòng hoặc câu mở đầu.
5. Không được tự tạo câu mới.
6. Kết quả phải khớp chính xác từng ký tự với một câu trong danh sách hợp lệ.
7. Nếu ảnh không đủ rõ, có nhiều vật thể ngang nhau, hoặc không chắc chắn, trả về: Đây là rác khác.
8. Ưu tiên vật thể nằm gần trung tâm ảnh và chiếm diện tích lớn nhất.
9. Chỉ chọn một vật thể chính.
10. Không suy đoán dựa trên tên file, lịch sử hội thoại hoặc kiến thức ngoài ảnh.

LUẬT NHẬN DIỆN TIỀN:
- Nếu nhìn thấy tiền giấy Việt Nam và nhận ra mệnh giá, phải trả đúng câu theo mệnh giá.
- Các mệnh giá được phép là: 500 đồng, 1.000 đồng, 2.000 đồng, 5.000 đồng, 10.000 đồng, 20.000 đồng, 50.000 đồng, 100.000 đồng, 200.000 đồng và 500.000 đồng.
- Nếu là tiền Việt Nam nhưng không đọc chắc được mệnh giá, trả về: Đây là rác khác.
- Không được trả về câu chung chung như “Đây là tiền Việt Nam”.
- Không được nhầm số tiền in trên tờ tiền với mệnh giá khác.

LUẬT NHẬN DIỆN 24 NHÓM VẬT THỂ:
- Bút: nhận diện bút viết.
- Chăn: nhận diện chăn hoặc mền.
- Chậu rửa: nhận diện chậu dùng để rửa hoặc chứa nước.
- Giẻ lau: nhận diện khăn hoặc mảnh vải dùng để lau.
- Đồng hồ: nhận diện đồng hồ đeo tay hoặc đồng hồ để bàn.
- Cốc: nhận diện cốc hoặc ly.
- Bát: nhận diện bát ăn cơm.
- Ấm: nhận diện ấm đựng hoặc đun nước.
- Chìa khóa: nhận diện chìa khóa.
- Dao nhà bếp: nhận diện dao dùng trong nhà bếp.
- Lá cây: nhận diện lá cây tự nhiên.
- Bóng đèn: nhận diện bóng đèn điện.
- Áo: nhận diện áo mặc.
- Lon kim loại: nhận diện lon bằng kim loại.
- Quả cam hoặc quả quất: nhận diện quả cam hoặc quả quất.
- Giấy: nhận diện tờ giấy hoặc giấy rời.
- Túi nhựa: nhận diện túi làm bằng nhựa.
- Vật sắc nhọn nguy hiểm: nhận diện vật có thể gây đứt hoặc đâm, ví dụ mảnh kính, dao hoặc vật sắc nhọn. Nếu đúng nhóm này phải cảnh báo.
- Thìa: nhận diện thìa ăn.
- Thước: nhận diện thước đo.
- Bàn chải đánh răng: nhận diện bàn chải dùng để đánh răng.
- Chai nước: nhận diện chai đựng nước.
- Đũa: nhận diện một chiếc đũa hoặc đôi đũa.

QUY TẮC ƯU TIÊN:
1. Tiền giấy Việt Nam có thể đọc rõ mệnh giá.
2. Vật sắc nhọn nguy hiểm.
3. Một trong các vật thể cụ thể còn lại.
4. Nếu không thuộc các nhóm trên, phân loại theo ba nhóm rác: hữu cơ, vô cơ hoặc khác.

PHÂN LOẠI BA NHÓM RÁC:
- Rác hữu cơ: thức ăn, rau, củ, quả hoặc vật có nguồn gốc hữu cơ đang phân hủy.
- Rác vô cơ: vật liệu vô cơ hoặc vật có thể đưa vào nhóm vô cơ/tái chế theo quy ước của thiết bị, chẳng hạn kim loại, giấy, nhựa, thủy tinh, nếu không được nhận diện chắc chắn là một vật thể cụ thể ở trên.
- Rác khác: vật không xác định được, ảnh mờ, vật không nằm trong danh sách, hoặc trường hợp không đủ chắc chắn.

DANH SÁCH CÂU TRẢ LỜI HỢP LỆ — PHẢI SAO CHÉP ĐÚNG:
Đây là tờ năm trăm đồng.
Đây là tờ một ngàn đồng.
Đây là tờ hai ngàn đồng.
Đây là tờ năm ngàn đồng.
Đây là tờ mười ngàn đồng.
Đây là tờ hai mươi ngàn đồng.
Đây là tờ năm mươi ngàn đồng.
Đây là tờ một trăm ngàn đồng.
Đây là tờ hai trăm ngàn đồng.
Đây là tờ năm trăm ngàn đồng.
Đây là cây bút.
Đây là cái chăn.
Đây là chậu rửa.
Đây là giẻ lau.
Đây là đồng hồ.
Đây là cái cốc.
Đây là cái bát.
Đây là cái ấm.
Đây là chìa khóa.
Đây là dao nhà bếp.
Đây là lá cây.
Đây là bóng đèn.
Đây là cái áo.
Đây là lon kim loại.
Đây là quả cam hoặc quả quất.
Đây là giấy.
Đây là túi nhựa.
Cảnh báo, đây là vật sắc nhọn nguy hiểm.
Đây là cái thìa.
Đây là cái thước.
Đây là bàn chải đánh răng.
Đây là chai nước.
Đây là đôi đũa.
Đây là rác vô cơ.
Đây là rác hữu cơ.
Đây là rác khác.

Bây giờ hãy xem ảnh và trả về đúng một câu trong danh sách trên.
```

## 6. Gọi Gemini API

API key để trong biến môi trường:

```text
GEMINI_API_KEY=
```

Endpoint dự kiến:

```text
https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={GEMINI_API_KEY}
```

Payload dự kiến:

```json
{
  "contents": [
    {
      "parts": [
        {"text": "<PROMPT_DAY_DU_O_TREN>"},
        {
          "inline_data": {
            "mime_type": "image/jpeg",
            "data": "<ANH_BASE64>"
          }
        }
      ]
    }
  ],
  "generationConfig": {
    "temperature": 0,
    "candidateCount": 1,
    "maxOutputTokens": 40
  }
}
```

`temperature` phải bằng `0` để giảm việc model sáng tạo câu ngoài danh sách. `maxOutputTokens` thấp để tránh câu trả lời dài.

## 7. Kiểm tra câu trả lời của Gemini

Không được tin rằng Gemini luôn làm đúng prompt. Sau khi nhận response:

1. Lấy trường text trong response.
2. `strip()` khoảng trắng đầu và cuối.
3. Nếu text nằm chính xác trong `MESSAGE_TO_MP3`, phát file MP3 tương ứng.
4. Nếu text không hợp lệ, không được cố đoán bằng cách tìm gần đúng tùy ý.
5. Với text không hợp lệ, dùng câu an toàn:

```text
Đây là rác khác.
```

Sau đó phát `36-ay-la-rac-khac.mp3`.

Có thể ghi log câu gốc Gemini trả về để sửa prompt sau này, nhưng không phát trực tiếp câu gốc khi chưa kiểm tra.

## 8. Luồng chương trình dự kiến

```python
while True:
    wait_for_button_press(GPIO25)
    image_path = None

    try:
        image_path = capture_jpeg()
        raw_result = gemini_client.classify(image_path)
        message = normalize_and_validate(raw_result)
        mp3_path = MESSAGE_TO_MP3[message]
        play_mp3(mp3_path)
    except Exception as error:
        log_error(error)
        play_mp3(MESSAGE_TO_MP3["Đây là rác khác."])
    finally:
        delete_file_if_exists(image_path)
        wait_for_button_release(GPIO25)
```

Nên chờ người dùng thả công tắc trước khi quay lại vòng lặp để một lần nhấn chỉ tạo một lượt nhận diện.

## 9. Xử lý lỗi

### Lỗi công tắc

- Ghi log lỗi GPIO.
- Không chạy camera nếu GPIO không khởi tạo được.
- Dùng pull-up nội bộ và debounce khoảng 50–150 ms.

### Lỗi camera

- Không gửi ảnh rỗng.
- Phát thông báo lỗi cục bộ nếu có MP3 riêng.
- Xóa file tạm nếu file đã được tạo.

### Lỗi mạng hoặc Gemini API

- Đặt timeout cho HTTP request.
- Thử lại tối đa một lần nếu lỗi tạm thời.
- Nếu vẫn lỗi, phát câu mặc định `Đây là rác khác.` hoặc tạo MP3 lỗi riêng sau này.

### Gemini trả về sai định dạng

- Không đọc câu trả lời bằng TTS trực tiếp.
- Không chọn MP3 bằng tìm kiếm gần đúng.
- Dùng `Đây là rác khác.` làm fallback.

### API key bị thiếu

- Kiểm tra lúc khởi động.
- In hướng dẫn cấu hình ra log.
- Không gửi request nếu API key là chuỗi rỗng.

## 10. Kiểm thử trước khi chạy thật

1. Kiểm tra GPIO25 bằng mô phỏng `RPi.GPIO`, xác nhận nhấn là LOW và thả là HIGH.
2. Chạy camera độc lập, xác nhận file JPEG được tạo.
3. Gọi Gemini với một ảnh thử và in nguyên văn kết quả.
4. Kiểm tra bộ lọc chỉ chấp nhận 36 câu hợp lệ.
5. Kiểm tra câu ngoài danh sách được đổi thành `Đây là rác khác.`.
6. Kiểm tra đủ 36 câu đều có MP3 trong `../X/mp3/`.
7. Kiểm tra mỗi câu được ánh xạ đến đúng MP3, đặc biệt các mệnh giá tiền.
8. Kiểm tra ảnh tạm bị xóa sau cả trường hợp thành công và lỗi.
9. Kiểm tra nhấn giữ công tắc chỉ tạo một lượt nhận diện.
10. Chạy thử tối thiểu các ảnh: tiền, bút, lon kim loại, lá cây, vật sắc nhọn và vật không xác định.

## 11. Lưu ý quan trọng về prompt và phân loại

- `gemini-2.5-flash-lite` có thể nhầm vật thể hoặc trả lời ngoài định dạng. Bộ kiểm tra 36 câu bắt buộc phải nằm trong Python, không chỉ dựa vào prompt.
- Câu “rác vô cơ” và “rác hữu cơ” chỉ nên dùng khi vật không được xác định chắc chắn là một trong các vật thể cụ thể.
- Với ảnh mờ hoặc không đủ thông tin, ưu tiên `Đây là rác khác.` thay vì đoán nguy hiểm.
- Không để Gemini tự viết câu thông báo mới vì sẽ không có MP3 tương ứng.
- Không gửi API key vào log hoặc commit vào mã nguồn.
