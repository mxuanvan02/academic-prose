# Submission Integrity Declarations

A submission to a leading journal carries a set of short, non-narrative texts that
are not part of the manuscript's argument and are graded by different criteria:
the cover letter, the novelty or contribution statement, the authorship and
contribution record, the conflict-of-interest declaration, the data and code
availability statement, the ethics approval statement, and — increasingly
mandatory — the generative-AI use disclosure.

These texts fail differently from prose. A body paragraph fails by overclaiming;
a declaration fails by **asserting a state of the world that nobody verified**.
The controlling rule is therefore stricter than the prose contract: a declaration
may only state what the author has confirmed, and a drafting agent may never
supply its content by inference.

## The prohibition

Do not generate, complete, guess, or plausibly reconstruct any of the following.
Each is `fabricated_declaration`, a blocking failure:

- an author list, an affiliation, an ORCID, or a corresponding author;
- a contribution assignment (who did what);
- an ethics approval, its committee, or its protocol number;
- a consent statement;
- a trial, review, or preregistration identifier;
- a funding source or grant number;
- a conflict-of-interest status;
- a data or code location, licence, or access condition;
- a statement that a dataset is available when its availability is unknown;
- a prior-submission or preprint history;
- a permission or copyright clearance.

The correct output when the information is absent is a **visible placeholder plus
a named blocker**, never a filled field. A declaration is the one place in a
submission where an empty slot is safer than a fluent sentence: an invented ethics
approval is misconduct, while a missing one is an administrative gap.

Code for the opposite failure — a placeholder silently carried into a delivered
artifact — is `placeholder_residue`, already blocking. Both directions are
enforced: do not fill, and do not ship unfilled without flagging.

## Cover letter

The cover letter is a short argument addressed to an editor, not a summary
addressed to a reader. Its job is to let the editor decide whether the paper
belongs in this journal and which handling editor should see it.

Required progression:

1. The problem and why this journal's readership is the right audience.
2. What the paper establishes, in one sentence, as a delta against current work.
3. Why the result meets this journal's stated scope and standard.
4. Administrative facts: originality, concurrent submission status, prior related
   work by the same authors, suggested or excluded reviewers where invited.

Failure modes:

- **Abstract paste.** Reproducing the abstract answers a different question and
  wastes the only direct channel to the editor. Code `coverletter_as_abstract`.
- **Promotion in place of a claim.** "Groundbreaking", "first-ever", "will
  transform the field" carry no information and shift the burden to the editor.
  Code `promotional_contribution`, already in the taxonomy.
- **Venue-blind text.** A letter that would work unchanged for any journal has not
  argued fit. Name the scope clause or the recent line of work in that venue.
- **Overreach on standing.** Claiming novelty the manuscript does not demonstrate
  is checked immediately against the paper.

## Novelty and contribution statement

Where the journal requires an explicit statement, it must be falsifiable and
enumerable, and it must map onto the manuscript.

Contract:

- Each contribution names the **mechanism** that makes it a contribution rather
  than an activity. "We build a four-stage pipeline" is an activity; "the
  reference-anchoring stage makes every item traceable to its source provision" is
  a contribution. Code `activity_as_contribution`, already in the taxonomy.
- Each contribution is stated against a **named incumbent**, not against
  "existing methods".
- The statement's items correspond one-to-one with the manuscript's contribution
  list and with its research questions. A contribution present here and absent in
  the paper is `unsupported_novelty`, already blocking; a research question that
  yields no contribution is `unanswerable_rq`.
- Novelty type is declared: new problem formulation, new mechanism, new guarantee,
  new regime of applicability, or first evidence where only conjecture existed.
  A "novel combination" needs a reason the combination was not obvious.
- Contributions are **counted honestly**. Restating one contribution at three
  granularities to reach three bullets is `contribution_count_inflation`:
  reviewers merge them and read the merged count.

## Authorship and contribution record

- Authorship order, corresponding author, and equal-contribution marks are author
  decisions. Record what is supplied; never infer from who wrote which section.
- Where a structured taxonomy is required, map each supplied contribution to its
  category and leave unmapped categories empty rather than distributing them
  plausibly.
- Do not add, remove, reorder, or merge authors during a revision pass. An
  authorship change between versions requires the journal's own procedure and is
  outside a drafting agent's authority.
- Acknowledgements are not authorship. Moving a contributor between the two
  changes a formal claim.

## Conflict of interest and funding

- Report exactly what the authors supply, including "none declared" when they
  declare none. Do not derive a COI status from affiliations, and do not infer
  funding from a topic.
- A grant number is an identifier: it is a rigid designator, never translated,
  never reformatted for tidiness. See
  `references/terminology-localization.md`.
- Where a funder requires specific acknowledgement wording, that wording is a
  template constraint and outranks style preferences.

## Data, code, and materials availability

Four distinct states, routinely collapsed into one optimistic sentence:

| State | Permissible statement |
|---|---|
| Openly deposited | name the repository, the identifier, and the licence |
| Available on request | name who decides and under what condition |
| Restricted | name the restriction and its legal or ethical basis |
| Not available | say so, and name what this prevents a reader from checking |

Collapsing a restricted or on-request state into "data are available" is
`availability_overstatement`, blocking. A statement naming a repository without a
resolvable identifier is `fabricated_declaration`.

Where the deposit is planned but not complete at submission, say that, with the
intended repository. A future intention stated in the present tense is an
overstatement.

## Ethics, consent, and permissions

- Human-subject, animal, clinical, and personal-data work requires an approval
  statement whose committee, protocol identifier, and date come from the authors.
  Absent those, output the placeholder and the blocker.
- Consent and assent are separate statements from approval.
- Third-party material — figures, instruments, extended quotations — requires a
  permission statement whose existence the author confirms.
- A statement that approval "was obtained" without an identifiable approving body
  is not a declaration; it is an assertion the journal cannot check.

## Generative-AI use disclosure

Most leading venues now require disclosure of generative-AI use and prohibit
listing an AI system as an author. Two rules govern the drafting agent's own
involvement:

1. **The disclosure describes actual use.** State which stages used which class of
   tool and for what purpose — drafting assistance, translation, code generation,
   analysis, figure production. Understating is a misrepresentation; inventing a
   tool that was not used is `fabricated_declaration`.
2. **The disclosure never transfers responsibility.** Authors remain accountable
   for every claim, including those an assistant drafted. A disclosure phrased so
   as to distribute responsibility to a tool is `responsibility_deflection`.

An AI system is not an author and does not appear in the author list, the
contribution record, or the acknowledgements-as-contributor position.

Where the venue publishes required wording, use that wording verbatim; where it
does not, keep the statement factual, specific to stage and purpose, and free of
justification.

## Preregistration and protocol references

- A registration identifier is supplied by the author and verified against the
  registry. Never construct one, and never state that a study was preregistered
  because its design looks confirmatory.
- Where the analysis deviates from the registered plan, the deviation is reported
  with its reason. Silent deviation converts a confirmatory claim into an
  exploratory one without telling the reader — the prose trace is
  `exploratory_as_confirmatory`; see
  `references/quantitative-reporting-standard.md`.
- An unregistered study is not defective. State that it was not preregistered and
  which inferences are therefore exploratory.

## Audit procedure

Run before any submission package is called ready:

1. **Inventory the declarations** the target venue requires, from the venue's own
   author instructions rather than from a summary file. An untraceable requirement
   is `fabricated_constraint`, already in the taxonomy.
2. **Source every field.** For each declaration, record whether its content came
   from the author, from a verifiable artifact, or from neither. "Neither" means
   placeholder plus blocker.
3. **Check the manuscript agreement.** Contribution statement against the paper's
   contribution list; availability statement against what is actually deposited;
   ethics statement against the methods described.
4. **Check the identifiers resolve.** DOIs, registry numbers, repository handles,
   ORCIDs. An unresolved identifier is reported, not silently kept.
5. **Check the AI disclosure against what actually happened** in producing the
   submission, including translation and figure generation.
6. **Sweep for placeholders** across both language versions before delivery.
7. **Report the blockers explicitly** in the delivery message. A submission
   package with unfilled declarations is a correct output; one with invented
   declarations is not.

## Blocking failures introduced here

- `fabricated_declaration` — any declaration field supplied by inference rather
  than by the author or a verifiable artifact.
- `availability_overstatement` — restricted, on-request, or unavailable data
  described as available.
- `responsibility_deflection` — a disclosure phrased to transfer accountability
  for claims to a tool.
- `coverletter_as_abstract` — a cover letter that summarises the paper instead of
  arguing venue fit.
- `contribution_count_inflation` — one contribution presented as several by
  restating it at different granularities.

## Verification status of this file

The declaration categories and prohibitions here are derived from this
repository's existing claim-integrity and template-authenticity contracts, and
from the general structure of submission requirements at established venues. This
file is **not** a citation of any specific journal's current policy, and journal
policies on generative-AI disclosure in particular are changing quickly. Retrieve
the target venue's own author instructions and let them govern; where this file
and the venue disagree, the venue wins.
