# Self-Narration and Config Dump

Two register leaks distinct from `operational_log_prose`. That failure imports the
register of a **build log**. These two import the register of the author's own
**drafting notes** and of the **source code**.

Measured case: the same Vietnamese dataset paper (HOEIT-LegalQA → HUJOS-TT).
Every number was correct, the manuscript hit its page cap, both language versions
passed the abstract word cap, and the visual gate returned zero findings. The user
still rejected the prose with: *"toàn là mấy câu tự thuật, tự nhắc nhở..."*

Correctness is not the axis these fail on. They fail because the sentence is about
**writing the paper** rather than about the world.

## 1. `self_reminder_prose`

The draft tells itself what to do instead of doing it. The tell is a modal of
obligation aimed at the text: `cần nêu rõ`, `cần nêu thẳng`, `cần được diễn giải
thận trọng`, `cần thận trọng vì`, `được nêu dưới đây`, `cần nêu cùng với`,
`nên được đọc là`. In English: *it should be noted that*, *care must be taken
when interpreting*, *the following must be stated*.

The instruction survived from the outline into the prose. A reader does not need
the instruction; they need its result.

| Self-reminder | Direct statement |
| --- | --- |
| Cơ chế phục hồi này tạo ra một ràng buộc **cần nêu rõ** về bản chất dữ liệu | Cơ chế phục hồi **đặt ra** một ràng buộc về bản chất dữ liệu |
| Một giới hạn về tái lập **cần nêu thẳng**: … | Khả năng tái lập **có một giới hạn ở bước sinh câu hỏi**: … |
| Các lựa chọn cố định của quy trình **được nêu dưới đây** để nghiên cứu khác lặp lại được | **Toàn bộ quy trình sử dụng các tham số cố định sau.** |
| Ba quyết định phương pháp luận **cần nêu cùng với** các tham số trên | **Các tham số trên xuất phát từ** ba quyết định phương pháp luận |
| Qwen2.5-7B và Gemma-2-9B **cần được diễn giải thận trọng** vì cùng họ với … | Qwen2.5-7B và Gemma-2-9B **cùng họ với** các mô hình xây dựng dữ liệu … Hai kết quả này **vì vậy mang giá trị chẩn đoán** |
| Đặt kết quả cạnh các bộ đối sánh ở mục 2 **cần thận trọng** vì khác ngôn ngữ … | So sánh với các bộ đối sánh ở mục 2 **chỉ có giá trị định tính, do** khác biệt về ngôn ngữ … |
| **Mọi phát biểu** về "mức độ nhận thức" **nên được đọc là** nhãn thao tác | **Các phát biểu** về "mức độ nhận thức" **vì vậy là** nhãn thao tác |

### Its defensive twin

A related tell clusters where the author fears overclaiming: a chain of
`chỉ …`, `không phải là …`, `không chứng minh …`, `không nên được …`, `không bảo
đảm …` in adjacent sentences. Each is individually licensed; stacked, they read as
self-defence and the finding disappears under the disclaimers.

Convert *deny the strong claim* into *state the bounded claim*:

- `Các kiểm tra này **chỉ** thiết lập X. **Chúng không chứng minh** Y.` →
  `Các kiểm tra này thiết lập X, **nhưng không thiết lập** Y, vì Y đòi hỏi …`
- `Kết quả cho thấy Z. **Chúng không chứng minh** nhân quả, **cũng không chứng
  minh** đã thẩm định.` → `Kết quả cho thấy Z. **Hiệu ứng này giới hạn trong
  thiết lập đã mô tả và không hàm ý** đã thẩm định.`

One boundary sentence carrying the scope beats three sentences denying claims
nobody made. This is the sentence-level analogue of the abstract rule in
*Abstract and Framing Contract*: one validity boundary, not a closing paragraph.

**Do not delete the hedge.** The scope must survive; only the self-address goes.
Deleting `không chứng minh nhân quả` outright is a `causal_overclaim` in the
opposite direction.

## 2. `config_dump_prose`

Parameters copied from a config file or CLI invocation, carrying their identifier
form into prose. Reproducibility requires the *values*; it never required the
variable names.

| Config form | Prose form |
| --- | --- |
| `\texttt{marker-pdf}` | công cụ marker-pdf |
| `Qwen2.5-7B-Instruct-AWQ` | Qwen2.5-7B-Instruct **ở dạng lượng tử hóa** AWQ |
| `qua vLLM` | **triển khai bằng thư viện suy luận** vLLM |
| `backend sinh không cho cố định seed` | **công cụ suy luận không cho phép cố định giá trị khởi tạo ngẫu nhiên** |
| `không thay đổi tập \texttt{qa\_id}` | không thay đổi **tập định danh bản ghi** |
| `top-$p$ 0,9` | **ngưỡng lấy mẫu tích lũy** top-$p$ 0,9 |
| `hình phạt lặp 1,15` | **hệ số phạt lặp** 1,15 |
| `giới hạn 512 token` | **độ dài đầu ra tối đa 512 đơn vị từ (token)** |
| `lượng tử hóa 4 bit, nhiệt độ 0,3` | **ở chế độ lượng tử hóa 4 bit, nhiệt độ lấy mẫu 0,3** |

Rules:

1. **Keep every number.** Registers change; values do not. The rewritten paragraph
   in the measured case retained all eleven parameters.
2. **Name the role before the identifier.** `thư viện suy luận vLLM` tells a reader
   outside the toolchain what vLLM is; bare `vLLM` does not.
3. **A bare parameter list is not a Methods paragraph.** Group by pipeline stage
   and let each stage's sentence say what the stage does, then how it is
   configured.
4. **Keep the English technical term in parentheses** on first Vietnamese use when
   the term is the field's standard (`đơn vị từ (token)`). Do not calque it away.
5. **A config dump leaves untranslated source-language terms next to it.** Both
   defects have one cause — the draft was written in the language the work was done
   in — so repair them in the same pass. Which terms are translated, kept, or
   glossed is not decided case by case here:
   [Terminology localization policy](terminology-localization.md) owns the four
   tests, the per-discipline renderings, the load-bearing distinctions, and the
   designator inventory. The config-dump repair is that policy's `keep_source`
   half: a Vietnamese category noun in front of a preserved name
   (`thư viện suy luận vLLM`).

## 3. The generated-artifact trap

Two pipeline failures surfaced while fixing the above. Both waste a full rebuild
cycle if unknown.

**Hardcoded strings in the exporter.** A line was removed from the LaTeX source;
the DOCX still printed it. Cause: the LaTeX→DOCX converter emitted the string
literally, so the source was never its authority. When an element persists in the
rendered artifact after removal from the source, grep the exporter before editing
the source again.

**Regeneration silently reverts hand edits.** The user hand-edited the delivered
DOCX: moved the English block from the end of the paper to the front, switched the
English author names to Western order, dropped the ngày nhận/chấp nhận line and
the whole author-information sheet, and changed `mô hình ngôn ngữ mở` to `mô hình
ngôn ngữ lớn`. None of that existed in the source. The next regeneration would
have erased all of it.

Protocol when the user returns an edited artifact:

1. Convert both their version and your last generated version to a diffable text
   form (`pandoc --track-changes=all` for DOCX).
2. Diff and enumerate every change, including structural moves and reorderings —
   not just word substitutions.
3. Back-port each change into the source, then rebuild and confirm the count of
   changes survived.
4. Treat their edits as authoritative on structure and terminology, and re-verify
   only the constraints their edits could break (page count, word caps, float
   placement).

The structural moves are the ones a naive diff loses: a block relocated from 90%
to 5% of the document shows up as one large deletion plus one large insertion, and
is easy to read as unrelated churn.
