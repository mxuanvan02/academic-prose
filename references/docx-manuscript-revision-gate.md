# DOCX manuscript revision and delivery gate

Use this reference when revising a manuscript directly in `.docx`, especially when both a clean copy and a Track Changes copy are required.

## 1. Treat DOCX structure as evidence, not appearance

DOCX is untrusted OOXML. Parse `word/document.xml` with `defusedxml`, never the standard XML parser. A visually obvious heading may still use paragraph style `Normal`; common manuscripts encode headings as numbered text whose text-bearing runs are all directly bold.

Recover logical section context using both signals:

1. `Heading1`–`Heading6` paragraph styles;
2. numbered paragraphs (`1`, `3.2`, `4.1.2`, etc.) whose non-empty text runs are all bold.

Convert recovered headings to logical Markdown-style boundaries before section-aware prose scans. Do not classify an ordinary numbered body sentence as a heading unless the formatting signal is also present.

Some declarations begin with an inline bold-like label rather than a separate heading, for example `Mã nguồn và dữ liệu.`. A scanner that licenses repository identifiers only in data/reproducibility sections may need this label promoted to a logical section boundary while preserving the paragraph remainder.

Regression coverage must include: styled heading, bold numbered heading on `Normal`, unbold numbered body text, promoted inline declaration label, malformed/untrusted DOCX handling, and CLI execution on DOCX rather than only direct function calls.

### Three silent text-extraction traps

Each of these produces plausible output that fails an assertion several steps
later, so budget for them before writing any verification code. Use
[`scripts/docx_accepted_text.py`](../scripts/docx_accepted_text.py), which handles
all three, rather than re-deriving the walk.

1. **`paragraph.text` is empty for tracked insertions.** Text inside `<w:ins>` is
   invisible to `python-docx`'s convenience accessor, so a newly inserted
   paragraph reads as `''` in the tracked copy while being correct in the clean
   copy. Any content assertion must run over an *accepted view* that keeps
   `<w:ins>` and drops `<w:del>` — otherwise the clean copy passes and the tracked
   copy fails for a reason that looks like a build bug.
2. **A tab is `<w:tab/>`, not `w:t` text.** Concatenating only `w:t` nodes turns
   the heading `\t3.7\tTitle` into `3.7Title`, so `startswith('4\t')` silently
   matches nothing and a `next(...)` generator raises `StopIteration` with no
   message. Headings also carry a *leading* numbering tab, so strip before
   comparing prefixes.
3. **`document.paragraphs` skips table cells.** A numeric-parity or
   first-use scan over paragraphs alone misses every figure that lives in a table.
   Walk `document.element.body` in order and flatten `w:tbl` rows.

A fourth, positional: **inserting a caption plus a table after an anchor requires
reverse insertion order.** Repeated `anchor.addnext(x)` places each element
immediately after the anchor, so the last call ends up first. Insert
spacer → table → caption to obtain caption → table → spacer. Also re-derive table
indices after insertion; a new table shifts `document.tables[i]` for everything
after it.

## 2. Separate scientific evidence limits from progress logs

A statement such as `nhãn Bloom được gán tự động và chưa được thẩm định độc lập` describes the status of the evidence. It is a scientific limitation and must not be classified as project-progress narration merely because it contains `chưa` or `not yet`.

Progress-state findings require an operational or future-completion cue, such as `chưa kịp`, `chưa hoàn tất`, `sẽ bổ sung sau`, `still in progress`, or `remains to be done`. Avoid broad patterns such as `has not been validated` that also match legitimate evidence boundaries.

When an academic-discourse scanner flags a limitation paragraph, adjudicate it manually against four questions:

1. What is the paragraph's rhetorical job?
2. What positive or bounded claim does it establish before stating the limit?
3. Does each limitation change interpretation, scope, or reproducibility?
4. Can repeated caveats be consolidated without deleting a scientific boundary?

Rewrite deficit-centred prose as finding or scope first, then one consequence-bearing boundary. Do not invent expert validation, cluster-aware uncertainty, McNemar details, deduplication results, or release evidence merely to obtain a clean scan.

## 3. Repository identifiers require public, section-specific context

A commit hash is licensed only when all of the following hold:

- the same relevant passage identifies a public repository URL;
- the passage occurs in a data, code-availability, artifact, appendix, or reproducibility context;
- the identifier supports an externally inspectable scientific artifact.

A bare commit in Methods, a local path, or an identifier without a public repository remains a finding. If the same commit appears once as unsupported Methods prose and once in a proper `Mã nguồn và dữ liệu` declaration, remove or recast the former rather than weakening the scanner. Do not call a repository or dataset a verified public release without confirmed access, licensing, and a stable tag/release/version.

## 4. Produce clean and tracked documents from the same verified source

Apply one replacement map to both outputs so their accepted text is identical.

For the clean copy:

- replace paragraph content without revision markup;
- assert that `word/document.xml` contains no `w:ins` or `w:del`;
- preserve paragraph properties, run formatting where possible, tables, images, relationships, and section settings.

For the tracked copy:

- retain deleted runs under `w:del` and inserted text under `w:ins`;
- set author/date/revision IDs consistently;
- enable `w:trackRevisions` in settings;
- remember that deleted text remains searchable in OOXML by design, so forbidden-string checks must distinguish clean from tracked output.

Do not regenerate from an older source after the author has hand-edited a document. Diff or back-port those edits first.

## 5. Completion requires a delivery gate

Creating the DOCX files is not completion. Before describing them as final or submission-ready, run all applicable checks:

1. **Package integrity:** ZIP test; required OOXML parts exist and parse safely.
2. **Document invariants:** expected paragraphs/tables/media; clean copy has no revision markup; tracked copy has insertions, deletions, and revision tracking enabled.
3. **Content gates:** rerun internal-register, process-logic, Vietnamese AI-pattern, and academic-discourse scans on the new clean DOCX; manually classify remaining candidates.
4. **Mutation/regression checks:** run targeted tests, integrated validator, and mutation checks after scanner changes.
5. **Office smoke test:** open or convert with LibreOffice in a clean output directory and check for repair warnings or conversion failure.
6. **Rendered verification:** inspect page count and representative rendered pages, especially headings, tables, page breaks, references, and the declaration section.
7. **Cross-copy consistency:** compare accepted text between the clean copy and the tracked copy after excluding deleted text.

If tool limits interrupt the process after file creation, report the files as provisional and list the unrun gates. Do not say the revision is complete and then announce validation as a future step.

## 6. Efficient debugging and status reporting

When a patch reports `old_string and new_string are identical`, multiple matches, or no matching hunk, stop retrying the same aggregate patch. Inspect exact symbols and nearby context, construct an `already present / missing` table, and apply small unique replacements. After each successful edit batch, run the narrowest relevant tests before the full validator.

Keep progress updates distinct and concise. Do not repeatedly announce the same next action; either execute it in that turn or state the concrete blocker.

## 7. Reading a revised DOCX back: four API traps that produce false failures

Section 5 requires verifying the **accepted view**. The traps below are how that
verification fails while the document is actually correct. All four were measured
in one delivery round; each cost a build-validate cycle.

### 7.1 `paragraph.text` drops text inside `w:ins`

`python-docx` builds `Paragraph.text` from direct `w:r` children. Runs wrapped in
`<w:ins>` are **not** direct children, so a tracked copy reports empty or
truncated paragraph text even though the insertion is present and correct. The
same applies to `_Cell.text` for table cells whose runs were marked inserted.

Symptom: the clean copy passes every needle assertion and the tracked copy fails
the identical assertion.

Fix: read the accepted view by walking `w:t` nodes and skipping any node with a
`w:del` ancestor (keep `w:ins` content, drop `w:del` content, ignore `w:delText`
entirely). Run
[`scripts/docx_accepted_view.py`](../scripts/docx_accepted_view.py) rather than
re-implementing this per project; it also does forbidden-string checks and
bilingual number parity.

Do **not** "fix" this by asserting against raw `word/document.xml`. Superseded
prose legitimately survives inside `w:del`, so a raw-XML substring check cannot
distinguish accepted text from deleted text — that is the failure section 5 warns
about, arrived at from the opposite direction.

### 7.2 `document.paragraphs` excludes table cell text

A bilingual parity check failed on the number `9` because it lived only in a
status table. `document.paragraphs` walks paragraphs, not tables, so every count,
verdict, or claim placed in a table is invisible to it.

Fix: iterate `body` children in document order and handle `w:p` and `w:tbl`
separately. This matters most for parity checks (numbers, hedges, verdicts) and
for word counts, where a table-only figure silently disappears from one language
half of the comparison.

### 7.3 Table indices shift after insertion

Inserting a table changes the index of every table after it, and a new table
appended near the end may not be the index you assumed. An assertion written as
`document.tables[2]` broke once the new table landed at `tables[3]`.

Fix: assert on shape **and** header content, not position alone. Locate the new
table by its header row text, then check its dimensions and body rows against the
values that generated it.

### 7.4 `addnext` insertions must be issued in reverse

`element.addnext(x)` places `x` immediately after `element`. Chaining
`anchor.addnext(a); a.addnext(b)` is fragile once the elements are being deep-copied,
and produced caption/table/spacer in the wrong order.

Fix: issue every insertion against the **same anchor in reverse of the desired
final order**. For the sequence `anchor, caption, table, spacer`, call
`anchor.addnext(spacer)`, then `anchor.addnext(table)`, then
`anchor.addnext(caption)`.

Related: when a caption paragraph is deep-copied as the template for a new
caption, strip everything except `w:pPr` before appending the new run, or the old
caption text survives underneath the new one.

### 7.5 Verify the insertion in the rendered PDF, not the paragraph count

A newly inserted table and caption can pass every structural assertion and still
straddle a page boundary. After inserting, render both copies, locate the caption
by page, and confirm every cell value appears on that page. In the measured round
the new table added exactly one page (15 → 16 clean, 17 → 18 tracked); a page
delta larger than the inserted content is a layout defect, not a page count.