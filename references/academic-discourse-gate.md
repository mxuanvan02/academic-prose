# Academic Discourse Gate

This gate detects paragraph-level problems that sentence-level style scans cannot reliably identify. It reports candidates; it never rewrites a limitation automatically and never treats length or negation alone as proof of poor prose.

## 1. Classes

| Code | Candidate condition | Manual question | Repair |
| --- | --- | --- | --- |
| `deficit_centered_paragraph` | several missing-work statements organize one paragraph | Is the paragraph about the inference, or about unfinished work? | Start from the conclusion that is bounded, then state the mechanism and consequence. |
| `caveat_saturation` | several claim boundaries accumulate across adjacent sentences | Does the paragraph preserve a positive bounded claim? | State one supported claim and one scope boundary; do not deny claims the paper never made. |
| `research_agenda_as_task_list` | future work becomes a list of obligations | Does each item open a research question and name a design and payoff? | Recast as question → feasible design → conclusion the design would license. |
| `clause_overload` | a long sentence contains enough pivots to obscure claim boundaries | Can each claim, condition, and consequence be recovered unambiguously? | Split while preserving causal, contrastive, and scope relations. |

All four are revision-level findings. A clean scan is partial verification because paragraph function and evidential sufficiency have no complete lexical signature.

## 2. Quantitative floor

The scanner uses deliberately conservative thresholds:

- `deficit_centered_paragraph`: at least two independent missing-work markers and at least three combined deficit, boundary, or task markers;
- `caveat_saturation`: at least three boundary markers across at least two sentences;
- `research_agenda_as_task_list`: at least three obligation markers in one paragraph;
- `clause_overload`: at least 65 words and seven structural pivots in one sentence.

Thresholds identify review sites, not verdicts. One legitimate limitation, one bounded claim, or one proposed design must remain silent. Headings, short labels, and bibliography entries are excluded.

## 3. Required manual pass

For each candidate, record the paragraph's rhetorical job, admissible subject, claim status, evidence anchor, and section role. Then apply one of these repairs:

1. `recast_from_inference` — begin with the conclusion that the limitation weakens;
2. `retain_one_bounded_claim` — preserve the positive claim and one explicit boundary;
3. `recast_as_question_design_payoff` — convert obligations into a research question, design, and inferential payoff;
4. `split_preserving_relations` — split clauses without dropping modality, negation, scope, or citations.

Do not delete a scientific limitation to make the scan clean. That is `required_move_deletion`. Do not invent validation, uncertainty estimates, or experiments to satisfy the gate.

## 4. Execution

```bash
python3 scripts/academic_discourse_scan.py draft.docx --genre manuscript --report discourse-report.md
python3 scripts/academic_discourse_scan.py draft.md --json discourse-findings.json
python3 scripts/test_academic_discourse_scan.py
```

Run this gate on every `draft`, `develop`, `revise`, `humanize`, `audit`, and `translate` delivery of manuscript-like prose. Run both language versions independently. A candidate resolved in only one version is a `CONS` failure.

## 5. Verification contract

The implementation is available only when all of the following pass:

- dirty Vietnamese and English fixtures trigger all four classes;
- clean Vietnamese and English fixtures remain silent;
- a DOCX fixture is read as paragraphs and triggers the expected class;
- a single limitation and a long but structurally simple sentence remain silent;
- the repository validator executes this test suite.

## 6. LaTeX sources: extract prose before scanning

Running the scanner on a raw `.tex` source counts preamble lines, title
blocks, and `tabular` rows as sentences. Measured (HOEIT HUJOS build,
2026-09-16): 7 `clause_overload` candidates, **all false positives** — the
quoted "sentences" were `\documentclass…\usepackage` chains, the bilingual
author/affiliation block, and table bodies. On prose-only text (preamble,
floats, tabular environments, center blocks, and the bibliography stripped;
`\caption` text preserved) the same scan reported 0 candidates, gate
`scan_clean`.

Workflow:

1. `python3 scripts/tex_prose_extract.py main.tex -o /tmp/prose.txt`
2. Re-run the scanner (and, for consistency, the other three gates) on the
   extracted prose.
3. Adjudicate any raw-`.tex` hit by inspecting the quoted text: if it quotes
   markup, record it as a false positive of the same class as an
   `immutable_source_false_positive` and continue. Only hits quoting real
   author prose warrant a repair. Never rewrite preamble or table markup to
   silence a scanner.
