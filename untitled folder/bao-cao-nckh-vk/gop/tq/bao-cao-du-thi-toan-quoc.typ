#set page(
  paper: "a4",
  margin: (x: 2cm, top: 2.5cm, bottom: 2.5cm),
  header: context {
    if counter(page).get().first() > 1 {
      align(center)[
        #text(size: 10pt, weight: "bold")[CUỘC THI SÁNG TẠO DÀNH CHO THANH THIẾU NIÊN, NHI ĐỒNG TOÀN QUỐC]\
        #text(size: 9pt)[LẦN THỨ 22 NĂM 2026]
        #v(-4pt)
        #line(length: 100%, stroke: 0.5pt)
      ]
    }
  },
  footer: context {
    if counter(page).get().first() > 1 {
      align(right)[#text(size: 10pt)[#counter(page).display()]]
    }
  },
)

#set text(font: "Times New Roman", size: 13pt, lang: "vi")
#set par(justify: true, leading: 0.8em, first-line-indent: 1.27cm)
#set heading(numbering: none)

#show heading: it => block(below: 12pt, above: 18pt)[
  #set text(weight: "bold", font: "Times New Roman")
  #if it.level == 1 {
    text(size: 14pt)[#it.body]
  } else if it.level == 2 {
    text(size: 13pt)[#it.body]
  } else {
    text(size: 13pt, style: "italic")[#it.body]
  }
]

#let title(body) = align(center)[#text(size: 16pt, weight: "bold")[#body]]
#let fig-caption(body) = align(center)[#v(4pt)#text(weight: "bold", style: "italic", size: 11pt)[#body]]

#show figure.where(kind: image): set figure(supplement: [Hình])
#show figure.where(kind: table): set figure(supplement: [Bảng])
#show figure.caption: it => [
  #v(4pt)
  #text(weight: "bold", style: "italic", size: 11pt)[
    #it.supplement #context it.counter.display(it.numbering). #it.body
  ]
]

#include "HOC-SINH-DIEN-DU-LIEU-THUC-TE.typ"
#import "HOC-SINH-DIEN-DU-LIEU-THUC-TE.typ": *

// =================== TRANG BÌA ===================
#align(center)[
  #v(0.5cm)
  #text(size: 14pt, weight: "bold")[
    CUỘC THI SÁNG TẠO DÀNH CHO THANH THIẾU NIÊN, NHI ĐỒNG\
    TOÀN QUỐC LẦN THỨ 22 NĂM 2026
  ]
  #v(2.5cm)
  #text(size: 12pt, weight: "bold")[TÊN ĐỀ TÀI DỰ THI:]
  #v(0.5cm)
  #text(size: 16pt, weight: "bold")[
    “THIẾT BỊ ĐEO THÔNG MINH HỖ TRỢ\
    NGƯỜI KHIẾM THỊ PHÂN LOẠI RÁC THẢI\
    TẠI NGUỒN TRÊN NỀN TẢNG TRÍ TUỆ NHÂN TẠO\
    (AI-GREEN EYE)”
  ]
  #v(2.5cm)
]

#align(left)[
  #set par(first-line-indent: 0pt)
  #text(weight: "bold")[LĨNH VỰC DỰ THI: ] Sản phẩm thân thiện với môi trường\
  #text(size: 11pt, style: "italic")[(Đăng ký theo Lĩnh vực số 3 - Điều 5, Thể lệ Cuộc thi Toàn quốc Lần thứ 22)]
  #v(0.3cm)
  #text(weight: "bold")[TÁC GIẢ:]
  #list(
    marker: ([o],),
    [#text(weight: "bold")[Nguyễn Hoàng Thiên Nga] – Lớp 8/4, Trường THCS Phan Văn Trị, Gò Vấp, TP. Hồ Chí Minh.],
    [#text(weight: "bold")[Trần Trung Hiếu] – Lớp 8/4, Trường THCS Phan Văn Trị, Gò Vấp, TP. Hồ Chí Minh.],
  )
  #v(0.2cm)
  #text(weight: "bold")[GIÁO VIÊN HƯỚNG DẪN: ] Võ Thị Thùy, Phan Anh\
  #text(weight: "bold")[ĐƠN VỊ ĐĂNG KÝ: ] Trường THCS Phan Văn Trị, Thành phố Hồ Chí Minh.
]
#pagebreak()

// =================== TÓM TẮT ĐỀ TÀI ===================
#title[TÓM TẮT ĐỀ TÀI: “AI-GREEN EYE”]
#v(0.5cm)

#text(weight: "bold")[Tính mới của đề tài:] AI-Green Eye kết hợp camera gắn trên vòng đeo đầu, thao tác bằng một nút bấm, chương trình phân loại chạy trực tiếp trên thiết bị và phản hồi bằng giọng nói tiếng Việt. Chúng em đã sử dụng #(bo-xu-ly-thuc-te), #(camera-thuc-te) và #(dau-ra-am-thanh-thuc-te). Với giải pháp này, người khiếm thị chỉ cần bấm nút để thiết bị chụp ảnh, thực hiện nhận diện và phát âm thanh hướng dẫn mà không cần kết nối mạng.

#text(weight: "bold")[Tính khoa học:] Đề tài sử dụng thị giác máy tính và mô hình nhận diện TensorFlow Lite gọn nhẹ. Mô hình của chúng em có kích thước #(kich-thuoc-model) và phân biệt ba nhóm rác: hữu cơ, vô cơ và rác khác. Dữ liệu được chia thành tập huấn luyện, tập xác thực và tập kiểm tra độc lập. Các kết quả trong báo cáo chỉ được điền sau khi nhóm kiểm tra bằng ảnh chụp mới từ thiết bị và lưu lại đầy đủ nhật ký đo đạc.

#text(weight: "bold")[Tính thực tiễn:] Mẫu thử sử dụng #(bo-xu-ly-thuc-te), #(camera-thuc-te) và #(dau-ra-am-thanh-thuc-te). Tổng chi phí thực tế là #(tong-chi-phi-thuc-te). Khối lượng phần vòng đeo trên đầu là #(khoi-luong-tren-kinh). Bộ thùng rác thử nghiệm có thêm chữ nổi Braille để hỗ trợ nhận biết bằng xúc giác.

#text(weight: "bold")[Tính cộng đồng:] AI-Green Eye mong muốn giúp người khiếm thị tự tay phân loại rác tại nguồn một cách dễ dàng và chủ động hơn. Theo thống kê #(nguon-so-lieu-nguoi-khiem-thi) #footnote[https://thanhnien.vn/gan-2-trieu-nguoi-viet-khiem-thi-suy-giam-thi-luc-chua-den-1-sach-chu-noi-185251114131539441.htm], hiện có khoảng #(so-nguoi-khiem-thi) người khiếm thị có thể được hưởng lợi từ giải pháp này.

#v(0.5cm)
#set par(first-line-indent: 0pt)
#grid(
  columns: (auto, 1fr),
  gutter: 10pt,
  [*LĨNH VỰC:*], [Sản phẩm thân thiện với môi trường],
  [*TÁC GIẢ:*], [Nguyễn Hoàng Thiên Nga, Trần Trung Hiếu],
  [*GIÁO VIÊN HƯỚNG DẪN:*], [Võ Thị Thùy, Phan Anh],
  [*THỜI GIAN THỰC HIỆN:*], [Tháng 12/2025 đến tháng 08/2026],
  [*ĐƠN VỊ THÀNH PHỐ NỘP:*], [Ban Tổ chức Cuộc thi Sáng tạo Thanh thiếu niên, Nhi đồng Thành phố Hồ Chí Minh],
)

#pagebreak()

// =================== LỜI CẢM ƠN ===================
#title[LỜI CẢM ƠN]
#v(0.5cm)

Chúng em xin bày tỏ lòng biết ơn sâu sắc đến Ban Giám hiệu cùng tập thể thầy cô giáo Trường THCS Phan Văn Trị đã luôn tạo điều kiện, động viên và giúp đỡ chúng em trong suốt quá trình nghiên cứu, thực hiện đề tài.

Đặc biệt, chúng em xin chân thành cảm ơn cô Võ Thị Thùy và thầy Phan Anh. Thầy cô đã dành nhiều thời gian, tâm huyết để định hướng ý tưởng, hướng dẫn chúng em giải quyết những vấn đề kỹ thuật về mô hình nhận diện, thiết kế phần cứng và hoàn thiện hồ sơ báo cáo.

Xin chân thành cảm ơn thầy Dương Huỳnh Thanh Phú và các cô, chú, anh, chị tại khu nhà ở dành cho người khiếm thị, số 446 Lý Thái Tổ, phường Vườn Lài, TP Hồ Chí Minh đã tạo điều kiện cho chúng em được tiếp xúc và có nhiều thông tin về nhu cầu thực tế của người khiếm thị. Đồng thời hoàn thành các khảo sát trong quá trình thực hiện đề tài này.

Chúng em cũng xin gửi lời cảm ơn đến Ban Tổ chức Cuộc thi Sáng tạo Thanh thiếu niên, Nhi đồng Thành phố Hồ Chí Minh đã ghi nhận đề tài ở cấp cơ sở và tạo cơ hội để chúng em đại diện Thành phố tham dự Cuộc thi toàn quốc. Cuối cùng, chúng em xin cảm ơn gia đình, bạn bè đã luôn động viên và đóng góp những ý kiến quý báu để chúng em tiếp tục hoàn thiện sản phẩm.

Chúng em xin chân thành cảm ơn!

#pagebreak()

// =================== MỤC LỤC ===================
#title[MỤC LỤC]
#v(0.5cm)
#outline(title: none, indent: 1.5em)
#pagebreak()

// =================== DANH SÁCH HÌNH ẢNH & BẢNG ===================
#title[DANH SÁCH HÌNH ẢNH]
#v(0.5cm)
#outline(title: none, target: figure.where(kind: image))

#v(1cm)
#title[DANH SÁCH BẢNG]
#v(0.5cm)
#outline(title: none, target: figure.where(kind: table))
#pagebreak()

// =================== NỘI DUNG CHÍNH ===================

= A. LÝ DO CHỌN ĐỀ TÀI

Chúng em nhận thấy phân loại rác tại nguồn có ý nghĩa thiết thực đối với việc bảo vệ môi trường, nhưng vẫn là một trở ngại đối với người khiếm thị. Do không thể nhận biết màu sắc của thùng rác hoặc đọc nhãn bằng thị giác, họ gặp khó khăn khi xác định nơi bỏ từng loại rác. Từ khảo sát thực tế, chúng em ghi nhận  người khiếm thị, người bị suy giảm thị lực gặp nhiều khó khăn trong việc phân loại rác.

Từ thực tế đó, chúng em đặt ra câu hỏi: _Làm thế nào để hỗ trợ người khiếm thị tự phân loại rác thuận tiện hơn mà vẫn hạn chế vướng víu khi thao tác?_

Từ câu hỏi trên, chúng em đề xuất thiết bị thông minh mang tên *AI-Green Eye*. Thiết bị được thiết kế dưới dạng vòng đeo trên đầu tích hợp camera góc nhìn trước trán và một nút bấm kích hoạt. Khi người dùng bấm nút, thiết bị chụp ảnh, dùng mô hình nhận diện để xác định nhóm rác và phát lời hướng dẫn về thùng rác tương ứng.

= B. CÂU HỎI NGHIÊN CỨU – VẤN ĐỀ NGHIÊN CỨU – MỤC TIÊU VÀ YÊU CẦU

== B1. Câu hỏi nghiên cứu
1. Chúng em có thể xây dựng một mô hình nhận diện rác đủ gọn nhẹ để chạy trên Raspberry Pi Zero 2 W mà không rò rỉ dữ liệu người dùng không?
2. Khung vòng đeo trên đầu cần được thiết kế như thế nào để có khối lượng phù hợp, ôm vừa vặn và phân bổ đều quanh vòm đầu, dễ thao tác và hạn chế cản trở việc nghe âm thanh xung quanh của người khiếm thị?
3. Thiết bị cần phát lời hướng dẫn ở mức âm lượng như thế nào để người dùng nghe rõ mà vẫn nhận biết được âm thanh xung quanh?

== B2. Vấn đề nghiên cứu
Chúng em nghiên cứu một thiết bị đeo ứng dụng trí tuệ nhân tạo nhằm hỗ trợ người khiếm thị phân loại rác sinh hoạt. Trọng tâm của đề tài là xây dựng mô hình nhận diện gọn nhẹ bằng TensorFlow Lite, thiết kế khung vòng đeo trên đầu bằng nhựa in 3D và làm nhãn chữ nổi Braille cho thùng rác để người dùng nhận biết bằng xúc giác.

== B3. Mục tiêu nghiên cứu
- Lắp ráp mẫu thử dạng vòng đeo trên đầu có khả năng chụp ảnh và nhận diện rác.
- Huấn luyện mô hình nhận diện để phân biệt ba nhóm: rác hữu cơ, rác vô cơ (tái chế) và rác khác; sau đó đo độ chính xác trên tập kiểm tra độc lập để đánh giá khả năng nhận diện với dữ liệu chưa dùng trong huấn luyện.
- Viết chương trình Python kết nối nút bấm, camera, mô hình nhận diện và loa; đồng thời đo độ trễ của thiết bị.
- Gắn chữ nổi Braille lên các thùng rác thử nghiệm và ghi nhận trải nghiệm thực tế của người dùng để đánh giá mức độ hỗ trợ của sản phẩm.

== B4. Yêu cầu đề tài
1. *Dễ sử dụng:* Chỉ có duy nhất một nút bấm để người dùng không bị bối rối.
2. *Thoải mái:* Thiết bị dạng vòng đeo trên đầu cần có khối lượng nhẹ, phân bố trọng tâm cân đối, dây điện gọn gàng để người dùng đội thoải mái khi sử dụng.
3. *An toàn và tôn trọng quyền riêng tư:* Camera được thiết kế để chỉ chụp ảnh khi người dùng bấm nút; việc xóa ảnh tạm sau khi xử lý phải được kiểm tra. Cách phát âm thanh cần hạn chế cản trở việc nghe bằng cả hai tai.
4. *Chi phí hợp lí:* Chi phí không quá cao để đa số người dùng có thể tiếp cận.

#pagebreak()

= CHƯƠNG 1. KẾ HOẠCH VÀ PHƯƠNG PHÁP NGHIÊN CỨU

== 1.1. Kế hoạch nghiên cứu
Đề tài được thực hiện từ tháng 12/2025 đến tháng 08/2026 với bảng phân công và tiến độ cụ thể như sau:

#figure(
  table(
    columns: (1.5cm, 4.5cm, 5cm, 2.5cm, 3.5cm),
    align: (center + horizon, left + horizon, left + horizon, center + horizon, left + horizon),
    table.header([*TT*], [*Nội dung công việc*], [*Các bước thực hiện*], [*Thời gian*], [*Người phụ trách*]),
    [1],
    [Khảo sát thực trạng và xác định vấn đề],
    [Tìm hiểu khó khăn của người mù, khảo sát các sản phẩm hỗ trợ hiện có trên thị trường.],
    [12/2025 - 01/2026],
    [Cả nhóm],

    [2],
    [Lập thiết kế kỹ thuật],
    [Vẽ sơ đồ hệ thống, chọn mua linh kiện, tính toán chi phí.],
    [02/2026 - 03/2026],
    [Trần Trung Hiếu],

    [3],
    [Xây dựng mô hình nhận diện],
    [Chụp ảnh rác thực tế, gắn nhãn và huấn luyện mô hình nhận diện.],
    [04/2026 - 05/2026],
    [Nguyễn Hoàng Thiên Nga],

    [4],
    [Lắp ráp và viết chương trình],
    [Lắp camera, mạch Raspberry Pi, in 3D vỏ hộp, viết mã Python điều khiển.],
    [05/2026 - 06/2026],
    [Trần Trung Hiếu],

    [5],
    [Thử nghiệm và sửa lỗi],
    [Thử nghiệm độ chính xác của máy, ghi nhật ký, nhờ người dùng thử và đánh giá.],
    [07/2026],
    [Cả nhóm],

    [6], [Hoàn thiện hồ sơ], [Viết báo cáo, quay video giới thiệu sản phẩm và nộp hồ sơ.], [08/2026], [Cả nhóm],
  ),
  caption: [Phân công và kế hoạch thực hiện chi tiết.],
  numbering: _ => "1.1",
)

== 1.2. Phương pháp nghiên cứu
Để thực hiện đề tài, chúng em sử dụng các phương pháp sau:
1. *Tìm hiểu lý thuyết:* Đọc sách về học máy, học sâu, huấn luyện mô hình phân loại ảnh và triển khai mô hình gọn nhẹ trên thiết bị nhúng @geron2022hands @chollet2021deep @warden2019tinyml.
2. *Thực hành chế tạo:* Chia công việc thành từng phần, tìm hiểu cách lập trình và kết nối phần cứng trên Raspberry Pi @monk2023raspberry, tra cứu thông số Raspberry Pi Zero 2 W @raspberrypi2026zero2w và tài liệu hệ điều hành DietPi @dietpi2026docs.
3. *Thử nghiệm và đo đạc:* Ghi nhật ký kết quả nhận diện đúng, sai và thời gian xử lý trong các điều kiện ánh sáng khác nhau để xác định những điểm cần cải thiện.
4. *Khảo sát người dùng:* Mời người dùng trải nghiệm mẫu thử và ghi chép ý kiến của họ về mức độ thuận tiện cũng như những điểm còn gây khó chịu khi sử dụng.

#pagebreak()

= CHƯƠNG 2. PHÂN TÍCH THỰC TRẠNG VÀ CƠ SỞ GIẢI PHÁP

== 2.1. Khó khăn của người khiếm thị trong phân loại rác
Qua khảo sát #footnote[#(bang-chung-khao-sat-nhu-cau)], chúng em nhận thấy người khiếm thị gặp ba trở ngại chính:
- *Khó nhận biết chất liệu của rác:* Khi chỉ nhận biết bằng xúc giác, người khiếm thị khó phân biệt một số vật thể có hình dạng gần giống nhau, chẳng hạn hộp giấy và hộp nhựa mềm.
- *Nguy cơ bị thương:* Việc chạm trực tiếp vào rác có thể khiến người dùng gặp mảnh chai, cạnh lon sắc hoặc chất bẩn.
- *Khó xác định thùng rác phù hợp:* Ngay cả khi nhận biết được vật đang cầm là giấy, người dùng vẫn có thể khó chọn đúng thùng nếu các thùng chỉ được phân biệt bằng màu sắc hoặc nhãn in.

#figure(
  image("image/khao sat.jpg", height: 13cm),
  caption: [Khảo sát thực tế về khó khăn của người khiếm thị trong phân loại rác.],
  numbering: _ => "2.1",
)

== 2.2. Chọn cách giải quyết
Từ những khó khăn trên, chúng em đề xuất ba phương án hỗ trợ phân loại rác và lập bảng so sánh:

#figure(
  table(
    columns: (3cm, 4.5cm, 4.5cm, 2.5cm),
    align: (left + horizon, left + horizon, left + horizon, center + horizon),
    table.header([*Phương án*], [*Ưu điểm*], [*Hạn chế*], [*Đánh giá*]),
    [1. Làm ứng dụng trên điện thoại],
    [Tận dụng camera và loa có sẵn của điện thoại, không cần mua thêm các linh kiện này.],
    [Người khiếm thị phải vừa cầm rác, vừa cầm điện thoại và thao tác trên màn hình nên chưa thuận tiện.],
    [Chưa phù hợp],

    [2. Đặt thiết bị cố định ở thùng rác],
    [Có thể sử dụng bộ xử lý có tài nguyên cao hơn và nguồn điện cố định.],
    [Người dùng phải di chuyển đến đúng vị trí đặt thiết bị và không thể mang theo khi cần.],
    [Kém linh hoạt],

    [3. Thiết bị đeo thông minh (AI-Green Eye)],
    [Thiết bị dạng vòng đeo trên đầu giúp người dùng hoàn toàn rảnh tay; camera hướng theo tầm nhìn phía trước và ảnh được xử lý trực tiếp trên thiết bị.],
    [Bộ xử lý nhỏ có tài nguyên hạn chế nên chương trình cần được điều chỉnh phù hợp.],
    [*Phù hợp nhất (Lựa chọn)*],
  ),
  caption: [Phân tích so sánh các phương án kỹ thuật hỗ trợ phân loại rác.],
  numbering: _ => "2.1",
)

== 2.3. Quyết định của nhóm
Từ kết quả so sánh, chúng em chọn *Phương án 3*: chế tạo thiết bị đeo thông minh sử dụng Raspberry Pi Zero 2 W với thiết kế dạng vòng đeo trên đầu. Giải pháp này giúp người dùng rảnh tay để cầm rác; thao tác chính là hướng camera trước trán về phía vật thể và bấm nút kích hoạt trên thân vòng đeo.

= CHƯƠNG 3. PHÂN TÍCH CÁC YẾU TỐ ẢNH HƯỞNG

== 3.1. Các vấn đề kỹ thuật
- *Ánh sáng thay đổi:* Khi đưa vật thể ra ngoài trời nắng hoặc vào nơi thiếu sáng, hình ảnh camera thu được thay đổi đáng kể nên mô hình nhận diện có thể cho kết quả sai.
- *Rác bị biến dạng:* Lon nước bị móp hoặc tờ giấy bị vò có hình dạng khác so với trạng thái nguyên vẹn. Vì vậy, chúng em cần bổ sung ảnh của các vật thể biến dạng vào dữ liệu huấn luyện.
- *Giới hạn của máy móc:* Bộ xử lý của chúng em là #(bo-xu-ly-thuc-te), có tài nguyên hạn chế. Vì vậy, nhóm dùng định dạng TensorFlow Lite/LiteRT để giảm kích thước mô hình và triển khai suy luận trên thiết bị @warden2019tinyml @google2026litert.

== 3.2. Yếu tố con người và an toàn
- *Khối lượng thiết bị:* Khung vòng đeo trên đầu cần có khối lượng nhẹ và phân bố đều quanh vòng đầu, có đệm êm để không gây nặng đầu hay khó chịu khi đeo lâu. Vì vậy, chúng em cân riêng phần vòng đeo và đánh giá mức độ thoải mái qua thử nghiệm đeo thực tế.
- *Khả năng nghe âm thanh xung quanh:* Thính giác có vai trò quan trọng trong việc định hướng của người khiếm thị. Vì vậy, chúng em chọn loa ngoài có kích thước nhỏ và sẽ kiểm tra để hạn chế cản trở việc nghe âm thanh xung quanh.
- *Tôn trọng quyền riêng tư:* Camera được thiết kế để chụp một ảnh khi người dùng bấm nút, thay vì chụp liên tục. Nhóm đặt yêu cầu chương trình xóa ảnh tạm sau khi xử lý và phải kiểm tra lại yêu cầu này trước khi mời người dùng thử nghiệm.

== 3.3. Tiêu chí đánh giá sản phẩm
Để biết sản phẩm có thành công hay không, chúng em tự đặt ra các tiêu chí kiểm tra nghiêm ngặt:

#align(center)[
  #table(
    columns: (3.5cm, 6.5cm, 4cm),
    align: (left + horizon, left + horizon, left + horizon),
    table.header([*Yêu cầu cốt lõi*], [*Mô tả chi tiết*], [*Cách chúng em kiểm tra*]),
    [1. Nhận diện chính xác],
    [Thiết bị cần nhận diện đúng nhóm rác trong điều kiện thử nghiệm.],
    [Dùng tập kiểm tra độc lập để thống kê số lần thiết bị thông báo đúng.],

    [2. Phản hồi nhanh],
    [Tính từ lúc bấm nút đến lúc loa phát ra âm thanh.],
    [Đo thời gian nhiều lần rồi tính trung bình.],

    [3. Trọng lượng nhẹ], [Đo phần vòng đeo trên đầu và hộp xử lý/nguồn pin.], [Dùng cân điện tử loại nhỏ để cân.],
    [4. Hạn chế cản trở thính giác],
    [Cách phát âm thanh cần hạn chế ảnh hưởng đến việc nghe âm thanh xung quanh.],
    [Dùng loa ngoài và ghi nhận khả năng nghe âm thanh xung quanh khi thử nghiệm.],

    [5. Tôn trọng quyền riêng tư],
    [Ảnh tạm cần được xóa sau khi xử lý.],
    [Kiểm tra chương trình và bộ nhớ sau mỗi lần nhận diện.],
  )
  #fig-caption[Bảng 3.1. Các yêu cầu kỹ thuật và tiêu chí đánh giá sản phẩm.]
]

= CHƯƠNG 4. GIẢI PHÁP VÀ MÔ HÌNH THỰC TẾ

== 4.1. Sơ đồ hoạt động
Khi sử dụng AI-Green Eye, thiết bị hoạt động theo quy trình: bấm nút -> chụp ảnh -> mô hình nhận diện -> phát lời hướng dẫn. Bộ xử lý của máy là #(bo-xu-ly-thuc-te), hình ảnh được thu bằng #(camera-thuc-te), còn âm thanh được phát theo cơ chế #(co-che-am-thanh-thuc-te).

#figure(
  block(
    stroke: 1pt + rgb("a0a0a0"),
    inset: 15pt,
    radius: 4pt,
    fill: rgb("f9f9f9"),
    [
      #grid(
        columns: (3cm, 1fr, 3.5cm, 1fr, 3.2cm),
        align: center + horizon,
        block(stroke: 1pt, inset: 5pt, fill: rgb("e1f5fe"))[*Đầu vào*\ (Camera +\ Nút bấm)],
        [#line(length: 100%, stroke: 0.8pt + blue) \ #text(size: 8pt)[Ảnh chụp (RGB)]],
        block(stroke: 1pt, inset: 5pt, fill: rgb("fff9c4"))[*Khối xử lý*\ (Mạch điện \ + trí tuệ nhân tạo)],
        [#line(length: 100%, stroke: 0.8pt + blue) \ #text(size: 8pt)[Kết quả loại rác]],
        block(stroke: 1pt, inset: 5pt, fill: rgb("e8f5e9"))[*Đầu ra*\ (Giọng nói \ hướng dẫn)],
      )
    ],
  ),
  caption: [Sơ đồ khối kiến trúc hệ thống AI-Green Eye.],
  kind: image,
  numbering: _ => "4.1",
)

== 4.2. Cấu tạo phần cứng
Để chế tạo mẫu thử dự thi, chúng em sử dụng các linh kiện sau:

#figure(
  table(
    columns: (4cm, 9cm,auto),
    align: (left + horizon, left + horizon, center + horizon),
    table.header([*Hạng mục*], [*Chi tiết linh kiện*], [*Hình ảnh*]),
    [Bộ xử lý trung tâm], [#(bo-xu-ly-thuc-te)],[#image("image/thiet bi/pi.png")],
    [Camera chụp ảnh], [#(camera-thuc-te)],[#image("image/thiet bi/cam.png",height: 2cm)],
    [Mạch và loa phát tiếng], [#(dau-ra-am-thanh-thuc-te)],[#image("image/thiet bi/max.png", height: 3cm)],
    [Pin cấp điện], [#(dung-luong-pin)],[],
    [Khối lượng đo được],
    [Phần vòng đeo trên đầu:  #(khoi-luong-toan-bo)],[#image("image/san pham hoan thien.jpg")],

    [Kích thước hộp], [#(kich-thuoc-san-pham)],
    // [Danh mục linh kiện và chi phí], [#(danh-sach-linh-kien-va-gia)],
  ),
  caption: [Danh mục và thông số chi tiết của các linh kiện.],
  numbering: _ => "4.1",
)

#figure(
  image("image/san pham 2.jpg", width: 60%),
  caption: [Bố trí phần cứng trên mẫu thử dùng để lập trình.],
  numbering: _ => "4.2",
)

#figure(
  image("image/san pham hoan thien.jpg"),
  caption: [Mẫu thử hoàn chỉnh với vỏ in 3D.],
  numbering: _ => "4.3",
)

== 4.3. Hoạt động của chương trình
Sau khi người dùng bấm nút, chương trình Python điều khiển các bước còn lại của thiết bị theo quy trình sau:
1. Mạch điện luôn trong trạng thái chờ.
2. Khi người dùng bấm nút trên vòng đeo đầu, camera chụp một ảnh và sau đó  thay đổi kích thước ảnh thành 224 × 224 để phù hợp với đầu vào của mô hình.
3. Hình ảnh được đưa vào mô hình nhận diện TensorFlow Lite để phân loại; quy trình tiền xử lý và phân loại ảnh được tham khảo từ tài liệu TensorFlow @tensorflow2026classification.
4. Chương trình đối chiếu kết quả với ngưỡng tin cậy 80% do chúng em đặt. Nếu điểm số dưới 80%, thiết bị nhắc người dùng chụp lại ảnh.
5. Nếu điểm số đạt từ 80% trở lên, thiết bị phát tên nhóm rác và hướng dẫn thùng rác tương ứng.
6. Cuối cùng, chương trình được yêu cầu xóa ảnh tạm trong cả trường hợp nhận diện thành công và trường hợp xảy ra lỗi. Nhóm sẽ kiểm tra bộ nhớ sau mỗi lần chạy để xác nhận yêu cầu này được thực hiện.

=== 4.3.1. Quá trình hoàn thiện chương trình
Trong quá trình hoàn thiện sản phẩm, chúng em đã nhiều lần điều chỉnh chương trình và thử các cách nhận diện khác nhau. Ban đầu, nhóm dự định phân biệt nhiều vật thể riêng lẻ, nhưng phương án này làm dữ liệu và âm thanh hướng dẫn trở nên phức tạp. Vì vậy, nhóm chuyển sang ba nhóm rác hữu cơ, vô cơ và rác khác để phù hợp với bộ thùng rác thử nghiệm. Nhóm sử dụng EfficientNet-B0, thuộc họ mô hình EfficientNet được đề xuất bởi Mingxing Tan và Quoc V. Le @tan2019efficientnet. Chúng em cũng điều chỉnh nút bấm, thử các ngưỡng tin cậy khác nhau và chuẩn bị lời hướng dẫn bằng tiếng Việt. Cấu hình hiện tại được chọn vì phù hợp hơn với khả năng xử lý của Raspberry Pi Zero 2 W; kết quả của cấu hình này được trình bày qua các phép thử ở Chương 5.

=== 4.3.2. Âm thanh hướng dẫn tương ứng
Dựa trên kết quả của mô hình nhận diện, chương trình chọn phát một trong các âm thanh sau:

#figure(
  table(
    columns: (3.3cm, 3.6cm, 3cm, 7cm),
    align: (center + horizon, left + horizon, left + horizon, left + horizon),
    table.header([*Nhãn dự đoán*], [*Chất liệu*], [*Phân loại*], [*Âm thanh sẽ phát ra*]),
    [`organic`], [Rác hữu cơ], [Nhóm hữu cơ], [Tiếng báo hiệu: "Đây là Rác hữu cơ"],
    [`inorganic`], [Rác vô cơ], [Nhóm vô cơ], [Tiếng báo hiệu: "Đây là Rác vô cơ"],
    // [`warning`], [Không xác định nhưng sắc nhọn], [Vật sắc nhọn], [Tiếng báo hiệu: "Cảnh báo vật sắc nhọn"],
    [`other`], [Rác bẩn/không rõ], [Nhóm khác], [Tiếng báo hiệu: "Rác khác loại"],
    [Dưới 0,80], [Không kết luận], [Bỏ qua], [Tiếng nhắc nhở: "Ảnh chưa rõ, vui lòng chụp lại"],
  ),
  caption: [Ánh xạ kết quả nhận diện với âm thanh hướng dẫn.],
  numbering: _ => "4.2",
)

== 4.4. Thiết kế và chế tạo khung vòng đeo đầu in 3D
Chúng em dùng phần mềm thiết kế 3D để tạo khung vòng đeo ôm quanh đầu người dùng. Khung vòng đeo tích hợp sẵn hốc gắn module camera ở vị trí chính giữa trán giúp góc chụp thẳng tự nhiên, vị trí gắn mạch khuếch đại âm thanh, khe gắn Raspberry Pi Zero 2 W và loa bên hông, cùng với các khớp điều chỉnh kích thước quai gài phía sau và đệm mút hai bên. Phần vòng đeo trên đầu có khối lượng #(khoi-luong-tren-kinh). Thiết kế này giúp trọng lượng được phân bố đều quanh vòng đầu, không gây tì đè lên sống mũi như dạng kính mắt thông thường.

#figure(
  image("image/1786641666242_1634650884594342833_6156200798043510897_c426a8e2c12386b73e6d155337abb62c.jpg", width: 85%),
  caption: [Bản vẽ thiết kế 3D và kích thước vỏ thiết bị.],
  numbering: _ => "4.4",
)

== 4.5. Làm nhãn chữ nổi Braille cho thùng rác
Sau khi nghe hướng dẫn, người khiếm thị vẫn cần xác định thùng tương ứng bằng xúc giác. Vì vậy, chúng em làm nhãn chữ nổi Braille và dán lên ba thùng rác thử nghiệm.

#figure(
  image("image/thung_rac.png"),
  caption: [Nhãn chữ nổi Braille trên ba thùng rác thử nghiệm.],
  numbering: _ => "4.5",
)

// == 4.6. Lắp ráp sản phẩm 


#pagebreak()

= CHƯƠNG 5. THỰC NGHIỆM VÀ ĐÁNH GIÁ HIỆU QUẢ

== 5.1. Dữ liệu huấn luyện mô hình nhận diện
// Để mô hình nhận biết rác, chúng em chụp tổng cộng #(so-anh-goc) của #(so-vat-the-doc-lap) vật thể khác nhau và tải thêm các ảnh của các vật thể đó từ internet, mỗi vật thể có số lượng ảnh trong dataset trong khoảng 900 đến 1100 tấm (tùy từng vật thể) sau khi làm sạch bằng cách loại bỏ ảnh lỗi, ảnh quá mờ hoặc trùng lặp, tổng cộng được 11,056 tấm; sau đó chia thành tập huấn luyện, tập xác thực và tập kiểm tra độc lập (tỉ lệ tương ứng 80% train/10% test/10% val).
// Tập kiểm tra độc lập phải gồm những ảnh chưa dùng để huấn luyện, trong đó có ảnh chụp bằng chính camera của thiết bị. Sau đó gom toàn bộ ảnh của các vật thuộc nhóm vô cơ, hữu cơ, rác khác thư mục tương ứng.
//
Quy trình xây dựng bộ dữ liệu được chúng em thực hiện theo các bước:

+ *Thu thập ảnh:* Nhóm chụp tổng cộng #(so-anh-goc) ảnh của #(so-vat-the-doc-lap) vật thể độc lập và bổ sung thêm ảnh của các vật thể tương ứng từ Internet.
+ *Sắp xếp theo từng vật thể:* Mỗi vật thể được lưu trong một thư mục riêng, sau đó loại bỏ các ảnh lỗi, ảnh quá mờ hoặc ảnh trùng lặp. Sau bước làm sạch ảnh tải về từ internet, toàn bộ dữ liệu gồm 11.056 ảnh.
+ *Gom theo nhóm rác:* Dựa trên loại của từng vật thể, nhóm thực hiện phân loại thủ công các thư mục vật thể vào ba nhóm rác hữu cơ, rác vô cơ và rác khác.
+ *Chia dữ liệu:* Trong thư mục của từng vật thể, nhóm chia ảnh thành ba tập:
  - 80% dùng để huấn luyện (train);
  - 10% dùng để kiểm tra (test);
  - 10% dùng để xác thực (validation).
+ *Tạo bộ dữ liệu hoàn chỉnh:* Trong mỗi nhóm rác tiếp tục có ba thư mục train, test và validation. Ảnh từ các vật thể tương ứng được sao chép vào đúng thư mục theo phần dữ liệu đã chia ở bước trước sao cho không có ảnh nào xuất hiện cùng lúc ở cả 3 thư mục train, test, validation để đảm bảo tính độc lập của các tập dữ liệu.

Kết quả cuối cùng là bộ dữ liệu gồm 3 lớp: hữu cơ, vô cơ và rác khác, mỗi lớp đều có đầy đủ tập train, test và validation.

Mô hình được huấn luyện trong #(so-epoch) vòng lặp và có kích thước #(kich-thuoc-model). Khi sử dụng EfficientNet-B0 224, Mô hình được huấn luyện trong 17 epoch. Trong quá trình huấn luyện, độ chính xác trên tập huấn luyện tăng từ khoảng 56% lên khoảng 91%, trong khi độ chính xác trên tập xác thực đạt khoảng 79–81% ở các epoch cuối. Loss trên tập huấn luyện giảm còn khoảng 0,26, trong khi validation loss khoảng 0,59.

#figure(
  image("image/training_history.png"),
  caption: [Biểu đồ độ chính xác và sai số từ lần huấn luyện mô hình.],
  numbering: _ => "5.1",
)

== 5.2. Kết quả nhận diện theo nhóm rác của mô hình đã huấn luyện và chuyển đổi sang tflite
Tiếp theo, nhóm chúng em dùng những vật thể không xuất hiện trong tập huấn luyện (không thuộc 97 vật thể trong dataset) để đánh giá khả năng nhận diện của thiết bị. Kết quả từng lần được ghi vào phiếu thử nghiệm rồi chúng em tổng hợp trong bảng sau:

// #image("image/confusion_matrix.png")

#align(center)[
  #table(
    columns: (4cm, 4cm, 4cm),
    align: (left + horizon, center + horizon, center + horizon),
    table.header([*Nhóm vật thể rác*], [*Số lần chụp*], [*Số lần nói đúng*]),
    [Hữu cơ (`organic`)], [#(n-huu-co-test)], [#(dung-huu-co-test)],
    [Vô cơ (`inorganic`)], [#(n-vo-co-test)], [#(dung-vo-co-test)],
    [Khác (`other`)], [#(n-khac-test)], [#(dung-khac-test)],
    [*Tổng cộng*], [#(tong-mau-test)], [#(tong-dung-test)],
  )
  #fig-caption[Bảng 5.1. Kết quả thử nghiệm nhận diện theo nhóm rác.]
]

Tỉ lệ nhận diện chính xác trong thực tế là $display(#tong-dung-test/#tong-mau-test).100% approx 88,08%$ thấp hơn $5,07%$ với độ chính xác của mô hình, nguyên nhân do điều kiện ánh sáng và vật thể nền gây nhiễu.

// #pagebreak()
== 5.3. Ma trận nhầm lẫn
Để phân tích cụ thể các trường hợp nhận diện sai, chúng em lập ma trận nhầm lẫn nhằm xác định mô hình thường nhầm giữa những nhóm rác nào:

#align(center)[
  #table(
    columns: (3.5cm, 2.5cm, 2.5cm, 2.5cm, 3.2cm),
    align: (left + horizon, center + horizon, center + horizon, center + horizon, center + horizon),
    table.header([*Nhóm thực tế / Kết quả nhận diện*], [*Hữu cơ*], [*Vô cơ*], [*Khác*], [*Tỉ lệ chính xác*]),
    [*Hữu cơ*], [#(cm-huu-co-huu-co-test)], [#(cm-huu-co-vo-co-test)], [#(cm-huu-co-khac-test)], [$approx 88,95%$],
    [*Vô cơ*], [#(cm-vo-co-huu-co-test)], [#(cm-vo-co-vo-co-test)], [#(cm-vo-co-khac-test)], [$approx 93,84%$],
    [*Khác*], [#(cm-khac-huu-co-test)], [#(cm-khac-vo-co-test)], [#(cm-khac-khac-test)], [$approx 77,60%$],
  )
  #fig-caption[Bảng 5.2. Ma trận nhầm lẫn của mô hình nhận diện.]
]

*Phân tích các trường hợp nhận diện sai:* #(phan-tich-loi-thuc-te). Kết quả từ ma trận nhầm lẫn cho thấy nhóm "Khác" có tỉ lệ chính xác thấp nhất ($approx 77,60%$) và là lớp cần được cải thiện nhất (chủ yếu do bị nhầm sang rác vô cơ với 60 lần). Từ những lỗi quan sát được, nhóm sẽ bổ sung ảnh phù hợp với các góc chụp và điều kiện mà mô hình còn nhận diện chưa tốt để nâng cao hiệu quả phân loại.

== 5.4. Thử nghiệm độ trễ và điều kiện ánh sáng
Chúng em đo thời gian từ lúc bấm nút đến khi loa bắt đầu phát lời hướng dẫn. Sau #(so-lan-do-do-tre) lần đo, độ trễ trung bình là #(do-tre-trung-binh) giây và lớn nhất là #(do-tre-lon-nhat) giây. Vì sử dụng điện thoại làm đồng hồ bấm giây và thao tác bằng tay nên kết quả đo chưa có độ chính xác cao, tuy nhiên chúng em khá hài lòng với kết quả này.

Bên cạnh độ trễ, chúng em thử nghiệm khả năng nhận diện tại sân trường, trong lớp và vào buổi tối:

#align(center)[
  #table(
    columns: (3.5cm, 2.2cm, 2.2cm, 2.2cm, 3.2cm),
    align: (left + horizon, center + horizon, center + horizon, center + horizon, center + horizon),
    table.header([*Môi trường*], [*Số lượt*], [*Đúng*], [*Sai*], [*Tỉ lệ chính xác*]),
    [Ngoài trời sáng], [#(n-ngoai-troi)], [#(dung-ngoai-troi)], [#(sai-ngoai-troi)], [#(ket-qua-ngoai-troi)],
    [Trong nhà vừa phải], [#(n-trong-nha)], [#(dung-trong-nha)], [#(sai-trong-nha)], [#(ket-qua-trong-nha)],
    [Tối thiếu sáng], [#(n-toi)], [#(dung-toi)], [#(sai-toi)], [#(ket-qua-anh-sang-yeu)],
    // [*Tổng cộng*], [#(tong-mau-test)], [#(tong-dung-test)], [143], [$approx 88,08%$],
  )
  #fig-caption[Bảng 5.3. Kết quả thử nghiệm dưới các điều kiện ánh sáng khác nhau.]
]

// *Cách cải thiện trong điều kiện thiếu sáng:* #(giai-phap-anh-sang-da-thu).

== 5.5. Thử nghiệm tính khả dụng của mô hình
Sau các phép thử kỹ thuật, nhóm mời người dùng trải nghiệm mẫu thử để ghi nhận mức độ thuận tiện và những điểm còn bất tiện:
- *Người giúp thử nghiệm:* #(doi-tuong-thu-nghiem).
- *Cách thức:* #(quy-trinh-thu-nghiem-nguoi-dung).
- *Khi tự nhận biết rác bằng xúc giác:* #(ket-qua-khong-thiet-bi).
- *Khi sử dụng mẫu thử AI-Green Eye:* #(ket-qua-co-thiet-bi).
- *Điểm còn thiếu sót:* #(han-che-thu-nghiem-nguoi-dung).

// #align(center)[
//   #(anh-thu-nghiem)
//   #fig-caption[Hình 5.2. Thử nghiệm khả dụng thực tế.]
// ]

// == 5.6. Nguyên tắc ghi nhận kết quả
// Ghi nhận trung thực số liệu đo được, với số lần đo tối thiểu 30 lần để có kết quả chính xác.

= CHƯƠNG 6. KHẢ NĂNG ÁP DỤNG VÀ AN TOÀN

// == 6.1. Chi phí mua linh kiện
// Chúng em lựa chọn linh kiện phù hợp với ngân sách và tận dụng những thiết bị sẵn có. Chi phí từng hạng mục được trình bày như sau:

// #align(center)[
//   #table(
//     columns: (4cm, 9cm),
//     align: (left + horizon, left + horizon),
//     table.header([*Hạng mục*], [*Số tiền thực tế*]),
//     [Tên linh kiện, số lượng, đơn giá], [#(danh-sach-linh-kien-va-gia)],
//     [Tổng cộng], [#(tong-chi-phi-thuc-te)],
//   )
//   #fig-caption[Bảng 6.1. Bảng dự toán chi phí linh kiện.]
// ]

== Khả năng áp dụng và định hướng phát triển
- *Hiện tại:* Thiết bị được thiết kế để phân loại ba nhóm hữu cơ, vô cơ và rác khác trong bộ ba thùng rác thử nghiệm có vị trí quy ước. Hiện thiết bị chỉ tập trung hỗ trợ phân loại rác, chưa có tính năng chỉ đường cho người khiếm thị. Mô hình nhận diện một số vật sắc nhọn nhưng tỉ lệ chính xác chưa cao khi nén model từ keras sang tflite nên chúng em sẽ tiếp tục hoàn thiện.

#align(center)[
  #image("image/thuc_nghiem_1.jpg", width: 80%)
  #fig-caption[Hình 6.1. Thử nghiệm với keras mà nhóm đã thực hiện.]
]

- *Trong tương lai:* Chúng em mong muốn mở rộng khả năng nhận diện các loại rác cụ thể hơn, chẳng hạn lon nhôm, chai nhựa và giấy; nhận diện chuẩn các vật sắc nhọn nguy hiểm; đọc mệnh giá tiền; đọc một số nhãn thuốc thông dụng và hướng dẫn sử dụng của thuốc đó. Đồng thời tích hợp thêm chức năng chỉ đường cho người khiếm thị.

// #pagebreak()
== 6.3. Các biện pháp an toàn
- *Điện và nhiệt:* Pin và mạch điện được đặt trong hộp bảo vệ. Nhiệt độ cao nhất đo được là #(nhiet-do-cao-nhat), nhiệt độ cpu được đo bởi phần mềm htop (kết hợp lm-sensors).  Nhiệt độ CPU nằm ở giải nhiệt độ cho phép, không ảnh hưởng đến người dùng vì thiết bị được thiết kế cách nhiệt ở phần vỏ rất tốt. Thời lượng pin là #(thoi-luong-pin)  với pin #dung-luong-pin. Nhóm chỉ mời người dùng đeo thử sau khi kiểm tra pin, dây điện và nhiệt độ.
- *Âm thanh:* Chúng em sử dụng #(dau-ra-am-thanh-thuc-te) nhằm hạn chế việc che kín cả hai tai. Trước khi thử nghiệm, âm lượng được điều chỉnh phù hợp và người dùng được hỏi lại về khả năng nghe âm thanh xung quanh.
- *Quyền riêng tư:* Camera được thiết kế để chỉ chụp khi người dùng bấm nút; ảnh được xử lý tại thiết bị và không truyền lên mạng. Bản hoàn thiện đặt yêu cầu xóa ảnh tạm sau mỗi lần nhận diện; nhóm phải kiểm tra bộ nhớ để xác nhận yêu cầu này được thực hiện.

= CHƯƠNG 7. KẾT LUẬN VÀ KIẾN NGHỊ

== 7.1. Kết luận
Đề tài *"AI-Green Eye"* đã hình thành một mẫu thử dạng vòng đeo trên đầu, gồm nút bấm, camera, bộ xử lý, mô hình nhận diện ba nhóm rác và phần phát lời hướng dẫn bằng tiếng Việt. Những kết quả về độ chính xác, độ trễ, khối lượng, nhiệt độ, thời lượng pin và trải nghiệm người dùng chỉ được kết luận khi có phiếu đo và minh chứng tương ứng. Ở giai đoạn hiện tại, sản phẩm cho thấy các bộ phận có thể được kết hợp thành một hệ thống hỗ trợ phân loại rác; hiệu quả thực tế vẫn cần tiếp tục được kiểm chứng và cải thiện.

== 7.2. Định hướng tiếp theo
1. Thu thập thêm ảnh rác bị móp méo, nhiều góc chụp và nhiều điều kiện ánh sáng để mô hình nhận diện ổn định hơn, hoàn thiện khả năng nhận diện các vật sắc nhọn nguy hiểm.
2. Tiếp tục mở rộng tính năng nhận diện mệnh giá tiền, nhận diện và đọc nhãn thuốc thông dụng, hướng dẫn sử dụng của thuốc đó. Tận dụng bộ kit lập trình của MacOS để xây dựng server kết nối MacOS và Pi vì MacOS có nhiều thư viện mạnh mẽ hỗ trợ phát triển Text-To-Speech, Speech-To-Text, Vision, Apple Intelligent,... đủ để hoàn thiện nhiều tính năng nâng cao mà vẫn đảm bảo dữ liệu người dùng không truyền lên mạng internet công cộng.
3. Xin phép thử nghiệm với thêm người khiếm thị để ghi nhận góp ý về nút bấm, âm lượng, lời hướng dẫn và nhãn Braille và các chức năng của sản phẩm.

== 7.3. Mong muốn của nhóm
- Chúng em kính mong Ban Tổ chức Cuộc thi Sáng tạo Toàn quốc hỗ trợ giới thiệu đề tài đến các đơn vị, cơ sở hỗ trợ người khiếm thị và trường học chuyên biệt để nhóm có cơ hội trình diễn thiết bị, tiếp nhận góp ý từ cộng đồng.
- Chúng em kiến nghị các cơ quan, đơn vị xem xét bổ sung nhãn chữ nổi Braille trên thùng rác tại công viên và các địa điểm công cộng, góp phần tạo môi trường thân thiện hơn với người khuyết tật.

#pagebreak()

= TÀI LIỆU THAM KHẢO

#set par(first-line-indent: 0pt)
#bibliography("references.bib", title: none, style: "ieee")

#pagebreak()

#let phuluc-counter = counter("phuluc")
#let in-phuluc = state("phuluc", false)

#show heading.where(level: 1): it => {
  context {
    if in-phuluc.at(here()) {
      phuluc-counter.step()
      block(above: 12pt, below: 6pt)[
        #set text(size: 13pt)
        #set align(left)
        *Phụ lục #context phuluc-counter.display(): #it.body*
      ]
    } else {
      it
    }
  }
}

#align(center)[
  *PHỤ LỤC*
]


// Tại vị trí bắt đầu PHỤ LỤC:
#in-phuluc.update(true)

= Code python để thu thập dữ liệu từ Internet (waste_images.py)

```python
#!/usr/bin/env python3
"""
AI Green Eye - Waste Image Downloader V6
Real photos only, no illustrations. Expanded keywords + plastic bag focus.
"""

import os
import sys
import subprocess
import hashlib
import time
import re
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np

try:
    from PIL import Image
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image

# ── Config ──────────────────────────────────────────────────
BASE_DIR = Path("dataset")
TIMEOUT = 20
MAX_WORKERS = 4
MIN_SIZE_KB = 10
MIN_DIM = 100

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,*/*;q=0.9",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.bing.com/",
}

BLOCKED_DOMAINS = [
    "shutterstock.com", "istockphoto.com", "gettyimages.com",
    "dreamstime.com", "123rf.com", "depositphotos.com",
    "adobestock.com", "alamy.com", "lookaside.fbsbx.com",
    "facebook.com", "bing.com", "microsoft.com",
    "vecteezy.com", "freepik.com", "flaticon.com",
    "vectorstock.com", "clipartmax.com", "clker.com",
    "openclipart.org",
]

ILLUSTRATION_KEYWORDS = [
    "vector", "illustration", "clipart", "cartoon", "drawing",
    "icon", "logo", "symbol", "graphic", "infographic",
    "diagram", "sketch", "doodle", "artwork", "svg",
]

IMG_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp")

CATEGORIES = {
    "organic": {
        "target": 500,
        "queries": [
            # Loose organic
            "banana peel garbage real photo",
            "apple core food scrap real",
            "vegetable peelings kitchen waste",
            "rotten fruit ground real photo",
            "dry leaves pile street real",
            "grass clippings lawn waste real",
            "used coffee grounds wet real",
            "eggshell compost real photo",
            "moldy bread food waste real",
            "tree branch yard waste pile",
            "rice leftover food waste real",
            "corn husk compost real photo",
            "orange peel garbage real photo",
            "watermelon rind waste real",
            "mango seed food scrap real",
            "fish bones food waste real",
            "meat scraps food waste real",
            "onion skin vegetable waste real",
            "carrot peeling kitchen scrap real",
            "tomato rotten waste real photo",
            "food waste bin kitchen real",
            "compost pile outdoor real photo",
            "organic garbage dump real photo",
            "food leftover thrown away real",
            "fruit rot ground outdoor real",
            "wet organic waste real photo",
            "vegetable market waste real",
            "kitchen bin full organic real",
            "leftover rice thrown garbage real",
            "spoiled vegetable waste real",
            "rotten egg waste real photo",
            "bread crust thrown away real",
            "used tea bag waste real",
            "fruit peel pile waste real",
            "garden waste pile real photo",
            # In plastic bag
            "organic waste in plastic bag real",
            "food waste in plastic bag real",
            "fruit waste tied plastic bag real",
            "vegetable scraps black plastic bag",
            "kitchen organic waste garbage bag",
            "food scrap white plastic bag real",
            "banana peel plastic bag garbage",
            "rotten food plastic bag tied real",
            "organic trash bag street real",
            "food waste bag outdoor real photo",
            "wet waste plastic bag real photo",
            "compost bag organic real photo",
            "food garbage bag tied real photo",
            "organic rubbish bag real photo",
        ],
    },
    "inorganic": {
        "target": 500,
        "queries": [
            # Loose inorganic
            "crushed plastic bottles pile real",
            "aluminum cans recycling pile real",
            "tin can garbage dump real",
            "broken glass bottle ground real",
            "metal scrap pile real photo",
            "styrofoam packaging waste real",
            "plastic container trash real photo",
            "rubber tire waste dump real",
            "plastic wrap waste real photo",
            "glass jar broken waste real",
            "soda can crushed pile real",
            "plastic straw waste pile real",
            "bottle cap collection real photo",
            "plastic bag pollution street real",
            "cardboard box recycling pile real",
            "old newspaper waste pile real",
            "plastic cup thrown away real",
            "plastic bottle thrown street real",
            "metal can waste bin real photo",
            "broken plastic chair waste real",
            "foam cup waste pile real photo",
            "plastic packaging waste real photo",
            "bottle plastic thrown ground real",
            "empty bottle pile garbage real",
            "recycling bin plastic cans real",
            "plastic lid waste pile real",
            "broken plastic toy real photo",
            "used plastic bag waste real",
            "pvc pipe scrap real photo",
            "tin foil waste real photo",
            "broken umbrella waste real photo",
            "plastic hanger waste pile real",
            "used plastic wrap real photo",
            "old plastic bucket waste real",
            "plastic film waste real photo",
            # In plastic bag
            "inorganic waste in plastic bag real",
            "plastic bottles black garbage bag real",
            "cans bottles plastic bag tied real",
            "recycling plastic bag full real photo",
            "plastic waste tied bag street real",
            "inorganic trash bag outdoor real photo",
            "bottles cans white plastic bag real",
            "plastic garbage bag full street real",
            "mixed plastic waste bag real photo",
            "glass bottles plastic bag real photo",
            "cardboard plastic bag garbage real",
            "inorganic bag waste bin real photo",
            "plastic rubbish bag tied real photo",
            "cans garbage bag outdoor real",
        ],
    },
    "other": {
        "target": 400,
        "queries": [
            # Loose other
            "old batteries disposal pile real",
            "broken electronics e-waste real",
            "used light bulb trash real photo",
            "old shoes pile waste real photo",
            "torn clothing textile waste real",
            "construction debris rubble pile real",
            "paint can hazardous waste real",
            "broken toy junk pile real photo",
            "cigarette butts litter ground real",
            "ceramic broken pieces waste real",
            "used diaper waste real photo",
            "mixed household garbage real photo",
            "electronic waste dump real photo",
            "old phone broken waste real photo",
            "cable wire scrap waste real photo",
            "broken furniture waste outdoor real",
            "old book paper waste pile real",
            "used mask waste ground real photo",
            "sanitary waste bin real photo",
            "broken mirror waste real photo",
            "old mattress waste outdoor real",
            "chemical container waste real photo",
            "mixed garbage pile street real photo",
            "general waste bin full real photo",
            "hazardous waste pile real photo",
            # In plastic bag
            "mixed waste in plastic bag real photo",
            "other waste tied plastic bag real",
            "hazardous waste black garbage bag real",
            "household waste bag outdoor real photo",
            "mixed trash plastic bag street real",
            "other garbage bag tied real photo",
            "broken items plastic bag waste real",
            "general waste bag bin real photo",
            "rubbish bag other waste real photo",
        ],
    },
}


# ── Bing scraper ───────────────────────────────────────────
def bing_image_urls(query: str, count: int = 80) -> list:
    all_urls = []
    seen = set()
    encoded = quote(query)

    for page in range(4):
        offset = page * 35
        url = (
            f"https://www.bing.com/images/async"
            f"?q={encoded}&first={offset}&count=35"
            f"&adlt=strict&qft=+filterui:photo-photo"
        )
        req = Request(url, headers=HEADERS)
        try:
            with urlopen(req, timeout=15) as resp:
                html = resp.read().decode("utf-8", errors="ignore")
        except Exception:
            continue

        urls_json = re.findall(
            r'https?://[^"\\,\s\}<>]+\.(?:jpg|jpeg|png|webp|gif)',
            html, re.IGNORECASE,
        )
        urls_datasrc = re.findall(r'data-src="(https?://[^"]+)"', html)
        urls_src = re.findall(r'<img[^>]+src="(https?://[^"]+)"', html)

        candidates = urls_json + urls_datasrc + urls_src

        for u in candidates:
            u = u.replace("&amp;", "&")
            lower = u.lower()

            if any(d in lower for d in BLOCKED_DOMAINS):
                continue
            if lower.endswith(".svg"):
                continue
            if any(kw in lower for kw in ILLUSTRATION_KEYWORDS):
                continue
            if "pixel.quantserve" in lower or "b.scorecardresearch" in lower:
                continue
            if "/rp/" in u or "data:image" in u:
                continue
            if " " in u:
                continue

            has_ext = any(lower.split("?")[0].endswith(e) for e in IMG_EXTENSIONS)
            has_img_param = any(k in lower for k in ["image", "img", "photo", "pic"])
            if not has_ext and not has_img_param:
                continue

            if u not in seen:
                seen.add(u)
                all_urls.append(u)

        if len(all_urls) >= count:
            break
        time.sleep(0.3)

    return all_urls[:count]


# ── Illustration detector ──────────────────────────────────
def is_illustration(img: Image.Image) -> bool:
    img_small = img.convert("RGB").resize((64, 64))
    arr = np.array(img_small).reshape(-1, 3)
    unique = len(set(map(tuple, arr)))
    return unique < 200


# ── Download & validate ────────────────────────────────────
def download_one(url: str, save_path: Path) -> bool:
    try:
        req = Request(url, headers={
            "User-Agent": HEADERS["User-Agent"],
            "Referer": "https://www.bing.com/",
        })
        with urlopen(req, timeout=TIMEOUT) as resp:
            data = resp.read()

        if len(data) < MIN_SIZE_KB * 1024:
            return False

        save_path.write_bytes(data)

        with Image.open(save_path) as img:
            img.verify()

        with Image.open(save_path) as img:
            w, h = img.size
            if w < MIN_DIM or h < MIN_DIM:
                save_path.unlink(missing_ok=True)
                return False
            if is_illustration(img):
                save_path.unlink(missing_ok=True)
                return False

        return True
    except Exception:
        save_path.unlink(missing_ok=True)
        return False


def ext_from_url(url: str) -> str:
    lower = url.lower().split("?")[0]
    for e in [".png", ".webp", ".gif", ".bmp"]:
        if lower.endswith(e):
            return e
    return ".jpg"


# ── Category downloader ───────────────────────────────────
def count_images(folder: Path) -> int:
    if not folder.exists():
        return 0
    return sum(
        1 for p in folder.iterdir()
        if p.is_file() and p.suffix.lower() in IMG_EXTENSIONS
    )


def existing_hashes(folder: Path) -> set:
    hashes = set()
    if not folder.exists():
        return hashes
    for p in folder.iterdir():
        if p.is_file() and p.stat().st_size > 0:
            try:
                hashes.add(hashlib.md5(p.read_bytes()).hexdigest())
            except Exception:
                pass
    return hashes


def download_category(category: str, target: int, queries: list):
    dst = BASE_DIR / category
    dst.mkdir(parents=True, exist_ok=True)

    known = existing_hashes(dst)
    idx = count_images(dst)

    print(f"\n{'='*60}")
    print(f" {category.upper()}  target={target}  existing={idx}")
    print(f"{'='*60}")

    for qi, query in enumerate(queries, 1):
        current = count_images(dst)
        if current >= target:
            print(f"  [DONE] target reached ({current}/{target})")
            break

        need = target - current
        fetch = min(need + 15, 80)

        print(f"\n  [{qi}/{len(queries)}] '{query}'  have={current} need={need}")
        urls = bing_image_urls(query, fetch)
        print(f"    found {len(urls)} candidate URLs")

        ok = 0
        fail = 0

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
            futures = {}
            for url in urls:
                if count_images(dst) >= target:
                    break
                idx += 1
                ext = ext_from_url(url)
                path = dst / f"{category}_{idx:05d}{ext}"
                futures[pool.submit(download_one, url, path)] = path

            for future in as_completed(futures):
                path = futures[future]
                try:
                    if future.result():
                        h = hashlib.md5(path.read_bytes()).hexdigest()
                        if h in known:
                            path.unlink(missing_ok=True)
                            fail += 1
                        else:
                            known.add(h)
                            ok += 1
                    else:
                        fail += 1
                except Exception:
                    fail += 1

        total_now = count_images(dst)
        print(f"    ✓ saved={ok}  ✗ skip={fail}  total={total_now}")
        time.sleep(0.5)

    final = count_images(dst)
    mark = "✓" if final >= target else "△"
    print(f"\n  {mark} {category}: {final}/{target}")


# ── Summary ────────────────────────────────────────────────
def write_summary():
    lines = [
        "AI GREEN EYE - DATASET SUMMARY",
        "=" * 40,
        f"Generated: {time.strftime('%Y-%m-%d %H:%M')}",
        "",
    ]
    total = 0
    for cat in CATEGORIES:
        c = count_images(BASE_DIR / cat)
        total += c
        t = CATEGORIES[cat]["target"]
        mark = "✓" if c >= t else "△"
        lines.append(f"  {mark} {cat:<12}: {c:>4} / {t}")
    lines.append("-" * 40)
    lines.append(f"    {'TOTAL':<12}: {total:>4}")
    lines.append("")
    lines.append("Next: python train_model.py")

    report = "\n".join(lines)
    Path("dataset_summary.txt").write_text(report, encoding="utf-8")
    print("\n" + report)


# ── Main ───────────────────────────────────────────────────
def main():
    print("AI GREEN EYE - Waste Image Downloader V6")
    print(f"Categories: {list(CATEGORIES.keys())}")
    print(f"Output: {BASE_DIR.resolve()}\n")

    for category, cfg in CATEGORIES.items():
        download_category(category, cfg["target"], cfg["queries"])

    write_summary()


if __name__ == "__main__":
    main()
```

=  Training code (train_model.py)

```python
#!/usr/bin/env python3
"""
AI Green Eye - Train Waste Classifier
MobileNetV2 + transfer learning. Compatible với Keras 3 / TF 2.16+
"""

import os
import sys
import argparse
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import (
    EarlyStopping,
    ReduceLROnPlateau,
    ModelCheckpoint,
)

# ── Config ───────────────────────────────────────────────────
IMAGE_SIZE       = (224, 224)
BATCH_SIZE       = 32
EPOCHS_PHASE1    = 30
EPOCHS_PHASE2    = 20
LEARNING_RATE    = 0.001
VALIDATION_SPLIT = 0.2
CLASSES          = ["organic", "inorganic", "other"]
AUTOTUNE         = tf.data.AUTOTUNE


# ── Dataset ──────────────────────────────────────────────────
def find_dataset(custom: str = None) -> Path:
    if custom:
        p = Path(custom).resolve()
        if p.exists() and (p / "organic").exists():
            return p
        print(f"✗ Không tìm thấy dataset tại: {p}")
        sys.exit(1)

    candidates = [
        Path("dataset"),
        Path("../dataset"),
        Path.home() / "airgreeneye" / "dataset",
    ]
    for p in candidates:
        r = p.resolve()
        if r.exists() and (r / "organic").exists():
            return r

    print("✗ Không tìm thấy dataset.")
    print("  Chạy: python download_waste_images.py")
    sys.exit(1)


def check_dataset(dataset_dir: Path) -> bool:
    print(f"[1] Kiểm tra dataset: {dataset_dir}\n")
    ok = True
    for cls in CLASSES:
        d = dataset_dir / cls
        if not d.exists():
            print(f"  ✗ {cls}: không có thư mục")
            ok = False
            continue
        exts = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
        count = sum(1 for f in d.iterdir() if f.suffix.lower() in exts)
        mark = "✓" if count >= 250 else "△" if count >= 100 else "✗"
        print(f"  {mark} {cls}: {count} ảnh")
        if count < 100:
            ok = False
    print()
    return ok


# ── Data loading ─────────────────────────────────────────────
def augment(image, label):
    image = tf.image.random_flip_left_right(image)
    image = tf.image.random_brightness(image, 0.2)
    image = tf.image.random_contrast(image, 0.8, 1.2)
    image = tf.image.random_saturation(image, 0.8, 1.2)
    image = tf.image.resize_with_crop_or_pad(image, 240, 240)
    image = tf.image.resize(image, IMAGE_SIZE)
    return image, label


def load_data(dataset_dir: Path):
    print("[2] Tải dataset...\n")

    train_ds = tf.keras.utils.image_dataset_from_directory(
        str(dataset_dir),
        validation_split=VALIDATION_SPLIT,
        subset="training",
        seed=42,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="categorical",
        class_names=CLASSES,
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        str(dataset_dir),
        validation_split=VALIDATION_SPLIT,
        subset="validation",
        seed=42,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="categorical",
        class_names=CLASSES,
    )

    # Normalize [0,1]
    normalization = layers.Rescaling(1.0 / 255)

    train_ds = (
        train_ds
        .map(lambda x, y: (normalization(x), y), num_parallel_calls=AUTOTUNE)
        .map(augment, num_parallel_calls=AUTOTUNE)
        .cache()
        .shuffle(1000)
        .prefetch(AUTOTUNE)
    )

    val_ds = (
        val_ds
        .map(lambda x, y: (normalization(x), y), num_parallel_calls=AUTOTUNE)
        .cache()
        .prefetch(AUTOTUNE)
    )

    print(f"  Classes: {CLASSES}\n")
    return train_ds, val_ds


# ── Model ────────────────────────────────────────────────────
def build_model(num_classes: int):
    print("[3] Xây dựng model...\n")

    base = MobileNetV2(
        input_shape=(*IMAGE_SIZE, 3),
        include_top=False,
        weights="imagenet",
    )
    base.trainable = False

    model = models.Sequential([
        base,
        layers.GlobalAveragePooling2D(),
        layers.Dense(256, activation="relu"),
        layers.Dropout(0.5),
        layers.Dense(128, activation="relu"),
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation="softmax"),
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    print(f"  Tham số: {model.count_params():,}\n")
    return model, base


# ── Training ─────────────────────────────────────────────────
def train(model, base, train_ds, val_ds):
    callbacks_p1 = [
        EarlyStopping(
            monitor="val_loss",
            patience=5,
            restore_best_weights=True,
            verbose=1,
        ),
        ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=3,
            min_lr=1e-6,
            verbose=1,
        ),
        ModelCheckpoint(
            "best_model.keras",
            monitor="val_accuracy",
            save_best_only=True,
            mode="max",
            verbose=0,
        ),
    ]

    print("[4] Phase 1: Frozen base...\n")
    h1 = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS_PHASE1,
        callbacks=callbacks_p1,
        verbose=1,
    )

    print("\n[5] Phase 2: Fine-tuning...\n")
    base.trainable = True
    for layer in base.layers[:-30]:
        layer.trainable = False

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    callbacks_p2 = [
        EarlyStopping(
            monitor="val_loss",
            patience=5,
            restore_best_weights=True,
            verbose=1,
        ),
        ModelCheckpoint(
            "best_model.keras",
            monitor="val_accuracy",
            save_best_only=True,
            mode="max",
            verbose=0,
        ),
    ]

    h2 = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS_PHASE2,
        callbacks=callbacks_p2,
        verbose=1,
    )

    history = {}
    for key in h1.history:
        history[key] = h1.history[key] + h2.history.get(key, [])

    return history, model


# ── Finalize ─────────────────────────────────────────────────
def finalize(model, val_ds, history):
    print("\n[6] Lưu model...\n")

    val_loss, val_acc = model.evaluate(val_ds, verbose=0)
    print(f"  Val accuracy: {val_acc*100:.2f}%")
    print(f"  Val loss:     {val_loss:.4f}\n")

    if val_acc >= 0.85:
        print("  ✓ Accuracy tốt (≥85%)")
    elif val_acc >= 0.80:
        print("  ✓ Accuracy đạt yêu cầu (≥80%)")
    elif val_acc >= 0.70:
        print("  △ Accuracy trung bình, có thể thu thập thêm ảnh")
    else:
        print("  ✗ Accuracy thấp (<70%), kiểm tra lại dataset")

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    axes[0].plot(history.get("accuracy", []), label="train")
    axes[0].plot(history.get("val_accuracy", []), label="val")
    axes[0].axhline(y=0.80, color="r", linestyle="--", alpha=0.5, label="80%")
    axes[0].set_title("Accuracy")
    axes[0].set_xlabel("Epoch")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(history.get("loss", []), label="train")
    axes[1].plot(history.get("val_loss", []), label="val")
    axes[1].set_title("Loss")
    axes[1].set_xlabel("Epoch")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("training_history.png", dpi=100)
    print("  Saved: training_history.png")

    Path("class_labels.txt").write_text("\n".join(CLASSES), encoding="utf-8")
    print("  Saved: class_labels.txt")

    print("\n[DONE]")
    print("  best_model.keras")
    print("  class_labels.txt")
    print("  training_history.png")
    print("\nTiếp theo: python evaluate_model.py")


# ── Main ─────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", help="Đường dẫn dataset")
    args = parser.parse_args()

    print("AI GREEN EYE - Model Training")
    print(f"TensorFlow: {tf.__version__}")
    print(f"GPU: {len(tf.config.list_physical_devices('GPU')) > 0}\n")

    dataset_dir        = find_dataset(args.dataset)
    if not check_dataset(dataset_dir):
        print("Dataset không đủ. Thu thập thêm ảnh trước.")
        sys.exit(1)

    train_ds, val_ds   = load_data(dataset_dir)
    model, base        = build_model(len(CLASSES))
    history, model     = train(model, base, train_ds, val_ds)
    finalize(model, val_ds, history)


if __name__ == "__main__":
    main()
```

=  Code đánh giá (evaluate_model.py) kết quả training
```python
#!/usr/bin/env python3
"""
AI Green Eye - Evaluate Model
Kiểm tra accuracy, per-class metrics, confusion matrix.
Compatible với Keras 3 / TF 2.16+
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    precision_recall_fscore_support,
)

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import tensorflow as tf
from tensorflow.keras import layers

ACCEPT_ACCURACY = 0.80
IMAGE_SIZE      = (224, 224)
BATCH_SIZE      = 32
CLASSES         = ["organic", "inorganic", "other"]
AUTOTUNE        = tf.data.AUTOTUNE


# ── Load ─────────────────────────────────────────────────────
def load_model():
    path = Path("best_model.keras")
    if not path.exists():
        print("✗ Không tìm thấy best_model.keras")
        print("  Chạy: python train_model.py")
        sys.exit(1)
    print(f"[1] Load model: {path}\n")
    return tf.keras.models.load_model(str(path))


def find_dataset() -> Path:
    candidates = [Path("dataset"), Path("../dataset")]
    for p in candidates:
        r = p.resolve()
        if r.exists() and (r / "organic").exists():
            return r
    print("✗ Không tìm thấy dataset.")
    sys.exit(1)


# ── Test set ─────────────────────────────────────────────────
def load_test_set(dataset_dir: Path):
    print("[2] Tải test set...\n")

    # Dùng toàn bộ dataset không augment, không shuffle
    ds = tf.keras.utils.image_dataset_from_directory(
        str(dataset_dir),
        seed=42,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="categorical",
        class_names=CLASSES,
        shuffle=False,
    )

    normalization = layers.Rescaling(1.0 / 255)
    ds = ds.map(lambda x, y: (normalization(x), y), num_parallel_calls=AUTOTUNE)

    images, labels = [], []
    for x, y in ds:
        images.append(x.numpy())
        labels.append(y.numpy())

    images = np.concatenate(images)
    labels = np.concatenate(labels)
    labels_int = np.argmax(labels, axis=1)

    print(f"  Tổng: {len(images)} ảnh")
    for i, cls in enumerate(CLASSES):
        print(f"  {cls}: {int((labels_int == i).sum())} ảnh")
    print()

    return images, labels_int


# ── Evaluate ─────────────────────────────────────────────────
def evaluate(model, images, labels):
    print("[3] Chạy predictions...\n")
    preds     = model.predict(images, batch_size=BATCH_SIZE, verbose=0)
    pred_cls  = np.argmax(preds, axis=1)
    pred_prob = np.max(preds, axis=1)
    return pred_cls, pred_prob


def print_metrics(labels, pred_cls) -> float:
    print("[4] Kết quả\n" + "=" * 50)

    acc  = accuracy_score(labels, pred_cls)
    mark = "✓" if acc >= ACCEPT_ACCURACY else "✗"
    print(f"{mark} Accuracy: {acc*100:.2f}%  (ngưỡng: {ACCEPT_ACCURACY*100:.0f}%)\n")

    precision, recall, f1, support = precision_recall_fscore_support(
        labels, pred_cls, labels=range(len(CLASSES))
    )

    print("Per-class:")
    print("-" * 50)
    for i, cls in enumerate(CLASSES):
        m = "✓" if recall[i] >= ACCEPT_ACCURACY else "△" if recall[i] >= 0.6 else "✗"
        print(f"  {m} {cls:12s}  P={precision[i]:.3f}  R={recall[i]:.3f}  F1={f1[i]:.3f}  (n={support[i]})")

    print("\nClassification Report:")
    print("-" * 50)
    print(classification_report(labels, pred_cls, target_names=CLASSES, digits=3))

    return acc


# ── Confusion matrix ─────────────────────────────────────────
def plot_confusion(labels, pred_cls):
    print("[5] Confusion matrix...")
    cm      = confusion_matrix(labels, pred_cls)
    cm_norm = cm.astype("float") / cm.sum(axis=1, keepdims=True)

    plt.figure(figsize=(7, 5))
    plt.imshow(cm, cmap="Blues")

    for i in range(len(CLASSES)):
        for j in range(len(CLASSES)):
            plt.text(
                j, i,
                f"{cm[i,j]}\n({cm_norm[i,j]:.0%})",
                ha="center", va="center",
                color="white" if cm_norm[i,j] > 0.5 else "black",
                fontsize=10,
            )

    plt.xticks(range(len(CLASSES)), CLASSES, rotation=45)
    plt.yticks(range(len(CLASSES)), CLASSES)
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.title("Confusion Matrix")
    plt.colorbar()
    plt.tight_layout()
    plt.savefig("confusion_matrix.png", dpi=100)
    print("  Saved: confusion_matrix.png\n")


# ── Confidence plot ───────────────────────────────────────────
def plot_confidence(labels, pred_cls, pred_prob):
    print("[6] Confidence distribution...")
    correct = pred_cls == labels

    plt.figure(figsize=(8, 4))
    plt.hist(pred_prob[correct],  bins=20, alpha=0.7, label="Đúng", color="green")
    plt.hist(pred_prob[~correct], bins=20, alpha=0.7, label="Sai",  color="red")
    plt.axvline(x=0.80, color="orange", linestyle="--", label="Ngưỡng 80%")
    plt.xlabel("Confidence")
    plt.ylabel("Số lượng")
    plt.title("Phân bố Confidence")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("prediction_confidence.png", dpi=100)
    print("  Saved: prediction_confidence.png\n")


# ── Summary ──────────────────────────────────────────────────
def summary(acc: float):
    print("[DONE] Đánh giá hoàn tất\n")
    print("Files:")
    print("  confusion_matrix.png")
    print("  prediction_confidence.png\n")

    if acc >= ACCEPT_ACCURACY:
        print(f"✓ Model đạt yêu cầu ({acc*100:.1f}% ≥ {ACCEPT_ACCURACY*100:.0f}%)")
        print("  Tiếp theo: python convert_tflite.py")
    else:
        print(f"✗ Model chưa đạt ({acc*100:.1f}% < {ACCEPT_ACCURACY*100:.0f}%)")
        print("  Gợi ý:")
        print("  - Thu thập thêm ảnh mỗi class")
        print("  - Kiểm tra chất lượng dataset")
        print("  - Chạy lại: python train_model.py")


# ── Main ─────────────────────────────────────────────────────
def main():
    print("AI GREEN EYE - Model Evaluation\n")

    model               = load_model()
    dataset_dir         = find_dataset()
    images, labels      = load_test_set(dataset_dir)
    pred_cls, pred_prob = evaluate(model, images, labels)
    acc                 = print_metrics(labels, pred_cls)

    plot_confusion(labels, pred_cls)
    plot_confidence(labels, pred_cls, pred_prob)
    summary(acc)


if __name__ == "__main__":
    main()
```
= Chuyển sang file tflite để chạy trên Pi 2W (convert_tflite.py)
```python
#!/usr/bin/env python3
"""
AI Green Eye - Convert to TensorFlow Lite
Xuất model sang .tflite để chạy trên Raspberry Pi Zero 2W
với ai-edge-litert (Google).
"""

import os
import sys
import numpy as np
from pathlib import Path

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import tensorflow as tf

IMAGE_SIZE = (224, 224)
CLASSES    = ["organic", "inorganic", "other"]


# ── Find paths ───────────────────────────────────────────────
def find_model() -> Path:
    candidates = [
        Path("best_model.keras"),
        Path("../best_model.keras"),
    ]
    for p in candidates:
        r = p.resolve()
        if r.exists():
            return r
    print("✗ Không tìm thấy best_model.keras")
    print("  Chạy: python train_model.py")
    sys.exit(1)


def find_dataset() -> Path:
    candidates = [Path("dataset"), Path("../dataset")]
    for p in candidates:
        r = p.resolve()
        if r.exists() and (r / "organic").exists():
            return r
    return None


# ── Load representative dataset ──────────────────────────────
def load_rep_dataset(dataset_dir: Path) -> np.ndarray:
    if dataset_dir is None:
        print("  △ Không có dataset, dùng random data để calibrate")
        return np.random.rand(100, 224, 224, 3).astype(np.float32)

    ds = tf.keras.utils.image_dataset_from_directory(
        str(dataset_dir),
        image_size=IMAGE_SIZE,
        batch_size=32,
        shuffle=True,
        seed=42,
        class_names=CLASSES,
    )

    normalization = tf.keras.layers.Rescaling(1.0 / 255)
    images = []
    for x, _ in ds.take(8):
        images.append(normalization(x).numpy())

    data = np.concatenate(images)
    print(f"  ✓ Representative samples: {len(data)}")
    return data


# ── Convert full precision ────────────────────────────────────
def convert_full(model) -> tuple:
    print("\n[3] Full precision...")
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite    = converter.convert()
    path      = Path("waste_classifier_unquant.tflite")
    path.write_bytes(tflite)
    size = len(tflite) / (1024 * 1024)
    print(f"  ✓ {path.name} ({size:.1f}MB)")
    return path, size


# ── Convert INT8 quantized ────────────────────────────────────
def convert_int8(model, rep_data: np.ndarray) -> tuple:
    print("\n[4] INT8 quantized...")

    def representative_dataset():
        for i in range(min(len(rep_data), 256)):
            yield [rep_data[i:i+1].astype(np.float32)]

    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations                   = [tf.lite.Optimize.DEFAULT]
    converter.representative_dataset          = representative_dataset
    converter.target_spec.supported_ops       = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
    converter.inference_input_type            = tf.int8
    converter.inference_output_type           = tf.int8

    try:
        tflite = converter.convert()
        path   = Path("waste_classifier.tflite")
        path.write_bytes(tflite)
        size = len(tflite) / (1024 * 1024)
        print(f"  ✓ {path.name} ({size:.1f}MB) — INT8")
        return path, size

    except Exception as e:
        print(f"  △ INT8 thất bại: {e}")
        print("  Fallback: dynamic range quantization...")

        converter2 = tf.lite.TFLiteConverter.from_keras_model(model)
        converter2.optimizations = [tf.lite.Optimize.DEFAULT]
        tflite = converter2.convert()
        path   = Path("waste_classifier.tflite")
        path.write_bytes(tflite)
        size = len(tflite) / (1024 * 1024)
        print(f"  ✓ {path.name} ({size:.1f}MB) — dynamic")
        return path, size


# ── Verify ───────────────────────────────────────────────────
def verify(path: Path):
    print(f"\n[5] Kiểm tra {path.name}...")
    interpreter = tf.lite.Interpreter(model_path=str(path))
    interpreter.allocate_tensors()

    inp = interpreter.get_input_details()[0]
    out = interpreter.get_output_details()[0]

    print(f"  Input:  {inp['shape']}  dtype={inp['dtype'].__name__}")
    print(f"  Output: {out['shape']}  dtype={out['dtype'].__name__}")

    # Test inference
    if inp["dtype"] == np.int8:
        dummy = np.zeros([1, 224, 224, 3], dtype=np.int8)
    else:
        dummy = np.zeros([1, 224, 224, 3], dtype=np.float32)

    interpreter.set_tensor(inp["index"], dummy)
    interpreter.invoke()
    result = interpreter.get_tensor(out["index"])
    print(f"  Output shape: {result.shape}  ✓")


# ── Main ─────────────────────────────────────────────────────
def main():
    print("AI GREEN EYE - TFLite Conversion")
    print(f"TensorFlow: {tf.__version__}\n")

    # Load model
    model_path = find_model()
    print(f"[1] Load model: {model_path}")
    model = tf.keras.models.load_model(str(model_path))
    print(f"  Tham số: {model.count_params():,}")

    # Load rep dataset
    dataset_dir = find_dataset()
    print(f"\n[2] Representative dataset...")
    rep_data = load_rep_dataset(dataset_dir)

    # Convert
    full_path, full_size = convert_full(model)
    quant_path, quant_size = convert_int8(model, rep_data)

    # Verify
    verify(quant_path)

    # Class labels
    print("\n[6] Class labels...")
    labels_path = Path("class_labels.txt")
    if not labels_path.exists():
        labels_path.write_text("\n".join(CLASSES), encoding="utf-8")
        print("  Created: class_labels.txt")
    else:
        print("  ✓ Exists: class_labels.txt")

    # Summary
    print("\n" + "=" * 50)
    print("DONE - File để deploy lên Pi:")
    print(f"  ✓ {quant_path.name:<35} ({quant_size:.1f}MB) ← dùng cái này")
    print(f"  ✓ {full_path.name:<35} ({full_size:.1f}MB) ← backup")
    print(f"  ✓ class_labels.txt")
    print(f"\nCompression: {(1 - quant_size/full_size)*100:.1f}%")
    print("\nSao chép lên Pi:")
    print(f"  scp waste_classifier.tflite hieunga@hieunga.local:/home/hieunga/airgreeneye/")
    print(f"  scp class_labels.txt hieunga@hieunga.local:/home/hieunga/airgreeneye/")
    print("\nTiếp theo: python main.py (trên Pi)")


if __name__ == "__main__":
    main()
```
= Tạo các file mp3, để thông báo (code sau dành riêng cho máy Macbook, nếu dùng Windows hoặc Linux thì có thể dùng phần mềm chuyển text-to-speech khác để tạo file mp3 tương tự)

```python
#!/usr/bin/env python3
"""
AI Green Eye - Text to Speech
Tạo file mp3 thông báo bằng giọng Linh (macOS).
"""

import subprocess
from pathlib import Path

OUTPUT_DIR = Path("notification")
OUTPUT_DIR.mkdir(exist_ok=True)

VOICE = "Linh"

MESSAGES = {
    # STARTUP
    "HIGH_STARTUP_01_mat_than_san_sang":       "Hệ thống đã sẵn sàng",
    "MID_STARTUP_02_dang_khoi_dong":           "Đang khởi động, vui lòng chờ",
    "MID_STARTUP_03_cho_ket_noi_camera":       "Đang kết nối camera",
    "HIGH_STARTUP_04_camera_san_sang":         "Camera đã sẵn sàng",
    "LOW_STARTUP_05_lay_net_thanh_cong":       "Kết nối mạng thành công",
    "HIGH_SWITCH_47_he_thong_da_bat": "Hệ thống đã bật",
    "MID_SWITCH_48_he_thong_da_tat":  "Hệ thống đã tắt",

    # USER
    "MID_USER_43_san_sang_dua_vat_the":        "Vui lòng đưa vật thể vào trước camera",
    "MID_USER_44_giu_on_dinh":                 "Vui lòng giữ yên vật thể",
    "LOW_USER_45_khong_hieu_lenh":             "Xin lỗi, tôi không hiểu yêu cầu",
    "CRIT_USER_46_lien_he_ky_su":              "Vui lòng liên hệ kỹ thuật viên",

    # IMAGE
    "LOW_IMAGE_10_dang_xu_ly_anh":             "Đang xử lý hình ảnh",
    "LOW_IMAGE_11_xu_ly_thanh_cong":           "Xử lý hình ảnh hoàn tất",

    # INFERENCE
    "LOW_INFERENCE_14_dang_phan_loai":         "Đang phân loại rác",
    "LOW_INFERENCE_15_phan_loai_thanh_cong":   "Phân loại hoàn tất",
    "MID_INFERENCE_16_xu_ly_qua_lau":          "Quá trình xử lý mất nhiều thời gian hơn bình thường",

    #RESULT
    "HIGH_RESULT_17_rac_huu_co":               "Đây là rác hữu cơ",
    "HIGH_RESULT_18_rac_vo_co":                "Đây là rác vô cơ",
    "HIGH_RESULT_19_rac_khac_loai":            "Loại rác này chưa xác định được, vui lòng hỏi thêm",
    "MID_RESULT_20_khong_chac_chan":            "Tôi chưa chắc chắn về loại rác này, vui lòng thử lại",
    "MID_RESULT_21_khong_phai_rac":            "Vật thể này có vẻ không phải rác",

    # CAMERA
    "CRIT_CAMERA_06_khong_tim_camera":         "Không tìm thấy camera, vui lòng kiểm tra kết nối",
    "CRIT_CAMERA_07_loi_camera_chup_anh":      "Camera gặp sự cố khi chụp ảnh",
    "MID_CAMERA_08_anh_sang_toi_qua":          "Ánh sáng quá tối, vui lòng di chuyển đến nơi sáng hơn",
    "MID_CAMERA_09_khong_tim_vat_the":         "Không phát hiện vật thể, vui lòng đưa rác lại gần hơn",

    # MODEL
    "CRIT_IMAGE_12_mo_hinh_khong_tim":         "Không tìm thấy mô hình AI",
    "CRIT_IMAGE_13_mo_hinh_bi_loi":            "Mô hình AI gặp sự cố",
    "CRIT_HEALTH_42_tflite_chua_cai":          "Thư viện AI chưa được cài đặt",

    # HEALTH
    "HIGH_HEALTH_37_thiet_bi_khoe_manh":       "Thiết bị đang hoạt động tốt",
    "MID_HEALTH_38_co_loi_nho":                "Thiết bị có một số lỗi nhỏ",
    "CRIT_HEALTH_39_loi_nghiem_trong":         "Thiết bị gặp lỗi nghiêm trọng, vui lòng khởi động lại",
    "HIGH_HEALTH_40_bo_nho_day":               "Bộ nhớ gần đầy, hiệu suất có thể bị ảnh hưởng",
    "HIGH_HEALTH_41_qua_nong":                 "Nhiệt độ thiết bị quá cao, vui lòng để thiết bị nghỉ",

    # NETWORK
    "MID_NETWORK_27_wifi_ket_noi":             "Đã kết nối WiFi",
    "MID_NETWORK_28_wifi_mat_ket_noi":         "Mất kết nối WiFi",
    "MID_NETWORK_29_wifi_khong_tim":           "Không tìm thấy mạng WiFi",
    "LOW_NETWORK_30_dang_ket_noi_wifi":        "Đang kết nối WiFi, vui lòng chờ",

    # BATTERY
    "LOW_BATTERY_22_pin_day":                  "Pin đã đầy",
    "MID_BATTERY_23_pin_con_50":               "Pin còn năm mươi phần trăm",
    "HIGH_BATTERY_24_pin_con_20":              "Pin còn hai mươi phần trăm, vui lòng sạc sớm",
    "CRIT_BATTERY_25_pin_sap_het":             "Pin sắp hết, vui lòng sạc ngay",
    "CRIT_BATTERY_26_thiet_bi_tat_may":        "Pin quá thấp, thiết bị sẽ tắt",

    # UPDATE
    "LOW_UPDATE_31_kiem_tra_cap_nhat":         "Đang kiểm tra cập nhật",
    "MID_UPDATE_32_co_cap_nhat_moi":           "Có phiên bản mới, vui lòng cập nhật",
    "HIGH_UPDATE_33_dang_cap_nhat":            "Đang cập nhật, vui lòng không tắt thiết bị",
    "HIGH_UPDATE_34_cap_nhat_thanh_cong":      "Cập nhật thành công",
    "CRIT_UPDATE_35_cap_nhat_that_bai":        "Cập nhật thất bại, vui lòng thử lại",
    "LOW_UPDATE_36_phien_ban_moi_nhat":        "Thiết bị đang dùng phiên bản mới nhất",
}


def generate(name: str, text: str) -> bool:
    aiff_path = OUTPUT_DIR / f"{name}.aiff"
    mp3_path  = OUTPUT_DIR / f"{name}.mp3"

    # Bỏ qua nếu đã có
    if mp3_path.exists():
        print(f"  ✓ skip  {mp3_path.name}")
        return True

    try:
        # Tạo file aiff bằng say
        subprocess.run(
            ["say", "-v", VOICE, "-o", str(aiff_path), text],
            check=True,
            capture_output=True,
        )

        # Chuyển sang mp3 bằng ffmpeg
        subprocess.run(
            [
                "ffmpeg", "-y",
                "-i", str(aiff_path),
                "-codec:a", "libmp3lame",
                "-qscale:a", "2",
                str(mp3_path),
            ],
            check=True,
            capture_output=True,
        )

        aiff_path.unlink(missing_ok=True)
        print(f"  ✓ {mp3_path.name}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"  ✗ {name}: {e}")
        aiff_path.unlink(missing_ok=True)
        return False


def main():
    print("AI GREEN EYE - TTS Generator")
    print(f"Giọng: {VOICE}")
    print(f"Output: {OUTPUT_DIR.resolve()}\n")

    # Kiểm tra giọng Linh
    result = subprocess.run(["say", "-v", "?"], capture_output=True, text=True)
    if "Linh" not in result.stdout:
        print("✗ Giọng Linh không tìm thấy.")
        print("  Vào System Settings → Accessibility → Spoken Content → System Voice")
        print("  Tải giọng Linh (Vietnamese) về.\n")
        return

    # Kiểm tra ffmpeg
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
    except FileNotFoundError:
        print("✗ ffmpeg chưa cài. Chạy: brew install ffmpeg\n")
        return

    ok = 0
    fail = 0
    total = len(MESSAGES)

    for name, text in MESSAGES.items():
        if generate(name, text):
            ok += 1
        else:
            fail += 1

    print(f"\n{'='*40}")
    print(f"✓ Thành công: {ok}/{total}")
    if fail:
        print(f"✗ Thất bại:   {fail}/{total}")
    print(f"Output: {OUTPUT_DIR.resolve()}")
    print("\nSao chép lên Pi:")
    print("  scp -r notification/ hieunga@hieunga.local:/home/hieunga/airgreeneye/")


if __name__ == "__main__":
    main()
```
= Cấu hình toàn bộ hệ thống (config.py) (chạy trên Pi Zero 2W)
```python
#!/usr/bin/env python3
"""
AI Green Eye - Config
"""

from pathlib import Path

# ── Paths ────────────────────────────────────────────────────
BASE_DIR        = Path("/home/hieunga/airgreeneye")
MODEL_PATH      = BASE_DIR / "waste_classifier.tflite"
LABELS_PATH     = BASE_DIR / "class_labels.txt"
NOTIFY_DIR      = BASE_DIR / "notification"
CAPTURE_PATH    = BASE_DIR / "capture.jpg"

# ── Inference ────────────────────────────────────────────────
CONFIDENCE_THRESHOLD = 0.80
IMAGE_SIZE           = (224, 224)

# ── Motion detection ─────────────────────────────────────────
MOTION_THRESHOLD     = 25
MOTION_MIN_AREA      = 3000
COOLDOWN_SECONDS     = 5

# ── Camera ───────────────────────────────────────────────────
CAMERA_WIDTH         = 640
CAMERA_HEIGHT        = 480
CAMERA_WARMUP        = 2

# ── Audio ────────────────────────────────────────────────────
AUDIO_DEVICE         = "hw:0,0"

# ── Notification files ───────────────────────────────────────
NOTIFY = {
    "startup_ready":     "HIGH_STARTUP_01_mat_than_san_sang.mp3",
    "startup_booting":   "MID_STARTUP_02_dang_khoi_dong.mp3",
    "startup_camera":    "MID_STARTUP_03_cho_ket_noi_camera.mp3",
    "startup_cam_ok":    "HIGH_STARTUP_04_camera_san_sang.mp3",
    "startup_net_ok":    "LOW_STARTUP_05_lay_net_thanh_cong.mp3",
    "switch_on":         "HIGH_SWITCH_47_he_thong_da_bat.mp3",
    "switch_off":        "MID_SWITCH_48_he_thong_da_tat.mp3",
    "user_ready":        "MID_USER_43_san_sang_dua_vat_the.mp3",
    "user_hold":         "MID_USER_44_giu_on_dinh.mp3",
    "image_processing":  "LOW_IMAGE_10_dang_xu_ly_anh.mp3",
    "image_done":        "LOW_IMAGE_11_xu_ly_thanh_cong.mp3",
    "infer_running":     "LOW_INFERENCE_14_dang_phan_loai.mp3",
    "infer_done":        "LOW_INFERENCE_15_phan_loai_thanh_cong.mp3",
    "infer_slow":        "MID_INFERENCE_16_xu_ly_qua_lau.mp3",
    "result_organic":    "HIGH_RESULT_17_rac_huu_co.mp3",
    "result_inorganic":  "HIGH_RESULT_18_rac_vo_co.mp3",
    "result_other":      "HIGH_RESULT_19_rac_khac_loai.mp3",
    "result_uncertain":  "MID_RESULT_20_khong_chac_chan.mp3",
    "result_not_waste":  "MID_RESULT_21_khong_phai_rac.mp3",
    "cam_not_found":     "CRIT_CAMERA_06_khong_tim_camera.mp3",
    "cam_error":         "CRIT_CAMERA_07_loi_camera_chup_anh.mp3",
    "cam_dark":          "MID_CAMERA_08_anh_sang_toi_qua.mp3",
    "cam_no_object":     "MID_CAMERA_09_khong_tim_vat_the.mp3",
    "model_not_found":   "CRIT_IMAGE_12_mo_hinh_khong_tim.mp3",
    "model_error":       "CRIT_IMAGE_13_mo_hinh_bi_loi.mp3",
    "tflite_missing":    "CRIT_HEALTH_42_tflite_chua_cai.mp3",
    "health_ok":         "HIGH_HEALTH_37_thiet_bi_khoe_manh.mp3",
    "health_warning":    "MID_HEALTH_38_co_loi_nho.mp3",
    "health_critical":   "CRIT_HEALTH_39_loi_nghiem_trong.mp3",
    "memory_full":       "HIGH_HEALTH_40_bo_nho_day.mp3",
    "overheat":          "HIGH_HEALTH_41_qua_nong.mp3",
}

# ── Result → notify key map ───────────────────────────────────
RESULT_NOTIFY = {
    "organic":   "result_organic",
    "inorganic": "result_inorganic",
    "other":     "result_other",
}
```

= Đọc GPIO, điều khiển công tắc (switch.py) (chạy trên Pi Zero 2W)
```python
#!/usr/bin/env python3
"""
AI Green Eye - Toggle Switch
  - COM  → GND
  - ON   → GPIO17
  - OFF  → GPIO4
"""

import logging

logger = logging.getLogger(__name__)

SWITCH_ON_PIN  = 17
SWITCH_OFF_PIN = 4

try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False
    logger.warning("RPi.GPIO không khả dụng - switch sẽ luôn ở trạng thái ON")


def setup():
    if not GPIO_AVAILABLE:
        return
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(SWITCH_ON_PIN,  GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(SWITCH_OFF_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    logger.info("Switch GPIO setup: ON=GPIO%d, OFF=GPIO%d", SWITCH_ON_PIN, SWITCH_OFF_PIN)


def is_on() -> bool:
    if not GPIO_AVAILABLE:
        return True
    return GPIO.input(SWITCH_ON_PIN) == GPIO.LOW


def is_off() -> bool:
    if not GPIO_AVAILABLE:
        return False
    return GPIO.input(SWITCH_OFF_PIN) == GPIO.LOW


def cleanup():
    if GPIO_AVAILABLE:
        GPIO.cleanup()
```

= Điều khiển camera, chụp ảnh (camera.py) (chạy trên Pi Zero 2W)
```python
#!/usr/bin/env python3
"""
AI Green Eye - Camera
Chụp ảnh bằng rpicam-jpeg.
"""

import subprocess
import logging
import time
from pathlib import Path

from config import (
    CAPTURE_PATH,
    CAMERA_WIDTH,
    CAMERA_HEIGHT,
    CAMERA_WARMUP,
)

logger = logging.getLogger(__name__)


def warmup():
    time.sleep(CAMERA_WARMUP)


def capture() -> bool:
    try:
        result = subprocess.run(
            [
                "rpicam-jpeg",
                "--output", str(CAPTURE_PATH),
                "--width", str(CAMERA_WIDTH),
                "--height", str(CAMERA_HEIGHT),
                "--timeout", "500",
                "--nopreview",
            ],
            capture_output=True,
            timeout=10,
        )
        if result.returncode != 0:
            logger.error(f"rpicam-jpeg lỗi: {result.stderr.decode()}")
            return False
        if not CAPTURE_PATH.exists() or CAPTURE_PATH.stat().st_size == 0:
            logger.error("File ảnh không tồn tại hoặc rỗng.")
            return False
        return True
    except FileNotFoundError:
        logger.error("rpicam-jpeg không tìm thấy.")
        return False
    except subprocess.TimeoutExpired:
        logger.error("rpicam-jpeg timeout.")
        return False
    except Exception as e:
        logger.error(f"Lỗi camera: {e}")
        return False


def is_too_dark(threshold: int = 40) -> bool:
    try:
        from PIL import Image
        import numpy as np
        img = Image.open(CAPTURE_PATH).convert("L")
        mean = float(np.array(img).mean())
        logger.debug(f"Độ sáng trung bình: {mean:.1f}")
        return mean < threshold
    except Exception as e:
        logger.warning(f"Không kiểm tra được độ sáng: {e}")
        return False


def check_camera() -> bool:
    try:
        result = subprocess.run(
            ["rpicam-hello", "--timeout", "1000", "--nopreview"],
            capture_output=True,
            timeout=5,
        )
        return result.returncode == 0
    except Exception:
        return False


def stop():
    try:
        subprocess.run(
            ["killall", "rpicam-hello", "rpicam-jpeg"],
            capture_output=True,
            timeout=3,
        )
        logger.info("Camera đã dừng")
    except Exception as e:
        logger.debug(f"stop(): {e}")
```
= Xử lý ảnh, chạy AI model (inference.py) (chạy trên Pi Zero 2W)
```python
#!/usr/bin/env python3
"""
AI Green Eye - Inference
Chạy TFLite model phân loại rác.
"""

import logging
import numpy as np
from pathlib import Path
from PIL import Image

from config import MODEL_PATH, LABELS_PATH, IMAGE_SIZE, CONFIDENCE_THRESHOLD

logger = logging.getLogger(__name__)


def load_model():
    if not MODEL_PATH.exists():
        logger.error(f"Model không tìm thấy: {MODEL_PATH}")
        return None, None, None
    try:
        try:
            from ai_edge_litert.interpreter import Interpreter
            interpreter = Interpreter(model_path=str(MODEL_PATH))
            logger.info("Dùng ai-edge-litert")
        except ImportError:
            import tflite_runtime.interpreter as tflite
            interpreter = tflite.Interpreter(model_path=str(MODEL_PATH))
            logger.info("Dùng tflite-runtime")

        interpreter.allocate_tensors()
        input_details  = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        logger.info(f"Model loaded: input={input_details[0]['shape']} dtype={input_details[0]['dtype']}")
        return interpreter, input_details, output_details
    except Exception as e:
        logger.error(f"Lỗi load model: {e}")
        return None, None, None


def load_labels() -> list:
    if not LABELS_PATH.exists():
        logger.error(f"Labels không tìm thấy: {LABELS_PATH}")
        return []
    with open(LABELS_PATH, "r") as f:
        labels = [line.strip() for line in f if line.strip()]
    return labels


def preprocess(image_path: Path, input_dtype) -> np.ndarray:
    img = Image.open(image_path).convert("RGB")
    img = img.resize(IMAGE_SIZE)
    x = np.array(img, dtype=np.float32) / 255.0
    if input_dtype == np.int8:
        x = (x * 127).astype(np.int8)
    elif input_dtype == np.uint8:
        x = (x * 255).astype(np.uint8)
    return np.expand_dims(x, axis=0)


def run(interpreter, input_details, output_details, labels: list) -> dict:
    from config import CAPTURE_PATH
    if interpreter is None:
        return None
    try:
        x = preprocess(CAPTURE_PATH, input_details[0]["dtype"])
        interpreter.set_tensor(input_details[0]["index"], x)
        interpreter.invoke()
        output = interpreter.get_tensor(output_details[0]["index"])
        if output_details[0]["dtype"] == np.int8:
            scale, zero_point = output_details[0]["quantization"]
            output = (output.astype(np.float32) - zero_point) * scale
        e = np.exp(output[0] - np.max(output[0]))
        probs = e / e.sum()
        idx        = int(np.argmax(probs))
        confidence = float(probs[idx])
        label      = labels[idx] if idx < len(labels) else "unknown"
        logger.info(
            "Probs: %s -> %s (%.1f%%)",
            {labels[i]: f"{probs[i]:.3f}" for i in range(len(labels))},
            label,
            confidence * 100,
        )
        return {
            "class":      label,
            "confidence": confidence,
            "uncertain":  confidence < CONFIDENCE_THRESHOLD,
            "all_probs":  {labels[i]: float(probs[i]) for i in range(len(labels))},
        }
    except Exception as e:
        logger.error(f"Lỗi inference: {e}")
        return None
```
= Điều khiển toàn bộ hệ thống (main.py) (chạy trên Pi Zero 2W)
```python
#!/usr/bin/env python3
"""
AI Green Eye - Main
Toggle switch:
  - ON  (GPIO17 LOW): hoạt động ngay
  - Không ON: hoàn thành vòng lặp hiện tại rồi mới dừng
"""

import time
import logging
import signal
import sys

import audio
import camera
import inference
import motion
import switch
from config import COOLDOWN_SECONDS, RESULT_NOTIFY

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("main")

RETRY_DELAY = 5


def handle_shutdown(signum, frame):
    logger.info("Nhận signal tắt, dừng hệ thống.")
    audio.stop()
    try:
        camera.stop()
    except Exception:
        pass
    switch.cleanup()
    sys.exit(0)


signal.signal(signal.SIGINT, handle_shutdown)
signal.signal(signal.SIGTERM, handle_shutdown)


def init_camera() -> bool:
    audio.play("startup_camera", block=True)
    while True:
        if camera.check_camera():
            audio.play("startup_cam_ok", block=True)
            camera.warmup()
            return True
        logger.error("Camera lỗi, thử lại sau %ds", RETRY_DELAY)
        audio.play("cam_not_found", block=True)
        time.sleep(RETRY_DELAY)


def init_model():
    while True:
        interpreter, input_details, output_details = inference.load_model()
        if interpreter is None:
            logger.error("Model lỗi, thử lại sau %ds", RETRY_DELAY)
            audio.play("model_not_found", block=True)
            time.sleep(RETRY_DELAY)
            continue
        labels = inference.load_labels()
        if not labels:
            logger.error("Labels lỗi, thử lại sau %ds", RETRY_DELAY)
            audio.play("model_error", block=True)
            time.sleep(RETRY_DELAY)
            continue
        logger.info("Model loaded: classes=%s", labels)
        return interpreter, input_details, output_details, labels


def process_one(interpreter, input_details, output_details, labels):
    audio.play("image_processing")
    if not camera.capture():
        logger.error("Chụp ảnh thất bại")
        audio.play("cam_error", block=True)
        return
    if camera.is_too_dark():
        logger.warning("Ảnh quá tối")
        audio.play("cam_dark", block=True)
        return
    audio.play("infer_running")
    start = time.time()
    result = inference.run(interpreter, input_details, output_details, labels)
    elapsed = time.time() - start
    if result is None:
        logger.error("Inference thất bại")
        audio.play("model_error", block=True)
        return
    logger.info(
        "Kết quả: %s  (%.1f%%)  %.0fms",
        result["class"],
        result["confidence"] * 100,
        elapsed * 1000,
    )
    if elapsed > 5.0:
        audio.play("infer_slow")
        time.sleep(1.5)
    if result["uncertain"]:
        logger.info("Confidence thấp -> không chắc chắn")
        audio.play("result_uncertain", block=True)
        return
    notify_key = RESULT_NOTIFY.get(result["class"], "result_uncertain")
    audio.play(notify_key, block=True)


def main():
    logger.info("===== AI GREEN EYE - KHỞI ĐỘNG =====")
    audio.play("startup_booting", block=True)
    switch.setup()
    init_camera()
    interpreter, input_details, output_details, labels = init_model()
    audio.play("startup_ready", block=True)

    if switch.is_on():
        logger.info("Khởi động: công tắc ON")
        audio.play("switch_on", block=True)
        audio.play("user_ready", block=True)
        last_switch_state = "on"
    else:
        logger.info("Khởi động: công tắc OFF - chờ bật")
        audio.play("switch_off", block=True)
        last_switch_state = "off"

    detector = motion.MotionDetector()
    logger.info("Bắt đầu vòng lặp (cooldown=%ds)", COOLDOWN_SECONDS)

    while True:
        try:
            if last_switch_state == "off":
                if switch.is_on():
                    logger.info("Công tắc ON - khởi động lại")
                    audio.play("switch_on", block=True)
                    camera.warmup()
                    audio.play("startup_cam_ok", block=True)
                    audio.play("user_ready", block=True)
                    last_switch_state = "on"
                    detector = motion.MotionDetector()
                else:
                    time.sleep(0.5)
                continue

            if detector.check():
                logger.info("Phát hiện chuyển động")
                process_one(interpreter, input_details, output_details, labels)
            else:
                time.sleep(0.3)

            if not switch.is_on():
                logger.info("Công tắc OFF - hoàn thành vòng lặp, dừng")
                audio.play("switch_off", block=True)
                try:
                    camera.stop()
                    logger.info("Camera đã tắt")
                except Exception as e:
                    logger.warning("Lỗi tắt camera: %s", e)
                last_switch_state = "off"

        except KeyboardInterrupt:
            handle_shutdown(None, None)

        except Exception as e:
            logger.exception("Lỗi vòng lặp: %s", e)
            audio.play("health_warning", block=True)
            time.sleep(RETRY_DELAY)


if __name__ == "__main__":
    main()
```
= Cấu hình trên Pi 2W (systemd service) (airgreeneye.service) để tự động chạy khi bật máy

Bước 1: Tạo file airgreeneye.service  trong thư mục /etc/systemd/system/ (bằng lệnh ```bash sudo nano /etc/systemd/system/airgreeneye.service ```) với nội dung sau:


```ini
[Unit]
Description=AI Green Eye
After=network.target

[Service]
Type=simple
User=hieunga
WorkingDirectory=/home/hieunga/airgreeneye
ExecStart=/home/hieunga/airgreeneye/venv/bin/python3 main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Bước 2: Kích hoạt service để tự động chạy khi bật máy bằng cách chạy lần lượt các lệnh sau:
```bash
sudo systemctl daemon-reload
sudo systemctl enable airgreeneye
sudo systemctl start airgreeneye
```

Bước 3: Kiểm tra trạng thái của service bằng lệnh:
```bash 
sudo systemctl status airgreeneye
```

#pagebreak()
// ============================================================
// Chữ ký
// ============================================================
#grid(
  columns: (1fr, 1fr),
  [],[
  #set par(leading: 13pt * 0.3)
  #align(center)[
    #text(style: "italic")[TP. HCM, ngày 15 tháng 04 năm 2026]

    #text(style: "italic")[*Tác giả hoặc đại diện nhóm tác giả*]

    #text(style: "italic")[(Ký, ghi rõ họ tên)]
    
    
    // #image("ckHieu.png", fit: "contain")
    ]
  ]

)