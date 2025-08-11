## FORM

## ***

## 1. Chức năng

Form (hay còn gọi điều khiển Form) dùng để chứa các điều khiển khác (Buttons, Label…)

2. **Một số thuộc tính thường dùng**  
Điều khiển Form có một số thuộc tính như sau:

| **Tên** | **Ỹ nghĩa** |  
|---|---|  
| Name | Tên của Form. Trong một Project tên của các Form phải khác nhau. |  
| AcceptButton | Giá trị mà thuộc tính này nhận là tên của một Button trên Form (Nếu Form có chứa button). Khi đó nếu bạn nhấn phím **Enter** thì sự kiện Click của Button mà bạn chọn được thực thi mà không cần nhấn chuột vào Button đó. |  
| Autosize | Nhận một trong hai giá trị True hay False  \- True: Không cho phép thay đổi kích thước Form mà che đi các điều khiển khác chứa trên Form  \- False: Ngược lại |  
| AutoSizeMode | Cho phép thay đổi kích thước của Form hay không? (Khi di chuyển chuột vào các mép của Form mà hiện nên biểu tượng **↔** là cho phép). Và nhận một trong hai giá trị \- GrowOnly: Cho phép  \- và GrowAndShrink: Không cho phép |  
| BackColor | Chọn màu nền cho Form |  
| BackGroundImage | Chọn ảnh làm nền cho Form |  
| CancelButton | Giá trị mà thuộc tính này nhận là tên của một Button trên Form (Nếu Form có chứa button). Khi đó nếu bạn nhấn phím **ESC** thì sự kiện Click của Button mà bạn chọn được thực thi mà không cần nhấn chuột vào Button đó (tương tự như thuộc tính AcceptButton ). |  
| ControlBox | Nhận một trong hai giá trị True hay False  \- True: Cho phép các các nút: MaximizeBox, MinimizeBox, Close trên Titlebar xuất hiện  \- False: Không Cho phép các các nút: MaximizeBox, MinimizeBox, Close trên Titlebar xuất hiện (Khi đó các thuộc tính MaximizeBox, MinimizeBox của Form cũng mất đi) |  
| Font | Chọn kiểu Font chữ cho Form (Khi đó tất cả các điều khiển được thêm vào Form sẽ có thuộc tính Font giống như thuộc tính Font của Form) |  
| ForeColor | Tương tự như thuộc tính Font nhưng áp dụng đối với màu chữ |  
| FormBorderStyle | Chọn Style cho Form (Có 7 lựa chọn khác nhau). |  
| HelpButton | Nhận một trong hai giá trị True hay False. |  


- ***1 -***

---

|| \- True: Cho phép xuất hiện Buton có dấu **?** trên Titlebar (Với điều kiện: hai thuộc tính MaximizeBox, MaximizeBox phải đặt giá trị là False)  \- False: Ngược lại  → Thuộc tính này sẽ hay đi kèm với điều khiển **HelpProvider** về sau |  
|---|---|  
| Icon | Chọn một Icon (có đuôi mở rộng là .ico) trên máy tính của bạn thay cho Icon mặc định của Form mà VS tạo ra |  
| KeyPreview | Nhận một trong hai giá trị True hay False  \- True: Cho phép các sự kiện về bàn phím của Form (KeyUp, KeyDown, KeyPress… của Form) có hiệu lực.  \- False: Ngược lại |  
| MaximizeBox | Nhận một trong hai giá trị True hay False  \- True: Cho phép nút MaximizeBox trên Titlebar có hiệu lực  \- False: Ngược lại |  
| MaximizeBox | Tương tự như thuộc tính MaximizeBox |  
| Opacity | Độ trong suốt của Form |  
| ShowIcon | Nhận một trong hai giá trị True hay False  \- True: Cho phép xuất hiện Icon của Form  \- False: Không cho phép xuất hiện Icon của Form |  
| ShowInTaskbar | Nhận một trong hai giá trị True hay False  \- True: Cho phép hiện Form dưới khay Taskbar \- False: Ngược lại |  
| StartPosition | Vị trí hiển thị của Form so với màn hình hệ thống hay Form cha (5 lựa chọn khác nhau) |  
| Text | Giá trị Text của Form |  
| WindowState | Trạng thái hiển thị của Form khi chạy (Khi bạn nhấn vào nút **Run** của VS) (Có 3 lựa chọn khác nhau: Ẩn dưới khay Taskbar, mở rộng hết màn hình…). |  


## 3. Sự kiện

Một số sự kiện thường dùng

| **Tên** | **Ỹ nghĩa** |  
|---|---|  
| AutoSizeChanged | Xảy ra khi thuộc tính **Autosize** của Form chuyển từ True → False hay ngược lại là False → True. |  
| BackColorChanged | Xảy ra khi thuộc tính **BackColor** của Form thay đổi |  
| Click | Xảy ra khi người dùng Click chuột vào *vùng làm việc* thuộc Form |  
| ControlAdded | Xảy ra khi một điều khiển được Add vào Form |  
| ControlRemoved | Xảy ra khi một điều khiển bị xóa khỏi Form |  
| CursorChanged | Xảy ra khi thuộc tính **Cursor** của Form thay đổi |  
| DoubleClick | Xảy ra khi người dùng DoubleClick vào *vùng làm việc* của Form |  


- ***2 -***

---

| FontChanged | Xảy ra khi thuộc tính **Font** của Form có sự thay đổi |  
|---|---|  
| ForeColorChanged | Xảy ra khi thuộc tính **ForeColor** của Form có sự thay đổi |  
| FormClosed | Xảy ra khi Form đã đóng (Nhấn vào nút X màu đỏ trên Titlebar) |  
| FormClosing | Xảy ra khi Form đang đóng (2 sự kiện **FormClosed** và **FormClosing** thường dùng trong lập trình CSDL: khi xảy ra sự kiện này thì đóng kết nối CSDL) |  
| KeyDown | Xảy ra khi người dùng nhấn một phím hay một tố hợp phím (tùy thuộc vào xử lý của chúng ta) |  
| KeyPress | Xảy ra khi người dùng **nhấn** một phím |  
| KeyUp | Xảy ra khi người dùng **nhả** một phím. |  
| MouseClick | Xảy ra khi người dùng nhấn chuột (một trong 3 lựa chọn: Trái, giữa, phải) |  
| MouseDoubleClick | Xảy ra khi người dùng **DoubleClick** chuột vào một vùng làm việc của Form(một trong 3 lựa chọn: Trái, giữa, phải) |  
| MouseDown | Xảy ra khi người dùng nhấn chuột |  
| MouseHover | Xảy ra khi người dùng di chuyển vào các *vùng làm việc* Form |  
| MouseLeave | Xảy ra khi di chuyển chuột ra khỏi vùng làm việc của Form |  
| MouseMove | Xảy ra khi di chuyển chuột trên một *vùng làm việc* thuộc Form (nếu Form có chứa một điều khiển nào đó, khi di chuyển chuột trên điều khiển này thì không xảy ra sự kiện **MouseMove** của Form). |  
| MouseUp | Xảy ra khi người dùng nhả nhấn chuột (có thể là chuột trái, chuột phải, chuột giữa - chuột cuộn) |  
| Move | Xảy ra khi di chuyển Form (có sự thay đổi vị trí của Form) |  
| StyleChanged | Xảy ra khi thuộc tính **FormBorderStyle** của Form thay đổi |  
| TextChanged | Xảy ra khi thuộc tính **Text** của Form thay đổi. |  


- ***3 -***

---

4. **Minh họa một số sự kiện của Form (Code) (Với Form có tên là**

##### frmForm)

Sự kiện FormClosed  
//Sự kiện FormClosed - Sự kiện này được gọi khi Form đã đóng  
private void frmForm\_FormClosed(object sender, FormClosedEventArgs e) \{  
MessageBox.Show("Sự kiện FormClosed được gọi", "FormClosed",MessageBoxButtons.OK,MessageBoxIcon.Information);  
\}

## Sự kiện FormClosing

//Sự kiện FormClosing xảy ra khi Form đang đóng  
private void frmForm\_FormClosing(object sender, FormClosingEventArgs e) \{  
if (MessageBox.Show("Bạn có muốn đóng Form lại hay không?", "FormClosing",  
MessageBoxButtons.YesNo, MessageBoxIcon.Information) == DialogResult.Yes)  
e.Cancel = false;// Đóng Form lại  
else  
e.Cancel = true;//Không đóng Form nữa  
\}

## 4.3. Sự kiện KeyPress

//Sự kiện KeyPress  
private void frmForm\_KeyPress(object sender, KeyPressEventArgs e)  
\{  
//Nếu không chỉ rõ phím nào được nhấn thì khi nhấn bất cứ phím nào sự kiện KeyPress của Form đều xảy ra  
//Chỉ rõ phím nào được nhấn thì phát sinh sự kiện KeyPress làm như sau if (e.KeyChar = 'a')  
MessageBox.Show("Sự kiện KeyPress xảy ra khi bạn nhấn phím a");  
\}

# //Sự kiện KeyUp tương tự như sự kiện KeyPress

//Sự kiện KeyDown xảy ra khi nhấn một phím hay tổ hợp phím  
4.4. Sự kiện KeyDown  
private void frmForm\_KeyDown(object sender, KeyEventArgs e)  
\{  
//khi nhấn một phím bất kì trên bàn phím thì sự kiện KeyPress được gọi //Đồng thời sự kiện KeyDown cũng được gọi → KeyPress là trường hợp riêng của KeyDown  
//Áp dụng: Nhấn một tổ hợp phím thì sự kiện KeyDown mới được gọi //Như Windows Media: Nhấn Ctrl+F để di chuyển bài tiếp theo  
if (e.KeyCode == Keys.F && e.Modifiers == Keys.Control) MessageBox.Show("Sự kiện KeyDown được gọi khi bạn nhấn Ctrl + F");

- ***4 -***

---

\}

4.5. Sự kiện MouseClick  
//Sự kiện MouseClick  
private void frmForm\_MouseClick(object sender, MouseEventArgs e)  
\{  
//Nếu bạn không muốn biết người dùng nhấn chuột TRÁI hay PHẢI hay GIỮA thì khi nhấn bất kì  
//Chuột nào cũng xảy ra sự kiện MouseClick của Form  
//Còn nếu bạn muốn bắt được sự kiện người dùng nhấn chuột TRÁI, PHẢI, hay GIỮA làm thế này  
if (e.Button == MouseButtons.Left)  
MessageBox.Show("Sự kiện MouseClick xảy ra khi bạn Click chuột TRÁI");  
else if (e.Button==MouseButtons.Middle)  
MessageBox.Show("Sự kiện MouseClick xảy ra khi bạn Click chuột GIỮA");  
else if (e.Button==MouseButtons.Right)  
MessageBox.Show("Sự kiện MouseClick xảy ra khi bạn Click chuột PHẢI");  
\}

### //Các sự kiện MouseDoubleClick, MouseDown, MouseUp... Xử lý tương tự

- ***5 -***

