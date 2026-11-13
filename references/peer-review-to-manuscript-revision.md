# Peer review to evidence-bound manuscript revision

Use this workflow when the user supplies both a manuscript and reviewer comments and asks for a revised manuscript, rather than a response memo alone.

## 1. Build a comment-to-evidence matrix

For every reviewer request, record:

| Field | Meaning |
|---|---|
| `comment` | Atomic reviewer request; split compound comments |
| `location` | Manuscript sections, tables, captions, declarations, or repository artifacts affected |
| `evidence_status` | `available`, `derivable`, `externally_verifiable`, `requires_new_study`, or `author_only` |
| `action` | Revise, add, relabel, qualify, relocate, or leave unresolved |
| `verification` | Arithmetic, source metadata, repository state, experiment output, expert annotation, rights confirmation, etc. |
| `manuscript_result` | Exact bounded claim the manuscript may make after revision |

Do not start polished rewriting until every major comment has an evidence status.

## 2. Route requests by evidence status

- **`available`**: revise directly from supplied data or text.
- **`derivable`**: compute only closed quantities whose inputs are all available; state the denominator and derivation where readers need it.
- **`externally_verifiable`**: verify identifiers, citations, repository state, access, tags/releases, and licenses against authoritative sources. Treat the result as a dated observation if it can change.
- **`requires_new_study`**: do not invent expert validation, confidence intervals, ablations, cluster bootstrap, predictions, or adjudication results. State the affected inferential limit in Limitations and, if useful, give a testable design in Future Work.
- **`author_only`**: funding, rights, ethics, authorship, controlled-access terms, and institutional permission require an author-supplied statement or visible placeholder.

A reviewer request is not evidence that the requested result exists.

## 3. Keep workflow status out of publication prose

Do not paste the revision backlog into the manuscript. Phrases such as “must be completed before submission,” “the current files do not contain,” “the reviewer could not verify,” or “this item remains to be done” belong in a response matrix or collaborator note unless the genre explicitly licenses them.

Recast them into scientific register:

- “Bootstrap by document must be completed before submission” → “Item-level uncertainty does not account for dependence among questions from the same document; document-cluster uncertainty remains unquantified.”
- “The public artifact did not expose predictions” → “Item-level paired predictions are not included in the released artifact, so the reported paired test cannot be independently reconstructed from that artifact.”
- “Expert review has not been completed” → “Legal correctness and cognitive-label validity have not been established against an independent human reference standard.”

Future Work should state question → why current evidence cannot settle it → feasible design, not a task list.

## 4. Preserve the contribution while tightening claims

Use the claim ladder:

1. **Observed**: counts, rates, comparisons, and output distributions.
2. **Method-defined**: what the pipeline or automatic gate checks.
3. **Interpretation**: only what the design licenses.
4. **Validation/transfer**: label as unresolved unless independently tested.

Do not let repeated caveats bury the contribution. Put one strong validity boundary at each point where a reader could otherwise overinterpret the result, then avoid duplicating it in every paragraph.

Relabel experimental conditions precisely. If the correct source passage is supplied rather than retrieved, call it `oracle context` or `gold context`; do not imply retrieval performance.

## 5. Complete data-flow accounting without guessing

For pipeline papers, reconcile all stages as sets, not only as a linear funnel:

- requested outputs;
- generated candidates;
- automatic-filter survivors;
- release branch;
- evaluation branch;
- intersection and branch-only records;
- records in neither branch.

Use set arithmetic only when the required counts are closed. If causes of a shortfall are unavailable, report the count as unexplained and name the missing stratification; never assign likely causes as measured causes.

## 6. Treat availability and reproducibility as separate claims

Check independently:

- URL resolves without privileged credentials;
- artifact is public or controlled-access as stated;
- tagged/versioned release exists;
- exact commit or immutable identifier is named;
- prompts, parser rules, seeds, checkpoint revisions, lockfile/container, checksums, split manifest, and aggregate/result files align with the paper;
- licenses and redistribution rights are declared by component.

A reachable repository is not a frozen reproducible release. A reachable dataset is not proof of redistribution rights. A transient HTTP result should be reported as a dated verification observation, preferably in the response record; include it in the manuscript only when the availability statement genuinely needs a current-status disclosure.

## 7. Revise all propagation sites

After a substantive claim change, sweep:

- title and both abstracts;
- introduction and contribution list;
- methods and condition labels;
- results, tables, footnotes, and captions;
- limitations, ethics/intended use, and future work;
- conclusion;
- data/code availability;
- both language versions.

The same claim must not appear as automatic in Methods, validated in the Abstract, and benchmark-grade in the Conclusion.

Two additions that recur on computational papers:

- **Generated artifacts.** Caption and table text emitted by a script is
  regenerated on every pipeline run, so patching only the emitted `.tex` is
  silently reverted. Patch the generator, re-emit, and diff the regenerated file
  against the copy in the manuscript tree.
- **Search by claim variant, not by the phrase already fixed.** The copy just
  edited is the worst place to search from; the duplicates that survive use a
  different wording of the same claim. Enumerate the variants and sweep each,
  then confirm the change in the rendered PDF, which is what a referee reads.

## 8. Deliver separate artifacts

When appropriate, provide:

1. a clean revised manuscript;
2. a tracked/redlined manuscript;
3. a concise unresolved-action matrix for requests requiring new studies or author confirmation.

The clean manuscript must read as a publication, not as a response letter. The unresolved-action matrix is where submission tasks, owners, evidence needed, and reviewer mapping belong.

## 9. Handle second-round review as a convergence pass

When a reviewer returns after an earlier revision, do not restart from the original manuscript or treat every repeated request as a prose problem.

1. Use the latest accepted clean manuscript as the new source of truth. Produce the new clean and tracked versions against that artifact so the redline shows only the current round.
2. Reclassify each comment as `resolved`, `partial`, `unresolved_requires_evidence`, or `new_editorial_issue`. Repeated requests for expert validation, paired predictions, clustered uncertainty, duplicate audits, frozen releases, or rights confirmation remain evidence dependencies; another disclaimer does not resolve them.

   But run the artifact search in the parent skill's *"Before accepting that a request needs a new study"* section before confirming `unresolved_requires_evidence` on any of them, because this list is a list of *dependencies*, not a list of things that are necessarily missing. They split cleanly by who can produce them:

   - **Computable from existing artifacts if the run outputs survive:** per-run valid/N-A/empty counts and the accuracy denominator; 2×2 transition tables, McNemar variants, and clustered or permutation-free uncertainty; exact and near-duplicate audits across splits; split-disjointness; provision-anchor overlap as a stated upper bound. Each needs per-item predictions or the released dataset, nothing more. Measured: all three of these closed in a single round from files already on disk.
   - **Genuinely blocked without new work:** expert legal validation, inter-rater agreement, option-order permutation (needs new inference runs), cause-level stratification of pipeline shortfalls (needs a re-run with request-level logging), and the frozen public release plus rights declarations (author and institution only).

   Carrying a computable item as unresolved for a second round is the costlier error of the two: it reads to the editor as a study that cannot answer basic questions about its own experiment, when the answer was one script away.

3. When a closure lands, treat it as a claim change and sweep every propagation site including the other language version. An abstract sentence that correctly said a quantity was unreported becomes a false statement about the paper's own body the moment the quantity appears, and the version you did not hand-edit is where it survives.
3. Give priority to editorial issues that the new review exposes, especially reviewer-response language leaking into the manuscript. Replace submission instructions, dated access-test narratives, and phrases about what “the reviewed artifacts contain” with a compact statement of the affected inference. Keep operational status in the unresolved-action matrix.
4. Use implementation evidence narrowly. A dependency constraint such as `package>=1.0.0` does not identify the runtime version. Parser code can establish the accepted label set and fallback value, but cannot establish the observed count of parseable outputs unless run reports or item-level outputs are available. Likewise, `non-empty output` is not equivalent to `parsed as A–D`.
5. If source code clarifies a method, report the method semantics rather than narrating the code inspection. Name exact commits only when they are stable evidence relevant to reproducibility; do not turn repository forensics into manuscript prose.
6. Compress future work after the first round. Preserve the open question, inferential consequence, and feasible design, but remove a reviewer-style checklist that competes with the contribution narrative.

For tracked DOCX delivery, verify the **accepted view**, not raw XML string presence alone: superseded reviewer-language correctly remains inside `w:del`. Check the clean artifact for forbidden prose and inspect insertions/deletions separately in the tracked artifact. Then hand off to the document skill for schema validation and rendered-page inspection; forced `pageBreakBefore` and caption `keepNext` properties should be judged from the PDF, not inferred from paragraph counts.

## 10. When the author wants convergence before submission, not a single review

Some authors have no reviewer comments yet and do not want a draft — they want the
manuscript brought to a state that survives review, delivered only once it does. Run
independent rounds rather than one review pass.

**Round composition.** Split by criterion, one reviewer each, because a reviewer holding
two criteria spends its effort on the first: (1) domain theory and argument, (2) factual
and citation verification against primary sources, (3) format and compliance measured by
command rather than estimated. A fourth for language quality repays itself on Vietnamese
prose, where register decay is invisible to the other three.

**Independence.** Each round is a reviewer scoped to "audit the current artifact against
these criteria", with no memory of prior verdicts. A reviewer asked to confirm its own
earlier finding rationalises the fix instead of re-deriving it. The previous round's
findings go in as a checklist to **verify**, never as context to agree with — and every
round also asks what broke while fixing.

**What counts as fixed.** A criterion passes only when the reviewer re-derives the
judgment from the current artifact. "The author says it was fixed" is not evidence, and
neither is a pass from the reviewer that raised it.

**A reviewer finding is a candidate, not a verdict.** Independent reviewers produce
false positives at a steady rate, and applying one costs more than the defect it
imagined — it edits a passage that was correct, and the next round cannot tell the
difference. Verify every finding against the artifact before editing. Three shapes recur:

- *"This reference is never cited."* Search the bare surname, not the citation string.
  A Vietnamese APA manuscript inverts the name (`Nguyễn, T.` in the list, `Nguyễn (2024)`
  in text) and may use `và nnk.` where the reviewer greps for `et al.`; a reviewer that
  searches its own English phrasing reports a miss that is not there. Confirm the hit in
  the rendered file, then discard the finding.
- *"This number contradicts the source."* Check the version the manuscript actually
  cites. A preprint and its journal version routinely report different sample sizes and
different summary statistics for the same study, and a reviewer holding the other
  version will confidently report the correct figure as wrong. Fix only when the cited
  version disagrees with the manuscript.
- *"This claim is asserted too strongly."* Apply it to the sentence, not to the whole
  thesis. Reviewers escalate from one unhedged sentence to a demand that the central
  claim be demoted to a hypothesis; the second is a different paper.

Record which findings you rejected and why, in the round summary. An author who sees four
findings and a silent no-op in the manuscript needs to know the review was weighed, not
skipped.

**A fix that adds words can break a structural cap.** When the ceiling is measured in
rendered pages and the floor in words, the two constraints pull against each other: the
manuscript sits at the page limit, the reviewer demands the omitted step be restored, and
the restore pushes the document one page over. Neither constraint is negotiable and the
reviewer will not weigh them. Measure the rendered page count after every expansion pass,
not only at delivery, and hold the word count inside both bounds by cutting what the
restore made redundant rather than by rejecting the finding. Read the page count from the
converter's own report (`pdfinfo | awk '/Pages:/{print $2}'`) — a looser pattern that
matches any trailing number will read a figure out of an unrelated line and hide the
overflow.

**Never let the loop manufacture agreement.** If two consecutive rounds return the same
class of objection, the brief or the architecture is wrong, not the prose. Fix the brief,
and say that you did.

**Reporting.** Do not present a round that still reports defects as finished unless the
author asked to see work in progress. Give the round number, what changed, and what
remains open — a reviewer that caught nothing and a reviewer that caught four things must
not read the same in the summary.

## 11. Acceptance gate

Before delivery, verify:

- every major reviewer comment maps to a revision, bounded non-revision, or explicit author/new-study dependency;
- no new result, citation, release status, rights claim, or validation outcome was invented;
- every derived count reconciles arithmetically;
- external metadata matches the intended source, not merely a resolving identifier;
- bilingual claims, numbers, and hedges agree;
- internal-register and process-logic scans have been adjudicated;
- tracked and clean artifacts contain the same accepted content;
- document structure and rendered layout pass the companion document skill’s checks.
