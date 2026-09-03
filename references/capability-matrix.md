# Academic Prose Capability Matrix

The composition engine is the common core. It converts a rhetorical purpose,
claims, evidence, and constraints into an inspectable discourse architecture
before producing academic prose in the target language. Translation, PDF
processing, and surface rewriting are adapters; they do not define the skill's
primary capability.

| Capability | Use when | Required operation | Output |
| --- | --- | --- | --- |
| `conceptualize` | a topic, problem, or research material is not yet a defensible writing task | delimit the question, audience, purpose, concepts, assumptions, and evidence gaps | rhetorical brief + candidate claim structure |
| `outline` | the user needs a section, chapter, article, thesis, or report architecture | map section functions and claim dependencies, not merely topic headings | annotated outline + unresolved evidence |
| `argue` | a position must be justified or bounded | construct claim-evidence-warrant-qualification relations and credible counterpositions | argument map + prose plan |
| `synthesize` | multiple supplied sources or findings must become one account | compare them through shared dimensions; distinguish convergence, tension, and absence of evidence | thematic synthesis + source boundaries |
| `draft` | sufficient claims and evidence exist for new prose | design paragraphs and realize the planned rhetorical moves | clean academic text + evidence status |
| `develop` | a note, claim, paragraph, or section is underdeveloped | add only warranted evidence, warrants, qualification, and transitions | fuller argument without invented content |
| `compress` | text must be shortened | preserve the claim hierarchy, evidence status, stance, scope, and essential qualifications | shorter text + material omissions disclosed |
| `expand` | text must be longer or more explicit | expose implicit warranted steps and mark missing support instead of padding | expanded text + `needs_source` items |
| `paraphrase` | wording must change while content remains stable | preserve propositions, attribution, terminology, stance, scope, and citation anchors | reformulated academic prose |
| `humanize` | prose carries machine tells but its claims are already settled | remove AI patterns under the academic precedence chain without touching evidence, stance, scope, or protected elements | de-slopped text + pattern log + surface-rewriting gate |
| `revise` | an existing draft needs substantive improvement | diagnose and repair architecture, evidence placement, coherence, stance, and sentence realization | revised text + change audit |
| `audit` | quality or compliance must be assessed without silent rewriting | inspect claims, evidence, rhetorical moves, terminology, logic, machine tells, and target-language expression | severity-ranked findings + gate decision |
| `translate` | scholarly content must move between English and Vietnamese | map source claims into the same composition engine, then reconstruct natural prose in the target language | faithful target-language text + glossary + audit |

## Routing Contract

- Default to `draft` when the user asks to write and supplies adequate material.
- Start with `conceptualize` or `outline` when the writing task or evidence base is
  not yet coherent. Do not hide missing decisions by generating polished prose.
- Route literature provided by the user to `synthesize`; this skill does not
  search for missing literature or invent citation metadata.
- Route shortening, expansion, and paraphrase through the existing claim ledger.
  These are semantic transformations, not surface-only rewriting.
- Use `translate` when a source-language text is an input, in either direction.
  Declare the target language; it selects the target-language standard and the
  `LANG` scoring reference. Pair translation with a PDF tool only when
  extraction or reconstruction is also required.
- Terminology localization is not confined to `translate`. Authored text carries
  source-language terms for the same reason translated text does, so `draft`,
  `develop`, `revise`, and `audit` all run the localization decision and gate;
  see [Terminology localization policy](terminology-localization.md).
- The translation adapter explicitly covers both English-to-Vietnamese and
  Vietnamese-to-English academic transfer. Keep one claim ledger and glossary
  across the pair; direction changes the target-language realization, not the
  evidence or stance contract.
- Use `humanize` only when the claims are settled and the defect is surface
  register. When the text also has evidence, architecture, or stance problems,
  route to `revise` and treat pattern removal as its final layer.

## Humanize versus revise versus paraphrase

These three are easy to confuse and have different licenses.

| | Changes propositions | Changes structure | Changes wording | Typical trigger |
| --- | --- | --- | --- | --- |
| `humanize` | never | only paragraph-internal merges | yes | text reads as machine-generated |
| `revise` | may correct unsupported claims | yes | yes | argument or evidence placement is wrong |
| `paraphrase` | never | no | yes | wording must differ, register is already fine |

`humanize` is the narrowest of the three. It may merge or split a paragraph and
delete an empty sentence, but it may not add a claim, remove a supported one,
change who owns a claim, or alter how strongly it is stated. Read
[AI pattern taxonomy](ai-pattern-taxonomy.md) before running it, and apply the
surface-rewriting gate in [Quality rubric](quality-rubric.md) before delivery.

Every capability that introduces or reorganizes a consequential claim must use
the rhetorical brief, claim-evidence ledger, and paragraph plan at a depth
proportional to the task. Short edits may keep those artifacts implicit, but the
same evidence and no-fabrication constraints still apply.

The capability describes the semantic operation, not the final medium. Apply
the same operation to manuscripts, reports, slide content, speaker notes, bài
giảng, học liệu, đề cương, and assessment items. For structured deliverables,
use `deliverable-playbooks.md` to adapt density, sequencing, and content layers
without weakening the common quality gate.
