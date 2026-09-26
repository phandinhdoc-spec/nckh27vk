#import "@preview/cetz:0.3.4" as cetz: canvas, draw

#set page(
  paper: "a4",
  margin: (left: 3cm, right: 2cm, top: 2cm, bottom: 2cm),
  // header: context {
  //   if counter(page).get().first() > 1 {
  //     align(center)[
  //       #text(size: 10pt, weight: "bold")[CUỘC THI NGHIÊN CỨU KHOA HỌC]\
  //       #text(size: 9pt)[LẦN THỨ 22 NĂM 2026]
  //       #v(-4pt)
  //       #line(length: 100%, stroke: 0.5pt)
  //     ]
  //   }
  // },
  footer: context {
    if counter(page).get().first() > 1 {
      align(center)[#text(size: 10pt)[#counter(page).display()]]
    }
  },
)

#set text(font: "Times New Roman", size: 14pt, lang: "vi", region: "VN")
#let ten-du-an = [Thiết bị thông minh sử dụng AI hỗ trợ người khiếm thị]
#set par(justify: true, leading: 0.6em, spacing: 0.6em, first-line-indent: (amount: 8mm, all: true))

#set list(indent: 8mm, body-indent: 0.6em, spacing: 0.6em, marker: ([-], [+]))
#show list.item: it => [
  #set par(first-line-indent: 0mm, hanging-indent: -16mm)
  #it
]
#set enum(indent: 8mm, body-indent: 0.6em, spacing: 0.6em)
#show enum.item: it => [
  #set par(first-line-indent: 0mm, hanging-indent: -16mm)
  #it
]
// Tham khảo ~/TypstLib/local/vn-edu/0.1.0/vn-pages.typ (hàm vn-pages):
// chép ý tưởng set/show vào trực tiếp file này, KHÔNG import @local.
// Quy định báo cáo NCKH yêu cầu Times New Roman 14pt nên nâng từ 13pt của mẫu;
// scheme đánh số dùng A / 1 / 1.1 theo văn bản báo cáo (mẫu dùng I / 1 / 1.1).
#set heading(numbering: (..nums) => {
  if nums.len() == 1 {
    numbering("A. ", nums.at(0))
  } else if nums.len() == 2 {
    numbering("1. ", nums.at(1))
  } else if nums.len() == 3 {
    numbering("1.1. ", nums.at(1), nums.at(2))
  }
})

#show heading.where(level: 1): it => {
  v(0.6em, weak: true)
  block(width: 100%)[
    #set text(font: "Times New Roman", size: 14pt, lang: "vi", region: "VN")
    #align(left)[#text(weight: "bold")[#counter(heading).display(it.numbering) #h(0.2em) #it.body]]
  ]
  v(0.6em, weak: true)
}
#show heading.where(level: 2): it => {
  v(0.6em, weak: true)
  block(width: 100%)[
    #set text(font: "Times New Roman", size: 14pt, lang: "vi", region: "VN")
    #h(8mm)
    #text(weight: "bold")[#counter(heading).display(it.numbering) #h(0.2em) #it.body]
  ]
  v(0.6em, weak: true)
}
#show heading.where(level: 3): it => {
  v(0.6em, weak: true)
  block(width: 100%)[
    #set text(font: "Times New Roman", size: 14pt, lang: "vi", region: "VN", style: "italic")
    #h(8mm)
    #text(weight: "bold")[#counter(heading).display(it.numbering) #h(0.2em) #it.body]
  ]
  v(0.6em, weak: true)
}

#let title(body) = align(center)[#text(size: 14pt, weight: "bold")[#body]]
#let fig-caption(body) = align(center)[#v(4pt)#text(weight: "bold", style: "italic", size: 14pt)[#body]]

#show figure.where(kind: image): set figure(supplement: [Hình])
#show figure.where(kind: table): set figure(supplement: [Bảng])
#show figure.caption: it => [
  #v(4pt)
  #text(weight: "bold", style: "italic", size: 11pt)[
    #it.supplement #context it.counter.display(it.numbering). #it.body
  ]
]


== Nghiên cứu thuật toán đo khoảng cách giữa người khiếm thị và vật cản trên đường

- Vì các sản phẩm tương tự đã có bán, nên rất có thể đã có thuật toán tính khoảng cách giữa 2 vật thể, nhưng chúng em không tìm thấy nó trên google search và chatgpt. Vì vậy, chúng em nghiên cứu tỉ lệ khoảng cách giữa 2 vật trong thực tế và khoảng cách 2 điểm ảnh tương ứng trên ảnh. Khi đã có tỉ lệ này.


*Trước tiên chúng em tìm hiểu cách tạo ảnh bởi camera, đồng thời góc của camera khi chụp ảnh phù hợp với dự án. *

- Ảnh được chụp bằng camera nhưng hướng xuống dưới, vì người khiếm thị có thói quen là ít khi cúi đầu xuống. Do đó, góc nhìn của camera cần đảm bảo thu được hình ảnh vật cản khi đi đường, thu được hình ảnh các vật ở tầm xa và gần.

- Khi chụp ảnh, theo nguyên lý tạo ảnh qua thấu kính hội tụ:
  - Hình ảnh 3D thực tế được thu lại thành hình ảnh 2D trên cảm biến camera.
  - Khoảng cách từ vật đến thấu kính, tiêu cự và vị trí ảnh liên hệ với nhau.
  - Tỉ lệ giữa kích thước thực tế và ảnh giống như tỉ lệ giữa khoảng cách thực tế và trên bản đồ (tỉ lệ bản đồ). thuật toán dưới đây đi tìm tỉ lệ này, để từ khoảng cách giữa các điểm ảnh suy ra khoảng cách thực tế.

*Sau đó chúng em nghiên cứu kiến thức nền và tìm ra công thức như sau: *

Với camera có góc nhìn $70^0$, cài đặt chất lượng ảnh là 640 x 640, với khoảng cách $d_1$ được đo từ cảm biến GY53L1X, góc nghiêng giữa mặt camera và phương thẳng đứng là $alpha$ (được đo bởi cảm biến GY-52), khoảng cách giữa hai vật trong thực tế là $d$ thì ta có công thức:


#align(center)[
  #block(
    stroke: 1pt + rgb("a0a0a0"),
    inset: 15pt,
    radius: 4pt,
    fill: rgb("#edf5e1"),
    [
      $ d_1 / d = 320 / (L cos(alpha - 35^0) sin(35^0)) $
    ],
  )
]

* Chứng minh *:
#figure(
  image("so-do-khoang-cach-camera.svg", width: 100%),
  caption: [Sơ đồ minh họa thuật toán đo khoảng cách vật cản.],
  numbering: _ => "4.0",
)

Hình trên: Camera đặt tại O, trục chính OG, vì camera có giới hạn góc nhìn, giả sử là $70^0$ nên chỉ nhìn thấy từ N đến M, H là chân người khiếm thị, T là vật cản (chân vật cản trên đường). Sử dụng nguyên tắc tạo ảnh của thấu kính hội tụ, ta đưa ảnh của các điểm trên đường vào mặt phẳng Nx đi qua N và vuông góc với OG.

Trước tiên ta đi tìm tỉ lệ giữa 2 điểm ảnh trên ảnh (G" và N") với khoảng cách G'N.

Khi chụp hình, chúng em quy định ảnh được chuyển về tỉ lệ 640 × 640 pixel, đủ để phân biệt vật thể hơn nữa dung lượng nhỏ dễ truyền qua mạng. Vì G" nằm ở trung tâm của ảnh nên nó có tọa độ (320, 320). Tọa độ của N" là (640, 320) nên khoảng cách điểm ảnh là $d_1 =320$ pixel.

// Câu cũ: OG được đo bằng cảm biến GY53-L1-X với độ chính xác khi đo khoảng cách từ 2cm đến 2,5cm tùy điều kiện ánh sáng. Góc nghiêng $alpha$ của camera được đo bằng cảm biến GY-52, biến thể của MPU6050 chuyên dùng đo các góc nghiêng với độ chính xác rất cao.
OG được đo bằng cảm biến GY53L1X (là cảm biến VL53L1X ghép với vi điều khiển STM32) chuyên đo khoảng cách, đo được từ 5 cm đến 4 m với độ chính xác khoảng 2 cm đến 2,5 cm tùy điều kiện ánh sáng. Góc nghiêng $alpha$ của camera được đo bằng cảm biến GY25 (phát triển từ MPU6050), đo được ba góc roll, pitch, yaw với độ chính xác rất cao. Đặt $L = O G$

Ta có: $O H = L cos (alpha)$

$hat(N O G) = alpha - 35^0$ suy ra tính được $H N = O H tan(alpha - 35^0)$, tương tự ta tính được $H G, H M, N G, O N, O M$ bằng Pytago hoặc lượng giác. $ O N = O H cos(alpha - 35^0) = L cos(alpha) cos(alpha - 35^0) $

Nên ta tính được $d_2 = N G' = O N sin (35^0)$

Vậy ta đã tìm được tỉ lệ điểm ảnh và tỉ lệ thực tế trên mặt phẳng chứa Nx là $d_1 : d_2 = 320 / (O N sin (35^0))$

Từ đó ta tìm tỉ lệ giữa "ảnh" trên mặt Nx và khoảng cách thực tế.

Đặt $d = N G$ ta có $d_2 / d = (N G')/(N G) = cos (alpha)$ Vì $hat(T N x) = hat(H O G)$ (hai góc có cạnh tương ứng vuông góc)

Vậy tỉ lệ điểm ảnh và tỉ lệ thực tế giữa các điểm nằm trên mặt đường là:

$
  d_1 / d = d_1 / d_2 . d_2 / d = 320 / (O N sin (35^0)) . cos (alpha) = 320 / (L cos(alpha) cos(alpha - 35^0) sin (35^0)) . cos (alpha)
$

$ d_1 / d = 320 / (L cos(alpha - 35^0) sin(35^0)) $

Trên đây là thuật toán xác định khoảng cách giữa hai vật trong thực tế khi biết khoảng cách giữa hai điểm ảnh trong ảnh chụp, mà khoảng cách giữa hai điểm ảnh được xác định bằng thuật toán nhận diện vật thể (object detection) trong mô hình AI, thuật toán này khá phổ biến với độ chính xác rất cao.

