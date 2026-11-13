# Calque Audit: finding word-for-word translations in a non-English manuscript

Use when an author says a phrase "nghe không tự nhiên" / "sounds translated", when a
manuscript was drafted from English sources or by an LLM working in English, or when
reviewing a translation-heavy draft. The deliverable is a list of phrases changed to
idiomatic target-language wording **plus** a list of phrases deliberately kept, each
with its evidence.

## The corpus method fails on genre mismatch — do not trust frequency counts

Counting how often a phrase occurs in a local text corpus looks rigorous and produced
three consecutive false verdicts on one manuscript:

1. A legal-instrument corpus flagged `đặc tả`, `ngữ liệu`, `ánh xạ`, `tường minh` as
   calques (0 hits). All four are standard Vietnamese IT/linguistics terminology; the
   corpus simply never discussed them.
2. A downloaded "same journal" corpus turned out to be the journal's **Natural Science**
   section while the manuscript was education/law — structurally unable to contain the
   manuscript's vocabulary.
3. A section code guessed from a search endpoint (`-ED` read as Education) was actually
   Economics and Development.

Rules:
1. Before using any corpus for wording verdicts, **print the title of every document in
   it** and check the genre matches the manuscript. Volume of words proves nothing.
2. If the only available corpus is the wrong genre, discard the method rather than
   lowering the threshold. A frequency ratio computed across genres is noise.
3. Never conclude "this term is not used in Vietnamese scholarship" from a corpus you
   did not verify. Say what you could not verify.

## Four checks that do work

**A. Internal contradiction — the strongest evidence, needs no external source.**
Scan sentence pairs for near-duplicates (Jaccard on content-word sets ≥ 0.55) and scan
for *two different phrasings of one concept*. When the draft says `bộ chấm` in three
places and `công cụ chấm` in one, or uses `chỉ báo` for *indicator* in the literature
review but `chỉ số` for the same thing in the discussion, one of the two is the calque.
Internal inconsistency is checkable without any corpus.

**B. Back-translate against the manuscript's own other-language block.**
Bilingual submissions carry an abstract in both languages; the EN block is the draft's
own statement of what each concept is. Compare term by term:

- EN `automatic indicators` → VN had `chỉ số tự động`. In Vietnamese social science,
  **indicator = chỉ báo**, **index = chỉ số**. Wrong term, and the manuscript already
  used `chỉ báo` twice elsewhere.
- EN `saturated` → `bão hòa`. The finding was a ceiling effect, so `chạm trần` says it.
- EN `counterfactual` → `phản-thực`. Not a Vietnamese word; `phản thực tế` is.
- EN `inter-rater` → `liên-người`. Hyphenated calque; `giữa (những) người thẩm định`.

**C. Exclude pinned strings before choosing what to change.** Grep every candidate term
in the verification scripts. Terms may be pinned because a reviewer demanded them,
because a hedge must match across languages, or because they are a defined scale name.

- `trạng thái định danh` (nominal-scale states) is a measurement term — keep.
  `định danh văn bản quy phạm` (identify the governing document) is the calque — change.
  Same word, opposite verdicts, and only the context distinguishes them.
- A hedge-parity check pins `chưa được kiểm định thực nghiệm` ↔ `not been empirically
  validated`. Deleting the passive `được` to save one word in a word-limited abstract
  broke the check and failed the build. Find the word elsewhere.

**D. Sync any term that also appears inside a figure.** Figure labels are drawn by a
script, so renaming a term in the prose silently diverges the two. Grep the plotting
script for every changed term, edit the label, regenerate the image, and re-verify that
the embedded image hash matches the new file. Also check the new label is not longer
than the old — a longer string can overflow its box, which a vision check catches.

## Things that look like calques and are not

- **Quoted data values.** EN strings inside the prose may be the dataset's own labels
  being reported (`“understanding” (5 câu) và “understand” (4 câu)`). Check whether the
  text is quoting data before translating it.
- **Established loanwords.** `kappa`, `alpha của Krippendorff`, `conjunctive` (with a
  Vietnamese gloss immediately beside it), `logic`. Keep.
- **Markup.** `width=`, `figures/` are image syntax, not untranslated prose.
- **Structures that are normal in the target language.** Measured against a same-genre
  corpus, `được + V` passives, `các + N` plurals, `dựa trên`, and even `của` density
  were all at or below corpus rates. Nominal density was the only structural signal that
  exceeded the corpus (3.3×), and that is a compression target, not a calque.

## Terminology vs. register — separate the two verdicts

A phrase can be a correct technical term and still be awkward prose. `phán quyết`
(*verdict*, standard in arbitration law) appears 27 times as the framework's output
label. Attempts to confirm the legal usage hit three blocked sources (404, 403, JS-gated
page), so the term was **left unchanged and reported as unverified** rather than
replaced on memory. Do not swap a term you cannot source; flag it for the author.

## A superseded review file can declare verbatim constraints that no longer bind

Renaming a calque can break a "must stay verbatim" list written by an earlier review
round. Before honoring or overriding such a list, establish which round it belongs to:

1. Grep the **live verification scripts** for the string. A phrase pinned only in a
   markdown note is not enforced; a phrase pinned in a script fails the build.
2. Test whether the document's own proposals were ever applied. One audit proposed a
   replacement abstract containing a specific statistic; the current abstract did not
   contain it, so the document had been superseded by the next review round.
3. Separate the letter of a constraint from its intent. The real invariant was "do not
   delete a qualification to save words". After renaming `định danh văn bản quy phạm` →
   `nêu văn bản quy phạm` and `vị trí trích xuất` → `vị trí trích nguồn`, all four
   qualifications were still present under the new wording, verified by count. Renaming
   a calque is not deleting a hedge.

Write the verdict into the project folder where the next session will read it, or the
same conflict gets re-litigated and someone "restores" the calque.

## Verify the word count after every edit, not after the batch

Two edits labelled "cut redundant words" actually added 1 and 1 words because the
replacement phrasing was longer; the abstract crossed its 250-word cap and the audit
failed. The delta sign was misread at the time. Print the section's word count after
each pass and compare against the cap, and never describe an edit as a cut without
reading the numbers back.

## Do not "fix" one term into three variants

Replacing `cổng` (*gate*) produced `chốt kiểm`, `chốt kiểm soát`, and `chốt kiểm căn cứ`
in three places — still awkward, now also inconsistent. Pick one replacement, apply it
to every occurrence, then grep for the stem to confirm exactly one variant survives.
