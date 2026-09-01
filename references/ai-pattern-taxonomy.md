# AI Pattern Taxonomy Under Academic Constraint

This registry adapts the 35 patterns of Wikipedia's ["Signs of AI writing"](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), as codified by [blader/humanizer](https://github.com/blader/humanizer), to academic discourse. A general humanizer optimizes for natural voice. Academic prose additionally protects evidence, stance, scope, citations, terminology, and genre-mandated moves. Where the two conflict, integrity wins.

## Precedence

Insert AI-pattern removal into the standard priority chain as a late layer:

```text
claim and evidence integrity
-> terminology identity
-> scientific stance and scope
-> argument and discourse logic
-> genre and style-guide convention
-> target-language naturalness
-> AI-pattern removal
-> surface polish
```

A later layer may never repair itself by damaging an earlier one. Removing a pattern is not an improvement if it changes what the text claims, who claims it, how strongly, or under what conditions.

## Verdict vocabulary

| Verdict | Meaning |
| --- | --- |
| `apply` | remove the pattern in academic prose; no routine exception |
| `guard` | remove the pattern only after the stated academic exception is excluded |
| `redirect` | the surface form is an AI tell, but deletion is wrong; repair the underlying move instead |
| `restrict` | apply only within the stated narrow bound; the general form of the rule is unsafe here |
| `defer` | a declared style guide, template, or output format decides; do not normalize by default |

Every row names the blocking or major failure that an unguarded edit would cause. Those codes come from [Quality rubric](quality-rubric.md), [Writing failure taxonomy](writing-failure-taxonomy.md), and [Cross-language transfer taxonomy](cross-language-transfer-taxonomy.md). The gate that already governs writing and translation also governs humanizing; this table adds no separate enforcement path.

## Content patterns

| # | Pattern | Verdict | Academic exception | Risk if unguarded |
| --- | --- | --- | --- | --- |
| 1 | Inflated importance and legacy | `apply` | none | `promotional_contribution`, `unsupported_novelty` |
| 2 | Name-dropping to prove importance | `guard` | a citation is not name-dropping; venue prestige claims are | `citation_corruption` |
| 3 | Shallow analysis with -ing phrases | `apply` | none | `claim_without_warrant`, `empty_transition` |
| 4 | Sales language | `apply` | none | `register_drift`, `promotional_contribution` |
| 5 | Vague sources | `redirect` | mark the claim `needs_source`; do not silently delete it | `claim_without_status` |
| 6 | Formulaic challenges and outlook | `redirect` | Limitations and Future Work are mandated moves; repair, never cut | `ceremonial_limitation` |

**§2 detail.** Remove the prestige frame, keep the reference. `Được công bố trên một tạp chí uy tín thuộc nhóm Q1, nghiên cứu của Trần (2021) cho thấy...` becomes `Trần (2021) cho thấy...`. Deleting `(Trần, 2021)` is a blocking citation error.

**§5 detail.** `Nhiều nghiên cứu cho thấy phương pháp này hiệu quả hơn` with no reference is the pattern. The repair is a source or a `needs_source` entry, not deletion of the proposition. When the sentence does carry references, it is not this pattern.

**§6 detail.** Upstream cuts the challenges paragraph. Academic genres require it. The real failure is a limitation stated without its inferential consequence. Repair direction: `Nghiên cứu còn một số hạn chế nhất định.` becomes `Cỡ mẫu 42 người không cho phép suy rộng kết quả ra ngoài nhóm sinh viên năm nhất.`

## Language and grammar patterns

| # | Pattern | Verdict | Academic exception | Risk if unguarded |
| --- | --- | --- | --- | --- |
| 7 | Overused AI words | `guard` | established disciplinary terms keep their form | `terminology_error` |
| 8 | Avoiding is and are | `guard` | a copular frame may carry attribution | `attribution_shift` |
| 9 | Not X but Y and clipped negatives | `apply` | the contrast may be real; only the template is banned | `convergence_or_tension` loss |
| 10 | Forced groups of three | `guard` | three reported findings are data, not rhetoric | claim loss |
| 11 | Synonym cycling and repeated openings | `apply` | reinforces glossary identity; never add synonyms to break repetition | `terminology_drift` |
| 12 | False from X to Y ranges | `guard` | real numeric, date, and dose ranges are data | `numeric_corruption` |
| 13 | Passive voice and missing subjects | `restrict` | Methods may foreground procedure over actor | `attribution_shift` |

**§7 detail.** `key`, `landscape`, `gate`, `crucial`, and `interplay` are watched words in general prose and legitimate terms in cryptography, evolutionary biology, digital logic, continuous integration, and physics. Check the domain profile before rewriting. Vietnamese Sino-Vietnamese terms fixed by a field (`then chốt` in a quoted policy title, `nút thắt` in logistics) are terminology, not padding.

**§8 detail.** `X được xem là Y` may state that some community regards X as Y. Flattening it to `X là Y` transfers the claim to the author. Collapse the frame only when the source itself asserts identity.

**§10 detail.** When the text reports three measured outcomes, reducing them to two loses a claim. Collapse a triad only when its members are synonyms or ornaments.

**§13 detail.** Prefer an explicit actor when the actor is recoverable and naming it does not reassign the finding. `Các mẫu được ủ ở 37 °C trong 24 giờ` is correct Methods prose; forcing `Chúng tôi ủ các mẫu` is acceptable only if the venue permits first person and the authors did perform the step.

## Style patterns

| # | Pattern | Verdict | Academic exception | Risk if unguarded |
| --- | --- | --- | --- | --- |
| 14 | Em and en dashes | `restrict` | en dash is required in ranges, eponyms, and minus signs | `range_notation_corruption` |
| 15 | Too much bold text | `guard` | bold vectors, matrices, and template run-in headings are semantic | `placeholder_corruption` |
| 16 | Lists with bold mini-headings | `defer` | structured abstracts and slide layers are template-mandated | template violation |
| 17 | Title case in headings | `defer` | the journal or template style guide decides | `CONS` failure |
| 18 | Emojis | `apply` | only when an emoji is the object of study | none |
| 19 | Curly quotation marks | `defer` | the output format decides; LaTeX source differs from DOCX | `placeholder_corruption` |
| 26 | Too many hyphenated pairs | `guard` | chemical, gene, and eponymous compounds keep their hyphens | `terminology_error` |
| 27 | Pretending to reveal a deeper truth | `apply` | none | `register_drift` |
| 28 | Announcing the next point | `guard` | a thesis roadmap paragraph is a genre convention | genre violation |
| 29 | Heading repeated in the first sentence | `apply` | none | none |
| 30 | Writing about the previous version | `restrict` | Related Work, Background, and response letters are about prior work | claim loss |
| 31 | Forced punchlines and fragments | `apply` | none | `register_drift` |
| 32 | Formulaic sayings | `apply` | none | `unsupported_claim` |
| 33 | Fake-candid openings | `guard` | speaker notes and spoken delivery may open conversationally | none |
| 34 | Answering objections no one raised | `guard` | `evidence_boundary` and review responses do this legitimately | claim loss |
| 35 | Rejecting fake alternatives | `guard` | `alternative_explanation` is a required Discussion move | claim loss |

**§14 detail.** This is the highest-frequency corruption risk when humanizing academic text. The em dash rule stands for prose. The en dash must survive in every one of the following, and a hyphen is not an acceptable substitute where the source used an en dash:

- numeric and measurement ranges: `12–18 mg`, `p = 0,01–0,05`;
- page, table, figure, and date ranges: `tr. 145–162`, `2018–2023`;
- eponymous compounds naming two people: `Kaplan–Meier`, `Mann–Whitney U`, `Cox–Snell`;
- a minus sign or negative value in text;
- coordinate and axis notation copied from a figure or table.

In LaTeX sources, `--` and `---` are the encodings of en and em dash. Do not treat them as stray hyphens. Convert `---` to punctuation only when editing prose, and never inside math mode, `verbatim`, `lstlisting`, labels, keys, or bibliography fields.

**§17 and §19 detail.** These are format decisions, not voice decisions. When the task declares a target journal, template, or `.tex` versus `.docx` output, follow that declaration. Normalize only in the absence of a declared convention. Vietnamese academic headings default to sentence case with proper nouns preserved.

**§30 detail.** Apply to documentation prose that should describe current behavior. Suppress in Related Work, Background, a revision-response letter, and any section whose function is to characterize prior work. Deleting a comparison to earlier work removes the baseline that a bounded contribution depends on.

## Chatbot patterns

| # | Pattern | Verdict | Academic exception | Risk if unguarded |
| --- | --- | --- | --- | --- |
| 20 | Chatbot text left in the answer | `apply` | none | none |
| 21 | Knowledge-limit disclaimers and guesses | `restrict` | see the split below | `evidence_fabrication` or `evidence_boundary` loss |
| 22 | Overly agreeable tone | `guard` | conventional courtesy in a response-to-reviewers letter | none |

**§21 detail: the required split.** Upstream treats one pattern; academic use needs two verdicts.

- The speculative half is a blocking failure and must be removed without replacement. `Thông tin về quy mô mẫu không được nêu rõ, có thể nghiên cứu đã sử dụng khoảng 100 người tham gia` fabricates evidence. Remove the guess; state that the source does not report the sample size.
- The evidence-limit half is a legitimate `evidence_boundary` move and must be preserved. `Dữ liệu hiện có không cho phép xác định chiều của quan hệ này` is not an AI tell. Deleting it removes a scope statement the argument depends on.

The distinguishing test: does the sentence assert something the source does not support, or does it delimit what the available material can support? The first is fabrication. The second is scholarship.

## Filler and hedging

| # | Pattern | Verdict | Academic exception | Risk if unguarded |
| --- | --- | --- | --- | --- |
| 23 | Filler phrases | `apply` | none | none |
| 24 | Too many qualifiers | `restrict` | never reduce hedging to zero | `stance_upgrade`, `hedge_loss` |
| 25 | Generic positive endings | `guard` | a bounded implication or warranted research need is a real move | claim loss |

**§24 detail: the highest-risk rule in the set.** Calibrated hedging carries epistemic force in academic prose. A general humanizer treats hedges as filler; here, removing the last hedge is a blocking stance upgrade.

Permitted operation: collapse a stack to one calibrated marker.

- `Kết quả có thể có khả năng cho thấy một xu hướng nhất định` becomes `Kết quả có thể cho thấy một xu hướng`.
- `It could potentially be argued that the policy might have some effect` becomes `The policy may affect outcomes`.

Forbidden operation: reaching zero.

- `Phương pháp này có thể cải thiện độ chính xác` must not become `Phương pháp này cải thiện độ chính xác`.
- `may reduce` must not become `reduces`.

Before returning a humanized academic text, compare the modality of every consequential claim against the source or the claim ledger. Any strengthened claim is a block, regardless of how much better the sentence reads.

**§25 detail.** Cut `hứa hẹn nhiều triển vọng trong tương lai`. Keep `Kết quả này giới hạn ở nhóm bệnh nhân ngoại trú và cần được kiểm chứng trên cỡ mẫu lớn hơn`, which is a warranted `research_need`.

## Language-specific registries

The 35 patterns above are language-neutral in structure but their watched-word lists are English. Use the paired registries:

- [Vietnamese AI pattern registry](ai-pattern-vietnamese.md) for Vietnamese watched words, calques, and false positives.
- [Academic English standard](academic-english-standard.md) for English register, hedging inventory, and style-guide handling.

## Cross-check before delivery

1. Every consequential claim retains its modality, polarity, scope, attribution, and quantity.
2. No citation, DOI, URL, identifier, formula, unit, or protected token was altered.
3. Every en dash in a range, eponym, or negative value survived.
4. No Limitations, Future Work, evidence-boundary, or alternative-explanation move was deleted.
5. Locked terminology is unchanged and no ornamental synonym was introduced.
6. Declared style-guide and output-format conventions are intact.
7. Where the author supplied a writing sample, its rhythm and punctuation habits were followed instead of the default rules.

A humanized academic text that fails any of these is a regression, not a rewrite.
