# Author-side peer-review revision for computational papers

Playbook for revising a manuscript in response to received peer-review reports
when the paper ships a public code/data artifact. Core rule: **every answer to
a reviewer must be grounded in re-executed evidence, never in recall of what
the numbers "probably" were.** This is the author side; for refereeing someone
else's paper use the peer-review/refereeing skills instead.

## 0. Match the review to the manuscript first

Before planning anything, verify submission ID and title inside the review
against the manuscript being revised. Machines that host several paper projects
accumulate review files for *other* submissions, and a cached review whose
filename pattern matches the task looks authoritative even when it belongs to a
different paper. A mismatched review
produces a confidently wrong revision plan. If no review file for the target
paper exists anywhere, ask the author for it — do not substitute an older
internal feedback report without explicit confirmation.

## 1. Reproduce before responding

1. Clone the **public artifact repo** referenced in the manuscript's Data/Code
   statement (not whatever local experiment clone is handy — local branch
   clones may be stale variants whose constants do not match the submitted
   numbers; verify constants like safety band, seeds, window length, n/cell
   against the manuscript text before trusting a pipeline).
2. Run the pipeline (`reproduce.sh` or the individual experiment scripts).
3. Byte-diff every regenerated `.tex` table against the submitted ones.
   - Identical → your evidence base is confirmed; you can quote numbers and
     CIs freely.
   - Caption-only diffs → keep the submitted caption (it was usually improved
     deliberately); keep regenerated numbers.
   - Number diffs → STOP; resolve which pipeline produced the submission
     before writing a single response word.
4. Regenerate figures from the fresh CSVs so figure/table/manuscript cannot
   drift apart.

## 2. Read the code behind each reviewer claim

Reviewers routinely collapse two same-named components that live in different
code paths. A measured instance: an ablation table removed a named term from
the *scoring* function only, while the namesake mechanism in the *budget* rule
was never varied. The reviewer read "the term does not help" as covering both.
The same shape recurs whenever one named quantity enters a system at two places. Grep the exact functions the reviewer's claim
touches, and establish what was and was not actually varied, before conceding
or rebutting.

## 3. Answer "why keep component X?" with a fresh targeted ablation

When a reviewer shows your component is neutral or counterproductive on the
reported metrics:

1. Write a minimal script reusing the published primitives (import or
   copy the exact functions; stdlib-only, deterministic, same seeds/windows
   as the submitted runs) that toggles exactly the constant under question.
2. Report mean ± 95% CI for every metric, and check the reviewer-quoted delta
   against CI overlap (e.g. Δobj = 0.0017 vs half-widths ±0.0024/±0.0021 →
   within noise; the honest statement is "neutral knob", not a defense).
3. If the component is neutral in the evaluated regime but plausibly matters
   in a harsher one, offer the author two options with measured fallback:
   **(A)** reframe honestly — demote the component to a conservative design
   knob, report the new ablation, state the neutrality as a limitation;
   **(B)** run the harsher regime (e.g. an `extreme_burst` channel already
   parameterized in the codebase) and report both regimes truthfully, falling
   back to (A) if the mechanism still shows no effect. Never fabricate a
   defense and never hide the unfavorable measurement; a headline claim that
   the evidence weakens must be re-scoped, and the author decides how.

## 4. Non-monotonic trends: report the whole sequence

When a reviewer extrapolates a trend ("safety gap widens with N — will it
worsen beyond N=20?"), pull the per-point values with CIs. Real data often
shows a non-monotonic sequence (measured missed-event gap: +1.29 pp at N=3,
−0.04 at N=8, 0.00 at N=12, +1.86 at N=20, with overlapping CIs at N=20).
State the sequence, the CI overlap, and explicitly mark beyond-range behavior
as unknown → limitation, not reassurance.

## 5. Figure label-overlap check without vision

When a reviewer reports overlapping symbols/annotations and the vision tool is
unavailable, detect collisions programmatically: open the figure PDF with
PyMuPDF, extract text spans with bboxes (`page.get_text("dict")`), sort by
(y, x), and test pairwise intersection. This caught four data labels colliding
in a tight low-bandwidth cluster — including two policies at *identical*
coordinates, which no amount of dx/dy nudging can fix (needs leader lines or
offset stacking) — plus an annotation ("low-bandwidth region") overlapping an
unrelated label. After fixing the plot script, re-run the bbox check and
require zero intersections before delivery.

## 6. Page budget and author-approval discipline

- Build a review-point → evidence-type table first (text-only verified /
  needs new experiment / figure fix), with the measured evidence attached to
  each row, and let the author approve the plan **before** editing.
- If the manuscript sits at the venue's hard page cap, every addition must be
  offset by tightening elsewhere; if it still overflows, ask the author —
  never silently cut content to fit (overflow → appendix or author decision).
- Keep new reviewer-facing text inside the manuscript's existing markup
  convention when one exists (e.g. `\rev{}`/`revblock` environments that
  render highlighted in the review copy and neutral in the clean copy).

## 7. Response-letter hygiene

Each response: quote the reviewer point → state what was measured or changed
→ cite the exact table/figure/line where the change lives. Distinguish
verified-from-code statements from inferred ones. If an answer is "we could
not measure this", say so and route it to limitations/future work.

Length register: match the reviewers' own brevity. See *The response letter* in
`revision-response-genres.md`.

Glyph pitfall when building the letter with `pandoc` + `xelatex` and Latin
Modern: Greek and math glyphs (ρ, δ, ≈, ≥, −, →) are **silently dropped** — the
build still exits 0 and prints only a `Missing character` warning. ASCII-fy the
Markdown before building, then grep the build log for `Missing character`.

## 8. Keep reviewer identities out of the public artifact

A reproducibility repository is publication-facing. Reviewer identities, reviewer
question numbers, and revision-round framing are prohibited internal register
there exactly as in the manuscript: the Internal Register gate covers the
repository, not only prose.

The leak channels are wider than prose, and each needs its own sweep:

- commit messages, which also expose author name and email through the platform's
  `.patch` endpoint;
- file and output names tagged with reviewer question numbers, which map a public
  path onto a confidential comment;
- repository documentation whose structure reveals which artifact answers which
  reviewer -- a "revision-round experiments" section, or reproduction steps keyed
  one-to-one onto reviewer questions;
- script docstrings and inline comments recording what a reviewer objected to, or
  which regime was the one under review.

Write the repository as though no review had occurred: descriptive names, and
documentation covering contributions, method, application, and a one-command
entry point. The reviewer-to-change mapping belongs only in the letter to the
editor.

**Rewriting history does not remove the material.** Hosting platforms keep
serving objects that no reference reaches, and several of those routes are
anonymous and enumerable:

- a commit page, and its `.patch`/`.diff` form, resolve from the SHA alone;
- the public events feed lists every push with its before/head SHAs, so the whole
  orphaned chain is recoverable with no prior knowledge;
- code search and the commit-list UI expose only reachable commits.

That asymmetry is the trap. A fresh clone grepped across every reachable ref
reports zero matches and gives false assurance, because the exposure lives in
objects the clone never fetches. Verify a sanitization three ways before calling
it clean: reachable history in a fresh clone, each orphaned SHA fetched by URL,
and the public events feed. Only deleting the repository -- which lets the
platform garbage-collect the orphaned objects -- or making it private actually
removes the content. Both need author consent, and the full history is backed up
first (`git bundle create --all`). Never report "history rewritten, therefore
clean", and never characterize residual exposure as low-risk without measuring it.

## 9. Recurring revision-round failures documented elsewhere

Two failure modes keep appearing during a revision round. Their general form
lives in another reference, so consult it rather than re-deriving a local rule:

- **A softened or re-scoped claim survives in another artifact** -- a table
  caption, a conclusion, or text emitted by a generator script. See *Revise all
  propagation sites* in `peer-review-to-manuscript-revision.md`, which now covers
  generated artifacts and the search-by-variant rule.
- **A verification probe reports the wrong verdict** -- hyphenation splitting a
  phrase, asymmetric case folding, probing a composite file instead of the one
  that holds the target, an exit code swallowed by a pipe, or a scan run over
  under-extracted input; and **a delivery bundle packed before the last edit**.
  See the recipes in `latex-pre-submission-verification.md`.
