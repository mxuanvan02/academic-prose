# Whole-manuscript structural revision

Use this playbook when feedback concerns density, section roles, citation coverage, notation order, or the meaning of the paper—not merely sentence polish.

When the feedback is a received peer-review report on a paper with a public code/data artifact, follow `references/peer-review-revision-evidence.md` first (reproduce → verify tables byte-for-byte → answer from re-executed evidence); this file then governs the structural editing itself.

## 1. Diagnose by rhetorical function

Build a section map before editing:

| Section | Required job | Common contamination |
|---|---|---|
| Introduction | problem → evidence-backed gap → objective → contributions | detailed results, methods minutiae, unsupported background claims |
| Related Work | organize prior approaches and expose the precise unresolved gap | bibliography-by-bibliography summary, claims that belong in Introduction |
| Method | define objects, mechanism, notation, and rationale in dependency order | experimental settings, statistics, results |
| Experimental Design | population/unit, arms, outcomes, calibration, tests, exclusions | method motivation, result interpretation |
| Results | report estimates, denominators, uncertainty, and predeclared status | causal explanation, implications, recommendations |
| Discussion | interpret, bound, compare, explain trade-offs and limitations | replaying every number from Results |
| Conclusion | answer the research question at the licensed scope | a second abstract or full result inventory |

When a section does two incompatible jobs, move material before compressing it. Sentence-level shortening cannot repair a role error.

## 2. Citation audit by claim, not section

Mark every externally checkable background or comparative statement as one of:

- common disciplinary knowledge;
- supported by a nearby citation;
- author result or design choice;
- `needs_source`.

The Introduction deserves an explicit pass because broad motivation often accumulates uncited claims. Place citations directly after the proposition they support. Do not add citations to author contributions or design decisions merely to increase citation density, and never invent a source.

## 3. Notation onboarding

Create a dependency graph for symbols and predicates. A symbol must not appear in prose, a table, or an equation before its inputs and purpose are introduced.

For a family such as `G_1 … G_n`, use this order:

1. explain the conceptual groups and why they are separate;
2. provide a compact role table (identifier, check, scientific meaning) when eight or more conditions would overload prose;
3. define the input objects and normalizers;
4. formalize predicates in numerical/dependency order;
5. define aggregate indicators only after all components;
6. explain limitations and calibration after the formal definitions.

A role table is useful content, not page filler. It should let a reader understand why `G_6` exists before reading its formula. Do not introduce `G_6–G_8` first merely because they are the novel conditions.

## 4. Compression without scientific loss

Compress in this order:

1. remove repeated interpretation across Abstract, Introduction, Results, Discussion, and Conclusion;
2. move details to the section that owns them;
3. merge sentences with the same claim/evidence pair;
4. replace repeated gate explanations with one role table;
5. shorten surface prose last.

Preserve denominators, uncertainty, inferential status, calibration scope, exclusions, replication criteria, deviations, and limitations that change interpretation. Compare the old and new drafts for removed citations, labels, numerical tokens, and reproducibility details. Treat the comparison as a diagnostic, not an automatic mandate to restore every removed token.

Never add prose or stretch layout merely to hit a recommended page range. If the venue has a lower bound, add only scientifically useful content such as a notation map or missing reproducibility detail. Distinguish a recommended range from an absolute maximum and its actual consequence.

### Measure in the artifact's own units, and stop hand-nudging

Compression toward a hard cap fails in a specific, repeatable way: the agent
edits a section, re-counts an approximation, and iterates. Two failure modes
follow, both observed.

**Counting the wrong thing.** A cap stated as "including footnotes and
references" is three budgets, not one. Measure them separately and report the
sum, because the compressible bucket is usually the smallest of the three: one
measured manuscript sat at 7.6k body + 1.4k footnotes + 1.1k bibliography, so
"cut 800 words" meant cutting 10% of the body, not 8% of the document. Count in
the delivered artifact (the DOCX/PDF), not the Markdown source — Markdown
`\S+` counting inflates by treating table pipes and footnote markers as words,
and deflates by missing content the converter generates. See
[Venue constraint budget](venue-constraint-budget.md) for the three-bucket
procedure and `scripts/docx_journal_build.py` for a re-runnable measurement.

**Nudging past the target.** Rewriting a section to be shorter reliably makes it
longer when the rewrite also sharpens an argument. One measured sequence moved
11,173 → 11,211 (up 38) on a pass whose stated intent was compression, after
several passes of single-digit progress. The rule: if a pass moves the count the
wrong way, or the last two passes each netted under ~50 words against a
several-hundred-word deficit, stop patching sentences. Re-budget per section
with an explicit word allowance and rewrite the over-budget sections whole.
Per-sentence nudging cannot close a large deficit and burns a full
convert-and-measure cycle per attempt.

Two corollaries. Fix content before layout: the count is a property of the text,
so recount in text space and convert once the number is inside the cap. And when
replacing text programmatically, verify the replacement applied — after several
compression passes the string you remember is not the string in the file, and a
silent no-op looks identical to a successful edit until the count fails to move.
Report the miss count, never assume zero.

## 5. Disclaimer and scope-statement placement

A common framing error is placing limitations, caveats, or scope disclaimers inside the contributions paragraph, Results summary, or Conclusion opening. This undermines the paper's value before the reviewer can assess it. Apply these placement rules:

| Statement type | Correct location | Wrong location |
|---|---|---|
| "Labels not expert-validated" | Limitations section; Abstract boundary sentence (last) | Contributions paragraph; Results opening |
| "Does not evaluate retrieval/legal correctness" | Limitations; Abstract boundary sentence | Contributions paragraph; Results body |
| "Same-family models reported separately" | Methods (experimental design); Table footnote | Contributions paragraph (as self-deprecation) |
| "Not representative of all law" | Limitations; forward reference from Results | Results subsection on coverage |
| "Model used only for filtering" | Methods (with forward ref to Limitations) | Related Work (as standalone disclaimer) |

Principle: **Contributions = assertions.** Scope and limitations belong in their own section or as the final boundary sentence of the Abstract. In Results, report what was observed; interpret in Discussion; bound in Limitations. A forward reference (`see Section X`) is acceptable when a result naturally invites a caveat, but the caveat itself must live in the designated section.

When auditing a draft, scan every contributions paragraph, Results opening, and Conclusion for phrases like "chưa được thẩm định", "không đánh giá", "chỉ mang giá trị", "không đồng nghĩa", "phù hợp nhất cho nghiên cứu sơ bộ". These are red flags when they appear outside Limitations or the Abstract's closing boundary.

## 6. Methods rationale requirement

Every methodological step must explain **why** it was chosen, not just **what** was done. A Methods section that lists actions without justification reads as a protocol dump, not a scientific argument. For each step, answer:

1. What problem does this step solve?
2. Why this specific approach/threshold/model rather than alternatives?
3. What would go wrong if this step were omitted?

Example — audit step "remove degenerate stems":
- ❌ "Bước 2 loại câu hỏi suy biến: thân câu không chứa dấu hỏi hoặc từ nghi vấn tiếng Việt."
- ✅ "Bước 2 loại câu hỏi suy biến, tức các bản ghi mà phần thân câu không chứa dấu hỏi hoặc từ nghi vấn tiếng Việt. Lý do: câu hỏi trắc nghiệm phải đặt ra một yêu cầu trả lời xác định; thân câu chỉ là nhãn chủ đề không thể đánh giá được vì không có đáp án đúng hay sai."

This applies equally to model selection ("Qwen2.5-7B-Instruct được chọn vì khả năng tiếng Việt và sự sẵn có của trọng số mở, cho phép tái lập mà không phụ thuộc vào API thương mại"), threshold choices, and filtering criteria.

Related Work should be written as continuous prose paragraphs, not subsections, unless the venue explicitly requires structured related work. Subsections fragment the narrative and invite bibliography-by-bibliography summaries instead of synthesized positioning.

## 7. Results–Discussion separation

Run a sentence-level classification:

- numerical observation, interval, test, or prespecified status → Results;
- mechanism, interpretation, validity consequence, trade-off, or implication → Discussion;
- design definition or grading rule → Experimental Design.

Results may include minimal orientation (e.g., “higher/lower”) but not an explanation of why the pattern occurred. Discussion may cite a few anchor values but must not repeat the full result inventory.

## 8. Validation ladder

After structural edits:

1. build with the declared document engine;
2. verify no undefined citations/references, duplicate labels, fatal errors, or overfull boxes;
3. confirm every bibliography key is valid and inspect uncited entries rather than deleting automatically;
4. verify notation first-occurrence order programmatically and then visually;
5. compare quantitative claims and conclusions against the pre-edit evidence ledger;
6. inspect a contact sheet for all pages, then inspect dense pages and pages containing changed tables/equations at readable scale;
7. rebuild from the release archive in a clean directory.

A static check can be wrong because its search pattern is wrong. When a gate reports impossible positions such as all `-1`, inspect the source representation (`G_1` versus `G_{1}`) before declaring a manuscript failure.

## 9. Reporting to the author

Lead with the artifact and the scientific changes, not a long process diary. Report:

- what changed by section;
- what was deliberately preserved;
- build/page status and unresolved risks;
- the final files.

Do not claim completion until the actual PDF and source archive have been read or rebuilt. Keep progress updates short and avoid repeatedly announcing the same next step.