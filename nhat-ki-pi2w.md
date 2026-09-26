# NHẬT KÍ NGHIÊN CỨU DỰ ÁN — PHẦN RASPBERRY PI ZERO 2 W

> **Tên đề tài:** AI - Green - Eye  
> **Phần phụ trách:** Thiết bị đeo Raspberry Pi Zero 2 W  
> **Nhóm thực hiện:** Học sinh THCS  
> **Giáo viên hướng dẫn:** ................................................  
> **Ngày bắt đầu:** 08/05/2026  
> **Ngày cập nhật gần nhất:** 26/09/2026  

## Lưu ý về cách ghi nhật kí

Nhật kí này được tái dựng từ quá trình phát triển thực tế, tài liệu và mã nguồn hiện còn lưu. Một số mốc trước tháng 9/2026 không còn giờ làm việc chính xác nên được ghi theo tiến trình hợp lí của dự án. Nội dung được viết theo cách học sinh THCS có thể hiểu, có thể tự trình bày khi báo cáo sản phẩm.

AI được dùng để hỗ trợ giải thích nguyên lí cảm biến, gợi ý cách lập trình, tìm lỗi và so sánh phương án. Nhóm học sinh vẫn phải tự lắp mạch, chạy thử, quan sát kết quả, ghi lại lỗi và quyết định giữ hay thay đổi phương án.

---

# NGÀY 08/05/2026

**GIAI ĐOẠN:** Chọn thiết bị trung tâm  
**THỜI GIAN:** Không ghi lại chính xác – tái dựng hồi cứu

## 1. MỤC TIÊU
Chọn một máy tính nhỏ có thể gắn trên thiết bị đeo, kết nối camera, mic, loa và cảm biến.

## 2. DỤNG CỤ & VẬT LIỆU SỬ DỤNG
- Raspberry Pi Zero 2 W.
- Camera Raspberry Pi.
- Mic USB.
- Loa nhỏ.

## 3. TIẾN TRÌNH THỰC HIỆN & HIỆN TƯỢNG
Nhóm khảo sát Raspberry Pi Zero 2 W vì thiết bị nhỏ, có Wi‑Fi, chạy Linux và có thể điều khiển camera, âm thanh và cảm biến. Tuy nhiên khả năng xử lí AI nặng bị hạn chế.

Nhóm quyết định Pi sẽ đóng vai trò “bộ điều khiển tại chỗ”: thu dữ liệu, gửi lên Server và nhận câu trả lời về phát cho người dùng.

## 4. KẾT QUẢ & SỐ LIỆU THÔ
- Chọn Raspberry Pi Zero 2 W làm thiết bị chính.
- Không chạy AI nặng trực tiếp trên Pi.

## 5. RÚT KINH NGHIỆM & LỖI SAI
Thiết bị nhỏ phù hợp để đeo nhưng phải tiết kiệm tài nguyên và pin.

## 6. KẾ HOẠCH TIẾP THEO
Thử camera và xác định cách gắn camera trên đầu người dùng.

---

# NGÀY 18/05/2026

**GIAI ĐOẠN:** Khảo sát camera  
**THỜI GIAN:** Không ghi lại chính xác – tái dựng hồi cứu

## 1. MỤC TIÊU
Kiểm tra camera có thể dùng để quan sát vật phía trước hay không.

## 2. DỤNG CỤ & VẬT LIỆU SỬ DỤNG
- Raspberry Pi Zero 2 W.
- Raspberry Pi Camera Module 3, góc nhìn khoảng 75°.
- Cáp camera.

## 3. TIẾN TRÌNH THỰC HIỆN & HIỆN TƯỢNG
Camera được dự kiến đặt gần tầm mắt để hình ảnh thu được gần với hướng nhìn của người dùng. Nhóm thử chụp ảnh trong nhà và nhận thấy góc camera, độ cao camera và độ nghiêng đều ảnh hưởng mạnh đến việc ước lượng vị trí vật.

## 4. KẾT QUẢ & SỐ LIỆU THÔ
- Camera có thể chụp ảnh đủ để AI nhận dạng vật.
- Xác định cần biết độ cao camera và góc nghiêng để hỗ trợ tính khoảng cách thực tế.

## 5. RÚT KINH NGHIỆM & LỖI SAI
Chỉ nhìn ảnh 2D thì khó biết chính xác vật cách người dùng bao xa.

## 6. KẾ HOẠCH TIẾP THEO
Bổ sung cảm biến đo khoảng cách hướng cùng trục camera.

---

# NGÀY 29/05/2026

**GIAI ĐOẠN:** Bổ sung cảm biến khoảng cách  
**THỜI GIAN:** Không ghi lại chính xác – tái dựng hồi cứu

## 1. MỤC TIÊU
Có một khoảng cách thực làm mốc cho ảnh camera.

## 2. DỤNG CỤ & VẬT LIỆU SỬ DỤNG
- Camera.
- Cảm biến ToF GY-53-L1X / VL53L1X.
- Raspberry Pi.

## 3. TIẾN TRÌNH THỰC HIỆN & HIỆN TƯỢNG
Nhóm đề xuất đặt cảm biến đo khoảng cách sát camera và hướng gần như cùng trục với camera. Cảm biến sẽ đo khoảng cách đến vật gần trung tâm ảnh. Giá trị này được dùng như một “thước đo thật” để hỗ trợ suy ra khoảng cách tới các vật khác trong ảnh.

## 4. KẾT QUẢ & SỐ LIỆU THÔ
- Chọn hướng dùng cảm biến ToF làm mốc khoảng cách.
- Xác định cảm biến phải được lắp thẳng hướng với camera.

## 5. RÚT KINH NGHIỆM & LỖI SAI
Nếu cảm biến nhìn lệch camera thì khoảng cách đo được có thể thuộc về vật khác với vật ở giữa ảnh.

## 6. KẾ HOẠCH TIẾP THEO
Tìm cách đo góc nghiêng camera.

---

# NGÀY 10/06/2026

**GIAI ĐOẠN:** Đo góc nghiêng thiết bị  
**THỜI GIAN:** Không ghi lại chính xác – tái dựng hồi cứu

## 1. MỤC TIÊU
Biết camera đang hướng xuống hay hướng lên bao nhiêu so với mặt đất.

## 2. DỤNG CỤ & VẬT LIỆU SỬ DỤNG
- Hai cảm biến chuyển động MPU6050/GY-25.
- Raspberry Pi.

## 3. TIẾN TRÌNH THỰC HIỆN & HIỆN TƯỢNG
Nhóm nhận thấy nếu chỉ biết khoảng cách từ camera đến vật thì chưa đủ. Khi người dùng cúi đầu hoặc ngẩng đầu, hướng nhìn thay đổi. Nhóm dùng cảm biến chuyển động để đo góc nghiêng. Phương án dùng hai cảm biến được xem xét để tăng độ tin cậy và kiểm tra chéo sai số.

## 4. KẾT QUẢ & SỐ LIỆU THÔ
- Xác định góc nghiêng là dữ liệu cần thiết.
- Chọn dùng cảm biến chuyển động để theo dõi tư thế camera.

## 5. RÚT KINH NGHIỆM & LỖI SAI
Khoảng cách trong ảnh không thể suy ra chính xác nếu bỏ qua tư thế camera.

## 6. KẾ HOẠCH TIẾP THEO
Bổ sung cảm biến áp suất để theo dõi thay đổi độ cao.

---

# NGÀY 22/06/2026

**GIAI ĐOẠN:** Khảo sát cảm biến GY63  
**THỜI GIAN:** Không ghi lại chính xác – tái dựng hồi cứu

## 1. MỤC TIÊU
Đo áp suất không khí và ước lượng thay đổi độ cao của thiết bị.

## 2. DỤNG CỤ & VẬT LIỆU SỬ DỤNG
- Module GY63.
- Cảm biến MS5611-01BA03.
- Raspberry Pi.

## 3. TIẾN TRÌNH THỰC HIỆN & HIỆN TƯỢNG
Nhóm tìm hiểu và xác định GY63 đang dùng cảm biến áp suất MS5611-01BA03. Cảm biến có thể đo áp suất và từ đó ước lượng độ cao tương đối.

Dữ liệu này không tự xác định được vật thể, nhưng có ích để biết thiết bị đang thay đổi độ cao, hỗ trợ thêm cho việc hiểu tư thế và chuyển động của người dùng.

## 4. KẾT QUẢ & SỐ LIỆU THÔ
- GY63 được chọn làm cảm biến áp suất.
- Giao tiếp dự kiến bằng I2C.

## 5. RÚT KINH NGHIỆM & LỖI SAI
Độ cao tính từ áp suất chỉ là giá trị hỗ trợ vì áp suất môi trường có thể thay đổi.

## 6. KẾ HOẠCH TIẾP THEO
Thiết kế phần âm thanh để người dùng có thể nói lệnh và nghe câu trả lời.

---

# NGÀY 05/07/2026

**GIAI ĐOẠN:** Thiết kế giao tiếp bằng giọng nói  
**THỜI GIAN:** Không ghi lại chính xác – tái dựng hồi cứu

## 1. MỤC TIÊU
Cho người dùng tương tác mà không cần nhìn màn hình hoặc bấm nhiều nút.

## 2. DỤNG CỤ & VẬT LIỆU SỬ DỤNG
- Mic USB.
- Loa.
- Raspberry Pi.

## 3. TIẾN TRÌNH THỰC HIỆN & HIỆN TƯỢNG
Nhóm chọn điều khiển bằng giọng nói. Mic USB được ưu tiên vì dễ kết nối và ổn định. Người dùng sẽ nói một từ khóa đánh thức rồi nói yêu cầu, ví dụ hỏi phía trước có gì.

## 4. KẾT QUẢ & SỐ LIỆU THÔ
- Chọn mic USB làm nguồn thu chính.
- Dự kiến dùng từ khóa “Thiên Nhãn”.

## 5. RÚT KINH NGHIỆM & LỖI SAI
Nếu mic luôn gửi toàn bộ âm thanh lên mạng thì vừa tốn dữ liệu vừa ảnh hưởng riêng tư. Cần cắt đúng đoạn có tiếng nói.

## 6. KẾ HOẠCH TIẾP THEO
Tìm cách phát hiện đoạn có giọng nói và chỉ gửi đoạn cần thiết.

---

# NGÀY 19/07/2026

**GIAI ĐOẠN:** Phát hiện đoạn có tiếng nói  
**THỜI GIAN:** Không ghi lại chính xác – tái dựng hồi cứu

## 1. MỤC TIÊU
Giữ mic hoạt động liên tục nhưng không gửi âm thanh khi người dùng im lặng.

## 2. DỤNG CỤ & VẬT LIỆU SỬ DỤNG
- Mic USB.
- Python.
- Công cụ `arecord`.

## 3. TIẾN TRÌNH THỰC HIỆN & HIỆN TƯỢNG
Pi giữ một luồng mic mở liên tục. Chương trình đo mức âm thanh nền, rồi chỉ bắt đầu ghi một câu khi tín hiệu vượt ngưỡng trong một khoảng thời gian ngắn. Khi người dùng im lặng đủ lâu, câu nói được kết thúc.

## 4. KẾT QUẢ & SỐ LIỆU THÔ
- Mic không phải đóng/mở liên tục.
- Có cơ chế VAD đơn giản dựa trên mức âm thanh.

## 5. RÚT KINH NGHIỆM & LỖI SAI
Ngưỡng cố định có thể sai ở nơi quá ồn hoặc quá yên, nên cần dựa thêm vào tiếng ồn nền.

## 6. KẾ HOẠCH TIẾP THEO
Gửi đoạn âm thanh đã cắt để chuyển thành văn bản.

---

# NGÀY 03/08/2026

**GIAI ĐOẠN:** Nhận dạng giọng nói  
**THỜI GIAN:** Không ghi lại chính xác – tái dựng hồi cứu

## 1. MỤC TIÊU
Chuyển câu nói tiếng Việt thành văn bản để Server hiểu được.

## 2. DỤNG CỤ & VẬT LIỆU SỬ DỤNG
- Mic USB.
- MP3.
- Groq Whisper.

## 3. TIẾN TRÌNH THỰC HIỆN & HIỆN TƯỢNG
Đoạn âm thanh PCM được mã hóa sang MP3 rồi gửi tới dịch vụ nhận dạng giọng nói. Kết quả trả về là văn bản tiếng Việt.

Nhóm thử hai kiểu nói: “Thiên Nhãn mấy giờ rồi” trong một câu và nói “Thiên Nhãn”, sau đó mới nói câu hỏi ở lượt tiếp theo.

## 4. KẾT QUẢ & SỐ LIỆU THÔ
- Nhận dạng được câu lệnh tiếng Việt.
- Từ khóa đánh thức hỗ trợ cả dạng cùng câu và hai lượt.

## 5. RÚT KINH NGHIỆM & LỖI SAI
Cần bỏ qua các câu không có từ khóa để tránh kích hoạt nhầm.

## 6. KẾ HOẠCH TIẾP THEO
Ghép câu lệnh văn bản với camera và Server.

---

# NGÀY 16/08/2026

**GIAI ĐOẠN:** Ghép camera với câu lệnh  
**THỜI GIAN:** Không ghi lại chính xác – tái dựng hồi cứu

## 1. MỤC TIÊU
Chỉ chụp ảnh khi người dùng thật sự hỏi về vật trước mặt.

## 2. DỤNG CỤ & VẬT LIỆU SỬ DỤNG
- Camera.
- Python.
- Danh sách từ khóa thị giác.

## 3. TIẾN TRÌNH THỰC HIỆN & HIỆN TƯỢNG
Nhóm tạo danh sách từ như “nhìn”, “xem”, “trước mặt”, “cái này”, “màn hình”. Nếu câu lệnh chứa các từ này, Pi chụp ảnh JPEG rồi gửi cùng câu lệnh. Nếu không, Pi chỉ gửi văn bản.

## 4. KẾT QUẢ & SỐ LIỆU THÔ
- Giảm số lần chụp và gửi ảnh không cần thiết.
- Luồng câu lệnh nhanh hơn đối với câu hỏi không cần camera.

## 5. RÚT KINH NGHIỆM & LỖI SAI
Danh sách từ khóa chỉ là giải pháp tạm thời; có thể bỏ sót những cách nói khác nghĩa giống nhau.

## 6. KẾ HOẠCH TIẾP THEO
Hoàn thiện phần phát âm thanh trả lời.

---

# NGÀY 30/08/2026

**GIAI ĐOẠN:** Phát âm thanh qua loa  
**THỜI GIAN:** Không ghi lại chính xác – tái dựng hồi cứu

## 1. MỤC TIÊU
Phát câu trả lời của Server trực tiếp cho người dùng nghe.

## 2. DỤNG CỤ & VẬT LIỆU SỬ DỤNG
- Mạch MAX98357A.
- Loa nhỏ.
- Raspberry Pi.

## 3. TIẾN TRÌNH THỰ HIỆN & HIỆN TƯỢNG
Nhóm chọn mạch khuếch đại âm thanh MAX98357A nối với các chân I2S của Pi. MP3 trả về từ Server được phát qua loa này.

Đường âm thanh chính được cố định qua MAX98357A để tránh phụ thuộc tai nghe Bluetooth.

## 4. KẾT QUẢ & SỐ LIỆU THÔ
- Loa có thể phát phản hồi từ Server.
- Bluetooth không còn là điều kiện bắt buộc để thiết bị hoạt động.

## 5. RÚT KINH NGHIỆM & LỖI SAI
Bluetooth có thể kết nối chậm hoặc không ổn định, nên không nên dùng làm đường âm thanh duy nhất.

## 6. KẾ HOẠCH TIẾP THEO
Gộp mic, camera, cảm biến và loa thành chương trình chính.

---

# NGÀY 10/09/2026

**GIAI ĐOẠN:** Gộp các thiết bị ngoại vi  
**THỜI GIAN:** Không ghi lại chính xác – tái dựng hồi cứu

## 1. MỤC TIÊU
Để Pi có thể đồng thời quản lí mic, camera, cảm biến và âm thanh.

## 2. DỤNG CỤ & VẬT LIỆU SỬ DỤNG
- Raspberry Pi Zero 2 W.
- GY25.
- GY63.
- Camera.
- Mic USB.
- MAX98357A.

## 3. TIẾN TRÌNH THỰC HIỆN & HIỆN TƯỢNG
Mã nguồn được chia thành các file như `devices.py`, `sensors.py`, `config.py`, `history.py` và `app.py`. Cảm biến GY25 được đọc qua UART; GY63 được đọc qua I2C.

Nếu một cảm biến bị lỗi hoặc chưa cắm, chương trình vẫn tiếp tục chạy và trả giá trị rỗng thay vì dừng toàn bộ hệ thống.

## 4. KẾT QUẢ & SỐ LIỆU THÔ
- Pi có thể đọc nhiều thiết bị trong một chương trình.
- Thiếu một cảm biến không làm hệ thống ngừng hoàn toàn.

## 5. RÚT KINH NGHIỆM & LỖI SAI
Thiết bị thật phải chịu được tình huống một phần cứng bị rút hoặc mất kết nối.

## 6. KẾ HOẠCH TIẾP THEO
Chuẩn hóa cách cài đặt trên DietPi.

---

# NGÀY 20/09/2026

**GIAI ĐOẠN:** Chuẩn hóa cài đặt Raspberry Pi  
**THỜI GIAN:** Theo tiến trình phát triển hiện tại

## 1. MỤC TIÊU
Có một quy trình cài đặt lại Pi mà không phải nhớ từng lệnh thủ công.

## 2. DỤNG CỤ & VẬT LIỆU SỬ DỤNG
- DietPi Trixie ARM64.
- Script `setup_pi2w.sh`.
- SSH.

## 3. TIẾN TRÌNH THỰ HIỆN & HIỆN TƯỢNG
Nhóm viết script để cài các gói cần thiết, bật camera, UART, I2C, cấu hình loa, cài chương trình vào `/opt/thiennhan` và tạo service tự chạy.

Nhờ script này, nếu Pi phải cài lại hệ điều hành thì có thể phục hồi môi trường nhanh hơn và giảm lỗi do quên bước.

## 4. KẾT QUẢ & SỐ LIỆU THÔ
- Có script cài đặt tự động.
- Chương trình có thể chạy bằng service và tự khởi động lại khi lỗi.

## 5. RÚT KINH NGHIỆM & LỖI SAI
Cài thủ công từng lần rất dễ tạo ra hai Pi có cấu hình khác nhau.

## 6. KẾ HOẠCH TIẾP THEO
Kiểm tra lại sau khi cài mới DietPi.

---

# NGÀY 24/09/2026

**GIAI ĐOẠN:** Đấu nối cảm biến với Pi  
**THỜI GIAN:** Theo thử nghiệm phần cứng thực tế

## 1. MỤC TIÊU
Kết nối cảm biến chuyển động và cảm biến áp suất với Raspberry Pi đúng chân.

## 2. DỤNG CỤ & VẬT LIỆU SỬ DỤNG
- Raspberry Pi Zero 2 W.
- GY25/MPU6050.
- GY63/MS5611-01BA03.
- Dây nối.

## 3. TIẾN TRÌNH THỰ HIỆN & HIỆN TƯỢNG
Nhóm chuẩn hóa kết nối GY25 qua UART và GY63 qua I2C. GY63 dùng bus I2C số 1, với SDA ở GPIO2 và SCL ở GPIO3. GY25 dùng cổng serial của Pi.

## 4. KẾT QUẢ & SỐ LIỆU THÔ
- GY25 cung cấp yaw, pitch, roll.
- GY63 cung cấp áp suất, nhiệt độ và độ cao ước lượng.

## 5. RÚT KINH NGHIỆM & LỖI SAI
Phải phân biệt số GPIO và số chân vật lí trên Pi; nhầm hai loại số này có thể đấu sai mạch.

## 6. KẾ HOẠCH TIẾP THEO
Kiểm tra toàn bộ chương trình trên Pi vừa cài lại.

---

# NGÀY 25/09/2026

**GIAI ĐOẠN:** Cài lại DietPi và kiểm tra SSH  
**THỜI GIAN:** Theo thử nghiệm thực tế

## 1. MỤC TIÊU
Đưa Pi trở lại trạng thái sạch và kiểm tra kết nối từ Mac.

## 2. DỤNG CỤ & VẬT LIỆU SỬ DỤNG
- Raspberry Pi Zero 2 W.
- DietPi.
- MacBook.
- SSH.

## 3. TIẾN TRÌNH THỰC HIỆN & HIỆN TƯỢNG
Sau khi cài lại DietPi, nhóm kiểm tra địa chỉ mạng và thử SSH từ Mac vào Pi. Đồng thời rà lại file setup để đảm bảo các phần camera, âm thanh, UART, I2C và service vẫn phù hợp với hệ điều hành mới.

## 4. KẾT QUẢ & SỐ LIỆU THÔ
- Pi có thể được quản lí từ xa qua SSH.
- Có thể tiếp tục triển khai mã nguồn mà không cần gắn màn hình và bàn phím vào Pi.

## 5. RÚT KINH NGHIỆM & LỖI SAI
Khi cài lại hệ điều hành, địa chỉ IP, tên thiết bị hoặc cấu hình mạng có thể thay đổi nên cần kiểm tra lại trước khi cho rằng chương trình bị lỗi.

## 6. KẾ HOẠCH TIẾP THEO
Đưa code Pi vào repository chung và kiểm tra luồng với Server.

---

# NGÀY 26/09/2026

**GIAI ĐOẠN:** Chuẩn hóa mã nguồn và lưu trữ dự án  
**THỜI GIAN:** Cập nhật hiện tại

## 1. MỤC TIÊU
Đưa mã nguồn Pi và Server về cùng một repository để dễ theo dõi phiên bản.

## 2. DỤNG CỤ & VẬT LIỆU SỬ DỤNG
- Git.
- GitHub.
- Repository `phandinhdoc-spec/nckh27vk`.

## 3. TIẾN TRÌNH THỰC HIỆN & HIỆN TƯỢNG
Toàn bộ thư mục NCKH27VK được chuyển sang quản lí chung bằng Git. Phần Pi hiện có chương trình Python, file cấu hình, driver cảm biến, lịch sử dữ liệu, chương trình kiểm tra camera và script cài đặt Pi.

Luồng hiện tại được xác định rõ: mic USB → phát hiện tiếng nói → nhận dạng giọng nói → kiểm tra từ khóa “Thiên Nhãn” → đọc cảm biến → chụp ảnh nếu cần → gửi lệnh lên Server → nhận MP3 → phát qua MAX98357A.

## 4. KẾT QUẢ & SỐ LIỆU THÔ
- Mã nguồn Pi được lưu cùng Server trên GitHub.
- Pi chỉ làm phần thu nhận dữ liệu và điều khiển thiết bị, không chạy AI nặng.
- Dữ liệu mic không được lưu lâu dài; ảnh và âm thanh phản hồi có cơ chế lưu lịch sử giới hạn.

## 5. RÚT KINH NGHIỆM & LỖI SAI
Hệ thống đã có kiến trúc rõ nhưng vẫn cần nhiều số liệu thực nghiệm như thời gian phản hồi, tỉ lệ nhận đúng câu lệnh, độ chính xác cảm biến và thời lượng pin.

## 6. KẾ HOẠCH TIẾP THEO
- Đo thời gian từ lúc người dùng nói đến lúc loa phát câu trả lời.
- Thử ở môi trường ồn và yên.
- Đo sai số cảm biến khoảng cách và góc nghiêng.
- Kiểm tra độ ổn định khi thiết bị chạy liên tục.
- Bổ sung các số liệu thực nghiệm vào báo cáo nghiên cứu.

**Ghi nhận sử dụng AI:** AI hỗ trợ hệ thống hóa nhật kí từ mã nguồn và quá trình làm việc; nhóm cần kiểm tra lại từng mốc trước khi dùng trong hồ sơ chính thức.
