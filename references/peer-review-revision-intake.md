# Peer-Review-Driven Revision Intake

Trigger: user asks to "revise bản thảo theo peer review" / revise per reviewer comments — especially when the uploaded artifact turns out to be only the manuscript.

## Rules

1. **Locate the review document before touching the manuscript.** A zip containing only `.tex`/`.pdf`/tables/figures is the manuscript, not the review. The review must exist as a separate artifact (PDF/DOCX/MD/TXT, email text, or pasted comments).
2. **Verify review↔manuscript match by title.** Similar-sounding review files from OTHER papers commonly sit in `~/.hermes/cache/documents/out_*/` and `~/reviews/`. Always compare the paper title quoted in the review against the manuscript title before treating it as the review.
   - Real trap: while revising a networking/scheduling manuscript, the newest review-pattern files on disk belonged to a *different* paper in the same venue family — matching filename pattern, completely different submission.
3. **Search order for the review:** uploaded zip contents → manuscript PDF annotations (e.g. pymupdf `page.annots()`) → recent files in `~/.hermes/cache/documents/` → `~/reviews/`, project dirs → `session_search` for past review sessions.
4. **Old self-generated feedback is not a substitute.** Internal feedback from a previous session (e.g. an LLM-run peer-review pass) may already have been incorporated into the current manuscript; re-applying it without diffing produces duplicate or no-op edits. Only reuse it if the user explicitly picks that option.
5. **If the review is not found → ask the user to send/paste it. Never reconstruct or guess reviewer comments.** (Standing user rule: thiếu bằng chứng → BLOCKED.)
6. **Once the review is in hand:** map each comment → manuscript location → proposed fix, present a severity-ordered plan for user sign-off BEFORE editing (user prefers "lên plan trước để anh chốt"), and back up to `_backups/<ts>/` before in-place edits.
