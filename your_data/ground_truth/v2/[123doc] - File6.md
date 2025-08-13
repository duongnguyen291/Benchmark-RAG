**Parcels :** lô / mảnh đất

**Survey :** nhìn lại / bản đồ

- **Cách tạo bản vẽ mới :**

từ khung Toolspace (bên trái) =\&gt; Drawing Template =\&gt;AutoCad =\&gt; AutoCad Civil 3D (Metric) NCS =\&gt; chuột phải =\&gt; Creat new drawing .

- Lệnh tắt để chuyển cửa sổ từ file sang file khác : Ctrl + Tab

- **Phương pháp chép lại giữ nguyên vị trí (điểm)**

Edit =\&gt; copy =\&gt; Edit =\&gt; Paste to Ogirinal Coordinates

- **Đây là cách xem thuộc tính đơn vị đo của bản vẽ**

Toolspace =\&gt; Ta chọn thẻ Setting bên phải =\&gt; phải chuột =\&gt; Edit drawing setting =\&gt; Units … =\&gt; metter , 1/1000 là ok

- **Tạo surface mới :**

Menu Surface =\&gt; creat surface =\&gt; đặt tên =\&gt; OK

- **tạo mặt địa hình có đường đồng mức**

Bên Toolspaces =\&gt; Drawing 2 =\&gt; Definition =\&gt; Drawing Object =\&gt; phải chuột =\&gt; add =\&gt; sau khi hiện ra 1 bảng ta chọn **Text =\&gt;** ok =\&gt; khối chọn các điểm cần lên địa hình =\&gt; enter

- **Đem điểm text lên cao độ địa hình :** ở đây ta phải hiểu là do lúc đầu định dạng điểm chỉ có X,Y Z=0 nên ta phải đem lên cao độ thực địa để tính toán

Menu surfaces =\&gt; Ultilities =\&gt; Move text to elevation =\&gt; khối chọn các điểm text =\&gt; enter .

- Một số thuật ngữ trong Surfaces Style (phải chuột trên các đường đồng mức)

\+ Contour Interval : khoảng không gian đường đồng mức

\+ Minor Interval : khoảng cách đđm con

\+ Major Interval : khoảng cách đđm chính (chú ý = 5 lần đđm con)

- Thẻ Display :

\+ Slope : độ dốc

\+ Slope arrow : muỗi tên chỉ độ dốc

\+ Border : đường viền

…. Các đường này ta chọn bóng đèn sáng là mở - ngược lại là tắt (có thể chọn màu cho các đường thể hiện)

- Menu Surfaces :

\+ Add surfaces labels : tạo nhãn bề mặt

\+ Spot elevation : cao độ điểm ---- ta có thể dùng điểm này để kiểm tra cao độ đường đồng mức

- Khi chọn đđm =\&gt; phải chuột =\&gt; surfaces properties… =\&gt; ở thẻ analysis ta có thể tô màu theo độ cao cho địa hình được chọn như sau

Ranges – number : ở đây ta chọn số lượng cấp độ mà ta muốn chia ra cao độ (mỗi màu sẽ thể hiện cho 1 khu vực cao độ ) chọn muỗi tên **xuống =\&gt;** ở bên dưới sẽ hiện ra các bảng màu và chiều cao giới hạn trong 1 khoảng ta có thể điều chỉnh.

**….Chú ý** : ở đây nếu sau khi ta chọn xong mà khu đất vẫn không thay đổi màu =\&gt; có nghĩa ta chưa mởa display cao độ =\&gt; phải chuột trên đđm =\&gt; edit surfaces style =\&gt; trong thẻ display ta **mở bóng đèn của mục Elevation lên**

**Thể hiện bảng ghi chú màu cho địa hình** : menu surfaces =\&gt; add legend table =\&gt; nó sẽ hiện ra rất nhiều lựa chọn cho ta như : đđm , độ dốc , muỗi tên độ dốc , cao độ …

- ở đây ta chọn cao độ Elevation =\&gt; click chọn điểm đầu cho bảng =\&gt; xong .

<!-- -->

- **Hiện hướng muỗi tên của độ dốc** – ta vẫn vào thẻ display =\&gt; Spot arrow – ta mở đèn lên =\&gt; ok.

- **Gán cao độ cho đường đm** : vào menu surfaces =\&gt; add surfaces label =\&gt; contour multiple at interval =\&gt; ta sẽ vẽ lên khu đất có chứa đường đm (ta nên vẽ theo hướng mà mình muốn bố trí cao độ và từ thấp tới cao – có nghĩa thường là chéo theo độ dốc ) =\&gt; enter . Để bỏ đi cái đường ta mới vẽ mà ko phải xoá đi sẽ làm mất cao độ -\&gt; ta chọn đường =\&gt; mo =\&gt; enter =\&gt; ở **toolspace** =\&gt; ta chọn **display contour label line** từ **tru**e thành **False** là xong .

- **TẠO MẶT THIẾT KẾ :**

. ..Ta tạo = cách đánh dtext ở 4 điểm hoặc vẽ plyline cũng được .Nếu vẽ = 4 điểm dt thì ta copy và sửa cao độ lại =\&gt; nhớ đem lên cao độ địa hình = cách menu surfaces =\&gt; ullitities =\&gt; chọn cái cuối cùng .

…Sau đó ta tạo mặt mới từ 4 điểm hoặc các đường này = cách : menu surfaces=\&gt; creat surfaces =\&gt; ta đặt tên là **thietke** =\&gt; ok. Lúc này trên bảng **toolspaces** sẽ hiện ra 1 tên mặt mới là thietke nhưng vẫn chưa có mặc định gì – ta chọn thietke – definition =\&gt; drawing object =\&gt; add =\&gt; hiện ra 1 bảng ta chọn **Text** =\&gt; **click chọn 4** **điểm** =\&gt; enter là xong sẽ hiện ra 1 mặt mới là thietke.

- Sau khi tạo mặt thiết kế chồng lên điạ hình tự nhiên thì nhiều hình , số , màu sắc quá =\&gt; **ta bỏ bớt** = cách phải chuột vào đđm =\&gt; …=\&gt; display =\&gt; ta chỉ chừa lại đường biên thôi (border) còn lại thì tắt đèn hết cho dễ nhìn . ok

------- Nhưng ở đây ta tắt là tắt luôn của cả 2 mặt nên ta phải tạo lại **1 mặt tô màu mới** cho thietke = cách : chọn đường bao thietke =\&gt; phải chuột =\&gt; surfaces properties =\&gt; ta chọn **information** – nhìn bên dưới **surfaces style** ta chọn hình tam giác đen bên phải nó =\&gt; chọn **creat new** =\&gt; đặt tên là thietke 1 hay gì đó cũng đc =\&gt; qua thẻ analysis ta cũng tạo lại các lớp màu cao độ … =\&gt; xong . ----- sau đó ta lại phải chuột vào edit surfaces… =\&gt; mở đèn đđm , slope , spot srrow … là ok.

===🡺 ta có thể gán giá trị cho các đđm của thietke bước ở trên.

- **SAU ĐÓ TA VẼ 1 PLYLINE .**

- Rồi từ đây ta sẽ lấy 1 số cao độ tại các điểm giao : =\&gt; menu surfaces =\&gt; add surfaces label =\&gt; spot elevation =\&gt; enter thì nó sẽ hiện ra **2 mặt cho mình chọn** - ở đây chọn mặt nào cũng được **nhưng chọn mặt điạ hình tự nhiên gọn hơn** .

=🡺 click chọn vào 1 điểm giao – nó sẽ hiện ra EL …. : không cần quan tâm vì mình sẽ tạo 1 cái mới từ nó = cách : phải chuột vào nó =\&gt; **edit label style** hiện ra 1 bảng ta chọn **tam giác đen** =\&gt; **creat new** – ta đặt tên là **caodonut** =\&gt; ok

----- qua thẻ general =\&gt; layor ta chọn **dấu …** =\&gt; new =\&gt; đặt tên –chọn màu …

-----qua thẻ Layout =\&gt; name : CDTN (cao độ tự nhiên) rồi chọn **dấu tam giác đen** ở trên kế bên chữ A+ =\&gt; chọn **reference Text =\&gt;** hiện ra 1 bảng ta chọn **Surfaces**

----- trở lại Name : ta ghi **CDTK** (Cao độ thiết kế )

-----xong rồi chọn xuống chỗ text =\&gt; content =\&gt; chọn **dấu …** nó sẽ hiện ra 1 bảng cho mình đánh cấu trúc nhãn vào .

----ở mục properties ta chọn surfaces Elevation để tùy chỉnh các mục thập phân …

----xong ta chọn dấu muỗi tên ngang màu trắng =\&gt; ok.

- Ok =\&gt; ok là xong phần này – ta vẽ thử 1 điểm thì nó ra dấu ? –

- **nên ta mới gán lại từ đầu**

----chọn menu general =\&gt; add label =\&gt; hiện ra 1 bảng

----feature =\&gt; ta chọn surfaces

----label type =\&gt; ta chọn Spot Elevation

----spot Elevation style =\&gt; ta chọn tên cái ta vừa làm ( **caodonut** )

- xong rồi chọn Add là kết thúc Add label .

**CHÚ Ý** : Có thể nó hiện ra tới 3 4 dòng gì đó thể hiện cao độ nhưng mình chỉ muốn có 2 dòng thôi thì .TA LÀM : phải chuột tại 1 điểm có cao độ (không đúng ý ) vào edit label style =\&gt; bấm nút **hìng vuông + tam giác den** để vào lại phần chi tiết

----Ở đây , trong thẻ Layout – phần Component Name : nếu ta thấy có những cái tên ko cần có thể chọn **dấu X** màu đỏ để bỏ .

----Chỉ giữ lại cao độ tk và cao độ tự nhiên ( ở bài này là vậy )

----Xong sau đó ta có thể thao tác lại như tuỳ chỉnh bỏ bớt các chũ thừa = **Content** =\&gt; **dấu …**

----Bên thẻ **Dragged State** - là phần hiệu chỉnh muỗi tên …

----Ta chỉ cần làm ở 1 điểm và Copy lên các điểm còn lại

**TÍNH KHỐI LƯỢNG (TỔNG )**

Vào Menu Surfaces =\&gt; Ulitities =\&gt; Volumes .

Chọn Creat New Volumes Entry : chọn bề mặt (1 cái là địa hình 1 cái là thiết kế )

**GHI ĐỘ DỐC : chú ý rằng độ dốc nếu copy nó ko tự thay đổi như những giá trị khác ở trên nên muốn tính hay vẽ chỗ nào ta phải vẽ hết chứ ko copy kéo qua được .**

**Ta** chọn surfaces =\&gt; add Sufaces label =\&gt; Slope … rồi chọn bề mặt – ta chọn bề mặt thiết kế chứ ko chọn điạ hình làm gì .

----xong ta chọn 2 điểm – vẽ

---- ta có thể edit lại :

--component name : chọn tên **surfaces slope**

--content : chọn **…**

--hiện ra 1 bảng : trong phần **properties ta có thể them khoảng cách** = cách chọn : Surfaces Slope Distance =\&gt; chọn dấu muỗi tên cho nó qua

**Tùy chỉnh them = cách đánh them chữ L phía trước nó và chữ I phía trước độ dốc (surfaces slope )**

--Xong ra ngoài Layout chỗ component name ta chọn Direction Arrow – để tuỳ chỉnh fix length = giá trị True và cách osset Y lên (nếu cần )