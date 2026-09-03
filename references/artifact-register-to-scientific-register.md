# From Project Artifacts to Scientific Register

Measured case: a Vietnamese dataset/benchmark paper (HOEIT-LegalQA → HUJOS-TT) drafted from a
working repository. Every number was correct and every citation resolved; the user still
rejected a whole section with: *"toàn nội dung kiểu này sao lại đưa vào em? bản thảo chủ yếu
trình bày mình đã làm gì thôi chứ? Còn hạn chế và hướng tương lai thì phải về mặt khoa học."*

The draft had inherited the register of its sources — `quality_gates.json`, an audit summary,
two empty annotator CSVs, a claim ledger. Those answer *what state is the project in*. A paper
answers *what is now known, and under what conditions*.

## The eight sites found in one sweep

Not one section. A register leak shows up wherever the draft touched an artifact:

| # | Section | Artifact-register text | Scientific-register replacement |
| --- | --- | --- | --- |
| 1 | Limitations | "Hai tệp annotator có 240 dòng nhưng các cột đánh giá đều trống" | labels have no human reference annotation, so reliability is unquantified and generator error cannot be separated from source-context error |
| 2 | Limitations | "nhãn lĩnh vực hiện là giá trị placeholder giống nhau cho toàn bộ 14.210 bản ghi" | the dataset is not stratified by domain, so per-domain performance cannot be analysed — a material gap in a domain where difficulty varies sharply |
| 3 | Limitations | "các điểm tự động đạt mức tối đa trong một số báo cáo" | the automatic scorer saturates near the ceiling and loses discriminative power, so it functions as a coarse error filter only |
| 4 | Limitations | "Audit trước đó cho thấy 84 ảnh và 78 ứng viên bảng chỉ là kho ứng viên, chưa có tài sản nào được người xác nhận" | the multimodal subset holds 29 items after adjudication, too few for a statistically meaningful visual evaluation; the paper therefore makes no multimodal-benchmark claim |
| 5 | Methods (context stage) | four per-bucket candidate tallies (1.528 / 469 / 891 / 263) plus "75 chuyển duyệt thủ công và 165 bị loại trong báo cáo đủ điều kiện" | the OCR-noise rate (31,15%) and the three anchor-precision levels of the recovery mechanism, plus the constraint that recovered context is content-equivalent, not verbatim |
| 6 | Methods (release stage) | "Mẫu số này thuộc tệp dữ liệu xử lý 16.158 bản ghi, không phải toàn bộ 14.210" and a 155/154-record reconciliation note | one sentence on the mechanism: both branches derive from the same filtered pool but place the language filter at different points, so the evaluation set is not a subset of the release and the two totals share no denominator |
| 7 | Results ("Kiểm tra tính toàn vẹn") | a QA checklist — 48 Markdown files match 48 PDFs, zero `qa_id` collisions | opens by stating *why* traceability and non-duplication are preconditions for measuring model performance, reports the checks as premises, then states explicitly what they do **not** establish (legal correctness) |
| 8 | Conclusion | "Các bước tiếp theo cần ưu tiên là …" (a task list) | a `Hướng nghiên cứu` section: four open problems, each with the question, why current evidence cannot settle it, and a feasible design |

## The test that catches all eight

> If the team did more work next week and this sentence changed, but the scientific finding did
> not, the sentence is bookkeeping.

Rows 1–4 all fail it: fill the columns, add the tags, calibrate the scorer, qualify the assets
— every sentence evaporates while the paper's contribution is untouched. Rows 5–7 fail a
variant: the numbers are stable but their *unit of analysis* is the team's spreadsheet
(candidates, files, rows) rather than the phenomenon.

## What NOT to do with the leak

**Do not delete the numbers.** The target is a change of register, not a loss of
verifiability. Rows 5 and 6 keep their load-bearing quantities (31,15% noise rate; the fact
that two totals have different denominators) and drop only the reconstruction of the audit
trail. A reviewer must still be able to audit the work.

**Do not let a limitation stand without its consequence.** Each rewritten limitation names the
inference it weakens: which claim is unavailable, over what scope. A limitation with no
consequence is `ceremonial_limitation`, a different failure with the same smell.

**Separate ethics from limitations.** The original section was titled `Hạn chế và vấn đề đạo
đức` and mixed distribution rights into a list of measurement limits. Rights and intended-use
scope are a normative statement, not a validity bound; they earned their own section.

**Reorder the tail.** Correct order after the sweep: Hạn chế → Đạo đức và phạm vi sử dụng →
Hướng nghiên cứu → Kết luận. The conclusion closes the paper; it cannot sit before the open
problems it does not resolve.

## A side effect worth expecting

Rewriting the Methods paragraph (row 5) forced a read of the actual pipeline code, which
revealed that a VLM stage present in the implementation and in Figure 1 was **missing from the
prose entirely** — the earlier draft had "resolved" the figure/text mismatch by planning to
edit the figure. Register cleanup and evidence verification are the same pass: an artifact-
register sentence is usually a sentence nobody traced back to the system.

## Future-work rewrite pattern

Each item needs three parts, in this order:

1. the open question, phrased as a question about the world rather than about the project;
2. why the present evidence cannot settle it;
3. a design that could, concrete enough to argue with.

Worked example from the same paper: *"Obtain expert review"* (task) →
*"Establish a human reference set annotated by legal and educational-measurement experts,
measure inter-rater reliability, and estimate convergence between automatic and expert
cognitive labels; this is a precondition before any claim about the dataset's cognitive
stratification counts as verified."*
