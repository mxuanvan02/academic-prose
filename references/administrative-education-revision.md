# Administrative education document revision

Use this playbook for Vietnamese curriculum plans, teaching plans, appendices, lesson plans, and similar school-administration artifacts. The content skill owns wording and claim integrity; the DOCX/slide skill owns layout and rendering.

## 1. Lock the evidence boundary

Before rewriting, classify each item:

- **Locked:** lesson names, periods, weeks, assessment positions, legal references, competency codes, STEM/STEAM labels, English annotations, and placeholders for unknown staffing or enrolment data.
- **Derivable:** totals and summary statements that can be recomputed from row-level entries.
- **Unknown:** values absent from a reliable source. Keep the placeholder or mark for human completion; never infer them from OCR noise or nearby documents.

A smoother sentence is not permission to change a locked item.

## 2. Recompute summaries from rows

Treat row-level curriculum entries as the primary internal evidence. Recompute statements such as total lessons, lessons taught by stations, integration-level counts, periods, and themes from those rows. Then compare the result across every related appendix.

Do not repair a discrepancy by choosing the more plausible summary. Record:

1. source rows used;
2. computed value;
3. obsolete summary value;
4. all locations updated.

If the row classification itself is uncertain, retain the original value and flag it for human review.

## 3. Distinguish duplication from structural resumption

Repeated labels can be semantically required. A theme heading may appear again after a midterm or semester assessment to resume the same content strand. Before deleting a repeated heading, inspect the sequence:

`theme -> lessons -> assessment block -> same theme -> next lessons`

This is a resumption, not an accidental duplicate. The layout gate should keep each heading with the first following lesson, but the prose audit must not remove it merely because the wording repeats.

## 4. Rewrite at the right level

Replace mechanical requirement formulas with observable learning outcomes while preserving scope and cognitive demand. Prefer verbs such as `phân biệt được`, `thực hiện được`, `thiết kế được`, and `giải thích được` only when licensed by the source.

For conditions of implementation, bind resources to the specific activity rather than copying a generic inventory into every row. Preserve institutional register: concise, explicit, and administrative; do not imitate journal prose or add ornamental formality.

Maintain an old-to-new ledger for material edits, including the evidence or internal inconsistency that licenses each factual correction.

## 5. Design activities as an auditable evidence chain

For every educational activity—especially the activity appendix—write and audit this chain in order:

`objective -> learner task -> product/evidence -> observable criteria -> competency`

Each link must constrain the next:

1. **Objective:** state the knowledge, skill, or disposition the learner must demonstrate.
2. **Learner task:** describe what the learner actually does; a teaching method label is not a task.
3. **Product/evidence:** name the file, artefact, operation, log, checklist, test case, explanation, or performance that will be observed.
4. **Criteria:** state what makes the product or process acceptable; use countable, testable, or directly observable conditions where possible.
5. **Competency:** assign only the competency that the task and evidence actually expose.

Reject rows that jump directly from a broad objective to a competency label. Also reject generic evidence such as `sản phẩm học tập` when the concrete artefact can be named. Conditions of implementation belong to this same chain: equipment, data, accounts, safety constraints, and collaborators must support the specified task rather than decorate the row.

## 6. Gate STEM/STEAM and digital-competency labels

### STEM/STEAM classification gate

Do not treat STEM/STEAM as an enrichment label. Record it only when the activity contains all of the following:

- a practical problem, need, or design constraint;
- appropriate integration of disciplinary knowledge;
- a process that designs or selects a solution, creates or implements it, tests it, and improves it;
- an assessable product and criteria for both result and process.

`Dạy học theo trạm`, ordinary software practice, use of digital equipment, or coordination with another subject does not by itself establish STEM. Use STEAM only when the arts contribution changes communication, usability, interpretation, or design quality under explicit criteria; decorative styling is insufficient. If the chain is incomplete, classify the row as ordinary subject practice or digital-competency development and state that it is not STEM/STEAM when ambiguity is likely.

Never publish totals such as “N STEM lessons” or “N station lessons” unless every counted row has passed the same gate and the total can be recomputed from those rows.

### Digital-competency traceability gate

Use the official component-level code only after verifying the controlling legal framework and only when it can be traced to an observable task and evidence. Maintain a compact traceability matrix:

| lesson/activity | learner task | evidence | criterion | component code |
| --- | --- | --- | --- | --- |

A domain name alone is not a component code. Repeated appearances of a code do not establish proficiency, and frequency counts must not be presented as attainment levels. If the source framework cannot be read reliably, describe the competency and evidence first, leave the code pending, and resolve it from the authoritative text before final delivery.

## 7. Synchronize related appendices from one source of truth

When several appendices describe the same curriculum, choose one row-level source of truth before editing. For Vietnamese school plans, the activity appendix normally owns the full design chain, while distribution and teacher-plan appendices carry compact annotations.

For each specially classified activity:

1. lock its identity: lesson/activity, week or period, product, classification, and competency code;
2. place the full objective–task–evidence–criteria chain in the activity appendix;
3. mirror a concise but recognizable product/evidence annotation in the distribution and teacher-plan appendices;
4. compare the two compact annotation maps by row identifier, not by visual position;
5. sweep summaries and narrative sections for obsolete totals, labels, and organizational names.

Do not copy the full activity paragraph into every appendix. Synchronization means semantic identity and traceability, not textual duplication.

## 8. Run prose gates on extracted UTF-8 text

The scanners are text tools. Unless a script explicitly supports DOCX, extract text to UTF-8 first, recursively including body paragraphs, top-level tables, and nested tables. Do not pass the binary `.docx` to a UTF-8 reader.

Check each script's current CLI with `-h`; genre vocabularies differ. For this class of document, the supported mappings used by the current scripts are:

```bash
python scripts/vi_ai_pattern_scan.py document.txt --genre thesis --json vi.json --quiet
python scripts/process_logic_scan.py document.txt --json logic.json --quiet
python scripts/internal_register_scan.py document.txt --genre teaching --json register.json --quiet
```

`administrative` is not a valid genre unless the script's help explicitly lists it. An invalid genre, Unicode decode error, or missing script path is an invocation failure—not a finding in the document. Correct the invocation and rerun.

Interpret exit codes per script rather than assuming one shared convention. A clean scan is partial verification only; manually inspect terminology drift, changed modality, unsupported corrections, and structural repetition.

## 9. Cross-document and rendering gates

After revision:

- compare paragraph/cell text and package structure with the source;
- verify every intended old/new replacement and absence of obsolete summaries;
- cross-check totals and labels across related appendices;
- sample every STEM/STEAM or competency annotation backward from compact note to concrete task, evidence, and criterion in the source-of-truth row;
- confirm organizational names and legal-framework references are identical across the document set;
- run the DOCX skill's table-pagination and render QA;
- keep the edited files separate from the authoritative copies until the user approves them.

Never call the content gate complete merely because the files open or the automated scanners return zero. Delivery requires both a clean cross-document traceability check and rendered-page QA.