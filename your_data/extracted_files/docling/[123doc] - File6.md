Parcels :

lô / m ảnh đấ t

Survey :

nhìn l ạ i / b ản đồ

## -Cách t ạ o b ả n v ẽ m ớ i :

t ừ khung Toolspace (bên trái) =&gt; Drawing Template =&gt;AutoCad =&gt; AutoCad Civil 3D (Metric) NCS =&gt; chu ộ t ph ả i =&gt; Creat new drawing .

- -L ệ nh t ắt để chuy ể n c ử a s ổ t ừ file sang file khác : Ctrl + Tab
- -P hương pháp chép lạ i gi ữ nguyên v ị trí (điể m) Edit =&gt; copy =&gt; Edit =&gt; Paste to Ogirinal Coordinates
- -Đ ây là cách xem thu ộc tính đơ n v ị đo củ a b ả n v ẽ

Toolspace =&gt; Ta ch ọ n th ẻ Setting bên ph ả i =&gt; ph ả i chu ộ t =&gt; Edit drawing setting =&gt; Units … =&gt; metter , 1/1000 là ok

- -T ạ o surface m ớ i :

Menu Surface =&gt; creat surface =&gt; đặ t tên =&gt; OK

- -t ạ o m ặt địa hình có đường đồ ng m ứ c

Bên Toolspaces =&gt; Drawing 2 =&gt; Definition =&gt; Drawing Object =&gt; ph ả i chu ộ t =&gt; add =&gt; sau khi hi ệ n ra 1 b ả ng ta ch ọ n Text =&gt; ok =&gt; kh ố i ch ọn các điể m c ần lên đị a hình =&gt; enter

- -Đem điểm text lên cao độ đị a hình : ở đây ta phả i hi ểu là do lúc đầu đị nh d ạng điể m ch ỉ có X,Y Z=0 nên ta ph ải đem lên cao độ th ực địa để tính toán

Menu surfaces =&gt; Ultilities =&gt; Move text to elevation =&gt; kh ố i  ch ọ n các điể m text =&gt; enter .

- -M ộ t s ố thu ậ t ng ữ trong Surfaces Style (ph ả i chu ột trên các đường đồ ng m ứ c)
+ Contour Interval : kho ảng không gian đường đồ ng m ứ c
+ Minor Interval : kho ảng cách đđm con
+ Major Interval : kho ảng cách đđm chính (chú ý = 5 lần đđm con)
- -Th ẻ Display :
+ Slope : độ d ố

c

+ Slope arrow : mu ỗ i tên ch ỉ độ d ố c
+ Border : đườ ng vi ề n
- …. Các đườ ng này ta ch ọn bóng đèn sáng là mở -ngượ c l ạ i là t ắ t (có th ể ch ọ n màu cho các đườ ng th ể hi ệ n)
- -Menu Surfaces :
+ Add surfaces labels : t ạ o nhãn b ề m ặ t
+ Spot elevation : cao độ điể m ---- ta có th ể dùng điểm này để ki ểm tra cao độ đường đồ ng m ứ c
- -Khi ch ọn đđm =&gt; phả i chu ột =&gt; surfaces properties… =&gt; ở th ẻ analysis ta có th ể tô màu theo độ cao cho địa hình đượ c ch ọ n như sau

Ranges -number : ở đây ta chọ n s ố lượ ng c ấp độ mà ta mu ốn chia ra cao độ (m ỗ i màu s ẽ th ể hi ệ n cho 1 khu v ực cao độ ) ch ọ n mu ỗ i tên xu ố ng  =&gt; ở bên dướ i s ẽ hi ệ n ra các b ả ng màu và chi ề u cao gi ớ i h ạ n trong 1 kho ả ng ta có th ể điề u ch ỉ nh.

- ….Chú ý : ở đây nế u sau khi ta ch ọn xong mà khu đấ t v ẫn không thay đổ i màu =&gt; có nghĩa ta chưa mởa display cao độ =&gt; ph ả i chu ột trên đđm =&gt; edit surfaces style =&gt; trong th ẻ display ta m ở bóng đèn củ a m ụ c Elevation lên
- Th ể hi ệ n b ảng ghi chú màu cho đị a hình : menu surfaces =&gt; add legend table =&gt; nó s ẽ hi ệ n ra r ấ t nhi ề u l ự a ch ọn cho ta như : đđm , độ d ố c , mu ỗi tên độ d ốc , cao độ …
-  ở đây ta chọn cao độ Elevation =&gt; click ch ọn điểm đầ u cho b ả ng =&gt; xong .
- -Hi ện hướ ng mu ỗ i tên c ủa độ d ố c -ta v ẫ n vào th ẻ display =&gt; Spot arrow -ta m ở đèn lên =&gt; ok.
- -Gán cao độ cho đường đm : vào menu surfaces =&gt; add surfaces label =&gt; contour multiple at interval =&gt; ta s ẽ v ẽ lên khu đấ t có ch ứa đường đm (ta nên vẽ theo hướ ng mà mình mu ố n b ố trí cao độ và t ừ th ấ p t ớ i cao -có nghĩa thường là chéo theo độ d ố c ) =&gt; enter . Để b ỏ đi cái đườ ng ta m ớ i v ẽ mà ko ph ải xoá đi sẽ làm m ất cao độ -&gt; ta ch ọn đườ ng =&gt; mo =&gt; enter =&gt; ở toolspace =&gt; ta ch ọ n display contour label line t ừ tru e thành False là xong .

## -T Ạ O M Ặ T THI Ế T K Ế :

- . ..Ta t ạo = cách đánh dtext ở 4 điể m ho ặ c v ẽ plyline cũng đượ c .N ế u v ẽ = 4 điể m dt thì ta copy và  s ửa cao độ l ạ i =&gt; nh ớ đem lên cao độ đị a hình = cách menu surfaces =&gt; ullitities =&gt; ch ọ n cái cu ố i cùng .
- …Sau đó ta tạ o m ặ t m ớ i t ừ 4 điể m ho ặc các đườ ng này = cách : menu surfaces=&gt; creat surfaces =&gt; ta đặ t tên là thietke =&gt; ok. Lúc này trên b ả ng toolspaces s ẽ hi ệ n ra 1 tên m ặ t m ới là thietke nhưng vẫn chưa có mặc đị nh gì -ta ch ọ n thietke -definition =&gt; drawing object =&gt; add =&gt; hi ệ n ra 1 b ả ng ta ch ọ n Text =&gt; click ch ọ n 4 điể m =&gt; enter là xong s ẽ hi ệ n ra 1 m ặ t m ớ i là  thietke.
- -Sau khi t ạ o m ặ t thi ế t k ế ch ồng lên điạ hình t ự nhiên thì nhi ề u hình , s ố , màu s ắ c quá =&gt; ta b ỏ b ớ t = cách ph ả i chu ột vào đđm =&gt; …=&gt; display =&gt; ta chỉ ch ừ a l ại đườ ng biên thôi (border) còn l ạ i thì t ắt đèn hế t cho d ễ nhìn . ok -------Nhưng ở đây ta tắ t là t ắ t luôn c ủ a c ả 2 m ặ t nên ta ph ả i t ạ o l ạ i 1 m ặ t tô màu m ớ i cho thietke = cách : ch ọn đườ ng bao thietke =&gt; ph ả i chu ộ t =&gt; surfaces properties =&gt; ta ch ọ n information -nhìn bên dướ i surfaces style ta ch ọ n hình tam giác đen bên phả i nó =&gt; ch ọ n creat new =&gt; đặt tên là thietke 1 hay gì đó cũng đc =&gt; qua th ẻ analysis ta cũng tạ o l ạ i các l ớp màu cao độ … =&gt; xong . -----sau đó ta lạ i ph ả i chu ột vào edit surfaces… =&gt; mở đèn đđm , slope , spot srrow … là ok. === ➔ ta có th ể gán giá tr ị cho các đđm của thietke bướ c ở trên.

## -SAU ĐÓ TA VẼ 1 PLYLINE .

- -R ồ i t ừ đây ta sẽ l ấ y 1 s ố cao độ t ại các điể m giao : =&gt; menu surfaces =&gt; add surfaces label =&gt; spot elevation =&gt; enter thì nó s ẽ hi ệ n ra 2 m ặ t cho mình ch ọ n -ở đây chọ n m ặt nào cũng đượ c nhưng chọ n m ặt điạ hình t ự nhiên g ọn hơn .
- = ➔ click ch ọn vào 1 điể m giao -nó s ẽ hi ện ra EL …. : không c ầ n quan tâm vì mình s ẽ t ạ o 1 cái m ớ i t ừ nó = cách : ph ả i  chu ộ t vào nó =&gt; edit label style hi ệ n ra 1 b ả ng ta ch ọ n tam giác đen =&gt; creat new -ta đặ t tên là caodonut =&gt; ok
- ----- qua th ẻ general =&gt; layor ta ch ọ n d ấu … =&gt; new =&gt; đặ t tên -ch ọn màu …
- -----qua th ẻ Layout =&gt; name : CDTN (cao độ t ự nhiên) r ồ i ch ọ n d ấu tam giác đen ở trên k ế bên ch ữ A+ =&gt; ch ọ n reference Text =&gt; hi ệ n ra 1 b ả ng ta ch ọ n Surfaces ----- tr ở l ạ i Name : ta ghi CDTK (Cao độ thi ế t k ế )
- -----xong r ồ i ch ọ n xu ố ng ch ỗ text =&gt; content =&gt; ch ọ n d ấu … nó s ẽ hi ệ n ra 1 b ả ng cho mình đánh cấ u trúc nhãn vào .
- ----ở m ụ c properties ta ch ọn surfaces Elevation để tùy ch ỉ nh các m ụ c th ập phân … ----xong ta ch ọ n d ấ u mu ỗ i tên ngang màu tr ắ ng =&gt; ok.
-  Ok =&gt; ok là xong ph ầ n này -ta v ẽ th ử 1 điể m thì nó ra d ấ u ? -

##  nên ta m ớ i gán l ạ i t ừ đầ u

- ----ch ọ n menu general =&gt; add label =&gt; hi ệ n ra 1 b ả ng
- ----feature =&gt; ta ch ọ n surfaces
- ----label type =&gt; ta ch ọ n Spot Elevation
- ----spot Elevation style =&gt; ta ch ọ n tên cái ta v ừ a làm ( caodonut )
-  xong r ồ i ch ọ n Add là k ế t thúc Add label .

CHÚ Ý : Có th ể nó hi ệ n ra t ới 3 4 dòng gì đó thể hi ện cao độ nhưng mình chỉ mu ố n có 2 dòng thôi thì  .TA LÀM : ph ả i chu ộ t t ại 1 điểm có cao độ (không đúng ý ) vào edit label style =&gt; b ấ m nút hìng vuông + tam giác den để vào l ạ i ph ầ n chi ti ế t ----Ở đây , trong thẻ Layout -ph ầ n Component Name : n ế u ta th ấ y có nh ữ ng cái tên ko c ầ n có th ể ch ọ n d ấ u X màu đỏ để b ỏ .

- ----Ch ỉ gi ữ l ại cao độ tk và cao độ t ự nhiên ( ở bài này là v ậ y )
- ----Xong sau đó ta có thể thao tác l ại như tuỳ ch ỉ nh b ỏ b ớt các chũ thừ a = Content =&gt; d ấu …
- ----Bên th ẻ Dragged State - là ph ầ n hi ệ u ch ỉ nh mu ỗi tên …
- ----Ta ch ỉ c ầ n làm ở 1 điểm và Copy lên các điể m còn l ạ i

## TÍNH KH ỐI LƯỢ NG (T Ổ NG )

Vào Menu Surfaces =&gt; Ulitities =&gt; Volumes .

Ch ọ n Creat New Volumes Entry : ch ọ n b ề m ặt (1 cái là đị a hình 1 cái là thi ế t k ế )

## GHI ĐỘ D Ố C : chú ý r ằng độ d ố c n ế u copy nó ko t ự thay đổi như nhữ ng giá tr ị khác ở trên nên mu ố n tính hay v ẽ ch ỗ nào ta ph ả i v ẽ h ế t ch ứ ko copy kéo qua đượ c .

Ta ch ọn surfaces =&gt; add Sufaces label =&gt; Slope … rồ i ch ọ n b ề m ặ t -ta ch ọ n b ề m ặ t thi ế t k ế ch ứ ko ch ọn điạ hình làm gì .

- ----xong ta ch ọn 2 điể m -v ẽ
- ---- ta có th ể edit l ạ i :

--component name : ch ọ n tên surfaces slope

…

- --content : ch ọ n
- --hi ệ n ra 1 b ả ng : trong ph ầ n properties ta có th ể them kho ả ng cách = cách ch ọ n :

Surfaces Slope Distance =&gt; ch ọ n d ấ u mu ỗ i tên cho nó qua

Tùy ch ỉnh them = cách đánh them chữ L phía trướ c nó và ch ữ I phía trước độ d ố c (surfaces slope )

--Xong ra ngoài Layout ch ỗ component name ta ch ọ n Direction Arrow -để tu ỳ ch ỉ nh fix length = giá tr ị True và cách osset Y lên (n ế u c ầ n )