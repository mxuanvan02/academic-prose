# Academic Writing Failure Taxonomy

Use these labels when auditing text composed from notes, evidence, or an
outline. Translation-specific errors remain in the English-to-Vietnamese
transfer taxonomy.

| Code | Failure | Required response |
| --- | --- | --- |
| `invented_sample_size` | a sample size absent from the input is supplied | remove and mark the missing input |
| `causal_overclaim` | non-causal evidence is written as a causal conclusion | restore the observed relation and qualify it |
| `causal_claim` | a causal claim appears without causal evidence | block or rewrite as association/interpretation |
| `unsupported_novelty` | novelty or priority is asserted without a defined comparison basis | mark `needs_source` or delimit the contribution |
| `author_catalogue` | literature is listed source by source without synthesis | reorganize around a common analytic dimension |
| `source_by_source_summary` | summaries replace comparison and argument | synthesize convergence, tension, and evidence limits |
| `population_generalization` | a bounded result is generalized beyond its sample or conditions | restore scope and consequence |
| `invented_citation` | a citation or bibliographic fact is fabricated | remove it and mark `needs_source` |
| `evidence_dump` | evidence is presented without the claim or warrant it supports | connect or remove it |
| `topic_outline` | headings name topics but encode no argumentative progression | rebuild from section purpose and claim hierarchy |
| `ceremonial_limitation` | a weakness is named without its inferential consequence | state what conclusion is affected and how |
| `promotional_contribution` | contribution language exceeds the supplied comparison and evidence | delimit the baseline, addition, and scope |
| `empty_transition` | a connective creates apparent flow without a logical relation | use conceptual continuity or remove it |
| `claim_without_warrant` | evidence and conclusion are adjacent but their inferential link is absent | supply a licensed warrant or weaken the claim |
| `operational_log_prose` | internal build, audit, or QA bookkeeping is written as manuscript content: intermediate candidate tallies, file/column states, checklist confirmations, artifact names, reconciliation notes | keep the finding the check licenses; move the bookkeeping to an appendix, data statement, or repository record |
| `progress_state_limitation` | a limitation reports the current state of the project's work rather than a bound on inference: unfilled fields, unfinished steps, artifacts not yet produced | restate as the validity, reliability, generalizability, or measurement limit that the missing work leaves open |
| `todo_future_work` | future work lists tasks the team owes rather than open research questions | restate each item as a question, the design that would answer it, and what it would license |
| `results_digest_abstract` | the abstract enumerates counts and closes on caveats, so the aim and contributions are never stated | rebuild as gap → aim → contributions with mechanisms → principal finding → one boundary sentence |
| `unanswerable_rq` | a research question yields no contribution, typically by asking what limitations must be declared | recast as an empirical question whose answer is the contribution, or delete it and renumber |
| `activity_as_contribution` | a contribution names work performed rather than the mechanism that makes it novel or usable | add the mechanism: what the step enables that its absence would not |
| `fabricated_constraint` | a numeric limit is enforced from the author's own derived notes rather than the authoritative source, and content is cut to satisfy it | re-derive the limit from the template or a measured published article; restore any content removed for it |
| `self_reminder_prose` | the draft instructs itself instead of stating the result: a modal of obligation aimed at the text (`cần nêu rõ`, `cần nêu thẳng`, `cần được diễn giải thận trọng`, `được nêu dưới đây`, *it should be noted that*) | delete the instruction and keep its result as a direct assertion; the scope it carried must survive |
| `defensive_disclaimer_stack` | three or more adjacent sentences deny strong claims (`chỉ …`, `không phải là …`, `không chứng minh …`, `không bảo đảm …`) until the finding disappears under its own disclaimers | collapse to one boundary sentence stating the bounded claim, not denying the unmade one |
| `config_dump_prose` | parameters are copied from a config file or CLI call and keep their identifier form in prose (`seed`, `backend`, `qa_id`, bare `vLLM`, `top-$p$`, `512 token`) | keep every value; name the role before the identifier and group parameters by pipeline stage |
| `generated_artifact_drift` | an element persists in the rendered artifact after removal from source (exporter hardcode), or hand edits to a delivered artifact are lost on regeneration | grep the exporter before re-editing source; diff the user's returned artifact against your last build and back-port every change, including structural moves |
| `untranslated_generic_technicalism` | a source-language term is retained in target-language prose because it is familiar to the author's working environment, not because it names a unique external object | apply the designator and established-rendering tests; translate and lock one rendering |
| `overtranslation_of_designator` | a rigid designator is translated: model, product, library, standard number, statute short title, gene/taxon symbol, eponym, dataset name, unit, or identifier | restore the exact string; put the Vietnamese category noun in front of it instead |
| `distinction_collapse_by_translation` | two source concepts the argument separates receive one target rendering (validity/reliability, efficacy/effectiveness, hazard/risk, verification/validation) | restore two lexically distinct renderings and gloss each at first use |
| `invented_vietnamese_term` | a rendering inferred by the writer is presented as the field's established term | demote to a source term plus descriptive gloss and mark `needs_review`, or cite the authority |
| `mixed_rendering` | the same concept alternates between its source form and its translation, or between two translations, within one language version | lock one rendering per concept per version |
| `institutional_false_friend` | a system-specific Vietnamese institutional, legal, or academic-title term is mapped onto a foreign near-equivalent without a gloss | keep the numbering/identity and gloss the institutional difference |
| `document_as_subject` | the sentence is about the paper, a section, or the act of writing (`phần này sẽ trình bày`, `như đã đề cập ở trên`, *this section will*) | delete a second roadmap; recast remaining cases so the subject is the object of study |
| `verification_log_prose` | a checklist confirmation is reported as a result (`đã kiểm tra`, `checksum khớp`, `0 lỗi`) | state the property the check establishes and, explicitly, the property it does not; relocate the log |
| `internal_artifact_reference` | a path on the author's machine, a working filename, a ticket, a bare commit hash, or a sheet column appears in publication-facing prose | relocate the identifier to a data card or repository record; keep public DOI/URL/dataset names |
| `repo_artifact_reference` | a repository script or data filename appears in body prose outside a data or reproducibility statement | state what the step does; move the filename into the reproducibility statement, where it is a legitimate public identifier |
| `assistant_residue` | the drafting conversation is visible (`theo yêu cầu của anh`, *as requested*, *the assistant*) | delete; the published text has no addressee inside the production process |
| `placeholder_residue` | a drafting token survived (`TODO`, `TBD`, `[…]`, `???`) | resolve or delete before delivery |
| `revision_response_leak` | reviewer-letter register appears in the manuscript (`theo góp ý của phản biện`) | move it to the response letter; the manuscript states the resulting claim |

`invented_sample_size`, `causal_overclaim`, `causal_claim`,
`population_generalization`, `invented_citation`, `fabricated_constraint`,
`assistant_residue`, `placeholder_residue`, and `internal_artifact_reference`
are blocking. Other failures require revision when they materially affect the
argument.

`fabricated_constraint` is blocking because it is the only failure here that
destroys correct work. The others degrade a claim; this one deletes content that
was compliant, and the deletion is invisible afterwards — nothing in the
manuscript records that a section was shortened to satisfy a rule nobody
imposed.

`self_reminder_prose`, `document_as_subject`, `defensive_disclaimer_stack`,
`config_dump_prose`, `progress_state_limitation`, `operational_log_prose`,
`verification_log_prose`, `todo_future_work`, and `revision_response_leak`
require revision on every occurrence rather than only when material. All are
visible to a reviewer on a first reading. A lexical scanner raises the floor;
paraphrases still require a manual pass over Methods, Limitations, Future Work,
and every integrity subsection. See
[Internal register gate](internal-register-gate.md).

`overtranslation_of_designator` and `distinction_collapse_by_translation` are
blocking. Both change what the text refers to rather than how it reads: the first
severs the reader from an external object, the second erases a contrast the argument
depends on. The remaining terminology codes require revision, and
`invented_vietnamese_term` additionally requires that the uncertainty be reported
rather than absorbed. See
[Terminology localization policy](terminology-localization.md).

`generated_artifact_drift` is blocking in one direction. Regenerating an
artifact over a user's hand edits destroys correct work exactly as
`fabricated_constraint` does, and just as invisibly — the rebuilt file carries
no record that the edits existed.

## Operational record versus scientific claim

`operational_log_prose`, `progress_state_limitation`, and `todo_future_work`
share one cause: a build log, audit spreadsheet, or task tracker is used as the
draft's source, so its unit of analysis (files, rows, candidates, completed
steps) survives into the manuscript. The text stays true and still fails,
because a reader cannot act on it.

Apply this test to every sentence in a Methods, Limitations, or Future Work
section: **if the sentence would change when the team finishes more work but the
scientific finding would not, it is a progress report.** Two rewrites follow.

- Progress form: *"The two annotator files contain 240 rows but the rating
  columns are empty, so no kappa is reported."* The reader learns the state of
  two files.
- Inference form: *"Labels have no human reference annotation, so label
  reliability is unquantified and error from the generator cannot be separated
  from error in the source context."* The reader learns which conclusions are
  unavailable and why.

Intermediate pipeline tallies follow the same rule. Report the quantity that
carries a mechanism (an error rate, a retention rate, a measured skew) and the
procedure it triggered; drop the per-bucket candidate counts that only
reconstruct the team's spreadsheet. Reconciliation notes between two artifacts
are content only when the discrepancy changes how a number may be used — then
state the consequence ("the two figures share no denominator and cannot be
compared"), not the audit trail.

Verification checklists invert the usual direction of evidence: passing them
licenses nothing on its own, so a bare confirmation is not a result. Write the
property the check establishes and, explicitly, the property it does not.
