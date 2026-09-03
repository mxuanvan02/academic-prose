# Vietnamese AI Pattern Registry

The 35 upstream patterns were derived from English text. Their watched-word lists do not transfer. This registry supplies the Vietnamese evidence: the words and constructions that mark machine-generated or machine-translated Vietnamese academic prose, and the constructions that merely look suspicious to an English-trained rule.

Two generators produce Vietnamese AI slop, and they leave different traces:

1. **Native generation.** A model writing directly in Vietnamese overproduces ceremonial vocabulary, symmetric four-part parallelism, and evaluative padding.
2. **Translation from English.** A model rendering English source text leaves calques, dummy subjects, nominalization stacks, and English punctuation conventions.

The second class overlaps [Cross-language transfer taxonomy](cross-language-transfer-taxonomy.md). Use that registry for the transfer error; use this one for the AI-tell judgment.

## 1. Ceremonial and inflated vocabulary

Vietnamese equivalent of §1 and §4. These are the strongest single-word signals in Vietnamese academic drafts.

**Watched words:** đóng vai trò then chốt, giữ vai trò quan trọng, có ý nghĩa vô cùng quan trọng, mang tính đột phá, vượt trội, tối ưu (as an unquantified compliment), toàn diện, sâu sắc, mạnh mẽ, đáng kể (without a number), phong phú, đa dạng, sinh động, nổi bật, tiên tiến, hiện đại, hàng đầu, uy tín, chuyên sâu, thiết thực, hiệu quả cao, chất lượng cao, không ngừng, ngày càng, mở ra hướng đi mới, tạo tiền đề, góp phần không nhỏ, khẳng định vị thế, dấu mốc quan trọng, bước tiến quan trọng

**Repair.** Replace the evaluation with the measurement, or delete it.

- Before: `Phương pháp đề xuất mang tính đột phá và cho kết quả vượt trội đáng kể so với các phương pháp hiện có.`
- After: `Phương pháp đề xuất đạt F1 0,847, cao hơn 2,3 điểm so với mô hình cơ sở BiLSTM-CRF.`
- When no number exists: `Phương pháp đề xuất cho kết quả cao hơn mô hình cơ sở BiLSTM-CRF.` and mark the magnitude `needs_source`.

`đáng kể` deserves separate attention. In statistics it renders *significant* and is licensed only when a test supports it. Used as a vague intensifier it is padding; used for an unsupported statistical claim it is a stance upgrade. Distinguish `khác biệt có ý nghĩa thống kê (p < 0,05)` from `cải thiện đáng kể`.

## 2. Empty framing constructions

Vietnamese equivalent of §23. These are frames that occupy a clause and assert nothing.

| Padding | Repair |
| --- | --- |
| `có thể thấy rằng`, `có thể nhận thấy rằng` | delete; state the observation |
| `điều này cho thấy rằng` | keep only when an inference is actually drawn |
| `như đã đề cập ở trên`, `như chúng ta đã biết` | delete |
| `nhìn chung`, `về cơ bản`, `nói chung là` | delete unless it marks a real generalization |
| `trong bối cảnh hiện nay`, `trong thời đại ngày nay` | delete or replace with the specific period |
| `việc tiến hành thực hiện` | `thực hiện` |
| `nhằm mục đích để` | `nhằm` or `để` |
| `có một nhu cầu cần thiết phải` | `cần` |
| `mang tính chất` + adjective | use the adjective directly |
| `đóng vai trò là` | `là` |
| `thực hiện việc phân tích` | `phân tích` |
| `quá trình xử lý dữ liệu được tiến hành` | `dữ liệu được xử lý` or name the actor |
| `một trong những ... nhất` | state the rank or delete |
| `không thể phủ nhận rằng` | delete |
| `đáng chú ý là`, `cần lưu ý rằng` | delete unless the emphasis carries a real caveat |

## 3. Symmetric parallelism and forced enumeration

Vietnamese equivalent of §10, with a Vietnamese-specific form. Vietnamese rhetorical tradition favors balanced pairs and four-part constructions, which models overproduce.

**Signals.** Four-syllable balanced compounds used decoratively (`toàn diện sâu sắc`, `phong phú đa dạng`, `nhanh chóng hiệu quả`, `chính xác kịp thời`); three-item lists whose members are synonyms; every sentence in a paragraph opening with the same connective.

- Before: `Hệ thống hoạt động nhanh chóng, hiệu quả và chính xác, đáp ứng đầy đủ và toàn diện các yêu cầu đa dạng và phong phú của người dùng.`
- After: `Hệ thống trả kết quả trong 200 ms với độ chính xác 94% trên tập kiểm tra.`

Preserve a triad when its members are three distinct reported findings. Collapsing measured outcomes loses claims.

## 4. Translation calques

Vietnamese equivalent of §7, sourced from English generation. These are grammatical but not idiomatic Vietnamese.

| Calque | Source | Idiomatic Vietnamese |
| --- | --- | --- |
| `đóng một vai trò quan trọng trong` | plays an important role in | `quan trọng đối với`, or name the function |
| `nó được phát hiện ra rằng` | it was found that | `kết quả cho thấy` |
| `có một số lượng lớn các` | there are a large number of | `nhiều` |
| `điều quan trọng cần lưu ý là` | it is important to note that | delete |
| `trong điều khoản của` | in terms of | `về`, `xét theo` |
| `dựa trên một cơ sở hàng ngày` | on a daily basis | `hằng ngày` |
| `đối chiếu chống lại` | compare against | `đối chiếu với` |
| `cam kết với chất lượng` | commitment to quality | `bảo đảm chất lượng` |
| `cung cấp một cái nhìn sâu sắc` | provide deep insight | `cho thấy`, `làm rõ` |
| `mở đường cho` | pave the way for | `tạo điều kiện cho`, or delete |
| `bức tranh toàn cảnh về` | landscape of | `tổng quan về` |
| `minh chứng cho` (as filler) | is a testament to | delete or state the evidence |
| `được thiết kế để` (when purpose is obvious) | designed to | `dùng để`, or delete |
| `theo cách mà` | in such a way that | restructure the clause |
| `một cách + adjective` (overused) | adverbial -ly | use the adjective or a verb |

Also watch: `sự` and `việc` stacked across a clause (`việc thực hiện sự đánh giá quá trình cải thiện chất lượng`), pervasive `được`/`bị` with no discourse reason, and long prenominal modifier chains copied from English noun stacks.

## 5. Ornamental synonym cycling

Vietnamese equivalent of §11, and a genuine hazard because Vietnamese offers a Sino-Vietnamese and a native word for most concepts. A model alternates them to avoid repetition; a reader infers two constructs.

- Before: `Mô hình học sâu đạt độ chính xác cao. Mạng nơ-ron sâu này cho kết quả tốt. Kiến trúc đề xuất vượt các baseline.`
- After: `Mô hình học sâu đề xuất đạt độ chính xác 94%, cao hơn cả ba mô hình cơ sở.`

Repetition of a locked term is correct. Never introduce a synonym to satisfy a repetition rule; that is `terminology_drift`, a major failure.

## 6. Vietnamese hedging inventory

Vietnamese counterpart of §24. Reducing these to zero is a blocking stance upgrade. The permitted operation is collapsing a stack to one calibrated marker.

| Force | Markers |
| --- | --- |
| possibility | `có thể`, `có khả năng` |
| tentative inference | `dường như`, `nhìn chung có xu hướng` |
| suggestion from evidence | `gợi ý rằng`, `cho thấy khả năng` |
| partial scope | `phần nào`, `trong phạm vi dữ liệu hiện có`, `ở nhóm được khảo sát` |
| attribution | `theo`, `được cho là`, `một số tác giả cho rằng` |
| bounded recommendation | `nên xem xét`, `có thể cân nhắc` |

Forbidden upgrades: `có thể cho thấy` to `chứng minh`; `có liên quan đến` to `gây ra` or `dẫn đến`; `gợi ý` to `khẳng định`; `nên` to `bắt buộc` or `cần phải`; deleting `trong phạm vi dữ liệu hiện có`.

Stack collapse example: `Kết quả có thể có khả năng phần nào gợi ý rằng phương pháp này dường như hiệu quả hơn` becomes `Kết quả gợi ý phương pháp này hiệu quả hơn`. One marker survives. Zero markers is a block.

## 7. Vietnamese-specific false positives

Do not flag any of the following. Each is correct Vietnamese academic prose that an English-trained rule misreads.

- **Topic-comment structure.** `Về phương pháp, nghiên cứu sử dụng thiết kế cắt ngang.` This is native Vietnamese information structure, not a dummy subject.
- **Omitted subject with a recoverable antecedent.** Vietnamese licenses subject ellipsis far more freely than English. Do not insert `chúng tôi` or `nó` to satisfy §13.
- **Sino-Vietnamese disciplinary terms.** `khả thi`, `tối ưu hóa`, `định lượng`, `hồi quy`, `suy rộng`, `nội suy`, `chuẩn hóa`, `phân tầng` are terminology. §7 targets ceremonial vocabulary, not formal register as such.
- **`Chúng tôi` in Methods.** Standard Vietnamese academic first person plural, including for a single author, where the venue permits it.
- **Formal address conventions.** Salutations in a thesis acknowledgement or a defense presentation predate any model.
- **`Trong nghiên cứu này` opening a section.** A conventional Vietnamese framing move, not §28 announcement, when it is followed immediately by content rather than by a promise of content.
- **Genre-mandated Vietnamese sections.** `Tính cấp thiết của đề tài`, `Ý nghĩa khoa học và thực tiễn`, `Kết luận và kiến nghị` are required by Vietnamese thesis and grant templates. Repair weak content; never delete the section as §6 formulaic structure.
- **Decimal comma and Vietnamese number formatting.** `0,847` and `1.250.000` are correct Vietnamese convention. Do not normalize to English punctuation, and do not read the comma as a typo.
- **En dash in Vietnamese ranges.** `từ 12–18 mg`, `giai đoạn 2018–2023`, `tr. 145–162`. The §14 dash rule must not touch these.
- **Vietnamese diacritics inside protected tokens.** Author names, institution names, and quoted titles keep their exact form.
- **Repetition of a locked term.** Correct by policy; see §5 above.

## 8. Diagnostic threshold

One ceremonial word proves nothing. Vietnamese academic prose written by a careful human still contains `quan trọng`, `có thể`, and balanced pairs. Treat a passage as machine-marked only when several independent signals co-occur: ceremonial vocabulary plus empty framing plus symmetric padding plus evaluation without measurement. Absence of citations is not evidence, and polish is not evidence.

When the author supplied a writing sample, the sample governs. Match its rhythm, its Sino-Vietnamese density, and its punctuation habits rather than these defaults.
