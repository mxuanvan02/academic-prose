# Dataset release swap: manuscript + repository consolidation

Condensed from a measured case: author decided the audited
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
  output verbatim (here: `verify.py` → 33/33 PASS). Two stages: while
  *pre-shipping*, if the script hardcodes a path (`SRC = "fix/v2"`), recreate
  that layout in a temp dir rather than editing it — the point is proving the
  *shipped* script passes. Then, before the final push, **de-hardcode it**
  (accept a path argument, default to the released `data/` layout) so
  downstream users can actually run it, and re-run to confirm the same pass
  count on the shipped version.
- Fix provenance discrepancies found while consolidating: card claimed "17
  multimodal rows", direct count said 5 (1 train + 4 test) — count from the
  data, never from an older card. Citation must carry the full author list of
  the manuscript (7 authors), not the 2–3 names in old bibtex stubs.
- README metric claims must match the manuscript protocol (cluster bootstrap,
  not "Wilson intervals" left over from an earlier design).
- Declarations block placement: check a recently published article from the
  same journal section (fetch PDF, pdftotext, search "Acknowledg") — measured on an
  puts Acknowledgement immediately before References; unnumbered
  `\section*{Lời cảm ơn}` / `\section*{Tài trợ}` / `\section*{Khai báo sử dụng
  trí tuệ nhân tạo}` matched that convention.
- Stage pushes, never auto-push: clone → edit workdir → show diff → wait for
  author approval (user rule: không push khi chưa duyệt).

## Pushing a layout consolidation to Hugging Face atomically

A version-label drop means deleting the old tree and adding the new one **in
one commit**, so the repo never sits in a half-migrated state where both
layouts coexist. `huggingface_hub` does this with mixed operations:

```python
import os; os.environ['HF_TOKEN'] = Path('~/.cache/huggingface/token').expanduser().read_text().strip()
from huggingface_hub import HfApi
from huggingface_hub.hf_api import CommitOperationAdd, CommitOperationDelete
api = HfApi()  # picks up HF_TOKEN from env; do NOT pass token=*** inline
# 1. enumerate current remote files
import json, urllib.request
H={'Authorization':f'Bearer {os.environ['HF_TOKEN']}'}
d=json.loads(urllib.request.urlopen(urllib.request.Request(
  'https://huggingface.co/api/datasets/<repo>?full=true',headers=H),timeout=60).read())
remote={f['rfilename'] for f in d['siblings']}
keep={'.gitattributes','README.md'}            # README is overwritten, not deleted
deletes=[CommitOperationDelete(path_in_repo=f) for f in sorted(remote-keep)]
uploads=[CommitOperationAdd(path_in_repo=str(p.relative_to(STAGING)), path_or_fileobj=p)
         for p in STAGING.rglob('*') if p.is_file()]
api.create_commit(repo_id='<repo>', repo_type='dataset',
                  commit_message='...', operations=deletes+uploads)
```

Measured: 114 operations (98 delete + 16 add) in one commit, ~9 s. `commit()`
does not exist on this version — use `create_commit()`. Two pitfalls hit live:
(a) the execute_code sandbox redacts a bare `token=*** into a syntax error, so
read the token into `os.environ['HF_TOKEN']` and let `HfApi()` pick it up;
(b) `create_commit` needs `path_or_fileobj` as a Path, and files with spaces or
Vietnamese in the name work fine unquoted.

## Post-push verification when the repo is private

`datasets-server.huggingface.co/{splits,size,first-rows}` returns **501** for
private datasets ("only supported for PRO users / Enterprise Hub") — so the
standard "did the config actually parse" probe is unavailable. Verify three
ways instead, all of which work on a private repo with the token:

1. **File list ≡ staged tree.** Re-fetch `?full=true`, assert
   `set(remote) == staged_files | {'.gitattributes'}`. Catches a silently
   dropped or extra file.
2. **Byte-level hash equality.** For each data file + card + scripts, GET
   `.../resolve/main/<path>` (URL-quote the path) and compare
   `sha256(remote_bytes) == sha256(staged_bytes)`. Hashes must be computed on
   bytes, not re-encoded text (`.md` round-trips through `read_text` change
   nothing here but binary `.jsonl` would).
3. **Card frontmatter resolves against the remote.** Fetch
   `.../raw/main/README.md`, parse the YAML `configs[].data_files`, and assert
   each declared `path` exists in the remote file set. This is the manual
   stand-in for the 501'd splits API — it proves the default config points at
   files that are actually there.

Then sweep the live card text for leftover version labels (`v1`, `v2_audited`,
`build_v2`, `verify_v2`, ` v2 `) — expect 0 hits each. A follow-up card
correction (e.g. narrowing an overclaiming script description) is its own
single-file `create_commit`, re-verified the same way.

## Making the dataset repo public, with anonymous verification

Visibility change is an explicit, irreversible author decision — only do it on a
direct instruction ("đổi HF sang public luôn nhé"), never inferred. The
`huggingface_hub` Python method name for this varies by version (an
`update_repo_visibility` call raised `AttributeError` on hub 1.25.1), so the
robust path is the REST settings endpoint, which is version-independent:

```python
url = 'https://huggingface.co/api/datasets/<repo>/settings'
req = urllib.request.Request(url, data=json.dumps({'private': False}).encode(),
    method='PUT', headers={'Authorization': f'Bearer {tok}',
                           'Content-Type': 'application/json'})
# -> 200 {"private": false}
```

**Verify public the way an outsider would — with NO token.** A token'd request
proves nothing about public access. Two anonymous probes:
1. `GET https://huggingface.co/api/datasets/<repo>` with only a `User-Agent`
   header → body must show `"private": false`.
2. `GET .../resolve/main/data/test.jsonl` with a `Range: bytes=0-200` header and
   no auth → must return real file bytes. This is the proof a reviewer can
   actually download without credentials.

Only after both pass, tell the author the repo is public and that it cannot be
privated-and-forgotten (URLs may be cached/indexed).

## GitHub branch consolidation before "clean the repo"

When the author asks to handle open PRs and "clean" a repo, do not trust a
local `git merge-base` / `git rev-list --count` if the working clone was made
with `--depth` — a shallow clone reports bogus merge-bases (it returned an empty
base and "behind 0" for branches that the GitHub API showed 41 ahead / 0
behind). The authoritative source is the compare API:

```bash
gh api repos/<owner>/<repo>/compare/<base>...<head> \
   --jq '{status, ahead_by, behind_by}'   # status:"ahead", behind_by:0 => head is a superset
gh api repos/<owner>/<repo>/pulls/<N>/files --paginate \
   --jq '.[] | select(.status=="removed") | .filename'   # exactly what the merge deletes
```

Decision rule: `behind_by == 0` means the head branch contains all of base's
history, so merging loses no code. Then read the removed-file list before
merging — here it was only `cloudflared` + `cloudflared.log` (a tunnel binary and
its log that should never have been committed), which is a cleanup, not a loss.
Report both facts to the author rather than just "merged". Merge with
`gh pr merge <N> --merge`; afterward `behind_by:1` on base...head is just the
merge commit and is expected.

## Code-only LICENSE for a repo that ships restricted data

A pipeline repo whose *data* is restricted still wants an open *code* license.
Ship `LICENSE` as MIT but scope it explicitly, in both languages, so the MIT
grant cannot be read as covering the corpus: state that it covers the code and
does **not** cover source textbooks, page images, or verbatim excerpts, which
follow the dataset's own license (link it). Mirror the same split in a README
"Giấy phép" section. This keeps the repo a legitimate open artifact without
implying redistribution rights the data does not have.

## Data-availability statement in the manuscript

Once the artifacts are public, add an unnumbered `\section*{Tính sẵn có của dữ
liệu và mã nguồn}` in the declarations block — placed after Funding and before
the AI-disclosure, matching that journal's declarations ordering. It carries the
two canonical links (HF dataset, GitHub repo) plus one clause each on what is
reproducible there (audit/verify/recompute scripts) and the license scope (MIT
for code, not the corpus). Use `\url{}` (hyperref is already loaded); after the
build, `pdftotext` the PDF and assert both link strings and the heading are
present in the rendered text — a `\url` that silently breaks in a float or a
missing package shows up only there. This is transparency the author asked for,
not boilerplate: it is what lets a reviewer reach the exact release the numbers
came from.

## Reading a figure when vision tools are unavailable

`vision_analyze` failing (provider 503) plus no root for tesseract is not a
dead end: `uv venv /tmp/ocrenv && uv pip install --python /tmp/ocrenv/bin/python
rapidocr-onnxruntime pillow`, then run OCR **via terminal with the venv
python** (the execute_code sandbox does not see the venv). RapidOCR read the
pipeline diagram verbatim (4 stages, tool names per column) — enough to decide
the figure carried no stale numbers and could be kept. Sort detections by box
y-then-x to reconstruct reading order.
