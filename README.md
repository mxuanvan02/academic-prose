# academic-vi

`academic-vi` là Agent Skill chuyên kiến tạo, dịch, biên tập và kiểm định nội
dung học thuật bằng tiếng Việt. Skill không chỉ sửa câu chữ ở bước cuối mà tổ
chức nội dung từ **tuyên bố, bằng chứng và mục đích tu từ** trước khi viết.

Nguyên tắc trung tâm:

> Tuyên bố và bằng chứng có trước câu chữ; toàn vẹn ngữ nghĩa có trước độ trôi
> chảy.

## Vì sao cần academic-vi?

Một văn bản có vẻ trang trọng chưa chắc đã là văn bản học thuật tốt. Những lỗi
nghiêm trọng thường nằm dưới bề mặt ngôn ngữ: khẳng định mạnh hơn bằng chứng,
đổi tương quan thành quan hệ nhân quả, nhập kết quả với diễn giải, dùng thuật
ngữ không nhất quán hoặc bê nguyên cú pháp và tên trường dữ liệu từ tài liệu kỹ
thuật vào bài báo.

`academic-vi` xử lý các vấn đề đó bằng một quy trình viết có thể kiểm tra:

1. xác định thể loại, độc giả, mục đích và phạm vi;
2. lập bản đồ giữa tuyên bố và bằng chứng;
3. thiết kế cấu trúc lập luận và chức năng từng đoạn;
4. khóa thuật ngữ ở cấp tài liệu;
5. viết bằng tiếng Việt học thuật tự nhiên;
6. phản biện đối nghịch và kiểm định trước khi bàn giao.

Skill không tạo uy tín học thuật bằng cách bịa dữ liệu, nguồn dẫn hoặc lời giải
thích. Nội dung chưa có căn cứ phải được đánh dấu `needs_source`, thu hẹp mức
khẳng định hoặc tách khỏi bản thảo.

## Phạm vi sử dụng

Skill được định tuyến theo **mục đích học thuật**, không theo đuôi tệp. Khi nội
dung tiếng Việt phục vụ nghiên cứu, khoa học hoặc giáo dục đại học,
`academic-vi` có thể tự động được chọn cho:

- bài báo, luận văn, luận án, báo cáo và đề cương nghiên cứu;
- tóm tắt, tổng quan, phương pháp, kết quả, thảo luận và kết luận;
- slide báo cáo khoa học và lời thuyết trình;
- bài giảng, giáo án, học liệu và đề cương môn học;
- câu hỏi, bài tập và nội dung đánh giá học tập;
- dịch Anh - Việt, diễn đạt lại, rút gọn, mở rộng và biên tập học thuật;
- kiểm định lập luận, bằng chứng, thuật ngữ và văn phong của bản thảo có sẵn.

Việc tự động kích hoạt phụ thuộc vào cơ chế khám phá năng lực của tác tử hoặc
môi trường điều phối đang sử dụng. `SKILL.md` khai báo các tín hiệu định tuyến
chung; cú pháp gọi phụ thuộc vào môi trường. Nếu môi trường không hỗ trợ tự
động định tuyến, người dùng chỉ cần nêu rõ yêu cầu áp dụng `academic-vi` trong
lời nhắc.

Nội dung tiếng Việt thông thường chỉ nhắc đến một chủ đề kỹ thuật không mặc
nhiên thuộc phạm vi này. Mục đích giao tiếp phải thực sự là học thuật, nghiên
cứu, khoa học hoặc giảng dạy ở cấp phù hợp.

## Năng lực

`academic-vi` dùng chung một động cơ kiến tạo diễn ngôn cho 12 thao tác:

| Năng lực | Khi sử dụng | Sản phẩm chính |
| --- | --- | --- |
| `conceptualize` | Chủ đề chưa thành vấn đề viết có thể bảo vệ | Hồ sơ tu từ và cấu trúc tuyên bố sơ bộ |
| `outline` | Cần kiến trúc bài, chương hoặc báo cáo | Dàn ý có chức năng và quan hệ phụ thuộc |
| `argue` | Cần xây dựng hoặc giới hạn một lập trường | Bản đồ tuyên bố - bằng chứng - bảo chứng |
| `synthesize` | Cần tổng hợp nhiều nguồn đã cung cấp | Tổng hợp theo chủ đề, điểm hội tụ và bất đồng |
| `draft` | Đã đủ vật liệu để viết mới | Văn bản học thuật tiếng Việt hoàn chỉnh |
| `develop` | Ghi chú hoặc đoạn viết còn thiếu chiều sâu | Lập luận đầy đủ hơn nhưng không thêm dữ kiện giả |
| `compress` | Cần rút gọn bài hoặc nội dung slide | Bản ngắn hơn, giữ phạm vi và điều kiện thiết yếu |
| `expand` | Cần làm rõ hoặc phát triển nội dung | Bản mở rộng và danh sách phần còn thiếu nguồn |
| `paraphrase` | Cần đổi cách diễn đạt, giữ nguyên nội dung | Văn bản diễn đạt lại với ngữ nghĩa ổn định |
| `revise` | Bản thảo cần sửa ở cấp nội dung và diễn ngôn | Bản sửa cùng kiểm toán thay đổi |
| `audit` | Cần đánh giá mà không âm thầm viết lại | Phát hiện theo mức độ và quyết định cổng |
| `translate` | Chuyển nội dung học thuật sang tiếng Việt | Bản dịch, bảng thuật ngữ và kiểm toán |

## Cài đặt

Repository không phụ thuộc vào một tác tử duy nhất. Có thể tích hợp bằng bất kỳ
cơ chế nào đọc được hợp đồng trong `SKILL.md` và các tài liệu tham chiếu đi
kèm. Lệnh dưới đây là một cách cài đặt cho môi trường hỗ trợ trình quản lý
Agent Skills tương thích:

```bash
npx skills add mxuanvan02/academic-vi -g --all
```

Khi tích hợp thủ công, đặt repository tại vị trí mà môi trường có thể khám phá
và đăng ký `SKILL.md` làm hợp đồng định tuyến chính. Tệp
`agents/openai.yaml` chỉ là bộ điều hợp giao diện tùy chọn cho các môi trường
tương thích; nó không xác định hành vi cốt lõi của dự án.

## Cách sử dụng

### Viết bài từ bằng chứng

```text
Viết phần Thảo luận bằng tiếng Việt từ các kết quả và nguồn dưới đây. Lập sổ
tuyên bố - bằng chứng, đánh dấu nội dung cần nguồn, thiết kế tiến trình đoạn
văn, sau đó viết và phản biện đối nghịch.
```

### Xây dựng lập luận trước khi viết

```text
Xác định vấn đề nghiên cứu, phạm vi, giả định và cấu trúc tuyên bố. Tạo dàn ý
chú giải bằng tiếng Việt; không trình bày nội dung chưa có bằng chứng như một
sự thật đã xác lập.
```

### Dịch học thuật Anh - Việt

```text
Dịch phần tóm tắt này sang tiếng Việt học thuật. Giữ nguyên mức độ khẳng định,
số liệu, trích dẫn và thuật ngữ; trả kèm bảng thuật ngữ và kiểm toán các điểm
có nguy cơ lệch nghĩa.
```

### Biên tập một bản thảo tiếng Việt

```text
Biên tập phần Kết quả này theo chuẩn tiếng Việt học thuật. Phát hiện tuyên bố
vượt bằng chứng, nhiễu cú pháp tiếng Anh, thuật ngữ trôi nghĩa, chi tiết triển
khai thừa và câu chữ không tự nhiên. Không tự bổ sung dữ kiện hoặc nguồn dẫn.
```

### Soạn slide báo cáo khoa học

```text
Tạo slide báo cáo nghiên cứu bằng tiếng Việt. Xây dựng mạch lập luận, tiêu đề
mang thông điệp, nội dung từng slide, thuật ngữ và lời thuyết trình; dùng công
cụ trình chiếu cho bố cục, phân cấp thị giác và xuất tệp.
```

Với slide, mỗi trang nên có một chức năng giao tiếp và một tuyên bố chính. Việc
rút gọn không được làm mất điều kiện, giới hạn, nguồn dẫn hoặc thay đổi ý nghĩa
khoa học. Lời thuyết trình không được mâu thuẫn hay nâng mức khẳng định so với
nội dung trên trang.

### Soạn bài giảng và học liệu

```text
Xây dựng bài giảng đại học bằng tiếng Việt từ các tài liệu này. Xác định người
học, kiến thức đầu vào và chuẩn đầu ra; thiết kế phần giải thích, ví dụ, hoạt
động thực hành và đánh giá sao cho liên kết với nhau.
```

### Phối hợp với dịch PDF

```text
Trích xuất nội dung PDF ở chế độ bàn giao, dịch sang tiếng Việt học thuật rồi
tái dựng tệp. Giữ nguyên công thức, ký hiệu, số liệu và trích dẫn; kiểm định
mức độ khẳng định khoa học trước khi hoàn tất.
```

Trong cách phối hợp này, `academic-vi` chịu trách nhiệm về nội dung tiếng Việt;
công cụ PDF chịu trách nhiệm về trích xuất, bố cục và tái dựng tệp.

## Quy trình viết

Mọi tác vụ viết đáng kể đi qua bảy bước, với độ sâu tỷ lệ theo độ phức tạp:

1. **Hồ sơ tu từ**: ngành, thể loại, độc giả, chức năng phần, mục đích, câu hỏi trung tâm, độ dài và ràng buộc.
2. **Sổ tuyên bố - bằng chứng**: phân biệt dữ kiện được cung cấp, lập trường tác giả, suy luận có căn cứ và nội dung cần nguồn.
3. **Kiến trúc diễn ngôn**: sắp xếp tuyên bố chính, luận cứ, bằng chứng, bảo chứng, giới hạn, phản đề và hàm ý.
4. **Thiết kế đoạn**: giao cho mỗi đoạn một chức năng tu từ chính và một chuỗi chuyển động có kiểm soát.
5. **Soạn thảo**: hiện thực hóa kiến trúc bằng tiếng Việt đương đại, thuật ngữ ổn định và mức khẳng định phù hợp.
6. **Phản biện đối nghịch**: truy từng phát biểu thực nghiệm về bằng chứng, kiểm tra liên từ, phạm vi và lỗ hổng logic.
7. **Sửa và qua cổng**: xử lý lỗi bằng chứng, cấu trúc, lập trường và nhất quán trước khi đánh bóng câu chữ.

Với yêu cầu ngắn, các hiện vật trung gian có thể được giữ ngầm. Hợp đồng về
bằng chứng và không bịa đặt vẫn được áp dụng đầy đủ.

## Tiêu chuẩn tiếng Việt học thuật

Skill ưu tiên theo thứ tự:

**nghĩa -> thuật ngữ -> lập trường khoa học -> logic -> diễn đạt tiếng Việt -> hình thức**

Một lớp phía sau không được làm hỏng lớp phía trước. Một số nguyên tắc chính:

- dùng cấu trúc chủ thể - hành động - đối tượng khi bằng chứng cho phép;
- thay danh hóa rỗng bằng động từ, nhưng giữ thuật ngữ đã ổn định trong ngành;
- không dịch từng từ hoặc bê nguyên kết hợp từ của tiếng Anh;
- chỉ dùng bị động khi đối tượng chịu tác động hoặc quy trình là trọng tâm;
- ưu tiên lặp lại thuật ngữ chính xác hơn thay từ đồng nghĩa để trang trí;
- không dùng văn phong khoa trương, báo chí hoặc hành chính để tạo vẻ học thuật;
- không biến “gợi ý” thành “khẳng định”, “liên quan” thành “gây ra”;
- không thêm lời giải thích chỉ để câu văn có vẻ đầy đủ.

## Trừu tượng hóa cho văn bản công bố

Bài báo và luận văn phải nói bằng khái niệm khoa học, không bằng chi tiết lưu
trữ nội bộ. Tên trường lược đồ, khóa cấu hình, cờ trạng thái, tên thư mục và
nhãn vận hành không nên xuất hiện trong lập luận chính chỉ vì chúng có trong
mã nguồn hoặc thẻ dữ liệu.

Ví dụ, bài báo nên nêu rằng dữ liệu được chia ở cấp tài liệu và vị trí đáp án
được cân bằng bằng quy trình tất định. Tên kỹ thuật của các trường dùng để lưu
những giá trị đó thường chỉ cần nằm trong thẻ dữ liệu hoặc tài liệu API.

Ngược lại, tên mô hình, phần mềm, tham số hoặc mã định danh vẫn phải được giữ
khi chúng cần cho khả năng tái lập, xác định đúng đối tượng nghiên cứu hoặc
tránh nhập nhằng phương pháp. Việc trừu tượng hóa không được che giấu một lựa
chọn phương pháp có ảnh hưởng đến kết quả.

## Cổng chất lượng

Mỗi sản phẩm đáng kể được đánh giá trên sáu chiều, theo thang 0-5:

| Mã | Chiều đánh giá | Yêu cầu |
| --- | --- | --- |
| `SEM` | Toàn vẹn tuyên bố và bằng chứng | Mọi phát biểu có căn cứ hoặc được giới hạn rõ |
| `TERM` | Thuật ngữ | Đúng nghĩa chuyên ngành và nhất quán toàn tài liệu |
| `STANCE` | Lập trường khoa học | Đúng mức độ chắc chắn, quan hệ nhân quả và phạm vi suy luận |
| `LOGIC` | Lập luận và diễn ngôn | Quan hệ tuyên bố - bằng chứng và chức năng các phần rõ ràng |
| `VI` | Độ tự nhiên của tiếng Việt học thuật | Cú pháp, kết hợp từ, văn phong và luồng thông tin phù hợp |
| `CONS` | Tính nhất quán | Tên gọi, viết tắt, thời, định dạng và chính sách thuật ngữ ổn định |

Quyết định `pass` yêu cầu mọi chiều đạt ít nhất 4/5 và không có lỗi chặn. Một
điểm trung bình cao không thể bù cho lỗi đảo nghĩa, mất phủ định, nâng quan hệ
thành nhân quả, sai số liệu, hỏng trích dẫn, đổi phạm vi hoặc bịa bằng chứng.

Các quyết định có thể là:

- `pass`: đạt cổng và không còn thuật ngữ chưa giải quyết;
- `revise`: còn lỗi lớn nhưng có thể sửa bằng bằng chứng hiện có;
- `human_review`: nhập nhằng còn lại ảnh hưởng đến nội dung pháp lý, lâm sàng,
  khoa học, thuật ngữ trọng yếu hoặc thành phần được bảo vệ.

## Kết quả đầu ra

Với tác vụ viết mới đáng kể, skill ưu tiên trả văn bản sạch trước, sau đó báo
cáo ngắn gọn:

- các giả định đã sử dụng;
- tuyên bố còn ở trạng thái `needs_source`;
- lựa chọn thuật ngữ quan trọng;
- rủi ro lập luận hoặc phạm vi cần con người xem xét.

Với dịch hoặc biên tập đáng kể, đầu ra có thể gồm hồ sơ, bảng thuật ngữ, văn
bản đã sửa, kiểm toán thay đổi và quyết định cổng. Các schema JSON trong
`schemas/` hỗ trợ đầu ra có cấu trúc khi quy trình máy yêu cầu.

## Kiến trúc kho mã

```text
academic-vi/
├── SKILL.md                         # Hợp đồng và bộ định tuyến chính
├── agents/openai.yaml               # Bộ điều hợp giao diện tùy chọn
├── references/
│   ├── academic-vietnamese-standard.md
│   ├── composition-workflow.md
│   ├── capability-matrix.md
│   ├── argument-and-evidence.md
│   ├── genre-playbooks.md
│   ├── deliverable-playbooks.md
│   ├── rhetorical-moves.md
│   ├── writing-failure-taxonomy.md
│   ├── en-vi-transfer-taxonomy.md
│   ├── domain-profiles.md
│   ├── quality-rubric.md
│   └── pdf-translate-integration.md
├── schemas/                         # Lược đồ JSON cho các hiện vật trung gian
├── evals/                           # Tình huống đánh giá tổng hợp, không chứa bản thảo riêng tư
├── scripts/validate_skill.py        # Trình kiểm định cấu trúc và hợp đồng
└── tests/                           # Kiểm thử kho mã và lược đồ
```

## Những việc skill không thực hiện

`academic-vi` không thay thế các công cụ hoặc chuyên gia ở lớp khác:

- không tự tìm tài liệu hoặc phát hiện nguồn dẫn còn thiếu;
- không xác minh DOI, trích dẫn hay dữ kiện với cơ sở dữ liệu bên ngoài;
- không thẩm định thiết kế nghiên cứu, phương pháp thống kê hoặc giá trị pháp lý;
- không tự xác nhận tính đúng đắn lâm sàng, pháp luật hay sư phạm;
- không thao tác bố cục PDF, thiết kế slide hoặc xuất bản tệp;
- không biến đầu ra trôi chảy thành bằng chứng rằng nội dung đã đúng.

Khi cần, hãy phối hợp skill này với công cụ nghiên cứu tài liệu, phản biện
phương pháp, dịch PDF, tạo slide hoặc dàn trang. Ranh giới sở hữu phải rõ:
`academic-vi` kiểm soát nội dung học thuật tiếng Việt; công cụ chuyên dụng kiểm
soát lớp kỹ thuật tương ứng.

## Nguồn tham khảo và quan hệ kế thừa

Dự án tham khảo các nguồn công khai sau đây. Bảng này phân biệt rõ phần được
tham khảo với phần được xây dựng độc lập, tránh tạo ấn tượng rằng toàn bộ dự án
được phân nhánh hoặc sao chép từ một kho mã khác.

| Nguồn | Phạm vi tham khảo | Quan hệ với `academic-vi` |
| --- | --- | --- |
| [Agent Skills](https://github.com/agentskills/agentskills) | Chuẩn đóng gói và tích hợp dựa trên `SKILL.md` | Cung cấp quy ước để môi trường tương thích khám phá và sử dụng năng lực; không phải nguồn của lõi viết học thuật |
| [Vercel Skills](https://github.com/vercel-labs/skills) | Trình cài đặt được minh họa bằng lệnh `npx skills add` | Chỉ là một phương án cài đặt; dự án không phụ thuộc vào một trình cài hoặc môi trường thực thi duy nhất |
| [VI-Translate](https://github.com/breslee1707/VI-Translate) | Quy trình bàn giao dịch PDF, bảo toàn thành phần và tái dựng tài liệu | Là nguồn tham khảo trực tiếp cho lớp phối hợp dịch PDF; không phải nguồn của lõi viết học thuật, cổng chất lượng hoặc các lược đồ dữ liệu |

Lõi kiến tạo diễn ngôn, quy trình tuyên bố - bằng chứng, tiêu chuẩn tiếng Việt
học thuật, cổng chất lượng sáu chiều, các lược đồ và bộ đánh giá trong kho mã
này được phát triển cho `academic-vi`. Nếu một thành phần sau này kế thừa mã
hoặc nội dung từ dự án khác, nguồn và giấy phép tương ứng phải được ghi rõ tại
đây hoặc trong tệp thông báo dành cho bên thứ ba.

## Phát triển và kiểm định

Chạy trình kiểm định:

```bash
python3 scripts/validate_skill.py
```

Chạy toàn bộ kiểm thử:

```bash
python3 -m unittest discover -s tests -v
```

Bộ đánh giá hiện gồm các tình huống tổng hợp cho viết mới, dịch và biên tập.
Không có bản thảo riêng tư trong kho mã.

Khi đóng góp một quy tắc mới, cần nêu rõ ngành, thể loại, ngữ cảnh, lý do, ví
dụ đúng, phản ví dụ và phạm vi áp dụng. Không biến một sửa đổi cá biệt thành
quy tắc phổ quát nếu chưa có căn cứ.

## Giấy phép

Dự án được phát hành theo giấy phép [MIT](LICENSE).
