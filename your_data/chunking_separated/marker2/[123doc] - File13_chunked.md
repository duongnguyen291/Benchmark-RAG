{0}

{page_id}-{48}

# **FORM**

# \*\*\*

# **1. Chức năng**

Form (hay còn gọi điều khiển Form) dùng để chứa các điều khiển khác (Buttons, Label…)

# **2. Một số thuộc tính thường dùng**

Điều khiển Form có một số thuộc tính như sau:

============== VTNET - Duong ==============

{0}

{page_id}-{48}

# **FORM**

# \*\*\*

# **1. Chức năng**

Form (hay còn gọi điều khiển Form) dùng để chứa các điều khiển khác (Buttons, Label…)

# **2. Một số thuộc tính thường dùng**

Điều khiển Form có một số thuộc tính như sau:

| Tên | Ỹ nghĩa |
|-----------------|--------------------------------------------------------------------------------------------------------------|
| Name | Tên của<br>Form. Trong một<br>Project tên của các Form phải |
| | khác nhau. |
| AcceptButton | Giá trị mà thuộc tính này nhận là tên của một Button trên |
| | Form (Nếu Form có chứa button). Khi đó nếu bạn nhấn |
| | phím Enter<br>thì sự kiện Click của Button mà bạn chọn |
| | được thực thi mà không cần nhấn chuột vào Button đó. |
| Autosize | Nhận một trong hai giá trị True hay False |
| | -<br>True: Không cho phép thay đổi kích thước Form mà |
| | che đi các điều khiển khác chứa trên Form |
| | -<br>False: Ngược lại |
| AutoSizeMode | Cho phép thay đổi kích thước của Form hay không? (Khi |
| | di chuyển chuột vào các mép của Form mà hiện nên |
| | biểu tượng ↔<br>là cho phép). Và nhận một trong hai giá trị |
| | -<br>GrowOnly: Cho phép |
| | -<br>và GrowAndShrink: Không cho phép |
| BackColor | Chọn màu nền cho Form |
| BackGroundImage | Chọn ảnh làm nền cho Form |
| CancelButton | Giá trị mà thuộc tính này nhận là tên của một Button trên |
| | Form (Nếu Form có chứa button). Khi đó nếu bạn nhấn |
| | phím ESC<br>thì sự kiện Click của Button mà bạn chọn |
| | được thực thi mà không cần nhấn chuột vào Button đó |
| | (tương tự như thuộc tính AcceptButton ). |
| ControlBox | Nhận một trong hai giá trị True hay False<br>-<br>True:<br>Cho<br>phép<br>các<br>các<br>nút:<br>MaximizeBox, |
| | MinimizeBox, Close trên Titlebar xuất hiện |
| | -<br>False: Không Cho phép các các nút: MaximizeBox, |
| | MinimizeBox, Close trên Titlebar xuất hiện (Khi đó |
| | các thuộc tính MaximizeBox, MinimizeBox của Form |
| | cũng mất đi) |
| Font | Chọn kiểu Font chữ cho Form (Khi đó tất cả các điều |
| | khiển được thêm vào Form sẽ có thuộc tính Font giống |
| | như thuộc tính Font của Form) |
| ForeColor | Tương tự như thuộc tính Font nhưng áp dụng đối với |
| | màu chữ |
| FormBorderStyle | Chọn Style cho Form (Có 7 lựa chọn khác nhau). |
| HelpButton | Nhận một trong hai giá trị True hay False. |

============== VTNET - Duong ==============

{1}

{page_id}-{48}

#### *Chuyên đề 02: Công nghệ .NET GV: Hoàng Quốc Việt*

| | -<br>True: Cho phép xuất hiện Buton có dấu ?<br>trên<br>Titlebar (Với điều kiện: hai thuộc tính MaximizeBox,<br>MaximizeBox phải đặt giá trị là False)<br>-<br>False: Ngược lại<br>→ Thuộc tính này sẽ hay đi kèm với điều khiển<br>HelpProvider<br>về sau |
|---------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Icon | Chọn một Icon (có đuôi mở rộng là .ico) trên máy tính<br>của bạn thay cho Icon mặc định của Form mà VS tạo ra |
| KeyPreview | Nhận một trong hai giá trị<br>True hay False<br>-<br>True: Cho phép các sự kiện về bàn phím của Form<br>(KeyUp, KeyDown, KeyPress… của Form) có hiệu<br>lực.<br>-<br>False: Ngược lại |
| MaximizeBox | Nhận một trong hai giá trị True hay False<br>-<br>True: Cho phép nút MaximizeBox trên Titlebar có<br>hiệu lực<br>-<br>False: Ngược lại |
| MaximizeBox | Tương tự như thuộc tính MaximizeBox |
| Opacity | Độ trong suốt của Form |
| ShowIcon | Nhận một trong hai giá trị True hay False<br>-<br>True: Cho phép xuất hiện Icon của Form<br>-<br>False: Không cho phép xuất hiện Icon của Form |
| ShowInTaskbar | Nhận một trong hai giá trị True hay False<br>-<br>True: Cho phép hiện Form dưới khay Taskbar<br>-<br>False: Ngược lại |
| StartPosition | Vị trí hiển thị của Form so với màn hình hệ thống hay<br>Form cha (5 lựa chọn khác nhau) |
| Text | Giá trị Text của Form |
| WindowState | Trạng thái hiển thị của Form khi chạy (Khi bạn nhấn vào<br>nút Run của VS) (Có 3 lựa chọn khác nhau: Ẩn dưới<br>khay Taskbar, mở rộng hết màn hình…). |

============== VTNET - Duong ==============

### **3. Sự kiện**

Một số sự kiện thường dùng

| Tên | Ỹ nghĩa |
|------------------|--------------------------------------------------------------|
| AutoSizeChanged | Xảy ra khi thuộc tính Autosize<br>của Form chuyển từ<br>True |
| | → False hay ngược lại là False → True. |
| BackColorChanged | Xảy ra khi thuộc tính BackColor<br>của Form thay |
| | đổi |
| Click | Xảy ra khi người dùng Click chuột vào vùng làm việc |
| | thuộc Form |
| ControlAdded | Xảy ra khi một điều khiển được Add vào Form |
| ControlRemoved | Xảy ra khi một điều khiển bị<br>xóa khỏi Form |
| CursorChanged | Xảy ra khi thuộc tính Cursor<br>của Form thay đổi |
| DoubleClick | Xảy ra khi người dùng DoubleClick vào vùng làm việc |
| | của<br>Form |

{2}

{page_id}-{48}

#### *Chuyên đề 02: Công nghệ .NET GV: Hoàng Quốc Việt*

============== VTNET - Duong ==============

{2}

{page_id}-{48}

#### *Chuyên đề 02: Công nghệ .NET GV: Hoàng Quốc Việt*

| FontChanged | Xảy ra khi thuộc tính Font<br>của Form có sự thay đổi |
|------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ForeColorChanged | Xảy ra khi thuộc tính ForeColor<br>của Form có sự thay đổi |
| FormClosed | Xảy ra khi Form đã đóng (Nhấn vào nút X<br>màu đỏ trên<br>Titlebar) |
| FormClosing | Xảy ra khi Form đang đóng (2 sự kiện FormClosed<br>và<br>FormClosing<br>thường dùng trong lập trình CSDL: khi<br>xảy ra sự kiện này thì đóng kết nối CSDL) |
| KeyDown | Xảy ra khi người dùng nhấn một phím hay một tố hợp<br>phím (tùy thuộc vào xử lý của chúng ta) |
| KeyPress | Xảy ra khi người dùng nhấn<br>một phím |
| KeyUp | Xảy ra khi người dùng nhả<br>một phím. |
| MouseClick | Xảy ra khi người dùng nhấn chuột (một trong 3 lựa chọn:<br>Trái, giữa, phải) |
| MouseDoubleClick | Xảy ra khi người dùng DoubleClick<br>chuột vào một<br>vùng làm việc<br>của<br>Form(một trong 3 lựa chọn: Trái, giữa,<br>phải) |
| MouseDown | Xảy ra khi người dùng nhấn chuột |
| MouseHover | Xảy ra khi người dùng di chuyển vào các vùng làm việc<br>Form |
| MouseLeave | Xảy ra khi di chuyển chuột ra khỏi vùng làm việc của<br>Form |
| MouseMove | Xảy ra khi di chuyển chuột trên một vùng làm việc<br>thuộc<br>Form (nếu Form có chứa một điều khiển nào đó, khi di<br>chuyển chuột trên điều khiển này thì không xảy ra sự<br>kiện MouseMove<br>của Form). |
| MouseUp | Xảy ra khi người dùng nhả nhấn chuột (có thể là chuột<br>trái, chuột phải, chuột giữa -<br>chuột<br>cuộn) |
| Move | Xảy ra khi di chuyển Form (có sự thay đổi vị trí của<br>Form) |
| StyleChanged | Xảy ra khi thuộc tính FormBorderStyle<br>của Form thay<br>đổi |
| TextChanged | Xảy ra khi thuộc tính Text<br>của Form thay đổi. |

============== VTNET - Duong ==============

{3}

{page_id}-{48}

## **4. Minh họa một số sự kiện của Form (Code) (Với Form có tên là frmForm)**

#### Sự kiện FormClosed

//Sự kiện FormClosed - Sự kiện này được gọi khi Form đã đóng private void frmForm\_FormClosed(object sender, FormClosedEventArgs e) {

MessageBox.Show("Sự kiện FormClosed được gọi",

"FormClosed",MessageBoxButtons.OK,MessageBoxIcon.Information); }

# Sự kiện FormClosing

//Sự kiện FormClosing xảy ra khi Form đang đóng private void frmForm\_FormClosing(object sender, FormClosingEventArgs e) {

if (MessageBox.Show("Bạn có muốn đóng Form lại hay không?", "FormClosing",

```
MessageBoxButtons.YesNo, MessageBoxIcon.Information) == 
DialogResult.Yes)
```

e.Cancel = false;// Đóng Form lại

else

e.Cancel = true;//Không đóng Form nữa

}

4.3. Sự kiện KeyPress

//Sự kiện KeyPress

```
private void frmForm_KeyPress(object sender, KeyPressEventArgs e)
{
```

```
//Nếu không chỉ rõ phím nào được nhấn thì khi nhấn bất cứ phím nào sự 
kiện KeyPress của Form đều xảy ra
```

```
//Chỉ rõ phím nào được nhấn thì phát sinh sự kiện KeyPress làm như sau
if (e.KeyChar = 'a')
```

```
MessageBox.Show("Sự kiện KeyPress xảy ra khi bạn nhấn phím a");
```

```
}
```

//Sự kiện KeyUp tương tự như sự kiện KeyPress

============== VTNET - Duong ==============

```
//Chỉ rõ phím nào được nhấn thì phát sinh sự kiện KeyPress làm như sau
if (e.KeyChar = 'a')
```

```
MessageBox.Show("Sự kiện KeyPress xảy ra khi bạn nhấn phím a");
```

```
}
```

//Sự kiện KeyUp tương tự như sự kiện KeyPress

//Sự kiện KeyDown xảy ra khi nhấn một phím hay tổ hợp phím

# 4.4. Sự kiện KeyDown

private void frmForm\_KeyDown(object sender, KeyEventArgs e)

{

//khi nhấn một phím bất kì trên bàn phím thì sự kiện KeyPress được gọi //Đồng thời sự kiện KeyDown cũng được gọi → KeyPress là trường hợp riêng của KeyDown

//Áp dụng: Nhấn một tổ hợp phím thì sự kiện KeyDown mới được gọi //Như Windows Media: Nhấn Ctrl+F để di chuyển bài tiếp theo

if (e.KeyCode == Keys.F && e.Modifiers == Keys.Control) MessageBox.Show("Sự kiện KeyDown được gọi khi bạn nhấn Ctrl + F");

{4}

{page_id}-{48}

============== VTNET - Duong ==============

if (e.KeyCode == Keys.F && e.Modifiers == Keys.Control) MessageBox.Show("Sự kiện KeyDown được gọi khi bạn nhấn Ctrl + F");

{4}

{page_id}-{48}

| } |
|------------------------------------------------------------------------------------------------------------------------------|
| 4.5.<br>Sự kiện MouseClick<br>//Sự kiện MouseClick |
| private<br>void<br>frmForm_MouseClick(object<br>sender, MouseEventArgs<br>e)<br>{ |
| //Nếu bạn không muốn biết người dùng nhấn chuột TRÁI hay PHẢI hay<br>GIỮA thì khi nhấn bất kì |
| //Chuột nào cũng xảy ra sự kiện MouseClick của Form<br>//Còn nếu bạn muốn bắt được sự kiện người dùng nhấn chuột TRÁI, PHẢI, |
| hay GIỮA làm thế này |
| if<br>(e.Button == MouseButtons.Left)<br>MessageBox.Show("Sự kiện MouseClick xảy ra khi bạn Click chuột |
| TRÁI"); |
| else<br>if<br>(e.Button==MouseButtons.Middle)<br>MessageBox.Show("Sự kiện MouseClick xảy ra khi bạn Click chuột |
| GIỮA");<br>else<br>if<br>(e.Button==MouseButtons.Right) |
| MessageBox.Show("Sự kiện MouseClick xảy ra khi bạn Click chuột<br>PHẢI"); |
| } |

# **//Các sự kiện MouseDoubleClick, MouseDown, MouseUp... Xử lý tương tự**