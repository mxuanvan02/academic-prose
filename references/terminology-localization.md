# Terminology Localization Policy

Whether a foreign-language term is translated, kept, or glossed. This applies to
originally-authored text as much as to translation: an author drafting in
Vietnamese leaves English terms in for the same reason a translator does — they
are the words the work was done in. A term left untranslated is therefore not a
transfer error; it is a terminology decision that was never made.

The decision is about the **referent and the reader**, never about how familiar
the word looks. Familiarity in a laboratory, a codebase, or an English-language
literature is not evidence that a word is a proper name.

## 1. Four tests, in order

Apply in sequence; the first test that returns a verdict decides.

1. **Designator test.** Does the term name a unique external object whose identity
   is carried by that string — a model, product, library, standard number, statute
   short title, dataset, gene or taxon symbol, eponym, unit, code identifier, or a
   quoted interface label? If yes: `keep_source`. Altering the string breaks
   retrieval and citation.
2. **Established-rendering test.** Does the field already own a Vietnamese
   rendering in an authoritative register (§3)? If yes: `translate`, and use that
   rendering even if colleagues speak the English form.
3. **Distinction test.** Would translating collapse two source concepts that the
   argument separates (§5)? If yes: `keep_with_gloss` or `translate_with_gloss`,
   with the two renderings kept lexically distinct.
4. **Reader test.** Would a specialist fail to index the Vietnamese form, or a
   non-specialist fail to read the English one? Use `translate_with_gloss` when the
   term is the paper's own object of study or the field's retrieval key; otherwise
   `translate`.

If no test resolves, the entry is `needs_review`: write the source term with a
descriptive gloss and flag it. Do not coin silently.

## 2. Four policies

| Policy | Form in running text | Use when |
| --- | --- | --- |
| `keep_source` | the exact source string, optionally preceded by a Vietnamese category noun (`thư viện suy luận vLLM`, `chuẩn ISO 9001`) | rigid designators |
| `translate` | one Vietnamese rendering, no parenthesis | the field owns the concept |
| `translate_with_gloss` | Vietnamese + `(source form)` at first use | established rendering, but specialists index on the source term |
| `keep_with_gloss` | source term + Vietnamese descriptive gloss at first use | no stable Vietnamese rendering exists, or translation would collapse a needed distinction |

A category noun in front of a preserved designator is the usual repair for prose
that reads as a config dump: it tells a reader outside the toolchain what kind of
object the name denotes without translating the name.

## 3. Authority order for a Vietnamese rendering

1. Legal instrument or national standard where the term is legally defined (luật,
   nghị định, TCVN).
2. Discipline textbook, council-approved specialist dictionary, or ministry
   curriculum.
3. Attested usage across Vietnamese journal articles in the same subfield.
4. An official Vietnamese version issued by an international body (WHO, ISO, UN).
5. The writer's own morphological inference.

Tier 5 alone never licenses an asserted standard term. This skill does not search
literature; when no authority is at hand, record `needs_review` and keep the source
term with a gloss. A coined rendering presented as the field's established term is
`invented_vietnamese_term`.

**Usage precedes etymology.** Where a calque is the field's settled term — `rủi ro
đạo đức` for *moral hazard*, `án lệ` for *precedent*, `học sâu` for *deep
learning* — the settled term wins over a more literal or more elegant coinage.
Terminological correctness here is a fact about the discourse community, not about
translation quality.

## 4. The same source word takes different renderings by discipline

This is why a global word list is the wrong instrument.

| Source term | Discipline | Rendering |
| --- | --- | --- |
| `baseline` | evaluation, experiment | mốc cơ sở; thiết lập cơ sở; mô hình cơ sở |
| `baseline` | econometrics, finance | kỳ gốc |
| `baseline` | clinical research | giá trị ban đầu, trước can thiệp |
| `control` | experiment | đối chứng; nhóm chứng |
| `control` | management, policy | kiểm soát |
| `control` | engineering | điều khiển |
| `treatment` | clinical research | điều trị; can thiệp |
| `treatment` | statistics | mức xử lý |
| `treatment` | materials, chemistry | xử lý mẫu |
| `trial` | clinical research | thử nghiệm |
| `trial` | law | phiên tòa |
| `case` | medicine | ca bệnh |
| `case` | law | vụ việc; án |
| `case` | research methods | trường hợp |
| `subject` | empirical research | đối tượng nghiên cứu |
| `subject` | education, curriculum | môn học |
| `subject` | grammar, logic | chủ ngữ; chủ thể |
| `culture` | microbiology | nuôi cấy |
| `culture` | humanities, social science | văn hóa |
| `stress` | mechanics | ứng suất |
| `stress` | psychology, health | căng thẳng |
| `stress` | linguistics | trọng âm |
| `charge` | physics, chemistry | điện tích |
| `charge` | law | cáo buộc |
| `charge` | economics | phí |
| `resistance` | physics | điện trở; lực cản |
| `resistance` | medicine | kháng thuốc; sức đề kháng |
| `resistance` | social science | kháng cự |
| `cell` | biology | tế bào |
| `cell` | energy | pin |
| `solution` | chemistry | dung dịch |
| `solution` | policy, engineering | giải pháp |
| `volume` | physics, chemistry | thể tích |
| `volume` | publishing | tập |
| `mass` | physics | khối lượng |
| `mass` | social science | quần chúng |
| `weight` | physics | trọng lượng |
| `weight` | statistics, psychometrics | trọng số |
| `field` | physics | trường |
| `field` | academic writing | lĩnh vực |
| `order` | mathematics | bậc |
| `order` | law, administration | lệnh; quyết định |
| `order` | biological taxonomy | bộ |
| `degree` | mathematics, thermodynamics | bậc; độ |
| `degree` | education | bằng cấp |
| `mean` | statistics | trung bình |
| `population` | statistics | tổng thể |
| `population` | demography, ecology | dân số; quần thể |
| `incidence` | epidemiology | tỷ lệ mới mắc |
| `incidence` | optics, geometry | góc tới |
| `exposure` | epidemiology, toxicology | phơi nhiễm |
| `exposure` | radiology, photography | phơi sáng |
| `exposure` | finance | mức rủi ro đang gánh |
| `survey` | social science | khảo sát |
| `survey` | geodesy, civil engineering | trắc địa |
| `instrument` | measurement | công cụ đo |
| `instrument` | law | văn bản pháp lý |
| `protocol` | computing | giao thức |
| `protocol` | laboratory, clinical | quy trình |
| `protocol` | diplomacy | nghị định thư |
| `code` | computing | mã |
| `code` | law | bộ luật |
| `act` | law | đạo luật |
| `act` | sociology, ethics | hành vi |
| `sentence` | law | bản án |
| `sentence` | linguistics | câu |
| `party` | law | bên |
| `party` | political science | đảng |
| `evidence` | science | bằng chứng |
| `evidence` | law | chứng cứ |
| `argument` | academic prose | lập luận |
| `argument` | mathematics, computing | đối số |
| `function` | mathematics | hàm |
| `function` | biology, sociology | chức năng |
| `class` | computing, statistics | lớp |
| `class` | sociology | giai cấp; tầng lớp |
| `interest` | finance | lãi suất |
| `interest` | political science, ethics | lợi ích |
| `capital` | economics | vốn |
| `capital` | geography | thủ đô |
| `demand` | economics | cầu |
| `demand` | law | yêu cầu |
| `equity` | finance | vốn chủ sở hữu |
| `equity` | ethics, education, policy | công bằng |
| `inflation` | economics | lạm phát |
| `inflation` | psychometrics | phóng đại hệ số |
| `efficient` | economics | hiệu quả phân bổ |
| `efficient` | engineering | hiệu suất |
| `consistent` | statistics, of an estimator | vững |
| `consistent` | argument | nhất quán |
| `compliance` | policy, medicine | tuân thủ |
| `compliance` | mechanics | độ biến dạng |
| `regulation` | law, policy | quy định; điều tiết |
| `regulation` | physiology | điều hòa |
| `implementation` | computing, policy | triển khai |
| `implementation` | law | thực thi |
| `review` | research writing | tổng quan |
| `review` | peer evaluation | phản biện |
| `assessment` | education | đánh giá người học |
| `evaluation` | programme, policy | đánh giá chương trình |
| `performance` | computing, engineering | hiệu năng |
| `performance` | education, sport | thành tích |
| `performance` | arts | biểu diễn |
| `agency` | social theory | năng lực hành động |
| `agency` | administration | cơ quan |
| `construct` | psychometrics, social science | cấu niệm |
| `factor` | statistics | nhân tố; hệ số |
| `factor` | ordinary analysis | yếu tố |
| `index` | statistics, economics | chỉ số |
| `index` | publishing | mục lục |
| `rate` | epidemiology, demography | tỷ lệ |
| `rate` | physics | tốc độ |
| `rate` | finance | lãi suất |
| `panel` | econometrics, survey | dữ liệu bảng |
| `panel` | governance | hội đồng |
| `wave` | survey research | đợt |
| `wave` | physics | sóng |
| `pipeline` | computing | quy trình |
| `pipeline` | petroleum, civil engineering | đường ống |
| `outcome` | clinical trial | kết cục |
| `outcome` | software, engineering | đầu ra |
| `outcome` | education, policy | kết quả đầu ra |
| `bias` | statistics | sai lệch |
| `bias` | social science, ethics | thiên lệch; định kiến |
| `power` | statistics | lực kiểm định |
| `power` | electrical engineering | công suất |
| `power` | political science | quyền lực |
| `validation` | measurement, psychometrics | thẩm định giá trị |
| `validation` | software, simulation | kiểm định tính đúng đắn |
| `context` | linguistics, NLP | ngữ cảnh |
| `context` | policy, qualitative research | bối cảnh |
| `benchmark` | evaluation | bộ dữ liệu đối sánh; bài đánh giá đối sánh |
| `benchmark` | surveying, finance | mốc chuẩn; chỉ số tham chiếu |
| `significant` | statistics | có ý nghĩa thống kê |
| `significant` | ordinary academic prose | quan trọng, never as a silent stand-in for a test |

Each glossary entry therefore carries its `domain`. One document may legitimately
use two renderings of the same source word when two disciplines are in play,
provided each rendering is locked to one concept. Copying a rendering across
disciplines is a terminology error even when the Vietnamese is idiomatic.

The table is a **polysemy diagnostic**, not a dictionary and not an allowlist. A
term absent from it still runs the four tests, and a term present in it still
takes the rendering its own discipline uses. Add a row only when a source word has
been observed to split across fields; do not grow it into a bilingual glossary of
one field.

## 5. Load-bearing distinctions

The strongest argument for keeping or glossing a source term is that the target
language tends to absorb two concepts into one word.

| Source pair | Must stay distinct | Collapse risk |
| --- | --- | --- |
| validity / reliability | giá trị (validity) / độ tin cậy (reliability) | both drift to `độ tin cậy` |
| accuracy / precision | two distinct renderings, each glossed at first use | contested in Vietnamese; do not assume one |
| efficacy / effectiveness | hiệu lực (efficacy) / hiệu quả thực hành (effectiveness) | both drift to `hiệu quả` |
| hazard / risk | nguy cơ tức thời (hazard) / nguy cơ (risk) | both drift to `nguy cơ` |
| assessment / evaluation | đánh giá người học / đánh giá chương trình | both drift to `đánh giá` |
| verification / validation | kiểm chứng / thẩm định | both drift to `kiểm định` |
| equity / equality | công bằng / bình đẳng | both drift to `công bằng` |
| statistical significance / practical importance | có ý nghĩa thống kê / quan trọng về thực hành | both drift to `đáng kể` |
| token / word | đơn vị từ (token) / từ | both drift to `từ` |

When two source terms are separated in the argument, their renderings must be
separated too, and each carries its source form at first use. Collapsing them is
`distinction_collapse_by_translation`, a blocking failure, because it changes what
the text claims rather than how it reads.

## 6. Rigid designators

Never translate: model, architecture, product, and library names; standard and
instrument numbers (`ISO 9001`, `TCVN 5687`, `IEEE 802.11`, `ICD-10`); statute
short titles and provision numbers; gene, protein, and taxon symbols and binomials
(`TP53`, `SARS-CoV-2`, `Escherichia coli`); eponyms; dataset and index proper names
(`SQuAD`, `PISA`, `TIMSS`, `VN-Index`); quoted interface labels; code identifiers;
units and symbols.

Two half-cases recur:

- **An eponym takes a Vietnamese frame around a preserved name**: `hệ số alpha của
  Cronbach`, `hiệu chỉnh Bonferroni`, `thang đo Likert`. The name survives; the
  category noun is Vietnamese.
- **A word that is both a common noun and a designator splits by referent**:
  `transformer` the electrical device is `máy biến áp`; `Transformer` the
  architecture keeps its name. Decide by what the sentence refers to, not by
  spelling.

Translating a designator is `overtranslation_of_designator`, blocking for the same
reason as a corrupted citation: the reader can no longer reach the object.

## 7. Where this policy does not reach

- verbatim quotations, reference titles, and bibliographic metadata;
- figure and table content reproduced from a source;
- code, configuration keys, schema fields, CLI flags, and file names;
- interface labels that are themselves the object of study;
- the source-language version of a bilingual document;
- a venue instruction that mandates a particular form.

Abstraction is not concealment: a methodological choice that a reader needs in
order to judge the work stays in the text, in disciplinary language. See the
publication-facing abstraction rule in
[Academic Vietnamese standard](academic-vietnamese-standard.md).

## 8. Consistency and bilingual pairing

- One rendering per concept per language version. Alternating between the source
  term and its translation is `mixed_rendering`, a `CONS` failure.
- Gloss at first use in the abstract and at first use in the body. Not in every
  section, not in table headers, not in figure captions where space is the
  constraint.
- In a bilingual document, every translated term maps to the exact source term used
  in the other version. A concept glossed in one version must be recoverable in the
  other.
- Abbreviations: expand once per language version, then use the abbreviation. Do
  not translate an abbreviation's letters (`GDP`, not a re-lettered Vietnamese
  acronym) unless the field has an established Vietnamese abbreviation.

## 9. Reverse direction: Vietnamese to English

Vietnamese institutional, legal, administrative, and academic-title terms are
system-specific and rarely have an exact foreign equivalent.

- Instruments: `Nghị định 15/2018/NĐ-CP` → *Decree 15/2018/ND-CP*; `Thông tư` →
  *Circular*; `Bộ luật` → *Code* against `Luật` → *Law*. Keep the numbering intact.
- Titles: `phó giáo sư` → *Associate Professor*, with a note that it is a
  state-conferred title rather than an appointment; `nghiên cứu sinh` →
  *doctoral candidate*, not *research student*.
- Administrative units: `xã`, `phường`, `huyện`, `thị xã` → commune, ward,
  district, town, with the Vietnamese in parentheses at first use when the argument
  depends on the administrative level.

Mapping any of these onto a near-equivalent without a gloss is
`institutional_false_friend`. Inflating a Sino-Vietnamese term into Latinate
English is `sino_vietnamese_overtranslation` in
[Cross-language transfer taxonomy](cross-language-transfer-taxonomy.md).

## 10. Genre and audience

The four tests decide *whether* a term is translated. Genre decides *how much
support the reader needs*.

| Genre | Localization stance |
| --- | --- |
| journal article for specialists | translate generic terms; keep designators; gloss once at first use |
| Vietnamese thesis or ministry report | prefer established Vietnamese; gloss designators; follow the template's own terminology where it names one |
| conference paper in computing or physics | more designators in running text are expected; still translate generic nouns |
| teaching material, slides, assessment items | Vietnamese first with the source form in parentheses, because the learner must acquire both |
| clinical guideline or public-health text | official Vietnamese of the issuing body outranks journal usage |
| legal commentary | never paraphrase an operative term; keep the statutory wording and gloss the analysis |
| grant proposal | institutional Vietnamese for agencies, programmes, and degrees; do not invent English calques of them |
| abstract | one gloss per key term, since this is usually the first occurrence; do not spend the word cap on a second gloss |
| figure and table headers | the locked short form; no new parenthesis if the body already glossed it |

A teaching text that keeps source-language generics in order to look technical
fails the reader test. A specialist article that translates a retrieval name fails
the designator test. One glossary can serve both genres with different
`gloss_at_first_use` values; it cannot serve them with different `preferred`
renderings.

## 11. Loanword, calque, and Sino-Vietnamese

Three historically distinct routes produce a Vietnamese scientific term. They are
not ranked by elegance.

1. **Settled calque or Sino-Vietnamese term.** `học sâu`, `rủi ro đạo đức`,
   `án lệ`, `hồi quy`, `phân tầng`, `nội suy`, `định lượng`. Use it. Replacing it
   with a purer native paraphrase, or reverting to the source term, are both
   errors.
2. **Settled loan.** `internet`, `vitamin`, `laser`, `virus`, `protein`, `radar`.
   Do not force these into Vietnamese morphology to appear more formal.
3. **Unsettled term.** No tier-1--4 authority exists. Use `keep_with_gloss` or
   `needs_review`; do not promote a one-off coinage.

A source-language insertion in otherwise Vietnamese prose (`các baseline`, `một
pipeline hoàn chỉnh`) is not a loan in this sense; it is an undecided generic. In
the other direction, a Sino-Vietnamese term is not ceremonial vocabulary merely
because it is formal — see the false positives in
[Vietnamese AI pattern registry](ai-pattern-vietnamese.md).

Multi-word terms are classified as a unit. `random forest` the algorithm is a
designator; `random sampling` is a generic method name and translates
(`lấy mẫu ngẫu nhiên`). Translating a named method word by word is
`overtranslation_of_designator`; retaining a generic collocation word by word is
`untranslated_generic_technicalism`.

## 12. Venue, stylesheet, and author glossary

A declared stylesheet outranks this policy's defaults for *form*, never for
identity.

- If the venue forbids source-language terms in body prose, `translate_with_gloss`
  tightens to `translate`, except for rigid designators, which still `keep_source`
  behind a category noun.
- If the venue's keyword list or indexing language is English, those strings stay
  English even when the body is Vietnamese.
- If the author supplies a glossary, it governs renderings within its scope. It
  does not license translating a designator or collapsing a load-bearing
  distinction.
- If two authorities at the same tier disagree, record both, choose one, and mark
  `needs_review` rather than oscillating silently, which is `mixed_rendering`.

Capitalization, italics, or scare quotes do not create a designator: `Baseline` as
a heading is still the generic noun. A trademark that has become a generic term in
the field follows current disciplinary usage rather than the legal status of the
mark.

## 13. Audit procedure

1. Extract every Latin-script run in body prose, excluding the protected zones in §7.
2. Classify each into `keep_source`, `translate`, `translate_with_gloss`,
   `keep_with_gloss`, or `needs_review`.
3. Check the reverse direction: every Vietnamese rendering that should have been a
   designator, and every institutional term mapped without a gloss.
4. Report counts per policy and the list of `needs_review` items. Do not narrate
   the sweep.

Codes: `untranslated_generic_technicalism`, `overtranslation_of_designator`,
`distinction_collapse_by_translation`, `invented_vietnamese_term`,
`mixed_rendering`, `institutional_false_friend`. The second and third are blocking.
See [Writing failure taxonomy](writing-failure-taxonomy.md) and the terminology
localization gate in [Quality rubric](quality-rubric.md).
