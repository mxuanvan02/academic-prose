# Venue Constraint Budget and Artifact-Measured Compliance

A manuscript can be argued well, cited honestly, and still be returned by the
editorial office, because venue compliance is arithmetic rather than prose
quality. This reference covers the failure class where **the constraint was
discovered late, or measured in the wrong artifact**.

Two rules carry most of the weight:

1. **Extract every numeric constraint before drafting**, not after.
2. **Measure compliance in the delivered artifact**, never in the source
   Markdown/LaTeX, because the venue counts things the source does not.

---

## 1. Pre-draft constraint extraction

Before writing a word, read the venue's own pages and record every number into a
table you will re-check at delivery. Venue rules are usually split across four
separate pages, and each page holds constraints the others omit:

| Page (typical slug) | Constraints usually found there |
| --- | --- |
| `about/submissions` | file format, submission checklist |
| `quy-dinh-chung` / general rules | **word range**, **reference floor**, font, size, line spacing, margins, page size, page-number position |
| `huong-dan-quy-cach-viet-bai` / style guide | abstract cap, keyword count, required section order, heading style per level |
| `trich-dan` / citation guide | citation system, note vs bibliography form, DOI policy |

Two constraint types are the ones that bite, because they are **floors**, not
ceilings, and no amount of late editing produces them cheaply:

- **Reference floor** (e.g. `Danh mục Tài liệu tham khảo phải có 10 công trình
  trở lên`). A draft built on 6 sources needs a literature pass, not a formatting
  pass. Discovering this after the argument is finished forces either a scramble
  or padding — and padding a bibliography with unread sources is
  `evidence_fabrication` territory.
- **Word floor** (e.g. `6.000 - 10.000 từ`). A draft at 5,991 words is
  non-compliant in the same way a 12,000-word draft is.

Record whether the range is inclusive of footnotes and references. This single
clause moves the effective budget by thousands of words. Measured case: a venue
specifying `6.000 - 10.000 từ, bao gồm chú thích chân trang và danh mục tài liệu
tham khảo (không bao gồm tóm tắt hay từ khóa)` — so notes and bibliography are
**inside** the cap and the abstracts are **outside** it.

## 2. Budget accounting

When notes and bibliography count against the cap, the budget must be
apportioned *before* drafting:

```
cap                     10,000
- bibliography (N refs × ~30 words)        ≈ 1,100   for 37 refs
- footnote definitions (M notes)           ≈ 1,330   for 60 notes
- tables                                   ≈   775   for 4 tables
=========================================================
available for running prose                ≈ 6,800
```

The consequence is counter-intuitive and worth stating plainly: **every source
you add costs prose twice** — once in the bibliography entry, once in the
first-occurrence footnote. A Chicago notes-bibliography venue with 37 sources
spends roughly a quarter of the entire budget on apparatus. Decide the source
count against the budget, not independently of it.

Corollary: a citation-dense related-work section is not free. Budget it
explicitly rather than discovering at delivery that the argument must be cut to
pay for the citations.

## 3. Measure in the delivered artifact

Source-format word counts are wrong in both directions, so a Markdown count is
not evidence of compliance.

Markdown **over**counts:
- table row delimiters (`|`, `|---|`) tokenise as words under `\S+`
- footnote markers (`[^n12]`) tokenise as words
- emphasis and heading syntax (`**`, `##`)

Markdown **under**counts, relative to what the venue's Word counter sees:
- nothing structural, but the net error is unpredictable

Measured divergence from this class of task: source said **9,999** while the
built DOCX measured **10,138** — a 139-word error, enough to fail a cap that the
source appeared to satisfy. The fix is to count inside the DOCX, in three buckets
that must be summed:

1. body paragraphs from the first numbered section onward
2. **table cell text** (python-docx paragraph iteration does not reach it)
3. **footnote bodies** from `word/footnotes.xml`

`scripts/docx_journal_build.py` implements the build and this three-bucket
measurement. Run it, read the printed numbers, and only then claim compliance.

## 4. Compression moves the wrong way — expect it

Rewriting a passage to shorten it reliably *lengthens* it on some passes, because
sharpening an argument adds qualifying clauses. Two measured sequences:

- body: `11,173 → 11,211` (a compression pass that added 38 words)
- abstract: `302 → 283 → 270 → 264 → 258 → 266 → 256 → 254 → 244` (two of eight
  passes moved the wrong way)

Three consequences:

1. **Re-measure after every pass.** Never chain two compression edits and assume
   the direction.
2. **Do not rebuild the artifact to check the count.** Count in text space; build
   once at the end. Each needless build in this class of task cost a full pandoc
   + python-docx + PDF cycle for no information.
3. **When a pass moves the wrong way, stop paraphrasing and start cutting.**
   Paraphrase-compression has a floor; removing a redundant sentence or a
   duplicated hedge does not. Identify passages that restate an earlier point
   and delete them, rather than re-wording the whole section again.

Never cut a limitation, an evidence boundary, a denominator, or a hedge to make
budget — that is `required_move_deletion` or `stance_upgrade`. Cut redundancy,
restatement, and ceremonial framing first; move genuinely surplus material to an
appendix if the venue permits one; and if the budget still does not close, tell
the author which substantive content is at risk and let them decide.

## 5. Sweep the venue's own back-catalogue for related work

**Author-directed rule for domestic and regional venues:** before drafting
related work, sweep the target journal's own published archive and cite the
relevant papers. Editors and referees of a regional journal are frequently the
authors of that archive; a related-work section that cites only international
literature reads as unaware of the venue it is being submitted to.

This is not padding. It changes the argument: it lets the paper state what the
local literature has established and what it has left open, which is a sharper
gap statement than a purely international framing produces.

Retrieval recipe for an OJS-hosted journal (most Vietnamese university journals):

- issue list: `/index.php/<journal>/issue/archive` — **paginated**, follow
  `?page=2,3,…` until a page yields zero issue links
- issue table of contents: `/index.php/<journal>/issue/view/<id>`
- article landing page: `/index.php/<journal>/article/view/<id>`
- article metadata lives in `<meta name="citation_*">` tags on the landing page:
  `citation_title`, `citation_author` (repeated), `citation_date`,
  `citation_firstpage`, `citation_issue`, `citation_doi` when present

Practical notes from a full sweep of one journal (26 issues, 348 articles):

- Filter titles by domain keywords, then read candidate landing pages; title
  filtering alone over-selects (`đánh giá tác động môi trường` matches an
  assessment filter but is not pedagogy).
- Many such journals assign **no DOI**. The citation guide will then require a
  stable, verifiable URL instead. Record the landing-page URL, not the PDF
  galley URL, which changes between galley revisions.
- Author names arrive in inconsistent forms across issues (`PHAN , . T. H.`
  versus `Phan Trung Hiền`). Re-read the landing page for the canonical form
  rather than normalising the malformed one.

## 6. Verify a self-computed corpus statistic before reporting it

When you characterise a corpus with a number you computed yourself — "44% of
items contain an all-of-the-above option" — that number is an `OPEN`
recomputation in the sense of
[Reviewer recomputation gate](reviewer-recomputation-gate.md): its inputs include
your own pattern, which the corpus never stated.

Measured failure from this class of task: a regex for the *all of the above*
distractor reported **44% (26/59)**. The pattern matched the bare Vietnamese word
`cả`, which also occurs in `cả nước` and `bao gồm cả …`. The verified figure was
**12% (7/59)** — inflated nearly fourfold.

Procedure, mandatory before any corpus statistic enters prose:

1. **Print the matched instances**, not just the count. Read a sample of hits
   verbatim.
2. **Print a sample of non-matches** too, to catch the opposite error.
3. Anchor patterns at word boundaries and to the full construction
   (`tất cả các phương án trên`, `cả A, B, C đều đúng`), never to a single
   high-frequency function word.
4. If a reported figure turns out wrong, **retract it explicitly and state the
   cause**, then confirm it is used nowhere else. Silently replacing the number
   leaves the earlier figure alive in the reader's notes.

## 7. Evidence sourcing when the intended corpus is unavailable

Two lessons about where sample items may legitimately come from:

- **A library catalogue is not an item bank.** University libraries hold
  textbooks, theses, and monographs; they do not hold examination item banks with
  answer keys and item rationales. Do not treat "search the library" as a route
  to assessment items.
- **A public competition question set is the wrong population** for a study
  scoped to university coursework, even when it is genuinely official. A
  secondary-school legal-knowledge quiz can supply *formal* parameters (stem
  length, how provisions are cited, distractor style) but contains none of the
  cognitive operations a higher-education framework targets, and usually ships
  **without an answer key** — so it cannot serve as ground truth.
- **Check local project datasets before searching the web.** A prior project of
  the author's may already contain a domain-appropriate, provenance-tracked,
  key-bearing corpus. In this class of task the best available source was a local
  legal-textbook QA dataset with per-item source document, page range, Bloom
  level, and a rubric enumerating `common_errors` — strictly better than any
  public source found, and it was found last rather than first.

When declaring a source, separate what is verified from what the file merely
asserts about itself. A PDF stating `Kèm theo Quyết định số 44/QĐ-BTC` is not a
verified provenance claim if the file was retrieved from a third-party document
mirror and no copy could be located on the issuing body's own site. Under a venue
rule forbidding `nguồn không thể kiểm chứng`, that source is not citable, and
saying so is the correct outcome rather than a failure to try harder.
