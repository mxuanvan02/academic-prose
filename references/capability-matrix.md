# Vietnamese Academic Capability Matrix

The composition engine is the common core. It converts a rhetorical purpose,
claims, evidence, and constraints into an inspectable discourse architecture
before producing Vietnamese prose. Translation and PDF processing are adapters;
they do not define the skill's primary capability.

| Capability | Use when | Required operation | Output |
| --- | --- | --- | --- |
| `conceptualize` | a topic, problem, or research material is not yet a defensible writing task | delimit the question, audience, purpose, concepts, assumptions, and evidence gaps | rhetorical brief + candidate claim structure |
| `outline` | the user needs a section, chapter, article, thesis, or report architecture | map section functions and claim dependencies, not merely topic headings | annotated outline + unresolved evidence |
| `argue` | a position must be justified or bounded | construct claim-evidence-warrant-qualification relations and credible counterpositions | argument map + prose plan |
| `synthesize` | multiple supplied sources or findings must become one account | compare them through shared dimensions; distinguish convergence, tension, and absence of evidence | thematic synthesis + source boundaries |
| `draft` | sufficient claims and evidence exist for new prose | design paragraphs and realize the planned rhetorical moves | clean Vietnamese academic text + evidence status |
| `develop` | a note, claim, paragraph, or section is underdeveloped | add only warranted evidence, warrants, qualification, and transitions | fuller argument without invented content |
| `compress` | text must be shortened | preserve the claim hierarchy, evidence status, stance, scope, and essential qualifications | shorter text + material omissions disclosed |
| `expand` | text must be longer or more explicit | expose implicit warranted steps and mark missing support instead of padding | expanded text + `needs_source` items |
| `paraphrase` | wording must change while content remains stable | preserve propositions, attribution, terminology, stance, scope, and citation anchors | reformulated Vietnamese academic prose |
| `revise` | an existing Vietnamese draft needs substantive improvement | diagnose and repair architecture, evidence placement, coherence, stance, and sentence realization | revised text + change audit |
| `audit` | quality or compliance must be assessed without silent rewriting | inspect claims, evidence, rhetorical moves, terminology, logic, and Vietnamese expression | severity-ranked findings + gate decision |
| `translate` | English scholarly content must become Vietnamese | map source claims into the same composition engine, then reconstruct natural Vietnamese discourse | faithful Vietnamese text + glossary + audit |

## Routing Contract

- Default to `draft` when the user asks to write and supplies adequate material.
- Start with `conceptualize` or `outline` when the writing task or evidence base is
  not yet coherent. Do not hide missing decisions by generating polished prose.
- Route literature provided by the user to `synthesize`; this skill does not
  search for missing literature or invent citation metadata.
- Route shortening, expansion, and paraphrase through the existing claim ledger.
  These are semantic transformations, not surface-only rewriting.
- Use `translate` only when a source language text is an input. Pair it with a
  PDF translation tool only when extraction or reconstruction is also required.

Every capability that introduces or reorganizes a consequential claim must use
the rhetorical brief, claim-evidence ledger, and paragraph plan at a depth
proportional to the task. Short edits may keep those artifacts implicit, but the
same evidence and no-fabrication constraints still apply.

The capability describes the semantic operation, not the final medium. Apply
the same operation to manuscripts, reports, slide content, speaker notes, bài
giảng, học liệu, đề cương, and assessment items. For structured deliverables,
use `deliverable-playbooks.md` to adapt density, sequencing, and content layers
without weakening the common quality gate.
