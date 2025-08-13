**FORM**

\*\*\*

1.  **Chức năng**

Form (hay còn gọi điều khiển Form) dùng để chứa các điều khiển khác (Buttons, Label…)

2.  **Một số thuộc tính thường dùng**

Điều khiển Form có một số thuộc tính như sau:

<table>
<colgroup>
<col style="width: 34%" />
<col style="width: 65%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><strong>Tên</strong></th>
<th style="text-align: center;"><strong>Ỹ nghĩa</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>Name</td>
<td style="text-align: left;">Tên của Form. Trong một Project tên của các Form phải khác nhau.</td>
</tr>
<tr>
<td>AcceptButton</td>
<td style="text-align: left;">Giá trị mà thuộc tính này nhận là tên của một Button trên Form (Nếu Form có chứa button). Khi đó nếu bạn nhấn phím <strong>Enter</strong> thì sự kiện Click của Button mà bạn chọn được thực thi mà không cần nhấn chuột vào Button đó.</td>
</tr>
<tr>
<td>Autosize</td>
<td style="text-align: left;"><p>Nhận một trong hai giá trị True hay False</p>
<p>- True: Không cho phép thay đổi kích thước Form mà che đi các điều khiển khác chứa trên Form</p>
<p>- False: Ngược lại</p></td>
</tr>
<tr>
<td>AutoSizeMode</td>
<td style="text-align: left;"><p>Cho phép thay đổi kích thước của Form hay không? (Khi di chuyển chuột vào các mép của Form mà hiện nên biểu tượng <strong>↔︎</strong> là cho phép). Và nhận một trong hai giá trị</p>
<ul>
<li><p>GrowOnly: Cho phép</p></li>
<li><p>và GrowAndShrink: Không cho phép</p></li>
</ul></td>
</tr>
<tr>
<td>BackColor</td>
<td style="text-align: left;">Chọn màu nền cho Form</td>
</tr>
<tr>
<td>BackGroundImage</td>
<td style="text-align: left;">Chọn ảnh làm nền cho Form</td>
</tr>
<tr>
<td>CancelButton</td>
<td style="text-align: left;">Giá trị mà thuộc tính này nhận là tên của một Button trên Form (Nếu Form có chứa button). Khi đó nếu bạn nhấn phím <strong>ESC</strong> thì sự kiện Click của Button mà bạn chọn được thực thi mà không cần nhấn chuột vào Button đó (tương tự như thuộc tính AcceptButton ).</td>
</tr>
<tr>
<td>ControlBox</td>
<td style="text-align: left;"><p>Nhận một trong hai giá trị True hay False</p>
<ul>
<li><p>True: Cho phép các các nút: MaximizeBox, MinimizeBox, Close trên Titlebar xuất hiện</p></li>
<li><p>False: Không Cho phép các các nút: MaximizeBox, MinimizeBox, Close trên Titlebar xuất hiện (Khi đó các thuộc tính MaximizeBox, MinimizeBox của Form cũng mất đi)</p></li>
</ul></td>
</tr>
<tr>
<td>Font</td>
<td style="text-align: left;">Chọn kiểu Font chữ cho Form (Khi đó tất cả các điều khiển được thêm vào Form sẽ có thuộc tính Font giống như thuộc tính Font của Form)</td>
</tr>
<tr>
<td>ForeColor</td>
<td style="text-align: left;">Tương tự như thuộc tính Font nhưng áp dụng đối với màu chữ</td>
</tr>
<tr>
<td>FormBorderStyle</td>
<td style="text-align: left;">Chọn Style cho Form (Có 7 lựa chọn khác nhau).</td>
</tr>
<tr>
<td>HelpButton</td>
<td style="text-align: left;"><p>Nhận một trong hai giá trị True hay False.</p>
<ul>
<li><p>True: Cho phép xuất hiện Buton có dấu <strong>?</strong> trên Titlebar (Với điều kiện: hai thuộc tính MaximizeBox, MaximizeBox phải đặt giá trị là False)</p></li>
<li><p>False: Ngược lại</p></li>
</ul>
<p>→ Thuộc tính này sẽ hay đi kèm với điều khiển <strong>HelpProvider</strong> về sau</p></td>
</tr>
<tr>
<td>Icon</td>
<td style="text-align: left;">Chọn một Icon (có đuôi mở rộng là .ico) trên máy tính của bạn thay cho Icon mặc định của Form mà VS tạo ra</td>
</tr>
<tr>
<td>KeyPreview</td>
<td style="text-align: left;"><p>Nhận một trong hai giá trị True hay False</p>
<ul>
<li><p>True: Cho phép các sự kiện về bàn phím của Form (KeyUp, KeyDown, KeyPress… của Form) có hiệu lực.</p></li>
<li><p>False: Ngược lại</p></li>
</ul></td>
</tr>
<tr>
<td>MaximizeBox</td>
<td style="text-align: left;"><p>Nhận một trong hai giá trị True hay False</p>
<ul>
<li><p>True: Cho phép nút MaximizeBox trên Titlebar có hiệu lực</p></li>
<li><p>False: Ngược lại</p></li>
</ul></td>
</tr>
<tr>
<td>MaximizeBox</td>
<td style="text-align: left;">Tương tự như thuộc tính MaximizeBox</td>
</tr>
<tr>
<td>Opacity</td>
<td style="text-align: left;">Độ trong suốt của Form</td>
</tr>
<tr>
<td>ShowIcon</td>
<td style="text-align: left;"><p>Nhận một trong hai giá trị True hay False</p>
<ul>
<li><p>True: Cho phép xuất hiện Icon của Form</p></li>
<li><p>False: Không cho phép xuất hiện Icon của Form</p></li>
</ul></td>
</tr>
<tr>
<td>ShowInTaskbar</td>
<td style="text-align: left;"><p>Nhận một trong hai giá trị True hay False</p>
<ul>
<li><p>True: Cho phép hiện Form dưới khay Taskbar</p></li>
<li><p>False: Ngược lại</p></li>
</ul></td>
</tr>
<tr>
<td>StartPosition</td>
<td style="text-align: left;">Vị trí hiển thị của Form so với màn hình hệ thống hay Form cha (5 lựa chọn khác nhau)</td>
</tr>
<tr>
<td>Text</td>
<td style="text-align: left;">Giá trị Text của Form</td>
</tr>
<tr>
<td>WindowState</td>
<td style="text-align: left;">Trạng thái hiển thị của Form khi chạy (Khi bạn nhấn vào nút <strong>Run</strong> của VS) (Có 3 lựa chọn khác nhau: Ẩn dưới khay Taskbar, mở rộng hết màn hình…).</td>
</tr>
</tbody>
</table>

3.  **Sự kiện**

Một số sự kiện thường dùng

| **Tên** | **Ỹ nghĩa** |
|----|:---|
| AutoSizeChanged | Xảy ra khi thuộc tính **Autosize** của Form chuyển từ True → False hay ngược lại là False → True. |
| BackColorChanged | Xảy ra khi thuộc tính **BackColor** của Form thay đổi |
| Click | Xảy ra khi người dùng Click chuột vào *vùng làm việc* thuộc Form |
| ControlAdded | Xảy ra khi một điều khiển được Add vào Form |
| ControlRemoved | Xảy ra khi một điều khiển bị xóa khỏi Form |
| CursorChanged | Xảy ra khi thuộc tính **Cursor** của Form thay đổi |
| DoubleClick | Xảy ra khi người dùng DoubleClick vào *vùng làm việc* của Form |
| FontChanged | Xảy ra khi thuộc tính **Font** của Form có sự thay đổi |
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

4.  

5.  **Minh họa một số sự kiện của Form (Code) (Với Form có tên là frmForm)**

    1.  Sự kiện FormClosed

//Sự kiện FormClosed - Sự kiện này được gọi khi Form đã đóng

private void frmForm_FormClosed(object sender, FormClosedEventArgs e)

{

MessageBox.Show("Sự kiện FormClosed được gọi", "FormClosed",MessageBoxButtons.OK,MessageBoxIcon.Information);

}

2.  Sự kiện FormClosing

//Sự kiện FormClosing xảy ra khi Form đang đóng

private void frmForm_FormClosing(object sender, FormClosingEventArgs e)

{

if (MessageBox.Show("Bạn có muốn đóng Form lại hay không?", "FormClosing",

MessageBoxButtons.YesNo, MessageBoxIcon.Information) == DialogResult.Yes)

e.Cancel = false;// Đóng Form lại

else

e.Cancel = true;//Không đóng Form nữa

}

4.3. Sự kiện KeyPress

//Sự kiện KeyPress

private void frmForm_KeyPress(object sender, KeyPressEventArgs e)

{

//Nếu không chỉ rõ phím nào được nhấn thì khi nhấn bất cứ phím nào sự kiện KeyPress của Form đều xảy ra

//Chỉ rõ phím nào được nhấn thì phát sinh sự kiện KeyPress làm như sau

if (e.KeyChar = 'a')

MessageBox.Show("Sự kiện KeyPress xảy ra khi bạn nhấn phím a");

}

//Sự kiện KeyUp tương tự như sự kiện KeyPress

//Sự kiện KeyDown xảy ra khi nhấn một phím hay tổ hợp phím

4.  Sự kiện KeyDown

private void frmForm_KeyDown(object sender, KeyEventArgs e)

{

//khi nhấn một phím bất kì trên bàn phím thì sự kiện KeyPress được gọi

//Đồng thời sự kiện KeyDown cũng được gọi → KeyPress là trường hợp riêng của KeyDown

//Áp dụng: Nhấn một tổ hợp phím thì sự kiện KeyDown mới được gọi

//Như Windows Media: Nhấn Ctrl+F để di chuyển bài tiếp theo

if (e.KeyCode == Keys.F && e.Modifiers == Keys.Control)

MessageBox.Show("Sự kiện KeyDown được gọi khi bạn nhấn Ctrl + F");

}

5.  Sự kiện MouseClick

//Sự kiện MouseClick

private void frmForm_MouseClick(object sender, MouseEventArgs e)

{

//Nếu bạn không muốn biết người dùng nhấn chuột TRÁI hay PHẢI hay GIỮA thì khi nhấn bất kì

//Chuột nào cũng xảy ra sự kiện MouseClick của Form

//Còn nếu bạn muốn bắt được sự kiện người dùng nhấn chuột TRÁI, PHẢI, hay GIỮA làm thế này

if (e.Button == MouseButtons.Left)

MessageBox.Show("Sự kiện MouseClick xảy ra khi bạn Click chuột TRÁI");

else if (e.Button==MouseButtons.Middle)

MessageBox.Show("Sự kiện MouseClick xảy ra khi bạn Click chuột GIỮA");

else if (e.Button==MouseButtons.Right)

MessageBox.Show("Sự kiện MouseClick xảy ra khi bạn Click chuột PHẢI");

}

**//Các sự kiện MouseDoubleClick, MouseDown, MouseUp... Xử lý tương tự**
