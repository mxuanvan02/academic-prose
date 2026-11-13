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

## 2b. Explanatory colon chains

Vietnamese academic prose states explanations in clauses, not in label-colon-explanation frames. The colon that introduces an explanation is an English and French punctuation habit; models reproduce it at high density. A Vietnamese manuscript whose body paragraphs carry several explanatory colons reads as translated rather than written.

**Signals.** A noun phrase or a clause ending in `:` followed by the explanation; heading titles of the form `Khung phân tích: ...`; abstract sentences of the form `... với ba điều kiện: A, B và C`; `cơ chế thứ nhất là X: ...` / `cơ chế thứ hai là Y: ...` enumerations inside one paragraph.

| Colon frame | Repair |
| --- | --- |
| `... với ba điều kiện: A, B và C` | `... kèm theo ba điều kiện gồm A, B và C` |
| `Cơ chế thứ nhất là hiệu ứng quy mô: máy rút tiền làm giảm ...` | `Cơ chế thứ nhất là hiệu ứng quy mô, khi máy rút tiền làm giảm ...` |
| `kết quả đảo ngược hoàn toàn: nhóm dùng AI ...` | `kết quả đảo ngược hoàn toàn khi nhóm dùng AI ...` |
| `có ý nghĩa quan trọng: một nghề là ...` | `có ý nghĩa quan trọng vì một nghề là ...` |
| `loại trừ giả thuyết ngược: việc dùng ...` | `loại trừ giả thuyết ngược, cụ thể là việc dùng ...` |
| `theo một quy luật có thể nhận diện: khi ...` | `theo một quy luật có thể nhận diện, theo đó khi ...` |
| Heading `Khung phân tích: vòng đời bốn pha` | `Khung phân tích vòng đời bốn pha` |

The connective must match the real logical relation. Use `vì` or `do` for cause, `khi` for condition or time, `theo đó` for restatement, `cụ thể là` for specification, `gồm` for enumeration. Do not substitute one connective for another to silence the rule, and do not delete the explanation to remove the colon; the relation is content.

When the colon separates a long explanation into its own sentence, prefer a full stop plus a new sentence over any connective: `Đối với trí tuệ nhân tạo, các thiết chế tương đương chưa tồn tại ở dạng được xã hội công nhận rộng rãi. Hiện chưa có chuẩn năng lực người dùng ...`.

**False positives.** Do not flag the following, each of which is correct Vietnamese:

- Venue-mandated labels `Tóm tắt.`, `Từ khóa:`, `Abstract.`, `Keywords:`, `Bảng 1.`, `Hình 2.`.
- Bibliographic punctuation inside reference entries (`Explorations in Economic History, 46(4), 418–435`), publisher places (`Hà Nội: Nhà xuất bản ...`), and DOI or URL strings.
- Ratios, times, and scriptural or legal citation forms (`10:1`, `08:30`, `Luật số 12/2020: điều 3`).
- English-language titles and abstracts in a bilingual manuscript, where the colon after a title is standard academic English.

**Threshold.** Body prose should carry at most one explanatory colon per 1.000 words. Headings and captions should carry none. A single colon in a long manuscript is a stylistic choice; a colon every two or three paragraphs is a machine signature.

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

**When the subject is literature, this table is incomplete.** English literary criticism has its own idiom, and translating it yields calques absent from the list above (`nằm ở chỗ` rendering *lies in the fact that*, `đóng gói` for *packages*, `cái đứng` for *that standing*, `ở tầng sâu nhất` for *at the deepest level*). Those, plus the long-`và`-chain repair, the tertium comparationis requirement, and the literary hedge inventory, are in [Vietnamese prose about literature and comparison](vietnamese-literary-prose.md). Load it whenever the deliverable is Vietnamese prose about literature rather than data.

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

## 9. Title colon split

The colon-split title (`Chủ đề lớn: Phụ đề thu hẹp`) is a high-signal machine tell in Vietnamese academic deliverables and is rejected outright by the author. It fails three ways at once: it substitutes punctuation for syntax, it repeats the head noun across both halves, and the subtitle is usually narrower than what the document actually argues.

Repair by recasting into a single nominal phrase. A course-essay title built as `PHẦN MỀM NGUỒN MỞ TRONG KỶ NGUYÊN CHUỖI CUNG ỨNG PHẦN MỀM: GIẤY PHÉP, MÔ HÌNH PHÁT TRIỂN VÀ AN TOÀN CHUỖI CUNG ỨNG` becomes `GIẤY PHÉP, MÔ HÌNH PHÁT TRIỂN VÀ AN TOÀN CHUỖI CUNG ỨNG CỦA PHẦN MỀM MÃ NGUỒN MỞ` — same scope, one phrase, no repeated token, no colon.

The rule extends to section headings. Table and figure captions are the licensed exception: `Bảng 1: Tên bảng` is the established Vietnamese house convention and appears in the author's own approved theses; `vi_ai_pattern_scan` flags caption colons as candidates — adjudicate them as licensed, do not rewrite. Apply it before delivery rather than after the author points it out, and re-run `vi_ai_pattern_scan` with URLs and DOIs stripped so citation strings do not hide the real colon density in prose.

The same scrutiny applies to a title with no colon at all. A title stacked as two
nominalizations (`Biến hình không hoàn tất và sự im lặng của cơ thể nữ`) reads
crowded, repeats the `X của Y` skeleton, and leaves it unclear whether the two
halves are the axes the argument actually makes. Prefer concrete noun phrases
naming the analytical object (`tiếng nói bị tước` over `sự im lặng của cơ thể
nữ`), then re-read the body and confirm both halves are truly argued. A title
promising an axis the paper only touches is framing drift, the same defect the
colon-split title commits.

## 11. Vietnamese self-reference and first-person register

A Vietnamese manuscript that refers to itself as "bài" and speaks in the bare first person "ta" reads as a machine rendering of an English draft. Both are **structural** tells: the detector matches the SLOT, not a vocabulary list, because the repair is a register change, not a word swap.

### 11.1 Self-reference

The manuscript naming itself as "bài" is not wrong in isolation, but it is a conversational register that Vietnamese academic prose does not use for its own argument. The natural self-references are "nghiên cứu này", "nghiên cứu", "công trình này", and the first person "chúng tôi".

| Machine register | Vietnamese academic register |
| --- | --- |
| "chỉ báo của bài" | "chỉ báo mà chúng tôi dùng" / "chỉ báo của nghiên cứu" |
| "quy ước đếm của bài" | "quy ước đếm trong nghiên cứu này" |
| "mô phỏng của bài" | "mô phỏng của nghiên cứu" / "mô phỏng trong nghiên cứu này" |
| "bài không đo được độ lớn đó" | "nghiên cứu không đo được độ lớn đó" |
| "phát hiện quan trọng nhất của bài" | "phát hiện quan trọng nhất của nghiên cứu" |
| "bài báo đặt ra câu hỏi" | "nghiên cứu đặt ra câu hỏi" |

**Licensed, because they name an object rather than the manuscript:** "bài báo" (a paper), "bài toán" (a problem), "bài học" (a lesson), "bài tập" (an exercise), "bài nghiên cứu" (a study). A detector that excludes only "bài báo" flags "Mục tiêu của bài toán là giảm thiểu sai số bám" — a measured false positive that became a regression test.

### 11.2 Bare first person "ta"

"Ta" in a VERB slot is a spoken register; Vietnamese academic prose uses "chúng tôi" (including for a single author, where the venue permits it).

| Machine register | Vietnamese academic register |
| --- | --- |
| "ta cần phải chuyển đổi..." | "chúng tôi cần chuyển đổi..." / "nghiên cứu cần chuyển đổi..." |
| "ta đề xuất phương pháp..." | "chúng tôi đề xuất phương pháp..." |
| "ta thấy rằng..." | "chúng tôi thấy rằng..." / "kết quả cho thấy..." |

**Licensed, because "ta" is a noun there:** "héc-ta", "đơn vị ta", "nhà nghiên cứu ta". The detector therefore requires a following verb from a closed set, not the token alone.

### 11.3 Audit

Count in the Vietnamese text layer only:

- `của bài` and `bài +` a finite verb, excluding the licensed compound nouns — each occurrence is a candidate.
- bare `ta` followed by a verb — each occurrence is a candidate.

One occurrence is a stylistic choice; the register becomes a defect when it recurs through the document. The scanner reports both as separate classes (`self_reference`, `bare_first_person`) with limit 0, because a Vietnamese manuscript for a journal or thesis does not use either register at all.

## 10. A clean `translation_calque` count does not certify a translation

`vi_ai_pattern_scan.py` hunts fixed calque phrases (`mở đường cho`, `cung cấp một cái nhìn`, `nó được phát hiện ra rằng`). A word-by-word translation that is wrong at the SENTENCE-STRUCTURE level scores `translation_calque = 0` while still reading as machine output. Measured on a translated manuscript the author rejected as “văn phong còn dịch word by word, câu chữ lủng củng”: the scanner reported 0 calques, 0 symmetric padding, 0 hedge stacks, and `machine_marked_passage = 0`, while the structural layer measured 29 em dashes, 126 unreasoned `được` (19,2 per 1.000 words), 28 `sự + V`, 10 `việc + V`, and 47 explanatory colons (7,2 per 1.000 words against the §2b ceiling of 1,0).

Before delivering any `translate`, `humanize`, or `audit` output in Vietnamese, measure the structural layer separately from the phrase registries:

| Signal | Ceiling | Repair |
| --- | --- | --- |
| em dash `—` in body prose | 0 | the four construction types in [Academic Vietnamese standard](academic-vietnamese-standard.md) |
| explanatory colons per 1.000 prose words | 1,0 | §2b connective table (`vì`, `khi`, `theo đó`, `cụ thể là`, `gồm`) |
| colons in headings and captions | 0 | fold into one noun phrase; `Bảng 1:` / `Hình 2:` stay |
| `được` / `bị` | no ceiling; compare against the source | rewrite active or drop the subject, never delete mechanically |
| `sự + V`, `việc + V` | no ceiling; compare against the source | replace the nominalisation with its verb |

Count on the prose subset only: strip code fences, markdown table rows, headings, blockquotes, and `$...$` / `\[...\]` math before counting colons, or math notation (`\hat\varepsilon{=}0.2369:\ q{=}...`) and table rows report false hits.

Every hit remains a candidate, not a verdict, and the repair is to rewrite the whole sentence — a global `được` deletion destroys meaning and a global colon replacement leaves clauses dangling. Adjudicate, then re-read the paragraph.

**Gate the gate.** Such a structural scan must be run against one known-good and one known-bad fixture and prove it exits 0 on the good one and non-zero on the bad one. A scanner that only ever reports FAIL cannot distinguish a bad translation from a strict threshold.

### Let the parser adjudicate markdown damage, never a regex

Undigested markdown (a literal `**` printed on the page) is visible to the reader and invisible to the XeLaTeX log, so it must be gated. Two regexes written for it produced measured false positives:

1. Counting `\*\*\s|\s\*\*` indicted 41 lines, of which **26 were valid bold** such as `**Nguyễn Tương Tri** (tác giả liên hệ),` — the space sits AFTER the closing pair, where CommonMark allows it.
2. Even after stripping `**…**` pairs, the regex still indicted `**H2 Không có mỏ neo.** … OPT\_\* …` purely because the line contains a deliberately escaped asterisk. Pandoc bolds that run correctly and renders `OPT_*` correctly.

The arbiter is the parser. `pandoc SRC -t native` turns a broken `**` pair into a bare text token `Str "**"`, while valid bold becomes `Strong [...]`:

```bash
pandoc "$SRC" -t native 2>/dev/null | grep -cE 'Str "\*\*?"'   # must be 0
```

Calibrate on three variants before trusting the count: broken bold = 1, valid bold containing an escaped `\*` = 0, plain valid bold = 0. The usual cause is a space on the INNER edge (`** text **`), which fails flanking and leaves the pair as text.
