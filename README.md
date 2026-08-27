# academic-vi

A write-first Agent Skill for thinking through, structuring, drafting, translating, revising, and auditing Vietnamese academic discourse. Its central rule is: **claims and evidence precede prose; semantic integrity precedes fluency**.

## What It Adds

- A Vietnamese academic prose standard.
- A claim-evidence ledger and composition workflow from notes to complete text.
- A routing matrix for conceptualization, outlining, argumentation, synthesis,
  drafting, development, compression, expansion, paraphrase, revision, audit,
  and translation.
- Rhetorical playbooks for abstracts, introductions, synthesis, methods, results, discussions, and conclusions.
- An English-to-Vietnamese interference taxonomy.
- Discipline and genre profiles without pretending one style fits every field.
- A six-dimension quality gate with blocking semantic failures.
- Traceable glossary and revision records.
- A handoff contract for `pdf-translate`.

It does not search literature, review research methodology, verify citations against external databases, or manipulate PDF layout.

## Install

```bash
npx skills add mxuanvan02/academic-vi -g --all
```

## Use

Write from research material:

```text
Use $academic-vi to turn these claims, evidence, and constraints into a Vietnamese
Discussion section. Build a claim-evidence ledger, mark anything needing a source,
design the paragraph progression, then draft and adversarially review it.
```

Develop an argument before drafting:

```text
Use $academic-vi to conceptualize this research problem, build a claim-evidence
ledger, and produce an annotated Vietnamese outline. Do not draft unsupported
claims as facts.
```

```text
Use $academic-vi to translate this abstract into publication-quality Vietnamese.
Preserve scientific stance and produce a terminology table and audit.
```

```text
Use $academic-vi to revise this Discussion section. Detect English interference,
overstatement, terminology drift, and unnatural Vietnamese academic prose.
```

With PDF handoff:

```text
Use $pdf-translate in handoff mode and $academic-vi for the English-to-Vietnamese
translation. Preserve every formula placeholder and audit scientific stance.
```

## Quality Model

Every substantial output is evaluated on claim-evidence integrity (`SEM`), terminology (`TERM`), scientific stance (`STANCE`), argument and discourse logic (`LOGIC`), Vietnamese academic naturalness (`VI`), and document consistency (`CONS`). A high average cannot compensate for a blocking semantic or evidence error.

## Validation

```bash
python3 scripts/validate_skill.py
python3 -m unittest discover -s tests -v
```

All eval examples are synthetic. No private manuscript is included.
