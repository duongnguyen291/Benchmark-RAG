

{0}------------------------------------------------

**Parcels :** lô / mảnh đất

**Survey :** nhìn lại / bản đồ

từ khung Toolspace (bên trái) => Drawing Template =>AutoCad => AutoCad
Civil 3D (Metric) NCS => chuột phải => Creat new drawing.

- Lệnh tắt để chuyển cửa sổ từ file sang file khác : Ctrl + Tab

- **Phương pháp chép lại giữ nguyên vị trí (điểm)**
  Edit => copy => Edit => Paste to Ogirinal Coordinates

- **Đây là cách xem thuộc tính đơn vị đo của bản vẽ**

Toolspace => Ta chọn thẻ Setting bên phải => phải chuột => Edit drawing

setting => Units ... => metter, 1/1000 là ok

Bên Toolspaces => Drawing 2 => Definition => Drawing Object => phải
chuột => add => sau khi hiện ra 1 bảng ta chọn Text => ok => khối chọn các điểm
cần lên địa hình => enter

- Đem điểm text lên cao độ địa hình : ở đây ta phải hiểu là do lúc đầu định
  dạng điểm chỉ có X,Y Z=0 nên ta phải đem lên cao độ thực địa để tính toán

Menu surfaces => Ultilities => Move text to elevation => khối chọn các điểm text => enter .

- Một số thuật ngữ trong Surfaces Style (phải chuột trên các đường đồng mức)
- Contour Interval: khoảng không gian đường đồng mức

- Minor Interval : khoảng cách đờm con

- Major Interval : khoảng cách đđm chính (chú ý = 5 lần đđm con)

{1}------------------------------------------------

Các đường này ta chọn bóng đèn sáng là mở - ngược lại là tắt (có thể chọn màu
cho các đường thể hiện)

- Menu Surfaces :

- Add surfaces labels : tạo nhãn bề mặt

- Spot elevation : cao độ điểm ---- ta có thể dùng điểm này để kiểm tra cao độ
  đường đồng mức

Khi chọn đậm => phải chuột => surfaces properties... => ở thẻ analysis ta có
thể tô màu theo độ cao cho địa hình được chọn như sau

...Sau đó ta tạo mặt mới từ 4 điểm hoặc các đường này = cách : menu surfaces=>
creat surfaces => ta đặt tên là **thietke** => ok. Lúc này trên bảng **toolspaces** sẽ hiện ra
1 tên mặt mới là thietke nhưng vẫn chưa có mặc định gì – ta chọn thietke

efinition => drawing object => add => hiện ra 1 bảng ta chọn **Text** => click chọn 4
điểm => enter là xong sẽ hiện ra 1 mặt mới là thietke.

{2}------------------------------------------------

- Sau khi tạo mặt thiết kế chồng lên điạ hình tự nhiên thì nhiều hình , số , màu sắc quá

=> **ta bỏ bớt** = cách phải chuột vào đđm => ...=> display => ta chỉ chừa lại đường biên thôi (border) còn lại thì tắt đèn hết cho dễ nhìn . ok

------ Nhưng ở đây ta tắt là tắt luôn của cả 2 mặt nên ta phải tạo lại **1 mặt tô màu mới** cho thietke = cách : chọn đường bao thietke => phải chuột => surfaces properties => ta chọn **information** – nhìn bên dưới **surfaces style** ta chọn hình tam giác đen bên phải nó => chọn **creat new** => đặt tên là thietke 1 hay gì đó cũng đc => qua thẻ analysis ta cũng tạo lại các lớp màu cao độ => xong. ------ sau đó ta lại phải chuột vào edit surfaces... => mở đèn đđm , slope , spot srrow ... là ok.
------ ta có thể gán giá trị cho các đđm của thietke bước ở trên.

\$\Longrightarrow\$ ta có thê gán giá trị cho các đđm của thietke bước ở trên.

- Rồi từ đây ta sẽ lấy 1 số cao độ tại các điểm giao : => menu surfaces => add surfaces label => spot elevation => enter thì nó sẽ hiện ra 2 mặt cho mình chọn - ở đây chọn mặt nào cũng được nhưng chọn mặt điạ hình tự nhiên gọn hơn .

=➔ click chọn vào 1 điểm giao – nó sẽ hiện ra EL .... : không cần quan tâm vì mình sẽ tạo 1 cái mới từ nó = cách : phải chuột vào nó => **edit label style** hiện ra 1 bảng ta chọn tam giác đen => creat new - ta đặt tên là caodonut => ok

------ qua thẻ general => layor ta chọn dấu ... => new => đặt tên – chọn màu ...

-----qua thẻ Layout => name : CDTN (cao độ tự nhiên) rồi chọn dấu **tam giác đen** ở
trên kế bên chữ A+ => chọn **reference Text** => hiện ra 1 bảng ta chọn **Surfaces**
----- trở lại Name : ta ghi CDTK (Cao độ thiết kế )

-----xong rồi chọn xuống chỗ text => content => chọn dấu ... nó sẽ hiện ra 1 bảng
cho mình đánh cấu trúc nhãn vào .

----ở mục properties ta chọn surfaces Elevation để tùy chỉnh các mục thập phân ...
----xong ta chọn dấu muỗi tên ngang màu trắng => ok.

=> Ok => ok là xong phần này – ta vẽ thử 1 điểm thì nó ra dấu ? –

----chọn menu general => add label => hiện ra 1 bảng

---feature => ta chọn surfaces

---label type => ta chọn Spot Elevation

{3}------------------------------------------------

**CHÚ Ý** : Có thể nó hiện ra tới 3 4 dòng gì đó thể hiện cao độ nhưng mình chỉ
muốn có 2 dòng thôi thì .TA LÀM : phải chuột tại 1 điểm có cao độ (không đúng ý
) vào edit label style => bấm nút **hìng vuông + tam giác den** để vào lại phần chi tiết
----Ở đây , trong thẻ Layout – phần Component Name : nếu ta thấy có những cái tên
ko cần có thể chọn **dấu X** màu đỏ để bỏ .

----Xong sau đó ta có thể thao tác lại như tuỳ chỉnh bỏ bớt các chũ thừa = **Content**
=> dấu ...

--- ta có thể edit lại :

--component name : chọn tên surfaces slope

--content : chọn ...

--hiện ra 1 bảng : trong phần properties ta có thể them khoảng cách = cách chọn :
Surfaces Slope Distance => chọn dấu muỗi tên cho nó qua

--Xong ra ngoài Layout chỗ component name ta chọn Direction Arrow – để tuỳ chỉnh fix length = giá trị True và cách osset Y lên (nếu cần)