# HUL Template Decoy and Caption Orphan Fix

Measured case: a Vietnamese manuscript reframed for the HUL journal template.
Author correction: submitted DOCX used the wrong template; `Hình`/`Bảng`
captions stood alone.

## 1. Template decoy (HUL `hul_journal_assets/`)

Same folder held two `.docx` files; filename alone misled:

| File | Size | Role | Evidence |
| --- | --- | --- | --- |
| `template.docx` | 12K, 21 paras, 3 tables | author-declaration form only (`Phiếu khai báo`) | styles: bare `normal`; no manuscript body |
| `ban_thao_TQA_nganh_luat_theo_the_le.docx` | 30K, 135 paras (298 w/ tables), 7 tables | real manuscript frame | A4 `11906x16838`, margins `1417/1134/1134/1134`, styles `Heading1/2/3, FirstParagraph, BodyText, Compact, Bibliography`, `word/footnotes.xml` with 6 footnotes |

Rule: decide the frame by `pgSz` + `pgMar` + style set + `footnotes.xml`
presence, never by filename. Copy `sectPr` and the style set from the
proven frame into the draft.

## 2. Citation regime mismatch

Draft used bracket citations `[1]-[17]`; `citation.pdf` in the same folder
mandates **Chicago Notes-Bibliography 18th** (footnotes + end bibliography,
no `ibid`/`sđd`, DOI/URL required). Bracket list passing content gates is
still a venue-format block. Ask the author before bulk-converting: footnotes
vs. keep brackets as provisional.

## 3. Orphan captions

Measured on 8 captions (Hình 1-4, Bảng 1-4): `keepNext=True` alone did not
hold caption to its table/figure; the HUL frame itself had
`keepNext=False keepLines=False` on caption paras. Fix as one block:

- caption para: `keepNext=true + keepLines=true + widowControl=true`
- following table/image para: `keepLines=true`
- verify by body-order walk: caption index immediately precedes its
  table/image element (e.g. caption idx 46 -> table idx 47)

## 4. Drifting figures

4 PNGs present in `word/media/` but raw `w:drawing` count was 0: they rode
legacy `w:pict`/`v:shape` nodes. Re-embed as `wp:inline` with a real `a:blip`
embed id so each figure stays with its caption.

## 5. There is no manuscript template — do not go looking for one

Measured on tapchi.hul.edu.vn (5 rule pages + both Drive attachments): the
journal publishes exactly ONE downloadable form, the author declaration
(`PHIẾU KHAI BÁO THÔNG TIN TÁC GIẢ`, Google Doc, `1SlSHJh-…`). Manuscript
layout exists only as PROSE rules on `/quy-dinh-chung-ve-gui-bai-viet` and
`/huong-dan-quy-cach-viet-bai`; the other two Drive files are a submission
walkthrough and the Chicago-NB citation guide.

Consequence: "fill the journal's template" is unsatisfiable. Build to the
written spec instead, and say so plainly rather than passing off a
self-made file as the official one.

## 6. Template decoys are stronger than filenames suggest

Beyond two same-folder `.docx` files, check PROVENANCE metadata before
trusting any frame. A 37 KB file whose `docProps/core.xml` carries
`<dc:creator>python-docx</dc:creator>`, a stock 2013 creation date and
`customXml/item1.xml` `StyleName="APA"` is python-docx's own default
template with margins edited to match the spec — not a journal artifact.
Its `word/styles.xml` (350 KB, 164 styleIds) looks convincingly "real".

## 7. Submission layout ≠ published layout — but measure BOTH, don't assert

Published galleries are post-acceptance typesetting. Evidence is in the PDF
metadata: `Producer: iLovePDF` (art684/690/698) and `Pdftools SDK` (art644).
They carry 2 columns on the abstract page, author names, `Ngày nhận bài /
phản biện / đăng bài`, and a non-A4 trim (số 68/2026 measured 538.68×765.48
pt ≈ 19×27 cm, while số 52/2022 is A4). `/quy-trinh-binh-duyet` states the
manuscript is submitted **ẩn danh** (double-blind), so those elements belong
to nobody but the editorial office.

Do not stop at "the written rules win". When the author asks for the
published look, build BOTH and let them choose — the house layout is
measurable and reproducible:

```
trim                19.00 x 27.00 cm            14/14 articles
text box            x[42.6, 499.6] pt -> L1.50 R1.38 T1.35 B1.27 cm
body                Times New Roman 13.0 pt, leading ~1.3 (16.8-17.5 pt)
footnote text       10.6 pt   (OOXML stores half-points -> use 10.5)
first-line indent   27.9 pt = 558 twips = 0.98 cm
folio               centred, y=714.8 pt, 13 pt
abstract            TWO columns: Tóm tắt left | Abstract right
labels              'Tóm tắt:' 'Từ khóa:' 'Abstract:' 'Keywords:' = bold+italic
                    (span-level vote 14/14 — NOT bold-only)
headings            1. bold | 1.1. bold-italic | 1.1.1. italic
tables              ruled, 15-42 drawn objects per article
```

Two traps when reproducing it:

- **Footnotes need `footer_distance` ≈ 1.3 cm.** At 0.7 cm the folio lands at
  y=731.1 pt instead of 714.8 pt — 0.55 cm too low.
- **The 2×2 abstract table breaks word counting.** Moving Tóm tắt/Từ khóa/
  Abstract/Keywords out of `doc.paragraphs` into a borderless table makes a
  naive counter add them to the body: measured 9825 → 10247 words, i.e. a
  FALSE breach of the 6000–10000 limit. The journal rule itself excludes
  abstracts and keywords ("không bao gồm tóm tắt hay từ khóa"), so split
  table paragraphs into abstract-layout vs content and count only content.

## 8. Column detection: three wrong detectors, one right one

Verifying "is page 1 two columns?" failed three times before it worked. Each
failure was in the measurer, not the document:

| Attempt | Method | Wrong because |
| --- | --- | --- |
| v1 | leftmost x per y band | columns advancing in lockstep leave no band starting on the right → false negative |
| v2 | bucket spans left/right of `W/2` | published EN column starts x=264 on a 538.7 pt page, i.e. just LEFT of mid=269.3 → 23 EN spans miscounted as left |
| v3 | cluster span starts, ≥10 spans per cluster, gap >100 pt | correct: published (48.0, 23)+(263.7, 23), built (45.6, 23)+(274.1, 23) → both TWO COLUMNS |

Rule: cluster, never threshold on the page midpoint. And when a detector's
verdict contradicts its own printed raw data (clusters clearly showing two
dominant start positions), trust the data and fix the detector.

Also: when measuring a page RANGE with `pdftotext -bbox`, never pass `-f 5
-l 20` in one call — all pages share one y-axis and words from different
pages merge into the same line band. It reported 1 520 "spaces"; per-page
scanning found 7 129. Scan page by page.

Explain every outlier instead of counting it: of 4 inter-word gaps > 6 pt,
2 were raised superscript footnote references `33`/`34` (they land in another
y band) and 2 were table-cell boundaries → 0 unexplained.

## 9. Bibliography traps (all four measured)

- **Heading missed by a length guard.** `DANH MỤC TÀI LIỆU THAM KHẢO` is 29
  chars; an `len(txt) > 30` title test silently skips it, leaving the
  heading justified and unbolded. Threshold must be ≤ 20.
- **Auto-numbering hides the numbers.** pandoc turns `1. Author…` into
  `w:numPr`, so digits never reach the paragraph text and text extraction /
  word counts lose them. Strip `numPr`, prepend a literal `N. ` run and add
  a hanging indent (`w:left=360 w:hanging=360`).
- **Codepoint order misfiles Vietnamese.** Plain Python sort puts `Đ`, `ô`
  and `İ` out of place. Use `locale.setlocale(LC_COLLATE,'vi_VN.UTF-8')` +
  `strxfrm`, then Chicago tie-breaks: 1-author before multi-author, then
  title ignoring a leading A/An/The.
- **Justify stretches lines around DOIs.** The trailing DOI/URL is one
  unbreakable token, so justified entries blow up every space on the line
  (measured `Assessment      Practice.”     Higher     Education   43`).
  Bibliography must be LEFT aligned; after the fix max inter-word gap in the
  list dropped to 3.64 pt against a 3.25 pt median.

## 10. Verify layout by measurement, and audit the measurer

A verifier that silently checks nothing is worse than no verifier: it printed
`SCHEMA VIOLATIONS: 0` / `PASS` while 76 real violations sat in the file. Two
concrete ways that happened:

- **Namespace mismatch in a membership test.** The checker built
  `order = ('tblStyle', 'tblW', ...)` from bare names but compared against
  `short(tag)` which returned `'w:tblStyle'`. Membership was always False, so
  `ranks` stayed empty and `[] != sorted([])` never fired. Give the checker a
  **self-test on a deliberately misordered fixture** and refuse to print any
  verdict when the self-test fails -- that single guard caught it.
- **A detector blind to its own subject.** After removing table borders,
  `page.find_tables()` detected zero tables, so a check phrased as "no black
  lines inside detected table regions" passed *because* the tables had become
  invisible to it. Anchor region checks on something independent of the
  property under test (the `Bảng N.` caption), not on a detector that shares
  the failure mode.

Also: `pdftotext -f 5 -l 20 -bbox` in ONE call gives all pages a shared y-axis,
merging words across pages. It reported 1 520 "spaces"; per-page scanning found
7 129. Scan page by page. And when a verdict contradicts the raw numbers it
just printed, trust the numbers.

Explain every outlier instead of counting it: of 4 inter-word gaps > 6 pt,
2 were raised superscript footnote references and 2 were table-cell boundaries
-> 0 unexplained.

## 11. Colour is a real defect class — and it hides in the STYLE, not the run

Measured escape: the A4 build rendered both titles and all 28 headings in Word
theme accent1 blue (0x4F81BD; 35 spans / 290 words) while all 14 published
articles are 100% `#000000`. Every earlier check passed because none of them
looked at colour.

Diagnosis order that found it: count colours per span in the rendered PDF, then
grep the DOCX for the source.

- `w:hyperlink` count = 0 and no explicit `w:color` in `document.xml` -> the
  obvious suspect (pandoc auto-linking DOIs) was NOT the cause.
- The colour lived in `word/styles.xml`: `Heading 1/2/3` from python-docx's
  default template carry `<w:color w:themeColor="accent1" w:val="4F81BD"/>`,
  and any frame built on that template inherits it.

Fix at both levels, because either alone can miss a path:

1. strip `w:themeColor`/`w:themeShade`/`w:themeTint` from every style's `rPr`
   and set `w:val="000000"`. Setting `w:val` alone is NOT enough — the theme
   attributes override it.
2. set run-level `font.color.rgb = RGBColor(0,0,0)`; run colour outranks style.

Then gate it: check `styles.xml` for any `w:color w:val` != 000000, count
remaining `w:themeColor="`, and count non-black spans in the PDF. Verified
after the fix: `0 non-black spans` on both builds, `Hyperlink` style itself
rewritten to `w:val="000000"`.

## 12. Before calling a typography gap a defect, test content difference

Published articles measured 20-29% italic words in their bibliography vs 11%
in ours, which looked like lost `*...*` markup. Per-word audit of source
markdown against rendered spans showed **37/37 italic spans preserved** -- the
gap was real content difference: Chicago NB italicises whole book/thesis
titles (long Vietnamese titles in the corpus) while our list cites English
journal articles with short journal names. Rule: compare *per-role ratios*
only after confirming the markup survived; a ratio difference is not evidence
of a rendering bug.

## 13. python-docx appends; Word reads sequences strictly

Every hand-built OOXML child lands at the END of its parent, so content is
correct but positionally invalid, and LibreOffice hides it completely (its PDF
renders fine) while Word may drop the element or offer to repair the file.
Measured in one build: 76 violations -- `tblLook before jc` on 4 tables and
`jc before keepNext` on 72 paragraphs.

Fix once, in a shared module, as the LAST step of the build (any later
`append()` re-introduces the error): sort children of `tblPr` (CT_TblPrBase),
`tcPr`, `pPr` (CT_PPrBase), `rPr` into schema order. Two traps:

- `keepNext`/`ind` must precede `spacing` and `jc`; `tblBorders` must precede
  `shd`/`tblLayout`/`tblCellMar`/`tblLook`.
- Do NOT find an insertion anchor by iterating a tuple of tag names -- that
  returns the first *listed* tag, not the first *present* one, and left
  `tblBorders` after `tblLook` on the abstract table. Sort the actual children.

Also avoid `getattr(a, 'x', None) or getattr(a, 'y', None)` on lxml elements:
they are sequence-like, so a childless element is falsy and the wrong root is
picked (raised FutureWarning, becomes a hard bug when lxml changes truthiness).

## 13. A borderless table needs three separate kills

Setting `w:tblBorders val="none"` on all six edges still left one 0.75pt rule
under every header row. Cause chain, each needing its own fix:

1. pandoc's `Table` style carries conditional formatting
   `<w:tblStylePr w:type="firstRow"><w:tcPr><w:tcBorders><w:bottom w:val="single"/>`,
   activated by `<w:tblLook w:firstRow="1">`. Conditional formatting outranks
   plain `tblBorders` -> strip `tblStylePr` from styles AND set `firstRow="0"`.
2. Cell-level `tcBorders` beat `tblBorders` -> write `val="none"` per cell.
3. Child order (see 12) or Word ignores 1 and 2.

Verify by counting black strokes in the rendered PDF, with a control proving
the publisher's conversion preserves hairlines (198 running-head rules survived
across 14 articles), otherwise "no lines found" cannot be distinguished from
"lines lost in conversion".

## 14. Region classifiers: three ways they lied, and the anchoring rule

Classifying "is this wide gap a table gutter or stretched prose?" produced a
false `REAL DEFECT` verdict three times in a row. Each failure was in the
classifier, never in the document:

| Version | Region source | False verdict because |
| --- | --- | --- |
| v1 | `page.find_tables()` | the build is deliberately borderless, so zero tables are detected and every gutter reads as prose |
| v2 | caption `Bảng N.` + next `^\d+\.\s` line | table CELLS are numbered (`1. Nhận diện vấn đề pháp lý`), so the band was cut at the first cell; bands were also per-page and died at a page break |
| v3 | `span_text in cell_text` | PyMuPDF fuses adjacent cells into ONE span, so no single cell contains the fused string |

Rule: anchor region membership on the **DOCX cell text**, not on anything the
renderer can see (borders, detected tables, captions, headings). When a span
fails the substring test, decompose it against the cell list before calling it
a defect -- a fused span is an extractor artefact.

Final resolution of the last outlier, with evidence rather than assertion:
11.4pt gap on p10, left span `'1. Nhận diện vấn đề Người học phải xác '`
fused two cells (whole-span-in-one-cell = False), right span 16/16 chars
matched a cell, all three spans shared baseline y=724.8 and sat below the
caption at y=665.3 -> column gutter, not stretched prose.

Run the same classifier on a build where it is known to be right: the ruled A4
build classified 62 identical gaps as TABLE-GUTTER while the borderless build
called the same text UNEXPLAINED. That cross-build contradiction is the tell.

## 15. A vision report is a CLAIM -- measure the file before believing it

Once `vision_analyze` worked, it reported 11 layout differences, including
"the Vietnamese abstract body is entirely italic instead of only the label".
Direct measurement said the opposite: the house build carried exactly
`italic=2` of 59 words (the two labels) with `TimesNewRomanPS-BoldItal` --
already correct. Acting on that report would have broken a good build.

What the same report DID contain was one real defect, found only because the
measurement was run anyway: the A4 build had `italic=0` labels (13 words, 0
italic) where published art684/685/686 show `13.3% / 15.4% / 4.5%` with every
italic word inside a label. Root cause was in `build_frame.py`: it recognised
the labels (to skip justifying them) but then ran one uniform `style_run(r)`
over all runs, so the italic was never applied.

Rule: for each vision-reported difference, run the corresponding measurement
on the DOCX runs and the PDF spans FIRST. Three outcomes are possible --
real defect, publisher-added element, or hallucination -- and only measurement
tells them apart.

Publisher-added vs author's responsibility, decided by evidence not
assumption: published page 1 carries a journal header, an author block with
`Ngày nhận bài: 10/4/2026` / review / publish dates, rules and issue-relative
page numbers. Acceptance dates cannot exist before submission, so those are
typesetting additions; a double-blind manuscript must NOT carry the author
block. Keep the manuscript anonymous and put identity in the separate
declaration form.

Fixing a straddling label: the boundary can fall inside one run, so split the
run in XML before styling -- deep-copy `w:rPr` onto the new tail `w:r` so
font/size/colour survive, then style head bold+italic and tail roman.

## 17. Đừng dựng "người rơm", và đừng phòng thủ trước cáo buộc không ai nêu

Hai lỗi khung lập luận mà tác giả bắt được, ghi để không lặp:

1. **Strawman ở phần "lý do chọn đề tài".** Bản đầu ngầm bảo giảng viên luật
   không biết phân biệt "đúng giáo trình ≠ đúng luật" / "luật hết hiệu lực vẫn
   dùng cho tình huống quá khứ". Đó là điều hiển nhiên với dân trong nghề → lấy
   nó làm khoảng trống khiến đóng góp thành tầm thường VÀ xúc phạm người đọc.
   Phản biện gạch ngay. Sửa: khoảng trống KHÔNG phải "một hiểu biết còn thiếu",
   mà là "tri thức sẵn có chưa được làm tường minh / kiểm được / tái lập /
   chuyển giao ở quy mô". Chuyển từ "dạy điều hiển nhiên" sang "hệ thống hóa +
   kiểm định + truy vết" — đúng tầm một bài phương pháp.

2. **Phòng thủ lộ ý.** Lần sửa đầu em viết "giảng viên THỪA SỨC phân biệt
   nguồn, nên khó khăn không nằm ở chỗ họ thiếu hiểu biết...". Anh bác: viết
   câu phủ định đó = tự tố cáo mình TỪNG nghĩ họ không biết; "không ai nghi ngờ
   điều đó" nên nhắc tới là thừa và vẫn xúc phạm. Nguyên tắc: **khi viết phải
   đọc ra HÀM Ý câu chữ để lộ, không chỉ nghĩa đen.** Đừng thanh minh cho một
   cáo buộc chẳng ai nêu — hãy phát biểu vấn đề THẲNG ở dạng khách quan
   ("thẩm định là công việc dựa trên phán đoán chuyên môn, phán đoán ấy diễn ra
   trong đầu, không được ghi lại nên không kiểm/tái lập/chuyển giao được"),
   tuyệt đối không nhắc chuyện người ta "biết hay không biết".

Đồng bộ khi đổi khung nền: một thay đổi trục lập luận kéo theo Tóm tắt/Abstract,
1.1, 1.2 (câu chốt mỗi hướng), 1.3, 3.7, Kết luận — sửa hết một lượt rồi mới build.

## 19. Front-matter roles: detect by structure, never by literal string

A build script centred the title with `CENTERED = ("TÊN BÀI VIẾT", "PAPER TITLE")`.
The moment the title was reworded the paragraph fell through to the default `JUSTIFY` branch, so
the title lost its centring **and** inherited the 1 cm first-line indent: line 1 stretched from
the indent to the right margin, line 2 sat left-aligned. It stayed invisible while the title fit
on one line; the first rewording that wrapped to two lines exposed it.

Rule: match front-matter roles by **structure**, not by content.

- Title = paragraph whose letters are all uppercase and whose length > 20 chars.
- Author block = line starting with a superscript marker (`¹²³`), the corresponding-author
  asterisk, a labelled contact line (`Tác giả liên hệ:`, `Corresponding author`,
  `Lead author email:`), or any line containing an e-mail address.
- Never branch on author names, institution names, or title words.

Two guards make this safe:

1. **Over-match test.** Run each detector over the real body and require 0 hits. Body prose never
   starts with a superscript digit and never contains `@`, so the author-block detector is safe by
   construction; the all-uppercase test also returns 0 on body prose and on headings (headings
   contain lowercase).
2. **Branch order.** Put the author-block branch *before* the bibliography-entry branch, then assert
   every reference paragraph is still `LEFT` with a hanging indent -- otherwise a reference whose
   note contains an e-mail gets centred.

## 20. Centred vs justified: measure a published article, then verify by coordinate

Do not decide front-matter alignment from taste. Read x0/x1 per line from a **published** article of
the same venue with PyMuPDF: if x0 differs on every line of the title/author region, that region is
centred; if x0 is constant, it is left or justified. Measured on two published articles of the target
venue, taken from the venue's own archive: title and author block centred, abstract and keywords
justified. Pick the measurement articles from the venue actually being submitted to, and re-measure
when the venue changes -- alignment conventions differ between journals, so a measurement carried over
from another venue is not evidence about this one.

After any layout change, verify by coordinate rather than by eye:

- Derive the text block from **body pages** (most common x0 and x1 over lines with >= 8 words).
  Do not compute the right edge from the margin setting: it misreported 538.6 pt against a true
  541.7 pt and produced 22 false "line overflows the margin" alarms. Measured against the true
  edge, overflows were 0.
- Assert |line centre - block centre| < 4 pt for every title and author line (achieved 1.6 pt max).
- Assert 0 body paragraphs are centred and 0 references lost their hanging indent.

## 21. A tool can report success without writing anything

`skill_manage` returned `operations_applied: 2, success: true` for two patches to this file, yet the
new text existed in **no** copy on disk (`grep -rl` for the marker across `$HOME` found nothing).
Treat a reported write as a claim: after every skill edit, re-read the file from disk and assert the
marker string is present. Verify the *canonical* path, not a mirror -- mirror hashes can match each
other while both miss the edit.

## 22. Choose keywords from measured usage; reject field-generic verbs

Count each candidate phrase in the body (strip tables and citation markers) and require it to be a
concept the article actually builds on, preferring phrases that also appear in a heading. Frequency
alone is not enough: a high-frequency but field-generic term is a bad keyword because it retrieves
nothing specific -- "kiểm chứng"/"verification" appeared 28 times yet belongs to almost every
methods-aware article, and the author rejected it on exactly that ground. Prefer the article's own
apparatus: its named framework, its study population, its analytical object.

Also measure the venue: both published articles of the target venue carried exactly **3 keywords**, not the 6
the draft had. Verify each kept keyword still appears in the body after every revision round; a
keyword used once, or only in the keyword line itself, is not a keyword.

## 18. Checklist before calling it submission-ready

1. `pgSz`/`pgMar` match the proven frame.
2. Full style remap applied (no `Normal`-only body).
3. Caption keep-together block verified by index walk.
4. Figures re-embedded inline with blip ids.
5. Footnote/bibliography regime confirmed with the author.
6. LibreOffice PDF render + 4 academic-prose gates re-run.
7. Title/author centring re-verified **by coordinate** after any rewording of the title.
8. Over-match test run: 0 body paragraphs claimed by the title/author detectors.
9. Every keyword re-counted in the body; venue keyword count matched.
10. Skill edits re-read from disk at the canonical path (a success report is a claim, not a write).
