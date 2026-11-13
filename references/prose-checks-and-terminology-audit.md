# Reviewer-phrased prose checks and terminology consistency

Two bundles a methods reviewer phrases as "writing" problems. Neither is a
style preference: both are repeatable checks, and both must be verified on the
built PDF's text layer, because a stale build hides every prose fix.

## Reviewer demand → owning reference

Eight checks that a methods reviewer phrases as "writing" problems. Each is
already owned by a reference — follow the pointer instead of restating it:

| Reviewer demand | Owner |
|---|---|
| Rename terms with the wrong professional connotation (`kiểm toán` → `rà soát`) | `references/terminology-localization.md` |
| Gloss every borrowed English term at first use | `references/academic-vietnamese-standard.md` |
| Never invent an expansion for an identifier you did not coin | `references/terminology-adjudication.md` |
| Disambiguate the task family at first use (`hỏi–đáp` vs `trắc nghiệm bốn lựa chọn`) | `references/terminology-localization.md` |
| Keywords must be field-standard, searchable terms | `references/contribution-statement-design.md` |
| Downgrade an unsupported claim in *every* section, not one | `references/veracity-protestation-gate.md` |
| One claim, one owning section — cut duplicates, do not reword them | `references/manuscript-structural-revision.md` |
| Do not let a negation drift into an opposite assertion when compressing | `references/process-logic-gate.md` |

Two things the pointers do **not** cover, and this is where the checks earn
their place: a renamed term must be swept through its whole family (`kiểm toán
viên` survives a bare `kiểm toán` replace), and every fix above must be verified
on the **built PDF's text layer** — a stale build hides all of them.

## Comparative-literature and contribution genres

Two references sit outside the manuscript pipeline and are easy to miss:

- **Literary and comparative prose** — `references/vietnamese-literary-prose.md`
  owns Vietnamese prose *about* literature: calques from English literary
  criticism, `và` chains, stating the *tertium comparationis*, hedge discipline
  in literary claims, evidence of institutional acts, and the false positives
  specific to this genre (e.g. the colon scan must be judged against a density,
  not against zero). It is not a variant of the manuscript rules — load it
  whenever the object of study is a literary work rather than a dataset.
- **Contribution statements** — `references/contribution-statement-design.md`
  owns the "ba đóng góp" paragraph: one or two sentences per contribution, a
  number plus the price paid, never claiming impossibility for the layer the
  paper then fixes, and stating where the result does *not* reach.

## Terminology consistency audit

Use after writing or revising a Vietnamese scientific manuscript when the user
asks for term consistency ("đồng nhất thuật ngữ, các cụm từ"), or when a
reviewer flags wording drift. Real failing case (a legal-QA revision round):
`thí nghiệm` vs `thực nghiệm`, `không có ngữ cảnh` vs `không ngữ cảnh`,
`mức độ nhận thức` vs `mức nhận thức`, `bản phát hành cuối cùng` vs
`bản phát hành cuối` — each appeared 1–4 times against a 6–21 count majority.

**Procedure:**
1. Enumerate candidate variant pairs from the domain glossary and from problem
   phrasing (reviewers' own words). Do not rely on a spell dictionary — the
   variants are all spelled correctly.
2. Count every variant **across the whole .tex with a script**, not by
   eyeballing. Report counts where one side is ≥2 and the other side is
   visible (≥1), and where the intended meaning is identical.
3. Fix in one direction: the majority form wins; the minority is replaced.
   Reserve exceptions for *defined* terms whose meaning is genuinely
   different (e.g. `câu trả lời đúng` inside a formula definition vs
   `đáp án đúng` as dataset field — check context before a global replace).
4. Re-scan after the fix: target = 0 for every minority form, and verify the
   majority count went UP by the removed minority count (a replace that
   silently regressed means the term was embedded in another token, e.g.
   `kiểm toán` inside `kiểm toán viên`).
5. Build the PDF and confirm the page count did not move (term-only edits
   must not change pagination; if it did, a sentence was rewritten, not a
   term swapped).

**Term pairs with known drift in Vietnamese legal/NLP manuscripts:**
`thí nghiệm / thực nghiệm` (choose thực nghiệm for evaluation-settings),
`không có ngữ cảnh / không ngữ cảnh` (choose không ngữ cảnh as the condition
label), `mức độ nhận thức / mức nhận thức` (choose mức nhận thức, Bloom's
revised taxonomy term), `bản phát hành cuối cùng / bản phát hành cuối`
(choose ngắn), `kiểm toán / rà soát` (reviewer flagged financial-audit
connotation → rà soát), `tỷ lệ / tỉ lệ`, `tự động / tư động`, `đọan / đoạn`,
truy hồi / truy hôi. Always re-measure after each pass — an edit can introduce
a NEW minority form while fixing an old one.
