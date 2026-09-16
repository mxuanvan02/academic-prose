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
