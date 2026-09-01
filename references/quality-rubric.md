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

The last two are specific to surface-level rewriting. They exist because a
style pass can destroy content without changing a single proposition: dashes
carry quantitative meaning, and genre-mandated moves carry scope.

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
