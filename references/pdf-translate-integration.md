# PDF Translate Integration

`academic-vi` owns language decisions. `pdf-translate` owns PDF extraction, formula placeholders, page layout, and reconstruction.

## Recommended Flow

1. Run `$pdf-translate` handoff extraction to produce source segments.
2. Inspect representative segments and establish one document profile and glossary before bulk translation.
3. Translate each `src` exactly once with `$academic-vi`, using surrounding segments for discourse context.
4. Preserve each placeholder such as `<b0></b0>` with identical identity, count, and order.
5. Write `{"src":"...","dst":"..."}` JSONL records; copy `src` byte-for-byte from extraction.
6. Rebuild with `$pdf-translate`, emit missing segments, and resolve or report every miss.
7. Verify text fidelity first, then page count, formulas, glyphs, clipping, overlap, tables, figures, citations, and URLs.

## Boundaries

- Never use the Google draft as authoritative terminology.
- Never alter a placeholder to improve Vietnamese word order; restructure text around it.
- A protected table/figure may remain untranslated due to PDF rules; report this as a partial result.
- For long papers, profile the complete abstract/introduction plus representative methods/results/discussion segments before locking the glossary.

## Prompt

```text
Use $pdf-translate in handoff mode and $academic-vi for translation.
Build one document-level glossary, preserve scientific stance and all placeholders,
audit blocking failures, then rebuild and visually verify the PDF.
```
