# Process-Logic Gate

Prose that reports a research process fails differently from prose that reports a
finding. The numbers can be right, the citations can resolve, the sentence can
read fluently, and the reader still cannot tell **what already existed**, **what
happened afterwards**, and **what role the later procedure served**. That is a
logic defect, not a style preference, and it is repaired by restoring the missing
proposition rather than by rewording.

This gate is language-neutral. It applies to Vietnamese and English alike, and to
any genre that describes a procedure: methods sections, review protocols,
pipeline descriptions, audit trails, provenance statements, and the abstract that
compresses them.

## 1. The three propositions

Every process sentence carries up to three propositions. Name each one before
revising.

| Proposition | Question it answers | Failure when omitted |
| --- | --- | --- |
| **Prior state** | what already existed, and prior to *which named event* | the reader cannot place the corpus, dataset, or artifact in time |
| **Later action** | what procedure was run afterwards | the ordering collapses and the two steps read as simultaneous |
| **Role** | what the later procedure was *for* | the later procedure is silently read as the origin of the prior state |

The third omission is the most damaging, because the reader supplies a default:
a search reported next to a corpus is assumed to have produced that corpus. A
coverage check then reads as a sampling frame, and a provenance claim the author
never made becomes the claim the reader takes away.

## 2. Four candidate classes

The scanner reports candidates in these classes. A lexical hit is a candidate,
never a verdict.

| Class | Code | Trigger |
| --- | --- | --- |
| unanchored prior state | `chronology_anchor_omitted` | a state is asserted to precede something the sentence does not name |
| compressed chain | `compressed_process_chain` | prior state, later procedure, and purpose are fused into one noun chain |
| opaque role | `opaque_procedure_role` | a later procedure is ordered but neither this sentence nor the next states its role |
| reminder for a boundary | `reminder_instead_of_boundary` | reminder framing stands in for a stated evidence limit |

`reminder_instead_of_boundary` overlaps the internal-register gate by design: an
author who has not decided what the boundary *is* reaches for a reminder, so the
two defects co-occur. Repair the logic first, then re-run the register gate.

## 3. Verdicts

| Verdict | Use when | Operation |
| --- | --- | --- |
| `recast_with_named_anchor` | the prior state is real but its comparison event is unnamed | name the event: `được xây dựng trước khi chạy truy vấn X` |
| `split_into_three_propositions` | one sentence carries all three propositions | break into clauses, one proposition each, in chronological order |
| `state_role` | the later procedure's function is missing | state it, including a negative role: `chỉ dùng để kiểm tra độ bao phủ`, `không tạo thêm nguồn mới` |
| `state_boundary` | a reminder stands in for a limit | state the limit and what it prevents concluding |

Two operations are forbidden.

**Do not compress back.** Merging the repaired clauses to save a line reproduces
the defect. Length is not the metric; recoverable order is.

**Do not promote the later procedure.** Recasting `tập lõi được hình thành trước`
into a sentence whose subject is the search reverses the provenance. The prior
state stays the subject of its own proposition.

## 4. Worked repairs

| Defective | Repaired |
| --- | --- |
| kết hợp tập tham chiếu hình thành trước với các truy vấn OpenAlex bổ sung | Tập tham chiếu được xác lập trước khi chạy truy vấn OpenAlex. Các truy vấn được thực hiện sau đó và chỉ giữ vai trò kiểm tra độ bao phủ của tập này. |
| tập lõi được xây dựng trước, tiếp theo là tìm kiếm bổ sung và sàng lọc thủ công | Tập lõi được xây dựng trước khi chạy tìm kiếm bổ sung; các lượt tìm kiếm sau đó chỉ dùng để kiểm tra độ bao phủ, và kết quả được sàng lọc thủ công. |
| Có 64 nguồn tham chiếu đã được hình thành trước; | Có 64 nguồn tham chiếu đã được xác lập trước khi thẩm định ứng viên mới; |
| The corpus was assembled beforehand; searches were run later. | The corpus was assembled prior to the database searches, which were run afterwards only to assess coverage. |
| Hạn chế cần lưu ý: ngưỡng bằng chứng gây thiên lệch khả dụng. | Ngưỡng bằng chứng nghiêng về công trình có toàn văn truy cập được, một dạng thiên lệch khả dụng, nên kết luận không suy rộng cho các công trình không truy xuất được. |

## 5. Licensed constructions and false positives

A detector that fires on these destroys correct writing. Each was measured on a
real manuscript, not invented for the fixtures.

- **Anchored chronology.** `trước khi`, `trước bước`, `prior to`,
  `before running` name the event. Not a candidate.
- **Role stated in the next sentence.** The role may legitimately land in the
  following sentence; the scanner reads a two-sentence window before reporting.
- **Negative role.** `không tạo thêm nguồn mới`, `did not add any source` is a
  stated role. Denying an effect is stating the function.
- **`bổ sung` as an adjective.** `dữ liệu tìm kiếm bổ sung`, `tìm kiếm bổ sung`
  are noun phrases, not ordering markers. Only `sau đó`, `tiếp theo`,
  `trước khi`, `later`, `subsequently` order a procedure.
- **Ordinary physical time.** `Nhiệt độ giảm trước khi bơm được bật` describes
  the object of study, not the research process. Not in scope.
- **Enumerated procedure steps.** `Tiếp theo, 10 chuỗi truy vấn được chạy và thu
  về 246 bản ghi` states the action and its result inside a numbered pipeline
  whose purpose was declared once at the top. Not a candidate.

## 6. Running the gate

```bash
python3 scripts/process_logic_scan.py Chapter/noidung_chap2.tex
python3 scripts/process_logic_scan.py main.tex --json findings.json --quiet
python3 scripts/process_logic_scan.py draft.md --report process_report.md
```

Exit codes: `0` no candidate, `2` candidates present, `3` input error. A non-zero
exit is a request for the three-proposition review, not a rejection of the text.

The verification suite is `scripts/test_process_logic_scan.py`. It asserts the
same class on a Vietnamese and an English fixture, and it asserts silence on each
licensed construction in §5. Run it after any pattern change; the false-positive
tests are the ones that decay first.

**Absence of hits is a partial verification.** An unanchored prior state can be
paraphrased with no lexical signature. The manual pass over Methods, the data
provenance statement, and the abstract remains required.

## 7. Interaction with the other gates

Order matters. Run this gate **before** the internal-register gate and before any
surface polish:

```text
process logic (order and role recoverable)
-> internal register (subject admissible)
-> stance and hedging
-> target-language naturalness
-> surface polish
```

Rewriting for register first tends to delete the very clause that carried the
role, which converts a register defect into a provenance error. Repairing the
logic first leaves the register gate a smaller and safer job.
