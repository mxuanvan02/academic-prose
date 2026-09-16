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

## 10. Acceptance gate

Before delivery, verify:

- every major reviewer comment maps to a revision, bounded non-revision, or explicit author/new-study dependency;
- no new result, citation, release status, rights claim, or validation outcome was invented;
- every derived count reconciles arithmetically;
- external metadata matches the intended source, not merely a resolving identifier;
- bilingual claims, numbers, and hedges agree;
- internal-register and process-logic scans have been adjudicated;
- tracked and clean artifacts contain the same accepted content;
- document structure and rendered layout pass the companion document skill’s checks.
