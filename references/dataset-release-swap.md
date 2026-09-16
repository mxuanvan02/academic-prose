# Dataset release swap: manuscript + repository consolidation

Condensed from the HOEIT-LegalQA case (Sep 2026): author decided the audited
subset (4,668) supersedes the pre-audit eval layer (14,210) and asked to "drop
the version label — this is the final for submission". The manuscript had
passed six review rounds on the old numbers.

## Step 1 — Classify the relation between releases

Never assume a "v2" is new data. Subset-check by item ID and verify
field-level identity on question stem, options, and gold key:

```python
v2_ids <= v1_ids per split, and
(v1[id].question, v1[id].options, v1[id].gold) == (v2[id]....) for all ids
```

Measured result: 4,668/4,668 identical → v2 is a *filtered subset*, so the
per-item model prediction ledgers from the v1 run remain valid evidence for
v2. Only the aggregation changes. If identity fails (items regenerated,
options rebalanced), the ledgers are stale and re-inference may genuinely be
required — say so before promising recomputation.

Note: option *order* rebalancing (length-rank equalisation) can coexist with
identical qa_id sets — check whether gold_letter/content per qa_id still
match, as done here (they did; balance was achieved by subsampling, not
reordering).

## Step 2 — Find the per-item ledgers before any `requires_new_study` call

Search order that worked (all outside the prose repo):
1. Grep data disks by benchmark model name (`Llama-3-8B`, `gemma_2_9b`) in
   `*.json/*.jsonl` — found `research/results/benchmarks/bench_colab_l4_<model>_{ctx,noctx}.json`.
2. Each ledger had `details: [{qa_id, gt_letter, pred_letter, is_correct, raw_output, empty_raw_output}]`
   — exactly the fields needed for accuracy, transitions, McNemar, and bootstrap.
3. The prose repo's `.gitignore` hides `research/results/` — the ledgers live
   on the working/data disk copy, not in the GitHub clone.

## Step 3 — Validate the recomputation pipeline against published numbers

Run the full stats pipeline on the OLD release first. It must reproduce every
published figure to rounding:
- accuracies 30.89/43.60 etc. matched exactly;
- Yates-corrected McNemar matched to 2 significant digits;
- cluster bootstrap CIs matched within ±0.06 pp (B=10,000, seed 42, fresh
  `random.Random(seed)` per model).

Only after this agreement did the new-release numbers become licensed. Save
the script as a citable artifact (`compute_final_stats.py`) beside the release
and print the protocol (B, seed, test definition) in its docstring.

## Step 4 — Propagate, including claims that flip polarity

Descriptive claims that were true of v1 and false of v2:
- "Bloom distribution approximately balanced" → v2 is 30.5/31.8/**37.7** (audit
  removed items non-randomly). Rewritten in abstract, Table 2, Limitations.
- Duplication stats (9 cross-split dup records, 7 near-dup pairs) → recomputed
  to 0 cross-split, 29 within-split (0.62%), 0 near-dup. The old sentence about
  "Câu hỏi thi:" prefix artifacts was deleted, not renumbered.
- Test denominator 2,172 → 688 in every table, caption, and in-text mention.
  Grep for the old numbers (`14.210|2.172|6,03–19,38`) and adjudicate each hit:
  numbers describing the *pre-audit* stage stay where the pipeline narrative
  needs them; numbers describing the *released set* must all change.

Regenerate data-derived figures in the same round. Vietnamese labels in
matplotlib: DejaVu Sans covers all VN glyphs including uppercase
(ẨỔỂỞỮỸ...) — verify with fontTools `getBestCmap()` before rendering, per the
archify lesson about missing glyphs.

## Step 5 — Repository/dataset-card consolidation

- Flatten the release: `data/{train,dev,test}.jsonl` + `scripts/` +
  `LICENSE.md`; drop "v1/v2" from card title, pretty_name, config names, and
  LICENSE headings. Superseded builds stay reproducible from the build script
  + stats, not as a competing default config.
- Run the dataset's OWN verification script on the staged files and report its
  output verbatim (here: `verify.py` → 33/33 PASS). If the script hardcodes a
  path (`SRC = "fix/v2"`), recreate that layout in a temp dir rather than
  editing the script — the point is proving the *shipped* script passes.
- Fix provenance discrepancies found while consolidating: card claimed "17
  multimodal rows", direct count said 5 (1 train + 4 test) — count from the
  data, never from an older card. Citation must carry the full author list of
  the manuscript (7 authors), not the 2–3 names in old bibtex stubs.
- README metric claims must match the manuscript protocol (cluster bootstrap,
  not "Wilson intervals" left over from an earlier design).
- Declarations block placement: check a recently published article from the
  same journal section (fetch PDF, pdftotext, search "Acknowledg") — HUJOS-TT
  puts Acknowledgement immediately before References; unnumbered
  `\section*{Lời cảm ơn}` / `\section*{Tài trợ}` / `\section*{Khai báo sử dụng
  trí tuệ nhân tạo}` matched that convention.
- Stage pushes, never auto-push: clone → edit workdir → show diff → wait for
  author approval (user rule: không push khi chưa duyệt).

## Reading a figure when vision tools are unavailable

`vision_analyze` failing (provider 503) plus no root for tesseract is not a
dead end: `uv venv /tmp/ocrenv && uv pip install --python /tmp/ocrenv/bin/python
rapidocr-onnxruntime pillow`, then run OCR **via terminal with the venv
python** (the execute_code sandbox does not see the venv). RapidOCR read the
pipeline diagram verbatim (4 stages, tool names per column) — enough to decide
the figure carried no stale numbers and could be kept. Sort detections by box
y-then-x to reconstruct reading order.
