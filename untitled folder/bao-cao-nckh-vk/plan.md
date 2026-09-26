# Plan — làm sạch tq-end2.typ (NCKH27VK)

Run: run_20260924_193720_609c79
File gốc: /Users/phananh/TEMP/NCKH27VK/bao-cao-nckh-vk/tq-end2.typ
Bản làm việc: tq-end2-work.typ

## Baseline (W1.1)
- hash gốc tq-end2.typ: 4f5d4c3294a4579a85fe4340121aef25effe2a33
- hash bản làm việc: bằng nhau (cp byte-copy)
- typst compile: exit 0
- pdfinfo: 26 trang, A4 (595.276 x 841.89 pts)
- chars: 79313
- grep đếm cụm cũ: "cuộc thi hè"=2, "phân loại rác"=8, "bản dự thi hè"=1

## Cấu trúc đề mục (=A/B/C/D)
- A. LÝ DO CHỌN DỰ ÁN (dòng 224)
- B. CÂU HỎI NGHIÊN CỨU, VẤN ĐỀ NGHIÊN CỨU VÀ GIẢ THUYẾT KHOA HỌC (dòng 257-497, 8 tiểu mục)
- C. TIẾN HÀNH NGHIÊN CỨU (dòng 498-897)
- D. TÀI LIỆU THAM KHẢO (dòng 898)

## Phân loại dấu vết dự án cũ (W1.2) — từ grep tất định

(a) Biến #let chết (KHÔNG được dùng ở đâu, grep #(<tên>) = 0):
  Dòng 113-150: phan-tich-loi-thuc-te, n-huu-co-test, dung-huu-co-test,
  n-vo-co-test, dung-vo-co-test, n-khac-test, dung-khac-test,
  cm-huu-co-huu-co-test, cm-huu-co-vo-co-test, cm-huu-co-khac-test,
  cm-vo-co-huu-co-test, cm-vo-co-vo-co-test, cm-vo-co-khac-test,
  cm-khac-huu-co-test, cm-khac-vo-co-test, cm-khac-khac-test,
  tong-mau-test, tong-dung-test, so-lan-do-do-tre, do-tre-trung-binh,
  do-tre-lon-nhat, ket-qua-ngoai-troi, ket-qua-trong-nha,
  ket-qua-anh-sang-yeu, doi-tuong-thu-nghiem, quy-trinh-thu-nghiem-nguoi-dung,
  ket-qua-khong-thiet-bi, ket-qua-co-thiet-bi, han-che-thu-nghiem-nguoi-dung,
  n-ngoai-troi, dung-ngoai-troi, sai-ngoai-troi, n-trong-nha, dung-trong-nha,
  sai-trong-nha, n-toi, dung-toi, sai-toi, so-anh-goc, so-vat-the-doc-lap,
  cach-chia-du-lieu, so-epoch, kich-thuoc-model, so-lop-vat-the,
  accuracy-train, accuracy-validation, accuracy-test
  -> Tất cả XOÁ (trừ biến live còn dùng: khoi-luong-*, bang-chung-khao-sat-nhu-cau,
  tong-chi-phi-thuc-te, danh-sach-linh-kien-va-gia... giữ)

(b) Khối // bình luận nội dung dự án cũ (XOÁ):
  mục A: dòng 239-243 (khó khăn phân loại rác cũ), 251 (caption cũ)
  mục B: 266-271 (vấn đề cũ), 282-288 (mục tiêu cũ), 319/393/443 (ghi chú đổi chương),
          332-339 (bảng kế hoạch cũ), 377-382 (phương pháp cũ), 397, 431, 446, 450
  -> treo cụm "giữ lại để đối chiếu" không còn phù hợp cho báo cáo chính thức

(c) Live text cần viết lại (bỏ dẫn cuộc thi hè, giữ ý):
  dòng 704: "Ở bản dự thi hè, toàn bộ việc nhận diện chạy trực tiếp trên thiết bị..."
    -> viết lại "Ở phương án chạy trực tiếp trên thiết bị (không qua API)..."
  dòng 855: "Các số liệu huấn luyện, tập dữ liệu, độ chính xác phân loại rác và hình
    biểu đồ trong hồ sơ cuộc thi hè thuộc phiên bản cũ..."
    -> bỏ "hồ sơ cuộc thi hè", nói là số liệu phiên bản chạy on-device cũ
  dòng 885: "...Số liệu và mô hình của báo cáo cuộc thi hè không thể đại diện..."
    -> bỏ "của báo cáo cuộc thi hè"

(d) Ứng viên chuyển Phụ lục (W3.1 quyết):
  mô tả chi tiết nhãn Braille/thùng rác 785-842 (giữ, đưa Phụ lục nếu dài)
  các bảng chi tiết mở rộng (nếu có) — quyết định khi làm T3

## Tiêu chí nghiệm thu
- typst compile tq-end2-work.typ exit 0; pdfinfo A4
- grep âm trên .typ lẫn pdftotext: cuộc thi hè, dự thi hè, trại hè, Cuộc thi Sáng tạo
  dành cho thanh thiếu niên, n-huu-co, cm-*, tong-mau-test, phan-tich-loi-thuc-te
- file gốc tq-end2.typ giữ nguyên hash
- "phân loại rác" chỉ còn ở vai hỏi đáp phụ hiện tại (thead hợp lệ)