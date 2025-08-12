# BÀI SỐ 4a

 Các hàm INT, MOD xử lý số nguyên; các phép toán trên dữ liệu kiểu ngày (hiệu của 2 ngày), định dạng kiểu ngày. Vận dụng hàm tìm kiếm HLOOKUP để tìm một giá trị tham gia vào quá trình tính toán.

# KHÁCH SẠN BẠCH LIÊN

# MS LPH NDEN

# NDI

# STU SNG

# TTUAN

# TNGAY

# THTIEN

# a1 A

06/12/95 06/15/95

0

3

# 0 đ

330,000 đ

330,000 đ

# a2

# C

06/12/95 06/15/95

0

3

# 0 đ

225,000 đ

225,000 đ

# a3

# C

06/12/95 06/21/95

1

2

500,000 đ

150,000 đ

650,000 đ

# a4

# B

06/12/95 06/25/95

1

6

600,000 đ

540,000 đ 1,140,000 đ

# a5

# B

06/12/95 06/28/95

2

2

1,200,000 đ

180,000 đ 1,380,000 đ

# a6

# C

06/17/95 06/29/95

1

5

500,000 đ

375,000 đ

875,000 đ

# a7 A

07/01/95 07/03/95

0

2

# 0 đ

220,000 đ

220,000 đ

# a8 A

07/02/95 07/09/95

1

0

700,000 đ

# 0 đ

700,000 đ

# a9

# C

07/25/95 08/10/95

2

2

1,000,000 đ

150,000 đ 1,150,000 đ

# a10 B

07/26/95 08/12/95

2

3

1,200,000 đ

270,000 đ 1,470,000 đ

Tổng cộng: 5,700,000 đ 2,440,000 đ 8,140,000 đ

# Loại phòng

# A

# B

# C

# Đơn giá tiền tuần

700000

600000

500000

# Đơn giá tiền ngày

110000

90000

75000

 Lưu ý: Trong bảng dữ liệu trên, STU, SNG là số tuần và số ngày lưu trú của khách. TTUAN, TNGAY là tiền trọ theo tuần và theo ngày (vì khách sạn giảm giá đối với khách thuê phòng đăng ký theo tuần).

Câu 1 Từ giá trị ngày đến và ngày đi hãy tính số tuần (STU) và số ngày (SNG) lưu trú

# (ví dụ: 12 ngày thì tính là 1 tuần và 5 ngày).

Câu 2 Dựa vào bảng giá tiền theo từng loại A, B, C cho trên, hãy tính số tiền theo tuần

# và theo ngày của các khách trọ

Câu 3 Tính TTIEN bằng tổng của tiền tuần và tiền ngày; tính tổng cộng cho các cột

# TTUAN, TNGAY và TTIEN

Câu 4 Định dạng cho các cột ngày đi và ngày đến theo dạng năm có 4 chữ số (ví dụ

1995) và định dạng cho các cột tiền có dạng #,## đ.

Câu 5 Trang trí và lưu với tên BTAP4.XLS  Hướng dẫn thực hành: 1. Một tuần gồm 7 ngày; do đó số tuần bằng phần nguyên của số ngày lưu trú chia cho 7. Số ngày sau khi tính tuần sẽ là phần dư của phép chia 7. Ta có công thức tính như sau: [STU] = INT(([NDI]-[NDEN])/7) [SNG] = MOD([NDI]-[NDEN], 7)

2. Để biết đơn giá (theo loại phòng) ta dò tìm trong bảng giá, và vì bảng giá bố trí số liệu theo chiều ngang nên ta dùng hàm HLOOKUP. Khi đó đơn giá tiền tuần ở hàng thứ 2 và đơn giá tiền ngày ở hàng thứ 3 của bảng tìm. Ta có:

[TTUAN] = [STU] * HLOOKUP([LPH], bảng_tìm, 2, 0) [TNGAY] = [SNG] * HLOOKUP([LPH], bảng_tìm, 3, 0)

Trong đó, bảng_tìm là khoảng gồm 9 ô (có khung tô đậm) từ ô có giá trị A đến ô có chứa 75000. Dùng mouse để chọn 9 ô này, sau đó nhấn F4 để tạo tham chiếu tuyệt đối.

Có thể đặt tên cho vùng 9 ô của bảng đơn giá (ví dụ Table4) khi đó trong công thức ta chỉ cần nhập tên Table4 ở vị trí của bảng_tìm.

 Sau khi ghi xong, copy nội dung Sheet1 sang Sheet2 và sửa lại dữ liệu ở bảng tìm thành bảng dọc và dùng VLOOKUP để làm lại câu 2. (để copy sheet, có thể chọn tên Sheet ở dòng chứa tên các Sheet và nhấn Ctrl+Drag kéo sang bên cạnh để copy).

# BÀI SỐ 4b

#  Sử dụng hàm tìm kiếm VLOOKUP

# MSO

# TEN

# SLUONG

# TTIEN

# GCHU

# A

# DOS

40

4800000

# X

# B

# WORD

20

2800000

# C

# EXCEL

35

4550000

# X

# A

# DOS

25

3000000

# C

# EXCEL

35

4550000

# X

# B

# WORD

15

2100000

# C

# EXCEL

40

5200000

# X

# B

# WORD

25

3500000

# A

# DOS

45

5400000

# X

# Mã số

# Tên

# Đơn giá

# A

# DOS

120000

# B

# WORD

140000

# C

# EXCEL

130000

Câu 1 Chọn Sheet3 của BTAP4 để nhập dữ liệu. Câu 2 Căn cứ vào bảng chứa tên và đơn giá của mã số để điền thông tin vào cột TEN Câu 3 Tính TTIEN bằng số lượng nhân đơn giá tùy thuộc vào loại, và tạo dạng với

# đơn vị tiền là $ (dạng #,##0 “$”)

Câu 4 Cột GCHU đánh dấu X nếu TTIEN lớn hơn 4000000, ngược lại để trống

# (Lưu ý chuỗi trống là chuỗi có dạng “” )

Câu 5 Trang trí và ghi lại những thay đổi vừa tạo ra ở Sheet3.