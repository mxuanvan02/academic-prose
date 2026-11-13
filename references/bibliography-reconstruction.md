# Bibliography reconstruction from in-text citations

Use when a manuscript cites `[1]–[22]` (or any range) but ships no `Tài liệu tham khảo / References` section, or when numbering is discontinuous.

## 1. Extract true citation set from OOXML, not the dump

- Parse `word/document.xml` for bracket tokens `\[...\]`; expand ranges (`[1–5]`, `[10–12]`) and splits (`[6,7]`).
- Exclude false positives like `[Q(0,025), Q(0,975)]` (formula quantiles, not citations).
- Measured case (a 43-entry revision round): raw max was 22 but distinct set was `[1-12,18-22]` — `[13-17]` never cited. Missing numbers are a finding, not a renumbering license until confirmed.

## 2. Verify each candidate before writing prose

- Search-first, then take DOI from result, then re-resolve via Crossref and compare title/author/year/venue.
- Keep a private ledger: `verified` (Crossref match) vs `inferred` (no match / arXiv-only / report).
- Never invent a reference to fill a gap. If `[13-17]` have zero in-text hits across XML + rendered PDF, they are absent — not "to be guessed".

## 2b. Audit an ALREADY-WRITTEN bibliography — the fabrication classes

Writing references from recall produces a specific, repeatable set of defects. A
full-text audit of a 43-entry bibliography found seven, of which three were
outright fabrications that no format check would catch. Audit every entry against
Crossref/arXiv before delivery; do not trust your own earlier drafting.

| Defect class | Measured example | Fix |
| --- | --- | --- |
| Wrong journal + volume + pages invented for a real paper | Woollett & Maguire 2012 cited as `Hippocampus, 22(7), 1492–1497`; the real venue is `NeuroReport, 23(15), 885–888` (DOI 10.1097/WNR.0b013e328359317e) | Re-resolve by title; take venue/volume/pages from the Crossref record |
| Invented title from the paper's abstract wording | arXiv:2510.26518 cited as "Improving human oversight of AI fact-verification"; real title is "Human-AI Complementarity: A Goal for Amplified Oversight" | Fetch the arXiv `abs` page (the Atom API 406s intermittently) and copy the title |
| Wrong author, transplanted from another entry | arXiv:2507.15855 attributed to "Nguyễn H., et al."; real authors are Huang Y. and Yang L. F. | Same as above; then grep the BODY for the wrong surname, because prose usually repeats it ("kết quả của Nguyễn và cộng sự") |
| Reversed author order | `Bijker W. E., Pinch T. J.` where Crossref lists Pinch first | Crossref `author` array is the order of record; fix the reference AND every in-text attribution |
| Anonymized entry that has real authors | "Human-artificial intelligence interaction in gastrointestinal endoscopy" with no authors; Crossref gives Campion J., O'Connor D., Lahiff C. | Never ship an authorless journal article when the record names authors |
| Preprint cited after it was published | Grace et al. cited as arXiv:2401.02843 only; it is in JAIR 84 (2025), DOI 10.1613/jair.1.19087 | Prefer the published version; keep arXiv only for genuine preprints |
| No verifiable identifier at all | entry with neither DOI, URL, nor arXiv ID | Every entry must carry one; an entry without any is unauditable |

Audit script shape that found all seven:

1. Split the manuscript at the bibliography heading; parse entries with `^(\d+)\.\s+(.+)`.
2. For each DOI in the entry, `GET api.crossref.org/works/<doi>` and print the
   returned title, container-title, volume, issue, page, year, and author list.
   Read them back against the entry text — a 200 status alone proves nothing,
   and a near-miss DOI can resolve to a completely different paper.
3. URL-encode DOIs containing parentheses: `10.1016/0005-1098(83)90046-8` returns
   404 raw and 200 quoted. A 404 here is a quoting bug, not a bad DOI.
4. For arXiv IDs, use the `abs` HTML page with a browser User-Agent; the Atom API
   returns 406 for some IDs.
5. Check URLs with a real browser UA. `403` from imf.org and eprints.soton.ac.uk is
   bot-blocking, not a dead link — keep the link, add the DOI. A `202` from
   legislation.gov.uk is an async-render stub, also fine for humans.
6. Assert citation integrity in both directions: every `[n]` in the body exists in
   the list and every listed entry is cited. Then assert first-appearance order is
   ascending, which numeric-style venues require.

When an entry is corrected, grep the body prose for the old author surname and the
old venue name. The reference list is not the only place a fabricated detail lives.

## 3. Repair discontinuous numbering by remap, not placeholders

- Do NOT ship `[13] [Không trích dẫn — giữ chỗ]` placeholders to "preserve numbering".
- Delete unused entries, renumber bibliography continuously (`18→13, 19→14, 20→15, 21→16, 22→17` in measured case).
- Remap every in-text occurrence including ranges: `[18]`→`[13]`, `[19]`→`[14]`, `[20,21]`→`[15,16]`, `[22]`→`[17]`.
- Assert after remap: `missing in-text not in bib == []`, `bib not cited == []`, old numbers still present `== 0`.

## 4. Keep verification language out of the artifact

- Trailing `— Verified` / `— Verified via Crossref` / `— Inferred placeholder` in reference paragraphs triggers `verification_log_prose` in `scripts/internal_register_scan.py --genre manuscript` (measured: 17 hits, gate fail despite otherwise clean scans).
- Ship clean entries: authors, title, venue, year, DOI only. Keep verified/inferred status in a separate audit note or chat summary, never in DOCX prose.
- Re-run all four gates after cleaning: `internal_register_scan`, `process_logic_scan`, `vi_ai_pattern_scan`, `academic_discourse_scan` must all be `scan_clean` / 0 candidates.

## 5. Delivery checklist for DOCX

- Insert `6 Tài liệu tham khảo` as a numbered heading paragraph after Kết luận, then one paragraph per `[n]` entry.
- Produce clean + tracked copies from the same source; tracked copy must enable `w:trackRevisions`.
- Office smoke: LibreOffice convert to PDF in a clean dir, confirm page count delta is only the added bibliography (measured: 9→10 pages), and cross-copy accepted text matches.

## Hai lớp lỗi còn sót sau khi biểu ghi đã "có DOI thật"

Một DOI tồn tại và một title khớp Crossref vẫn chưa đủ. Hai lớp lỗi sau chỉ lộ ra khi đối chiếu **nội dung nguồn**, không phải siêu dữ liệu.

### Lớp 8 — Số liệu đúng nhưng trích sai nguồn

Số liệu lấy từ báo cáo/blog của tổ chức nhưng lại gắn citation vào bài báo học thuật cùng hệ thống, vì cả hai nói về một đối tượng. Cách phát hiện: tải chính nguồn được cite (PDF arXiv /全文) và grep từng con số trong câu. Nếu con số không xuất hiện trong nguồn đó, citation sai dù nguồn vẫn là tài liệu hợp lệ.

Kiểm tra bắt buộc cho mọi câu chứa số đo cụ thể:

```python
# mỗi con số trong câu phải xuất hiện trong NGUỒN được cite, không phải nguồn cùng chủ đề
for claim_number in numbers_in_sentence:
    assert claim_number in source_text_of_cited_ref
```

Blog tổ chức và bài báo học thuật là hai nguồn khác nhau và phải cite riêng. Khi một câu dùng số liệu của blog, cite blog; khi câu khác dùng thiết kế nghiên cứu của bài báo, cite bài báo. Đừng gộp về một số cho tiện.

### Lớp 9 — Đánh số lại citation mỗi khi đổi số citation

Với hệ trích dẫn dạng số, danh sách tài liệu phải đánh theo **lần xuất hiện đầu tiên** trong bài. Bất kỳ thao tác nào đổi số citation (sửa nguồn sai, thêm citation cho tổ chức được nhắc mà chưa cite) đều phá thứ tự này và phải đánh số lại toàn bộ.

Quy trình đánh số lại an toàn:

```python
order = []                                    # lần trích đầu, theo vị trí trong file
for m in re.finditer(r"\[(\d+)\]", body):
    n = int(m.group(1))
    if n not in order: order.append(n)
assert sorted(order) == list(range(1, N+1))   # không thiếu/không thừa
mapping = {old: i+1 for i, old in enumerate(order)}
body = re.sub(r"\[(\d+)\]", lambda m: f"[{mapping[int(m.group(1))]}]", body)  # MỘT lượt, tránh va chạm
```

Rồi verify lại sau khi ghi: `first_order == list(range(1, N+1))` và danh sách tài liệu cũng `1..N`.

Bẫy: kiểm tra ánh xạ tên tác giả ↔ số phải đọc họ tác giả **thẳng từ entry**, không gõ tay bảng ánh xạ. Bảng gõ tay thiếu một mục sẽ làm mọi số sau nó lệch một nấc và báo lỗi giả hàng loạt.

### Verify chéo tên tác giả với số citation

Sau khi đánh số lại, chạy kiểm tra hai chiều trên văn bản xuôi (loại hàng bảng Markdown, vì một hàng bảng trích nhiều nguồn):

1. Mỗi tên tác giả được nêu trong câu phải có ít nhất một citation trong câu đó trỏ tới entry chứa tên này.
2. Mỗi số citation trong câu có nêu tên tác giả phải trỏ tới entry chứa tên đó.

Một câu nêu nhiều tác giả với nhiều citation khác nhau là hợp lệ, nên điều kiện là giao khác rỗng, không phải bằng nhau.
