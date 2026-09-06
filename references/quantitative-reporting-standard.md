# Quantitative Reporting Standard

A number in a manuscript is a claim, and it inherits the same evidence contract as
a sentence. This file governs how quantitative results are *reported* — what must
accompany a number for a reader to evaluate it, and which reporting forms are
blocking failures. It does not decide whether an analysis was appropriate: that
is a methodological judgment made against the design, not a rhetorical one.

The distinction matters because the most common quantitative defect in a
submitted manuscript is not a wrong calculation. It is a correct calculation
reported in a form that cannot be checked.

## The reporting contract

Every quantitative claim in publication-facing prose carries four things:

1. **The estimate** — the quantity itself, with its unit.
2. **Its denominator** — the population, sample, or set of trials it summarises.
3. **Its uncertainty** — an interval, a standard error, or an explicit statement
   that uncertainty is unquantified and why.
4. **Its comparison basis**, where the claim is comparative — what it is being
   compared against, measured under what conditions.

A number missing (1) or (2) is unusable. A number missing (3) is
`uncertainty_omitted`. A comparative claim missing (4) is
`comparison_without_basis`. None of these is repairable by softening the sentence;
each needs the missing quantity or an explicit statement that it is unavailable.

### Denominators are not interchangeable

Two counts drawn from different populations, placed adjacently, assert a relation
the author did not intend — a reader performs the subtraction. This defect appears
most often in abstracts, where compression removes the qualifying clause that the
body still contains. Name the population for each figure, or report only one.

Code `denominator_mismatch`. It is distinct from `numeric_corruption`: no number
changed, and the sentence is still false.

## Uncertainty

### Intervals

Report the interval, not only the point estimate, and state what kind it is. A
confidence interval, a credible interval, a prediction interval, and a tolerance
interval answer different questions, and the label is part of the number.

State the coverage level explicitly. "95%" is conventional, not implied.

### Small samples take the t distribution

The reflex substitution of 1.96 for the appropriate critical value is common
enough to warrant its own code. The deciding condition is **whether the
population standard deviation is known**. When σ is unknown and estimated from
the sample, the standardised mean follows Student *t* with n−1 degrees of
freedom; the normal critical value is valid only when σ is known or n is large.

The consequence is not cosmetic. A verified demonstration at n=8: the *t* critical
value 2.364624 yields empirical coverage of 94.99%, while 1.96 yields 90.92%. The
narrower interval is not more precise — it under-covers, and the paper claims a
confidence it does not have.

Code `normal_approximation_misuse`. The corollary framing error, *narrower
therefore better*, is `precision_conflation`: interval width is not precision when
coverage fails.

### When uncertainty is genuinely unavailable

Sometimes it is: a single run of an expensive experiment, a census, an artifact
count. State that uncertainty is unquantified and name the reason. This is
scholarship. Presenting the point estimate as though uncertainty were zero is not.

## Significance, effect size, and power

### Report magnitude, not only significance

With sufficient samples, negligible differences reach significance. A significance
statement without an effect size tells a reader that a difference exists, not
whether it matters. Report the effect size with its own interval, and state the
practical threshold where the field has one.

Code `significance_without_magnitude`.

### p-values

Three prohibitions, each a distinct code:

- A p-value is not the probability that the hypothesis is true, and not the
  probability the result arose by chance. Prose asserting either is
  `pvalue_misinterpretation`.
- A non-significant result is not evidence of no effect. "No difference was
  found" and "there is no difference" are different claims; the second requires
  an equivalence or non-inferiority design. Code `absence_as_equivalence`.
- A threshold crossed by a hair and a threshold crossed decisively are not
  distinguished by the word "significant". Report the value.

Trailing thresholds after the fact — selecting the test, the subgroup, or the
outcome after seeing which gives significance — is a design failure, not a
reporting one, but its trace in prose is a reporting matter: a comparison
presented as planned when it was exploratory is `exploratory_as_confirmatory`.

### Multiplicity

When many comparisons are made, some will reach significance by construction. A
manuscript reporting multiple tests states how many were performed and what, if
anything, was done about it — correction, hierarchical testing, or an explicit
declaration that the analysis is exploratory and the reported p-values are
uncorrected. Silence on the count is `multiplicity_unreported`.

Reporting only the comparisons that reached significance, without the total, is
the same defect in its most severe form.

### Power and sample size

A sample size stated without its basis is a number a reader cannot evaluate. Where
a power calculation was performed, report the assumed effect size, the power, the
alpha, and the resulting n. Where it was not — which is legitimate for
exploratory, resource-bound, or secondary-data work — say so rather than
constructing a retrospective justification.

Never invent a power calculation to justify a sample already collected. This is
`invented_sample_size`, already in the taxonomy.

## Comparative claims

### Baseline parity

A comparison is only informative if the alternative was given a fair chance. State
for every baseline: the same data, the same preprocessing, the same tuning budget,
and the same evaluation protocol. Where any of these differs, the difference is
part of the result and must be reported.

Code `baseline_parity_unstated`. An untuned baseline compared against a tuned
method is not a finding, and a reviewer checks this before anything else.

Where a baseline's published result exists, report both your reproduction and the
published figure. A reproduction below the published number, unremarked, reads as
either a weak comparison or an implementation problem — say which.

### Ablation and attribution

A claim that a component contributes requires a condition in which it is absent.
A component whose removal does not change the result is not a contribution, and
the honest move is to narrow the claim rather than retain the component in the
contribution list.

### Uniform superiority

A method that wins everywhere is under-tested, or the evaluation leaked. Report
the regions where performance degrades and the mechanism that explains them. A
paper claiming uniform superiority without a failure analysis invites the reviewer
to find the failure instead.

Code `unbounded_superiority_claim`.

## Aggregation and derived numbers

- **Report the distribution, not the best run.** Multiple seeds, then a summary
  with dispersion. A maximum presented as a typical result is
  `best_run_as_result`.
- **A derived number is introduced where it is derived.** A quantity computed for
  the abstract, appearing nowhere in the body, has no method behind it. Introduce
  it in Results with its derivation and uncertainty first.
- **Distinguish measured from estimated from modelled.** Three different evidence
  statuses that a shared table silently merges. Where a table mixes them, mark
  each row.
- **Rounding is a claim about precision.** Six decimal places on a quantity
  measured to two significant figures asserts a precision the measurement does not
  support. Report at the precision the measurement licenses, and keep it
  consistent between the text, the tables, and the abstract.

## Language-specific realisation

Number formatting is a target-language convention, not a correctness matter, and
carrying one language's convention into the other is a `CONS` failure:

- Vietnamese uses the decimal comma (`0,847`); English uses the decimal point
  (`0.847`).
- Thousands separators, percent spacing, and interval notation follow the
  declared template.
- The en dash in a numeric range, an eponym, or a negative value is notation. A
  hyphen substituted for it is `range_notation_corruption`, already blocking.

Both language versions of a bilingual manuscript report the same estimates with
the same uncertainty. A hedge or an interval present in one and absent in the
other is a `CONS` failure.

## Audit procedure

Run on every delivery containing quantitative results:

1. **Inventory.** List every number in publication-facing prose, tables, and
   figure captions.
2. **Four-part check.** For each: estimate with unit, denominator, uncertainty,
   and — where comparative — comparison basis.
3. **Abstract trace.** Every number in the abstract occurs in the body or in a
   cited versioned artifact. No number appears first in the abstract.
4. **Adjacency check.** No two figures from different denominators sit adjacently
   without their populations named.
5. **Critical-value check.** For every interval on a small sample, confirm the
   distribution used and that σ is genuinely unknown or known as claimed.
6. **Multiplicity check.** Where several comparisons appear, the total count is
   stated and the correction — or its deliberate absence — is declared.
7. **Parity check.** Every baseline's data, tuning budget, and protocol stated.
8. **Precision check.** Rounding consistent across text, tables, and abstract,
   and licensed by the measurement.
9. **Bilingual check.** Estimates, intervals, and hedges identical across language
   versions; separators follow each language's convention.
10. **Provenance check.** Where machine-verified artifacts exist, every reported
    number traces to an artifact that is observed and not stale.

Steps 5, 6, and 7 are the ones a fluent draft passes while being wrong.

## Blocking failures introduced here

- `uncertainty_omitted` — an estimate presented with no interval and no statement
  that uncertainty is unquantified.
- `denominator_mismatch` — figures from different populations presented as
  comparable.
- `normal_approximation_misuse` — a normal critical value used where the
  population standard deviation is unknown and the sample small.
- `precision_conflation` — interval width presented as precision where coverage is
  not established.
- `significance_without_magnitude` — a significance claim with no effect size.
- `pvalue_misinterpretation` — a p-value described as the probability of a
  hypothesis or of chance.
- `absence_as_equivalence` — a non-significant result reported as no effect.
- `exploratory_as_confirmatory` — a post-hoc comparison presented as planned.
- `multiplicity_unreported` — multiple comparisons without the total count or a
  declared correction policy.
- `baseline_parity_unstated` — a comparative claim without the baseline's data,
  tuning budget, and protocol.
- `unbounded_superiority_claim` — uniform superiority claimed with no failure
  region analysis.
- `best_run_as_result` — a maximum over runs presented as the result.
- `comparison_without_basis` — a comparative claim with no named comparator.

## Verification status of this file

The coverage figures for the n=8 *t* versus normal demonstration were obtained by
Monte Carlo simulation (400,000 samples) during development of this gate and are
reported as measured. Everything else here is a reporting contract derived from
the claim-integrity rules this repository already enforces; none of it is a claim
about a specific journal's statistical requirements. Reporting guidelines named
in `references/research-genre-blueprints.md` remain the authority for
design-specific checklists, and the target journal's own instructions outrank both.
