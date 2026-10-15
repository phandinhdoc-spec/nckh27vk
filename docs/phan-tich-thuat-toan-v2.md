# Phân tích thuật toán xác định vị trí vật cản — NCKH27VK

Ngày phân tích: 10/10/2026.

Nguồn chính: **BÁO CÁO_CÔ THÙY-KHKT-VÒNG ĐEO DÒ ĐƯỜNG CHO NGƯỜI KHIẾM THỊ v2.pdf**, tập trung vào mục D.5, D.6 và D.7. Các trang được nhắc dưới đây là số thứ tự trang PDF, vì số trang in trong tài liệu bị lặp.

Đối chiếu mã nguồn tại commit [8fa9e9303629f764952c9a1447d19fc66ff4c08c](https://github.com/phandinhdoc-spec/nckh27vk/tree/8fa9e9303629f764952c9a1447d19fc66ff4c08c). Đây là phân tích tài liệu và mã nguồn, không phải báo cáo đã chạy thử trên phần cứng. Các ví dụ tính toán trong bản phân tích này là ví dụ lý thuyết, không phải số liệu thực nghiệm.

## 1. Nhận định chính

**Ý tưởng hình học có cơ sở đúng:** khi biết độ cao camera, hướng camera, thông số nội tại và tọa độ ảnh của một điểm thực sự nằm trên mặt đường phẳng, có thể tính vị trí điểm đó bằng giao của tia nhìn với mặt đường.

Cách tính khoảng cách bằng tam giác vuông và cách suy ra độ lệch ngang bằng tam giác đồng dạng trong báo cáo có thể đưa về một bộ công thức nhất quán. Không cần loại bỏ nền tảng này.

Tuy nhiên, bản hiện tại còn bốn vấn đề lớn:

1. Trộn tọa độ pixel với tọa độ chuẩn hóa khi bù roll, khiến hướng dẫn thay số có thể sai đơn vị.
2. Chưa xác định đủ điều kiện để dùng GY53 đo độ cao camera thông qua khoảng cách tới mặt đường.
3. Chưa chứng minh chất lượng định vị chân vật cản, đồng bộ ảnh–góc và khả năng cảnh báo khi người dùng đang đi.
4. Kết quả mô phỏng, thử nghiệm thực tế và các bảng còn trống chưa được tách bạch; chưa đủ căn cứ xác nhận độ chính xác 2,7% hay khả năng cảnh báo an toàn.

## 2. Bản chất của bài toán

Một điểm ảnh chỉ xác định **hướng nhìn**, không tự xác định khoảng cách. Có nhiều điểm ở các khoảng cách khác nhau nằm trên cùng tia nhìn và cho cùng vị trí ảnh.

Bài toán có nghiệm xác định vì thêm các điều kiện:

- Điểm cần tìm nằm trên mặt đường đã biết.
- Camera có độ cao xác định so với mặt đường.
- Biết hướng tia nhìn sau khi hiệu chỉnh tư thế camera.

Vì thế, nên mô tả phương pháp là:

> Ước lượng vị trí điểm tiếp xúc vật cản–mặt đường từ ảnh đơn, dựa trên mô hình camera phối cảnh và tư thế camera.

Không nên hiểu đây là phương pháp khôi phục khoảng cách đến mọi điểm trong ảnh.

AI có nhiệm vụ phát hiện vật và điểm tiếp xúc. Phần hình học chuyển điểm ảnh đó thành vị trí theo mét. Nếu AI chọn sai điểm, công thức hình học vẫn có thể trả về một con số trông hợp lý nhưng sai.

## 3. Bộ công thức thống nhất

### 3.1. Quy ước

| Ký hiệu | Ý nghĩa | Đơn vị |
|---|---|---|
| $u,v$ | Tọa độ điểm ảnh, gốc ở góc trái trên; $u$ sang phải, $v$ xuống dưới | pixel |
| $c_x,c_y$ | Tọa độ điểm chính của camera trong ảnh đang xử lý | pixel |
| $f_x,f_y$ | Tiêu cự theo hai trục ảnh | pixel |
| $a,b$ | Tọa độ ảnh chuẩn hóa | Không có đơn vị |
| $\theta$ | Góc chúc xuống của trục quang học so với phương ngang | radian khi tính bằng chương trình |
| $\varphi$ | Góc roll theo quy ước hình học được xác định bên dưới | radian |
| $h$ | Độ cao tâm camera so với mặt đường | mét |
| $X$ | Khoảng cách về phía trước theo hướng ngang của camera | mét |
| $Y$ | Độ lệch sang phải; bên trái mang dấu âm | mét |
| $D$ | Khoảng cách trên mặt đường từ chân đường vuông góc của camera đến điểm cần tìm | mét |

Lưu ý: “phía trước camera” chưa chắc là “hướng người đang đi” nếu người dùng quay đầu.

Điểm ảnh dùng trong công thức cần được xử lý méo kính theo thông số hiệu chuẩn. Để diễn giải đơn giản, dưới đây coi $u,v$ là tọa độ đã hiệu chỉnh phù hợp với bộ thông số nội tại đang dùng.

### 3.2. Chuẩn hóa điểm ảnh

$$
a=\frac{u-c_x}{f_x},\qquad b=\frac{v-c_y}{f_y}.
$$

Với giả thiết lý tưởng của báo cáo:

$$
c_x=c_y=319{,}5,\qquad f_x=f_y\approx836.
$$

Đây là giá trị ban đầu theo mô hình và cách cắt ảnh, không thay thế hiệu chuẩn camera thực tế.

### 3.3. Bù roll

Theo quy ước trục ảnh bị quay một góc $\varphi$ như hình 5.4:

$$
a_r=a\cos\varphi-b\sin\varphi,
$$

$$
b_r=a\sin\varphi+b\cos\varphi.
$$

Đây là phép đổi tọa độ của tia nhìn từ trục camera đang nghiêng sang trục ảnh đã cân bằng roll.

Công thức chỉ dùng trực tiếp khi góc roll của cảm biến đã được đổi sang đúng quy ước này. Cần xác định trục lắp đặt, dấu góc, góc lệch giữa IMU và camera và thứ tự quay. Không thể mặc định mọi giá trị có tên “roll” đều có cùng ý nghĩa.

### 3.4. Tính vị trí trên mặt đường

Đặt:

$$
k=\sin\theta+b_r\cos\theta.
$$

Khi tia nhìn hướng xuống và giao mặt đường phía trước camera:

$$
\boxed{X=h\frac{\cos\theta-b_r\sin\theta}{k}}
$$

$$
\boxed{Y=h\frac{a_r}{k}}
$$

$$
\boxed{D=\sqrt{X^2+Y^2}}
$$

Khoảng cách xiên từ tâm camera đến điểm vật cản là đại lượng khác:

$$
L=\sqrt{h^2+X^2+Y^2}.
$$

Không được dùng lẫn $X$, $D$ và $L$.

### 3.5. Chứng minh bằng lượng giác và đồng dạng

Trong mặt phẳng đứng chứa trục quang học sau khi cân bằng roll, đặt:

$$
\beta=\arctan b_r,\qquad \gamma=\theta+\beta.
$$

Với điểm ở phía trước và dưới camera:

$$
X=\frac{h}{\tan\gamma}.
$$

Do:

$$
\tan(\theta+\beta)
=\frac{\sin\theta+b_r\cos\theta}
{\cos\theta-b_r\sin\theta},
$$

suy ra công thức $X$ ở trên.

Nếu $P''$ là hình chiếu của điểm $P$ lên mặt phẳng đứng đó, thì:

$$
OP''=\frac{h}{\sin(\theta+\beta)}.
$$

Tam giác đồng dạng cho:

$$
Y=OP''\frac{a_r}{\sqrt{1+b_r^2}}.
$$

Mặt khác:

$$
\sin(\theta+\beta)
=\frac{\sin\theta+b_r\cos\theta}{\sqrt{1+b_r^2}},
$$

nên:

$$
Y=\frac{h\,a_r}{\sin\theta+b_r\cos\theta}.
$$

Như vậy, cách suy luận bằng tam giác đồng dạng của báo cáo phù hợp với bộ công thức này khi các ký hiệu và đơn vị được thống nhất.

**Điểm cần sửa trong cách định nghĩa góc:** với vật lệch sang bên, $\gamma$ ở công thức $X=h/\tan\gamma$ là góc hạ của tia chiếu $OP''$ trong mặt phẳng đứng. Nếu dùng góc hạ của chính tia $OP$ so với mặt phẳng ngang thì kết quả $h/\tan\gamma$ là $D$, không phải $X$.

### 3.6. Điều kiện loại kết quả

- $k\leq0$: tia nằm ngang hoặc hướng lên, không có giao mặt đường hữu hạn phía trước theo mô hình này.
- $k$ dương nhưng quá nhỏ: kết quả rất nhạy với sai số; cần từ chối hoặc đánh dấu độ tin cậy thấp.
- $X\leq0$: giao điểm không nằm phía trước theo trục đã chọn.
- Không thấy điểm tiếp xúc, điểm bị che khuất hoặc mặt đường không phù hợp mô hình: không suy ra khoảng cách như một phép đo hợp lệ.
- Dữ liệu góc quá cũ, mất cảm biến hoặc ảnh không đúng cấu hình hiệu chuẩn: không dùng kết quả.
- Ngoài khoảng đã kiểm chứng: báo ngoài miền tin cậy, không ép giá trị về 2 m hoặc 10 m.

Ngưỡng $k$ tối thiểu cần dựa trên sai số đầu vào và cự ly cho phép, không chọn tùy ý.

## 4. Các điểm đúng và các lỗi cần sửa trong báo cáo

### 4.1. Đổi tiêu cự sang pixel: đúng có điều kiện

Phép tính:

$$
f_{\mathrm{px}}=\frac{4{,}74}{0{,}0014}\frac{640}{2592}
\approx835{,}98
$$

đúng nếu đúng camera, đúng bước điểm ảnh, ảnh gốc đúng chế độ đã mô tả, cắt giữa về $2592\times2592$, rồi thu đều về $640\times640$.

Thông số 4608 × 2592 và tiêu cự 4,74 mm phù hợp với Camera Module 3 bản tiêu chuẩn trong tài liệu Raspberry Pi [1]. Cần kiểm tra camera đang lắp thực sự là loại đó; không áp dụng các giá trị này cho module khác.

Chỉ đặt đầu ra 640 × 640 chưa chứng minh quy trình cắt ảnh giống giả thiết. Kéo méo toàn bộ ảnh chữ nhật, cắt giữa hoặc thêm viền cho ra ánh xạ pixel khác nhau.

Theo mô hình OpenCV, cần xác định $f_x,f_y,c_x,c_y$ và méo kính; khi đổi kích thước ảnh phải đổi các thông số nội tại tương ứng [2].

### 4.2. Mặt phẳng ảnh đi qua tiêu điểm: là xấp xỉ

Ví dụ dùng công thức thấu kính, vật cách 2 m cho khoảng ảnh khoảng 4,7513 mm với tiêu cự 4,74 mm, là xấp xỉ hợp lý.

Tuy nhiên, nên viết rõ đây là **mô hình camera lý tưởng hóa**. Không nên suy luận rằng toàn bộ ảnh quang học thực của các vật ở mọi khoảng cách đều nằm chính xác tại tiêu diện.

Đối với thuật toán, có thể dùng mặt phẳng ảnh quy ước ở khoảng cách tiêu cự hiệu dụng và bộ thông số hiệu chuẩn. Cách trình bày này tránh nhầm mặt phẳng toán học với vị trí ảnh nét thực tế của từng vật.

### 4.3. Trộn pixel và tọa độ chuẩn hóa: cần sửa trước khi lập trình

Ở trang PDF 14, báo cáo định nghĩa:

$$
x_n=\frac{u-319{,}5}{f_{\mathrm{px}}},
\qquad
y_n=\frac{v-319{,}5}{f_{\mathrm{px}}}.
$$

Hai số này không có đơn vị.

Ở trang PDF 16, $x',y'$ được tính từ $x_n,y_n$, nên cũng không có đơn vị. Nhưng tài liệu hướng dẫn thay chúng vào vị trí $x,y$ của công thức trước đó chứa:

$$
\sqrt{f_{\mathrm{px}}^2+y^2}.
$$

Nếu làm theo trực tiếp, sẽ cộng bình phương một đại lượng pixel với bình phương một đại lượng không có đơn vị.

Có hai cách sửa hợp lệ:

1. Quay tọa độ lệch tâm **theo pixel**, rồi dùng công thức có $f_{\mathrm{px}}$; cách này cần lưu ý khi $f_x\ne f_y$.
2. Chuẩn hóa trước, quay $a,b$ và dùng nhất quán công thức ở mục 3.

Cách thứ hai phù hợp hơn để triển khai và tránh nhầm ký hiệu.

### 4.4. Định nghĩa $X=HP$ không đúng với vật lệch ngang

Ở phần mở đầu mô hình, báo cáo gắn $X$ với $HP$. Nhưng nếu $P$ lệch sang bên:

$$
HP=D,\qquad HP''=X,\qquad P''P=|Y|.
$$

Phải thống nhất từ đầu. Đồng thời, độ dài đoạn thẳng luôn không âm, còn tọa độ $Y$ cần có dấu để phân biệt trái và phải.

### 4.5. Bỏ qua roll vẫn gây sai số cho vật giữa ảnh

Báo cáo nói vật có $x_n=0$ thì gần như không sai khi bỏ qua roll. Chính xác hơn:

$$
b_r-b=a\sin\varphi+b(\cos\varphi-1).
$$

Khi $a=0$, vẫn còn:

$$
b_r-b=b(\cos\varphi-1).
$$

Sai số không triệt tiêu, trừ những trường hợp đặc biệt. Nó thường nhỏ hơn thành phần bậc nhất khi góc nhỏ, nhưng ở khoảng cách xa hoặc roll lớn vẫn cần tính đến.

## 5. Vai trò của GY53 trong việc xác định độ cao

Báo cáo dùng khoảng cách $OG$ do GY53 đo để suy ra $OH=h$.

Nếu cảm biến đo đúng điểm mặt đất trên trục quang học, có thể viết:

$$
h=OG\sin\theta.
$$

Nhưng cần đồng thời thỏa mãn:

- Tia đo được hiệu chuẩn cùng hướng với trục camera.
- Gốc đo và độ lệch vị trí giữa cảm biến với camera được xử lý.
- Vật phản hồi thực sự là mặt đất.
- Mặt đường phù hợp giả thiết nằm ngang.
- Khoảng cách nằm trong miền đo tin cậy.

VL53L1X có tầm đo tối đa công bố tới 4 m và trường nhìn điển hình 27°; nó không phải một tia hình học có độ rộng bằng không [3].

Theo chính ví dụ của báo cáo:

$$
h=1{,}55\text{ m},\qquad\theta=24^\circ
$$

thì:

$$
OG=\frac{1{,}55}{\sin24^\circ}\approx3{,}81\text{ m}.
$$

Đây đã gần giới hạn 4 m công bố. Khi đầu ngẩng lên, khoảng cách tới mặt đất tăng; khi có vật chắn, cảm biến có thể trả khoảng cách tới vật thay vì mặt đường.

Do đó, chưa thể xem mọi lần đọc GY53 là phép đo độ cao hợp lệ. Có thể dùng độ cao camera được đo ban đầu cho mô hình thử nghiệm; nếu cập nhật bằng cảm biến thì phải có điều kiện xác nhận mặt đất và xử lý dữ liệu không hợp lệ. Độ cao cũng thay đổi khi người dùng cúi hoặc bước đi.

Tầm nhìn hình học tới 10 m không có nghĩa GY53 đo trực tiếp được 10 m.

## 6. Sai số thực tế nằm ở đâu?

### 6.1. Sai số góc và sai số chọn điểm ảnh

Các ví dụ dưới đây được tính với:

$$
h=1{,}55\text{ m},\quad
\theta=24^\circ,\quad
f=836,\quad
\varphi=0,\quad Y=0.
$$

| $X$ thật | Tọa độ $v$ lý tưởng | $X$ nếu chọn điểm thấp hơn 5 pixel | $X$ nếu góc hạ lớn hơn $1^\circ$ |
|---:|---:|---:|---:|
| 2 m | 524,47 | 1,977 m | 1,929 m |
| 5 m | 220,16 | 4,898 m | 4,708 m |
| 10 m | 92,53 | 9,644 m | 8,964 m |

Ở 10 m, chỉ 5 pixel đã tạo sai số khoảng 35,6 cm trong trường hợp này. Sai số góc $1^\circ$ tạo chênh lệch hơn 1 m.

Vì vậy, mục tiêu sai số khoảng 5% ở 10 m cần kiểm chứng cả độ chính xác góc lẫn độ chính xác chân vật. Không thể chỉ kiểm tra cảm biến.

### 6.2. Đồng bộ ảnh và góc

Ảnh và số đo pitch/roll phải đại diện cùng thời điểm. Lấy góc sau khi chụp lúc người dùng đã quay hoặc cúi đầu sẽ đưa tư thế khác vào ảnh cũ.

Cần ghi timestamp chụp, timestamp mẫu IMU, độ lệch thời gian và quy tắc từ chối mẫu quá cũ. Việc đọc cảm biến “trước khi gửi request” chưa tự bảo đảm đồng bộ với lúc phơi sáng.

### 6.3. Sai số độ cao và mặt đường

Với các biến còn lại cố định, $X$ và $Y$ tỉ lệ thuận với $h$:

$$
\frac{\Delta X}{X}=\frac{\Delta h}{h}.
$$

Nếu độ cao giả định 1,55 m lệch 5 cm thì riêng thành phần đó đã tương ứng khoảng 3,23%.

Dốc, bậc thềm, vỉa hè hoặc điểm chân vật nằm cao hơn mặt đường giả định sẽ làm sai điều kiện giao tia–mặt phẳng. Đây không chỉ là nhiễu cảm biến có thể khử bằng lấy trung bình.

### 6.4. Không dùng độ phân tán để thay độ chính xác

Độ lệch quanh trung bình:

$$
\frac1n\sum_{i=1}^n|A_i-\overline A|
$$

phản ánh độ phân tán. Nó không chứng minh phép đo gần giá trị thật.

Ví dụ, vật thật ở 5 m nhưng mọi lần đo đều ra 6 m: độ phân tán bằng 0, sai số thật vẫn là 1 m.

Để đánh giá thuật toán, cần giá trị đối chiếu từ thước hoặc bố trí đã biết:

$$
\mathrm{MAE}=\frac1n\sum_{i=1}^n|\widehat X_i-X_i^{\mathrm{ref}}|,
$$

$$
\mathrm{MAPE}
=\frac{100\%}{n}\sum_{i=1}^n
\frac{|\widehat X_i-X_i^{\mathrm{ref}}|}{X_i^{\mathrm{ref}}}.
$$

Cần thêm sai số lớn nhất, độ lệch có dấu trung bình và số mẫu không tính được. Với $Y=0$, không dùng sai số phần trăm chia cho $Y$; dùng sai số tuyệt đối theo cm.

Lấy nhiều mẫu không loại bỏ sai lệch hệ thống như lắp cảm biến lệch góc hoặc dùng sai tiêu cự.

## 7. Từ định vị điểm đến cảnh báo va chạm

### 7.1. Khoảng cách đúng chưa đủ

Một điểm chân vật chưa mô tả toàn bộ bề rộng vật cản. Điểm giữa có thể ở ngoài lối đi nhưng mép vật vẫn chắn đường.

Cần xét vùng chiếm chỗ của vật trên mặt đường và vùng người dùng sẽ đi qua. Các trường hợp cần xử lý riêng gồm vật nhô ngang, cành cây ngang đầu, mặt bàn, hố và bậc xuống; phép chiếu một điểm chân lên mặt đường không giải quyết đầy đủ những trường hợp này.

### 7.2. Hướng camera khác hướng di chuyển

Pitch và roll chưa đủ để biết vật nằm bên trái hay bên phải quỹ đạo đi nếu người dùng quay đầu.

Công thức mục 3 trả vị trí theo hướng ngang của camera. Muốn cảnh báo theo hướng đi cần xác định quan hệ giữa camera và hướng di chuyển. Có số đo yaw không tự động đồng nghĩa đã biết hướng đi của người dùng.

### 7.3. Lập luận về độ trễ chưa đủ

Báo cáo sử dụng:

$$
D\ge vt+d_0+\Delta D_{\max}
$$

và thay $v=1$ m/s, $t=4{,}8$ s, $d_0=0{,}5$ m, $\Delta D_{\max}=0{,}88$ m để được khoảng 6,18 m.

Phép cộng này đúng với các giả thiết đã nêu. Tuy nhiên, “6,18 m nhỏ hơn 10 m” không chứng minh hệ thống đủ khả năng cảnh báo:

- Vật có thể chỉ xuất hiện ở 2–4 m do bị che khuất hoặc đi vào từ bên cạnh.
- Thiết bị chụp theo yêu cầu có thêm thời gian chờ lần chụp tiếp theo.
- Tổng độ trễ còn gồm chụp, truyền, AI, tổng hợp tiếng nói và thời điểm người nghe hiểu cảnh báo.
- Nếu dùng $d_0$ để gộp phản ứng và dừng thì phải xác định, đo và giải thích rõ.
- Với vật lệch ngang, phải xét quỹ đạo va chạm; dùng khoảng cách $D$ đơn lẻ có thể gây hiểu nhầm.
- “Lớn nhất” trong một số lần thử không phải giới hạn chắc chắn cho mọi điều kiện mạng.

Nên đo độ trễ đầu-cuối và thời gian từ lúc vật xuất hiện đến cảnh báo có ích, kèm tỉ lệ trễ hoặc không phản hồi.

## 8. Những kết luận thực nghiệm chưa đủ căn cứ trong bản PDF

| Nội dung | Vấn đề cần xử lý |
|---|---|
| 200 lần thử máy tính | Cần mã mô phỏng, phân bố nhiễu, biên độ sai số, cấu hình, seed và dữ liệu kết quả |
| Sai số trung bình 18,9 cm; 2,7%; lớn nhất 4,3% | Bảng 7.2.1 còn trống; chưa thể tái tính các chỉ số từ dữ liệu gốc |
| Bù roll giảm 25,6% xuống 1,8% | Thiếu vị trí vật, tập góc, cách tạo nhiễu và mẫu đối chiếu |
| Tỉ lệ 93,3% = 28/30 | Đúng về số học, nhưng thiếu định nghĩa ba vùng, mẫu thử và ma trận nhầm lẫn |
| Bảng 7.2.2 về cảnh báo | Chưa có số lượt sớm, kịp, trễ và không thông báo |
| Sai số khoảng cách và tỉ lệ cảnh báo hụt | Là hai chỉ số khác nhau; tài liệu đang giải thích chúng lẫn nhau |
| Các giả thuyết H1–H4 ở cuối | Chưa tương ứng rõ với ba giả thuyết ở đầu |
| “Tiên phong” và tính mới | Mô hình chiếu phối cảnh, quay tọa độ và giao tia–mặt phẳng là kiến thức nền; cần chứng minh điểm mới ở cách tích hợp, thiết kế hoặc đánh giá |

Không đủ dữ liệu để kết luận các con số trên sai. Nhưng cũng chưa đủ dữ liệu để xác nhận chúng là kết quả của thiết bị thực.

Nếu là mô phỏng, phải ghi “kết quả mô phỏng” và giới hạn kết luận trong điều kiện mô phỏng. Không chuyển kết luận đó thành hiệu quả khi người khiếm thị đi ngoài đường.

## 9. Đối chiếu với mã nguồn hiện có

Phạm vi đối chiếu là các luồng chính trong thư mục Pi 3 và Server tại commit ghi đầu tài liệu; không khẳng định trạng thái phần mềm đang cài trên thiết bị.

| Thành phần | Điều quan sát được | Ý nghĩa |
|---|---|---|
| [Pi 3/sensors.py](../Pi%203/sensors.py) | Đọc GY25 qua UART và GY63/MS5611 qua I²C | Không phải bằng chứng đã triển khai GY53 như báo cáo |
| [Pi 3/README.md](../Pi%203/README.md) | Ghi rõ driver hiện có GY25, GY63, chưa có GY53 | Cần thống nhất phần cứng báo cáo với phiên bản triển khai |
| [Pi 3/app.py](../Pi%203/app.py) | Đọc dữ liệu cảm biến rồi truyền vào lời gọi client.command | Cần kiểm tra tiếp hợp đồng truyền dữ liệu và thời điểm chụp |
| [CommandRoutes.swift](../Server/Sources/ThienNhanServer/Command/CommandRoutes.swift) | CommandRequest không khai báo dữ liệu IMU/cảm biến; có nhánh trả thông báo hướng dẫn đường chưa hiệu chuẩn | Chưa có bằng chứng luồng này dùng góc cảm biến để tính khoảng cách |
| [VisionRoutes.swift](../Server/Sources/ThienNhanServer/Vision/VisionRoutes.swift) | OCR trả vùng chữ theo pixel | Vùng chữ không phải tọa độ tiếp xúc vật cản–mặt đường |

Trong các luồng này, chưa thấy mô-đun triển khai bộ công thức giao tia–mặt đường tương ứng báo cáo. Không thể dùng sự tồn tại của driver và OCR để xác nhận thuật toán định vị đã hoàn thành.

Tài liệu này không sửa chương trình hoặc mở nhánh hướng dẫn đường đang bị chặn.

## 10. Thứ tự hoàn thiện đề xuất

1. **Chốt quy ước hình học:** đơn vị, chiều trục, dấu pitch/roll, $X,Y,D,L$ và ý nghĩa hướng phía trước.
2. **Chốt camera và quy trình ảnh:** đúng module, chế độ ảnh, crop/resize, hiệu chuẩn nội tại và méo kính.
3. **Viết mô-đun hình học thuần:** nhận điểm ảnh, tư thế, độ cao; trả vị trí cùng trạng thái hợp lệ.
4. **Kiểm chứng hình học riêng:** dùng điểm đánh dấu có tọa độ thật và chọn pixel thủ công, chưa đưa sai số AI vào.
5. **Hiệu chuẩn IMU–camera và đồng bộ timestamp:** kiểm tra cả đứng yên lẫn đổi góc đầu.
6. **Đánh giá định vị chân vật:** đo sai số pixel và tỉ lệ không thấy điểm tiếp xúc trên ảnh thực.
7. **Đánh giá hệ thống khi chuyển động:** quỹ đạo, độ rộng vật, tổng độ trễ, phát hiện hụt và báo giả.
8. **Cập nhật báo cáo bằng dữ liệu:** tách mô phỏng, thực nghiệm tĩnh và thực nghiệm động.

Mỗi lượt đo nên lưu: mã ảnh, timestamp ảnh/IMU, camera profile, $h$, pitch/roll, $u,v$, vị trí thật, vị trí tính, trạng thái hợp lệ, độ trễ và kết quả cảnh báo. Công khai cấu hình và bảng dữ liệu sẽ giúp tái kiểm chứng các kết luận.

## 11. Kết luận

Có thể giữ nền tảng lượng giác và tam giác đồng dạng của báo cáo. Việc cần làm trước là thống nhất tọa độ, sửa hướng dẫn bù roll, xác định nguồn độ cao đáng tin và kiểm chứng phép đo trên ảnh thực.

Bộ công thức hình học cho vị trí của **điểm nằm trên mặt đường theo các giả thiết xác định**. Khả năng phát hiện vật cản và cảnh báo kịp lúc là bài toán hệ thống rộng hơn, chưa được chứng minh bằng các bảng hiện có.

## Tài liệu đối chiếu

- [1] Raspberry Pi, [Camera Modules — Industrial Customer Presentation](https://www.raspberrypi.com/app/uploads/2025/03/Industrial-Customer-Presentation_Camera-Modules.pdf): thông số Camera Module 3, độ phân giải và tiêu cự các phiên bản.
- [2] OpenCV, [Camera Calibration and 3D Reconstruction](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html), cùng [Camera Calibration tutorial](https://docs.opencv.org/4.13.0/dc/dbb/tutorial_py_calibration.html): mô hình phối cảnh, nội tại camera, hiệu chỉnh méo và đổi kích thước ảnh.
- [3] STMicroelectronics, [VL53L1X](https://www.st.com/en/imaging-and-photonics-solutions/vl53l1x.html): tầm đo công bố và trường nhìn cảm biến.
- [4] Mã nguồn [NCKH27VK tại commit được đối chiếu](https://github.com/phandinhdoc-spec/nckh27vk/tree/8fa9e9303629f764952c9a1447d19fc66ff4c08c).
