# Page-Budget Compression for LaTeX

Worked recipe for absorbing new content into a page-capped LaTeX manuscript
without deleting evidence. Derived from a measured case: a 15-page LNCS
submission had to gain two TikZ figures and a new results subsection, and ended
at 16 pages with the body *shorter* than the original.

## Order of operations

1. Snapshot the original source and build it in the same environment, so you have
   a true baseline page count. A baseline you cannot rebuild is not a baseline.
2. Lock the numeric invariant (§1 below).
3. Measure page fullness (§2) — this decides whether prose is even a lever.
4. Diagnose by drift analysis (§3) to localise where the extra height came from.
5. Pull levers in yield order: captions → duplication → typography → prose (§4).
6. Handle figures as a height-and-floor problem, not a word problem (§5).
7. Re-verify everything after the final build (§6).

## 1. Numeric invariant

Extract the distinct set of numeric tokens from every prose file and keep it.
Any compression batch that shrinks the set has deleted evidence.

```python
import re, sys
FILES = ["main.tex", "results/final_results.tex", "results/final_discussion.tex"]
nums = set()
for f in FILES:
    t = open(f, encoding="utf-8").read()
    t = re.sub(r"(?<!\\)%.*", "", t)          # strip comments only
    nums |= set(re.findall(r"\d+(?:[.,]\d+)*", t))
open(sys.argv[1], "w").write("\n".join(sorted(nums)) + "\n")
print("distinct:", len(nums))
```

Compare after each batch:

```python
base = set(open("baseline.txt").read().split())
now  = set(open("now.txt").read().split())
print("LOST:", sorted(base - now) or "none")   # must stay empty
print("ADDED:", sorted(now - base) or "none")  # inspect, usually harmless
```

Two measured cautions:

- **A shrunk set is a real finding; a grown set usually is not.** `\label{eq:g78}`
  contributes the token `78`. Confirm an addition is a label or identifier
  before reporting it.
- **Repeat counts may legitimately collapse.** De-duplicating a number from three
  sections to one site plus `\ref` reduces occurrences, not the distinct set. The
  distinct set is the invariant; occurrence counts are not.

## 2. Page fullness decides whether prose is a lever

If every page is already full to the last line, removing words only reflows text
into the same number of lines. Measure before cutting.

```python
import fitz
d = fitz.open("main.pdf")
for i, p in enumerate(d, 1):
    bs = [b for b in p.get_text("blocks") if b[4].strip()]
    if not bs: continue
    print(f"p{i:2d} bottom {max(b[3] for b in bs):6.1f} "
          f"words {len(p.get_text().split()):4d} drawings {len(p.get_drawings()):4d}")
```

Measured result on a 16-page manuscript: pages 1–15 all bottomed at 665.7–668 of
666pt usable, i.e. **completely full**. Page 16 held 57 words (two bibliography
items, ~90pt). So the gap was ~8 lines — and prose cuts inside an already-full
document shift that gap around without closing it. This is why the first three
compression passes moved nothing.

Also look for *slack* rather than assuming uniform density: a float placed badly
leaves a half-empty page. In this case there was none, which is itself the
finding — with no slack, only the levers in §4 that genuinely remove lines work.

## 3. Drift analysis localises the extra height

Compare section-by-section line counts between the original and current built
PDFs. Word counts hide this; line counts expose it.

```python
import fitz, re
HEADS = ["Abstract","Introduction","Related Work","Method","Experimental Setup",
         "Results","Discussion","Conclusion","Data Availability","References"]
def per_section(path):
    txt = "\n".join(p.get_text() for p in fitz.open(path)).replace("\u2014","---")
    idx = sorted((m.start(), h) for h in HEADS
                 for m in [re.search(r"\n"+re.escape(h)+r"\n", txt)] if m)
    idx.append((len(txt), "END"))
    out = {}
    for i in range(len(idx)-1):
        seg = txt[idx[i][0]:idx[i+1][0]]
        out[idx[i][1]] = (len([l for l in seg.split("\n") if l.strip()]),
                          len(seg.split()))
    return out
o, n = per_section("orig/main.pdf"), per_section("main.pdf")
for h in o:
    print(f"{h:22s} lines {o[h][0]:4d} -> {n[h][0]:4d}  ({n[h][0]-o[h][0]:+d})")
```

Measured output on the case:

| Section | Original lines | Current lines | Δ |
|---|---|---|---|
| Introduction | 51 | 53 | +2 |
| Method | 228 | 228 | 0 |
| Experimental Setup | 73 | 70 | −3 |
| **Results** | **157** | **173** | **+16** |
| Discussion | 69 | 70 | +1 |
| Conclusion | 13 | 9 | −4 |
| **References** | **146** | **152** | **+6** |

The +16 in Results was the new reviewer-mandated subsection, and +6 in References
was one added citation with a DOI URL. Neither was deletable. That table is what
proved the page growth was structural rather than verbose.

## 4. Levers in measured yield order

**Captions (highest yield).** Authors do not treat captions as prose, so they
bloat. Measured: two newly written captions ran **102 and 109 words** against the
author's own **34-word** caption for a comparable figure. Cutting both to ~55
words — keeping every number, every `\eqref`, and enough text that the figure
remains self-contained — freed roughly a page on its own. Rule of thumb: a
caption states what the figure shows and what the marks mean; anything that
repeats body prose belongs in the body.

**Cross-section duplication.** Track where each number appears:

```bash
for n in "0.40" "0.18" "2091" "2056" "37/44" "85"; do
  echo "[$n]"; grep -rn "$n" main.tex results/*.tex
done
```

In the case, admission rates appeared in abstract, introduction, methods, results
and discussion; prompt lengths in two places; per-gate rejection counts in two.
Keep one site, replace the others with `\ref` or a short clause. Freed ~200 words
with zero datum lost. Do not delete a number from the section where it is the
evidence for a claim.

**Typography that changes no content.** `\usepackage{microtype}` was absent from
the preamble. Adding it — protrusion and expansion only, no change to font size,
type area or margins — moved the overflow page from 235 words to 163. This is
legitimate because it alters no content and no venue-fixed dimension. Check first
that the author has not deliberately locked the preamble; the case manuscript
carried a comment saying font size, type area and margins were untouched, which
`microtype` respects.

**Prose (last).** Only where genuinely redundant: recap paragraphs, connective
padding, a sentence whose content the figure or table already carries. Measured
yield per pass was low (0–2 lines) once the above were done, because the document
was already dense.

**Levers that failed — do not retry blind:**

- `\looseness=-1` on four long paragraphs: no change. TeX cannot compress a
  paragraph with no slack.
- Shortening prose when the spill is a **large block**: reflow only. The measured
  case cut ~350 words from a full 16-page manuscript and stayed at 16.
- Removing a displayed-equation line break to save height: it *added* height when
  a shared `\label` had to be split into two, because two lines occupied what had
  been one.

## 4b. When prose compression does work: the spill is a heading, not a block

The item above is not "prose never helps". It fails when the overflow page holds a
large body of content that must all move. It **succeeds** when the spill is small
enough that a handful of saved lines pulls a *heading* up one page, because the
block under that heading then reflows into the space the heading vacated.

Measured: LNCS manuscript at 16 pages, page 16 holding 12 bibliography lines.
Pages 1–15 each ended at 665.9pt against a type-area bottom of 665.9pt — full to
the last line, so there was no slack to absorb anything and every saving had to
come from real line reductions. Fourteen prose sites were tightened (restatements
and wordy constructions only, no datum, bound, limitation or hedge removed):
**4692 → 4658 words, and the document reached 15 pages**, with References starting
on page 15 and zero spill. The yield was not proportional to the word count; it
came from ~12 saved *lines*, which was exactly the cost of moving the References
heading from page 16 to page 15 and letting 64 bibliography lines fit there.

So budget prose cuts in **lines toward the heading move**, not in words toward a
percentage. Rule of thumb from the two measured cases: if the spill is more than
roughly a third of a page of continuous content, prose is the wrong lever; if the
spill is a heading plus a few lines, prose is the *only* lever left once captions
and typography are spent.

**Check whether the caption lever is already spent before ranking it first.** The
ordering above assumes captions are fat. Measure them: in the LNCS case all
captions totalled **126 words with a 37-word maximum**, so lever 1 was unavailable
and `microtype` was already loaded with `\looseness` unused, so lever 3 was too.
A ranking is a prior, not a measurement.

## 4c. Measure fullness against the type area, not the paper

To find out whether pages have slack, divide the last text baseline by the
**type-area height**, not by the paper height. Using 842pt (A4) on an LNCS build
reported every page as ~68% full, which made all fifteen pages look like they had
room to give and pointed at a lever that did not exist. The correct denominator
made the opposite visible: `bottom == type-area bottom`, i.e. zero slack anywhere,
which is precisely why only genuine line reductions could help.

Likewise, take per-section budgets from the `.tex` sources. Slicing the extracted
PDF at `\section` boundaries makes the final section swallow the References
(measured: "Conclusion" reporting 797 words, Abstract reporting 0).

## 4d. Test whether the weakest cut was necessary

A compression pass that reaches the target usually contains at least one edit that
bought nothing, because page count is quantised. Identify the cut that most
damaged the prose — typically one that replaced a self-contained claim with a
cross-reference, which the Conclusion must never do since it has to close the loop
on the stated objectives — and rebuild **both** versions in scratch.

Measured: with the cross-referencing Conclusion the build was 15 pages with zero
spill; restoring the self-contained Conclusion was *also* 15 pages with zero spill.
The weaker wording had purchased nothing, so the stronger one went back at no
cost. The only difference worth reporting was informational: References moved from
page 14 to page 15, so body length read 14 pages instead of 13, while the total
the venue counts stayed 15.

When reading the edited regions back, normalise whitespace in both probe and
haystack before matching — LaTeX source line-breaks mid-phrase, and a probe with a
single space silently misses an edit that landed. Print the neighbourhood and read
it; do not extract sentences with `rfind('. ')`, which walks back past the edit
into the previous section. And when the boundary check greps the rendered PDF,
expect hyphenation (`seman- tic`): a strict pattern will report a missing claim
that is in fact present.

## 5. Figures: height cost and the legibility floor

A figure embedded at `\textwidth` scales by `textwidth_pt / canvas_width_pt`, and
every font scales with it. The 6pt floor therefore imposes a **maximum canvas
width**, which in turn caps how short (wide) a figure can be made:

```
canvas_max = smallest_standalone_font_pt × textwidth_pt / floor_pt
```

Measured for LNCS (`textwidth = 345.83pt`, floor 6pt, `\footnotesize` math
subscripts at 6pt): `canvas_max = 6 × 345.83 / 6 = 346pt`. The two figures sat at
323pt and 340pt — already at the ceiling. Neither could be widened to reduce
height. Compute this **before** laying out; designing a figure wide and scaling
it down is the usual way the budget becomes unreachable.

Measure the embedded font on the **built manuscript page**, not the standalone
crop. The same figure reported 5.5pt standalone and **4.34pt** embedded at
scale 0.787.

```python
import fitz
d = fitz.open("main.pdf")
for i, p in enumerate(d, 1):
    if "Fig. 1." in p.get_text():
        sz = [s["size"]/0.996264 for b in p.get_text("dict")["blocks"]
              for l in b.get("lines", []) for s in l.get("spans", [])
              if s["text"].strip()]
        print(f"p{i}: min {min(sz):.2f} TeXpt, spans under 6pt: {sum(x<6 for x in sz)}")
```

The `0.996264` factor converts PDF big points to TeX printer points
(`72/72.27`); without it every 6pt font measures 5.98pt and looks like a failure.

**A pre-existing figure can carry the same defect.** The author's own admission
figure rendered its `×` marks at 5.5pt standalone → 4.34pt embedded, and a
document-mode scan reported **50** sub-floor spans. It was present identically in
the original 15-page build, so it was a latent defect, not a regression. Fixing it
meant raising the mark size in the generating script (5.5 → 8.0pt, and the tick
labels 7.5 → 8pt, since bumping only the marks exposed the ticks as the new
minimum) and regenerating from the published records. Verify that **only** the
font changed: page size identical, the fill-colour multiset identical
(24/10/11/6/6 plus 170/73 cells), and the mark counts identical (73 `×`, 170 `·`).
Extracted-token count *did* move (263 → 240) purely because larger glyphs merge
into fewer text spans — confirm by counting marks, not tokens, before treating
that as data loss.

## 6. Re-verification checklist after the final build

Run all of these; a clean build alone proves nothing.

1. `pdflatex → bibtex → pdflatex → pdflatex`, exit code 0.
2. Zero undefined references and citations; zero overfull hboxes and vboxes.
3. Numeric invariant intact (§1).
4. Every `\label{fig:*}` and `\label{tab:*}` is targeted by at least one `\ref` —
   check programmatically, both directions (unreferenced labels and dangling refs).
5. Document-mode geometry gate on the built PDF, including the small-text check,
   across **all** pages.
6. Per-figure gates on the standalone crops, plus any check the gate does not
   perform (for TikZ: arrowheads erased by a later white mask — see the
   tikz-geometry-gate skill).
7. Float placement: caption page against first-`\ref` page. A figure drifting 12
   pages from its first reference is a defect even when the build is clean.
8. Zip the package without build artifacts, extract into an empty directory, and
   rebuild: same page count, same text. Confirm figure sources in the package
   still compile.
9. If a data/code repository ships a verifier for reported quantities, re-run it —
   prose edits must not disturb any number it recomputes.

## When to stop and ask

Stop at the floor. If the only remaining candidates for deletion are content a
reviewer or supervisor mandated — stratified bounds, limitations, a disclosed
deviation — report the measured ceiling instead of shipping a thinner argument.
In the case: 16 pages with three figures and all mandated content, against a
15-page target, with the shortfall attributable to +16 lines of required results
and +6 lines of required references, quantified by §3.

Moving material to an appendix does **not** reduce total page count of the same
PDF. It helps only when the venue counts the main body separately. State which
applies before offering it as a fix, or the promised page saving will not arrive.

### The references-only last page is the real floor

A measured end state: after compressing every prose block over 130 words
(17 blocks) plus the abstract, the final page held **only** bibliography entries
(307 words, ending at 512pt of 666), while the page above it was full at
665.9pt. At that point no further prose cut can reach the target, because the
remaining overflow is reference lines, not body lines. Diagnose this state
before promising another page: print the last page's word count *and* its
content head — if it starts with bibliography entries, the body is already
compressed to its floor.

The remaining levers then all touch the citation apparatus, which is the
author's evidence, not padding: dropping long DOI/URL rendering, tightening
`\itemsep` in `thebibliography`, or shortening venue names. Each is a decision
for the author or supervisor, not a mechanical cleanup — ask, with the measured
line count needed, rather than editing citations unilaterally. In the case the
answer was to accept one page over target with the body intact.

One caution from the same run: after 17 compression patches the body word count
can *rise* slightly (6,242 → 6,390) because rewriting long paragraphs into
shorter sentences adds line breaks, and words-per-line drops at paragraph ends.
Judge compression by rendered lines per section (drift analysis, §3), never by
word count — the same trap as judging a page budget by words.
