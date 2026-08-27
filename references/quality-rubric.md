# Quality Rubric

Score each dimension from 0 to 5. The gate requires all dimensions at least 4, with no blocking failure. Scores are evidence summaries, not substitutes for error findings.

| ID | Dimension | 5 means |
| --- | --- | --- |
| `SEM` | Claim and evidence integrity | propositions are supported or visibly qualified; roles, conditions, quantities, and protected elements are preserved |
| `TERM` | Terminology | domain meanings are correct and glossary use is stable |
| `STANCE` | Scientific stance | modality, causality, attribution, and inference strength are calibrated |
| `LOGIC` | Argument and discourse logic | claim-evidence-warrant relations, section moves, and paragraph functions are clear and licensed |
| `VI` | Vietnamese academic naturalness | syntax, collocation, register, and information flow are idiomatic and restrained |
| `CONS` | Document consistency | terms, abbreviations, names, tense/aspect policy, and formatting remain coherent |

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

## Decision

- `pass`: all dimensions >= 4, no block, no unresolved term below 0.80 confidence.
- `revise`: repairable block/major error or any dimension < 4.
- `human_review`: unresolved ambiguity affects a claim, legal/clinical meaning, key terminology, or protected content.

The audit must cite the source and draft span that supports each finding. Do not assign a low score without actionable evidence.
