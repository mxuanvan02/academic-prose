# Evidence-bound full-manuscript audit

When the author asks to reread the whole manuscript and fix similar problems, do not stop after repairing the quoted sentence or the abstract. Sweep the entire source, including both abstracts, title/keywords, headings, captions, tables, Methods, Results, Limitations, Future Work, Conclusion, and references as protected citation zones.

Use this order:

1. **Read for meaning before word substitution.** For every paragraph, identify its subject, main predicate, evidence, and rhetorical job. Rewrite sentences that lack a determinate actor or relation; do not merely translate individual English tokens.
2. **Build a terminology ledger.** For each technical term, classify it as a proper name/model/tool, an established Vietnamese concept, or an implementation detail. Keep proper names; translate established concepts; translate implementation details unless reproducibility requires them. First use may retain the original in parentheses, but later prose should use the Vietnamese rendering consistently.
3. **Separate publication prose from pipeline notes.** Replace schema/configuration language such as `manifest`, `seed`, `checkpoint`, `prompt`, `environment`, `metadata`, and `benchmark` with reader-facing terms (`bản kê dữ liệu`, `hạt giống ngẫu nhiên`, `phiên bản mô hình`, `câu lệnh sinh`, `môi trường thực thi`, `thông tin nguồn`, `bộ chuẩn đánh giá`) unless the identifier itself is necessary for reproducibility.
4. **Compress by section ownership.** Abstract states gap, aim, contribution, principal finding, and one validity boundary; it must not become a log of every count, failed record, or QA check. Results owns detailed counts and tables; Methods owns procedures; Limitations owns threats to interpretation; Future Work owns unresolved research questions rather than task lists.
5. **Propagate every substantive edit.** If a body claim is shortened, weakened, or newly bounded, check the title, both abstracts, introduction, contribution statement, Results, Conclusion, captions, and English counterpart for stale or stronger wording.
6. **Build only after prose stabilizes.** A successful XeLaTeX build verifies syntax and references, not Vietnamese meaning. Run the prose scans, then compile twice, inspect overfull boxes, table widths, page count, and extracted PDF text. A remaining overfull box or unresolved English phrase is not a reason to declare the manuscript final.

For this workflow, avoid repeated progress announcements. Report the actual audit result, remaining blockers, and the next concrete artifact only after the whole-document pass.
**The author's rhetorical brief overrides the default abstract progression.** If the author asks for a very short prospective abstract that “only says what the work will do,” write only the aim, planned method, and evaluation scope, normally in about 60–90 words; omit results, p-values, findings, interpretation, and validity caveats. Do not re-expand it merely to satisfy the full progression below. When the request also says “add a Vietnamese version” while discussing the abstract, provide a bilingual abstract—not a translation of the whole manuscript—unless full-document translation is explicitly requested. Count each language independently and preserve future orientation and claim strength across versions.

An abstract is not a results digest, and Limitations are not its closing move. When
an abstract reads as a list of counts that terminates in caveats, the reviewer
cannot state what the paper set out to do — and that absence propagates: the
introduction, the research questions, and the contribution list inherit the same
directionlessness. Diagnose this at the paper level, not the sentence level.

Required abstract progression, in this order:

1. **Gap** — one sentence on what the field lacks, scoped to the target venue's readership.
2. **Aim** — one sentence naming what this paper builds, measures, or establishes.
3. **Contributions** — enumerated, each carrying the mechanism that makes it a contribution rather than an activity. "A four-stage pipeline" is an activity; "a four-stage pipeline whose reference-anchoring step makes every item traceable to its source provision" is a contribution.
4. **Principal finding** — including the result with reach beyond this dataset, if there is one.
5. **Validity boundary** — one sentence. Not two, not a closing paragraph.

Structural checks that travel with it:

- **Research questions map one-to-one onto contributions.** An RQ that yields no
  contribution is a framing defect: it signals the paper is describing its own
  process rather than answering something. An RQ of the form "what limitations
  must be stated?" is the usual offender — it produces a Limitations section, not
  a finding. Recast it as an empirical question whose answer *is* the contribution.
- **Counts in the abstract carry their denominator.** Two figures from different
  denominators placed side by side read as a subtraction the author did not intend.
  Name the population for each, or drop one.
- **Rank findings by reach.** When one result is method-general and another is
  dataset-specific, the abstract and conclusion should say which is which.
- Enforce the venue's word cap on both language versions independently and report
  the measured count, never the estimated one.
- **Compress to the cap in text space, not in build space.** Recount with a word
  counter after every edit and rebuild only once the count is inside the cap.
  Rewriting an abstract to sharpen its aim reliably *adds* words even when the
  intent is to cut: one measured sequence ran 302 → 283 → 270 → 264 → 258 →
  **266** → 256 → 254 → 244, so two of eight passes moved the wrong way and each
  cost a full multi-pass LaTeX + BibTeX cycle for nothing.
- When the source draft is far over cap (478 words against a 250 cap), tell the
  user that more than half their text was removed and that the abstract is the
  section most needing their review. A silent 50% cut of an author's own words is
  not a formatting change.

### Conclusion progression: close the loop on the stated objectives

The conclusion answers *were the objectives met*, not *what were the numbers*.
Author correction, and it generalizes: *"ban đầu đặt ra những mục tiêu gì thì kết
lại chứ... anh đọc qua thì giống như nói lại các con số, bị lệch trọng tâm nội
dung cần truyền tải."*

Required progression, in order:

1. **Restate the objectives** in the framing the introduction used — same count,
   same wording family (three RQs → three objectives).
2. **State whether they were met**, bounded by the design's reach ("ở mức độ cho
   phép của thiết kế"), as one clause per objective or one covering sentence.
3. **Name the transferable lesson** a reader building something similar should
   keep (e.g. a deterministic audit must follow model-based generation; a single
   aggregate metric does not describe model behaviour).
4. **Bound the resource's status** in one sentence, forward-referencing the
   limitations section instead of restating it.

Blocking check: **no measurement values in the conclusion body.** Counts,
accuracies, percentage-point ranges and interval bounds belong to Results. The
conclusion may name *which* quantity was measured ("ngữ cảnh nguồn đúng gắn với
cải thiện độ chính xác ổn định ở cả bốn mô hình") but never its value. Verify
mechanically — extract the conclusion span from the built PDF text and assert the
only numeric token is the page number in the footer.

This mirrors the abstract rule in the opposite direction: the abstract carries the
principal finding *with* its number; the conclusion carries the finding's meaning
*without* one.
