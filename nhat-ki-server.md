# NHẬT KÍ NGHIÊN CỨU DỰ ÁN — PHẦN SERVER

> **Tên đề tài:** AI - Green - Eye  
> **Phần phụ trách:** Máy chủ xử lí trung tâm  
> **Nhóm thực hiện:** Học sinh THCS  
> **Giáo viên hướng dẫn:** ................................................  
> **Ngày bắt đầu:** 05/05/2026  
> **Ngày cập nhật gần nhất:** 26/09/2026  

## Lưu ý về cách ghi nhật kí

Nhật kí này được tái dựng từ quá trình phát triển thực tế, tài liệu và mã nguồn hiện còn lưu. Một số mốc trước tháng 9/2026 không còn ngày, giờ làm việc chính xác. Các mốc này là **tái dựng hồi cứu** từ sản phẩm cuối, tài liệu còn lưu và hướng phát triển của nhóm; vì vậy chúng mô tả quá trình hình thành phương án, không được xem là bằng chứng rằng một chức năng đã hoàn thành đúng ngày ghi. Từ tháng 9/2026, nhật kí ưu tiên các sự việc có thể đối chiếu với mã nguồn và quá trình thử nghiệm còn lưu. Nội dung được viết theo cách học sinh THCS có thể hiểu và trình bày.

AI được dùng để hỗ trợ tìm hiểu ý tưởng, gợi ý cách lập trình, giải thích lỗi và phản biện phương án. Nhóm học sinh vẫn phải tự lựa chọn phương án, chạy thử, quan sát kết quả và quyết định giữ hay bỏ giải pháp.

---

# NGÀY 05/05/2026

**GIAI ĐOẠN:** Hình thành kiến trúc tổng thể  
**THỜI GIAN:** Không ghi lại chính xác – tái dựng hồi cứu

## 1. MỤC TIÊU
Xác định cách để một thiết bị đeo nhỏ có thể nhận biết đồ vật, nghe câu hỏi và trả lời bằng âm thanh mà không phải tự xử lí toàn bộ AI trên thiết bị.

## 2. DỤNG CỤ & VẬT LIỆU SỬ DỤNG
- Máy tính xách tay dùng làm máy chủ thử nghiệm.
- Raspberry Pi dự kiến gắn trên thiết bị.
- Kết nối mạng Wi‑Fi.
- ChatGPT dùng để trao đổi kiến trúc.

## 3. TIẾN TRÌNH THỰC HIỆN & HIỆN TƯỢNG
Nhóm nhận thấy Raspberry Pi Zero 2 W có kích thước nhỏ nhưng khả năng tính toán hạn chế. Nếu chạy nhận dạng hình ảnh, nhận dạng giọng nói và AI cùng lúc trên Pi thì hệ thống dễ chậm, nóng và hao pin.

Nhóm đề xuất tách hệ thống thành hai phần: Pi chỉ thu âm, chụp ảnh và đọc cảm biến; máy tính mạnh hơn ở nơi khác làm phần xử lí AI rồi gửi câu trả lời lại.

## 4. KẾT QUẢ & SỐ LIỆU THÔ
- Chưa có số liệu thực nghiệm.
- Chọn mô hình **Pi nhẹ – Server xử lí nặng**.
- Dữ liệu chính cần truyền: câu lệnh, ảnh, dữ liệu cảm biến và âm thanh phản hồi.

## 5. RÚT KINH NGHIỆM & LỖI SAI
Không nên cố làm mọi việc trên Raspberry Pi chỉ vì thiết bị có thể chạy Python. Phải phân công đúng phần việc theo khả năng phần cứng.

## 6. KẾ HOẠCH TIẾP THEO
Tìm cách để Pi gửi yêu cầu đến máy tính qua mạng và nhận câu trả lời trở lại.

**Ghi nhận sử dụng AI:** dùng AI để so sánh ưu nhược điểm giữa xử lí toàn bộ trên Pi và tách Server.

---

# NGÀY 12/05/2026

**GIAI ĐOẠN:** Thiết kế giao tiếp Pi – Server  
**THỜI GIAN:** Không ghi lại chính xác – tái dựng hồi cứu

## 1. MỤC TIÊU
Xây dựng cách trao đổi dữ liệu giữa Raspberry Pi và máy chủ.

## 2. DỤNG CỤ & VẬT LIỆU SỬ DỤNG
- Raspberry Pi.
- Máy tính Mac dùng làm Server thử nghiệm.
- Mạng Wi‑Fi.
- Công cụ kiểm thử HTTP.

## 3. TIẾN TRÌNH THỰC HIỆN & HIỆN TƯỢNG
Nhóm chọn cách giao tiếp qua HTTP vì dễ kiểm tra và có thể gửi cả văn bản lẫn ảnh. Ý tưởng là Pi gửi một yêu cầu đến Server; Server xử lí rồi trả về dữ liệu phản hồi.

Nhóm thử hình dung các đường dẫn riêng như kiểm tra Server có hoạt động hay không, gửi lệnh, gửi ảnh và chuyển văn bản thành tiếng nói.

## 4. KẾT QUẢ & SỐ LIỆU THÔ
- Xác định cần API kiểm tra trạng thái và API xử lí lệnh.
- Chưa chốt ngôn ngữ lập trình Server.

## 5. RÚT KINH NGHIỆM & LỖI SAI
Nếu không chuẩn hóa dữ liệu gửi qua mạng từ đầu thì về sau Pi và Server dễ hiểu sai nhau.

## 6. KẾ HOẠCH TIẾP THEO
Chọn công nghệ viết Server và thử dựng dịch vụ đơn giản.

---

# NGÀY 20/05/2026

**GIAI ĐOẠN:** Lựa chọn công nghệ Server  
**THỜI GIAN:** Không ghi lại chính xác – tái dựng hồi cứu

## 1. MỤC TIÊU
Chọn ngôn ngữ và bộ khung phù hợp để viết máy chủ.

## 2. DỤNG CỤ & VẬT LIỆU SỬ DỤNG
- MacBook.
- Swift.
- Swift Package Manager.
- Hummingbird.

## 3. TIẾN TRÌNH THỰC HIỆN & HIỆN TƯỢNG
Nhóm chọn Swift để tận dụng máy Mac và các thư viện có sẵn. Hummingbird được dùng làm bộ khung web nhẹ để tạo các đường dẫn nhận yêu cầu từ Pi.

Nhóm tạo cấu trúc chương trình gồm phần cấu hình, phần Server, phần lệnh, phần AI, phần hình ảnh và phần chuyển văn bản thành âm thanh.

## 4. KẾT QUẢ & SỐ LIỆU THÔ
- Chọn Swift Package Manager để quản lí dự án.
- Hình thành cách chia chương trình thành các phần nhỏ để sau này dễ kiểm tra và sửa lỗi.

## 5. RÚT KINH NGHIỆM & LỖI SAI
Tách các chức năng ra nhiều thư mục giúp học sinh dễ biết lỗi đang nằm ở phần nào hơn là viết tất cả vào một file dài.

## 6. KẾ HOẠCH TIẾP THEO
Tạo API kiểm tra trạng thái và API nhận câu lệnh đầu tiên.

---

# NGÀY 02/06/2026

**GIAI ĐOẠN:** Tạo Server chạy được  
**THỜI GIAN:** Không ghi lại chính xác – tái dựng hồi cứu

## 1. MỤC TIÊU
Làm cho Server có thể khởi động và trả lời một yêu cầu đơn giản.

## 2. DỤNG CỤ & VẬT LIỆU SỬ DỤNG
- Swift.
- Hummingbird.
- Terminal.

## 3. TIẾN TRÌNH THỰC HIỆN & HIỆN TƯỢNG
Nhóm tạo đường dẫn kiểm tra trạng thái để biết Server còn hoạt động. Sau khi chạy `swift run`, máy chủ có thể nhận yêu cầu từ thiết bị khác trong mạng.

Việc có một đường dẫn kiểm tra riêng rất hữu ích vì khi Pi không nhận được câu trả lời, nhóm có thể kiểm tra xem lỗi nằm ở mạng hay ở AI.

## 4. KẾT QUẢ & SỐ LIỆU THÔ
- Hình thành yêu cầu phải có một API kiểm tra trạng thái riêng (`/health`).
- Kết quả Server chạy thực tế được xác nhận ở giai đoạn thử nghiệm tháng 9; mốc này chỉ ghi lại bước xây dựng phương án.

## 5. RÚT KINH NGHIỆM & LỖI SAI
Phải kiểm tra từng tầng riêng: Server chạy chưa, mạng có thông chưa, rồi mới kiểm tra AI.

## 6. KẾ HOẠCH TIẾP THEO
Kết nối dịch vụ AI để trả lời câu hỏi bằng văn bản.

---

# NGÀY 16/06/2026

**GIAI ĐOẠN:** Kết nối AI  
**THỜI GIAN:** Không ghi lại chính xác – tái dựng hồi cứu

## 1. MỤC TIÊU
Cho Server gửi câu hỏi tới mô hình AI và nhận câu trả lời.

## 2. DỤNG CỤ & VẬT LIỆU SỬ DỤNG
- Server Swift.
- API AI.
- File cấu hình `.env`.

## 3. TIẾN TRÌNH THỰC HIỆN & HIỆN TƯỢNG
Nhóm thêm phần cấu hình khóa API và model. Server nhận câu hỏi, gửi tới mô hình AI rồi lấy nội dung trả lời.

Nhóm nhận thấy khóa API không được ghi trực tiếp vào mã nguồn vì khi đưa dự án lên GitHub sẽ dễ bị lộ. Vì vậy thông tin bí mật được chuyển sang file môi trường.

## 4. KẾT QUẢ & SỐ LIỆU THÔ
- Chọn cách gọi AI qua API và tách khóa bí mật sang biến môi trường.
- Việc gọi model thực tế tiếp tục được kiểm tra ở các giai đoạn sau.

## 5. RÚT KINH NGHIỆM & LỖI SAI
Bảo mật khóa API là yêu cầu quan trọng ngay cả với dự án học sinh.

## 6. KẾ HOẠCH TIẾP THEO
Cho Server nhận ảnh từ Pi để mô tả vật trước mặt.

---

# NGÀY 05/07/2026

**GIAI ĐOẠN:** Xử lí hình ảnh  
**THỜI GIAN:** Không ghi lại chính xác – tái dựng hồi cứu

## 1. MỤC TIÊU
Cho Server có thể nhận ảnh từ camera và dùng AI để mô tả nội dung.

## 2. DỤNG CỤ & VẬT LIỆU SỬ DỤNG
- Ảnh JPEG thử nghiệm.
- Server Swift.
- Dịch vụ AI có khả năng đọc ảnh.

## 3. TIẾN TRÌNH THỰC HIỆN & HIỆN TƯỢNG
Nhóm thử gửi ảnh lên Server cùng câu hỏi như “phía trước có gì?”. Server chuyển ảnh và câu hỏi tới mô hình AI, sau đó nhận lại mô tả bằng văn bản.

Nhóm cũng khảo sát khả năng đọc chữ trong ảnh để hỗ trợ người dùng đọc nhãn, biển báo hoặc văn bản ngắn.

## 4. KẾT QUẢ & SỐ LIỆU THÔ
- Xác định Server cần nhận được ảnh JPEG và có phần xử lí thị giác/OCR.
- Xác định đầu ra văn bản của bước này sẽ được dùng tiếp để tạo lời nói.

## 5. RÚT KINH NGHIỆM & LỖI SAI
Ảnh quá lớn làm thời gian truyền và xử lí tăng. Pi chỉ nên chụp khi câu lệnh thật sự cần quan sát.

## 6. KẾ HOẠCH TIẾP THEO
Thêm chức năng chuyển câu trả lời thành âm thanh.

---

# NGÀY 20/07/2026

**GIAI ĐOẠN:** Chuyển văn bản thành âm thanh  
**THỜI GIAN:** Không ghi lại chính xác – tái dựng hồi cứu

## 1. MỤC TIÊU
Để người dùng không cần nhìn màn hình mà vẫn nhận được câu trả lời.

## 2. DỤNG CỤ & VẬT LIỆU SỬ DỤNG
- Server.
- Công cụ chuyển văn bản thành giọng nói.
- Bộ mã hóa MP3.

## 3. TIẾN TRÌNH THỰC HIỆN & HIỆN TƯỢNG
Sau khi AI sinh câu trả lời, Server chuyển văn bản thành giọng nói rồi mã hóa thành MP3. File âm thanh này được gửi về Pi để phát qua loa.

Nhóm chọn MP3 vì dung lượng nhỏ hơn WAV, phù hợp truyền qua mạng.

## 4. KẾT QUẢ & SỐ LIỆU THÔ
- Chọn hướng tạo âm thanh trả lời và mã hóa MP3; bộ mã hóa `lame` được đưa vào cấu hình Server hiện tại.
- Chưa ghi số liệu về thời gian tạo âm thanh ở mốc hồi cứu này.

## 5. RÚT KINH NGHIỆM & LỖI SAI
Không nên gửi file âm thanh quá lớn vì làm phản hồi chậm.

## 6. KẾ HOẠCH TIẾP THEO
Gộp các bước nhận lệnh, quan sát và trả âm thanh thành một luồng hoàn chỉnh.

---

# NGÀY 08/08/2026

**GIAI ĐOẠN:** Gộp luồng xử lí lệnh  
**THỜI GIAN:** Không ghi lại chính xác – tái dựng hồi cứu

## 1. MỤC TIÊU
Cho Server tự quyết định câu lệnh nào cần ảnh và câu lệnh nào chỉ cần trả lời bằng kiến thức.

## 2. DỤNG CỤ & VẬT LIỆU SỬ DỤNG
- Server Swift.
- Các module Command, Vision, AI và TTS.

## 3. TIẾN TRÌNH THỰC HIỆN & HIỆN TƯỢNG
Nhóm xây dựng luồng: nhận câu lệnh → xác định cần quan sát hay không → nếu cần thì dùng ảnh → hỏi AI → tạo âm thanh → trả MP3 về Pi.

Việc tách bước “lập kế hoạch” giúp tránh việc lúc nào cũng chụp ảnh.

## 4. KẾT QUẢ & SỐ LIỆU THÔ
- Thiết kế hai nhiệm vụ chính: lập kế hoạch xử lí và thực hiện câu lệnh; kiến trúc hiện tại thể hiện bằng `/plan` và `/command`.
- Chưa có số đo thời gian phản hồi ở mốc hồi cứu này.

## 5. RÚT KINH NGHIỆM & LỖI SAI
Cần giới hạn số bước để phản hồi không quá chậm.

## 6. KẾ HOẠCH TIẾP THEO
Tối ưu việc nhận giọng nói và quyết định phần nào nên chạy ở Pi, phần nào ở Server.

---

# NGÀY 02/09/2026

**GIAI ĐOẠN:** Tối ưu kiến trúc xử lí giọng nói  
**THỜI GIAN:** Không ghi lại chính xác – tái dựng hồi cứu

## 1. MỤC TIÊU
Giảm tải cho Server và làm phản hồi nhanh hơn.

## 2. DỤNG CỤ & VẬT LIỆU SỬ DỤNG
- Raspberry Pi Zero 2 W.
- Mic USB.
- Groq Whisper.
- Server Swift.

## 3. TIẾN TRÌNH THỰC HIỆN & HIỆN TƯỢNG
Ban đầu nhóm dự định để Server nhận file âm thanh và chạy nhận dạng giọng nói. Sau khi thử nghiệm, nhóm chuyển bước nhận dạng giọng nói sang Pi gọi trực tiếp dịch vụ Whisper. Pi chỉ gửi phần văn bản đã nhận dạng sang Server.

Cách này làm Server bớt một tầng xử lí và không phải nhận file âm thanh của người dùng.

## 4. KẾT QUẢ & SỐ LIỆU THÔ
- Luồng chính chuyển sang: **mic → Pi nhận dạng → văn bản → Server**.
- Server tập trung vào lập kế hoạch, hình ảnh, AI và tạo âm thanh trả lời.

## 5. RÚT KINH NGHIỆM & LỖI SAI
Kiến trúc tốt không phải kiến trúc cố định từ đầu. Khi thử thực tế, có thể chuyển một chức năng sang nơi phù hợp hơn.

## 6. KẾ HOẠCH TIẾP THEO
Kiểm tra toàn bộ Server với Pi thật.

---

# NGÀY 17/09/2026

**GIAI ĐOẠN:** Chuẩn hóa cấu trúc Server  
**THỜI GIAN:** Đối chiếu mã nguồn hiện tại

## 1. MỤC TIÊU
Sắp xếp mã nguồn để dễ bảo trì và dễ giải thích khi báo cáo.

## 2. DỤNG CỤ & VẬT LIỆU SỬ DỤNG
- Swift.
- Hummingbird.
- Cấu trúc `Sources/ThienNhanServer`.

## 3. TIẾN TRÌNH THỰC HIỆN & HIỆN TƯỢNG
Mã nguồn được chia thành các phần `Command`, `Gemini`, `Vision`, `TTS`, `STT`, cấu hình và Server chính. Việc chia nhỏ giúp nhóm kiểm tra riêng từng chức năng.

## 4. KẾT QUẢ & SỐ LIỆU THÔ
- Có cấu trúc Server rõ ràng.
- Các chức năng chính được tách thành module.

## 5. RÚT KINH NGHIỆM & LỖI SAI
Một chương trình chạy được chưa chắc đã dễ sửa. Cấu trúc mã nguồn cũng là một phần quan trọng của sản phẩm.

## 6. KẾ HOẠCH TIẾP THEO
Kiểm tra model AI và các lỗi cấu hình thật.

---

# NGÀY 23/09/2026

**GIAI ĐOẠN:** Sửa lỗi model AI  
**THỜI GIAN:** Theo quá trình thử nghiệm thực tế

## 1. MỤC TIÊU
Tìm nguyên nhân Server gọi AI bị lỗi dù mã nguồn vẫn biên dịch được.

## 2. DỤNG CỤ & VẬT LIỆU SỬ DỤNG
- Terminal.
- File `.env`.
- API AI.

## 3. TIẾN TRÌNH THỰC HIỆN & HIỆN TƯỢNG
Server trả lỗi HTTP 404 khi gọi model cấu hình lúc đó. Nhóm kiểm tra thông báo từ API và thử model khác; kết quả cho thấy lỗi liên quan đến model/cấu hình dịch vụ chứ không phải lỗi biên dịch của Server.

Nhóm thử model mới trước khi thay đổi cấu hình chính để tránh sửa nhiều thứ cùng lúc.

## 4. KẾT QUẢ & SỐ LIỆU THÔ
- Khoanh vùng được lỗi ở phần model/cấu hình API.
- Xác nhận cần thử API độc lập trước khi sửa mã nguồn Server.

## 5. RÚT KINH NGHIỆM & LỖI SAI
Khi gặp lỗi, không nên mặc định cho rằng mã nguồn sai. Cần kiểm tra cả API, cấu hình và dịch vụ bên ngoài.

## 6. KẾ HOẠCH TIẾP THEO
Giảm chi phí gọi AI và chuẩn hóa luồng Server – Pi.

**Ghi nhận sử dụng AI:** dùng AI hỗ trợ đọc thông báo lỗi và đề xuất cách khoanh vùng nguyên nhân; nhóm tự chạy thử để xác nhận.

---

# NGÀY 25/09/2026

**GIAI ĐOẠN:** Hoàn thiện luồng Server thực tế  
**THỜI GIAN:** Theo mã nguồn hiện tại

## 1. MỤC TIÊU
Đảm bảo Server chỉ làm phần xử lí nặng, còn Pi phụ trách thiết bị ngoại vi và nhận dạng giọng nói ban đầu.

## 2. DỤNG CỤ & VẬT LIỆU SỬ DỤNG
- Server Swift.
- Raspberry Pi Zero 2 W.
- Tailscale/Wi‑Fi.

## 3. TIẾN TRÌNH THỰC HIỆN & HIỆN TƯỢNG
Luồng được chuẩn hóa: Pi nghe mic và nhận dạng lời nói, gửi văn bản cùng dữ liệu cảm biến lên Server. Nếu câu lệnh cần quan sát, Pi gửi thêm ảnh. Server dùng AI để trả lời rồi tạo MP3 gửi về Pi.

## 4. KẾT QUẢ & SỐ LIỆU THÔ
Đối chiếu mã nguồn hiện tại cho thấy Server có các đường dẫn chính cho kiểm tra trạng thái, lập kế hoạch, AI, OCR, TTS và xử lí lệnh. Đây là cấu trúc phần mềm hiện có; nhật kí chưa coi đó là số liệu chứng minh độ chính xác của AI.

## 5. RÚT KINH NGHIỆM & LỖI SAI
Giữ Server tập trung vào chức năng cốt lõi làm hệ thống dễ hiểu và dễ kiểm tra hơn.

## 6. KẾ HOẠCH TIẾP THEO
Kiểm tra độ ổn định khi Pi và Server chạy trong thời gian dài.

---

# NGÀY 26/09/2026

**GIAI ĐOẠN:** Chuẩn hóa và lưu trữ dự án  
**THỜI GIAN:** Cập nhật hiện tại

## 1. MỤC TIÊU
Đưa toàn bộ mã nguồn Server và Pi về chung một repository để tránh thất lạc phiên bản.

## 2. DỤNG CỤ & VẬT LIỆU SỬ DỤNG
- Git.
- GitHub.
- Repository `phandinhdoc-spec/nckh27vk`.

## 3. TIẾN TRÌNH THỰC HIỆN & HIỆN TƯỢNG
Trước đây phần Git chủ yếu nằm trong thư mục Server. Nhóm chuyển sang quản lí toàn bộ thư mục NCKH27VK bằng một repository chung để Server và Pi được lưu cùng một nơi.

## 4. KẾT QUẢ & SỐ LIỆU THÔ
- Toàn bộ dự án được đưa lên repository chung.
- Server và Pi hiện được quản lí trong cùng repository.
- **Chưa có đủ số liệu định lượng** về độ trễ, tỉ lệ trả lời đúng và độ ổn định chạy dài; đây là phần phải đo tiếp.

## 5. RÚT KINH NGHIỆM & LỖI SAI
Cấu trúc lưu trữ rõ ràng giúp tránh tình trạng sửa đúng code nhưng lại cập nhật nhầm repository.

## 6. KẾ HOẠCH TIẾP THEO
Tiếp tục kiểm thử thực tế, đo thời gian phản hồi và bổ sung số liệu định lượng cho báo cáo nghiên cứu.

**Ghi nhận sử dụng AI:** AI hỗ trợ hệ thống hóa lại nhật kí từ mã nguồn và lịch sử làm việc; nhóm cần kiểm tra lại từng mốc trước khi dùng trong hồ sơ chính thức.


## BẢNG SỐ LIỆU CẦN BỔ SUNG SAU THỬ NGHIỆM

| Nội dung đo | Cách đo dự kiến | Số lần thử tối thiểu | Kết quả |
|---|---|---:|---|
| Thời gian Server xử lí câu hỏi không cần ảnh | tính từ lúc nhận request đến lúc trả MP3 | 10 | Chưa đo |
| Thời gian xử lí câu hỏi có ảnh | cùng cách trên, có JPEG | 10 | Chưa đo |
| Tỉ lệ request thành công | số request thành công / tổng số request | 20 | Chưa đo |
| Độ ổn định chạy liên tục | cho Server chạy và ghi lỗi | 1–2 giờ | Chưa đo |

> **Nguyên tắc:** chỉ điền số sau khi nhóm trực tiếp thử và lưu kết quả; không dùng số do AI ước lượng.
