# Review-to-Revision Memo Compression

Use when an author provides a manuscript and an existing review, then asks for a concise review or revision memo to guide manuscript changes. This is an author-side synthesis task, not an independent referee report.

## Workflow

1. Read both artifacts before drafting. Build a two-column ledger: review concern → manuscript evidence/location.
2. Collapse duplicates into issue classes. Typical classes are claim/evidence scope, data and method reproducibility, quantitative validation, interpretation versus proposal, novelty/related work, and declarations.
3. Keep requests executable. Each retained item should name the manuscript action and, where data permit, the metric, table, figure, or analysis to add.
4. Separate observed evidence from proposed architecture. Do not convert a reviewer's recommendation into a manuscript result; preserve hedges around causal, AI, and biological claims.
5. Use an explicit priority rule: first changes that can invalidate the headline claim, then changes needed to reproduce or quantify the work, then presentation and end-matter repairs. End with at most three highest-impact priorities when the author must triage.
6. Draft to the requested one-page/word budget immediately. Prefer one brief assessment plus 4–6 grouped numbered actions; remove repeated rationale before shrinking typography.
7. Render and verify the actual deliverable. For a one-page Word/PDF memo, check final PDF page count and page size, not only Markdown/HTML length. If direct HTML→DOCX export fails, use HTML→ODT→DOCX, then render the final DOCX to PDF. Confirm the DOCX and PDF paths exist and are nonempty.

## Compression rules

- Preserve recommendation, evidence boundary, and all numbers that drive an action.
- Merge concerns that request the same evidence, such as event-engine implementation, alarm-flapping definition, and alert-reduction metrics.
- Replace explanatory paragraphs with a single reason followed by an executable request.
- Do not add literature, data, or validation results that were not supplied.
- If the review and manuscript disagree on a fact, flag it for author verification rather than silently choosing one.

## Common failure modes

- Producing a full referee report when the author asked for a revision aid.
- Leaving 20–25 duplicated concerns as separate bullets.
- Claiming “one page” from word count alone without measuring the rendered PDF.
- Repeatedly changing content after a layout failure instead of controlling the document style and rechecking the final artifact.
- Delivering a PDF that passed page-count validation while the requested DOCX was never actually created.
