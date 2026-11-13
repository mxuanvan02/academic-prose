# Adjudicating a terminology choice the user proposes

Trigger: the user asks whether term A is better than term B in a manuscript —
"dùng từ X thì đúng hơn so với Y nhỉ?", "should this be A or B?", "nghe có ổn
không?". They are proposing a change and asking for a judgement, not ordering a
global replace.

The failure modes this protocol exists to prevent:

1. **Answering from intuition or from the model's priors.** The user does not
   accept conclusions from model memory — he expects the target venue's own
   published corpus to be queried. "I think A is more common" is not evidence.
2. **Silently global-replacing.** Vietnamese academic text almost always
   contains at least one *fixed technical term* built from the word being
   discussed. A blanket replace corrupts it, and the result is worse than the
   original inconsistency.
3. **Fixing the wrong thing.** When a manuscript uses several near-synonyms, the
   user's proposed pair is often not where the actual defect is.

## Sequence

### 1. Count every variant in the manuscript first

Grep all near-synonyms, not just the two named, and get line numbers:

```
thực nghiệm  → 6 occurrences (lines 124, 142, 169, 247, 293, 310)
thử nghiệm   → 0
thí nghiệm   → 1 (line 214)     ← the actual outlier
```

This step regularly reveals that the manuscript is already consistent in the
user's proposed pair and the real defect is a third variant nobody mentioned.
Report what was found before recommending anything.

### 2. Query the target venue's published corpus

Search the journal/conference site for each term and count published articles:

```
<venue-site> search "thực nghiệm" → 20 articles
<venue-site> search "thử nghiệm"  → 23 articles
```

Two conclusions follow, and both matter:

- **Both terms are in use at the venue** → neither is disqualifying, so the
  choice is about register and internal consistency, not compliance. Say this
  plainly; it removes a false constraint.
- Cite a real published title as an existence proof ("XÁC SUẤT LÝ THUYẾT VÀ
  XÁC SUẤT THỰC NGHIỆM TRONG SÁCH GIÁO KHOA...", published 2025-01-20).

If the venue search is unavailable or blocked, say so and fall back to
register/semantic argument — do not invent counts.

### 3. Identify fixed technical terms that block replacement

Scan occurrences for any that are part of an established term of art with a
standard translation. These cannot be changed without changing meaning:

| Surface form | Fixed term | English |
| --- | --- | --- |
| hàm phân vị **thực nghiệm** | empirical quantile function | statistics |
| nghiên cứu **thực nghiệm** | empirical / experimental research | methodology |
| **thử nghiệm** lâm sàng | clinical trial | medicine |
| **thí nghiệm** | laboratory experiment | physics/chemistry |

If even one occurrence is a fixed term, global replacement is off the table and
the manuscript must retain that word somewhere. State this as a hard constraint
with the line number, because it decides the recommendation.

### 4. Argue register, with the English gloss

Vietnamese academic near-synonyms usually map to distinct English words. Naming
the mapping settles the question:

- **thực nghiệm** = experiment / empirical — the standard term for an
  *Experiments* section in CS/ML papers, for evaluation with statistical tests.
- **thử nghiệm** = trial / testing — product trials, pilots, "chạy thử". Using it
  for a quantitative evaluation with McNemar/bootstrap is a mild register slip.
- **thí nghiệm** = laboratory experiment — physics/chemistry wet lab. Wrong for
  model evaluation, and wrong for legal-textbook data.

The genre of the manuscript decides which English word is the right target, and
that in turn decides the Vietnamese term.

### 5. Recommend, then ask — do not apply

Present: (a) what was counted, (b) the venue evidence, (c) the blocking fixed
term, (d) the recommendation with reasoning, (e) the specific edit proposed.
Then wait for the user to choose. He decides terminology; he does not want a
silent rewrite.

Offer the bounded alternative explicitly ("if you still prefer B for the
evaluation sections, I can change those 5 places and keep the fixed term") so
the decision is cheap to make either way.

### 6. After the user decides: verify consistency and rebuild

```
grep -c "<chosen>"    → N     (all occurrences)
grep -c "<rejected>"  → 0     (no variant survives)
grep -c "<third>"     → 0
```

Then rebuild and confirm the same counts in the **PDF text layer**, not just the
`.tex` source — that is where a reader will actually see it:

```bash
xelatex main.tex && xelatex main.tex
pdftotext main.pdf - | grep -c "<chosen>"
pdftotext main.pdf - | grep -c "<rejected>"   # must be 0
```

Archive the prior PDF/zip before overwriting canonical filenames, report the new
SHA256, and send both artifacts to the correct
`discord:<chat_id>:<thread_id>` target.

## Worked example

Manuscript: a Vietnamese dataset/benchmark paper for a local journal. User asks whether
*thử nghiệm* is better than *thực nghiệm*.

Findings: 6× *thực nghiệm*, 0× *thử nghiệm*, 1× *thí nghiệm* (line 214). Venue
search: 20 vs 23 published articles — both in use, so no compliance issue.
Blocking constraint: line 169 has *hàm phân vị thực nghiệm* (empirical quantile
function), a fixed statistical term. Genre: the term appears in headings
"Thiết lập thực nghiệm", "Đánh giá thực nghiệm", "Kết quả thực nghiệm" — these
are *Experiments* sections, so *thực nghiệm* is the correct register.

Recommendation: keep *thực nghiệm*, and fix the one real defect — line 214's
*thí nghiệm* → *thực nghiệm*. User approved ("ok vậy thống nhất nhé"). Result:
7× *thực nghiệm*, 0× the other two, in both source and PDF; 14 pages, 0 overfull,
TEXT MATCH between staging and package builds.
