# Word-cap budget compliance (whole-body caps)

The abstract contract already warns against compressing "in build space." This file
covers the harder case: a **whole-body cap whose scope includes the citation
machinery**, e.g. Vietnamese journals stating `6.000 - 10.000 từ, bao gồm chú thích
chân trang và danh mục tài liệu tham khảo (không bao gồm tóm tắt hay từ khóa)`.

The failure this prevents is not overlength. It is **spending an entire session
converging on a number** — measured: nine compression passes over one manuscript
(11,647 → 11,483 → 11,310 → 11,239 → 11,173 → **11,211** → 10,789 → 10,454 → …
→ 9,999), where one pass moved the wrong way and several cost a full DOCX rebuild
for a net gain under 100 words.

## 1. Read the cap's scope before writing a sentence

Four independent questions, all answered from the venue's own text:

- Does the cap include **footnotes**? (Chicago NB venues: usually yes.)
- Does it include the **bibliography**?
- Does it include **tables**? (Usually unstated — assume yes, because Word counts them.)
- Is the **abstract excluded**? (Usually yes, with its own separate cap.)

A cap of 10,000 "including footnotes and references" is not a 10,000-word prose
allowance. In the measured case it was a **7,540-word** prose allowance.

## 2. Cost the incompressible machinery FIRST, then budget backwards

Footnote definitions and bibliography entries are near-incompressible: their length is
fixed by the citation style, not by your prose. Measure them before drafting.

Measured cost, Chicago Notes-Bibliography, 37 sources / 60 note markers:

| Component | Words | Compressible? |
|---|---|---|
| Footnote definitions (60 notes) | ~1,330 | No — style-fixed |
| Bibliography (37 entries) | ~1,129 | No — style-fixed |
| Tables (4) | ~775 | Partly (cell wording) |
| **Machinery subtotal** | **~3,234** | |
| Prose allowance under a 10,000 cap | **~6,770–7,540** | Yes |

So: `prose_allowance = cap − footnotes − bibliography − tables`. Compute this number
**once**, write to it, and stop treating the cap as the prose target.

### The call for papers and its own attached template disagree — read both, take the intersection

Venues routinely publish a number in the notice and a different one in the template they
attach. Measured case: the notice said `tóm tắt 200–250 chữ`, `4–6 từ khóa`,
`5.000–7.000 chữ`; the attached template said `tói đa 200 từ`, `tối đa 5 từ khóa`,
`không quá 9 trang A4`. Four of the five figures conflict, and the binding document is
the template — it is what the editor will paste the submission into.

Resolve this at intake, before drafting, by intersecting:

| Constraint | Notice | Template | Write to |
| --- | --- | --- | --- |
| Abstract | 200–250 | ≤200 | **exactly 200** — the only value in both ranges |
| Keywords | 4–6 | ≤5 | **4 or 5** |
| Length | 5.000–7.000 words | ≤9 pages | both; see the floor/ceiling trap below |

A figure that satisfies only one document is a defect the other document's checker will
flag. Landing the abstract on exactly 200 words cost three rebuilds when discovered late;
costed at intake it costs one.

Also read the template for requirements the notice omits entirely. The same template
demanded a full English title plus Abstract and Keywords blocks, and a declaration of AI
tool use — neither appeared in the notice. A submission missing a required block is
rejected on format before a reviewer reads a word.

### A word floor with a page ceiling is a trap — measure both after every pass

`5.000–7.000 words` and `≤9 pages` are not redundant statements of one limit. They point
in opposite directions once the manuscript is dense: at 12 pt single-spaced with 3 cm
margins, ~6.100 words of Vietnamese fills nine pages, so the floor and the ceiling leave
a window of a few hundred words and no more.

Consequences that must be planned for:

- **A reviewer fix that restores omitted content can push the page count over.** The
  restore is not optional and the ceiling is not negotiable, so the space has to come
  from cutting what the restore made redundant — not from refusing the fix.
- **Re-measure the rendered page count after every content pass**, not at delivery. A
  pass that adds three sentences of substance is exactly the pass that breaks the
  ceiling, and it looks harmless in the word count.
- **Read the page count from the converter's own line.**
  `pdfinfo file.pdf | awk '/Pages:/{print $2}'` is unambiguous; a looser pattern like
  `grep -o '[0-9]*$' | head -1` matches a number out of any trailing field and will
  report a nine-page document as two.

## 3. Citation density is a budget decision, not only a quality decision

Chicago NB charges **twice** per source: a full first note (~25–30 words) plus a
bibliography entry (~30 words). Each additional source therefore costs ~60 words of
cap before a single sentence of analysis.

Consequence: when a venue demands a minimum reference count (e.g. `≥10`), decide the
target count against the budget *before* drafting the literature review. Going from 6
to 37 sources consumed ~1,900 words of cap — a legitimate trade (the review became the
paper's strongest section) but one that must be **planned**, not discovered at
rebuild #7.

Never delete a verified source purely to fit. Compress prose instead, or ask the author.

## 4. Count in the delivered artifact's model, never in the source

Markdown and Word disagree, and Word is the one that matters:

- Markdown `\S+` counts inflate: table pipes (`|`, `|---|`) and footnote markers
  (`[^n12]`) each register as "words."
- Word counts table cell text; a naive body-text extractor skips it.
- Measured divergence on the same manuscript: **9,999** by the Markdown estimate vs
  **10,138** measured inside the built `.docx`. The gap was enough to fail the cap.

Extract from the built artifact: `document.xml` paragraphs **plus** table cell text
**plus** `footnotes.xml` bodies. Verify the same way for margins, font size, line
spacing, footnote count, and reference count.

## 5. Write a build+verify script on the first build, not the tenth

Every manual rebuild is a chance to lose the footnote wiring or the page setup. Make
one idempotent script that converts, applies formatting, and prints a compliance table
in one run. Then each compression pass costs one command.

The script must print, in one block: page size, all four margins, body font/size, line
spacing, footnote ref count vs footnote body count, reference count, abstract word
counts, and the scoped body total against the cap. Anything not printed will be the
thing that silently breaks.

Pitfalls that cost real time:

- A **minimal pandoc reference `.docx` has no table styles.** `table.style = "Table
  Grid"` raises `KeyError: no style with name 'Table Grid'`. Apply `tblBorders` XML
  directly instead of naming a style.
- **Footnote survival is the thing to assert.** After any rebuild, check
  `footnotes.xml` exists and that ref count == body count. A smaller output file is a
  signal to verify, not to assume corruption: in the measured case a 39 KB build had
  the same 60/60 footnotes as the 52 KB one.
- Convert markdown footnotes with `-f markdown+footnotes` so they become **real Word
  footnotes**, not inline text.

## 6. Compress by rhetorical redundancy, never by nibbling

If a pass yields under ~100 words, the method is wrong. Stop editing sentences and
apply the compression order in `manuscript-structural-revision.md` §4: cut interpretation
repeated across Abstract / Results / Discussion / Conclusion first.

Two structural cuts that each freed 300+ words with no loss of claim:

- **Merge a 5-subsection recommendations chapter into one section with bolded lead-ins.**
  Five `##` headings each carrying its own framing sentence became five bold clauses.
- **Collapse a worked example's narration into its table.** If a table already states
  the comparison, the paragraph restating it row by row is redundant.

Also: preserve every footnote marker's position while compressing. Renumber markers
programmatically from a source registry (`{key: {full, short, bib}}`) and regenerate
notes in order of first appearance — hand-editing note keys during compression
produced duplicate keys (`haladyna2002` twice) that silently broke the short-form
chain.

## 7. Delegating exemplar/source retrieval

When fanning out to subagents to find real published exemplars or verify sources,
request `web` and `terminal` toolsets. A `browser`-only child cannot fall back to
`curl` when a CDP endpoint isn't reachable, and returns zero sources after several
minutes. `curl` + a search API is also simply the right tool for static HTML and PDF
retrieval — faster than a browser stack and scriptable.

Retrieval notes that worked:

- Government/portal media endpoints may return **403 on a bare GET**. Retry with a
  `Referer` header matching the hosting site before concluding the file is unavailable.
- Prefer **search-then-fetch**: run the query, collect candidate URLs from results,
  then fetch. Guessing paths on a `.gov.vn` host wastes attempts.
- Verify every DOI against Crossref and keep `verified` separate from `inferred`. In
  one batch, 15/18 guessed DOIs resolved; 3 resolved to a **different paper** than
  intended — a silent failure that only title comparison catches.
- When an institutional library is unreachable, say so with the evidence (status codes
  per URL) and state the **methodological** reason a different source is better, rather
  than presenting the fallback as a consolation.
