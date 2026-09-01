# Academic Prose

[![validate](https://github.com/mxuanvan02/academic-prose/actions/workflows/validate.yml/badge.svg)](https://github.com/mxuanvan02/academic-prose/actions/workflows/validate.yml)

Agent Skill song ngữ để kiến tạo, dịch, biên tập, humanize và kiểm định diễn ngôn
học thuật tiếng Việt và tiếng Anh. Skill tổ chức nội dung từ tuyên bố, bằng chứng
và mục đích tu từ, sau đó hiện thực hóa thành văn bản trong ngôn ngữ đích.

> Tuyên bố và bằng chứng có trước câu chữ; toàn vẹn ngữ nghĩa có trước độ trôi chảy.

Một văn bản trang trọng chưa chắc là văn bản học thuật tốt. Lỗi nghiêm trọng
thường nằm dưới bề mặt ngôn ngữ: khẳng định mạnh hơn bằng chứng, đổi tương quan
thành nhân quả, nhập kết quả với diễn giải, thuật ngữ trôi nghĩa, hoặc bê nguyên
cú pháp tiếng Anh và tên trường dữ liệu vào bài báo. Skill xử lý các lỗi đó bằng
một quy trình bảy bước có thể kiểm tra, và đánh dấu `needs_source` cho mọi nội
dung chưa có căn cứ thay vì viết trơn qua.

## Cài đặt

Cài đặt bằng trình quản lý Skills:

```bash
npx skills add mxuanvan02/academic-prose -g --all
```

Khi tích hợp thủ công, đặt repository tại vị trí môi trường có thể khám phá và
đăng ký `SKILL.md` làm hợp đồng định tuyến chính. `agents/openai.yaml` cung cấp
metadata giao diện cho môi trường tương thích.

## Cách sử dụng

Skill được định tuyến theo mục đích học thuật của nội dung, không theo loại tệp
hay định dạng đầu ra. Nó tự kích hoạt cho bài báo, luận văn, báo cáo, đề cương,
slide khoa học, bài giảng, học liệu, nội dung đánh giá, dịch Anh - Việt và kiểm
định bản thảo. `SKILL.md` khai báo tín hiệu định tuyến chung; cú pháp gọi phụ
thuộc vào môi trường.

```text
Viết phần Thảo luận bằng tiếng Việt từ các kết quả dưới đây. Lập sổ tuyên bố -
bằng chứng, đánh dấu nội dung cần nguồn, sau đó viết và phản biện đối nghịch.
```

```text
Dịch phần tóm tắt này sang tiếng Việt học thuật. Giữ nguyên mức độ khẳng định,
số liệu, trích dẫn và thuật ngữ; trả kèm bảng thuật ngữ và kiểm toán.
```

```text
Biên tập phần Kết quả theo chuẩn tiếng Việt học thuật. Phát hiện tuyên bố vượt
bằng chứng, nhiễu cú pháp tiếng Anh và thuật ngữ trôi nghĩa. Không bổ sung dữ kiện.
```

Bảy nhóm cách sử dụng được công bố đều có kịch bản mô phỏng tương ứng, nên mỗi
tuyên bố trong tài liệu này đều gắn với một phép kiểm tra chạy được:

| Nhóm | Kịch bản |
| --- | --- |
| Viết từ bằng chứng | `usage-discussion-from-evidence` |
| Lập luận trước khi viết | `usage-argument-outline` |
| Dịch Anh - Việt | `usage-en-vi-translation` |
| Biên tập bản thảo tiếng Việt | `usage-vietnamese-revision` |
| Slide báo cáo khoa học | `usage-research-slides` |
| Bài giảng và học liệu | `usage-university-lesson` |
| Bàn giao dịch PDF | `usage-pdf-handoff` |

Ví dụ đầy đủ cho từng nhóm: [`evals/usage-claim-cases.json`](evals/usage-claim-cases.json).
Ví dụ cho từng năng lực: [`evals/capability-examples.json`](evals/capability-examples.json).

## Năng lực

Mười ba thao tác dùng chung một động cơ kiến tạo diễn ngôn. Chi tiết định tuyến
và điều kiện áp dụng: [`references/capability-matrix.md`](references/capability-matrix.md).

| Năng lực | Sản phẩm chính |
| --- | --- |
| `conceptualize` | Hồ sơ tu từ và cấu trúc tuyên bố sơ bộ |
| `outline` | Dàn ý có chức năng và quan hệ phụ thuộc |
| `argue` | Bản đồ tuyên bố - bằng chứng - bảo chứng |
| `synthesize` | Tổng hợp theo chủ đề, điểm hội tụ và bất đồng |
| `draft` | Văn bản học thuật hoàn chỉnh ở ngôn ngữ đích |
| `develop` | Lập luận đầy đủ hơn, không thêm dữ kiện giả |
| `compress` | Bản ngắn hơn, giữ phạm vi và điều kiện thiết yếu |
| `expand` | Bản mở rộng và danh sách phần còn thiếu nguồn |
| `paraphrase` | Diễn đạt lại với ngữ nghĩa ổn định |
| `revise` | Bản sửa kèm kiểm toán thay đổi |
| `audit` | Phát hiện theo mức độ và quyết định cổng |
| `humanize` | Văn bản đã làm sạch, nhật ký pattern và cổng kiểm định |
| `translate` | Bản dịch, bảng thuật ngữ và kiểm toán |

## Cổng chất lượng

Sản phẩm được đánh giá trên sáu chiều theo thang 0-5: `SEM` toàn vẹn tuyên bố và
bằng chứng, `TERM` thuật ngữ, `STANCE` lập trường khoa học, `LOGIC` lập luận,
`LANG` độ tự nhiên của ngôn ngữ đích, `CONS` tính nhất quán.

Quyết định `pass` yêu cầu mọi chiều đạt ít nhất 4/5 và không có lỗi chặn. Điểm
trung bình cao không bù được lỗi đảo nghĩa, mất phủ định, nâng tương quan thành
nhân quả, sai số liệu, hỏng trích dẫn, đổi phạm vi hoặc bịa bằng chứng. Hai
quyết định còn lại là `revise` và `human_review`. Thang điểm và điều kiện chặn:
[`references/quality-rubric.md`](references/quality-rubric.md).

## Kiến trúc kho mã

```text
academic-prose/
├── SKILL.md              # Hợp đồng và bộ định tuyến chính
├── agents/openai.yaml    # Bộ điều hợp giao diện tùy chọn
├── references/           # 15 tài liệu chuẩn ngôn ngữ, quy trình và phân loại lỗi
├── schemas/              # Lược đồ JSON cho hiện vật trung gian
├── evals/                # Tình huống tổng hợp cho viết, dịch, humanize và usage
├── scripts/              # Trình kiểm định và hai trình mô phỏng
└── tests/                # Kiểm thử kho mã và lược đồ
```

## Phát triển

```bash
python3 scripts/validate_skill.py                  # cổng kiểm định đầy đủ
python3 -m unittest discover -s tests -v           # kiểm thử kho mã
python3 scripts/run_usage_simulations.py           # riêng mô phỏng usage
python3 scripts/run_capability_examples.py         # riêng ví dụ năng lực
```

Trình kiểm định gọi lại cả hai trình mô phỏng, nên một ví dụ hỏng sẽ làm cổng đỏ.
Mỗi phép kiểm tra được đột biến có chủ đích để chứng minh nó biết thất bại; một
phép kiểm tra không bao giờ đỏ thì không phải là bằng chứng.

Đây là kiểm định hợp đồng bằng dữ liệu tổng hợp. Kết quả xác nhận độ bao phủ của
các bất biến đã khai báo; chất lượng đầu ra thực tế còn phụ thuộc vào mô hình, dữ
liệu đầu vào, công cụ điều phối và việc thẩm định của con người.

Khi đóng góp một quy tắc mới, hãy nêu rõ ngành, thể loại, ngữ cảnh, lý do, ví dụ
đúng, phản ví dụ và phạm vi áp dụng.

## Nguồn tham khảo

| Nguồn | Nội dung được tham khảo |
| --- | --- |
| [Agent Skills](https://github.com/agentskills/agentskills) | Chuẩn đóng gói và tích hợp dựa trên `SKILL.md`, gồm quy ước để môi trường tương thích khám phá và sử dụng skill |
| [Vercel Skills](https://github.com/vercel-labs/skills) | Trình quản lý Skills và cú pháp cài đặt `npx skills add` được dùng trong hướng dẫn cài đặt |
| [VI-Translate](https://github.com/breslee1707/VI-Translate) | Quy trình bàn giao dịch PDF, bảo toàn thành phần và tái dựng tài liệu trong lớp phối hợp PDF |
| [Humanizer](https://github.com/blader/humanizer) | 35 pattern nhận diện văn phong do máy tạo, được chuyển thành lớp humanize có guardrail học thuật và hỗ trợ tiếng Việt |

## Giấy phép

[MIT](LICENSE)
