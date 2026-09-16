# Reviewer Recomputation Gate

Recomputing an audited document's number is the right instinct and an incomplete
control. A recomputation is itself a claim, and it inherits the same evidence
contract as the sentence it is used to attack. The failure this gate prevents is
narrow and expensive: **the auditor recomputes a quantity, gets a different
value, and reports the difference as the document's error, when the difference
was produced by an assumption the auditor supplied and the document never
stated.**

Directed at an author, that is a false accusation delivered with the authority of
arithmetic. It is worse than the defect it purports to find, because the author
cannot answer it without guessing which parameter table the auditor used.

## 1. Every recomputation is CLOSED or OPEN

Classify each recomputed quantity **before** writing a word about it.

**CLOSED** — every input is either printed in the audited document or a universal
constant. The recomputation is reproducible by any reader with the document in
hand. A disagreement is a finding, and the document is wrong.

**OPEN** — at least one input comes from an external parameter table, convention,
or software default that the document does not state, and for which the
discipline supplies more than one accepted version. The recomputation is *one
member of a family of admissible values*. A disagreement is **not** a finding.

The distinction is not about difficulty. An OPEN recomputation can be trivial
arithmetic; what makes it OPEN is that a second competent reader, using a
different but equally standard table, gets a different number and is equally
right.

Recurring sources of OPEN inputs: elemental, atomic, or physical property tables
that differ by compilation; unit and scale conversions with more than one
convention; reference or base periods; taxonomies and code lists that were
revised between editions; library defaults that changed across versions;
tokenization, rounding, and tie-breaking rules; any constant whose accepted value
depends on which authority is cited.

## 2. What each class licenses

| Class | Licensed finding | Forbidden |
| --- | --- | --- |
| CLOSED, agrees | none; record as verified | reporting a non-finding to appear thorough |
| CLOSED, disagrees | the document's value is wrong; state both values and the derivation | attributing it to a table the document did not use |
| OPEN, agrees | none | claiming the agreement validates the auditor's table |
| OPEN, disagrees | **only** that the parameter source is unstated, so the value cannot be reproduced | asserting the auditor's value, or implying the document's value is wrong |

The OPEN-disagrees row is the whole point. The reportable defect is a
**reproducibility gap in the document**, not an arithmetic error. Say that the
source of the parameter is unstated and that the value therefore cannot be
checked. Do not supply a competing number, because supplying it converts a real
and modest finding into an unfounded and severe one.

Code `open_input_recomputation`. It is blocking, and it belongs to the same
family as `fabricated_constraint`: both destroy correct work rather than merely
degrading a claim, and both are invisible afterwards.

## 3. Sensitivity sweep before assertion

For every OPEN quantity, the check is not one recomputation but several.

1. Enumerate the standard tables or conventions a competent author could have
   used. Two is rarely enough; three or four is usual.
2. Recompute under each, and record the resulting range.
3. Ask whether the document's value is **reachable** anywhere in that range.
   - Reachable: the author is not wrong. Downgrade to "state the source."
   - Unreachable under every standard option: now a discrepancy exists, and the
     range itself is the evidence for it. Report the range, not a single value.

A single recomputation that disagrees is a hypothesis. The sweep is what turns it
into evidence or retires it. Skipping the sweep is how an auditor arrives at a
confident, specific, wrong accusation.

Corollary for prose: where the sweep clears the author, the surviving sentence
asks for the parameter source and says nothing about the value. Where it does
not, report the range and name the tables, so the author can identify which one
they used.

## 4. Gathering is not falsification

An audit is commonly organised as repeated passes, and it is easy to mistake
their number for their strength. Passes fall into two kinds:

- **GATHER** — reading further, extracting more text, grepping for absent
  material, recomputing the document's own arithmetic, verifying identifiers
  against an external registry. Each pass finds defects *in the document*.
- **FALSIFY** — varying the auditor's own assumptions, re-deriving under a
  different admissible convention, seeking the reading under which the author is
  right, checking whether a stated disagreement survives its own sensitivity
  range. Each pass finds defects *in the audit*.

Every GATHER pass leaves an auditor-supplied assumption untouched, so no number
of them can detect an error located there. An audit consisting entirely of GATHER
passes is unverified with respect to its own claims, however many passes it ran,
and reporting a pass count as evidence of rigour overstates what was done.

Code `gather_only_verification`. Blocking. At least one FALSIFY pass is required
before any recomputed disagreement is asserted, and the audit report states which
pass performed it.

## 5. Audit procedure

1. **Inventory** every quantity recomputed during the audit, including ones that
   agreed.
2. **Classify** each CLOSED or OPEN, naming the external input that makes an OPEN
   quantity open.
3. **Sweep** every OPEN quantity across the plausible conventions and record the
   range.
4. **Downgrade** every OPEN disagreement whose target value is reachable inside
   that range to a request for the parameter source.
5. **Run one FALSIFY pass**: for each asserted disagreement, attempt to construct
   the assumption under which the author is correct. Record the attempt and its
   outcome.
6. **State the boundary** in the report: which quantities were verified, which
   could not be reproduced for want of a stated source, and which the audit did
   not examine at all.

Step 5 is the one a thorough-looking audit skips, and step 3 is the one that
retires most OPEN disagreements.

## 6. Pitfalls

- **Confidence tracks arithmetic, not evidence.** Having done a calculation feels
  like having verified something, and the feeling is identical whether the inputs
  were closed or open. The classification must be explicit and written down,
  because introspection does not distinguish the two cases.
- **A CLOSED check on the document's own printed range is the strongest finding
  available.** Comparing an author's reported value against a limit the same
  document states requires no external table at all. Prefer these; they cannot be
  answered by a parameter dispute.
- **Reachability, not equality, is the test for OPEN quantities.** An auditor's
  value differing in the second digit proves nothing when the range spans several
  units.
- **Discrete counts are usually CLOSED where continuous properties are OPEN.**
  A quantity built from integers fixed by definition has no competing table; a
  quantity built from measured properties usually has several. Classify per
  quantity, never per document.
- **An audit that reports every check as a finding is miscalibrated.** Verified
  quantities are results and belong in the report as such; padding a findings
  list with non-findings destroys the credibility of the real ones.
- **The same gate applies to an audit of your own draft.** Self-audit is where
  the GATHER-only failure is most likely, because the assumptions under
  examination are the ones that produced the draft.

## 7. Run the source's own verifier before recomputing

When a submission ships a released verification harness — a script that
recomputes its reported quantities from released records — **run it first**,
before any independent recomputation. It encodes the authors' conventions: which
denominators pair with which numerators, which items were excluded and why,
which grid of thresholds was actually tabulated, and how internal identifiers
map onto the names used in the prose. An external auditor otherwise has to guess
all of these, and guessing is where false findings come from.

Measured on first use of this gate: the shipped harness resolved 119 reported
quantities in one invocation, exit status 0, and **retired three of the four
discrepancies the auditor had independently "found"**. Independent recomputation
is not stronger evidence than the authors' own executable check; it is weaker,
because it substitutes the auditor's assumptions for the authors' declarations.

Two corollaries:

- A recomputation that disagrees with a shipped verifier is a claim about the
  verifier's conventions, not evidence of an error in the document. Read the
  verifier's source and its inline notes before concluding anything.
- Prefer the harness's output as the audit's quantitative backbone and reserve
  independent recomputation for quantities the harness does **not** cover. State
  which is which, so a reader knows what was checked by whom.

## 8. Three further auditor-side error classes

Section 1 covers the case where an input is *absent* from the document. These
three cover inputs that are **present and were discarded or misread**. All are
CLOSED recomputations that are nonetheless wrong, so the CLOSED/OPEN
classification alone does not catch them.

**`qualifier_dropped`** — the source states a restriction that narrows a count
or a set (*"…that both runs tabulate"*, *"…after a declared exclusion of two"*,
*"…over the same items"*), and the auditor computes the unrestricted version.
Measured: an auditor assumed a uniform threshold grid and reported a count of
nine where the manuscript's seven was correct, because it ignored the qualifier
naming which runs contribute. Fix: re-read the whole sentence containing the
number, and the sentence before it, for restrictive clauses **before** choosing
inputs. A number's denominator and its restriction are usually named within a
line or two of it.

**`documented_discrepancy_as_finding`** — two figures differ, the auditor
reports an inconsistency, and the authors have already documented why. Measured:
a κ table spanning every admitted item was flagged against an ablation universe
two items smaller; the shipped verifier carried an inline note stating exactly
that the larger n was deliberate and naming the reason. Fix: before asserting an
inconsistency, search the released code, records, and notes for both figures and
for explanatory keys (`note`, `why`, `is … and not …`). A deliberate denominator
difference recorded in a comment is not a manuscript defect — though asking the
authors to say so **in the prose** remains a legitimate, much smaller request.

**`identifier_mapping_bug`** — released records use internal identifiers
(run names, arm names, model or condition labels) that differ from the names in
the manuscript. Comparing counts before building the mapping produces wholesale
false mismatches, and the volume of them reads as a catastrophic defect.
Measured: an auditor reported four of five conditions mismatching, entirely
because internal arm labels had not been mapped to the manuscript's arm names;
after mapping, all fifteen quantities agreed. Fix: derive the mapping from a
quantity that **must** agree regardless of naming (a frame size, a grand total,
a sum of subsets), assert the mapping reproduces it, and only then compare
per-condition counts. Never report a mismatch rate computed across an unverified
mapping. This is the `evidence-claim-reconciliation` pitfall of comparing labels
instead of identities, occurring on the auditor's side of the table.

## 9. Withdrawn findings are reported, not deleted

An audit that silently drops a finding leaves no record that the check ran and
failed, so the same error recurs and nobody learns the gate worked. State which
findings were withdrawn and why, in the deliverable, classified by cause:

| Cause of withdrawal | What to report |
| --- | --- |
| the source's own verifier reproduced the value | the harness, its exit status, and the quantity count it covers |
| a qualifier in the source text was missed | the qualifier, quoted, and the corrected reading |
| the discrepancy was documented as deliberate | where it is documented, and whether the prose should say so too |
| the input was OPEN and the value is reachable | the sweep range, and the request for the parameter source |

Reporting withdrawals is evidence the falsification pass did real work. An audit
whose findings list contains only confirmations of its first impressions has not
falsified anything, whatever its pass count.
