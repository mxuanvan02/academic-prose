# Peer Review Report Genre

A reviewer report is a **form**, not an essay. Each numbered field answers its own
question and is read separately, often by different people. Prose habits that serve
a manuscript actively damage this genre: a field answered in flowing paragraphs
buries the verdict, and content repeated across fields reads as padding to an
editor who sees both.

This file governs the reviewer-side artifact. Author-side response letters are
governed by [Revision response genres](revision-response-genres.md); the arithmetic
discipline behind any recomputed disagreement is governed by
[Reviewer recomputation gate](reviewer-recomputation-gate.md).

## 1. Field brevity contract

A closed question gets a verdict in the **first word**, then one clause of reason.
Nothing else. Target 25–35 words for a yes/no-with-reason field in English; a
Vietnamese rendering of the same field runs longer and should stay under roughly
50. The long-form field (comments to the author) is where the argument lives.

```text
BAD   Partly. The engineering contribution is real but narrow: a curated dataset
      with labels and per-item references is released, and a two-stage classifier
      is benchmarked against five baselines under matched conditions. The novelty
      claim is overstated, and the central quantitative claim is not statistically
      supported at the reported sample size, so the contribution as currently
      framed does not yet advance the field beyond the existing literature.
GOOD  Partly. The released labelled dataset is a genuine asset, but the novelty
      claim is overstated and the headline gain is not statistically supported.
```

The long version says nothing the short one does not. Everything cut was either
restated later in the detailed comments or was scaffolding around the verdict.

Do not open a field with a preamble, a restatement of the question, or a summary of
what the paper attempted. The reader has the paper.

## 2. Fields must not overlap

The default failure is writing the technical findings twice: once for the editor
and once for the author. Give each field **disjoint** content.

| Field | Owns | Must not contain |
| --- | --- | --- |
| Comments to the author | every technical finding, each with its evidence | recommendation rationale, prior-round politics |
| Confidential comments to the editor | why this recommendation and not the adjacent one; defects in the *prior round's instructions*; judgment calls that are the editor's to make (self-citation necessity, scope, ethics) | the findings, restated |

Three consequences:

- The editor field is short. When it starts recapitulating statistics, the content
  belongs in the author field and the editor field has no argument of its own.
- **Name the decision boundary explicitly.** An editor needs to know why
  reject-with-resubmission rather than minor-revision, and the answer is usually a
  single decisive but *tractable* gap. Say that it is tractable; that is what
  distinguishes resubmission from rejection.
- **Correct the prior round when it was wrong.** A previous reviewer's instruction
  can contain a broken identifier, a misattributed criterion, or a demand the
  authors could not satisfy as written. Verify before treating non-compliance as
  a defect, and record the correction in the editor field so the authors are not
  penalised for obeying a faulty instruction. This is the one thing only a
  later reviewer can supply.

## 3. Finding structure inside the long field

One paragraph per finding, ordered by decisiveness, not by page order.

Each paragraph: **claim first, number second.** "The headline gain is three
samples" then the arithmetic. Never the reverse — a paragraph that opens with a
calculation forces the reader to hold numbers before knowing what they are for.

Close each finding with what would resolve it. A finding the authors cannot act on
is an accusation.

## 4. Compression must not cost evidence

When shortening, statistics survive and adjectives do not. After every compression
pass, verify that each of these is still present at least once: the test statistic
and its value, every interval, every count with its denominator, every identifier
(DOI, table number, section number), and every hedge that bounds a claim.

Removing a hedge to save words changes what the report asserts. Removing a
denominator makes a count unusable. Neither is a length saving.

**Recount after every pass, in text space.** Rewriting to sharpen a verdict
reliably *adds* words even when the intent is to cut, so a pass can move the count
in the wrong direction; measure rather than assume. Compare against the previous
measured count, not against an estimate.

## 5. Bilingual reports

When the report is delivered in two languages, both versions carry the same
verdicts, the same numbers, the same hedges, and the same recommendation string.
A finding present in one and absent in the other is a `CONS` failure.

Number separators follow each language's own convention — decimal comma in
Vietnamese, decimal point in English — while DOIs, identifiers, and version
strings stay byte-identical in both. Check that no DOI fragment was "corrected"
into the target language's separator.

## 6. Suggested references

Suggesting references as a reviewer is ethically constrained by most venues, so
the field carries its own contract:

1. Suggest only **primary sources for methods or criteria the manuscript already
   relies on**. A method used substantively but cited through an unrelated
   application paper is the legitimate case; a topic the paper does not address is
   not.
2. State explicitly that none of the suggestions is the reviewer's own work.
3. Verify every identifier against a registry before submitting, and give full
   bibliographic information even when the rest of the report is being compressed.
   This field is the one place where length is mandated by the form.
4. Say in one sentence per item **why** it is the right primary source, so the
   suggestion cannot read as citation pushing.

For the removal question, prefer "replace or reconsider" over "delete" unless a
reference is genuinely off-topic, and separate two distinct grounds: a method cited
through an unrelated domain, and self-citations supporting only generic claims.
Naming which references are on topic and should stay is part of a fair answer.

## 7. Pitfalls

- **Answering a closed question with an essay.** The form asks four short
  questions and one long one. Treating all five as long is the most common
  structural defect and the one users notice first.
- **Restating the paper.** A reviewer report contains no summary of the
  manuscript unless the form asks for one.
- **Hedging the verdict.** "Partly" is a verdict; "the paper has both strengths
  and weaknesses that must be weighed" is not.
- **Letting the editor field grow into a second review.** If it exceeds roughly a
  third of the author field, it has absorbed content that belongs elsewhere.
- **Reporting figures the reviewer could not inspect.** Where figures are raster
  images and only captions are legible, say so and scope every figure comment to
  caption and body text. Silence here reads as a claim to have inspected them.
- **Grading a revision without reading the response letter.** Several findings are
  only visible as the gap between what the letter claims was changed and what the
  manuscript now contains.
