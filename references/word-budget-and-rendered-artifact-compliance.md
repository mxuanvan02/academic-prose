# Word budget and rendered-artifact compliance

Use this when a venue states a **word or page limit** and you must deliver a
formatted artifact (DOCX/PDF) rather than a manuscript source. It covers two
failures that are invisible until they have already cost many rebuild cycles:
budgeting the citation apparatus too late, and measuring the wrong artifact.

Companion to [Whole-manuscript structural revision](manuscript-structural-revision.md)
§4, which owns *what to cut*. This file owns *how much must go, and how you know*.

---

## 1. Read what the limit actually counts

A word limit is a **scope declaration**, not a number. Before drafting, quote the
venue's own phrasing and classify every component as in-budget or out-of-budget.

Measured case (Tạp chí Pháp luật và Thực tiễn, Trường Đại học Luật, Đại học Huế):

> Dung lượng bài viết nghiên cứu lý luận là 6.000 - 10.000 từ, **bao gồm chú thích
> chân trang và danh mục tài liệu tham khảo** (không bao gồm tóm tắt hay từ khóa).

So the budget is:

```
in-budget  = main text + footnotes + bibliography
out-budget = Tóm tắt/Abstract, Từ khóa/Keywords
```

The abstract having its own separate cap (≤250 words) does **not** mean the
abstract is inside the main budget. Two independent constraints, measured
independently.

Corollary that drives everything below: when footnotes and bibliography are
in-budget, **the citation apparatus is not free**, and a citation-dense style
makes it very expensive.

## 2. Budget the apparatus BEFORE writing the main text

This is the single highest-leverage step, and skipping it is what causes the
death-by-a-thousand-cuts loop in §4.

Chicago Notes–Bibliography with first-full/subsequent-short notes costs roughly:

| Component | Rule of thumb (measured) |
|---|---|
| First full note | ~20–30 words |
| Subsequent short note | ~6–11 words |
| Bibliography entry | ~25–32 words |

Measured instance: **37 sources, 60 note markers** cost **1,329 words of notes +
1,129 words of bibliography = ~2,460 words**, i.e. **~25% of a 10,000-word
budget** consumed before a single sentence of argument.

Do the arithmetic first:

```
main_text_allowance = limit − (n_first_notes × 25)
                            − (n_short_notes × 9)
                            − (n_sources × 28)
```

For the measured case: `10,000 − ~2,460 ≈ 7,540 words of main text`. That number
should be fixed **before drafting**, then allocated per section as a hard cap.
Drafting to the full limit and discovering the apparatus afterwards is what
forces a dozen rewrite passes.

Tension to resolve consciously, not accidentally: venues often *also* set a
reference floor (here `Danh mục Tài liệu tham khảo phải có 10 công trình trở lên`).
More sources satisfies the floor while eating the budget. Pick a target count
deliberately — a comfortable margin above the floor, not the maximum you can
find — and state the trade-off to the author if they asked for exhaustive
coverage. Going from 6 sources to 37 tripled apparatus cost and forced the main
text down by ~1,900 words.

## 3. Measure the rendered artifact, not the source

Source-level word counts and the delivered DOCX **disagree**, and the DOCX is
what the editor measures.

Measured divergence on the same content: Markdown reported **9,999**; the built
DOCX reported **10,138**. Causes:

- Markdown table pipes/delimiters (`|`, `---`) are not words, but the rendered
  table's cell text is. Four tables contributed **775 words** in the DOCX.
- Footnote markers (`[^n12]`) count as tokens in a naive source count and vanish
  in the render; footnote *bodies* count in the render.
- A naive `\S+` split over source counts `|`, `---`, and markers as words,
  inflating the source figure in one direction while tables deflate it in another.

**Rule:** the compliance number is whatever you can extract from the built file.
Count three buckets separately from the DOCX so an overage is attributable:

```
main paragraphs (from §1 heading to end)  +
table cell text                            +
footnote bodies
= in-budget total
```

Measure the abstract caps from the DOCX too, and count keywords by splitting on
the list separator (`;`), not on whitespace — a naive whitespace count reported
**4 keywords** for a correct 5-keyword line and triggered a false repair.

See `scripts/verify_journal_docx.py` for the extraction.

## 4. The iterative-nibbling anti-pattern

Observed failure, worth naming because it feels productive: compress a little,
re-measure, compress a little, re-measure. Measured trace across passes —

```
11,569 → 11,483 → 11,310 → 11,239 → 11,173 → 11,211 → 11,094 → 10,966 → …
                                     ^^^^^^ went UP
```

Fifteen-plus passes, and at least one **increased** the count because "tightening"
a paragraph rewrote it longer. Each pass cost a full re-measure, and on a LaTeX
project each costs a full multi-pass build.

Do this instead:

1. Compute the **total overage in one measurement** (`current − limit`).
2. Compute the **per-section allowance** from §2, and measure every section.
3. Identify the specific sections that exceed their allowance and rewrite **those
   sections wholesale, once**, to the target length.
4. Re-measure **once**.

A rewrite-to-target beats N nibbles because you are writing toward a number
rather than away from one. When a pass moves the count the wrong way, stop
nibbling immediately — that is the signal the approach is wrong, not that the
next nibble will land.

Guard rail from the Journal-Template Authenticity Gate still applies: never cut
evidence, denominators, hedges, citations, or a limitation that changes an
inference in order to hit a number. If the content genuinely cannot fit, say so
and ask. Cutting a verified citation to save 28 words is the wrong trade.

## 5. Preserve marker integrity across compression

Compression rewrites the exact strings that carry the notes. Two mechanical
hazards:

- **Duplicate keys.** Reusing a marker name (`[^haladyna2002]` twice) silently
  collapses two distinct notes. Renumber markers to unique sequential keys
  (`[^n1] … [^n60]`) as a build step, generated from an ordered source table, so
  first-vs-short form is derived rather than hand-maintained.
- **Stale find/replace.** After several passes the text no longer matches the
  string you are replacing. Every batch substitution must report misses, and a
  miss means re-read the verbatim text rather than retry the same string.

Invariants to assert after every build: `markers == definitions`, no unused
source, no marker without a definition, and the bibliography entry count equals
the source count.

## 6. Vietnamese journal DOCX formatting

Formatting lives in the artifact, not the Markdown. Pandoc gets the structure and
real Word footnotes; everything else is applied programmatically afterwards.

```
pandoc src.md -f markdown+footnotes -t docx -o tmp.docx
```

`markdown+footnotes` produces genuine `word/footnotes.xml` entries — verify
`footnote refs == footnote bodies` rather than assuming.

Then apply, via python-docx plus raw XML where python-docx has no API:

- page size A4, margins per venue (measured case: top/bottom/right 2cm, left 2.5cm);
- body font and size (Times New Roman 13pt) applied to **every run**, including
  table cells and footnote bodies;
- line spacing 1.5 (`w:spacing w:line="360"`);
- page number centred in the footer via a `PAGE` field;
- heading emphasis by level: `1.` bold, `1.1.` bold-italic, `1.1.1.` italic;
- table borders written as raw `w:tblBorders` XML.

**Pitfall:** a minimal reference DOCX has no built-in table styles, so
`table.style = 'Table Grid'` raises `KeyError: "no style with name 'Table Grid'"`.
Write `w:tblBorders` directly instead of relying on a named style.

## 7. Delivery

Deliver the **DOCX** as the submission artifact when the venue asks for
Word/OpenOffice/RTF; a PDF alongside is a reading convenience only, and should be
labelled as such so the author does not submit it. Report the measured compliance
table (limit vs measured, per requirement) rather than asserting compliance.

## Exclude the label when counting an abstract

A measure routine counted every paragraph matching `^(Tóm tắt|Abstract)` **including its own
label**, so a 250-word abstract reported as 252 against a 250-word cap. Two words of
front-matter furniture ("Tóm tắt.") decided a pass/fail verdict.

Strip the label before counting:

```python
m = re.match(r"^(?:Tóm tắt\.|Abstract\.)\s*(.*)$", text, re.S)
if m:
    abstract_words.append(count(m.group(1)))
```

Same class of error, watch for it everywhere a counter and a renderer share a string: the
keyword line counted with `Từ khóa:` included, the heading counted with its number prefix
(`## 3.1.` adds tokens), table rows counted with their separator cells (`|---|` yields no
words but a row header may be duplicated across a page break and counted twice).

Corollary for reporting: when two counters disagree, resolve the discrepancy before
publishing a verdict. The manuscript-side count (250) and the artifact-side count (252) were
both "correct" by their own definitions; only one matched the venue's definition. Report the
number that matches the rule being applied, and say which rule it is.

## Read the venue's written rules before acting on an inferred house style

A house style measured from two published articles produced two recommendations: compress the
abstract to 150 words and cut the keywords to three. The venue's written Author Guidelines,
read directly from the submissions page, said something different -- abstracts up to 250
words, and **three to five** keyword phrases that **must appear in the abstract**. Both
recommendations were therefore void, and acting on the first would have deleted content for
no requirement while acting on the second would have **violated the written rule**: the
higher-frequency replacement phrase did not occur in the abstract, so the keyword line would
have failed the presence requirement.

Three rules follow, in the order that saves the most work:

1. **Fetch the written guideline before measuring published samples.** A sample of two is a
   hypothesis about the venue, not its rule. The guideline is usually one page and settles
   word caps, keyword counts, reference style, page frame and front-matter order at once.
2. **A written rule and published practice can disagree; do not restructure on the written
   rule alone.** Guidelines for one venue family place the English front matter at the END of
   the paper while its own published articles carry a bilingual front matter at the start.
   Report the divergence and ask the editor; moving a whole block is not a reversible edit.
3. **Measured frequency is evidence for a decision, never a licence to make it.** Choosing
   keywords by body frequency is sound method, but the swap belongs to the author, and the
   venue's presence-in-abstract rule outranks frequency anyway.

If a guideline page resists automated fetching (403 from the extraction backend), open it in a
real browser session rather than falling back to inference -- that is what produced the
numbers above.

## Measure the page budget in the venue's frame, not in the reading frame

A page-count comparison across different frames is not a measurement. The manuscript built
for the author's reading frame (A4, 13 pt, 1.5 line spacing, 2.5 cm margins) ran 37 pages
against a written cap of 12, but that gap mixes content with layout. Rebuild the SAME content
in the venue's frame -- page size, font family, point size, line spacing and all four margins
taken from the guideline -- then count pages of the rendered output. Measured this way the
same manuscript ran 29 pages against the 12-page cap, i.e. 2.4x, with 616 words per page, so
a compliant article holds roughly 7.400 words against the 17.875 present.

Report that as a **scope decision for the author**, with options ranked by how much of the
contribution they preserve (ask whether the cap applies to review articles; split the paper;
compress by moving cases to an appendix), never as a formatting task to be absorbed silently.
Do the frame rebuild as a throwaway probe writing outside the project tree; the deliverable
keeps the author's reading frame until the author chooses otherwise.

### Back up a deliverable before overwriting it, and never let a page count be the acceptance test

The rule above was written and then broken in the same session, at real cost. A rebuild of a
delivered report ran `rm -f <pdf>` with no copy taken first, built through the wrong recipe,
and the previously delivered artifact was gone with no way to reproduce it byte-for-byte: four
recipes were tried afterwards -- plain pandoc→docx→LibreOffice, the manuscript's own builder,
pandoc→xelatex, and pandoc→xelatex with A4 margins -- producing 17, 22, 19 and 0 pages against
the original 16. Exact recovery was impossible; only re-derivation was.

Two rules follow, and the second is the one that actually caused the damage:

* **Copy the artifact to a timestamped backup before any command that writes its path.** A
  rebuild is a destructive operation on a delivered file. `rm -f` immediately before a
  conversion is the most dangerous form, because a failed conversion then leaves *nothing*
  rather than the previous good output.
* **A page count is not an acceptance test.** The first replacement was rejected for running 23
  pages instead of the remembered 16, and a second build was made that produced 17 -- closer to
  the number and worse by every measure that mattered: Letter paper instead of A4, 6 of 13
  content probes absent from the rendered PDF, and the project's own delivery checker reporting
  broken layout on 7 pages plus one lost sentence. The rejected build passed that checker
  outright and matched every probe. Acceptance is the project's own checker plus a
  rendered-text parity probe across source, DOCX and PDF; a page count is an observation to
  explain, not a target to hit.

When a rebuild's page count differs from the remembered one, treat it as a question about the
**recipe** -- which input file, which engine, which frame -- and answer it by finding the
command that produced the original rather than by iterating builds until a number matches. Build
intermediates are the evidence: a reflowed Markdown left in `/tmp` with an mtime two seconds
before the artifact identified the real pipeline, which consumed that intermediate and not the
source file. Guessing recipes cannot find that, because the wrong input and the wrong engine
both look plausible.

### A blocked galley is not a dead end: published length is in the page range

Publisher galleys often sit behind a session cookie that automated fetching cannot
reproduce, so the article PDF is unreachable. Published LENGTH still is: every Crossref
record carries the printed page range, and the span of that range is the article's length in
the venue's own frame. Query `api.crossref.org/prefixes/<DOI-prefix>/works` with a cursor,
group by `container-title`, and measure `last - first + 1` per record. This settles whether a
written page cap binds without downloading a single PDF.

Measured on one venue family, the written cap of 12 pages was contradicted by its own output
across all three journals examined: target journal median 13 pages, max 22, with 58% of 67
measured articles over the cap (72% of the 18 published since 2024); a sibling journal
median 16, max 32, 80% over; a second sibling median 21, max 39, 96% over. A cap that the
venue's own output violates in the majority of cases is stale wording, not a submission
constraint -- but a manuscript longer than the LONGEST published article is still over,
regardless of what the written rule says. Report both facts; they answer different questions.

State the measurement's own limit: a published page range is the length AFTER editorial
layout and possible cutting, so it measures output practice, not the acceptance threshold.

### A 404 from Crossref means "no such journal", not "no data"

Guessing an ISSN produces a 404, which reads like an empty result and invites the wrong
conclusion that the venue publishes nothing. Recover the real ISSN instead of guessing it:
the published article DOIs carry the prefix and a journal mnemonic, in the shape
`<prefix>/<journal-mnemonic>.v<volume>i<issue>.<article-id>`, and querying by prefix
returns every container-title under it together with its ISSNs. Do not paste a real DOI
from the venue in hand as the example: the mnemonic identifies the journal, which makes
the lesson read as that venue's convention and ties a public repository to one submission
target. The shape carries the whole lesson. One journal appeared under TWO container-title spellings,
one of which had no page ranges at all, so selecting by title-match picked the empty group;
query by ISSN and merge the spellings. Also expect partial coverage -- 67 of 149 records
carried a parseable page range -- and report the denominator with the statistic.

## Four ways a verification check reports a defect that is not in the file

All four were measured on the same delivery run, and all four push toward "fixing" a
correct file. The common shape: the probe encodes an assumption about the artifact's
encoding rather than about its content. Write probes against a dump of the rendered text,
never against the source you just edited.

**A markdown emphasis marker does not survive rendering.** A probe written as
`8 / **13** / **22**` -- copied from the source table cell -- can never match, because
pandoc turns `**13**` into a bold run and the literal asterisks are gone. Measured on the
rendered PDF: the entire document contained **zero** occurrences of `**`, while the figure
`8 / 13 / 22` was present. Probes must use the rendered form. The same applies to any
markup the pipeline consumes: `_em_`, `` `code` `` backticks, `[link](url)` brackets,
heading hashes, table pipes.

**PDF text extraction drops spaces after certain diacritic-bearing glyphs.** Five long
headings failed an exact-substring probe while every individual word of each heading was
found. The raw extraction showed the cause: `THỂ LỆ THẬT` extracts as `THỂLỆTHẬT`, `VẤN ĐỀ
CẤU TRÚC` as `VẤN ĐỀCẤU TRÚC`. A visual read of the rendered page confirmed the headings are
correct on screen. The font renders fine; only the text layer loses the space. Fix the probe,
not the document: match on whitespace-squashed text as a fallback, keep the exact match as the
primary signal, and print which mode matched so a squash-only hit stays visible.

**A probe left pointing at a superseded phrase fails on the update.** A delivery checklist
that asserted the presence of a caveat paragraph ("not yet verified") kept failing after the
work it described was completed and the paragraph replaced by the measurement. When a report
records state, its probes must be updated in the same edit that changes the state; otherwise
the checklist measures the previous draft and trains you to ignore red.

**A vision read of a render can misread diacritics.** The same visual pass that correctly
cleared the headings also reported a repeated word, `vé vé`, where the source markdown reads
`vế về` -- zero occurrences of the reported form. Any finding that comes from looking at a
render must be confirmed against the source text before an edit is made, otherwise the
reviewer's own misreading becomes a defect injected into a correct file. This is the same
discipline as §15 of the caption-fix reference: a vision report is a claim, so measure the
file before believing it.

A check that fails on a correct file is worse than no check at all, because the next real
failure gets waved through as another false alarm. When a probe goes red, establish first
which of the two is broken -- the artifact or the probe -- and say so explicitly before
touching either.
