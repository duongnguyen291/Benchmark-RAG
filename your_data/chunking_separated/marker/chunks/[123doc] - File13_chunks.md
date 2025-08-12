{0}------------------------------------------------

Form (hay còn gọi điều khiển Form) dùng để chứa các điều khiển khác
(Buttons, Label...)

Điều khiển Form có một số thuộc tính như sau:

=== VTNET - Duong ===

Form (hay còn gọi điều khiển Form) dùng để chứa các điều khiển khác
(Buttons, Label...)

Điều khiển Form có một số thuộc tính như sau:

| Tên             | Ý nghĩa                                                                                                                                                                                                                                                                                                  |
|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Name            | Tên của Form. Trong một Project tên của các Form phải khác nhau.                                                                                                                                                                                                                                         |
| AcceptButton    | Giá trị mà thuộc tính này nhận là tên của một Button trên Form (Nếu Form có chứa button). Khi đó nếu bạn nhấn phím Enter thì sự kiện Click của Button mà bạn chọn được thực thi mà không cần nhấn chuột vào Button đó.                                                                                   |
| Autosize        | Nhận một trong hai giá trị True hay False<br>- True: Không cho phép thay đổi kích thước Form mà che đi các điều khiển khác chứa trên Form<br>- False: Ngược lại                                                                                                                                          |
| AutoSizeMode    | Cho phép thay đổi kích thước của Form hay không? (Khi di chuyển chuột vào các mép của Form mà hiện nên biểu tượng ↔ là cho phép). Và nhận một trong hai giá trị<br>- GrowOnly: Cho phép<br>- và GrowAndShrink: Không cho phép                                                                            |
| BackColor       | Chọn màu nền cho Form                                                                                                                                                                                                                                                                                    |
| BackGroundImage | Chọn ảnh làm nền cho Form                                                                                                                                                                                                                                                                                |
| CancelButton    | Giá trị mà thuộc tính này nhận là tên của một Button trên Form (Nếu Form có chứa button). Khi đó nếu bạn nhấn phím ESC thì sự kiện Click của Button mà bạn chọn được thực thi mà không cần nhấn chuột vào Button đó (tương tự như thuộc tính AcceptButton ).                                             |
| ControlBoxX     | Nhận một trong hai giá trị True hay False<br>- True: Cho phép các các nút: MaximizeBox, MinimizeBox, Close trên Titlebar xuất hiện<br>- False: Không Cho phép các các nút: MaximizeBox, MinimizeBox, Close trên Titlebar xuất hiện (Khi đó các thuộc tính MaximizeBox, MinimizeBox của Form cũng mất đi) |
| Font            | Chọn kiểu Font chữ cho Form (Khi đó tất cả các điều khiển được thêm vào Form sẽ có thuộc tính Font giống như thuộc tính Font của Form)                                                                                                                                                                   |
| ForeColor       | Tương tự như thuộc tính Font nhưng áp dụng đối với màu chữ                                                                                                                                                                                                                                               |
| FormBorderStyle | Chọn Style cho Form (Có 7 lựa chọn khác nhau).                                                                                                                                                                                                                                                           |
| HelpButton      | Nhân một trong hai giá trị True hay False.                                                                                                                                                                                                                                                               |
|                 |                                                                                                                                                                                                                                                                                                          |
| Icon            | Chọn một Icon (có đuôi mở rộng là .ico) trên máy tính của bạn thay cho Icon mặc định của Form mà VS tạo ra                                                                                                                                                                                               |
| KeyPreview      | Nhận một trong hai giá trị True hay False<br>- True: Cho phép các sự kiện về bàn phím của Form (KeyUp, KeyDown, KeyPress... của Form) có hiệu lực.<br>- False: Ngược lại                                                                                                                                 |
| MaximizeBox     | Nhận một trong hai giá trị True hay False<br>- True: Cho phép nút MaximizeBox trên Titlebar có hiệu lực<br>- False: Ngược lại                                                                                                                                                                            |
| MaximizeBox     | Tương tự như thuộc tính MaximizeBox                                                                                                                                                                                                                                                                      |
| Opacity         | Độ trong suốt của Form                                                                                                                                                                                                                                                                                   |
| ShowIcon        | Nhận một trong hai giá trị True hay False<br>- True: Cho phép xuất hiện Icon của Form<br>- False: Không cho phép xuất hiện Icon của Form                                                                                                                                                                 |
| ShowIn Taskbar  | Nhận một trong hai giá trị True hay False<br>- True: Cho phép hiện Form dưới khay Taskbar<br>- False: Ngược lại                                                                                                                                                                                          |
| StartPosition   | Vị trí hiển thị của Form so với màn hình hệ thống hay Form cha (5 lựa chọn khác nhau)                                                                                                                                                                                                                    |
| Text            | Giá trị Text của Form                                                                                                                                                                                                                                                                                    |
| WindowState     | Trạng thái hiển thị của Form khi chạy (Khi bạn nhấn vào nút Run của VS) (Có 3 lựa chọn khác nhau: Ẩn dưới khay Taskbar, mở rộng hết màn hình...)                                                                                                                                                         |

=== VTNET - Duong ===

Điều khiển Form có một số thuộc tính như sau:

| Tên             | Ý nghĩa                                                                                                                                                                                                                                                                                                  |
|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Name            | Tên của Form. Trong một Project tên của các Form phải khác nhau.                                                                                                                                                                                                                                         |
| AcceptButton    | Giá trị mà thuộc tính này nhận là tên của một Button trên Form (Nếu Form có chứa button). Khi đó nếu bạn nhấn phím Enter thì sự kiện Click của Button mà bạn chọn được thực thi mà không cần nhấn chuột vào Button đó.                                                                                   |
| Autosize        | Nhận một trong hai giá trị True hay False<br>- True: Không cho phép thay đổi kích thước Form mà che đi các điều khiển khác chứa trên Form<br>- False: Ngược lại                                                                                                                                          |
| AutoSizeMode    | Cho phép thay đổi kích thước của Form hay không? (Khi di chuyển chuột vào các mép của Form mà hiện nên biểu tượng ↔ là cho phép). Và nhận một trong hai giá trị<br>- GrowOnly: Cho phép<br>- và GrowAndShrink: Không cho phép                                                                            |
| BackColor       | Chọn màu nền cho Form                                                                                                                                                                                                                                                                                    |
| BackGroundImage | Chọn ảnh làm nền cho Form                                                                                                                                                                                                                                                                                |
| CancelButton    | Giá trị mà thuộc tính này nhận là tên của một Button trên Form (Nếu Form có chứa button). Khi đó nếu bạn nhấn phím ESC thì sự kiện Click của Button mà bạn chọn được thực thi mà không cần nhấn chuột vào Button đó (tương tự như thuộc tính AcceptButton ).                                             |
| ControlBoxX     | Nhận một trong hai giá trị True hay False<br>- True: Cho phép các các nút: MaximizeBox, MinimizeBox, Close trên Titlebar xuất hiện<br>- False: Không Cho phép các các nút: MaximizeBox, MinimizeBox, Close trên Titlebar xuất hiện (Khi đó các thuộc tính MaximizeBox, MinimizeBox của Form cũng mất đi) |
| Font            | Chọn kiểu Font chữ cho Form (Khi đó tất cả các điều khiển được thêm vào Form sẽ có thuộc tính Font giống như thuộc tính Font của Form)                                                                                                                                                                   |
| ForeColor       | Tương tự như thuộc tính Font nhưng áp dụng đối với màu chữ                                                                                                                                                                                                                                               |
| FormBorderStyle | Chọn Style cho Form (Có 7 lựa chọn khác nhau).                                                                                                                                                                                                                                                           |
| HelpButton      | Nhân một trong hai giá trị True hay False.                                                                                                                                                                                                                                                               |
|                 |                                                                                                                                                                                                                                                                                                          |
| Icon            | Chọn một Icon (có đuôi mở rộng là .ico) trên máy tính của bạn thay cho Icon mặc định của Form mà VS tạo ra                                                                                                                                                                                               |
| KeyPreview      | Nhận một trong hai giá trị True hay False<br>- True: Cho phép các sự kiện về bàn phím của Form (KeyUp, KeyDown, KeyPress... của Form) có hiệu lực.<br>- False: Ngược lại                                                                                                                                 |
| MaximizeBox     | Nhận một trong hai giá trị True hay False<br>- True: Cho phép nút MaximizeBox trên Titlebar có hiệu lực<br>- False: Ngược lại                                                                                                                                                                            |
| MaximizeBox     | Tương tự như thuộc tính MaximizeBox                                                                                                                                                                                                                                                                      |
| Opacity         | Độ trong suốt của Form                                                                                                                                                                                                                                                                                   |
| ShowIcon        | Nhận một trong hai giá trị True hay False<br>- True: Cho phép xuất hiện Icon của Form<br>- False: Không cho phép xuất hiện Icon của Form                                                                                                                                                                 |
| ShowIn Taskbar  | Nhận một trong hai giá trị True hay False<br>- True: Cho phép hiện Form dưới khay Taskbar<br>- False: Ngược lại                                                                                                                                                                                          |
| StartPosition   | Vị trí hiển thị của Form so với màn hình hệ thống hay Form cha (5 lựa chọn khác nhau)                                                                                                                                                                                                                    |
| Text            | Giá trị Text của Form                                                                                                                                                                                                                                                                                    |
| WindowState     | Trạng thái hiển thị của Form khi chạy (Khi bạn nhấn vào nút Run của VS) (Có 3 lựa chọn khác nhau: Ẩn dưới khay Taskbar, mở rộng hết màn hình...)                                                                                                                                                         |

{1}------------------------------------------------

=== VTNET - Duong ===

| Tên             | Ý nghĩa                                                                                                                                                                                                                                                                                                  |
|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Name            | Tên của Form. Trong một Project tên của các Form phải khác nhau.                                                                                                                                                                                                                                         |
| AcceptButton    | Giá trị mà thuộc tính này nhận là tên của một Button trên Form (Nếu Form có chứa button). Khi đó nếu bạn nhấn phím Enter thì sự kiện Click của Button mà bạn chọn được thực thi mà không cần nhấn chuột vào Button đó.                                                                                   |
| Autosize        | Nhận một trong hai giá trị True hay False<br>- True: Không cho phép thay đổi kích thước Form mà che đi các điều khiển khác chứa trên Form<br>- False: Ngược lại                                                                                                                                          |
| AutoSizeMode    | Cho phép thay đổi kích thước của Form hay không? (Khi di chuyển chuột vào các mép của Form mà hiện nên biểu tượng ↔ là cho phép). Và nhận một trong hai giá trị<br>- GrowOnly: Cho phép<br>- và GrowAndShrink: Không cho phép                                                                            |
| BackColor       | Chọn màu nền cho Form                                                                                                                                                                                                                                                                                    |
| BackGroundImage | Chọn ảnh làm nền cho Form                                                                                                                                                                                                                                                                                |
| CancelButton    | Giá trị mà thuộc tính này nhận là tên của một Button trên Form (Nếu Form có chứa button). Khi đó nếu bạn nhấn phím ESC thì sự kiện Click của Button mà bạn chọn được thực thi mà không cần nhấn chuột vào Button đó (tương tự như thuộc tính AcceptButton ).                                             |
| ControlBoxX     | Nhận một trong hai giá trị True hay False<br>- True: Cho phép các các nút: MaximizeBox, MinimizeBox, Close trên Titlebar xuất hiện<br>- False: Không Cho phép các các nút: MaximizeBox, MinimizeBox, Close trên Titlebar xuất hiện (Khi đó các thuộc tính MaximizeBox, MinimizeBox của Form cũng mất đi) |
| Font            | Chọn kiểu Font chữ cho Form (Khi đó tất cả các điều khiển được thêm vào Form sẽ có thuộc tính Font giống như thuộc tính Font của Form)                                                                                                                                                                   |
| ForeColor       | Tương tự như thuộc tính Font nhưng áp dụng đối với màu chữ                                                                                                                                                                                                                                               |
| FormBorderStyle | Chọn Style cho Form (Có 7 lựa chọn khác nhau).                                                                                                                                                                                                                                                           |
| HelpButton      | Nhân một trong hai giá trị True hay False.                                                                                                                                                                                                                                                               |
|                 |                                                                                                                                                                                                                                                                                                          |
| Icon            | Chọn một Icon (có đuôi mở rộng là .ico) trên máy tính của bạn thay cho Icon mặc định của Form mà VS tạo ra                                                                                                                                                                                               |
| KeyPreview      | Nhận một trong hai giá trị True hay False<br>- True: Cho phép các sự kiện về bàn phím của Form (KeyUp, KeyDown, KeyPress... của Form) có hiệu lực.<br>- False: Ngược lại                                                                                                                                 |
| MaximizeBox     | Nhận một trong hai giá trị True hay False<br>- True: Cho phép nút MaximizeBox trên Titlebar có hiệu lực<br>- False: Ngược lại                                                                                                                                                                            |
| MaximizeBox     | Tương tự như thuộc tính MaximizeBox                                                                                                                                                                                                                                                                      |
| Opacity         | Độ trong suốt của Form                                                                                                                                                                                                                                                                                   |
| ShowIcon        | Nhận một trong hai giá trị True hay False<br>- True: Cho phép xuất hiện Icon của Form<br>- False: Không cho phép xuất hiện Icon của Form                                                                                                                                                                 |
| ShowIn Taskbar  | Nhận một trong hai giá trị True hay False<br>- True: Cho phép hiện Form dưới khay Taskbar<br>- False: Ngược lại                                                                                                                                                                                          |
| StartPosition   | Vị trí hiển thị của Form so với màn hình hệ thống hay Form cha (5 lựa chọn khác nhau)                                                                                                                                                                                                                    |
| Text            | Giá trị Text của Form                                                                                                                                                                                                                                                                                    |
| WindowState     | Trạng thái hiển thị của Form khi chạy (Khi bạn nhấn vào nút Run của VS) (Có 3 lựa chọn khác nhau: Ẩn dưới khay Taskbar, mở rộng hết màn hình...)                                                                                                                                                         |

{1}------------------------------------------------

Một số sự kiện thường dùng

=== VTNET - Duong ===

{1}------------------------------------------------

Một số sự kiện thường dùng

| Tên              | Ý nghĩa                                                                                       |
|------------------|-----------------------------------------------------------------------------------------------|
| AutoSizeChanged  | Xảy ra khi thuộc tính Autosize của Form chuyển từ True → False hay ngược lại là False → True. |
| BackColorChanged | Xảy ra khi thuộc tính BackColor của Form thay đổi                                             |
| Click            | Xảy ra khi người dùng Click chuột vào vùng làm việc thuộc Form                                |
| ControlAdded     | Xảy ra khi một điều khiển được Add vào Form                                                   |
| ControlRemoved   | Xảy ra khi một điều khiển bị xóa khỏi Form                                                    |
| CursorChanged    | Xảy ra khi thuộc tính Cursor của Form thay đổi                                                |
| DoubleClick      | Xảy ra khi người dùng DoubleClick vào vùng làm việc của Form                                  |

=== VTNET - Duong ===

Một số sự kiện thường dùng

| Tên              | Ý nghĩa                                                                                       |
|------------------|-----------------------------------------------------------------------------------------------|
| AutoSizeChanged  | Xảy ra khi thuộc tính Autosize của Form chuyển từ True → False hay ngược lại là False → True. |
| BackColorChanged | Xảy ra khi thuộc tính BackColor của Form thay đổi                                             |
| Click            | Xảy ra khi người dùng Click chuột vào vùng làm việc thuộc Form                                |
| ControlAdded     | Xảy ra khi một điều khiển được Add vào Form                                                   |
| ControlRemoved   | Xảy ra khi một điều khiển bị xóa khỏi Form                                                    |
| CursorChanged    | Xảy ra khi thuộc tính Cursor của Form thay đổi                                                |
| DoubleClick      | Xảy ra khi người dùng DoubleClick vào vùng làm việc của Form                                  |

{2}------------------------------------------------

=== VTNET - Duong ===

| Tên              | Ý nghĩa                                                                                       |
|------------------|-----------------------------------------------------------------------------------------------|
| AutoSizeChanged  | Xảy ra khi thuộc tính Autosize của Form chuyển từ True → False hay ngược lại là False → True. |
| BackColorChanged | Xảy ra khi thuộc tính BackColor của Form thay đổi                                             |
| Click            | Xảy ra khi người dùng Click chuột vào vùng làm việc thuộc Form                                |
| ControlAdded     | Xảy ra khi một điều khiển được Add vào Form                                                   |
| ControlRemoved   | Xảy ra khi một điều khiển bị xóa khỏi Form                                                    |
| CursorChanged    | Xảy ra khi thuộc tính Cursor của Form thay đổi                                                |
| DoubleClick      | Xảy ra khi người dùng DoubleClick vào vùng làm việc của Form                                  |

{2}------------------------------------------------

| FontChanged      | Xảy ra khi thuộc tính Font của Form có sự thay đổi                                                                                                                                          |
|------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ForeColorChanged | Xảy ra khi thuộc tính ForeColor của Form có sự thay đổi                                                                                                                                     |
| FormClosed       | Xảy ra khi Form đã đóng (Nhấn vào nút X màu đỏ trên Titlebar)                                                                                                                               |
| FormClosing      | Xảy ra khi Form đang đóng (2 sự kiện FormClosed và FormClosing thường dùng trong lập trình CSDL: khi xảy ra sự kiện này thì đóng kết nối CSDL)                                              |
| KeyDown          | Xảy ra khi người dùng nhấn một phím hay một tố hợp phím (tùy thuộc vào xử lý của chúng ta)                                                                                                  |
| KeyPress         | Xảy ra khi người dùng nhấn một phím                                                                                                                                                         |
| KeyUp            | Xảy ra khi người dùng nhả một phím.                                                                                                                                                         |
| MouseClick       | Xảy ra khi người dùng nhấn chuột (một trong 3 lựa chọn: Trái, giữa, phải)                                                                                                                   |
| MouseDoubleClick | Xảy ra khi người dùng DoubleClick chuột vào một vùng làm việc của Form(một trong 3 lựa chọn: Trái, giữa, phải)                                                                              |
| MouseDown        | Xảy ra khi người dùng nhấn chuột                                                                                                                                                            |
| MouseHover       | Xảy ra khi người dùng di chuyển vào các vùng làm việc Form                                                                                                                                  |
| MouseLeave       | Xảy ra khi di chuyển chuột ra khỏi vùng làm việc của Form                                                                                                                                   |
| MouseMove        | Xảy ra khi di chuyển chuột trên một vùng làm việc thuộc Form (nếu Form có chứa một điều khiển nào đó, khi di chuyển chuột trên điều khiển này thì không xảy ra sự kiện MouseMove của Form). |
| MouseUp          | Xảy ra khi người dùng nhả nhấn chuột (có thể là chuột trái, chuột phải, chuột giữa - chuột cuộn)                                                                                            |
| Move             | Xảy ra khi di chuyển Form (có sự thay đổi vị trí của Form)                                                                                                                                  |
| StyleChanged     | Xảy ra khi thuộc tính FormBorderStyle của Form thay đổi                                                                                                                                     |
| TextChanged      | Xảy ra khi thuộc tính Text của Form thay đổi.                                                                                                                                               |

=== VTNET - Duong ===

{2}------------------------------------------------

| FontChanged      | Xảy ra khi thuộc tính Font của Form có sự thay đổi                                                                                                                                          |
|------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ForeColorChanged | Xảy ra khi thuộc tính ForeColor của Form có sự thay đổi                                                                                                                                     |
| FormClosed       | Xảy ra khi Form đã đóng (Nhấn vào nút X màu đỏ trên Titlebar)                                                                                                                               |
| FormClosing      | Xảy ra khi Form đang đóng (2 sự kiện FormClosed và FormClosing thường dùng trong lập trình CSDL: khi xảy ra sự kiện này thì đóng kết nối CSDL)                                              |
| KeyDown          | Xảy ra khi người dùng nhấn một phím hay một tố hợp phím (tùy thuộc vào xử lý của chúng ta)                                                                                                  |
| KeyPress         | Xảy ra khi người dùng nhấn một phím                                                                                                                                                         |
| KeyUp            | Xảy ra khi người dùng nhả một phím.                                                                                                                                                         |
| MouseClick       | Xảy ra khi người dùng nhấn chuột (một trong 3 lựa chọn: Trái, giữa, phải)                                                                                                                   |
| MouseDoubleClick | Xảy ra khi người dùng DoubleClick chuột vào một vùng làm việc của Form(một trong 3 lựa chọn: Trái, giữa, phải)                                                                              |
| MouseDown        | Xảy ra khi người dùng nhấn chuột                                                                                                                                                            |
| MouseHover       | Xảy ra khi người dùng di chuyển vào các vùng làm việc Form                                                                                                                                  |
| MouseLeave       | Xảy ra khi di chuyển chuột ra khỏi vùng làm việc của Form                                                                                                                                   |
| MouseMove        | Xảy ra khi di chuyển chuột trên một vùng làm việc thuộc Form (nếu Form có chứa một điều khiển nào đó, khi di chuyển chuột trên điều khiển này thì không xảy ra sự kiện MouseMove của Form). |
| MouseUp          | Xảy ra khi người dùng nhả nhấn chuột (có thể là chuột trái, chuột phải, chuột giữa - chuột cuộn)                                                                                            |
| Move             | Xảy ra khi di chuyển Form (có sự thay đổi vị trí của Form)                                                                                                                                  |
| StyleChanged     | Xảy ra khi thuộc tính FormBorderStyle của Form thay đổi                                                                                                                                     |
| TextChanged      | Xảy ra khi thuộc tính Text của Form thay đổi.                                                                                                                                               |

{3}------------------------------------------------

=== VTNET - Duong ===

| FontChanged      | Xảy ra khi thuộc tính Font của Form có sự thay đổi                                                                                                                                          |
|------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ForeColorChanged | Xảy ra khi thuộc tính ForeColor của Form có sự thay đổi                                                                                                                                     |
| FormClosed       | Xảy ra khi Form đã đóng (Nhấn vào nút X màu đỏ trên Titlebar)                                                                                                                               |
| FormClosing      | Xảy ra khi Form đang đóng (2 sự kiện FormClosed và FormClosing thường dùng trong lập trình CSDL: khi xảy ra sự kiện này thì đóng kết nối CSDL)                                              |
| KeyDown          | Xảy ra khi người dùng nhấn một phím hay một tố hợp phím (tùy thuộc vào xử lý của chúng ta)                                                                                                  |
| KeyPress         | Xảy ra khi người dùng nhấn một phím                                                                                                                                                         |
| KeyUp            | Xảy ra khi người dùng nhả một phím.                                                                                                                                                         |
| MouseClick       | Xảy ra khi người dùng nhấn chuột (một trong 3 lựa chọn: Trái, giữa, phải)                                                                                                                   |
| MouseDoubleClick | Xảy ra khi người dùng DoubleClick chuột vào một vùng làm việc của Form(một trong 3 lựa chọn: Trái, giữa, phải)                                                                              |
| MouseDown        | Xảy ra khi người dùng nhấn chuột                                                                                                                                                            |
| MouseHover       | Xảy ra khi người dùng di chuyển vào các vùng làm việc Form                                                                                                                                  |
| MouseLeave       | Xảy ra khi di chuyển chuột ra khỏi vùng làm việc của Form                                                                                                                                   |
| MouseMove        | Xảy ra khi di chuyển chuột trên một vùng làm việc thuộc Form (nếu Form có chứa một điều khiển nào đó, khi di chuyển chuột trên điều khiển này thì không xảy ra sự kiện MouseMove của Form). |
| MouseUp          | Xảy ra khi người dùng nhả nhấn chuột (có thể là chuột trái, chuột phải, chuột giữa - chuột cuộn)                                                                                            |
| Move             | Xảy ra khi di chuyển Form (có sự thay đổi vị trí của Form)                                                                                                                                  |
| StyleChanged     | Xảy ra khi thuộc tính FormBorderStyle của Form thay đổi                                                                                                                                     |
| TextChanged      | Xảy ra khi thuộc tính Text của Form thay đổi.                                                                                                                                               |

{3}------------------------------------------------

//Sự kiện FormClosed - Sự kiện này được gọi khi Form đã đóng
private void frmForm\_FormClosed(object sender, FormClosedEventArgs e)
{

=== VTNET - Duong ===

{3}------------------------------------------------

//Sự kiện FormClosed - Sự kiện này được gọi khi Form đã đóng
private void frmForm\_FormClosed(object sender, FormClosedEventArgs e)
{

MessageBox.Show("Sự kiện FormClosed được gọi",

"FormClosed",MessageBoxButtons.OK,MessageBoxIcon.Information);
}

//Sự kiện FormClosing xảy ra khi Form đang đóng
private void frmForm\_FormClosing(object sender, FormClosingEventArgs e)
{

if (MessageBox.Show("Bạn có muốn đóng Form lại hay không?",
"FormClosing",

e.Cancel = false;// Đóng Form lại

else

e.Cancel = true;//Không đóng Form nữa/Sự kiện KeyPress

//Sự kiện KeyUp tương tự như sự kiện KeyPress

//Sự kiện KeyDown xảy ra khi nhấn một phím hay tổ hợp phím

private void frmForm\_KeyDown(object sender, KeyEventArgs e)

{

//khi nhấn một phím bất kì trên bàn phím thì sự kiện KeyPress được gọi
//Đồng thời sự kiện KeyDown cũng được gọi → KeyPress là trường hợp
riêng của KeyDown

=== VTNET - Duong ===

{

//khi nhấn một phím bất kì trên bàn phím thì sự kiện KeyPress được gọi
//Đồng thời sự kiện KeyDown cũng được gọi → KeyPress là trường hợp
riêng của KeyDown

//Áp dụng: Nhấn một tổ hợp phím thì sự kiện KeyDown mới được gọi
//Như Windows Media: Nhấn Ctrl+F để di chuyển bài tiếp theo
if (o KouCode == Koug E88 Modifio == Koue Control

MessageBox.Show("Sự kiện KeyDown được gọi khi bạn nhấn Ctrl + F");

{4}------------------------------------------------
