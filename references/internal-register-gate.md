# Internal Register Gate

A manuscript says what is known about the world. An internal register says what
happened to the manuscript, to the project, or to the author while producing it.
The second is prohibited in publication-facing prose, and it is prohibited
absolutely: it is not a style preference that a good reason can override.

The prohibition needs a mechanism rather than a warning, because every one of
these defects passes every automated check a project normally runs. The text
compiles, resolves its citations, stays inside its page and word caps, contains
no fabricated number, and reads fluently. A reviewer sees it on the first page.

This gate operates in four modes, and all four are mandatory:

| Mode | When | Output |
| --- | --- | --- |
| `write` | before and during drafting | an admissible subject declared per paragraph |
| `check` | before every delivery | scan report + gate verdict |
| `read` | auditing a text you did not write | findings, no silent rewriting |
| `sweep` | after any hit is found anywhere | whole-document, all sections, both language versions |

## 1. What counts as internal register

Six classes. They have one cause — the draft was written next to the work
instead of next to the reader — and they need different repairs.

| Class | Code | The sentence is about | Example tell |
| --- | --- | --- | --- |
| self-address | `self_reminder_prose` | what the author must remember to write | `cần nêu rõ`, `cần thận trọng`, *it should be noted that* |
| document metadiscourse | `document_as_subject` | the paper, its sections, its own order | `phần này sẽ trình bày`, `như đã đề cập ở trên` |
| project bookkeeping | `progress_state_limitation` | the state of the team's work | `chưa kịp`, `sẽ bổ sung sau`, `đang trong quá trình` |
| operational log | `operational_log_prose`, `verification_log_prose` | files, runs, checks, tallies | `đã kiểm tra`, `checksum khớp`, `0 lỗi`, `đã biên dịch lại` |
| internal artifact | `internal_artifact_reference` | a path on the author's machine, a working filename, a ticket, a commit hash, a sheet column | `/Users/…`, `main.tex`, `v9_final`, `commit b4f0a2d`, `#123` |
| repository artifact | `repo_artifact_reference` | a script or data filename inside the project repository | `scripts/anchored_judge.py`, `all_judged_post_repair_v3.jsonl` |
| production residue | `assistant_residue`, `placeholder_residue`, `revision_response_leak` | the conversation or the revision that produced the text | `theo yêu cầu của anh`, `TODO`, `như phản biện đã chỉ ra` |

`defensive_disclaimer_stack` is the seventh member and the only one with no
lexical signature: each of its sentences is licensed alone, and the defect is
their density.

## 2. Three tests, applied to every candidate sentence

The tests are ordered. The first that returns a verdict decides. They are
deliberately mechanical: a criterion an author can argue with is a criterion that
never fires.

**Test 1 — Referent.** Identify the semantic subject. Admissible subjects are:
the object of study; the data; the method; a result; a cited work's claim; an
inference available to the reader. Inadmissible subjects are: this manuscript,
its sections, the act of writing, the project, the team, a file, a tool run, or
the conversation that produced the text. An inadmissible subject fails unless a
genre slot in §4 licenses it.

**Test 2 — Permanence.** Two probes:

- *Work probe.* Suppose the team does more work next week and the scientific
  finding is unchanged. Does the sentence change? If yes, it is bookkeeping.
- *Format probe.* Suppose the text is re-typeset, renumbered, or absorbed into a
  chapter. Does the sentence break? If yes, it is layout-dependent metadiscourse.
  A resolved cross-reference (`Bảng 2 cho thấy`) does not break, because the
  number is resolved for the reader. `ở đoạn trên` breaks.

**Test 3 — Outsider verifiability.** Can a reader holding only the published
artifact parse and check the sentence? If verification requires the repository,
the chat log, the spreadsheet, or the reviewer letter, the sentence is internal
even when every word of it is true.

## 3. Four verdicts, and the one that is forbidden

| Verdict | Use when | Operation |
| --- | --- | --- |
| `delete` | the sentence carries no claim once the self-address is removed | remove it; confirm no scope was lost |
| `recast` | it carries a claim in the wrong register | change the **subject** to an admissible one and state the bound it licenses |
| `relocate` | the content is needed for audit but not for argument | move to data card, appendix, repository record, or response letter; keep every number a reader needs |
| `license` | a genre slot in §4 permits it and the quota is unused | keep unchanged, count against the quota |

The forbidden operation is **soften**. Adding a hedge, a passive, or a
qualification to an internal sentence leaves it internal and now also vague.
`Có lẽ cần nêu rõ rằng…` is worse than the original. The repair changes what the
sentence is about, never how strongly it says it.

Recast preserves scope. Deleting `cần được diễn giải thận trọng` and stopping
there produces an overclaim in the opposite direction; the caution it carried
must reappear as a stated boundary. This is the same trap as `hedge_loss`.

Worked repairs:

| Internal | Recast |
| --- | --- |
| Một giới hạn cần nêu thẳng: nhãn chưa được thẩm định. | Nhãn chưa có đối chiếu của chuyên gia, nên độ tin cậy của nhãn không định lượng được. |
| Phần này sẽ trình bày quy trình xây dựng dữ liệu. | *(delete; the section heading already says it)* |
| Nhóm chưa kịp bổ sung phân tầng theo lĩnh vực. | Dữ liệu không phân tầng theo lĩnh vực, nên không thể phân tích hiệu năng theo từng lĩnh vực. |
| Chúng tôi đã kiểm tra và không phát hiện trùng lặp định danh. | Tập bản ghi có định danh duy nhất, điều kiện cần để các tỷ lệ ở Mục 4 không bị đếm trùng; kiểm tra này không bảo đảm nội dung không trùng lặp. |
| Kết quả trong tệp `ket_qua_v9.csv` cho thấy… | Kết quả cho thấy… *(số liệu giữ nguyên, tên tệp chuyển vào tuyên bố dữ liệu)* |
| Theo góp ý của phản biện, chúng tôi đã bổ sung Bảng 3. | *(delete from the manuscript; the point belongs in the response letter)* |

## 4. Licensed slots and false positives

A detector that fires on these destroys correct academic writing. Each is
permitted, and most carry a quota.

- **One roadmap passage per manuscript**, in the Introduction, naming what each
  section establishes. A second roadmap anywhere else is `document_as_subject`.
- **Resolved cross-references** to numbered objects: `Bảng 2`, `Hình 4`,
  `Mục 3.1`, `Phụ lục A`. Unlimited.
- **`Trong nghiên cứu này`** as a framing move, when content follows immediately
  rather than a promise of content.
- **`Chúng tôi` in Methods**, including for a single author where the venue
  permits it. Standard Vietnamese academic usage.
- **Genre-mandated sections**: Limitations, Future Work, Ethics and intended use,
  Data availability, Reproducibility, Acknowledgements. The section is required;
  its sentences still take an admissible subject. A limitation whose subject is
  the inference is correct; one whose subject is the project is not.
- **Vietnamese thesis and grant slots**: `Tính cấp thiết của đề tài`,
  `Ý nghĩa khoa học và thực tiễn`, `Kết luận và kiến nghị`. Repair weak content;
  never delete the slot.
- **Named artifacts in a data or reproducibility statement**: repository URL, DOI,
  dataset name, tool with version. These are `keep_source` designators under
  [Terminology localization policy](terminology-localization.md), not internal
  leakage. A path on the author's machine is leakage; a public identifier is not.
- **Response-to-reviewers letters and revision notes**: the genre *is* licensed
  self-narration. `revision_response_leak` fires only when that register appears
  in the manuscript.
- **Teaching material and speaker notes**: `Ở phần sau chúng ta sẽ…` is spoken
  discourse structure, not manuscript metadiscourse. Declare the genre.

## 5. Quantitative thresholds

A gate needs numbers, otherwise it is advice.

| Check | Threshold |
| --- | --- |
| self-address occurrences | 0 |
| assistant/chat residue | 0, blocking |
| placeholder residue (`TODO`, `TBD`, `[…]`, `???`) | 0, blocking |
| machine-local path, working filename, ticket, commit hash, or column name | 0, blocking |
| repository script or data filename in body prose | 0 outside a data/reproducibility statement; revision-level, not blocking |
| document-as-subject sentences | ≤ 1 per section, and ≤ 1 roadmap passage per document |
| verification-log sentences in Methods/Results body | 0; permitted in an integrity subsection only when paired with the property the check does **not** establish |
| project-state sentences in Limitations or Future Work | 0 |
| negation-of-claim markers (`chỉ`, `không phải`, `không chứng minh`, `không bảo đảm`, `không hàm ý`) | ≤ 2 within any 3 consecutive sentences |
| divergence between language versions after repair | 0 |

`SEM` cannot score 4 while a blocking class is present. `VOICE` cannot score 4
while any self-address remains. `CONS` cannot score 4 while one language version
was cleaned and the other was not.

## 6. Write mode: prevent instead of detect

The defect enters at drafting, so the cheapest control is upstream.

1. In the paragraph plan, record an **admissible subject** for each paragraph
   alongside its rhetorical function. A paragraph whose planned subject is the
   document, the project, or a file is rejected at the plan stage.
2. Draft from the claim ledger, not from the build log, the audit sheet, or the
   task tracker. When an artifact must be consulted, extract the number and close
   the artifact before writing the sentence.
3. Never carry an outline's imperative into prose. Outline entries are written as
   instructions (`nêu giới hạn về nhãn`); the prose realizes the instruction and
   discards it.
4. Write Limitations from the inference backwards: name the conclusion that
   weakens, then the mechanism that weakens it. Never from the task list forward.
5. Write Future Work as open questions with a feasible design, never as work the
   team owes.

## 7. Check mode: the scan

Run [`scripts/internal_register_scan.py`](../scripts/internal_register_scan.py)
on the manuscript source before every delivery.

```bash
python3 scripts/internal_register_scan.py main.tex --genre manuscript --report report.md
python3 scripts/internal_register_scan.py draft.docx --genre thesis --json findings.json
python3 scripts/internal_register_scan.py notes.md --genre response_letter
```

The scanner strips protected zones (math, verbatim, comments, citation and label
arguments, bibliography), segments sentences, applies the class patterns, and
evaluates the density thresholds. Exit code `1` means a blocking class is
present; `2` means revision-level findings only; `0` means clean.

Two properties of the scanner matter more than its pattern list:

- **A lexical hit is a candidate, not a verdict.** Every hit is resolved by the
  three tests in §2. The scanner reports; the author decides and records the
  verdict.
- **Absence of hits is not a pass.** Class `document_as_subject` and
  `progress_state_limitation` have paraphrases no pattern catches. The scan
  raises the floor; the manual pass over Methods, Limitations, Future Work, and
  every integrity subsection is still required.

Report the two numbers separately: hits the scanner found, and sites the manual
pass found. A scan-only clean report is a partial verification and must be
labelled as one.

The verification suite is [`scripts/test_internal_register_scan.py`](../scripts/test_internal_register_scan.py)
with fixtures under `scripts/fixtures/`. Each test names the criterion it checks,
so a failure points at a rule here rather than at a regex. Run it after any
pattern change; a detector nobody tests silently decays into either noise or
blindness.

### Calibration: three false positives that cost real edits

Every one of these was found by running the scan on four real manuscripts, not on
the fixtures. A detector tuned only on its own examples measures nothing.

1. **`không chỉ … mà còn` is an intensifier, not a denial.** It produced five
   spurious `defensive_disclaimer_stack` hits in one paper's Discussion. A
   negation marker followed by a correlative continuation is excluded.
2. **A LaTeX preamble is not prose.** `\newif`, `\InputIfFileExists{…}`, and
   package options tripped the artifact patterns. Scan only between
   `\begin{document}` and `\end{document}` when the marker is present.
3. **A repository filename is not a machine-local path.** `scripts/foo.py` in a
   reproducibility statement is a legitimate public identifier; `/Users/van/…`
   never is. Splitting these into two classes moved one manuscript from a false
   `block` to a correct revision-level finding, and left the genuine blocker (a
   bare commit hash in body prose) intact.

The general rule these share: **severity follows what the reader can reach.** A
public repository path is reachable and belongs in a data statement; a path on
one machine, a chat turn, and a placeholder are unreachable and block.

### Bilingual symmetry is part of the gate, not an extension of it

The class inventory above was built from Vietnamese examples. Run against English
prose carrying all ten defects, it reported **7 of 10** and a clean threshold table:
`progress_state_limitation`, `verification_log_prose`, and
`defensive_disclaimer_stack` had no English markers at all. Nothing in the output
announced that English was unchecked — the gate simply passed.

Every class therefore needs markers in both languages, a fixture in both languages,
and a test asserting the same class set on both. The English markers that were
missing:

| Class | English markers |
| --- | --- |
| `progress_state_limitation` | *has/have not yet been completed / validated / annotated*, *will be added later*, *is still in progress / underway / pending* |
| `verification_log_prose` | *we checked / verified / confirmed / reran / compiled*, *the checksum matched*, *zero errors*, *no errors were found*, *passed all checks* |
| `defensive_disclaimer_stack` | *do/does not prove / guarantee / imply / establish*, *cannot guarantee*, *only establish(es) / show(s) / reflect(s) / applies to* |

Two traps in the denial stack specifically:

- **Person agreement.** The first pattern carried only `does not prove`, so a genuine
  three-sentence stack containing `They do not prove Y` counted two markers and stayed
  under threshold. The class appeared absent rather than under-detected.
- **`not only … but also` must be excluded exactly as `không chỉ … mà còn` is.** It is
  an intensifier; without the exclusion an emphatic Discussion paragraph is graded as
  self-defence.

When a marker does not fire, print the matcher's output sentence by sentence before
editing the pattern. Guessing at the regex cost two revisions; one diagnostic print
located the cause immediately.

## 8. Read mode: auditing a text you did not write

Report; do not rewrite. For each finding give the span, the class, the failing
test, and the proposed verdict — and where the verdict is `recast`, propose the
admissible subject rather than a finished sentence, since the author owns the
claim. Distinguish a finding from a preference: if a sentence passes all three
tests and you merely dislike it, it is not a finding.

When the text is a translation or a bilingual pair, audit both versions. An
internal sentence removed from one version and left in the other is a `CONS`
failure, and the usual direction of the error is that the language the author
drafted in got cleaned and the other did not.

## 9. Sweep mode: one hit means many

A register leak is never confined to one sentence. It appears wherever the draft
touched the same source, because each of those places inherited that source's
unit of analysis. One measured sweep found **eight sites** from a single
user-reported sentence: Limitations, two Methods subsections, an integrity
subsection, and the Conclusion.

When any hit is confirmed, sweep before replying:

1. Every section, including the abstract, keywords, captions, table notes,
   acknowledgements, and data statements.
2. Both language versions.
3. Every summary section against the section it compresses — a summary inherits
   the body's register silently.
4. The exporter or template, if the artifact is generated. An internal string
   that survives removal from the source is hardcoded downstream; see
   `generated_artifact_drift`.

Expect the sweep to surface substantive findings, not only register ones.
Rewriting an operational Methods paragraph forces a reading of the actual
implementation, which is where undocumented stages and mislabelled figures
appear. Register cleanup and evidence verification are one pass.

## 10. Codes and severity

Blocking: `assistant_residue`, `placeholder_residue`,
`internal_artifact_reference`.

Revision on every occurrence: `self_reminder_prose`, `document_as_subject`,
`progress_state_limitation`, `operational_log_prose`, `verification_log_prose`,
`revision_response_leak`, `defensive_disclaimer_stack`.

The three blocking classes are blocking because they are unarguable: no reader of
a published article can act on a path from the author's machine, a placeholder, or
a sentence addressed to whoever helped write the draft. The rest are judgments
that a competent author can defend in a specific case, which is why they require
a recorded verdict rather than an automatic edit.

See [Writing failure taxonomy](writing-failure-taxonomy.md) for the full table,
[Self-narration and config dump](self-narration-and-config-dump.md) for the
self-address and config-dump substitution tables,
[Artifact register to scientific register](artifact-register-to-scientific-register.md)
for the eight-site defect table and the future-work rewrite pattern, and the
internal register gate in [Quality rubric](quality-rubric.md).
