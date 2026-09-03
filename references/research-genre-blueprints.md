# Research Genre Blueprints

Structural blueprints for empirical, computational, and engineering research
writing. Use this file to choose a section order **before** drafting. Move
identifiers are defined in [Rhetorical Move Registry](rhetorical-moves.md);
generic section moves are in [Genre Playbooks](genre-playbooks.md); legal
scholarship has its own logics in [Legal Research Genres](legal-research-genres.md).

A blueprint is a move set, not a mandatory template. Select the blueprint whose
evidence logic matches the study, then adapt to the target venue's author
guidelines. When a venue mandates a section order, the venue wins.

## Why The Blueprint Must Match The Evidence Logic

IMRAD is the dominant order for original empirical research, and its adoption is
documented rather than assumed (Oriokot et al. 2011, `10.1186/1756-0500-4-250`).
It encodes one specific logic: a question is posed, a procedure is executed,
observations are reported, and only then interpreted.

That logic fails when the study produces something other than observations. A
design-science paper produces an artefact and its evaluation. A systematic review
produces a synthesis over retrieved records. A simulation study produces
behaviour of a model under controlled scenarios, not measurements of the world.
Forcing IMRAD onto these yields an empty `Results` section or, worse, an
interpretation smuggled into `Results`.

Two invariants hold across every blueprint below:

1. **`Results` reports; `Discussion` interprets.** A causal explanation, a
   comparison to prior work, or a recommendation placed inside `Results` is a
   genre failure, not a stylistic preference.
2. **Every quantitative claim carries its denominator and its uncertainty.**
   `8/33 sources` is reportable; `many studies` is not. A point estimate without
   a spread, interval, or seed count is incomplete.

A useful discipline for the whole paper: each section should advance one claim,
and the paper should read as a single argument rather than a chronological lab
diary (Mensh & Kording 2017, `10.1371/journal.pcbi.1005619`).

## Selecting A Blueprint

Answer in order. Stop at the first match.

1. Does the paper synthesise *other studies* rather than generate new
   observations? -> **Systematic review** or **Systematic mapping**.
2. Does it evaluate an *artefact the authors built* (method, system, tool,
   architecture)? -> **Design science / engineering contribution**.
3. Are the observations produced by a *model executed under scenarios* rather
   than measured from the world? -> **Simulation study**.
4. Did the authors *assign* conditions to units? -> **Controlled experiment**.
5. Did the authors *observe without assigning*? -> **Observational study**.
6. Does the paper deliver a *predictive or diagnostic model* to be used on new
   cases? -> **Prediction model study**.
7. Is the paper a *protocol* for work not yet executed? -> **Protocol**.

If two apply, the paper likely contains two studies. Declare them as Study 1 and
Study 2 with separate method and result units rather than blending them.

## Systematic Review And Evidence Synthesis

Section order: Introduction -> Objectives and review questions -> Methods
(eligibility criteria, information sources, search strategy, selection process,
data collection, data items, risk-of-bias assessment, synthesis method) ->
Results (selection flow, study characteristics, risk of bias, synthesis results,
certainty of evidence) -> Discussion -> Conclusion.

The reporting checklist is PRISMA 2020 (Page et al. 2021, `10.1136/bmj.n71`).
Three obligations are routinely skipped and routinely flagged in review:

- **Report the selection flow with numbers at every stage**, including records
  identified, deduplicated, screened, excluded with reasons, sought for
  retrieval, not retrieved, and finally included. Records whose full text was
  never obtained belong to *reports not retrieved*, which sits **before**
  *reports assessed for eligibility*. Such a record cannot be counted as an
  included study.
- **State the synthesis method before showing the synthesis.** When effect
  measures are not commensurable, meta-analysis is not available; report the
  structured alternative and say so explicitly, following SWiM (Campbell et al.
  2020, `10.1136/bmj.l6890`).
- **Rate certainty separately from risk of bias.** Risk of bias describes
  individual studies; certainty describes the body of evidence for each outcome
  (Guyatt et al. 2008, `10.1136/bmj.39489.470347.AD`).

Denominator discipline is the most common failure mode. When the corpus is
tiered, every proportion must name its tier. `8/33 core-tier sources` and
`54/64 title-level records` are different populations; presenting the shift
between them as a reduction on one set is a claim error.

For software and computing venues, the review procedure is usually specified as
a systematic literature review (Kitchenham et al. 2009,
`10.1016/j.infsof.2008.09.009`). A **systematic mapping study** is a distinct
genre: it charts the distribution of research over a classification scheme
rather than answering a narrow effect question, and its results are category
frequencies plus a bubble or matrix map (Petersen et al. 2015,
`10.1016/j.infsof.2015.03.007`). Do not label a mapping study a systematic
review; the reader will expect synthesised effects that the design cannot
deliver.

## Design Science And Engineering Contribution

Section order: Introduction -> Problem relevance and requirements -> Related
work and gap -> Design objectives -> Artefact design (architecture, algorithm,
data model, interfaces) -> Demonstration -> Evaluation (criteria, baselines,
setup, metrics, results) -> Discussion of trade-offs and threats -> Conclusion
and further work.

The genre is defined by two paired obligations: an artefact must be built, and
its utility must be evaluated against stated criteria (Hevner et al. 2004,
`10.2307/25148625`). The procedural form usually cited is the six-activity
research methodology of problem identification, objectives, design and
development, demonstration, evaluation, and communication (Peffers et al. 2007,
`10.2753/MIS0742-1222240302`).

Keep the **design problem** and the **knowledge question** apart. "How should
this scheduler be built to meet these constraints?" is a design problem;
"does this scheduling policy reduce transmission count under packet loss?" is a
knowledge question. The engineering cycle treats them as different activities
with different validity criteria (Wieringa 2014, `10.1007/978-3-662-43839-8`).
A paper that answers only the design problem must not claim empirical superiority.

Evaluation obligations, in order of how often they are missing:

- Name the **baseline** and justify it. A comparison against no baseline supports
  the claim "the system runs", not "the system is better".
- State the **metric and its direction** before reporting numbers, and keep one
  stable definition throughout.
- Separate **demonstration** from **evaluation**. A worked example shows the
  artefact functions; it is not evidence of utility.
- Report **threats to validity** as a named section, not as a hedge sprinkled
  through Discussion.

## Simulation Study

Section order: Introduction -> Aims and research questions -> Model (conceptual
model, assumptions, governing equations, parameters and their provenance) ->
Experimental design (scenarios, factors, levels, comparators, replication and
seeding, run length, warm-up) -> Performance measures and estimands -> Results
per scenario -> Discussion (mechanism-level interpretation, limits of external
validity) -> Conclusion.

Two reporting frames apply depending on the field. For discrete-event and
operational simulation, report the model, its data sources, the experimental
setup, and the code and parameter availability (Monks et al. 2019,
`10.1080/17477778.2018.1442155`). For simulation studies that evaluate methods
or estimators, state aims, data-generating mechanisms, estimands, methods,
performance measures, and the number of repetitions with a rationale (Morris et
al. 2019, `10.1002/sim.8086`).

The claim boundary is the defining constraint of this genre. A simulation
provides **mechanism-level evidence under stated assumptions**. It is not causal
evidence about the world, not a field validation, and not a safety assessment.
State that boundary in the abstract and again in Discussion; a reviewer who has
to infer it will assume overclaiming.

Reproducibility items belong in the paper or a cited artefact, not in an
unlogged working directory: parameter tables with provenance, seeds, version
identifiers, and the exact analysis path from raw output to reported figure
(Sandve et al. 2013, `10.1371/journal.pcbi.1003285`).

When parameters are assumed rather than measured, label them **assumed** in the
table caption and in the text. Presenting an assumed parameter range as a
calibrated one is a claim-integrity failure that no amount of hedging elsewhere
repairs.

## Controlled Experiment

Section order: Introduction -> Hypotheses -> Methods (design, participants or
units, randomisation and allocation concealment, interventions, outcomes with
definitions, sample-size rationale, blinding, statistical methods) -> Results
(flow of units, baseline characteristics, outcome estimates with precision,
harms or failures) -> Discussion (interpretation, generalisability, limitations)
-> Conclusion.

The reference checklist for randomised trials is CONSORT 2010 (Schulz et al.
2010, `10.1136/bmj.c332`); for animal work, ARRIVE 2.0 (Percie du Sert et al.
2020, `10.1371/journal.pbio.3000410`). The transferable requirements for
engineering and computing experiments are: pre-specified primary outcome,
declared allocation procedure, unit-flow accounting including dropouts and
failed runs, and effect estimates reported with precision rather than as bare
significance verdicts.

Distinguish the **unit of assignment** from the **unit of analysis**. Assigning
conditions to sites but analysing individual readings inflates apparent
precision.

## Observational Study

Section order: Introduction -> Objectives with pre-specified hypotheses ->
Methods (design label, setting, participants and eligibility, variables with
definitions, data sources and measurement, bias handling, study size,
quantitative methods including confounder treatment) -> Results (participant
flow, descriptive data, outcome data, main results with adjusted estimates,
sensitivity analyses) -> Discussion (key results, limitations, interpretation,
generalisability) -> Conclusion.

The checklist is STROBE (von Elm et al. 2008, `10.1016/j.jclinepi.2007.11.008`).
State the design label explicitly: cohort, case-control, or cross-sectional.
Each supports different inferences, and a paper that leaves the label implicit
usually drifts into causal language the design cannot support. Report both
unadjusted and adjusted estimates, and name which variables were adjusted for
and why.

## Prediction Model Study

Section order: Introduction -> Objectives (development, validation, or both) ->
Methods (data source and split, participants, outcome definition and blinding to
predictors, candidate predictors, sample size, missing-data handling, model
specification, model performance measures, internal validation, model updating)
-> Results (participants, model development including full specification,
performance with calibration and discrimination, validation results) ->
Discussion (limitations, interpretation, implications) -> Conclusion.

The checklist is TRIPOD (Collins et al. 2015, `10.7326/M14-0697`). Two
requirements are non-negotiable and frequently violated: report the **full model
specification** so the model can be applied to a new case, and report
**calibration** alongside discrimination. A discrimination metric on its own
does not establish that predicted values match observed rates.

Label the study as development, internal validation, or external validation.
Reporting development performance and calling it validation is a scope error.

## Protocol And Registered Plan

Section order: Administrative information -> Introduction (rationale, objectives,
design) -> Methods (setting, eligibility, interventions, outcomes, timeline,
sample size, recruitment, allocation, blinding, data collection and management,
statistical analysis plan, monitoring) -> Ethics and dissemination.

The reference is SPIRIT (Chan et al. 2013, `10.1136/bmj.e7586`). A protocol is
written in the future or intended tense and reports **no results**. Every
outcome must be pre-specified with its measurement and timing, because the
protocol's function is to fix those decisions before data are seen.

## Economic Evaluation

Section order: Introduction -> Methods (population, setting, perspective,
comparators, time horizon, discount rate, outcome measures, resource and cost
valuation, model type, assumptions, analytics and uncertainty characterisation)
-> Results (base-case, uncertainty, sensitivity and scenario analyses) ->
Discussion -> Conclusion.

The checklist is CHEERS 2022 (Husereau et al. 2022, `10.1136/bmj-2021-067975`).
Perspective, time horizon, and discount rate must be stated before any cost is
reported; the same intervention yields different conclusions under different
perspectives, so omitting them makes the result uninterpretable.

## Sections Common To Every Blueprint

### Title

State object, scope, and where possible the contribution. Prefer specificity
that a database search can match over breadth that reads as a topic label.
Include the design when it disambiguates: `a systematic review`,
`a simulation study`, `a randomised trial`.

### Abstract

Order: context or problem -> gap -> objective or question -> method or material
-> principal result with its quantity -> bounded conclusion. Do not introduce a
claim, number, or implication absent from the body. For a mechanism-level or
simulation result, place the claim boundary inside the abstract; a reader who
stops at the abstract must not leave with a stronger claim than the study
supports.

### Introduction

The standard move sequence establishes a territory, reviews prior work,
indicates a gap or problem, and occupies that gap by stating the present work
(Swales 2014, `10.1075/z.184.513swa`; Swales & Feak 2012, `10.3998/mpub.2173936`).

A gap is not "few studies exist". A defensible gap names what remains
unresolved, why the unresolved part matters, and what the present work will
settle. State the contribution as a bounded claim, not a promise of importance.

### Related work

Organise by problem, construct, method, finding pattern, or disagreement.
An author-by-author catalogue is not a synthesis. Every paragraph should compare
sources along one stated analytic dimension and end at a position the present
work takes.

### Methods

State design and rationale, then context, procedure, measures, analysis, and
decision rules. Distinguish **method** (the instrument or technique) from
**methodology** (why that instrument suits this question). Listing techniques
without saying which question each serves is the most common weakness in this
section.

### Results

Orient the reader, report in question order, give quantities with uncertainty,
and stop at pattern description. No causal explanation, no comparison to prior
literature, no recommendation.

### Discussion

Answer the research question first, then interpret, then relate to prior work,
then consider alternative explanations, then delimit inference, then state
implications proportional to the evidence. Keep result, interpretation, and
implication separable in every paragraph.

### Limitations

Write it as a named unit with consequences attached. `The sample was small` is
not a limitation; `the sample supports direction of effect but not magnitude` is.
State what each limitation prevents the reader from concluding.

### Conclusion

Give the answer, the bounded contribution, the applicability limit, and the
warranted next step. Do not restate the abstract and do not widen the claim.

## Stance And Hedging Across The Paper

Stance markers are part of the claim, not decoration. Hedges, boosters,
attitude markers, and self-mention form a system that positions the writer
relative to the evidence and the reader (Hyland 2005,
`10.1177/1461445605050365`).

Consequences for revision and humanising passes:

- Collapse a stack of qualifiers to one calibrated marker; never reach zero.
  `may reduce` must not become `reduces`.
- Do not add a booster to compensate for a weak result.
- Keep attribution explicit: whether a statement is this study's finding, a
  cited source's claim, or the authors' interpretation must remain recoverable.

## Vietnamese Research Writing Notes

- Section names commonly expected in Vietnamese venues and theses: `Mở đầu`,
  `Tổng quan`, `Phương pháp nghiên cứu`, `Kết quả và thảo luận`, `Kết luận`.
  When `Kết quả và thảo luận` is merged, keep reporting and interpretation as
  separate paragraphs inside the merged section; merging headings does not
  license merging the two functions.
- `Tính cấp thiết của đề tài` is a genre-mandated move in Vietnamese proposals
  and theses. It is repaired when weak, never deleted.
- `Phương pháp nghiên cứu` in Vietnamese submissions is frequently a bare list
  such as `phân tích, tổng hợp, so sánh`. Bind each technique to the question it
  answers and the section where it is applied.
- Do not import a stronger claim during Vietnamese-to-English translation.
  `có thể góp phần` is not `demonstrates`.
- Number format is owned by the declared template, not by language default; see
  the number-format section of [Academic Vietnamese standard](academic-vietnamese-standard.md).

## Verification Status Of This File

Every DOI cited here was resolved against Crossref and matched on author, year,
title, and container before inclusion. Twenty-three candidate sources were
queried and twenty-three resolved.

Blueprint section orders are **syntheses of the cited reporting guidelines and
methodology sources**, arranged for practical use. They are not verbatim
checklists. When a claim about a specific checklist item matters, consult the
cited guideline directly rather than relying on the summary here.

Genre labels for Vietnamese venue conventions are drawn from observed practice
in the user's own documents and are marked as convention, not as a cited
standard.
