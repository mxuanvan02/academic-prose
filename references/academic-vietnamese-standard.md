# Academic Vietnamese Standard

## Priority

The priority order is: **meaning -> terminology -> scientific stance -> logic -> Vietnamese expression -> surface polish**. A later layer may not damage an earlier one.

## Sentence-Level Criteria

1. **Propositional completeness**: identify who or what performs, experiences, measures, or supports the stated relation.
2. **Predicate fitness**: choose Vietnamese verbs that collocate with the object and discipline; do not translate an English verb independently of its argument.
3. **Information structure**: place established context before new information when possible; keep the sentence focus visible.
4. **Controlled density**: split a sentence when embedded clauses obscure claim boundaries, but preserve their logical relation.
5. **Economy**: remove empty frames such as `có một nhu cầu để`, `tiến hành việc thực hiện`, or `mang tính chất`, unless they carry a real distinction.

## Paragraph-Level Criteria

- Each paragraph has a discernible function: frame, claim, evidence, interpretation, contrast, limitation, or implication.
- Pronouns and omitted subjects have unambiguous antecedents.
- Connectives represent relations present in the argument; do not insert `do đó` merely to improve flow.
- Repetition of a technical term is preferable to ornamental synonym substitution.
- A paragraph must not merge the author's findings with cited findings or speculation.

## Scientific Stance

Preserve the source's epistemic force:

| Source function | Typical Vietnamese | Forbidden upgrade |
| --- | --- | --- |
| reports an observation | `kết quả cho thấy`, `ghi nhận` | `chứng minh` |
| suggests an interpretation | `gợi ý`, `có thể cho thấy` | `khẳng định` |
| association | `có liên quan đến` | `dẫn đến`, `gây ra` |
| possibility | `có thể` | unqualified assertion |
| limitation | `chỉ áp dụng`, `không cho phép suy rộng` | vague `cần thận trọng` |
| recommendation | `đề xuất`, `nên xem xét` | `bắt buộc`, `cần phải` |

## Register

Use precise contemporary Vietnamese. Formality does not require archaic wording, excessive Sino-Vietnamese vocabulary, long nominal chains, or pervasive passive voice. Avoid promotional adjectives (`đột phá`, `vượt trội`) unless they are explicitly attributed and evidenced.

### Avoid label-driven prose

Do not turn ordinary argument into a sequence of labels followed by colons, such as `Hướng thứ nhất: ...`, `Giới hạn: ...`, `Câu hỏi nghiên cứu: ...`, or bold lead-ins of the form `**Thứ nhất, ...:**`. State the proposition directly and connect it to the surrounding argument in complete sentences. Likewise, do not compress several substantive points or answer options into an `A–B–C–D` chain separated by semicolons when natural sentences, a table, or a genuine list would be clearer.

This rule concerns prose, not required document structure. Preserve venue-mandated labels such as `Tóm tắt:`, `Từ khóa:`, `Abstract:`, and `Keywords:`, exact titles and quotations, bibliographic punctuation, table syntax, and colons that introduce material naturally. During revision, audit author-written body prose separately from these protected zones; do not alter required labels or source titles merely to make a pattern scan return zero.

When a user rejects label-driven writing, sweep the whole document rather than fixing only the cited sentence. Check headings, overview paragraphs, methods, examples, recommendations, conclusion, and both language versions. Preserve the claim, citation anchor, qualification, and logical relationship while changing only the realization.

### Formal terminology for adversarial and security contexts

When writing about fraud detection, adversarial scenarios, or security threats in Vietnamese academic prose, avoid colloquial or dramatic terms. Use formal, precise alternatives that reflect the technical nature of the work.

| Informal/Colloquial | Formal/Academic | Rationale |
| --- | --- | --- |
| đối thủ | tác nhân đe dọa, thực thể đối kháng | "Đối thủ" implies personal rivalry; "tác nhân" is neutral and technical |
| gian lận ngây thơ | gian lận cơ bản, gian lận đơn giản | "Ngây thơ" is anthropomorphic and informal |
| bên gian lận | tác nhân gian lận, thực thể gian lận | "Bên" is colloquial; "tác nhân" or "thực thể" is more formal |
| tấn công | kịch bản gian lận, hành vi gian lận, phương thức gian lận | "Tấn công" is dramatic; in fraud detection contexts, "kịch bản" or "hành vi" is more precise |
| kẻ gian | tác nhân gian lận | "Kẻ" has negative moral connotation; use neutral technical terms |
| lừa đảo | gian lận | "Lừa đảo" is colloquial; "gian lận" is the standard academic term |

**Why this matters:** Academic prose should describe phenomena objectively and technically. Colloquial terms introduce emotional or moral framing that is inappropriate for scientific writing. In adversarial machine learning and fraud detection, the focus is on characterizing behaviors and mechanisms, not on moral judgment.

**When to apply:** This rule applies to any discussion of fraud, adversarial behavior, security threats, or attack scenarios in Vietnamese academic prose. It does not apply to quoted material, proper nouns, or when discussing historical events where colloquial terms are part of the primary source.

**Test:** Read the sentence aloud. Does it sound like a news report or a technical paper? If it sounds dramatic or emotional, recast using formal terminology.

## Publication-Facing Abstraction

In publication-facing prose, express the research object, procedure, and data
structure through disciplinary concepts. Do not expose schema field names,
configuration keys, internal flags, directory names, or pipeline labels merely
because they occur in code or technical documentation. Retain a software tool,
model name, parameter, or identifier only when it is necessary for
reproducibility, identifies the object under study, or prevents substantive
ambiguity. Put operational lookup details in the data card, repository,
appendix, or other technical documentation instead of the main argument.

This abstraction must not conceal a consequential methodological choice. For
example, report that records were split at document level and that answer
positions were deterministically balanced; the internal names of the fields
that store those values are normally unnecessary.

## Number Format Is Template-Owned

The Vietnamese default decimal separator is the comma (`0,847`). This default is
a voice rule, not a claim rule, and it yields to a declared style guide or
institutional template. Do not rewrite a decimal separator, thousands separator,
or range notation unless the declared template asks for it.

Declare the number format in the rhetorical brief before any `revise`,
`humanize`, or `audit` pass. When the brief is silent, ask instead of
normalising.

Worked case. Vietnamese theses written to Decision 1418/QĐ-ĐHSP at Hue
University of Education use the decimal **point** and wrap each numeral in
inline math, as in `$18.2\%$` and `$58.8$--$75.3\%$`, so that table values match
figures generated by plotting libraries. Converting those to `18,2\%` would
break agreement between a table and the figure on the same page, so the point is
correct in that template. A related trap: TikZ coordinates such as `(5.1,0)` and
`(4.2,2.55)` are notation, not data. Rewriting them destroys the drawing.

## Punctuation: no em dash in Vietnamese academic prose

Vietnamese scholarly prose does not use the em dash (`—`) as a parenthetical or
appositive marker the way English does; it is an anglicism and reads as machine
writing. Measured case: a HUJOS manuscript carried 16 em dashes across two source
files, all introduced during rewrite rounds, and the author flagged them as a
defect. Repair by construction type, never by a blind global replace:

| Construction | Repair |
| --- | --- |
| `A — B — C` (parenthetical pair) | `A (B) C`, or `A, tức B, C` when B is a restatement |
| `A — B` introducing a list or an explanation | a full stop and a new sentence, or `A, gồm B` for an enumeration |
| `A — B` where B is an independent clause | `A; B`, adding the subject B needs (`; việc xác nhận cần…`) |
| `A — B` where B is a loose appositive | `A, B` or `A, một B…` |

**Do not repair a dash into a colon.** The obvious substitute is `A: B`, and it trades
one anglicism for another: the explanatory colon is the second half of the same
English punctuation habit, and a manuscript can pass a zero-em-dash check while
reading as translated because every repaired dash became a colon. A HUJOS
comparative-literature manuscript reached zero em dashes this way and still had to
be swept again to remove the colons the repair had introduced. When the target is
Vietnamese prose, prefer a full stop, or a connective that names the real
relation (`vì`, `khi`, `gồm`, `cụ thể là`, `tức là`). Reserve the colon for
venue-mandated labels and for a genuine one-off enumeration.

**Verify on the rendered PDF, and count characters — not bytes.** A `.tex` sweep that
reports zero `---` can still leave em dashes that came from a macro, a generated
table file, or a `.bbl`. Count in the PDF text layer:

```
pdftotext out.pdf - | python3 -c "import sys; print(sys.stdin.read().count('\u2014'))"
```

`tr -cd '—' | wc -c` is wrong: it counts UTF-8 bytes, and an em dash is three bytes,
so one surviving dash reports as 3 and a page of them as 185. Two survivors are
legitimate and must not be "fixed": an en dash inside a numeric range (`41–71%`,
`9–12`) or compound name (`Benjamini–Hochberg`), and any dash inside a reference
title (`Crop Evapotranspiration — Guidelines…`) — citation zones are immutable.
Comment rules (`% ----------`) never render; exclude them from the source count.

**A spaced hyphen is the same defect.** ` - ` used as a sentence-level dash
(`Thần linh quyết định - biến hình trong…`, `một bên - một bên`) is an em dash
with different characters, and the author rejects it as flatly as the em dash.
Count all three forms before and after a sweep:

```bash
grep -c "—" file.md            # em dash
grep -c " - " file.md          # spaced hyphen used as dash
grep -o "–" file.md | wc -l    # en dash: notation, must survive in ranges
```

A spaced hyphen inside a hyphenated compound (two institutional names joined by a
spaced hyphen) or inside a bibliographic range is notation, not prose; adjudicate
those rather than rewriting them.

En dashes in ranges (`mục 3.2–3.3`, `tr. 145–162`, `2018–2023`) are notation and
must survive; see [ai-pattern-taxonomy.md](ai-pattern-taxonomy.md) §14. Count the
em dashes before and after, and confirm zero remain — the count is the check, not
a re-read.

**The zero-count check has one legitimate exception: registered proper names.** An
em dash inside a journal or publisher name is part of the title, not prose. A
sweep that reported "1 em dash remaining" after the prose was already clean turned
out to be `CBE—Life Sciences Education` in the reference list; Crossref
`container-title` returned the identical string with the em dash. So scope the
final count to the prose files, and when a residual dash appears in the built
PDF, locate it and resolve it against the registry before reporting it as a
defect — "fixing" it would corrupt a citation.

Also unify borrowed technical nouns that already have a standard Vietnamese term
(`gate` → `cổng kiểm soát`) in the same pass; a mixed register inside one
paragraph is what makes reviewers suspect machine authorship.

## No "Title: Subtitle" colon in Vietnamese headings and titles

The colon-separated title/subtitle pattern is an English academic convention.
Vietnamese journal titles and section headings read as noun phrases or as a
heading linked by a preposition; a colon in a heading is an anglicism. Measured
case: a manuscript title audit found the title itself clean but one newly added
appendix heading carrying `Tình huống minh họa thứ hai: quy định chuyển tiếp và
tiêu chí 5` — introduced by the reviser, not the author.

Repair: replace the colon with `về`, `đối với`, or fold the two parts into one
noun phrase. Scope the sweep to headings and captions, not the whole file:

```python
import re
for m in re.finditer(r'(?m)^(#{1,4})\s+(.*)$', src):
    if ':' in m.group(2): print(m.group(2))   # must be empty at the end
```

**Do not extend this rule to journal-mandated label lines.** `**Tóm tắt:**`,
`**Từ khóa:**`, `**Abstract:**`, `**Keywords:**`, and the corresponding-author
line are format fields, not headings; their colons are required by the venue and
removing them fails the format audit. Verify both directions after the sweep:
zero headings with a colon, and each mandated label still present exactly once.

## Natural Vietnamese Voice (hồn tiếng Việt)

Vietnamese academic prose must sound like a Vietnamese scholar wrote it, not like a translation. The three rules that carry most of the weight:

1. **Self-reference in the right register.** The manuscript names itself as "nghiên cứu này", "nghiên cứu", or "công trình này", never as "bài" and never as "bài báo" in the middle of a sentence. The bare first person "ta" is replaced by "chúng tôi". See [Vietnamese AI pattern registry](ai-pattern-vietnamese.md) §11 for the repair table and the licensed compound nouns.
2. **Passive → active when the author is the actor.** Vietnamese prefers explicit actors, and a manuscript that hides its own actions behind `bị`/`được` reads as impersonal reporting. Keep the passive when the affected object is the discourse focus.
3. **Explicit subject for author actions.** A sentence describing what the authors did names the actor: "Khi chúng tôi dựng lại thửa ruộng…, kết luận thay đổi", not "Dựng lại thửa ruộng… đã thay đổi kết luận".

Do not add "chúng tôi" when the sentence is about the object under study rather than the authors' action, and do not insert it to satisfy a rule: Vietnamese licenses subject ellipsis far more freely than English.

### Pre-drafting gate: No word-by-word translation from English

Before drafting Vietnamese academic prose, verify that the writer is **thinking in Vietnamese**, not translating from English. This gate catches the most common failure mode: fluent Vietnamese sentences that are structurally English.

**General principles (not exhaustive rules):**

1. **Head-initial structure.** Vietnamese noun phrases place the head noun first, followed by modifiers. English does the opposite. When a Vietnamese phrase reads as a direct word-order mirror of English (modifier before head), it signals translation rather than composition. The test: can you identify the head noun, and do the modifiers follow it naturally? If the phrase feels "backwards" or requires mental reordering to parse, recast it.

2. **Verb-object collocation follows Vietnamese patterns, not English.** Every language has preferred verb-object pairings that are partly conventional, partly semantic. A Vietnamese verb that collocates naturally with one object may sound awkward with another, even when the English equivalent works. The test: does this verb-object pair appear in Vietnamese academic corpora, or does it feel like a calque? When in doubt, consult usage or recast the phrase.

3. **Number style follows Vietnamese convention, not English.** Vietnamese academic prose writes small numbers (typically 1-10, sometimes up to 12) as words in running text, and uses digits for larger numbers, measurements, and data. The boundary is conventional, not absolute; what matters is consistency and readability. The test: would a Vietnamese reader expect this number as a word or a digit in this context?

**Linguistic rationale:**

These principles exist because Vietnamese and English have different syntactic structures, different collocational conventions, and different number-writing traditions. A text that follows English patterns while using Vietnamese words reads as translated, not composed. The goal is not to forbid all English-influenced constructions—some are naturalized—but to catch cases where the English structure is still visible.

**Illustrative examples (not prescriptive):**

- Head-initial: "cơ chế hiệu chỉnh lặp qua phản hồi chuyên gia" (mechanism of iterative calibration through expert feedback) reads naturally; "phản hồi chuyên gia lặp" (expert feedback iterative) mirrors English order.
- Collocation: "tiến hành cải tiến" (conduct improvement) is natural; "thực hiện cải tiến" (implement improvement) is less common but not wrong. Context matters.
- Number style: "bốn câu hỏi" (four questions) in prose; "4.668 câu hỏi" (4,668 questions) for data. The boundary is conventional.

**Permitted exceptions:**

- Technical terms that have been naturalized (e.g., "machine learning" → "học máy" is standard; some fields retain English terms).
- Proper nouns, citations, and quoted material.
- Cases where the English structure has become conventional in Vietnamese academic prose through widespread use.

**Verdicts:**

- `word_by_word_translation`: The phrase mirrors English structure and reads as translated. Repair by recasting in natural Vietnamese word order.
- `collocation_mismatch`: The verb-object pair is unusual or absent from Vietnamese academic corpora. Repair by substituting a more natural collocation or recasting.
- `number_style_inconsistency`: Numbers are written inconsistently with Vietnamese convention. Repair by normalizing.

**Run this gate on every `draft`, `translate`, and `revise` delivery in Vietnamese.** A clean gate is a partial verification only; combine with the AI-pattern scan and the plain-reader pass. The gate is a heuristic, not a parser: use judgment, not pattern matching.

## Protected Elements

Whether a required foreign term is translated, kept, or glossed is decided by
[Terminology localization policy](terminology-localization.md), recorded once per
concept in the glossary, and enforced across the document. The abstraction rule
above removes implementation tokens with no publication-facing function; it does not
license translating a name that carries the identity of an external object.

When a protected element is substantively required, copy formulas, symbols,
values, units, citations, DOI, URLs, code, dataset names, model names, quoted
text, and structured placeholders exactly unless the task explicitly changes
their formatting. Preservation does not require including implementation
tokens that have no publication-facing function.
