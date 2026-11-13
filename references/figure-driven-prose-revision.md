# Figure-Driven Revision: replacing prose with measured graphics

Use when the author asks for "more figures, less text" on a manuscript that
currently has tables only, or when a venue's published articles carry figures and
the submission has none. The deliverable is a build that embeds real images,
passes every existing verifier, and has a **lower** prose word count than before
the figures were added — adding graphics without removing the prose they restate
makes the paper longer and reads as padding.

## 1. Ask whose style is the model, and let the venue arbitrate

An author who says "write like my senior/mentor" may mean a person, not the file
that happens to sit in the project. Two different failures happened in one
session: the agent adopted a paper already recorded in the project ledger as the
"style model" without asking, and later received the real mentor's paper — in
**another language and another genre** (IEEE English CS vs. a Vietnamese
pedagogy journal).

Resolve it in three moves:

1. **Confirm the person**, then locate their work (institutional research
   database, department page, the manuscript's own author list).
2. **Measure the mentor's habits mechanically** — headings, numbered
   contribution list, numbered formulas, algorithm blocks, figure/table counts,
   how weak results are reported, whether limitations get their own section.
3. **Let a published article of the target venue arbitrate.** A habit that both
   the mentor and an already-published venue article share is safe to adopt. A
   habit only the mentor has (numbered formulas, algorithm blocks in a CS
   paper) belongs to the *genre*, not to the person — importing it into a
   pedagogy submission violates venue conventions. Report the split as a table
   (mentor / published venue article / action) so the author can override.

The mentor's paper is still worth mining for habits that transfer across genres:
an explicit numbered contribution list, a "remainder of the paper" roadmap,
transparent reporting of a weak effect ("smaller, high-variance, which we report
transparently rather than overstate"), and a public data/code statement.

## 2. Generate every figure from the measurement bundle

Hard-coding a number into a plotting script creates a second source of truth
that will drift from the prose the next time the measurement changes. Read all
counts from the artifact the project's verifier already treats as canonical, and
`assert` the subset size against the bundle:

```python
BUNDLE = HERE.parent / "framework_application.json"
D = json.loads(BUNDLE.read_text(encoding="utf-8"))
N = D["n"]
...
sub = [r for r in rows if "to_tung_dan_su" in (r.get("item_id") or "").lower()]
assert len(sub) == N, f"focus subset {len(sub)} != bundle n {N}"
assert mat.sum() == N, f"labelled {mat.sum()} of {N}"
```

A first draft of a cross-tabulation figure silently fell back to a **typed-in
3×3 matrix** because the bundle lacked per-item labels; the fix was to read the
raw corpus instead of typing the numbers. If a fallback constant is unavoidable,
make it loud — a bare `mat = np.array([[139, 5, 0], ...])` in a plotting script
is an unauditable number in an otherwise reproducible paper.

Verify Vietnamese diacritics render before drawing anything. Check glyph
coverage with `fontTools` rather than eyeballing a render:

```python
from fontTools.ttLib import TTFont
need = {c for c in sample_text if ord(c) > 127}
cmap = set(); f = TTFont(path)
for t in f["cmap"].tables: cmap |= set(t.cmap.keys())
missing = [c for c in need if ord(c) not in cmap]   # must be empty
```

DejaVu Sans, Liberation Sans and Noto Sans all covered the 55 pre-composed
Vietnamese glyphs used here; tofu boxes appear only with Latin-1 fonts.

## 3. Vision-gate each figure before it enters the manuscript

A figure with clipped text is worse than no figure: it prints, and referees
notice. Send every generated PNG through the vision fallback with a checklist
prompt (text cut off / overflowing its box, overlapping blocks, unreadable axis
labels, Vietnamese diacritics intact) and fix what it reports.

Two traps from one run:

- **An empty vision reply is a tool failure, not a clean bill of health.** One
  figure returned `=== OK ... (0 chars) ===` — re-running with a more concrete
  prompt produced a 650-character list of real defects. Never read an empty
  response as SẠCH; require the model to answer with a literal token (`SẠCH`)
  when it finds nothing, so absence of defects is distinguishable from absence
  of output.
- **Text sized for the figure canvas overflows the box at print width.** A
  caption line inside a 17%-wide box overflowed both edges at 14.6 cm. Fixes:
  shorten the string, drop a font size, or widen the box — then re-run the gate.

## 4. Teach the build script to embed images, and gate placement

A markdown→DOCX builder that only knows tables renders an image line as literal
text. Add an image branch that (a) resolves the path relative to the source
file, (b) honours an explicit width so figures never exceed the text block, and
(c) emits a loud placeholder when the file is missing rather than skipping
silently:

```python
mimg = re.match(r'^!\[[^\]]*\]\(([^)]+)\)(?:\{width=([\d.]+)cm\})?\s*$', sline)
if mimg:
    img_path = Path(mimg.group(1))
    if not img_path.is_absolute():
        img_path = Path(src).parent / img_path
    width = Cm(float(mimg.group(2))) if mimg.group(2) else Cm(14.6)
    if img_path.exists():
        p = para(doc, WD_ALIGN_PARAGRAPH.CENTER, Pt(8), Pt(2))
        p.add_run().add_picture(str(img_path), width=width)
        # caption BELOW the image (venue rule); consume the next line if it is one
    else:
        style_run(p.add_run(f'[THIẾU HÌNH: {mimg.group(1)}]'), SIZE, True)
```

Caption side is a venue rule, not a preference: many Vietnamese journals require
**table titles above, figure titles below**. Encode it in the builder and assert
it in the format audit.

Then verify on the built artifacts, not on the markdown:

- DOCX: count image relationships (`r.reltype` contains `image`), walk
  `doc.element.body` and assert every drawing paragraph is **immediately
  followed** by a `Hình N.` caption paragraph.
- PDF: `page.get_images(full=True)` returns the *resource list* and reported
  "4 images" on all 31 pages. `page.get_image_info()` returns what is actually
  painted — it showed the truth (4 pages, one image each) plus each bbox. Use
  `get_image_info` and compare bbox width against the text-block width
  (page width minus margins) to prove nothing overflows.
- Orphan check: each `Hình N` must appear at least twice (once in prose, once in
  its caption). A figure no sentence points to is a defect.
- Render the figure pages to PNG at ~110 dpi and vision-check them: this catches
  a figure split across a page break and a caption orphaned onto the next page,
  which bbox arithmetic alone can miss.

## 5. Pay for the figures with prose, not with pages

Figures cost ~180 words of caption and lead-in. Recover more than that by
deleting prose that restates what a table or figure already shows:

- **Locate duplication mechanically**: for each prose sentence, test whether its
  distinguishing fragments also occur inside pipe-table lines. Sentences with
  two or more such fragments are restatements.
- **The strongest cuts are whole paragraphs that enumerate per-item results**
  the results table already carries. Replace with one sentence naming the shape
  of the distribution plus a pointer: "Bảng 8 ghi kết quả kèm căn cứ, Hình 3 cho
  thấy hình dạng phân bố."
- **Never cut a string a verifier pins.** Grep the verifiers first
  (`has('…')` in the referee script, `'…' in final` in the assembler) and check
  whether each pin lives in a table row or in prose. Pins inside table cells are
  safe when cutting prose; pins in prose must survive verbatim or the verifier
  must be re-pointed in the same change.
- Measure prose word count **excluding table and heading lines** before and after,
  and report both numbers. The honest target is "four figures added, prose word
  count flat or lower".

Track the word budget across the session: one pass added figures (+178 words)
and only recovered 7, which looked like progress until the count was printed.
Print the count after every compression pass, not once at the end.

## 6. Abstract style: sell the argument, keep one sample size

An abstract dense with percentages (8.6% · 79.1% · 95.1% · 129 · 155 · 2,371 · 14)
is unreadable, and each number is meaningless without its denominator and
method. Rewrite to the five-beat shape — context, gap, idea/contribution,
results **in words**, conclusion plus limits — and keep only the sample size.

But keep the **denominator** when the sample is a subset: "163 items" hides that
this is 163 of 2,371, and an author will notice. "163 trong 2.371 hồ sơ câu hỏi"
costs two words and restores the context.

Word caps bite in both directions. Reaching a ≤250 cap took five iterations of
"measure → cut two words → re-measure"; write the loop so it **asserts before
writing** and refuses to touch the file otherwise:

```python
n = len(cand.split()); assert n <= 250 and not missing_keywords
```

Keyword checks are substring tests against the abstract itself, so trimming to
fund a longer phrase can delete a term the venue requires — re-run the keyword
assertion after every abstract edit. And keep the EN abstract in **hedge
parity**: a qualifier present in one language must be present in the other, and
any verifier that pins a hedge phrase must find it in both.

## 7. Compression is where content gets destroyed

Two self-inflicted losses in one session, both caught only by an audit that
compared against a pre-session backup:

- **A `\s`-class regex swallowed paragraph boundaries.** Cleaning double spaces
  with `(?<=\.)\s{2,}` matched `\n\n` as well and merged 22 paragraphs, headings
  and the keyword line into the preceding prose. Use `str.replace('.  ', '. ')`
  or a `[ \t]` class. When a whole-file mutation goes wrong, rebuild from the
  backup and replay the guarded patch list — never hand-repair.
- **Merging citations merged claims.** Compressing "(Tarrant et al., 2006), the
  effect on learners (Tarrant & Ware, 2008), and non-functioning distractors
  (Belay et al., 2022)" into one clause with three citations deleted the third
  finding and mis-attributed it. Citations are not interchangeable punctuation.

After any compression pass, run a content audit against the backup: diff the
**set of cited authors** and the **set of numeric tokens**. Every "lost" author
must be explainable as a format change (parenthetical → narrative, separate →
grouped), and every lost number must be one the author asked to remove. Also
spot-check that content "deduplicated" from section A still exists in section B —
one dedupe pass deleted a finding outright instead of pointing at its duplicate.

**Restoring a wrongly-deleted finding re-creates the duplication it replaced.**
The Belay restore put the full clause back into the Introduction while the
literature section still carried it; a Jaccard scan over sentence pairs flagged
the pair at 0.96. After any restore, re-run the near-duplicate scan — restoration
and compression are the same operation with opposite signs, and only the scan
sees both.

**Build the cut-candidate list by excluding sentences that hold a single-occurrence
citation.** Count every in-text key across the prose: in one manuscript 33 of 72
keys appeared exactly once, so cutting those sentences orphans a reference and
fails the bibliography check that runs after assembly. Filter candidates to
sentences containing no single-occurrence key and no string a verifier pins, then
sort by length. This turns "find something to cut" from a reading exercise into a
ranked, safe work list.

**Report word count against the right baseline, or the number lies.** Splitting
long sentences *increases* total words slightly while making the text read much
shorter; adding figure captions and lead-ins adds ~180 words. Printing one
"before → after" number hides which pass did what. Print the count after **every**
pass and, at the end, a trajectory table against both the pre-review baseline and
the pre-figures baseline, so "more figures, less prose" can actually be checked
rather than asserted. If review-mandated additions outweigh the compression, say
so plainly and offer the structural lever (move an illustrative section to
supplementary) instead of quietly shaving hedges.
