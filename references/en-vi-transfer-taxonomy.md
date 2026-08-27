# English-to-Vietnamese Transfer Taxonomy

Use these labels in audits. Detection is contextual; examples are diagnostic, not blind replacement rules.

| Code | Error | Signal | Repair principle |
| --- | --- | --- | --- |
| `dummy_subject` | literal `it/there` subject | `nó được phát hiện rằng` | name the evidence or use the proposition directly |
| `nominalization_stack` | chained `sự/việc/quá trình` | action hidden inside nouns | restore a verb and actor where licensed |
| `passive_transfer` | pervasive `được/bị` | no discourse reason for passive | choose active or topic-comment structure |
| `literal_collocation` | words are correct separately but unnatural together | `chơi vai trò`, `cam kết với trích dẫn` | translate the whole predicate-argument unit |
| `preposition_transfer` | copied English relation | `đối chiếu chống lại` | select the Vietnamese semantic relation |
| `modifier_overload` | long prenominal chain | referents become ambiguous | unpack modifiers into clauses or postmodifiers |
| `pronoun_ambiguity` | `nó/điều này` lacks a clear antecedent | competing candidates | repeat the precise noun phrase |
| `connector_inflation` | added logic marker | causal/contrast relation not licensed | remove or use a neutral transition |
| `terminology_error` | source term is assigned the wrong domain meaning | a thermal property is rendered as an electrical property | recover the concept from definition, domain, and argument context |
| `terminology_drift` | one concept receives ornamental synonyms | reader may infer different constructs | enforce glossary identity |
| `register_drift` | journalistic, bureaucratic, conversational, or promotional tone | tone mismatches genre | restore restrained disciplinary register |
| `hedge_loss` | modality disappears | `may suggest` becomes assertion | restore epistemic force |
| `causal_upgrade` | association becomes cause | `associated with` -> `gây ra` | preserve relation type |
| `scope_shift` | population, condition, time, comparator, or quantifier changes | local result sounds universal | restore explicit scope |
| `attribution_shift` | source ownership changes | cited claim sounds like author's finding | restore attribution boundary |
| `explicitation_without_license` | translator adds plausible detail | source does not entail addition | remove or place in a separate note |

## Severity

- `block`: changes truth conditions, evidence ownership, stance, scope, quantity, or protected content.
- `major`: materially impairs terminology, logic, or interpretation.
- `minor`: unnatural or inefficient Vietnamese without semantic damage.

Fluency is not evidence of correctness. A smooth causal upgrade remains a blocking error.
