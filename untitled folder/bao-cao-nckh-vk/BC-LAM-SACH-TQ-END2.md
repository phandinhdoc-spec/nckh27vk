# Báo cáo cuối — Làm sạch tq-end2.typ (dấu vết cuộc thi khác)

Kết quả: ĐẠT

## Giao nộp
- Bản Typst đã sửa: /Users/phananh/TEMP/NCKH27VK/bao-cao-nckh-vk/tq-end2-work.typ
- PDF giao nộp:      /Users/phananh/TEMP/NCKH27VK/bao-cao-nckh-vk/tq-end2.pdf
  (27 trang, A4; lệnh biên dịch: `typst compile tq-end2-work.typ tq-end2.pdf`)
- File gốc tq-end2.typ KHÔNG đổi (hash 4f5d4c…3533 = như ban đầu).
- Backups: tq-end2.typ.bak-hd (bản trước), tq-end2.pdf.bak-* (PDF cũ).

## Nhóm thay đổi chính
1. Mục B (CÂU HỎI/ VẤN ĐỀ/ GIẢ THUYẾT/ THIẾT KẾ-PHƯƠNG PHÁP) được làm sạch khỏi mọi khối `//` nội dung dự án cũ (phân loại rác làm nòng cốt); nội dung live của mục B giờ nhất quán với luồng hiện tại: hỏi đáp giọng nói qua Gemini+CommandCode API, vòng đeo in 3D, cảm biến GY25/GY53L1X tránh vật cản.
2. Xoá 140 dòng (biến `#let` chết dòng 104-150 + khối bình luận/mô tả dự án cũ khắp file, gồm cả bìa cũ của cuộc thi Sáng tạo, "phân loại rác", "24 nhãn", "bài thi cấp thành phố").
3. Viết lại live text, bỏ mọi ám chỉ cuộc thi hè/dự thi hè/hồ sơ cuộc thi cũ mà giữ nguyên nghĩa kỹ thuật (4 câu ở "Quá trình hoàn thiện chương trình", "Kiểm thử hệ thống hiện hành", "Hạn chế", "Kết luận khoa học"). Theo góp ý kiểm chéo độc lập, câu ở "Kiểm thử hệ thống hiện hành" được viết lại gọn hơn (tránh lặp từ).
4. Chuyển mục "Làm nhãn chữ nổi Braille cho thùng rác" (bảng chấm Braille + 2 hình) sang mục mới "= PHỤ LỤC" đặt sau "D. TÀI LIỆU THAM KHẢO" (thành E. PHỤ LỤC) — chuẩn NCKH. Tham chiếu cũ "mục 8" đã đổi thành "chi tiết tại Phụ lục".

## Kiểm chứng
- typst compile exit 0; pdfinfo: 27 trang, A4 (595.276 x 841.89 pts).
- Số `image()`: 22 = 22; cả 19 đường dẫn ảnh tồn tại trên đĩa.
- Grep âm (cả .typ lẫn pdftotext) = 0: cuộc thi hè, dự thi hè, trại hè, Cuộc thi Sáng tạo, bài thi (cấp thành phố), phiên bản thi hè, hồ sơ cuộc thi, n-huu-co, cm-*, tong-mau-test, phan-tich-loi-thuc-te.
- Cụm "phân loại rác" còn đúng 2 chỗ hợp lệ (vai hỏi đáp phụ của thiết bị; và mô tả bối cảnh phương án mẫu ban đầu), đúng ngoại lệ đã ghi.
- File gốc tq-end2.typ không đổi hash.

## Ghi nhận
- Báo cáo còn 27 trang, chưa đạt quy định "≤ 15 trang A4". Việc giảm trang được giữ RIÊNG (ngoài phạm vi lần này) theo thoả thuận; cần làm tiếp nếu nộp chính thức.
- Kiểm chéo độc lập (AGY gemini-3.8-flash-high, read-only) xác nhận: sạch dấu vết cuộc thi khác; cách đặt Phụ lục sau Tài liệu tham khảo đúng chuẩn.