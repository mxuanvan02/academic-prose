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
