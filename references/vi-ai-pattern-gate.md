# Vietnamese AI-pattern gate

Operational gate for [Vietnamese AI pattern registry](ai-pattern-vietnamese.md).
The registry says *what* marks machine-generated Vietnamese academic prose; this
file says *how* the check runs, what it cannot see, and how a finding is closed.

Run it on every Vietnamese delivery, and on English text that a Vietnamese
author drafted or that was translated from Vietnamese. Pair it with
[Internal register gate](internal-register-gate.md): that gate removes the
drafting conversation, this one removes ceremonial padding and evaluation
without measurement.

## Core rule

**A lexical hit is a candidate, never a verdict.** One ceremonial word proves
nothing — careful human Vietnamese academic prose contains `quan trọng`,
`có thể`, and balanced pairs. Registry §8 requires several independent signals to
co-occur before a passage is called machine-marked, and the scanner implements
that as a separate `machine_marked_passage` class over a three-sentence window.

**Absence of hits is a partial verification only.** Two failure modes have no
lexical signature and are invisible here:

- `terminology_drift` — an ornamental synonym replacing a locked term reads
  perfectly well.
- hedge *deletion* — removing `trong phạm vi dữ liệu hiện có` is a blocking
  stance upgrade and leaves no trace the scanner can match.

Both need the manual pass over Methods, Results, Limitations, and any sentence
carrying a number.

## Classes

| class | catches | verdict |
| --- | --- | --- |
| `ceremonial_padding` | registry §1 watched vocabulary (`đóng vai trò then chốt`, `mang tính đột phá`, `vượt trội`, `toàn diện`, `uy tín`, `chuyên sâu`, English `plays an important role`, `groundbreaking`) | `replace_with_measurement` |
| `unquantified_intensifier` | `đáng kể` / `significantly` with no number, no citation, no statistical test in the sentence | `replace_with_measurement` |
| `empty_framing` | registry §2 frames that occupy a clause and assert nothing (`có thể thấy rằng`, `đóng vai trò là`, `it can be seen that`) | `delete` |
| `symmetric_padding` | registry §3 decorative four-syllable balanced compounds (`phong phú đa dạng`, `nhanh chóng hiệu quả`) | `replace_with_measurement` |
| `ornamental_triad` | three or more distinct ornamental adjectives in one sentence with no quantity anywhere in it | `replace_with_measurement` |
| `translation_calque` | registry §4 calques (`mở đường cho`, `nó được phát hiện ra rằng`, `trong điều khoản của`) | `recast` |
| `hedge_stack` | three or more distinct hedge markers in one sentence (registry §6 stack collapse) | `recast` |
| `machine_marked_passage` | three or more *distinct* classes inside a three-sentence window (registry §8) | `recast` |

Permitted verdicts: `replace_with_measurement`, `delete`, `recast`, `license`.
**`soften` is not a verdict** — hedging a ceremonial sentence leaves it
ceremonial and now also vague.

Collapsing a hedge stack must leave **one** calibrated marker. Zero markers is
`stance_upgrade`, a blocking failure in
[Quality rubric](quality-rubric.md).

## Licensed constructions (registry §7)

The scanner suppresses these itself; do not re-flag them by hand.

- **Negated ceremonial word.** `không tồn tại ngưỡng mà tại đó ET vượt trội
  tuyệt đối` *states* the finding. Deleting `vượt trội` deletes the claim.
- **Attributed magnitude.** `giảm truyền tin đáng kể~\cite{...}` — the source
  carries the number, not this sentence.
- **Statistical significance.** `khác biệt có ý nghĩa thống kê (p < 0,05)` is
  terminology, not padding.
- **Method-step names.** `đọc chuyên sâu` is the name of a PRISMA screening
  step, not a compliment.
- **Genre-mandated Vietnamese sections.** `Tính cấp thiết của đề tài`,
  `Ý nghĩa khoa học và thực tiễn`, `Kết luận và kiến nghị` are required by the
  Vietnamese thesis template. Repair weak content; never delete the section.
- **Acknowledgements.** `lòng biết ơn sâu sắc` predates any model. The whole
  `Lời cảm ơn` section is licensed.
- **Sino-Vietnamese terminology.** `khả thi`, `tối ưu hóa`, `định lượng`,
  `hồi quy`, `phân tầng` are formal register, not ceremony.
- **Topic-comment openings.** `Về phương pháp, nghiên cứu sử dụng …` is native
  Vietnamese information structure, not a dummy subject.
- **Decimal comma and en-dash ranges.** `0,847`, `2015–2025`, `tr. 145–162` are
  correct Vietnamese convention and must survive byte-identical.
- **Protected tokens.** `\cite{...}`, `\ref{...}`, `\label{...}`, math,
  `verbatim`/`lstlisting`, URLs, and DOIs are stripped before scanning.

## Usage

```bash
python3 scripts/vi_ai_pattern_scan.py manuscript.tex --report report.md
python3 scripts/vi_ai_pattern_scan.py notes.md --genre acknowledgement
python3 scripts/vi_ai_pattern_scan.py thesis.docx --json findings.json --quiet
```

Exit codes: `0` scan clean, `2` revision-level findings, `3` input error. There
is no exit `1` — this gate has no blocking class of its own; a blocking failure
is decided by the rubric after the manual pass.

Genres: `manuscript` (default), `thesis`, `acknowledgement`, `response_letter`,
`grant`. A genre only *licenses* classes; it never adds one.

## Calibration history

Do not tighten a pattern without measuring the false-positive rate on real
prose. First run on one Vietnamese thesis produced **24 candidates**, of which 9
were licensed constructions from §7. Each became a regression test:

| licensed construction | test |
| --- | --- |
| `vượt trội` inside a negation | `test_ceremonial_word_inside_a_negation_is_licensed` |
| `đọc chuyên sâu` as a method step | `test_method_step_name_is_licensed` |
| `đáng kể~\cite{...}` | `test_intensifier_with_a_citation_is_licensed` |
| `lòng biết ơn sâu sắc` | `test_acknowledgement_convention_is_licensed` |
| `Tính cấp thiết của đề tài` | `test_genre_mandated_vietnamese_section_is_licensed` |
| `0,847` / `2015–2025` | `test_decimal_comma_and_en_dash_survive` |
| `khả thi`, `hồi quy` | `test_sino_vietnamese_terminology_is_not_ceremonial` |
| `Về phương pháp, …` | `test_topic_comment_structure_is_not_a_dummy_subject` |
| `p < 0,05` | `test_statistical_significance_is_not_padding` |

After calibration the same thesis reported **15 real candidates**, all repaired
by replacing the evaluation with the measurement or deleting the frame.

## Maintenance

The pattern lists live in `scripts/vi_ai_pattern_scan.py` and mirror
[Vietnamese AI pattern registry](ai-pattern-vietnamese.md). When the registry
gains a watched word, add it to the scanner **and** add a fixture line, or the
registry and the gate drift apart.

`scripts/validate_skill.py` runs `scripts/test_vi_ai_pattern_scan.py` and
requires every fixture to exist, so deleting a fixture or dropping the English
branch of a pattern turns the validator red. That is the intended behaviour:
see [Skill repository maintenance](skill-repository-maintenance.md) for how to
prove a gate still has stopping power before shipping it.
