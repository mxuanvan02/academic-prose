# Bibliography reconstruction from in-text citations

Use when a manuscript cites `[1]–[22]` (or any range) but ships no `Tài liệu tham khảo / References` section, or when numbering is discontinuous.

## 1. Extract true citation set from OOXML, not the dump

- Parse `word/document.xml` for bracket tokens `\[...\]`; expand ranges (`[1–5]`, `[10–12]`) and splits (`[6,7]`).
- Exclude false positives like `[Q(0,025), Q(0,975)]` (formula quantiles, not citations).
- Measured case (HOEIT round 6): raw max was 22 but distinct set was `[1-12,18-22]` — `[13-17]` never cited. Missing numbers are a finding, not a renumbering license until confirmed.

## 2. Verify each candidate before writing prose

- Search-first, then take DOI from result, then re-resolve via Crossref and compare title/author/year/venue.
- Keep a private ledger: `verified` (Crossref match) vs `inferred` (no match / arXiv-only / report).
- Never invent a reference to fill a gap. If `[13-17]` have zero in-text hits across XML + rendered PDF, they are absent — not "to be guessed".

## 3. Repair discontinuous numbering by remap, not placeholders

- Do NOT ship `[13] [Không trích dẫn — giữ chỗ]` placeholders to "preserve numbering".
- Delete unused entries, renumber bibliography continuously (`18→13, 19→14, 20→15, 21→16, 22→17` in measured case).
- Remap every in-text occurrence including ranges: `[18]`→`[13]`, `[19]`→`[14]`, `[20,21]`→`[15,16]`, `[22]`→`[17]`.
- Assert after remap: `missing in-text not in bib == []`, `bib not cited == []`, old numbers still present `== 0`.

## 4. Keep verification language out of the artifact

- Trailing `— Verified` / `— Verified via Crossref` / `— Inferred placeholder` in reference paragraphs triggers `verification_log_prose` in `scripts/internal_register_scan.py --genre manuscript` (measured: 17 hits, gate fail despite otherwise clean scans).
- Ship clean entries: authors, title, venue, year, DOI only. Keep verified/inferred status in a separate audit note or chat summary, never in DOCX prose.
- Re-run all four gates after cleaning: `internal_register_scan`, `process_logic_scan`, `vi_ai_pattern_scan`, `academic_discourse_scan` must all be `scan_clean` / 0 candidates.

## 5. Delivery checklist for DOCX

- Insert `6 Tài liệu tham khảo` as a numbered heading paragraph after Kết luận, then one paragraph per `[n]` entry.
- Produce clean + tracked copies from the same source; tracked copy must enable `w:trackRevisions`.
- Office smoke: LibreOffice convert to PDF in a clean dir, confirm page count delta is only the added bibliography (measured: 9→10 pages), and cross-copy accepted text matches.
