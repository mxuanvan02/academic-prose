# Citation–Bibliography Integrity

Measured on a Vietnamese LaTeX manuscript (XeLaTeX + `polyglossia`, `article` class) at a late revision round.

## Failure observed
4 prose gates clean (internal_register 349 sents, process_logic 334, vi_ai 311, academic_discourse 69 paras) yet manuscript had **15 bracket-citation groups** (`[1–5]`, `[6,7]`, `[8,9]`, `[1]..[22]`) and **no §6 Tài liệu tham khảo / References** section. LibreOffice PDF 9 pages rendered without bibliography — submission blocker missed by prose scans.

## Why scans miss it
- `internal_register_scan`, `process_logic_scan`, `vi_ai_pattern_scan`, `academic_discourse_scan` check register/logic/style, not citation resolution.
- `has_TLTK` / `has References` flag must be checked separately.

## Recipe (use docx_accepted_text.py)
1. Dump accepted text: `python3 ~/.hermes/skills/academic-prose/scripts/docx_accepted_text.py --dump <docx> | head -n 200`
2. Extract citations: regex `\[\d+[–\-\d,]*\]` over accepted text; collect unique groups, count total.
3. Check bibliography: search accepted text for headings `Tài liệu tham khảo` / `References` / `Bibliography` (tab-prefixed `\t6\t` form in this template). `has_TLTK == False` is blocker if `cites_total > 0`.
4. Verify coverage: max cited number (here 22) vs entries present. Report `cites_total`, `has_TLTK`, `max_cite`.
5. Office smoke: `libreoffice --headless --convert-to pdf` then `zip_test None` + `paras/tables/media` counts to confirm not corrupt.

## Fix policy
- Never invent bibliography entries to satisfy count. Gate is `submission-integrity` → placeholder or author source required.
- Options offered to author: (a) provide `.bib` / list to insert, (b) insert placeholder `6. Tài liệu tham khảo — [CẦN BỔ SUNG]` with `[n] — cần bổ sung` lines to keep citations resolvable.
- Re-run smoke + cross-copy check after insertion.

## Pitfall to embed
A "clean 4-gate" report is not submission-ready. Always run citation-bibliography check as gate 5 before claiming ready-to-submit, especially for DOCX manuscripts with numeric bracket citations.

## LaTeX variant — the heading can render broken while the source looks fine
Measured on a Vietnamese XeLaTeX build (`polyglossia`, vietnamese default, `article` class): all 17 `\bibitem`s present, citations [1]–[17] resolved, zero build warnings — yet `pdftotext` showed the bibliography heading truncated to `Tài liệu` immediately followed by `[1] Kembhavi…`. The rendered artifact, not the source, carried the defect; both prose scans and a source grep passed.

Rules:
1. Verify the bibliography heading on **pdftotext of the built PDF**, not by grepping the `.tex`: search for the full string `Tài liệu tham khảo` (or `References`) and confirm the first `[1]` entry does not directly abut a partial heading.
2. Fix for `article`: `\renewcommand{\refname}{Tài liệu tham khảo}` immediately before `\begin{thebibliography}`. (`\bibname` applies to `book`/`report` classes.)
3. Rebuild twice, then re-verify heading text **and** full citation range `[1..N]` in the rendered text before calling the build final.

## Prose gates cannot catch a reversed finding — audit claims, not register
Measured on a Vietnamese master's essay: all four prose gates returned clean or licensed-only, yet the draft reversed an empirical result, mischaracterized a legal instrument, and cited a statutory number that had never been verified.

Rules, in the order that catches the most:
1. **Direction of a comparison must come from the paper's own table, never from memory.** Mockus/Fielding/Herbsleb (TOSEM 2002, Table III) reports Apache post-release defect density of 2.64 per KLOCA against 0.1–0.7 for four commercial projects — *worse*, not better — while the pre-system-test figure is 2.64 against 5.7–6.9, i.e. *better*. A result that cuts both ways is the signal you have a real finding; a one-directional paraphrase of a two-directional study is the classic reversal. Fetch the PDF and read the table before writing the sentence.
2. **Name the subject of a legal obligation from the article text, not from the headline.** Regulation (EU) 2024/2847 Art. 3(14) defines the `open-source software steward` as a *legal person* (foundations such as ASF, LF), Art. 2(2) excludes individuals contributing source code outside commercial activity, and Art. 64(10)(b) exempts stewards from administrative fines. "The burden falls on unpaid individuals" is the opposite of what the text says.
3. **Never write a statutory instrument number from memory.** Verify the circular/regulation on an official gazette (Vietnam: `congbao.chinhphu.vn`) and record signer, promulgation date, effective date, gazette issue. Mirror the same rule for CVE IDs (query the NVD API) and DOIs (query Crossref) — a DOI that 404s at Crossref is a fabricated venue or volume.
4. **Delete unsourced superlatives and round quantities.** `hàng triệu ứng dụng`, `phần lớn máy chủ Internet`, `được sử dụng rộng rãi nhất thế giới` read as evidence but carry none. Either attach a citable measurement or recast to the verifiable component list.
5. **Check the bibliography in both directions after every edit round.** Replacing a citation key in prose orphans the bib entry and breaks the other way too; diff `\cite{}` keys against `@type{key}` entries and require both `CITED-NOT-DEFINED` and `DEFINED-NOT-CITED` to be empty.
6. **A lexical gate hit can be a collision — adjudicate, don't blindly rewrite.** `đã biên dịch sẵn` (a prebuilt object file) trips `verification_log_prose`, whose pattern targets first-person process narration. Apply the three tests (admissible semantic subject, work-continues, re-typesetting); if the subject is a world entity and the reader can verify it from the cited source, the verdict is `license` — recast only when an equally exact wording removes the collision without distorting the technical meaning.
7. **Table captions are a licensed exception to the no-colon rule.** `Bảng 1: Tên bảng` is the Vietnamese house convention and appears in the author's own approved theses; `vi_ai_pattern_scan` flags caption colons as candidates by design. Adjudicate them as licensed rather than rewriting.

## Recitals explain, articles bind — never cite a preamble as an obligation
Measured on a Vietnamese master's essay: the draft said the EU Cyber Resilience Act "does not apply to individuals contributing source code", phrased as a binding rule. That sentence lives in **Recital 18**, a non-binding preamble. Article 2 (Scope) contains no such exclusion; the operative threshold is **Article 3(22)**, which defines `making available on the market` as supply `in the course of a commercial activity, whether in return for payment or free of charge`.

Rules:
1. Before attributing any obligation or exclusion to a regulation, locate the sentence and record whether it sits in a **Recital** (numbered `(n)` in the preamble) or an **Article** (binding). Fetch the full text — EUR-Lex HTML is often truncated or JS-gated, so pull it through the Wayback snapshot and grep the plain text.
2. Verify by grepping the article text, not by trusting a summary blog. Blogs routinely state Article numbers that do not exist in the adopted text (one source cited "Article 8" for steward obligations; the adopted text has **Article 24**).
3. Do not put named examples next to a quoted definition unless the instrument itself names them. Grepping the CRA full text for `Apache`, `Linux Foundation`, `Eclipse`, `Python Software Foundation` returned **zero** hits; the regulation only says "certain foundations". Naming ASF/LF right after quoting Art. 3(14) implies the text names them.
4. Cite EU provisions in the form the instrument uses — `Điểm b khoản 10 Điều 64` for Art. 64(10)(b), `Điểm 14 Điều 3` for Art. 3(14). Writing `Điều 3 khoản 14` reverses the hierarchy.

## Verify byline and date from the page, not from memory
The essay credited LWN article 967192 ("How the XZ backdoor works") to Jonathan Corbet. The page's own `FeatureByline` div says **Daroc Alden, April 2, 2024**. Corbet appears zero times. Any web citation must have author and date read off the fetched page; `grep -o 'FeatureByline">(.\{0,160\}\?)</div>'` is enough.

A `curl` HTTP 403/405 does **not** prove a URL is dead. `opensource.org/osd` returned 403 to bare curl but 200 to a browser User-Agent; `arstechnica.com` returns 405/403 to any curl but is live and archived. Test with a browser UA and with the Wayback availability API before reporting a broken reference.

## A reviewer subagent writes its findings into the session DB, not into your file
An independent reviewer was told to append findings to `FINDINGS.md` after each part. It wrote the header once, then stopped updating the file for 40+ minutes while continuing to work — the file looked stale and the run looked hung. The real work product was in `~/.hermes-racer/state.db`, table `messages`, keyed by `session_id`; its tool results contained the verified evidence (CRA article text, Công báo PDF of Thông tư 20/2014, LWN byline, NVD CWE data).

Rules:
1. Before concluding a long reviewer run is stuck, read `state.db` messages for its session — do not judge progress from the mtime of the file it was asked to maintain.
2. `assistant` rows can have empty `content` while `tool` rows carry all the substance; extract tool results too, filtered by keywords from the task.
3. An instruction to "write findings to a file after each part" is not self-enforcing. If the deliverable is the report, require the reviewer to emit it in its final message as well, and treat the file as a bonus.
4. Stop the run when the evidence gathered already covers the brief; a reviewer at 100+ minutes emitting no new claims is spending tokens, not finding defects.

## A co-author's dataset is a citable source, and blinding changes its form

A survey table, coding sheet, or corpus compiled by one of the authors reads as
"ours" and therefore tends to be introduced with an agentless sentence: `Một tác giả
thực hiện mã hóa, không có kiểm tra liên mã hóa`. That sentence names a limitation
but erases ownership, and a reviewer cannot tell whose work it is, whether it is
published, or how to check it. Ownership is a citation obligation even inside the
authors' own paper.

Rules:
1. **Name the compiler and give the artifact a reference entry.** `Bảng khảo sát dùng
trong bài do <tên> lập và mã hóa (<Họ> <năm>)`, plus an APA entry typed as an
unpublished manuscript when it has not appeared anywhere: `Họ, T. (2026). *Tiêu đề*
[Bản thảo chưa công bố]. Đơn vị.` Do not cite it as a published work, and do not
leave it uncited because it feels like an internal file.
2. **Say where the full table can be inspected.** `Toàn bộ bảng mã hóa được công bố ở
Phụ lục A và Phụ lục B để người đọc có thể kiểm tra lại từng trường hợp.` A
single-author coding scheme is only defensible if a reader can recode it.
3. **Put the source note under each table, not only in the Method paragraph.** A
reader who enters at Table 2 never sees section 2. `*Nguồn:* <tên> lập và mã hóa từ
<văn bản> (Phụ lục A).`
4. **In the blinded version, the same citation must survive with the identity
removed.** `compiled and coded by the first author ([Author] 2026)`, table notes
`*Source:* Compiled and coded by the first author`, reference entry
`[Author]. (2026). ... [Unpublished manuscript]`. Then verify: `grep -c '<tên tác
giả>' <bản ẩn danh>` must return 0. Blinding a paper and leaving the author's name
in a table note is the failure this check exists to catch — and the fix is not to
delete the citation, because an uncited dataset is the worse defect.

## A date attached to an event belongs to that event, not to a nearby landmark

Measured on a conference manuscript about two Vietnamese literary works: the draft said
*Tướng về hưu* and *Những ngọn gió Hua Tát* received the State Prize in **2021**, because
the author died in March 2021. Four independent notices carrying the award announcement
give **2022** — the decision was signed in December 2022, in the posthumous round. The
wrong year is the plausible one: it is the year the person died, and it sits beside the
real one.

Rules:
1. An award year comes from the awarding body's own decision or announcement, never from
   the year the recipient died, published, or was honoured by something else. Search
   `<work> <award name> truy tặng` and read the dated notice, not a biography summary.
2. Prefer the notice's own date over a secondary page's summary line. An infobox and a
   newspaper article can disagree; the awarding association's announcement is the
   tiebreak.
3. The same rule governs a reissue year. Two sources dated a novel's reissue under the
   author's own title to 1991, another to 1992. When sources split, name the year they
   agree on or state the uncertainty — never the year that fits the narrative
   (`một năm sau`).

## A sample size comes from the paper's Methods, not from its press release

The same manuscript wrote `hơn 300 người viết` for Doshi & Hauser (2024). The paper's own
dataset statement says `N=293`; 300 is the recruitment figure in the university press
release. Both are true of something; only one is true of the analysed sample.

Rules:
1. Read `N` from the Methods or the dataset description, not from abstract prose and not
   from a press release. Recruited ≠ analysed; excluded participants leave the
   denominator.
2. A replication paper can quote the original's post-exclusion N while the original
   headline quotes the pre-exclusion N. When two papers disagree, the original paper wins
   for the original's claim.
3. Give the analysed N with its referent (`293 người viết`), or hedge explicitly
   (`khoảng 300`). An unhedged rounded number becomes false precision.

## A preprint and its journal version carry different registered titles

A reference entry gave the journal-version title while its identifier pointed at the
arXiv preprint, whose registered title differs. An identifier that resolves proves the
record exists; it does not prove the title matches.

Rule: cite the title registered at the identifier you actually print, and when both
versions exist name which one you read (`arXiv:2504.13868` for the preprint, a `doi.org`
link for the journal version). A reader who opens the link must land on the title and
author list the entry names.

## A reviewer's finding is a hypothesis — verify the artifact before editing

Across five adversarial review rounds on one manuscript, nine findings were raised and
four were false. Acting on them would have introduced the defects the review existed to
remove. The false classes are repetitive, and each names a specific artifact that
settles it in one command.

| Finding | Why it was false | Check that settles it |
| --- | --- | --- |
| "source X is never cited" | cited in the Vietnamese in-text form `Tên và nnk. (năm)`; reviewer grepped `X et al.` | grep the source's **Vietnamese** author form, not the English one |
| "reference Y is never cited" | present; `pdftotext` broke the string across a line | count on `pdftotext - \| tr '\n' ' '`, never on raw line output |
| "bottom margin is 2.86 cm, spec is 2.50" | measured from the last text baseline, not the page box | read `python-docx` `section.bottom_margin`; a short final page inflates any text-based measure |
| "statistic Z is wrong" | reviewer confused two statistics from the same paper | fetch the paper's own sentence and quote it against the draft |

Rules:

1. Before accepting a finding, name the artifact that would prove it and check that
   artifact. A finding not tied to a file, a page, or a quoted source sentence is not
   actionable.
2. **Never change a number because a reviewer disputes it.** Change it only after
   reading the source's own sentence. Two statistics from one paper (a novelty gain and
   a similarity shift, both in the same results section) are the commonest confusion.
3. **Never change a layout spec from a text-position measurement.** Section properties
   are authoritative for margins; PDF `bbox` measures the last glyph drawn.
4. Keep a per-round ledger of findings adjudicated false, so the next round does not
   re-raise them and a real finding is not lost in the noise. Phrase each entry as the
   artifact checked and what it showed.
5. A review that reports only false positives and never a real defect is still useful
   data: it means the manuscript is converging. Do not loosen a gate to manufacture a
   finding.

## A quotation attributed to a literary work must be found in the work

A draft carried a line in quotation marks attributed to a novel, with a page-free
`(Author, năm)` parenthetical. The line was not the novel's prose — it was a critic's
commentary about the novel, recast to read like the text. Nothing flagged it: the
sentence was fluent, the attribution looked complete, and it sat inside an analysis that
read correctly.

Commentary and paraphrase are the common source of a misattributed quotation because
they share the work's vocabulary. The tell is grammatical: commentary **describes** the
text ("the novel shows", "the author sends") while the text **is** the utterance.

Rules:

1. Verify a quoted line from a primary literary work against the work's own text — a
   full-text copy, a scholarly edition, or an excerpt that carries the passage. A
   secondary study quoting the work is not the work.
2. When the exact wording cannot be located, drop the quotation marks and report the
   content, citing the study that discussed it. Never keep quotation marks on text you
   could not find.
3. Apply this hardest to the passages the argument leans on: a load-bearing quotation
   is the one least likely to be checked and most damaging when wrong.

## Pointer in SKILL.md
Section "Evidence-Bound Revision" item 6 now references this file.
