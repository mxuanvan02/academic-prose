# Revision Response Genres

The documents that surround a Q1 submission — the response to reviewers, the
cover letter, the novelty and contribution statement, the declarations block —
are the ones most often drafted last, fastest, and worst. They are also the ones
an editor reads first. A manuscript that survives peer review on merit can still
be rejected because its response letter conceded a claim the paper does not
concede, promised an analysis nobody ran, or answered a reviewer's question in
the register of a project status meeting.

This file owns those genres. It does not own whether a reviewer is right: that is
a scientific judgment made against evidence, not a rhetorical one.

## Why these genres need their own contract

Manuscript prose is addressed to a future reader who has only the published
artifact. A response letter is addressed to **three named readers with different
powers**: an editor who decides, reviewers who advise, and a future reader who
may never see the letter at all. The rhetorical situation is therefore inverted —
the drafting conversation is not a leak here, it is the subject.

That inversion is why the `internal_artifact_reference` prohibition relaxes in a
response letter and nowhere else. Naming a line number, a revised table, or a
version of the manuscript is not a register leak in a document whose whole job is
to locate changes. What does not relax is claim integrity: a response letter may
not assert a result the manuscript does not contain.

Consequence in the other direction, and this is the failure that actually kills
papers: **material introduced in a response letter must exist in the revised
manuscript**. A letter that argues a point the manuscript never makes leaves the
reviewer holding a private communication as evidence. Code `response_only_claim`.

## The response letter

### Structure

One block per reviewer comment, in the reviewers' own order, each block carrying
four parts and no more:

1. **The comment**, quoted verbatim, unabridged. Paraphrasing a criticism to make
   it easier to answer is `comment_softening` — an editor holding the original
   sees the edit immediately.
2. **The verdict**, stated before the explanation: accepted, accepted in part,
   or respectfully declined. An editor scanning thirty blocks needs the verdict
   in the first clause.
3. **What changed**, with a locator into the revised manuscript (section, table,
   figure, or line range) and the changed text quoted where it is short enough.
4. **Why**, only where the verdict needs a justification — a decline always does;
   a straightforward acceptance usually does not.

Do not open a block with gratitude. One thanks at the top of the letter is
courtesy; thirty are padding, and `symmetric_padding` applies here exactly as it
does in prose.

### The three verdicts

**Accept.** Make the change, then say precisely what it was. "We have revised the
Methods accordingly" is not a response; it forces the reviewer to hunt. Name the
subsection and quote the sentence that now stands.

**Accept in part.** The most common honest verdict and the most often mishandled.
State which part you accepted, which you did not, and why the boundary falls
there. Blurring the boundary to sound cooperative produces a letter that appears
to concede everything while the manuscript concedes nothing — the reviewer finds
the mismatch and reads it as evasion.

**Decline.** Legitimate and sometimes obligatory. A reviewer can be wrong, can
have read a different version, can be applying a criterion from another
subfield, or can be asking for an analysis the design cannot support. Decline on
evidence: name the reason, cite the specific text or result that settles it, and
offer the alternative you did provide. Never decline on convenience, never on
scope alone without saying why the scope is principled.

The failure mode with a name is `deference_capitulation`: agreeing with a
reviewer because a reviewer said it, then weakening a correct claim in the
manuscript to match. This is the same defect the adversarial-review discipline
guards against elsewhere in this skill — authority is not evidence. If the
reviewer is right, the correction is scientific and belongs in the paper. If the
reviewer is wrong, saying so with evidence is the scholarly act.

### Requests you cannot satisfy

Three cases, three honest answers, none of which is silence:

- **Out of scope for this design.** Say what the design can establish and what it
  cannot, and place the request in future work as a question with a feasible
  design — not as a task. A reviewer asking for a randomized trial of an
  observational finding is asking for a different paper; say that.
- **Infeasible with available data or resources.** State the specific barrier.
  "We were unable to" without a barrier reads as unwillingness.
- **Would require an analysis whose result you cannot predict.** Run it or decline
  it. Never promise it in the letter for a future revision — see below.

**A promise is a claim.** Writing that an analysis "will be included" commits you
to a result you have not seen, in a document the editor will hold you to. Code
`promissory_result`. Run the analysis and report it, or decline the request and
say why.

### Conflicting reviewers

When two reviewers demand opposite changes, do not satisfy both and do not pick
silently. Name the conflict, state which position the evidence supports, make
that change, and address the other reviewer's underlying concern by a different
route if one exists. The editor adjudicates conflicts and cannot do so from a
letter that pretends there was none.

## Cover letter, novelty statement, and declarations

These accompany a submission or a revision but are governed separately, because
they are factual assertions about the work and its authors rather than arguments
about reviewer comments. See
[Submission integrity declarations](submission-integrity-declarations.md) for the
cover letter, the novelty and contribution statement, authorship, ethics,
funding, conflicts, availability, preregistration, and generative-AI disclosure.

One consequence belongs here rather than there: a revision letter that argues a
contribution the revised manuscript does not state, or that restates one
contribution as three to look responsive, fails on the same codes the submission
gate enforces. Check the letter against the manuscript, not against the previous
letter.
## Audit procedure

Run on every response letter, cover letter, or declarations block before delivery:

1. **Coverage.** Every numbered reviewer comment has exactly one block. Missing
   comments and merged comments are both findings.
2. **Verbatim check.** Each quoted comment matches the reviewer's text character
   for character.
3. **Verdict present.** Every block states accept, accept in part, or decline in
   its first clause.
4. **Locator resolves.** Every claimed change points to a section, table, figure,
   or line range that exists in the revised manuscript.
5. **Bidirectional consistency.** Every change the letter claims is in the
   manuscript, and every substantive argument the letter makes appears in the
   manuscript. Both directions fail: `response_only_claim` catches the second.
6. **No promises.** No future-tense commitment to an unrun analysis or an
   unwritten section.
7. **No capitulation.** For every accepted comment that weakens a claim, confirm
   that evidence — not deference — drove the change.
8. **Declarations sourced.** Every declaration traceable to author-supplied fact
   or an explicit visible placeholder.
9. **Bilingual parity.** Where both language versions exist, verdicts, scope, and
   hedging match across them.

## Blocking failures introduced here

- `response_only_claim` — the letter argues something the revised manuscript does
  not contain.
- `promissory_result` — a result or analysis promised rather than reported.
- `deference_capitulation` — a correct claim weakened to agree with a reviewer,
  without evidence.
- `comment_softening` — a reviewer's criticism paraphrased, abridged, or
  reordered in a way that changes what was asked.
- `fabricated_declaration` — authorship, ethics, funding, conflict, registration,
  or availability content invented or inferred.

## Verification status of this file

These are genre contracts and audit procedures, derived from the failure taxonomy
this repository already enforces. They are not claims about any particular
journal's current submission requirements. Retrieve those from the journal, per
the journal-template authenticity gate in `SKILL.md`; a limit or policy that
appears only in a derived notes file is `fabricated_constraint` until re-derived
from the publisher's own text.
