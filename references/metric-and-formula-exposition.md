# Metric and formula exposition

Companion to the `Define Every Metric and Formula Before Its First Use` section of
SKILL.md. Use when a manuscript reports metrics, statistics, thresholds, or any
mathematical expression.

## The three-part pattern, per quantity

Write each definition as **concept → formula → boundary**, in that order, in
continuous prose with the formula on its own centred line. Never a label-colon
list, never a symbol glossary table.

```
<one sentence: what the quantity measures, in domain words>
        <formula, display line>
<one sentence: what each symbol counts, especially the denominator>
<one clause: what the quantity does not establish>
```

Budget roughly 2–4 sentences per quantity. A definition subsection covering six
statistics fits in about one page; if it runs longer, the prose is explaining the
derivation rather than the meaning.

## Worked bank of boundary clauses

These are the interpretive limits that reviewers actually check. Attach them at
the definition site, not in Limitations.

| Quantity | Formula | Boundary clause that must accompany it |
| --- | --- | --- |
| Accuracy | `Acc = c / n` | State whether `n` includes items with no parseable answer; report the count of valid answers separately so the real denominator per run is visible. |
| Difference in percentage points | `Δ = 100 × (Acc_a − Acc_b)` | A difference of k points from a low baseline and from a high baseline share the same subtraction but differ in relative change; say which is reported. |
| McNemar with continuity correction | `χ² = (\|b − c\| − 1)² / (b + c)`, 1 df | Define the 2×2 cells first; explain that the concordant cells carry no information about the difference; the `−1` is the Yates correction and makes p conservative at small `b + c`; a small p does not give the probability of the hypothesis. |
| Exact binomial on the discordant cells | `p = 2 P(X ≥ max(b, c))`, `X ~ B(b + c; 0.5)` | Reported alongside χ² to show the conclusion does not depend on the approximation. |
| Cluster bootstrap interval | `CI 95% = [Q(0.025), Q(0.975)]` over `B` resamples | Name the resampling **unit** (the cluster, not the item) and why items are dependent; an interval excluding zero fixes the direction of the effect under within-cluster dependence, and is not a statement about effect magnitude outside the evaluated set. |
| Jaccard over word shingles | `J(A,B) = \|A ∩ B\| / \|A ∪ B\|` | Define a shingle as every window of k consecutive words; give `J = 1` and `J = 0` in words; the threshold is a screening convention, so the pair count depends on shingle length and threshold and both belong in the caption. |
| Pass rate | survivors ÷ inputs | Measures the filter's selectivity, not the quality of what survived. |
| Label-output share | items choosing a label ÷ items evaluated | Independent of correctness, therefore identifies no mechanism for a skew. |
| Exact-duplicate rate | records in any group of size ≥ 2 ÷ total records | The counting unit decides the number: a key occurring twice contributes two records, not one. This is why a within-split record count and a cross-split key count are not comparable figures. |

## Placement verification

Rendered reading order is not evidence, and a caption can use a metric before the
body does. Verify by index in the source document:

1. Extract ordered body paragraph texts (see `scripts/docx_accepted_text.py` for
   DOCX; it walks the body in document order and includes table cells).
2. Record the index of the definition heading.
3. Record the index of the **first** occurrence of each metric name, symbol, and
   table caption that uses it.
4. Assert `definition_index < min(first_use_indices)` and fail the build otherwise.

Two traps in that check:

- Heading paragraphs commonly carry a leading numbering tab, so the accepted text
  reads `\t3.7\tTitle`. `startswith('3.7')` fails; strip before comparing.
- Table captions live in ordinary paragraphs but the numbers they describe live in
  table cells. A parity or first-use scan over `document.paragraphs` alone misses
  the cells entirely.

## Retrofit sequence

When the definitions are added to a manuscript that already reports the results:

1. Insert the definition subsection **without adding any empirical number**. Every
   figure stays where it already is.
2. Sweep the Results prose for sentences that were carrying an implicit
   definition, and delete the duplication rather than leaving both.
3. Re-check summary sections in both languages. An abstract that previously said a
   statistic was unavailable becomes false once the body reports it; that stale
   clause is a claim-integrity failure, not a leftover.
4. Re-measure page count and venue caps. A definition subsection adds roughly one
   page; if that breaks a verified cap, report the overage and ask rather than
   deleting definitions or evidence to fit.
