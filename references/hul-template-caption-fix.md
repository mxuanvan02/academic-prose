# HUL Template Decoy and Caption Orphan Fix

Session: HOEIT-LegalQA round 6 -> HUL journal reframe (2026-09-14).
User correction: submitted DOCX used the wrong template; `Hình`/`Bảng`
captions stood alone.

## 1. Template decoy (HUL `hul_journal_assets/`)

Same folder held two `.docx` files; filename alone misled:

| File | Size | Role | Evidence |
| --- | --- | --- | --- |
| `template.docx` | 12K, 21 paras, 3 tables | author-declaration form only (`Phiếu khai báo`) | styles: bare `normal`; no manuscript body |
| `ban_thao_TQA_nganh_luat_theo_the_le.docx` | 30K, 135 paras (298 w/ tables), 7 tables | real manuscript frame | A4 `11906x16838`, margins `1417/1134/1134/1134`, styles `Heading1/2/3, FirstParagraph, BodyText, Compact, Bibliography`, `word/footnotes.xml` with 6 footnotes |

Rule: decide the frame by `pgSz` + `pgMar` + style set + `footnotes.xml`
presence, never by filename. Copy `sectPr` and the style set from the
proven frame into the draft.

## 2. Citation regime mismatch

Draft used bracket citations `[1]-[17]`; `citation.pdf` in the same folder
mandates **Chicago Notes-Bibliography 18th** (footnotes + end bibliography,
no `ibid`/`sđd`, DOI/URL required). Bracket list passing content gates is
still a venue-format block. Ask the author before bulk-converting: footnotes
vs. keep brackets as provisional.

## 3. Orphan captions

Measured on 8 captions (Hình 1-4, Bảng 1-4): `keepNext=True` alone did not
hold caption to its table/figure; the HUL frame itself had
`keepNext=False keepLines=False` on caption paras. Fix as one block:

- caption para: `keepNext=true + keepLines=true + widowControl=true`
- following table/image para: `keepLines=true`
- verify by body-order walk: caption index immediately precedes its
  table/image element (e.g. caption idx 46 -> table idx 47)

## 4. Drifting figures

4 PNGs present in `word/media/` but raw `w:drawing` count was 0: they rode
legacy `w:pict`/`v:shape` nodes. Re-embed as `wp:inline` with a real `a:blip`
embed id so each figure stays with its caption.

## 5. Checklist before calling it submission-ready

1. `pgSz`/`pgMar` match the proven frame.
2. Full style remap applied (no `Normal`-only body).
3. Caption keep-together block verified by index walk.
4. Figures re-embedded inline with blip ids.
5. Footnote/bibliography regime confirmed with the author.
6. LibreOffice PDF render + 4 academic-prose gates re-run.
