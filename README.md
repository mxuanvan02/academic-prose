# academic-vi

An Agent Skill for writing, translating, revising, and auditing Vietnamese academic prose. Its central rule is simple: **semantic fidelity precedes fluency**.

## What It Adds

- A Vietnamese academic prose standard.
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

Every substantial output is evaluated on semantic fidelity (`SEM`), terminology (`TERM`), scientific stance (`STANCE`), discourse logic (`LOGIC`), Vietnamese academic naturalness (`VI`), and document consistency (`CONS`). A high average cannot compensate for a blocking semantic error.

## Validation

```bash
python3 scripts/validate_skill.py
python3 -m unittest discover -s tests -v
```

All eval examples are synthetic. No private manuscript is included.
