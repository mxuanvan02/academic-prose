# Skill Repository Maintenance

This skill is normally deployed in two places with different roles, and editing one
without the other is the usual cause of lost work.

| Location | Role |
| --- | --- |
| the runtime skills tree, wherever the host agent loads skills from | what the agent actually reads; edited first, because that is where a lesson is discovered |
| this repository | the published source; it alone owns the CI workflow and `scripts/public_hygiene_check.py` |

## 1. Never copy one-way

A recursive copy from runtime to repository is this skill's own
`generated_artifact_drift` failure applied to itself: everything that exists only at
the destination is destroyed, and the rebuilt file carries no record that it existed.

Measured loss from one such copy: the `## Learning From Feedback` heading. The
paragraph survived; the heading did not, so the section stopped being addressable by
this repository's own contract test. A diff would have shown it in one line.

Protocol:

1. Compare both trees recursively. Enumerate destination-only files **and**
   destination-only lines inside shared files.
2. Copy only the files that changed, then re-check that the destination-only lines
   survived.
3. Treat structural moves and heading changes as first-class diffs; a naive read
   loses them.

## 2. Adding a mechanism means extending the gate

A new reference document, detector, or threshold is not integrated until this
repository's validator can fail because of it. The sequence that works:

1. Add the paths to the `REQUIRED` tuple in `scripts/validate_skill.py` **and** to
   `tests/test_repository.py`, fixtures included.
2. Make the validator *invoke* the new test as a subprocess and fail on a non-zero
   return code or on `FAILED`/`ERROR` in its output. A required-file check proves the
   file exists, not that it works.
3. Add an explicit CI step so the gate is visible in the workflow log.
4. Assert from the contract test that new blocking codes appear in
   `references/quality-rubric.md`, so a code can never be enforced by a script while
   absent from the published rubric.

## 3. Prove the gate can go red

The convention here is that every check is mutated on purpose to show it knows how to
fail. Apply it to any new gate: delete one branch of the detector, run the validator,
confirm a non-zero exit and which tests failed, restore, confirm green.

A check that has never been observed red is not evidence. This is the same standard
the manuscript-facing rules impose on a verification claim: state the property the
check establishes and, separately, the property it does not.

## 4. Pitfalls found while doing this

- **Run the scanner tests from inside `scripts/`.** They import the scanner as a
  sibling module, so invoking them from the repository root raises
  `ModuleNotFoundError`. In CI use `working-directory: scripts`; for an ad-hoc
  diagnostic, load the module by absolute path.
- **When a marker does not fire, print the matcher's output sentence by sentence**
  before editing the pattern. Two regex revisions were spent guessing at the wrong
  clause; one diagnostic print located a missing person agreement (`do not` against
  `does not`) immediately.
- **Calibrate on real manuscripts, not only on fixtures.** A detector tuned on its own
  examples measures nothing. Running it across several genuine drafts produced three
  false positives that fixtures never would have: a correlative intensifier, a LaTeX
  preamble read as prose, and a repository filename graded as severely as a path on
  the author's machine.
- **Keep those calibration cases as permanent tests.** They are the only thing
  preventing the same false positive from returning at the next pattern edit.
- **A code name in an explanation paragraph cannot pin its blocking bullet.** This
  is the heading-vs-link-text pitfall in a second guise. `assertIn("venue_ambition_leak",
  rubric)` stayed green after the `- \`venue_ambition_leak\`: …` bullet was deleted,
  because the same identifier still occurred in the paragraph that groups the code
  with its trap family. Pin the bullet form — `assertIn("- `code`: ", rubric)` — and
  mutate by deleting that exact line to confirm red. Every code the rubric declares
  should be pinned this way; a name that appears twice can lose one occurrence
  silently.
- **A word-boundary omission produces a false positive that fixtures miss.** A
  venue-tier pattern written as `(?:journal|venue)[^.;]{0,40}\bQ[1-4]\b` matched
  *Re**venue** in Q1 of the observation window* — a fiscal quarter in a Results
  section. The clean fixture caught it only because the fixture was written to
  contain deliberately adjacent legitimate uses (interquartile range, first
  quartile, fiscal Q1, Scopus in Methods, "the impact of"). When adding a lexical
  class, write the clean fixture from the *near-miss vocabulary* first, then the
  dirty one; a clean fixture that avoids the danger words tests nothing.


- **A mutation harness must prove it mutated.** Three consecutive rounds reported
  "not caught" for assertions that were in fact sound: the harness substituted a
  string that did not occur, wrote the file back unchanged, and read the resulting
  green run as missing stopping power. Before trusting a negative result, assert
  inside the harness that the file hash changed *and* that the mutated construct is
  absent afterwards. A mutation that cannot be shown to have happened is not
  evidence about the check, and reporting it as one manufactures a defect in a
  working gate.
- **A name that is also link text cannot pin its heading.** `assertIn("Process
  logic gate", rubric)` stayed green after the `## ` heading was deleted, because
  the same words remain in the prose link
  `[Process logic gate](process-logic-gate.md)`. Pin the heading form,
  `assertIn("## Process logic gate", rubric)`, and mutate by deleting that exact
  line to confirm red.
- **A concatenated forbidden literal must be raw on BOTH halves.** The gate splits
  its tokens so it does not flag itself, and five entries wrote the second half as a
  plain string: `"BS\b"` is backspace 0x08, not a word boundary, so the compiled
  pattern ended in a control character and could never match anything. The gate
  printed PASS while real leaks of two codenames and one institution abbreviation sat
  in shipped files. `tests/test_public_hygiene_gate.py::TestEveryPatternIsAlive` now
  asserts (a) no compiled pattern contains 0x08 and (b) every label matches a
  canonical probe, so a pattern that dies fails loudly instead of silently.
  Two probe-writing traps, both measured here. First, a probe half that itself spells
  a complete forbidden token makes the gate flag the test file — split the probe the
  same way the gate splits its pattern, and say the rest by label. Second, a
  word-boundary pattern does not bound an underscore, so a codename joined into a path
  or filename with `_` is NOT matched; probe the space-delimited form and treat the
  underscore-joined form as a known gap, never as a caught case.
- **A gate that has only ever been seen green proves nothing about its patterns.**
  The wrapped-token suite showed a line break cannot defeat a LIVE pattern; it said
  nothing about whether each pattern was alive. Inventory-level assertions (one probe
  per label, asserted as a set equality against the pattern table) are what turn a
  new entry into a checked entry instead of a hopeful one.
- **A class-level detector test only needs one pattern to fire.** Deleting a single
  regex from a scanner left every behavioural test green, because the class still
  matched through its remaining patterns — so a gate whose patterns can be removed
  silently has no stopping power. Pin the full pattern inventory by identity in the
  test file so removing any one entry fails, and let the behavioural tests cover
  semantics rather than coverage.

- **`SKILL.md` has a hard size ceiling (100,000 characters) enforced by the
  editing tool, not by the validator.** `scripts/validate_skill.py` does not
  measure file size, so a green validation run does not mean the file is
  patchable — every edit against an oversized `SKILL.md` is rejected wholesale.
  When that happens, compress rather than append: find a section whose detail
  already lives in a reference, verify by normalized substring probe that every
  rule and failure code survives in the reference, then reduce the `SKILL.md`
  copy to the decision rules plus a pointer. Move anything unique to its owning
  reference *before* cutting it.

- **Measure the compressible ratio before promising one.** The advice above reads as though
  most of a section can be compressed. It cannot, and the gap is large enough to change the
  decision. A pilot on the most narration-dense section in `SKILL.md` -- 76% of its 3,685
  characters classified as narration by a keyword classifier -- recovered **391 characters,
  15% of that narration**. The other 85% could not be touched, for a reason the classifier
  cannot see: the rule inventory probes a normalised window around each obligation keyword,
  so an obligation survives only if the words around its keyword are unchanged. Rewrapping
  lines is free; **rewording a rule is not**. Most "narration" in this file is the tail of a
  sentence whose head carries an obligation, so it is frozen by association.

  Three consequences worth having before starting:

  * Extrapolating 15% across the file gives roughly **4,700-7,300 characters**, not the
    14,000-29,000 that a 30-60% rewrite assumption predicts. And that is an upper bound: the
    pilot section was chosen for *high* narration density, while the file average is 49%.
  * **Relocating** evidence and illustration into `references/` looks like a far bigger lever,
    because that directory has no ceiling and narration plus evidence totals 64,155 characters
    (64% of the file). **That total is a raw character count, not an achievable saving.** An
    earlier version of this lesson quoted it as "measured at 63,000-69,000 characters, about 8x
    the rewrite lever", which overstated it by implying a measurement of what could move.
    Relocation is free only where the reference already owns the text, and it almost never does:
    across all 203 obligations, 0 are duplicated at an 80-character prefix, 7 at a 40-character
    prefix, and 28 (14%) match on any six-word slice; exactly 1 of 29 sections has half or more
    of its obligations already present in the reference it points at, and that section is 903
    characters. So nearly every move requires authoring new reference content first and then
    verifying nothing was lost. It is a writing project, not a reformatting one.
  * Relocation also moves content out of the always-loaded body, so a rule that must fire
    unprompted cannot be relocated at any saving. That is a behaviour decision, not a formatting
    one. Do not try to bound it with a keyword classifier for "is this a trigger section":
    treating any mention of a `references/` path as a routing trigger fired on **21 of 29**
    sections, which discriminates nothing; requiring a routing verb next to the path still fired
    on 14. A column built on either is weak evidence, and the honest statement is that the
    always-fire classification has to be read, not detected.
  * **When a containment probe returns zero, widen it before believing it.** The same question
    -- "is this obligation already in a reference?" -- returned 0, 7 and 28 depending only on
    probe width (80-character prefix, 40-character prefix, any six-word slice). Reporting the
    narrowest as a fact produced a confident zero, and that zero was then used to argue the
    lever did not exist. Four probes at different widths cost nothing; a single narrow one is
    how this session produced four false negatives in a single pass of a different check.
  * Verify ownership *before* deleting an illustration. Every change in the pilot was a
    rewrite except one parenthetical example, and deletion is the only loss a rewrite can
    hide: no structural check notices it, because the obligation sentence survives without
    its example. A multi-needle probe against the reference is required, since a single
    narrow needle produced four false negatives in one pass of this same investigation.

- **Keyword classifiers need word boundaries, and the failure is doubly misleading.** An
  unbounded alternation matches `never` inside `when**ever**` and `block` inside
  `**block**s`, which classified 21 of 227 lines as obligations when they were ordinary prose.
  Each false obligation freezes a line that could legitimately be rewritten, and the harness
  then reports a *higher* count of protected rules while protecting things that were never
  rules -- so the defect reads as extra rigour rather than as an error. Bound every
  alternative; multi-syllable Vietnamese phrases need no boundary.

- **Never pipe a verification harness through `head`, `sed` or `tail`.** Doing so closed the
  pipe early, the harness died on SIGPIPE with rc=141, and the script proceeded to report a
  pass for a rewrite that had been written to the repository but never verified. A related
  defect in the same run printed `PILOT PASSED: saved 0 characters` after the rewrite had
  *aborted* -- the checks then ran against the original file and reported green about work
  that did not exist. Capture to a file and grep the file, and assert that the file's size
  actually changed before trusting any downstream check.

- **Do not normalise frontmatter to match one existing tool.** Publishing two new
  skills, the obvious move was to rewrite their frontmatter to the shape
  `system-one-work-loop` uses (`metadata:` carrying `version`/`license`/`status`).
  But the published tools do not share a convention: `academic-prose` uses top-level
  `license:` plus `metadata.version`; `system-one-work-loop` uses `metadata:` only;
  `ppt-master-officecli` has no metadata block at all. There was no convention to
  conform to, and the rewrite produced frontmatter carrying `version` **twice** while
  diverging from the live tree. Copy the live file verbatim and assert only what a
  public repo actually needs -- a licence and a version are declared, and no top-level
  key is duplicated. When a convention is worth having, establish it across every tool
  in its own change; do not smuggle it in through a publish PR.
- **`git status --porcelain` output must not be stripped before comparing.** Porcelain
  encodes "modified, not staged" as a LEADING SPACE, so the line is `' M path'`. A
  scope assertion written as `out.strip().split('\n') == [' M path']` can never match:
  it reported a scope failure on a commit that had exactly the intended one-file
  scope. Compare against the raw lines, or strip each line and compare the stripped
  forms on both sides. The dangerous direction is the opposite mistake -- a loose
  comparison that passes a wrong scope.
  A convenience wrapper that returns `r.stdout.strip()` reintroduces the bug
  invisibly: it removes the leading space from the FIRST line only, so a
  single-file scope check fails while a multi-file one appears to pass. Read
  porcelain through a call that does not strip, and assert on the raw lines.
- **`python -B -m py_compile` still writes `__pycache__`.** `-B` suppresses caches
  written by *importing*; `py_compile` writes its output deliberately, so the cache
  appears anyway (measured: one `.pyc` after a `-B` run). That matters here because the
  repo's hygiene gate treats a file it cannot decode as a `binary-file` finding, so
  running README's validation block twice in a row fails the second time on litter the
  first run left -- and `py_compile` runs immediately after the gate in that same
  block. Compile with an explicit `cfile` outside the repo
  (`py_compile.compile(src, cfile=<tmp>, doraise=True)`), or delete the caches and
  assert zero before committing. CI is unaffected: it checks out fresh and `__pycache__`
  is gitignored, so this is a local-verification trap only. Do not "fix" it by editing
  the gate, which ships byte-identically in every tool; that belongs in its own change.
- **Run the repository's own gate as a subprocess, the way CI does.** Reusing a gate's
  pattern list by importing it (`importlib` on `public_hygiene_check.py` to read
  `FORBIDDEN`) is convenient for scanning *other* trees, but it proves only that those
  patterns match. Whether the shipped script passes on the shipped tree is a different
  question, and the only honest test is to execute it:
  `python3 tools/<name>/scripts/public_hygiene_check.py`. Note that the script derives
  its scan root from `__file__` parents[1] and excludes itself, so an identical copy
  dropped into a new tool directory scopes correctly with no edit.
- **A renumbered section is not a deleted section.** Syncing a reference whose sections
  had grown from five to eighteen made a line-level diff report
  `## 5. Checklist before calling it submission-ready` as content canonical held and
  live lacked. It was present in live as section 18 with all six items byte-identical.
  Before treating a heading difference as a loss, extract the section BODY from both
  trees and compare the items; accept a renumber, abort on a missing item.

- **A gate with no tests can be defeated by a line break, and its PASS is believed.** The
  repo's hygiene gate builds literals by concatenation so it does not flag itself;
  `institution-3` was `"Hue " + "University"`, and the reference text wrapped between the two
  words, so the pattern never matched and the gate printed `PASS` on the exact text it exists to
  catch. Nothing noticed because the gate had zero tests. Match on whitespace-normalised text and
  keep an offset map back to the original, so the reported context and any allowlist's line test
  still resolve against the real file. Normalising cannot invent a match for secret-shaped
  patterns — a space breaks every character class they use — it can only reveal what a wrap was
  hiding; that reasoning was then asserted, not assumed, by a control on
  `BEGIN\nRSA PRIVATE KEY`, which the old gate also passed. Any gate like this needs a test that
  the wrapped form fires, and the fix needs one that the ordinary form still fires.
- **`tests/` ships to the runtime tree, so a repo-structure test must skip with a stated reason.**
  Measured: the runtime tree carries `evals/`, `tests/`, `agents/`, `schemas/`, `README.md` and
  `scripts/validate_skill.py`, byte-identical to canonical, while `scripts/public_hygiene_check.py`
  exists only in canonical and has no sibling `tools/` directory at runtime. A suite written on the
  opposite assumption computed `REPO_ROOT` as the tree's grandparent and produced **2 failures and
  12 errors out of 14** when copied to runtime. Guard it with
  `@unittest.skipUnless(GATE.is_file() and TOOLS_DIR.is_dir(), REASON)` where the reason names both
  missing things. A red runtime suite is a false alarm about content that was never meant to be
  there, and a failure everyone learns to ignore is worse than a skip. Then measure BOTH sides: in
  the repository the tests must really run (14 result markers `... ok`, 0 `... skipped`), and at
  runtime they must skip cleanly (`OK (skipped=14)`, no `ERROR`, no `FAILED`). A guard that skips
  everywhere is worse than no guard, so the in-repo count is the half that proves the tests exist.
- **Count unittest result markers, not substrings — and only with `-v`.** Two opposite failures,
  same cause. A check written as `'skipped' in line` reported a skip that had not happened, because
  this very suite contains a test NAMED `test_pycache_and_pyc_are_skipped`; the name alone tripped
  the counter and the run was reported as defective. Running without `-v` removes the per-test
  lines entirely, so the same counter reads `ok=0, skipped=0` against a summary of
  `OK (skipped=14)` — again a defect that does not exist. Match on `... ok` / `... skipped` /
  `... FAIL` / `... ERROR`, run with `-v`, and assert `ok + skipped == Ran N`. Read the
  `Ran N tests` line's own suite before attributing a count: in one CI log `Ran 40 tests` was the
  tool suite containing the gate tests, while a nearby `Ran 14 tests in 0.006s` belonged to a
  scanner self-test in `__main__`, and taking the latter as evidence would have "proved" the gate
  tests ran when the numbers belonged to something else.
- **Derive a positive control's expectation from the text, not from the intent behind it.** A
  control mutated the real reference by replacing `at Hue\nUniversity of Education` with
  `at Some\nInstitute` and expected a finding, on the reasoning that the institution
  abbreviation inside the decision number would then sit on a line without citation
  framing. It expected 1 and got 0 — and the gate was right: the mutation
  left `Decision 1418` on the SAME line as that abbreviation, so the citation is still
  legitimately allowed, and `institution-3` no longer matched because its text had been
  replaced. Diagnosing it meant
  printing every pattern match with its allow decision and the line it came from, which separates
  "nothing matched" from "matched and was allowed" — two states that mean opposite things about a
  gate, and a control asserting only a finding count cannot tell them apart. The controls that
  actually proved the allowance narrow were different ones: appending an unframed mention to an
  allowed file must still fail, with exactly one finding, because the framed citation on its own
  line stays allowed. That is what shows the context test is per LINE and not per FILE — a
  distinction that silently collapses if the context is checked against normalised text, where a
  whole file is one line.
- **Measure whether an open PR is superseded, and test for conflict instead of inferring it.** An
  open PR touching 18 files that base had also changed looked like a rebase job. Two measurements
  replaced the guess. For supersession, take the lines the PR *adds* from each file's patch and
  count how many already appear in current base content: **166 of 167 (99.4%)** did, and the single
  missing line was an older `version: "3.12.0"` — so the content had landed another way and the PR
  was stale, not behind. For conflict, overlapping filenames prove nothing: `git merge-tree
  --write-tree --name-only <base> <head>` reported real content conflicts in only **2 of the 18**
  (exit 0 means clean, 1 means conflict). Report both numbers and let the owner decide; do not
  rebase or close a PR on a filename-overlap count, and never on a guess.

## Generalizing a lesson into a reference

A lesson learned on one manuscript is not a list from that manuscript. When
recording one:

- **Never re-narrow an existing section to the paper currently in hand.** A term
  that appeared in one manuscript is locked in that document's own glossary; it
  does not become policy.
- **Add a row to a polysemy or distinction table only when the same source word
  has been observed to split across fields**, not because one paper used it.
- **Persist a new lesson only as a test, an authority, a distinction, or a
  genre/audience rule** — never as another single-field word list. A word list
  rots; the test that would have caught the word does not.

## 5. Publishing

Branch, commit, push, open a pull request, wait for CI, then merge. The history here is
pull-request based, and a direct push to the default branch breaks that. Scan the
staged diff for secrets before committing: the fixtures deliberately contain
path-shaped and commit-hash-shaped strings, which are synthetic test data rather than
credentials and should be recognized as such rather than removed.

Bump the version in the `SKILL.md` frontmatter **in the same commit that changes the
content**, then reconcile the runtime copy so the two locations do not drift apart
again. Bump in both trees at once and compare them byte for byte afterwards; editing
only one recreates the drift this section exists to prevent, and the next sync
silently reverts whichever side was missed.

### The gate scans files, so it cannot see the two channels that go public with them

A commit message and a pull-request description are published on the repository's web
UI, are searchable, and are indexed -- yet neither is a file inside a tool directory,
so the hygiene gate never reads them. Scanning "the staged diff" before committing does
not cover them either, because a diff contains content, not the message that describes
it. Measured twice in one session: a commit message spelled out two codenames while
explaining that they had been removed from the content, and a pull-request body pasted
a real DOI as an illustrative example after the same identifier had just been
genericized out of the files it described. Both would have shipped with a green gate.

Scan all three channels before pushing, with the gate's own pattern table plus the
identifier classes the gate has no pattern for:

```
git rev-list <base>..HEAD | while read s; do git log -1 --format=%B $s; done
```

Refer to identifiers **by their gate label** in prose that goes public (`codename-4`,
not the token). The label carries the whole lesson; the token only carries the leak.

Two consequences worth knowing before you need them:

- **An unpushed commit message can still be fixed.** `git reset --hard HEAD~1`, then
  `git commit --amend -F <file>`, then `git cherry-pick` the commits that sat above it.
  Prove the rewrite changed nothing but the message by comparing tree hashes
  (`git rev-parse <backup>^{tree}` against `git rev-parse HEAD^{tree}`) -- create a
  backup branch first, since `reset --hard` discards the working state.
- **A pushed one cannot, cleanly.** Amending after a push rewrites public history and
  leaves the old text in every fork, in CI logs and in any notification that quoted it.
  Treat a leaked message as published the moment the push returns, and decide whether
  the identifier was sensitive enough to warrant a force-push conversation.

This rule was written and then not followed: three consecutive content commits
carried `3.13.0` unchanged, the last real bump having been `3.11.0 -> 3.13.0`. A
version that never moves cannot do the one job it exists for -- telling an installed
copy apart from the current one -- so treat an unchanged version on a content commit
as a defect in that commit. Choose the increment by what the change does to a
consumer: added sections and references that break nothing is a minor bump, not a
patch bump and not a major one.

Before bumping, check whether the version is hard-coded anywhere else
(`grep -rn '<old version>' scripts/ tests/`); here it was not, and `validate_skill.py`
asserts no particular value, so the bump could not break CI. Verify that rather than
assuming it, because a validator that pins the version turns a one-line edit into a
two-file change.

### This skill's home is the ai-agent-tools monorepo

Measured correction (user): academic-prose lives at `tools/academic-prose/` inside
`github.com/mxuanvan02/ai-agent-tools` — that is where updates go. A legacy
standalone repo `mxuanvan02/academic-prose` still exists and accepts pushes; pushing
there is not an error the remote will catch, so check the intended destination with
the user (or their latest instruction) before pushing. When syncing runtime →
monorepo with rsync, exclude `.git` and `__pycache__` so repo-owned assets are not
deleted by `--delete`. **Measured, the runtime tree DOES carry `evals/`, `tests/`,
`agents/`, `schemas/`, `README.md` and `scripts/validate_skill.py`** — they are
byte-identical to canonical, so an earlier claim here that it "does not carry them"
was wrong and is the reason a repo-structure test was written that could not run at
runtime (see the `tests/` pitfall in section 4). The single canonical-only file is
`scripts/public_hygiene_check.py`; never sync it to the runtime tree, and never write
a runtime test that assumes it is there.

## 6. Publishing when the host CLI cannot see the repository

`gh` installed as a snap is confined and cannot read a repository under a dotted
directory such as `~/.hermes/skill_repos/`; it fails with `not a git repository`
even from inside the worktree. Do not conclude the remote is misconfigured. Push
over SSH as normal, then create and merge the pull request through the REST API
with a token that carries repo scope:

```text
POST /repos/{owner}/{repo}/pulls          -> returns the PR number
GET  /repos/{owner}/{repo}/commits/{sha}/check-runs   -> wait for conclusion
PUT  /repos/{owner}/{repo}/pulls/{n}/merge
```

A confined `gh` also cannot read `/tmp`: snaps get a private mount, so
`--input /tmp/body.json` fails with `open /tmp/body.json: no such file or
directory` while `ls -l` shows the file present. The error looks like a missing
file, not like a confinement problem, so it invites a pointless rewrite of the
payload.

**Moving the file under `$HOME` is not sufficient, and this section previously said
it was.** The snap `home` interface excludes hidden paths, so
`gh pr create --body-file ~/.pr_body.md` fails with `permission denied` on a file
that `ls -l` shows as `-rw-rw-r--` and that the shell reads without complaint. Two
distinct symptoms, one cause:

| payload path | error |
| --- | --- |
| `/tmp/body.json` | `no such file or directory` (private `/tmp` mount) |
| `~/.pr_body.md` | `permission denied` (hidden paths excluded) |

The robust fix is to stop asking `gh` to open anything -- let the HOST shell read
the file and pipe the payload on stdin:

```bash
# Written on one line on purpose: this text lives inside a non-raw Python triple-quoted
# string, where a trailing backslash is a LINE CONTINUATION and would silently join the
# lines on the way into the file.
python3 -c 'import json,pathlib,sys; a=sys.argv; print(json.dumps({"title":a[1],"head":a[2],"base":a[3],"body":pathlib.Path(a[4]).read_text()}))' T H B /tmp/body.md > /tmp/payload.json
cat /tmp/payload.json | gh api repos/$OWNER/$REPO/pulls --method POST --input -
```

`json.dumps` also removes the shell-quoting problem for a body containing backticks,
`$`, or newlines. A non-hidden path under `$HOME` works too (`~/pr_body.md`, and the
same applies to job logs fetched with `gh api .../jobs/{id}/logs`), but stdin needs no
writable location the snap can see at all. Then verify from the remote rather than
from the push output: a failed create leaves the branch pushed and zero PRs, which
reads like success. Check for an existing PR on the same head first
(`GET /repos/{o}/{r}/pulls?head={owner}:{branch}&state=all`) -- retrying after a
confusing failure otherwise opens a duplicate.

Set the PR base from the remote's actual default branch, not from an assumed
`main`. A monorepo may keep its work on a long-lived feature branch as
`origin/HEAD`; `git fetch origin main` then fails with
`couldn't find remote ref main`. Check `git branch -r` and where `origin/HEAD`
points before choosing `base`.

**A default branch name may itself contain a slash**, and the obvious way to strip
the remote prefix destroys it. Measured: `origin/HEAD` resolved to
`origin/feat/ai-agent-tools-monorepo`, and `.split('/')[-1]` turned that into
`ai-agent-tools-monorepo` -- not a ref, so `git rev-parse` died with
`Needed a single revision` before a single file was touched. Strip the literal
`origin/` prefix and then verify the remainder resolves:

```python
ref = git('rev-parse', '--abbrev-ref', 'origin/HEAD')
base = ref[len('origin/'):] if ref.startswith('origin/') else ref
assert git('rev-parse', '--verify', '-q', 'origin/' + base, check=False)
```

**The clone may be single-branch and shallow**, which breaks the usual way of
confirming a push. Such a clone's fetch refspec covers only the default branch
(`git config --get-all remote.origin.fetch`), so after
`git push -u origin my-new-branch` the ref `origin/my-new-branch` does not resolve
locally and `git rev-parse origin/my-new-branch` fails -- while the push actually
succeeded. Ask the remote instead of the local ref store:

```bash
git ls-remote --heads origin my-new-branch   # prints the sha that is really there
git rev-parse HEAD                            # must equal it
```

`gh` printing "Create a pull request for ... by visiting" is a hint that the push
landed, not proof of it; and a `fatal: Needed a single revision` from
`rev-parse origin/<branch>` is not proof that it did not. Only `ls-remote` settles
it.

**`git branch -D` refuses to delete the branch a worktree currently sits on**
(`cannot delete branch ... used by worktree`). That is exactly the state an aborted
run leaves behind, so a retry script that wants to recreate its branch must detach
first: `git checkout -q --detach origin/$BASE`, then delete, then re-create.

Read the token from the host's own credential store rather than echoing it, and
never interpolate it into a shell string — a malformed assignment produced a
syntax error that leaked the surrounding command into the log. Wait for the CI
conclusion before merging; a `mergeable: clean` response says nothing about
whether the checks passed.

## 7. A red CI on your PR may be the base branch's fault

Read the failing job log before touching your change, and read the **base
branch's** log too. Fetch both by run/job id and compare the traceback:

```text
GET /repos/{o}/{r}/actions/runs?branch={b}&per_page=1  -> runs[0].id
GET /repos/{o}/{r}/actions/runs/{run}/jobs             -> jobs[0].id, step conclusions
GET /repos/{o}/{r}/actions/jobs/{job}/logs             -> the raw log
```

A docs-only PR that failed `validate` with
`ModuleNotFoundError: No module named 'defusedxml'` turned out to fail identically
on the base branch two days earlier — same step, same traceback. The workflow had
no dependency-install step at all, and the machine that wrote the skill happened
to have `defusedxml` and `python-docx` installed, so every local run passed. A
green local suite therefore proves nothing about the runner; it only proves the
host has the imports.

Fix the cause, not the symptom: declare the imports the scripts actually make in
a `requirements.txt` and install it in the workflow before the contract step.
Never skip, disable or `continue-on-error` the failing test to get a green tick —
the OOXML test exists because DOCX input is untrusted and parsing it with the
stdlib parser allows entity expansion.

Then prove the fix under runner conditions rather than host conditions: build a
fresh venv, confirm the missing imports are absent in it (reproducing the
failure), install the requirements file, and re-run **every** command the workflow
runs with the venv interpreter. Scripts that spawn subprocesses via
`sys.executable` make this meaningful — the child inherits the venv, so the whole
gate runs dependency-clean. Only commit once that passes.

Note also that a repository's own `.github/workflows/` copy inside a tool
directory is not what CI executes: GitHub Actions reads `.github/workflows/` at
the **repo root** only. Diff the two; a nested copy can silently list different
steps than the one actually running.

After merging a CI fix, confirm the **base branch itself** goes green — that is
what proves the fix was the cause, since the base was red before. And check that
the new check-run's `started_at` is *later* than the merge timestamp and its
`head_sha` is the merge commit: a green conclusion read too early can be an
inherited result from the PR head, not a fresh run on the merged base.
