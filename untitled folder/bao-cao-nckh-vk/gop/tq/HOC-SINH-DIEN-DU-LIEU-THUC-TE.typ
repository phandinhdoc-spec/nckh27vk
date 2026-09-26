// HƯỚNG DẪN:
// 1. Chỉ thay nội dung trong dấu [...] bằng số liệu/ảnh đã đo hoặc kiểm chứng.
// 2. Không ước lượng, không chép số liệu mẫu. Giữ lại phiếu đo, ảnh gốc và log làm minh chứng.
// 3. Với ảnh, thay khối `cho-anh(...)` bằng: image("ten-anh.jpg", width: 100%)

#let can-dien(noi-dung) = text(fill: rgb("b00020"), weight: "bold")[#noi-dung]
#let cho-anh(noi-dung) = block(
  width: 100%,
  height: 4cm,
  stroke: 0.8pt + rgb("b00020"),
  inset: 10pt,
  align(center + horizon, can-dien(noi-dung)),
)
#let o-so-lieu = text(fill: rgb("b00020"), weight: "bold")[#raw("[____]")]

// A. Thông tin và nguồn chứng minh nhu cầu
#let nguon-so-lieu-nguoi-khiem-thi = [báo Thanh Niên, bài viết ngày 14/11/2025]
#let so-nguoi-khiem-thi = [gần 2 triệu người khiếm thị và người suy giảm thị lực]
#let bang-chung-khao-sat-nhu-cau = [tại khu nhà ở dành cho người khiếm thị, số 446 Lý Thái Tổ, phường Vườn Lài, TP Hồ Chí Minh]

// B. Cấu hình sản phẩm thực tế
#let bo-xu-ly-thuc-te = [Raspberry Pi Zero 2 W]
#let camera-thuc-te = [camera Raspberry Pi giao tiếp CSI chụp 640 × 480 rồi resize 224 × 224]
#let dau-ra-am-thanh-thuc-te = [loa mini qua mạch MAX98357A]
#let co-che-am-thanh-thuc-te = [tệp MP3 tiếng Việt ghi sẵn, phát cục bộ]
#let khoi-luong-tren-kinh = [104 g, không tính pin vì pin được đặt trong túi quần]
#let khoi-luong-toan-bo = [104 g, không tính pin; chưa có số cân toàn hệ thống vì loại pin có thể thay đổi]
#let dung-luong-pin = [pin sạc dự phòng 10000 mAh]
#let thoi-luong-pin = [gần 8 giờ chạy liên tục với pin 10000 mAh]
#let nhiet-do-cao-nhat = [60 °C ở CPU khi hoạt động ngoài trời nắng nóng, nhiệt độ môi trường khoảng 36 °C]
#let kich-thuoc-san-pham = [dạng vòng tròn; bán kính thay đổi bằng khóa cài phía sau để phù hợp với kích thước đầu]
#let tong-chi-phi-thuc-te = [1.937.000 đồng]
#let danh-sach-linh-kien-va-gia = [camera và module xử lý: 1.500.000 đồng; pin và mạch sạc: 160.000 đồng; loa và mạch MAX98357A: 105.000 đồng; vỏ in 3D và dây đeo: 140.000 đồng; công tắc: 32.000 đồng]
#let ma-nguon-thuc-te = [Mã nguồn chương trình nhận diện]
#let phien-ban-phan-mem = [chương trình dùng Python trên Linux ARM64; nhận diện bằng TensorFlow Lite; camera dùng rpicam-jpeg, âm thanh dùng mpg123]

// C. Dữ liệu và mô hình AI
#let so-anh-goc = [3.635 ảnh]
#let so-vat-the-doc-lap = [97 vật thể]
#let cach-chia-du-lieu = [80% train, 10% test, 10% validation; ảnh không xuất hiện đồng thời ở các tập]
#let so-epoch = [17 epoch]
#let kich-thuoc-model = [3,1 MB]
#let accuracy-train = can-dien[91%]
#let accuracy-validation = [82,6%]
#let accuracy-test = [94,58%]
#let bieu-do-huan-luyen = cho-anh[#image("image/training_history.png")]

// D. Bảng kiểm thử độc lập; các ô phải khớp với ma trận nhầm lẫn bên dưới
#let n-huu-co-test = [389]
#let dung-huu-co-test = [346]
#let n-vo-co-test = [503]
#let dung-vo-co-test = [472]
#let n-khac-test = [308]
#let dung-khac-test = [239]
#let cm-huu-co-huu-co-test = [346]
#let cm-huu-co-vo-co-test = [29]
#let cm-huu-co-khac-test = [14]
#let cm-vo-co-huu-co-test = [11]
#let cm-vo-co-vo-co-test = [472]
#let cm-vo-co-khac-test = [20]
#let cm-khac-huu-co-test = [9]
#let cm-khac-vo-co-test = [60]
#let cm-khac-khac-test = [239]
#let tong-mau-test = [1.200]
#let tong-dung-test = [1.057]
#let phan-tich-loi-thuc-te = [Ma trận ghi nhận rác khác bị nhầm sang vô cơ 60 lần, là lỗi lớn nhất; rác hữu cơ bị nhầm sang vô cơ 29 lần; rác vô cơ bị nhầm sang rác khác 20 lần.]

// E. Độ trễ, ánh sáng và khả dụng
#let so-lan-do-do-tre = [50]
#let do-tre-trung-binh = [2]
#let do-tre-trung-vi = can-dien[độ trễ trung vị, giây]
#let do-tre-lon-nhat = [3]
#let ket-qua-ngoai-troi = [95%]
#let ket-qua-trong-nha = [90%]
#let ket-qua-anh-sang-yeu = [75%]
#let giai-phap-anh-sang-da-thu = can-dien[giải pháp đã lắp và kết quả trước/sau; để trống nếu mới là hướng phát triển]
#let doi-tuong-thu-nghiem = [5 người tham gia mô phỏng trong trạng thái bịt mắt, có sự đồng ý trước khi thử]
#let quy-trinh-thu-nghiem-nguoi-dung = [mỗi người tham gia thực hiện 10 lượt thử nghiệm với các vật thể đã chuẩn bị; nhóm ghi thời gian và kết quả bỏ rác khi không dùng thiết bị và khi dùng AI-Green Eye]
#let ket-qua-khong-thiet-bi = [thời gian khoảng 45 giây mỗi lượt; tỉ lệ nhận biết sai 60%]
#let ket-qua-co-thiet-bi = [thời gian khoảng 5–7 giây mỗi lượt; rác được bỏ đúng thùng 90%]
#let han-che-thu-nghiem-nguoi-dung = [người tham gia là học sinh bịt mắt, không phải người khiếm thị; số người và số lượt còn ít; chưa có đủ ảnh minh chứng cho toàn bộ quá trình]

// F. Ảnh và bản vẽ bắt buộc thay bằng tư liệu thật
#let anh-san-pham-hoan-chinh = cho-anh[ảnh rõ toàn bộ mẫu thử hoàn chỉnh]
#let anh-bo-tri-phan-cung = cho-anh[ảnh các module trên kính, dây và hộp xử lý]
#let anh-can-khoi-luong = cho-anh[ảnh cân phần trên kính và toàn bộ thiết bị]
#let anh-ban-ve-cad = cho-anh[ảnh chụp màn hình/bản xuất CAD có kích thước]
#let anh-nhan-braille = cho-anh[ảnh nhãn Braille thật và thước đo khoảng cách chấm]
#let anh-thu-nghiem = cho-anh[ảnh thử nghiệm có sự đồng ý của người tham gia]

// G. Tài liệu tham khảo kỹ thuật/thực trạng thực sự đã đọc
#let tai-lieu-tham-khao-bo-sung = can-dien[tài liệu mạng nơ-ron, chuẩn Braille, nguồn dữ liệu và nghiên cứu liên quan]
#let n-ngoai-troi = [500]
#let dung-ngoai-troi = [475]
#let sai-ngoai-troi = [25]
#let n-trong-nha = [380]
#let dung-trong-nha = [342]
#let sai-trong-nha = [38]
#let n-toi = [320]
#let dung-toi = [240]
#let sai-toi = [80]
