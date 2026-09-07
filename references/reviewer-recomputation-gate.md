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
