# Quality Rubric

Score each dimension from 0 to 5. The gate requires all dimensions at least 4, with no blocking failure. Scores are evidence summaries, not substitutes for error findings.

| ID | Dimension | 5 means |
| --- | --- | --- |
| `SEM` | Claim and evidence integrity | propositions are supported or visibly qualified; roles, conditions, quantities, and protected elements are preserved |
| `TERM` | Terminology | domain meanings are correct and glossary use is stable |
| `STANCE` | Scientific stance | modality, causality, attribution, and inference strength are calibrated |
| `LOGIC` | Argument and discourse logic | claim-evidence-warrant relations, section moves, and paragraph functions are clear and licensed |
| `LANG` | Target-language academic naturalness | syntax, collocation, register, and information flow are idiomatic and restrained in the target language |
| `VOICE` | Freedom from machine tells | no ceremonial padding, formulaic structure, or chatbot residue remains, and the author's supplied voice is preserved |
| `CONS` | Document consistency | terms, abbreviations, names, tense/aspect policy, number format, and formatting remain coherent |

`LANG` is language-parameterized. Score Vietnamese output against
[Academic Vietnamese standard](academic-vietnamese-standard.md) and English
output against [Academic English standard](academic-english-standard.md).

`VOICE` is scored only when the task includes a humanizing or revision
objective. A translation audit that is not asked to humanize reports `VOICE` as
not applicable rather than assigning a low score.

## Blocking Failures

Any occurrence forces `revise` or `human_review`, regardless of average score:

- `meaning_reversal`: the proposition or relation is reversed.
- `negation_loss`: negation, exception, or exclusion is removed or introduced.
- `causal_upgrade`: non-causal evidence is rendered causally.
- `unsupported_claim`: content or explanation not entailed by the source is added.
- `numeric_corruption`: a number, unit, range, comparator, formula, or statistical value changes.
- `citation_corruption`: attribution, quotation, citation marker, DOI, URL, or identifier changes.
- `scope_shift`: sample- or condition-bound evidence becomes broader or narrower.
- `stance_upgrade`: possibility, suggestion, or recommendation becomes certainty or obligation.
- `placeholder_corruption`: a protected structured token changes order, identity, or count.
- `evidence_fabrication`: a source, datum, quotation, method detail, or empirical fact is invented.
- `claim_without_status`: a consequential new-writing claim is presented as established although its evidence status is unknown or `needs_source`.
- `range_notation_corruption`: an en dash, minus sign, or numeric separator that carries range, eponym, or value meaning is altered, including a hyphen substituted for an en dash.
- `required_move_deletion`: a limitation, evidence boundary, alternative explanation, attribution, or template-mandated section is deleted rather than repaired.
- `overtranslation_of_designator`: a rigid designator is translated, so the named object is no longer reachable.
- `distinction_collapse_by_translation`: two source concepts separated in the argument receive one target rendering.
- `assistant_residue`: the drafting conversation is visible in the published text.
- `placeholder_residue`: a drafting token (`TODO`, `TBD`, `[…]`, `???`) survived delivery.
- `internal_artifact_reference`: a local path, working filename, ticket, commit, or sheet column appears in publication-facing prose.

- `uncertainty_omitted`: an estimate is presented with no interval and no statement that uncertainty is unquantified.
- `denominator_mismatch`: figures drawn from different populations are presented as comparable.
- `normal_approximation_misuse`: a normal critical value is used where the population standard deviation is unknown and the sample is small.
- `precision_conflation`: interval width is presented as precision although coverage is not established.
- `significance_without_magnitude`: a significance claim carries no effect size.
- `pvalue_misinterpretation`: a p-value is described as the probability of a hypothesis or of chance.
- `absence_as_equivalence`: a non-significant result is reported as no effect.
- `exploratory_as_confirmatory`: a post-hoc comparison is presented as planned.
- `multiplicity_unreported`: multiple comparisons appear without the total count or a declared correction policy.
- `baseline_parity_unstated`: a comparative claim omits the baseline's data, tuning budget, and protocol.
- `unbounded_superiority_claim`: uniform superiority is claimed with no failure-region analysis.
- `best_run_as_result`: a maximum over runs is presented as the result.
- `comparison_without_basis`: a comparative claim names no comparator.
- `response_only_claim`: a revision letter argues something the revised manuscript does not contain.
- `promissory_result`: a result or analysis is promised rather than reported.
- `deference_capitulation`: a correct claim is weakened to agree with a reviewer, without evidence.
- `comment_softening`: a reviewer's criticism is paraphrased, abridged, or reordered so that what was asked changes.
- `fabricated_declaration`: authorship, ethics, funding, conflict, registration, or availability content is invented or inferred.
- `availability_overstatement`: restricted, on-request, or unavailable data is described as available.
- `responsibility_deflection`: a disclosure is phrased to transfer accountability for claims to a tool.
- `coverletter_as_abstract`: a cover letter summarises the paper instead of arguing venue fit.
- `contribution_count_inflation`: one contribution is presented as several by restating it at different granularities.
- `venue_ambition_leak`: the publication target, venue tier, or an anticipated referee reaction is argued inside publication-facing prose.

`range_notation_corruption` and `required_move_deletion` are surface-rewriting
traps: a style pass can destroy content without changing a proposition, because
dashes carry quantitative meaning and genre-mandated moves carry scope.
`overtranslation_of_designator` and `distinction_collapse_by_translation` are
terminology traps: a localization pass can destroy retrieval or erase a contrast
the argument depends on.
`assistant_residue`, `placeholder_residue`, and `internal_artifact_reference`
are register traps: the text is true and still unusable, because a reader of the
published artifact cannot act on a conversation, a placeholder, or a path on the
author's machine.

The thirteen quantitative codes are **inference traps**: every one of them can
occur in a sentence whose arithmetic is correct, because the defect is in what the
number is claimed to establish rather than in its value. `uncertainty_omitted`,
`denominator_mismatch`, and `baseline_parity_unstated` make a result
unreviewable; the rest license a conclusion the evidence does not support.

`response_only_claim`, `promissory_result`, `deference_capitulation`, and
`comment_softening` are **peer-review traps**: the letter and the manuscript are
separate artifacts, so a claim can be true of one and false of the other.

`venue_ambition_leak` is a **strategy trap**: the sentence is fluent and
motivating, so ordinary editing preserves it. It is licensed in a cover
letter and blocking in a manuscript, which makes the genre argument part of
the check rather than a footnote to it.

`fabricated_declaration`, `availability_overstatement`,
`responsibility_deflection`, `coverletter_as_abstract`, and
`contribution_count_inflation` are **submission traps**: they are assertions only
the authors and their institution can make, and a wrong one is a
research-integrity matter rather than a writing defect.

## Decision

- `pass`: all applicable dimensions >= 4, no block, no unresolved term below 0.80 confidence.
- `revise`: repairable block/major error or any applicable dimension < 4.
- `human_review`: unresolved ambiguity affects a claim, legal/clinical meaning, key terminology, or protected content.

The audit must cite the source and draft span that supports each finding. Do not assign a low score without actionable evidence.

## Surface-rewriting gate

When the task removes machine tells, add these checks before the decision. Each
maps to a blocking failure above.

1. Modality of every consequential claim is unchanged or explicitly relicensed.
2. Every en dash in a range, eponym, or negative value survived.
3. Every citation, DOI, URL, identifier, formula, and unit is byte-identical.
4. No limitation, evidence-boundary, alternative-explanation, or template section was removed.
5. Locked terminology is unchanged and no ornamental synonym was introduced.
6. Declared style-guide and output-format conventions are intact.
7. Number format follows the target-language convention in prose and is untouched inside protected tokens.

A rewrite that reads better and fails any of these is a regression.

## Terminology localization gate

Run when the output is Vietnamese, when either language version contains
source-language terms in body prose, or when a bilingual pair must stay aligned.
Each check maps to a code in
[Terminology localization policy](terminology-localization.md).

1. Every source-language run in body prose has a recorded policy: `keep_source`,
   `translate`, `translate_with_gloss`, `keep_with_gloss`, or `needs_review`.
2. No rigid designator was translated, and no preserved designator lacks a
   Vietnamese category noun where a reader outside the toolchain needs one.
3. Every load-bearing distinction the argument uses has two distinct renderings.
4. Each rendering has an authority at tier 1--4, or is reported as `needs_review`;
   no tier-5 coinage is asserted as the field's term.
5. One rendering per concept per language version, glossed at first use in the
   abstract and at first use in the body, and paired across the two versions.

`TERM` cannot score 4 while any check fails, and `CONS` cannot score 4 while a
concept alternates renderings.

## Internal register gate

Run on every delivery of publication-facing prose, in any language, whether the
text was authored or translated. Each check maps to a class in
[Internal register gate](internal-register-gate.md).

1. Every candidate sentence flagged by the scan has a recorded verdict:
   `delete`, `recast`, `relocate`, or `license`. **`soften` is not a verdict** —
   hedging an internal sentence leaves it internal and now also vague.
2. Zero occurrences of the three blocking classes: `assistant_residue`,
   `placeholder_residue`, `internal_artifact_reference`.
3. Zero self-address constructions; at most one roadmap passage per document and
   at most one document-as-subject sentence per section.
4. No sentence in Limitations or Future Work has the project as its subject; each
   names the inference it bounds or the question it opens.
5. No verification confirmation stands as a result: each states the property the
   check establishes and the property it does not.
6. At most two claim-negation markers within any three consecutive sentences.
7. Both language versions were cleaned, and the manual pass over Methods,
   Limitations, Future Work, and integrity subsections is reported separately
   from the scan.

`SEM` cannot score 4 while a blocking class is present. `VOICE` cannot score 4
while any self-address remains. `CONS` cannot score 4 while one language version
was cleaned and the other was not. A scan-only clean report is a partial
verification and must be labelled as one.

## Process logic gate

Run when the text narrates a procedure, a chronology, or a pipeline in any
language. Codes are defined in
[Process logic gate](process-logic-gate.md).

1. Every ordered step sequence is checked for `chronology_inversion`: a later
   step may not be described as a precondition of an earlier one.
2. Every quantifier, negation, and comparative scope is checked for
   `modifier_scope_drift`: the scope in the draft matches the scope in the
   source or in the ledger entry.
3. Each candidate carries a recorded verdict; a lexical hit is not a verdict.

`LOGIC` cannot score 4 while a chronology inversion stands. `SEM` cannot score 4
while a modifier scope differs from its source.

## Vietnamese AI-pattern gate

Run on every Vietnamese deliverable, and on English text carrying the same
machine tells. Codes and the licensed list are defined in
[Vietnamese AI-pattern gate](vi-ai-pattern-gate.md), whose evidence base is
[Vietnamese AI pattern registry](ai-pattern-vietnamese.md).

1. Every candidate has a recorded verdict: `replace_with_measurement`,
   `delete`, `recast`, or `license`. Softening a ceremonial phrase is not a
   verdict — the padding survives and the sentence is now also vague.
2. `ceremonial_padding` and `unquantified_intensifier` are repaired by supplying
   the measurement, or by deleting the evaluation when no number exists. Never
   invent a magnitude to satisfy this check.
3. `empty_framing`, `translation_calque`, and `symmetric_padding` are deleted or
   recast; the proposition they wrap must survive unchanged.
4. `hedge_stack` collapses to exactly one calibrated marker. Reducing hedges to
   zero is `stance_upgrade`, a blocking failure.
5. `machine_marked_passage` requires several independent signals to co-occur;
   one ceremonial word is not evidence of machine authorship.
6. The §7 licensed list is honoured: topic-comment structure, Sino-Vietnamese
   terminology, genre-mandated Vietnamese sections, decimal comma, en dash in
   ranges, and a repeated locked term are correct prose, not defects.

`VOICE` cannot score 4 while an unresolved candidate remains. `LANG` cannot
score 4 while a calque stands. A scan reporting zero candidates is a partial
verification: hedge deletion and terminology drift have no lexical signature.

## Venue-ambition gate

Run on every publication-facing deliverable, declaring the genre the artifact
actually is. Codes and the licensing table are in
[Internal register gate](internal-register-gate.md) section 11.

1. No sentence argues from venue tier, prestige, or an indexing metric.
2. No sentence states an intention to publish or submit.
3. No sentence names an anticipated referee reaction as the reason for a
   methodological choice.
4. Every hit is recast to the scientific reason. `delete` is permitted only
   when no methodological justification is being carried; `soften` is not a
   verdict.
5. The scan was run with the correct genre. A cover letter scanned as a
   manuscript reports findings the genre licenses.

`SEM` cannot score 4 while a leak stands, because the paper is asserting a
reason the evidence does not contain.

## Quantitative reporting gate

Run on every deliverable containing a numeric claim, in either language. Codes are
defined in [Quantitative reporting standard](quantitative-reporting-standard.md).

1. Every reported estimate carries its denominator and an interval, or an explicit
   statement that uncertainty is unquantified. Never invent an interval.
2. Two figures placed adjacently share a denominator, or the populations are named.
3. Small-sample intervals use the *t* distribution. A normal critical value
   requires a known population standard deviation or a large sample.
4. Every significance claim carries an effect size; every comparative claim names
   its comparator and states baseline parity.
5. Multiple comparisons declare their count and correction policy; post-hoc
   comparisons are labelled exploratory.
6. A superiority claim either bounds its scope or reports where the method fails.

`SEM` cannot score 4 while any of these is unresolved. Supplying a missing number
is the author's decision, never this skill's inference.

## Revision-response gate

Run on every response letter, cover letter, or rebuttal. Codes are defined in
[Revision response genres](revision-response-genres.md).

1. Every numbered reviewer comment has exactly one block, quoted verbatim, with an
   accept / accept-in-part / decline verdict in its first clause.
2. Every claimed change resolves to a location that exists in the revised
   manuscript, and every substantive argument in the letter appears there too.
3. No future-tense commitment stands in for an unrun analysis.
4. Every accepted comment that weakens a claim was driven by evidence rather than
   by deference.

`SEM` and `LOGIC` cannot score 4 while a letter–manuscript divergence stands.

## Submission declarations gate

Run before any submission artifact is called ready. Codes are defined in
[Submission integrity declarations](submission-integrity-declarations.md).

1. No declaration field is completed by inference. Unknown values emit a visible
   placeholder plus a named blocker, never a plausible value.
2. Availability statements match what exists and what it contains.
3. Generative-AI disclosure follows the target venue's own current policy,
   retrieved from the venue; no tool is named as author or contributor.
4. Contributions map one-to-one onto research questions and reported results.

`SEM` cannot score 4 while an unsourced declaration stands, and the delivery
message must list every blocker rather than presenting the artifact as complete.
