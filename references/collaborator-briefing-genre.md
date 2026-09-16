# Collaborator briefing genre

The genre that runs *before* drafting: convincing the person who must approve a
manuscript that the idea is worth writing. Its register is the inverse of
publication register, which is why an agent trained to produce papers produces the
wrong artifact here by default.

## Why this is a distinct genre, not a style setting

| | Manuscript | Collaborator briefing |
| --- | --- | --- |
| Reader | anonymous specialist in the field | the collaborator/supervisor deciding go/no-go |
| Background | assumed | must be built inside the artifact |
| Related work | cited | *demonstrated*, so its gap is visible |
| Weak points | bounded in Limitations | volunteered up front |
| Own tooling | invisible | role per step, including "not used yet" |
| Numbers | reported once, at final precision | shown as a table across the decision range |
| Failure mode | overclaim | reader cannot tell why they should care |

A briefing that reads as a paper abstract has failed even when every sentence is
true. The user's correction that produced this reference was, twice:

> "em chưa trình bày qua về ý tưởng đề xuất, chưa cho thấy được vai trò của em +
> [system] ở từng bước để cho kết quả"

> "trình bày rõ ràng hơn, ngôn ngữ, cách trình bày trên kiến thức cơ bản thôi, có
> thể thêm ví dụ trực quan để a nhìn rõ được các bài liên quan đã làm gì, tại sao
> em đề xuất ý tưởng đó và lí do vì sao nó đủ tốt, đủ hàm lượng khoa học"

Both arrived *after* a technically correct summary that led with theorem
statements. The defect was register and ordering, not accuracy.

## The vacuous-guarantee demonstration

The most effective motivation pattern found: take the prior framework's guarantee
and make it hold in a way that is obviously useless. It converts "there is a gap"
from an assertion into something the reader derives themselves.

Worked instance. Prior work controls the error rate among selected units for *any*
scoring function, including a bad one. Rather than asserting this is insufficient,
pose the question the reader is already forming:

> If the scorer is so bad it guesses at random, how does the promise still hold?

Then answer it: the procedure selects **nothing**. An empty output has error rate
zero, so the guarantee is satisfied. The promise holds and the pipeline is dead.

Follow immediately with measured numbers showing the whole compliant range, so the
reader sees the gap is quantitative rather than rhetorical:

| verifier quality | guarantee holds? | cost per accepted unit |
| --- | --- | --- |
| poor | yes | 825 |
| medium | yes | 29 |
| good | yes | 5.9 |

Every row is "valid" under the prior framework. The first row is worthless, and
nothing in the prior framework tells the practitioner which row they are in. That
is the contribution, and the reader has now built the argument themselves.

## Sustained analogy with an explicit mapping table

One analogy, held for the whole briefing, with a mapping table. Do not switch
vehicles between sections, and do not run two in parallel.

Requirements for a usable analogy:

1. **Every formal quantity maps to a part of it.** If a quantity has no
   counterpart, the analogy is too small — replace it rather than patching.
2. **Its failure modes are already intuitive.** The reader should be able to
   predict a result before being shown it.
3. **It is physical, not mathematical.** "Think of it as a projection" is a second
   formalism.

Publish the mapping as a table near the top:

| Formal | Analogue |
| --- | --- |
| generator | production line, outputs good and defective units |
| K validity criteria | K inspection stations |
| imperfect verifier | QC machine that misjudges |
| retention | fraction passing QC |
| cost per accepted unit | units produced per unit shipped |
| precision | fraction of shipped units genuinely good |

Then every later result can be stated twice — once in the analogy, once formally —
and the reader chooses which to read.

Analogies that carried their sections well in practice:

- **Ore assay for a ratio bound.** You cannot refine out more gold than the ore
  contains: ore at 44% and a target purity of 95% needs ≥ 95/44 = 2.14 kg of ore
  per kg of product, *however good the refinery is*. This makes an
  information-theoretic floor obvious, and it makes the corollary obvious too —
  to go below the floor you must find richer ore, not a better machine.
- **Graduated scale for a discreteness limit.** A scale marked only in 100 g steps
  cannot weigh 5 g. Maps directly onto a statistic confined to a lattice being
  compared against a finer threshold.
- **Same scale, but a tray.** The correction to the above: a coarse scale *can*
  register 25 light items placed on it together. This is the intuition for a
  step-up procedure's group behaviour, and the analogy survived the correction
  intact — a sign it was the right vehicle.

## Honest role assignment

Tabulate steps against actors, and mark unused components as unused. Assigning a
plausible role to a system that has contributed nothing is the tempting move
precisely when the user has asked "where does my system fit" — and it is the
answer that destroys trust when checked.

Say it plainly:

> To this point, [system] has participated in **no step**. The theory, code,
> tests, and tables were produced with a shell on the workstation. I am not
> inventing a role for it in the finished work.

Then find where it genuinely fits, and prefer a mechanical justification over an
enthusiastic one. Strongest available: the paper's central quantity is *calls per
accepted unit*, which is exactly what the system's cost ledger already records per
run. That makes it the **measuring instrument**, not another agent added to the
pipeline — a role that is both real and modest.

## Ranking scientific weight for a reviewer

Present the strength argument in the order a reviewer applies it:

1. **Theorem or observation?** "This is the limit, proven" outranks "we tried it
   and it was better".
2. **Quantified over all methods, or one comparison?** A bound of the form *for
   every acceptance rule* cannot be beaten by an engineering improvement. A 2%
   gain over a baseline expires in six months.
3. **Defeatable by swapping the model?** If the result uses no assumption about
   the model, "try it with a newer model" is not a valid referee request.
4. **Reproducible on a laptop?** Pure computation with a fixed seed and no
   credentials is the hardest reproducibility claim to attack, and it lets the
   theory half be submitted before the experimental half exists.
5. **Does it hand the practitioner a usable number?** An admissibility threshold
   the reader can measure their own component against is worth more than another
   table of comparisons.

## Volunteering the weak point

State it before the user finds it, and state what survives if it lands:

> The main bound's proof is one line. A reviewer may call it trivial. That risk is
> real. The mitigation is not to dress up the proof — it is that the paper does
> not rest on it alone: the finite-sample condition is the less obvious result,
> and the numerical study quantifies three effects the bound alone does not.

Volunteering this reads as competence. Having it discovered reads as either
oversight or concealment, and both cost more than the admission.

## Checklist before sending a briefing

- [ ] Prior work's mechanism shown, not merely cited
- [ ] Its insufficiency demonstrated, ideally by a vacuous-compliance case
- [ ] Proposal in one sentence, as a changed question
- [ ] Scientific weight ranked in reviewer order
- [ ] One analogy, with an explicit mapping table, held throughout
- [ ] Every claim paired with a number from a regenerating script
- [ ] Numbers shown as a table across the decision range, not one configuration
- [ ] Role table per step, with unused components marked unused
- [ ] Weakest point volunteered, with what survives it
- [ ] Exactly one decision requested at the end
