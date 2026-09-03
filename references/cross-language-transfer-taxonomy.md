# Cross-Language Transfer Taxonomy

Use these labels when auditing academic text that crossed a language boundary in
either direction. Detection is contextual; examples are diagnostic, not blind
replacement rules.

Transfer errors are distinct from AI-pattern tells. A calque is a transfer error
even in a text written by a human translator; a ceremonial adjective is an
AI tell even in a text that was never translated. When both apply to the same
span, repair the transfer error first, because it changes meaning.

They are also distinct from a terminology decision. Whether a term should be
translated at all, kept as a designator, or glossed is not an error in transfer;
it is a policy fixed once per concept in the glossary. `terminology_error` and
`terminology_drift` below presuppose that decision has been made. When a source
term appears untranslated in target-language prose, or a designator appears
translated, classify it under
[Terminology localization policy](terminology-localization.md) rather than as a
calque.

## Direction-neutral errors

These occur in both directions.

| Code | Error | Signal | Repair principle |
| --- | --- | --- | --- |
| `terminology_error` | the source term is assigned the wrong domain meaning | a thermal property is rendered as an electrical property | recover the concept from definition, domain, and argument context |
| `terminology_drift` | one concept receives ornamental synonyms | the reader may infer different constructs | enforce glossary identity |
| `register_drift` | journalistic, bureaucratic, conversational, or promotional tone | tone mismatches the genre | restore restrained disciplinary register |
| `hedge_loss` | modality disappears | `may suggest` becomes an assertion | restore epistemic force |
| `causal_upgrade` | association becomes cause | `associated with` becomes `gây ra` | preserve the relation type |
| `scope_shift` | population, condition, time, comparator, or quantifier changes | a local result sounds universal | restore explicit scope |
| `attribution_shift` | source ownership changes | a cited claim sounds like the author's finding | restore the attribution boundary |
| `explicitation_without_license` | the translator adds plausible detail | the source does not entail the addition | remove it or place it in a separate note |
| `connector_inflation` | a logic marker is added | the causal or contrastive relation is not licensed | remove it or use a neutral transition |
| `pronoun_ambiguity` | a pronoun lacks a clear antecedent | competing candidates | repeat the precise noun phrase |
| `number_format_transfer` | numeric convention is not converted, or is converted where it must not be | `0.847` appears in Vietnamese prose, or `0,847` in English prose | apply the target convention to prose and preserve it inside protected tokens |

`number_format_transfer` needs care in both directions. Vietnamese academic
convention uses a decimal comma and a period as thousands separator (`0,847`,
`1.250.000`); English uses the reverse. Convert running prose. Do not convert a
value inside a quoted string, a code block, a dataset identifier, a DOI, or a
figure label copied verbatim.

## English to Vietnamese

| Code | Error | Signal | Repair principle |
| --- | --- | --- | --- |
| `dummy_subject` | literal `it`/`there` subject | `nó được phát hiện rằng` | name the evidence or use the proposition directly |
| `nominalization_stack` | chained `sự`/`việc`/`quá trình` | the action is hidden inside nouns | restore a verb and actor where licensed |
| `passive_transfer` | pervasive `được`/`bị` | no discourse reason for the passive | choose active or topic-comment structure |
| `literal_collocation` | words are correct separately but unnatural together | `chơi vai trò`, `cam kết với trích dẫn` | translate the whole predicate-argument unit |
| `preposition_transfer` | a copied English relation | `đối chiếu chống lại` | select the Vietnamese semantic relation |
| `modifier_overload` | a long prenominal chain | referents become ambiguous | unpack modifiers into clauses or postmodifiers |

## Vietnamese to English

Vietnamese is a topic-prominent, isolating language with optional subjects and
no tense morphology. English requires an explicit subject and a tense choice.
That asymmetry produces errors that have no English-to-Vietnamese counterpart.

| Code | Error | Signal | Repair principle |
| --- | --- | --- | --- |
| `topic_comment_transfer` | a Vietnamese topic-comment sentence becomes an English fragment | `Về phương pháp, nghiên cứu dùng thiết kế cắt ngang` becomes `About the method, the study used...` | recast as subject-predicate: `The study used a cross-sectional design.` |
| `zero_subject_transfer` | Vietnamese subject ellipsis leaves English without a subject | `Sau đó đo lại sau sáu tuần` becomes `Then measured again after six weeks` | recover the actor from context, or use a licensed passive |
| `classifier_residue` | a Vietnamese classifier or light noun is rendered literally | `sự gia tăng của việc sử dụng` becomes `the increase of the usage` | drop the classifier and use the English noun or verb |
| `aspect_underspecification` | a tense or aspect is guessed because Vietnamese does not mark it | a reported result appears in the present tense, implying a standing fact | derive tense from the section function: Methods and Results past, established knowledge present |
| `plurality_underspecification` | Vietnamese unmarked number becomes a guessed English plural or singular | `mẫu` becomes `the sample` where the source means several samples | resolve from the reported quantity, or mark it unresolved |
| `sino_vietnamese_overtranslation` | a Sino-Vietnamese term is rendered with an inflated Latinate word | `khả thi` becomes `eventuates as practicable` instead of `feasible` | choose the ordinary disciplinary English term |
| `honorific_residue` | Vietnamese address or courtesy forms enter English academic register | `kính thưa`, `chúng em`, `quý thầy cô` in a manuscript | remove; keep them only in a spoken-delivery script |

`aspect_underspecification` is the most consequential of these, because a tense
choice can convert a bounded finding into a general claim. `Mô hình đạt độ chính
xác 94%` renders as `The model achieved 94% accuracy` when reporting this
study's result, and as `The model achieves 94% accuracy` only if the claim is a
standing property. The second form asserts more than the first.

## Severity

- `block`: changes truth conditions, evidence ownership, stance, scope, quantity, or protected content.
- `major`: materially impairs terminology, logic, or interpretation.
- `minor`: unnatural or inefficient target-language prose without semantic damage.

Fluency is not evidence of correctness. A smooth causal upgrade remains a
blocking error, and so does a fluent tense choice that turns a measured result
into a general law.

## Interaction with AI-pattern removal

When a text is both translated and humanized, run the transfer audit before the
AI-pattern pass, and re-run the stance check after it. Two failure modes recur:

1. Removing a calque also removes a hedge. `Nó có thể được cho là có liên quan
   đến` is a stack of transfer errors and hedges. The repair keeps one hedge:
   `có thể liên quan đến`. Reaching `liên quan đến` alone is `hedge_loss`.
2. Removing ceremonial vocabulary also removes attribution. `Theo một số tác
   giả, phương pháp này đóng vai trò quan trọng` should become `Theo một số tác
   giả, phương pháp này quan trọng`, not `Phương pháp này quan trọng`. The
   second drops `attribution_shift` protection.

See [AI pattern taxonomy](ai-pattern-taxonomy.md) for the precedence chain that
governs this interaction.
