# LaTeX Pre-Submission Verification Recipes

Measured on the HOEIT-LegalQA HUJOS submission (XeLaTeX + polyglossia Vietnamese,
article class). Five reusable gates that caught real defects after all four prose
scans reported clean.

## 1. Prose-extract before paragraph-level scans on LaTeX sources

`academic_discourse_scan.py` run on raw `.tex` reports `clause_overload`
candidates that are pure markup: preamble `\usepackage` chains, `tabular` rows
(`&`-separated cells), `center` title blocks. Measured: 7 candidates, all false
positives; none was author prose.

Adjudication rule: if the quoted "sentence" contains `\usepackage`, `\begin{...}`,
`&`, or `\\` sequences, classify as markup false positive — do not "split" it.

Recipe (strip preamble, floats, tables, bibliography, then commands):

```python
import re
tex = open('main.tex', encoding='utf-8').read()
body = tex.split(r'\begin{document}',1)[1].split(r'\end{document}',1)[0]
for env in ['table','figure','tabularx','tabular','center']:
    body = re.sub(r'\\begin\{'+env+r'\}.*?\\end\{'+env+r'\}', ' ', body, flags=re.S)
body = re.sub(r'\\begin\{thebibliography\}.*?\\end\{thebibliography\}', ' ', body, flags=re.S)
body = re.sub(r'\\[a-zA-Z]+\*?(\[[^\]]*\])?(\{[^{}]*\})?', ' ', body)
body = re.sub(r'[{}$~%]', ' ', body)
body = re.sub(r'&|\\\\', '\n', body)
open('prose_only.txt','w').write(re.sub(r'[ \t]+', ' ', body))
```

Scan `prose_only.txt` for paragraph-level gates; keep sentence-level gates
(vi_ai_pattern, internal_register, process_logic) on the `.tex` directly — they
tolerate markup and must still see captions.

## 2. Bibliography heading render check (`\refname` trap)

With polyglossia Vietnamese + article class, `thebibliography` can render a
truncated/wrong heading — measured: "Tài liệu" instead of "Tài liệu tham khảo".
Source inspection shows nothing wrong; the defect only appears in the built PDF.

- Verify by `pdftotext main.pdf` and assert the full heading string appears
  immediately before `[1]`. A naive `"References" in text` check silently fails.
- Fix: `\renewcommand{\refname}{Tài liệu tham khảo}` before
  `\begin{thebibliography}` (use `\bibname` for book/report classes).

This extends the citation-bibliography integrity check in SKILL.md §6: presence
of `\bibitem`s is necessary but not sufficient — the rendered heading is part
of the gate.

## 3. Declarations placement from a published article, not from a style guess

To place Lời cảm ơn / Tài trợ / Khai báo sử dụng AI (acknowledgement / funding /
generative-AI disclosure): download one recent published article PDF from the
same journal section and read where its declarations sit relative to References.

OJS galley recipe: `…/issue/current` → collect `article/view/<id>` links →
fetch `article/view/<id>/<galleyId>` (returns the PDF). Measured HUJOS-TT:
Acknowledgement (with grant code) sits immediately before References.

Vietnamese triad that shipped (unnumbered `\section*`, after Kết luận, before
`\renewcommand{\refname}` + bibliography):

- **Lời cảm ơn** — institution that provided environment + data (name the data:
  "48 tệp PDF giáo trình luật").
- **Tài trợ** — "Nghiên cứu này được tài trợ bởi <funder>, mã số <code>."
- **Khai báo sử dụng trí tuệ nhân tạo** — what AI was used for (grammar support
  in writing, code generation), plus author-responsibility clause. Never draft
  content the authors did not confirm; ask for the exact uses and grant code.

## 4. Per-record dataset-claim verification against the released artifact

When the manuscript characterizes a released dataset ("bộ dữ liệu trắc nghiệm",
"phân bố gần đồng đều", "chia theo giáo trình nguồn"), do not trust README stats
or summary files — download every split and scan **every record**.

HF download: `https://huggingface.co/datasets/<user>/<name>/resolve/main/<path>`
with `Authorization: Bearer <token from ~/.cache/huggingface/token>` for private
datasets. Per-record invariants for an MCQ release:

1. options field is a list of exactly 4;
2. question text non-empty (find the real field name first — `question_content`,
   not `question`; a schema-key dump of one record prevents thousands of false
   alarms from a wrong field guess);
3. options distinct after strip;
4. `gold_index` in 0–3, `gold_letter == 'ABCD'[gold_index]`,
   `ground_truth == options[gold_index]`;
5. aggregate counts (splits, Bloom/label distribution, answer-position balance,
   multimodal count, distinct source docs) reconciled against every manuscript
   table they appear in.

Measured: 14,210/14,210 v1 records passed all invariants; aggregates matched the
manuscript tables exactly (Bloom 4,784/4,711/4,715; splits 9,894/2,144/2,172;
positions A–D 3,544/3,564/3,557/3,545; 48 docs; 29 multimodal). That per-record
evidence is what licenses keeping the word "trắc nghiệm" in the title/abstract.

## 5. Manuscript ↔ GitHub README ↔ HF card drift sweep

A dataset paper has three public surfaces that drift independently. Sweep all
three before submission; measured drift classes:

- **Citation blocks**: three different author lists/titles across GH bibtex,
  HF card "Citation" section, and the manuscript title block. Unify to the
  manuscript (author-confirmed) version.
- **Model version names**: README `Vintern-1B-v3` vs config/manuscript
  `Vintern-1B-v3.5`. The implementation (config.py) adjudicates.
- **Statistics methods**: README "Wilson 95% CI" vs manuscript cluster
  bootstrap; only one describes the reported numbers.
- **Version relation**: HF card says "v2 supersedes v1, do not benchmark on v1"
  while the manuscript reports v1 numbers. The card must state explicitly which
  release the paper's figures come from, or readers/reviewers see a
  contradiction.
- **Broken relative links**: markdown referencing files not in the repo
  (`research/EXECUTION_RUNBOOK.md` etc.). Test every relative path.

Standing rule (this author): prepare fixes, present the diff, **never push
without explicit approval** — on both GitHub and HF.
