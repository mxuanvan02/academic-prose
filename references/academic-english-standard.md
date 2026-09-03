# Academic English Standard

This reference is the English counterpart of [Academic Vietnamese standard](academic-vietnamese-standard.md). Both realize the same composition engine; only the target-language criteria differ. Nothing here weakens the claim-integrity contract.

## Priority

The priority order is: **meaning -> terminology -> scientific stance -> logic -> English expression -> AI-pattern removal -> surface polish**. A later layer may not damage an earlier one.

## Sentence-Level Criteria

1. **Propositional completeness**: the reader can identify who or what performs, measures, or supports the stated relation, even when the actor is deliberately backgrounded.
2. **Predicate fitness**: choose verbs that collocate with the object and the discipline. `conduct an analysis` is weaker than `analyze` unless the noun carries a methodological distinction.
3. **Information structure**: place given information before new information; keep the sentence focus in end position where the argument allows.
4. **Controlled density**: split a sentence when nested clauses obscure claim boundaries, but preserve the logical relation between them.
5. **Economy**: remove empty frames such as `there is a need to`, `it is important to note that`, `in order to`, and `the fact that`, unless they carry a real distinction.
6. **Nominalization discipline**: prefer a verb when the noun hides the action (`we measured` over `measurement was performed`), but retain established nominal terms (`randomization`, `attrition`, `stratification`).

## Paragraph-Level Criteria

- Each paragraph has one discernible function: frame, claim, evidence, interpretation, contrast, limitation, or implication.
- The topic sentence carries the paragraph's claim, not merely its subject matter.
- Connectives represent relations present in the argument. Do not insert `therefore`, `moreover`, or `thus` to improve flow.
- Repeating a technical term is preferable to ornamental synonym substitution.
- A paragraph must not merge the authors' findings with cited findings or with speculation.

## Scientific Stance

Preserve the source's epistemic force. This table is the English mirror of the Vietnamese stance table.

| Source function | Typical English | Forbidden upgrade |
| --- | --- | --- |
| reports an observation | `results show`, `we observed`, `the data indicate` | `proves`, `demonstrates conclusively` |
| suggests an interpretation | `suggests`, `may indicate`, `is consistent with` | `establishes`, `confirms` |
| association | `is associated with`, `correlates with` | `causes`, `leads to`, `results in` |
| possibility | `may`, `might`, `could` | unqualified assertion |
| limitation | `applies only to`, `does not support generalization to` | vague `should be interpreted with caution` |
| recommendation | `we recommend`, `should be considered` | `must`, `is required` |
| absence of evidence | `we found no evidence that` | `there is no effect` |

The last row is a distinct failure mode. Absence of evidence is not evidence of absence, and collapsing the two is a blocking `stance_upgrade`.

## Hedging Inventory

Hedges carry epistemic force. Keep a functional inventory rather than a banned-word list.

| Function | Devices |
| --- | --- |
| epistemic modality | `may`, `might`, `could`, `appears to`, `seems to` |
| approximation | `approximately`, `about`, `on the order of` |
| frequency and extent | `often`, `in most cases`, `predominantly` |
| attribution shielding | `according to`, `X argues that`, `reportedly` |
| scope limitation | `within this sample`, `under these conditions`, `for the period studied` |

Collapse a stack to one calibrated device. Never reach zero. `may possibly indicate a potential trend` becomes `may indicate a trend`, not `indicates a trend`.

## Register

Use precise contemporary academic English. Formality does not require Latinate vocabulary, long nominal chains, or pervasive passive voice. Avoid promotional adjectives (`novel`, `groundbreaking`, `state-of-the-art`, `robust`) unless the comparison basis is defined and evidenced. `Novel` requires a stated baseline; otherwise it is `unsupported_novelty`.

First person is permitted in most contemporary venues and often improves clarity about who did what. Follow the declared style guide when one exists; do not impose or forbid first person by default.

## Style-Guide Deference

Heading capitalization, quotation-mark style, serial comma, number formatting, and reference style are format decisions owned by the declared style guide or template, not by voice preference. Common declarations:

| Convention | APA 7 | Chicago | IEEE | Vancouver |
| --- | --- | --- | --- | --- |
| headings | sentence case | headline case | headline case | sentence case |
| serial comma | required | required | required | varies |
| in-text citation | author-date | note or author-date | bracketed number | bracketed number |

When no style guide is declared, default to sentence-case headings, straight quotes in LaTeX and Markdown sources, and the serial comma. Record the assumption in the profile rather than silently normalizing.

## Publication-Facing Abstraction

Express the research object, procedure, and data structure through disciplinary concepts. Do not expose schema field names, configuration keys, internal flags, directory names, or pipeline labels merely because they occur in code or technical documentation. Retain a tool, model name, parameter, or identifier only when it is necessary for reproducibility, identifies the object under study, or prevents substantive ambiguity.

This abstraction must not conceal a consequential methodological choice. Report that records were split at document level; the internal names of the fields storing that value are normally unnecessary.

## Protected Elements

Copy formulas, symbols, values, units, citations, DOI, URLs, code, dataset names, model names, quoted text, and structured placeholders exactly unless the task explicitly changes their formatting.

English-specific protected notation that AI-pattern rules threaten:

- en dash in ranges (`12–18 mg`, `pp. 145–162`, `2018–2023`);
- en dash in eponymous compounds naming two people (`Kaplan–Meier`, `Mann–Whitney U`);
- minus sign versus hyphen in negative values;
- hyphenated chemical, gene, and compound-modifier terms (`beta-catenin`, `HLA-DRB1`, `first-order`);
- capitalization of gene symbols, taxa, units, and trademarked model names.

See [AI pattern taxonomy](ai-pattern-taxonomy.md) §14 and §26 for the interaction between dash and hyphen rules and these protected forms.

## English AI-Pattern Notes

The upstream watched-word lists are English and apply directly. Three additions matter in academic English specifically:

- **Methods passive is not an AI tell.** `Samples were incubated at 37 °C` is standard. Forcing an actor is correct only when the venue permits first person and the authors performed the step.
- **Structured-abstract labels are not bold mini-headings.** `**Background:**`, `**Methods:**`, `**Results:**` are template-mandated when the venue requires a structured abstract.
- **Related Work is about prior versions by design.** Pattern 30 does not apply to Background, Related Work, or a response-to-reviewers letter.

## Cross-Language Symmetry

Vietnamese institutional, legal, administrative, and academic-title terms are
system-specific and rarely have an exact English equivalent. Preserve instrument
numbering, and gloss the institutional difference rather than substituting a
near-equivalent; see the reverse-direction section of
[Terminology localization policy](terminology-localization.md).

When a document exists in both languages, keep one glossary with paired renderings, one claim ledger, and one stance calibration. A hedge present in one language must be present in the other. A claim that is `needs_source` in Vietnamese is `needs_source` in English. Divergence between versions is a `CONS` failure, not a stylistic choice.
