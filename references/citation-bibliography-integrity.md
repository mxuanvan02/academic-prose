# Citation–Bibliography Integrity

Session: HOEIT-LegalQA round 6 (2026-09-14) — doc_60e477135d35_HOEIT-LegalQA_revised_round6_clean.docx

## Failure observed
4 prose gates clean (internal_register 349 sents, process_logic 334, vi_ai 311, academic_discourse 69 paras) yet manuscript had **15 bracket-citation groups** (`[1–5]`, `[6,7]`, `[8,9]`, `[1]..[22]`) and **no §6 Tài liệu tham khảo / References** section. LibreOffice PDF 9 pages rendered without bibliography — submission blocker missed by prose scans.

## Why scans miss it
- `internal_register_scan`, `process_logic_scan`, `vi_ai_pattern_scan`, `academic_discourse_scan` check register/logic/style, not citation resolution.
- `has_TLTK` / `has References` flag must be checked separately.

## Recipe (use docx_accepted_text.py)
1. Dump accepted text: `python3 ~/.hermes/skills/academic-prose/scripts/docx_accepted_text.py --dump <docx> | head -n 200`
2. Extract citations: regex `\[\d+[–\-\d,]*\]` over accepted text; collect unique groups, count total.
3. Check bibliography: search accepted text for headings `Tài liệu tham khảo` / `References` / `Bibliography` (tab-prefixed `\t6\t` form in this template). `has_TLTK == False` is blocker if `cites_total > 0`.
4. Verify coverage: max cited number (here 22) vs entries present. Report `cites_total`, `has_TLTK`, `max_cite`.
5. Office smoke: `libreoffice --headless --convert-to pdf` then `zip_test None` + `paras/tables/media` counts to confirm not corrupt.

## Fix policy
- Never invent bibliography entries to satisfy count. Gate is `submission-integrity` → placeholder or author source required.
- Options offered to author: (a) provide `.bib` / list to insert, (b) insert placeholder `6. Tài liệu tham khảo — [CẦN BỔ SUNG]` with `[n] — cần bổ sung` lines to keep citations resolvable.
- Re-run smoke + cross-copy check after insertion.

## Pitfall to embed
A "clean 4-gate" report is not submission-ready. Always run citation-bibliography check as gate 5 before claiming ready-to-submit, especially for DOCX manuscripts with numeric bracket citations.

## LaTeX variant — the heading can render broken while the source looks fine
Session 2026-09-16, HOEIT HUJOS XeLaTeX build (`polyglossia`, vietnamese default, `article` class): all 17 `\bibitem`s present, citations [1]–[17] resolved, zero build warnings — yet `pdftotext` showed the bibliography heading truncated to `Tài liệu` immediately followed by `[1] Kembhavi…`. The rendered artifact, not the source, carried the defect; both prose scans and a source grep passed.

Rules:
1. Verify the bibliography heading on **pdftotext of the built PDF**, not by grepping the `.tex`: search for the full string `Tài liệu tham khảo` (or `References`) and confirm the first `[1]` entry does not directly abut a partial heading.
2. Fix for `article`: `\renewcommand{\refname}{Tài liệu tham khảo}` immediately before `\begin{thebibliography}`. (`\bibname` applies to `book`/`report` classes.)
3. Rebuild twice, then re-verify heading text **and** full citation range `[1..N]` in the rendered text before calling the build final.

## Pointer in SKILL.md
Section "Evidence-Bound Revision" item 6 now references this file.
