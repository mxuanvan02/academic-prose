# LaTeX Pre-Submission Verification Recipes

Measured on a Vietnamese journal submission (XeLaTeX + polyglossia Vietnamese,
article class). Five reusable gates that caught real defects after all four prose
scans reported clean.

## 1. Prose-extract before paragraph-level scans on LaTeX sources

`academic_discourse_scan.py` run on raw `.tex` reports `clause_overload`
candidates that are pure markup: preamble `\usepackage` chains, `tabular` rows
(`&`-separated cells), `center` title blocks. Measured: 7 candidates, all false
positives; none was author prose.

Adjudication rule: if the quoted "sentence" contains `\usepackage`, `\begin{...}`,
`&`, or `\\` sequences, classify as markup false positive — do not "split" it.

Recipe (strip preamble, floats, tables, bibliography, then commands):

```python
import re
tex = open('main.tex', encoding='utf-8').read()
body = tex.split(r'\begin{document}',1)[1].split(r'\end{document}',1)[0]
for env in ['table','figure','tabularx','tabular','center']:
    body = re.sub(r'\\begin\{'+env+r'\}.*?\\end\{'+env+r'\}', ' ', body, flags=re.S)
body = re.sub(r'\\begin\{thebibliography\}.*?\\end\{thebibliography\}', ' ', body, flags=re.S)
body = re.sub(r'\\[a-zA-Z]+\*?(\[[^\]]*\])?(\{[^{}]*\})?', ' ', body)
body = re.sub(r'[{}$~%]', ' ', body)
body = re.sub(r'&|\\\\', '\n', body)
open('prose_only.txt','w').write(re.sub(r'[ \t]+', ' ', body))
```

Scan `prose_only.txt` for paragraph-level gates; keep sentence-level gates
(vi_ai_pattern, internal_register, process_logic) on the `.tex` directly — they
tolerate markup and must still see captions.

The converse failure is under-extraction. A root file that only `\input`s its
body yields a few hundred words, and every paragraph-level gate then reports
`scan_clean` over almost nothing. Extract each input file, concatenate, and
confirm the word count is plausible for the paper before trusting a clean result.

## 2. Bibliography heading render check (`\refname` trap)

With polyglossia Vietnamese + article class, `thebibliography` can render a
truncated/wrong heading — measured: "Tài liệu" instead of "Tài liệu tham khảo".
Source inspection shows nothing wrong; the defect only appears in the built PDF.

- Verify by `pdftotext main.pdf` and assert the full heading string appears
  immediately before `[1]`. A naive `"References" in text` check silently fails.
- Fix: `\renewcommand{\refname}{Tài liệu tham khảo}` before
  `\begin{thebibliography}` (use `\bibname` for book/report classes).

This extends the citation-bibliography integrity check in SKILL.md §6: presence
of `\bibitem`s is necessary but not sufficient — the rendered heading is part
of the gate.

## 3. Declarations placement from a published article, not from a style guess

To place Lời cảm ơn / Tài trợ / Khai báo sử dụng AI (acknowledgement / funding /
generative-AI disclosure): download one recent published article PDF from the
same journal section and read where its declarations sit relative to References.

OJS galley recipe: `…/issue/current` → collect `article/view/<id>` links →
fetch `article/view/<id>/<galleyId>` (returns the PDF). Measured on an OJS-based
Acknowledgement (with grant code) sits immediately before References.

Vietnamese triad that shipped (unnumbered `\section*`, after Kết luận, before
`\renewcommand{\refname}` + bibliography):

- **Lời cảm ơn** — institution that provided environment + data (name the data:
  "48 tệp PDF giáo trình luật").
- **Tài trợ** — "Nghiên cứu này được tài trợ bởi <funder>, mã số <code>."
- **Khai báo sử dụng trí tuệ nhân tạo** — what AI was used for (grammar support
  in writing, code generation), plus author-responsibility clause. Never draft
  content the authors did not confirm; ask for the exact uses and grant code.

## 4. Per-record dataset-claim verification against the released artifact

When the manuscript characterizes a released dataset ("bộ dữ liệu trắc nghiệm",
"phân bố gần đồng đều", "chia theo giáo trình nguồn"), do not trust README stats
or summary files — download every split and scan **every record**.

HF download: `https://huggingface.co/datasets/<user>/<name>/resolve/main/<path>`
with `Authorization: Bearer <token from ~/.cache/huggingface/token>` for private
datasets. Per-record invariants for an MCQ release:

1. options field is a list of exactly 4;
2. question text non-empty (find the real field name first — `question_content`,
   not `question`; a schema-key dump of one record prevents thousands of false
   alarms from a wrong field guess);
3. options distinct after strip;
4. `gold_index` in 0–3, `gold_letter == 'ABCD'[gold_index]`,
   `ground_truth == options[gold_index]`;
5. aggregate counts (splits, Bloom/label distribution, answer-position balance,
   multimodal count, distinct source docs) reconciled against every manuscript
   table they appear in.

Measured: 14,210/14,210 v1 records passed all invariants; aggregates matched the
manuscript tables exactly (Bloom 4,784/4,711/4,715; splits 9,894/2,144/2,172;
positions A–D 3,544/3,564/3,557/3,545; 48 docs; 29 multimodal). That per-record
evidence is what licenses keeping the word "trắc nghiệm" in the title/abstract.

## 5. Manuscript ↔ GitHub README ↔ HF card drift sweep

A dataset paper has three public surfaces that drift independently. Sweep all
three before submission; measured drift classes:

- **Citation blocks**: three different author lists/titles across GH bibtex,
  HF card "Citation" section, and the manuscript title block. Unify to the
  manuscript (author-confirmed) version.
- **Model version names**: README `Vintern-1B-v3` vs config/manuscript
  `Vintern-1B-v3.5`. The implementation (config.py) adjudicates.
- **Statistics methods**: README "Wilson 95% CI" vs manuscript cluster
  bootstrap; only one describes the reported numbers.
- **Version relation**: HF card says "v2 supersedes v1, do not benchmark on v1"
  while the manuscript reports v1 numbers. The card must state explicitly which
  release the paper's figures come from, or readers/reviewers see a
  contradiction.
- **Broken relative links**: markdown referencing files not in the repo
  (`research/EXECUTION_RUNBOOK.md` etc.). Test every relative path.

Standing rule (this author): prepare fixes, present the diff, **never push
without explicit approval** — on both GitHub and HF. Exception: when the author
explicitly says "cập nhật lên repo github nhé", that is the approval — commit and
push in the same turn.

## 6. pdftotext verification: normalize whitespace before substring checks

Verifying that an edit landed in the built PDF by `phrase in pdftotext_output`
produces false MISS results, because pdftotext inserts line breaks wherever the
PDF wraps — including mid-phrase. Measured: 4 of 8 checks reported MISS on a
correctly built PDF; all 8 passed after normalization. Recipe:

```python
import re
tn = re.sub(r'\s+', ' ', pdftotext_output)   # collapse all whitespace
assert "cụm từ cần kiểm tra" in tn
```

Also normalize the needle the same way (no double spaces, matching dash
characters — the source may use en dash `–` where you type hyphen `-`).

Whitespace collapsing is not enough on its own. Three further ways the probe,
not the manuscript, is wrong:

- **A term broken at its own hyphen.** Line wrapping can split a hyphenated word
  (`load-\nbearing`), which survives whitespace collapsing. Strip whitespace *and*
  hyphens from both sides before comparing.
- **Asymmetric case folding.** Lower-casing the haystack while the needle keeps
  internal capitals (`AoI`) yields a false negative. Fold both sides or neither.
- **Probing the wrong artifact.** Scanning a composite paper PDF for float labels
  also matches prose mentions of the same names and undercounts. Probe the
  standalone float PDF when that is where the target lives.

And never let a pipeline stage consume an exit code: `scanner --quiet | sed …`
prints nothing and `$?` reports the last stage's status, so a "clean" gate proves
nothing. Redirect to a file, then read the code. When a probe disagrees with an
edit that should have produced it, debug the probe before believing either side.

## 7. Every float must be anchored by an in-text \ref before delivery

Author rule (this user, item 3 of a 7-point structural review): "Mọi hình/bảng
nên được nhắc vào trong nội dung bài (\ref{})". A float that no sentence
references is orphaned — the reader has no entry point. Sweep at delivery time:

1. Collect every `\label{...}` inside `figure`/`table` environments.
2. Collect every `\ref{...}` in body prose.
3. Every float label must appear in at least one prose reference *before* the
   float's position (LaTeX floats can move; the reference carries the reader).
4. The referencing sentence must be substantive — "Bảng dưới đây tóm tắt kết
   quả" is `meta_prose`; "Việc cung cấp đoạn trích nguồn đúng làm tăng độ
   chính xác 8,14–20,93 đpt (Bảng~\ref{tab:acc})" is evidence anchoring.

## 8. Adding citations: Crossref-verify each, then check render order

When a review asks to strengthen claims with references ("bổ sung thêm citation ở
một số claim"), the workflow that shipped:

1. **Map claim → candidate source.** Typical gaps in an empirical dataset paper:
   a named statistical test (McNemar 1947), a resampling method (Cameron–Gelbach–
   Miller 2008 cluster bootstrap), a similarity technique (Broder 1997 shingling),
   and a documented phenomenon you observe but do not explain (LLM option-order
   bias — Pezeshkpour & Hruschka 2024; pretraining contamination — Magar &
   Schwartz 2022). Citing the method at its *definition site* and the phenomenon
   at its *observation site* is what turns "chưa xác định nguyên nhân" from a gap
   into a positioned observation.
2. **Verify every candidate through Crossref** (`api.crossref.org/works?query.bibliographic=…`,
   then re-resolve the DOI and compare author/year/title). A candidate whose DOI
   cannot be verified is dropped, not guessed — measured: "Oren 2023 test-set
   contamination" did not resolve to the intended work and was excluded while the
   other five shipped.
3. **Numbered-style (Vancouver) order check after adding entries.** In-text
   citation numbers must equal first-appearance order. Inserting `\bibitem`s at
   the end of `thebibliography` in insertion-order-of-thinking silently breaks
   this: measured, Broder (first used at line 151) was listed *after* Cameron
   (first used at line 149), which would render [19]=Broder, [20]=Cameron while
   the text cites them in the opposite order. Fix by sorting new bibitems by
   first `\cite` position in the source. Verify from the built PDF text:
   for each new ref, find its in-text phrase and the bibliography entry number
   and assert they match (`[18]` McNemar, `[19]` Cameron, `[20]` Broder,
   `[21]` Pezeshkpour, `[22]` Magar).
4. Update the width argument of `\begin{thebibliography}{NN}` when the entry
   count grows past two digits' worth of label width (17 → 22).

## 9. Renaming public artifacts (GitHub repo, HF dataset) mid-submission

When the dataset/repo gets a better name after the manuscript already links the
old one, the rename touches every surface. Measured recipe:

- **GitHub**: `gh api -X PATCH repos/<owner>/<old> -f name=<new>` renames for
  real and old URLs keep redirecting. Then sweep the repo for the old name in
  user-facing docs (README, README_COLAB, LICENSE links, bibtex `url`).
  **Distinguish URLs from provenance paths**: `/content/TQA_Pipeline/...` inside
  scripts and dataset records is the environment where the data was generated —
  rewriting it falsifies provenance and breaks defaults; leave it and say why in
  the commit message.
- **Hugging Face**: the REST API has **no dataset rename** for token auth —
  `PUT /settings {"name": ...}` returns 200 but only sets the display name, the
  repo id does not change (verify via `api/datasets/<new>` → 404). Reliable path:
  `create_repo(new, public)` → `upload_folder(staging)` → verify per-file SHA-256
  remote-vs-staged (8/8 measured) → update every reference → **ask the author
  before deleting the old repo** (irreversible; offer "delete" vs "keep with
  pointer README").
- **Branch sync after rename**: a shallow clone (`--depth`) lacks the other
  branch's refs, so `git checkout -b main origin/main` fails confusingly. Clone
  full, merge, push. Verify with the GitHub compare API (`status/ahead_by/behind_by`),
  not local `git rev-list`, whose merge-base output is meaningless on a shallow
  clone.
- **Final sweep**: grep every artifact (manuscript PDF text, GH README on *both*
  branches, HF card live via `raw/main/README.md`, source-package BUILD.md) for
  the old identifiers; only provenance-path hits may remain.

## 10. Conclusion must contain no measurement values

See SKILL.md "Conclusion progression". Mechanical gate on the built PDF:

```python
i = text.find('Kết luận'); j = text.find('Lời cảm ơn')
nums = re.findall(r'\d[\d.,]*', text[i:j])
# expect [] — the only digit runs allowed are in the footer/page number,
# which pdftotext interleaves; strip standalone page numbers before asserting.
```

Measured false positive to expect: the page number ("10") lands inside the
conclusion span because pdftotext emits footers inline. Check each numeric token
against its raw-text context before calling it a violation.

## 11. Re-verify the shipped bundle after the last edit

Pack the delivery archive from the current build, then extract it into a clean
directory and compile *there*. An archive packed before a later edit silently
ships stale text: the working copy can already be fixed while the bundle still
carries the superseded wording.

Compare extracted against working artifacts at the text level — a digest over
normalized page text — not by file hash. PDFs embed timestamps and document IDs,
so byte-level comparison reports a difference for identical content and invites a
wrong conclusion in either direction.

## 12. Venue-facing punctuation gates must run on the built PDF, not the source

A "remove every colon/dash from headings and captions" request cannot be verified
by grepping `.tex`: much of what the reader sees is generated by packages, and
some of what grep hits is not prose at all.

1. **Package-generated labels.** `Table 1:` / `Figure 1:` / `References` never
   appear in the source. Fix them once in the preamble —
   `\captionsetup[labelsep=period]`, `\captionsetup[table]{name=Bảng}`,
   `\renewcommand{\refname}{Tài liệu tham khảo}` — instead of editing captions
   one by one. This also removes a real defect beyond punctuation: an English
   auto-label in a Vietnamese manuscript contradicts body prose that already
   writes `Bảng 3`, `Hình 2`.
2. **Caption setups do not cover every float type.** `algorithm2e` ignores the
   `caption` package, so `labelsep=period` leaves `Thuật toán 1:` untouched.
   It needs its own `\SetAlgoCaptionSeparator{.}`. After any label change,
   enumerate the float types actually used and confirm each one separately.
3. **Figure text lives in the plotting script.** Axis titles, panel titles and
   legend labels carrying em dashes or `Label:` patterns are in `fig_*.py`
   (`ax.set_title`, `PANEL` dicts, f-string legends). Sweeping only `.tex`
   reports a clean manuscript while the rendered figures still show the defect;
   fix the script and regenerate the figures.
4. **`.bib` notes are submission text.** A `note = {… Không DOI trên Crossref …}`
   verification remark is an internal operations note, and BibTeX prints it in
   the reference list. Audit note fields for provenance/verification language
   before submission.
5. **Three false-positive classes when locating headings by regex.** Page-mapping
   a section by matching its title against extracted text is where self-inflicted
   alarms concentrate. Measured cases, all from one manuscript pass:
   - *Prose wrap.* `-layout` breaks a sentence at the column width, so `… nêu ở
     Bảng 2.` followed by `Tín hiệu xác nhận ACK …` renders as a line starting
     with `Bảng 2.` and looks exactly like a duplicate float label.
   - *Subsection prefix.* Searching for `Kết luận` also matches
     `6.6 Kết luận có điều kiện từ hai năm khí hậu` and reports the conclusion
     four pages early.
   - *Pseudocode line numbers.* `algorithm2e` with `linesnumbered` prints
     `1`, `2`, … `8` down the listing margin; the pattern `^\d\s+(.+)$` then
     "finds" `8 Kết luận` on the algorithm's own page.

   Build the matcher from the real headings instead of guessing them: extract
   titles from the `.tex` (`\section*?{…}`, stripping `\ref`, math and markup),
   then require a **whole-line anchored** match, and normalize quotation glyphs
   (``` ``…'' ``` in source vs `“…”` in text). Confirm every page number against
   the document's own section order before quoting a page count to a third
   party — a page count written into a letter to an editor is a hard assertion.
   Also check float numbers for duplicates per `main.aux`, and normalize
   whitespace before substring assertions.
4. **Match the extraction mode to the document's layout.** Two-column IEEE
   output must be measured with `pdftotext -raw`; `-layout` interleaves the two
   columns on one output line, so line-anchored heading detection finds zero
   sections even though all ten are present. Whichever mode was used to measure
   the reference paper must be the mode used to measure the new one, otherwise
   the comparison table is meaningless in both directions.
5. **Class-specific renderers break naive counters.** Measured on IEEEtran:
   - Tables are numbered with **Roman numerals** (`TABLE I`), so `TABLE\s+(\d+)`
     reports zero tables out of eight.
   - `enumerate` renders as `1)`, `2)`, … not `(i)`, `(ii)`; a gate written
     against the manuscript's intended `(i)` style reports the contributions
     list as missing.
   - `\IEEEauthorrefmark{*}` is a compile error (`Missing number`): the macro
     takes an integer, so a corresponding-author marker must be a number.
   Enumerate the float and list styles the class actually produces before
   writing counters for them.
6. **Vietnamese reference titles require XeLaTeX.** `pdflatex` aborts with
   `Unicode character ậ (U+1EAD)` when a `.bib` entry carries the verbatim title
   of a Vietnamese legal instrument. Do not hand-escape the diacritics (it
   corrupts the citation); switch the engine and pick a font that actually has
   the block — verify with `fc-list <font> :lang=vi`, because TeX Gyre Termes
   reports `NO` for Vietnamese (no U+1E00 range) while Charis SIL reports `YES`.
7. **Section-number matchers must cover the whole Roman range.** A pattern
   listing `I|II|III|IV|V|VI|VII|VIII|IX|X` silently drops XI–XIV, so a
   fourteen-section paper reports ten and looks structurally deficient. List the
   numerals longest-first, or count `\section` occurrences in the source and use
   the PDF only as a cross-check.
8. **Enumerated-item matchers must tolerate inline emphasis.** An item opening
   with `\emph{…}` renders italic, so `^\s*(\d)\)\s+[A-Z][a-z]` matches nothing
   and a complete contributions list reads as absent. Anchor on the numeral alone
   (`^\s*(\d)\)\s+\S`) and assert the count, not the casing.
9. **A citation that fails to resolve is a fabrication risk, not a formatting
   problem.** Guessing a DOI and letting it into the bibliography is the failure
   mode to prevent: a plausible-looking DOI can resolve to an unrelated paper in
   the same journal. Query Crossref for the entry, read back title/container/
   year, and only then write the `.bib` record. Equally, check that a cited
   source is *on topic*: a meta-analysis of yield and water use does not support
   a claim about methane reduction, and the mismatch survives compilation
   silently.
6. **Protected zones still apply inside generated output.** Em dashes that
   survive in the reference list are often part of registered titles
   (`Crop Evapotranspiration — Guidelines…`, `Crop salt tolerance—current
   assessment`). Resolve each residual against Crossref `container-title` /
   `title` and leave the citation intact.

**Normalize whitespace before every substring assertion.** `-layout` output
breaks a long title or heading across lines, so an exact `in text` check on a
multi-word string reports FAIL on a correct document. Assert against
`" ".join(text.split())` for phrase checks and keep the raw text only for
line-oriented checks (labels at line start). A self-inflicted false FAIL here
is worse than a missed defect: it sends the author back to "fix" wording that
was already right.

Whitespace *normalization* is still not enough for **URLs and long unbreakable
tokens**: LaTeX may wrap a URL at `/` or `.`, and the line break survives as a
newline that normalization turns into a space *inside* the token
(`…/mxuanvan02/ TwinGate`). For URL/token counts, assert against
`re.sub(r"\s+", "", text)` (all whitespace stripped). Measured: a 3-URL gate
reported 2/3 after normalization and 3/3 after full stripping — the missing
URL was present and correct in the PDF all along.

Gate recipe: build, then assert on the whitespace-normalized PDF text — zero
`^(Bảng|Hình|Thuật toán|Table|Figure|Algorithm)\s*\d*\s*:`, zero em dashes
outside the reference list, zero `PLACEHOLDER`, funding string present, both
language versions of the title/abstract matching in claim, and float numbers
free of duplicates per `main.aux`.
