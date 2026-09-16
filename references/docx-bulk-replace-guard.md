# DOCX Bulk-Replace Guard

Measured failures from HOEIT-LegalQA round-6 DOCX edit (6.6 MB, 85 paras, 4 tables).
Global `str.replace` produced three classes of regression; guard before applying bulk edits.

## 1. Language- and zone-scoped terminology

- Vietnamese prose `metadata` → `siêu dữ liệu`/`thông tin nguồn` must not touch:
  - English Abstract (`source metadata supporting traceability` is the defined term)
  - Document-level metadata fields
- Second pass must not re-translate its own output: `source` → `source` on an already-translated paragraph produced `source thông tin nguồn`.
- Guard: filter paragraphs by detected language (`[a-z]{3,}` density vs Vietnamese diacritics) and by `w:lang`/heading style (`Abstract`, `Keywords`). Only apply VI replacements to VI-zoned `w:p`.

## 2. Caption renumbering is a cross-reference edit

- Renumbering `Bảng 1a → Bảng 1`, then shifting `Bảng 1→2`, `Bảng 2→3`, `Bảng 3→4` without patching in-text `Bảng 2 báo cáo ...; Bảng 3 báo cáo ...` leaves dangling refs.
- The `Ghi chú Bảng 2: ...` paragraph was detached — originally para 89 at document end, must move to immediately after its target table (`Table 2` at idx 75). Verify by paragraph index, not visual adjacency in Word.
- Guard: build `caption_para_idx` and `reference_para_idx` maps; after any caption edit, patch all `Bảng X` and `Hình X` mentions and relocate `Ghi chú Bảng X` to `target_tbl_idx + 1`.

## 3. Split-count reconciliation

- Section prose states `411 trượt mạch lạc, 335 trượt bám, 204 trượt cả hai = 542`; table stated `544 có điểm, 2 thiếu` → total 546 mismatch by 4.
- Fix must present one consistent total: `Loại 546; 542 có đủ điểm chấm (411 + 335 − 204), 4 thiếu điểm tổng hợp`.
- Guard: before writing a summary table cell that decomposes a total, recompute `total = a + b − overlap + missing` and assert equality with the text's stated total.

## 4. Double-prefix artifact

- `phiên bản checkpoint` with prefix insertion produced `phiên bản phiên bản checkpoint`.
- Guard: replace by regex with negative lookbehind `(?<!phiên bản )checkpoint` or operate on raw `checkpoint` token only.

## Verification protocol

After any bulk replacement on DOCX:
1. Read back via `scripts/docx_accepted_view.py` (not `Paragraph.text`) — tables are invisible to the latter.
2. Assert: no remaining source terms in target zone, no remaining old caption numbers, `Ghi chú Bảng X` immediately follows `Bảng X`, and table split arithmetic matches prose.
3. Check for doubled prefixes via `phiên bản phiên bản|source thông tin`.

References: `academic-prose/SKILL.md` § DOCX manuscript revision and delivery gate.
