## BÀI SỐ 4a

☞ Các hàm INT, MOD xử lý số nguyên; các phép toán trên dữ liệu kiểu ngày (hiệu của 2 ngày), định dạng kiểu ngày. Vận dụng hàm tìm kiếm HLOOKUP để tìm một giá trị tham gia vào quá trình tính toán.

**KHÁCH SẠN BẠCH LIÊN**

<table style="width:100%;">
<colgroup>
<col style="width: 5%" />
<col style="width: 7%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 7%" />
<col style="width: 7%" />
<col style="width: 15%" />
<col style="width: 15%" />
<col style="width: 15%" />
</colgroup>
<tbody>
<tr>
<td>MS</td>
<td>LPH</td>
<td>NDEN</td>
<td>NDI</td>
<td>STU</td>
<td>SNG</td>
<td style="text-align: right;">TTUAN</td>
<td style="text-align: right;">TNGAY</td>
<td style="text-align: right;">THTIEN</td>
</tr>
<tr>
<td>a1</td>
<td>A</td>
<td>06/12/95</td>
<td>06/15/95</td>
<td>0</td>
<td>3</td>
<td style="text-align: right;">0 đ</td>
<td style="text-align: right;">330,000 đ</td>
<td style="text-align: right;">330,000 đ</td>
</tr>
<tr>
<td>a2</td>
<td>C</td>
<td>06/12/95</td>
<td>06/15/95</td>
<td>0</td>
<td>3</td>
<td style="text-align: right;">0 đ</td>
<td style="text-align: right;">225,000 đ</td>
<td style="text-align: right;">225,000 đ</td>
</tr>
<tr>
<td>a3</td>
<td>C</td>
<td>06/12/95</td>
<td>06/21/95</td>
<td>1</td>
<td>2</td>
<td style="text-align: right;">500,000 đ</td>
<td style="text-align: right;">150,000 đ</td>
<td style="text-align: right;">650,000 đ</td>
</tr>
<tr>
<td>a4</td>
<td>B</td>
<td>06/12/95</td>
<td>06/25/95</td>
<td>1</td>
<td>6</td>
<td style="text-align: right;">600,000 đ</td>
<td style="text-align: right;">540,000 đ</td>
<td style="text-align: right;">1,140,000 đ</td>
</tr>
<tr>
<td>a5</td>
<td>B</td>
<td>06/12/95</td>
<td>06/28/95</td>
<td>2</td>
<td>2</td>
<td style="text-align: right;">1,200,000 đ</td>
<td style="text-align: right;">180,000 đ</td>
<td style="text-align: right;">1,380,000 đ</td>
</tr>
<tr>
<td>a6</td>
<td>C</td>
<td>06/17/95</td>
<td>06/29/95</td>
<td>1</td>
<td>5</td>
<td style="text-align: right;">500,000 đ</td>
<td style="text-align: right;">375,000 đ</td>
<td style="text-align: right;">875,000 đ</td>
</tr>
<tr>
<td>a7</td>
<td>A</td>
<td>07/01/95</td>
<td>07/03/95</td>
<td>0</td>
<td>2</td>
<td style="text-align: right;">0 đ</td>
<td style="text-align: right;">220,000 đ</td>
<td style="text-align: right;">220,000 đ</td>
</tr>
<tr>
<td>a8</td>
<td>A</td>
<td>07/02/95</td>
<td>07/09/95</td>
<td>1</td>
<td>0</td>
<td style="text-align: right;">700,000 đ</td>
<td style="text-align: right;">0 đ</td>
<td style="text-align: right;">700,000 đ</td>
</tr>
<tr>
<td>a9</td>
<td>C</td>
<td>07/25/95</td>
<td>08/10/95</td>
<td>2</td>
<td>2</td>
<td style="text-align: right;">1,000,000 đ</td>
<td style="text-align: right;">150,000 đ</td>
<td style="text-align: right;">1,150,000 đ</td>
</tr>
<tr>
<td>a10</td>
<td>B</td>
<td>07/26/95</td>
<td>08/12/95</td>
<td>2</td>
<td>3</td>
<td style="text-align: right;">1,200,000 đ</td>
<td style="text-align: right;">270,000 đ</td>
<td style="text-align: right;">1,470,000 đ</td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td style="text-align: right;"></td>
<td style="text-align: right;"></td>
<td style="text-align: right;"></td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td colspan="2">Tổng cộng:</td>
<td style="text-align: right;">5,700,000 đ</td>
<td style="text-align: right;">2,440,000 đ</td>
<td style="text-align: right;">8,140,000 đ</td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td style="text-align: right;"></td>
<td style="text-align: right;"></td>
<td style="text-align: right;"></td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td colspan="3" style="text-align: left;">Loại phòng</td>
<td style="text-align: right;">A</td>
<td style="text-align: right;">B</td>
<td style="text-align: right;">C</td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td colspan="3" style="text-align: left;">Đơn giá tiền tuần</td>
<td style="text-align: right;">700000</td>
<td style="text-align: right;">600000</td>
<td style="text-align: right;">500000</td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td colspan="3" style="text-align: left;">Đơn giá tiền ngày</td>
<td style="text-align: right;">110000</td>
<td style="text-align: right;">90000</td>
<td style="text-align: right;">75000</td>
</tr>
</tbody>
</table>

☞ <u>Lưu ý</u>: Trong bảng dữ liệu trên, STU, SNG là số tuần và số ngày lưu trú của khách. TTUAN, TNGAY là tiền trọ theo tuần và theo ngày (vì khách sạn giảm giá đối với khách thuê phòng đăng ký theo tuần).

**<u>Câu 1</u>** Từ giá trị ngày đến và ngày đi hãy tính số tuần (STU) và số ngày (SNG) lưu trú (ví dụ: 12 ngày thì tính là 1 tuần và 5 ngày).

**<u>Câu 2</u>** Dựa vào bảng giá tiền theo từng loại A, B, C cho trên, hãy tính số tiền theo tuần và theo ngày của các khách trọ

**<u>Câu 3</u>** Tính TTIEN bằng tổng của tiền tuần và tiền ngày; tính tổng cộng cho các cột TTUAN, TNGAY và TTIEN

**<u>Câu 4</u>** Định dạng cho các cột ngày đi và ngày đến theo dạng năm có 4 chữ số (ví dụ 1995) và định dạng cho các cột tiền có dạng \#,## đ.

**<u>Câu 5</u>** Trang trí và lưu với tên BTAP4.XLS

### ⬥ Hướng dẫn thực hành:

**1.** Một tuần gồm 7 ngày; do đó số tuần bằng phần nguyên của số ngày lưu trú chia cho 7. Số ngày sau khi tính tuần sẽ là phần dư của phép chia 7. Ta có công thức tính như sau:

\[STU\] = **INT**((\[NDI\]-\[NDEN\])/7)

\[SNG\] = **MOD**(\[NDI\]-\[NDEN\], 7)

**2.** Để biết đơn giá (theo loại phòng) ta dò tìm trong bảng giá, và vì bảng giá bố trí số liệu theo chiều ngang nên ta dùng hàm HLOOKUP. Khi đó đơn giá tiền tuần ở hàng thứ 2 và đơn giá tiền ngày ở hàng thứ 3 của bảng tìm. Ta có:

\[TTUAN\] = \[STU\] \* HLOOKUP(\[LPH\], *bảng_tìm*, 2, 0)

\[TNGAY\] = \[SNG\] \* HLOOKUP(\[LPH\], *bảng_tìm*, 3, 0)

\- Trong đó, *bảng_tìm* là khoảng gồm 9 ô (có khung tô đậm) từ ô có giá trị A đến ô có chứa 75000. Dùng mouse để chọn 9 ô này, sau đó nhấn F4 để tạo tham chiếu tuyệt đối.

\- Có thể đặt tên cho vùng 9 ô của bảng đơn giá (ví dụ Table4) khi đó trong công thức ta chỉ cần nhập tên Table4 ở vị trí của *bảng_tìm*.

☞ Sau khi ghi xong, copy nội dung Sheet1 sang Sheet2 và sửa lại dữ liệu ở bảng tìm thành bảng dọc và dùng VLOOKUP để làm lại câu 2. (để copy sheet, có thể chọn tên Sheet ở dòng chứa tên các Sheet và nhấn Ctrl+Drag kéo sang bên cạnh để copy).

## BÀI SỐ 4b

☞ Sử dụng hàm tìm kiếm VLOOKUP

|     |       |        |         |         |
|-----|-------|--------|---------|---------|
| MSO | TEN   | SLUONG | TTIEN   | GCHU    |
| A   | DOS   | 40     | 4800000 | X       |
| B   | WORD  | 20     | 2800000 |         |
| C   | EXCEL | 35     | 4550000 | X       |
| A   | DOS   | 25     | 3000000 |         |
| C   | EXCEL | 35     | 4550000 | X       |
| B   | WORD  | 15     | 2100000 |         |
| C   | EXCEL | 40     | 5200000 | X       |
| B   | WORD  | 25     | 3500000 |         |
| A   | DOS   | 45     | 5400000 | X       |
|     |       |        |         |         |
|     |       | Mã số  | Tên     | Đơn giá |
|     |       | A      | DOS     | 120000  |
|     |       | B      | WORD    | 140000  |
|     |       | C      | EXCEL   | 130000  |

**<u>Câu 1</u>** Chọn Sheet3 của BTAP4 để nhập dữ liệu.

**<u>Câu 2</u>** Căn cứ vào bảng chứa tên và đơn giá của mã số để điền thông tin vào cột TEN

**<u>Câu 3</u>** Tính TTIEN bằng số lượng nhân đơn giá tùy thuộc vào loại, và tạo dạng với đơn vị tiền là \$ (dạng \#,##0 “\$”)

**<u>Câu 4</u>** Cột GCHU đánh dấu X nếu TTIEN lớn hơn 4000000, ngược lại để trống

(Lưu ý chuỗi trống là chuỗi có dạng “” )

**<u>Câu 5</u>** Trang trí và ghi lại những thay đổi vừa tạo ra ở Sheet3.
