from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RepositoryContractTests(unittest.TestCase):
    def test_required_files_exist(self) -> None:
        required = (
            "SKILL.md",
            "README.md",
            "LICENSE",
            "agents/openai.yaml",
            "references/academic-vietnamese-standard.md",
            "references/academic-english-standard.md",
            "references/composition-workflow.md",
            "references/capability-matrix.md",
            "references/argument-and-evidence.md",
            "references/genre-playbooks.md",
            "references/deliverable-playbooks.md",
            "references/rhetorical-moves.md",
            "references/writing-failure-taxonomy.md",
            "references/cross-language-transfer-taxonomy.md",
            "references/ai-pattern-taxonomy.md",
            "references/ai-pattern-vietnamese.md",
            "references/domain-profiles.md",
            "references/quality-rubric.md",
            "references/pdf-translate-integration.md",
            "references/terminology-localization.md",
            "references/internal-register-gate.md",
            "references/self-narration-and-config-dump.md",
            "references/artifact-register-to-scientific-register.md",
            "schemas/audit-record.schema.json",
            "schemas/glossary-entry.schema.json",
            "schemas/claim-ledger.schema.json",
            "schemas/rhetorical-brief.schema.json",
            "schemas/paragraph-plan.schema.json",
            "evals/synthetic-cases.jsonl",
            "evals/writing-cases.jsonl",
            "evals/humanize-cases.jsonl",
            "evals/usage-claim-cases.json",
            "scripts/run_usage_simulations.py",
            "scripts/internal_register_scan.py",
            "scripts/test_internal_register_scan.py",
            "scripts/fixtures/internal_register_dirty.md",
            "scripts/fixtures/internal_register_dirty_en.md",
            "scripts/fixtures/internal_register_clean.md",
            "scripts/fixtures/internal_register_clean_en.md",
        )
        for relative_path in required:
            with self.subTest(path=relative_path):
                self.assertTrue((ROOT / relative_path).is_file())

    def test_skill_frontmatter_is_bilingual_academic_prose(self) -> None:
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\nname: academic-prose\n"))
        frontmatter = text.split("---", 2)[1]
        self.assertIn("Vietnamese", frontmatter)
        self.assertIn("English", frontmatter)
        self.assertIn("academic", frontmatter.lower())
        self.assertIn("humanize", frontmatter.lower())
        self.assertIn("English-to-Vietnamese", frontmatter)
        self.assertIn("Vietnamese-to-English", frontmatter)

    def test_rubric_declares_seven_dimensions_and_blocking_failures(self) -> None:
        rubric = (ROOT / "references/quality-rubric.md").read_text(encoding="utf-8")
        for dimension in ("SEM", "TERM", "STANCE", "LOGIC", "LANG", "VOICE", "CONS"):
            self.assertIn(f"`{dimension}`", rubric)
        for blocking_error in (
            "meaning_reversal",
            "negation_loss",
            "causal_upgrade",
            "unsupported_claim",
            "numeric_corruption",
            "citation_corruption",
            "scope_shift",
            "stance_upgrade",
            "range_notation_corruption",
            "required_move_deletion",
            "assistant_residue",
            "placeholder_residue",
            "internal_artifact_reference",
        ):
            self.assertIn(blocking_error, rubric)
        self.assertIn("Internal register gate", rubric)

    def test_writing_is_the_primary_workflow(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        workflow = (ROOT / "references/composition-workflow.md").read_text(
            encoding="utf-8"
        )
        for stage in (
            "Rhetorical brief",
            "Claim-evidence ledger",
            "Discourse architecture",
            "Paragraph design",
            "Draft",
            "Adversarial review",
        ):
            self.assertIn(stage, skill + workflow)
        self.assertIn("write-first", skill.lower())

    def test_capability_matrix_covers_bilingual_academic_work(self) -> None:
        matrix = (ROOT / "references/capability-matrix.md").read_text(
            encoding="utf-8"
        )
        capabilities = (
            "conceptualize",
            "outline",
            "argue",
            "synthesize",
            "draft",
            "develop",
            "compress",
            "expand",
            "paraphrase",
            "revise",
            "humanize",
            "audit",
            "translate",
        )
        for capability in capabilities:
            with self.subTest(capability=capability):
                self.assertIn(f"`{capability}`", matrix)
        self.assertIn("composition engine", matrix.lower())
        self.assertIn("adapter", matrix.lower())
        self.assertIn("Vietnamese-to-English", matrix)

    def test_routing_covers_structured_academic_deliverables(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        playbooks = (ROOT / "references/deliverable-playbooks.md").read_text(
            encoding="utf-8"
        )
        routing_contract = skill + playbooks
        for deliverable in (
            "slide",
            "bài giảng",
            "học liệu",
            "lời thuyết trình",
            "đề cương",
            "câu hỏi đánh giá",
        ):
            with self.subTest(deliverable=deliverable):
                self.assertIn(deliverable, routing_contract.lower())
        self.assertIn("tự động kích hoạt", routing_contract.lower())
        self.assertIn("mục đích học thuật", routing_contract.lower())

    def test_content_ownership_is_separate_from_layout_tools(self) -> None:
        playbooks = (ROOT / "references/deliverable-playbooks.md").read_text(
            encoding="utf-8"
        )
        normalized = " ".join(playbooks.lower().split())
        self.assertIn("academic-prose chịu trách nhiệm", normalized)
        self.assertIn("công cụ định dạng", normalized)
        self.assertIn("không làm suy giảm", normalized)

    def test_publication_prose_excludes_unnecessary_implementation_tokens(self) -> None:
        standard = (ROOT / "references/academic-english-standard.md").read_text(
            encoding="utf-8"
        )
        normalized = " ".join(standard.lower().split())
        self.assertIn("publication-facing", normalized)
        self.assertIn("schema field names", normalized)
        self.assertIn("configuration keys", normalized)
        self.assertIn("reproducibility", normalized)
        self.assertIn("technical documentation", normalized)

    def test_core_documentation_is_runtime_neutral(self) -> None:
        core_paths = (
            "README.md",
            "SKILL.md",
            "references/capability-matrix.md",
            "references/pdf-translate-integration.md",
        )
        core_text = "\n".join(
            (ROOT / path).read_text(encoding="utf-8") for path in core_paths
        )
        self.assertNotIn("$academic-prose", core_text)
        self.assertNotIn("$pdf-translate", core_text)

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        normalized = " ".join(readme.lower().split())
        self.assertIn("cú pháp gọi phụ thuộc vào môi trường", normalized)
        self.assertIn("cài đặt bằng trình quản lý skills", normalized)
        self.assertNotIn("dùng academic-prose để", normalized)

        openai_adapter = (ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
        self.assertNotIn("$academic-prose", openai_adapter)

    def test_readme_credits_external_reference_repositories(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        normalized = " ".join(readme.lower().split())
        self.assertIn("https://github.com/agentskills/agentskills", readme)
        self.assertIn("https://github.com/vercel-labs/skills", readme)
        self.assertIn("https://github.com/breslee1707/vi-translate", readme.lower())
        self.assertIn("https://github.com/blader/humanizer", readme)
        self.assertIn("chuẩn đóng gói và tích hợp", normalized)
        self.assertIn("quy trình bàn giao dịch pdf", normalized)
        self.assertIn("quy ước để môi trường tương thích khám phá", normalized)
        self.assertIn("trình quản lý skills và cú pháp cài đặt", normalized)
        self.assertIn("bảo toàn thành phần và tái dựng tài liệu", normalized)
        self.assertNotIn("không phải nguồn", normalized)
        self.assertNotIn("những việc skill không thực hiện", normalized)

    def test_writing_eval_starts_from_notes_and_evidence(self) -> None:
        records = [
            json.loads(line)
            for line in (ROOT / "evals/writing-cases.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
        ]
        self.assertGreaterEqual(len(records), 4)
        for record in records:
            with self.subTest(case=record["id"]):
                self.assertTrue(record["synthetic"])
                self.assertEqual(record["mode"], "write")
                self.assertIn("notes", record)
                self.assertIn("evidence", record)
                self.assertIn("expected_moves", record)

    def test_humanize_eval_is_bilingual_and_preserves_claims(self) -> None:
        records = [
            json.loads(line)
            for line in (ROOT / "evals/humanize-cases.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
        ]
        self.assertEqual(len(records), 15)
        self.assertEqual({record["language"] for record in records}, {"vi", "en"})
        self.assertEqual({record["mode"] for record in records}, {"humanize"})
        self.assertEqual(len({record["id"] for record in records}), len(records))
        for record in records:
            with self.subTest(case=record["id"]):
                self.assertTrue(record["synthetic"])
                self.assertTrue(record["source"])
                self.assertIn("expected_output", record)
                self.assertIn("expected_errors", record)
                self.assertIn(record["verdict"], {"apply", "guard", "redirect", "restrict", "defer"})

    def test_usage_claim_matrix_covers_every_readme_example(self) -> None:
        cases = json.loads(
            (ROOT / "evals/usage-claim-cases.json").read_text(encoding="utf-8")
        )
        self.assertEqual(len(cases), 7)
        self.assertEqual(len({case["id"] for case in cases}), 7)
        claims = {case["claim"] for case in cases}
        for expected in (
            "Viết phần Thảo luận từ bằng chứng",
            "Xây dựng lập luận và dàn ý khi đầu vào còn thiếu",
            "Dịch học thuật Anh - Việt",
            "Biên tập bản thảo tiếng Việt",
            "Soạn slide và lời thuyết trình nhất quán",
            "Soạn bài giảng và học liệu có liên kết",
            "Phối hợp bàn giao dịch PDF",
        ):
            with self.subTest(claim=expected):
                self.assertIn(expected, claims)
        for case in cases:
            with self.subTest(case=case["id"]):
                self.assertTrue(case["synthetic"])
                self.assertTrue(case["input"])
                self.assertTrue(case["output"])
                self.assertTrue(case["checks"])

    def test_usage_claim_simulator_rejects_mutations(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/run_usage_simulations.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("7 scenarios", result.stdout)
        match = re.search(r"(\d+) rejected mutations", result.stdout)
        self.assertIsNotNone(match)
        self.assertGreaterEqual(int(match.group(1)), 40)

    def test_examples_are_synthetic_and_do_not_contain_private_markers(self) -> None:
        for relative_path in (
            "evals/synthetic-cases.jsonl",
            "evals/writing-cases.jsonl",
            "evals/humanize-cases.jsonl",
        ):
            eval_text = (ROOT / relative_path).read_text(encoding="utf-8")
            self.assertNotIn("PRIVATE_MANUSCRIPT", eval_text)
            self.assertNotIn("CONFIDENTIAL_SOURCE", eval_text)
            for line in eval_text.splitlines():
                record = json.loads(line)
                self.assertTrue(record["synthetic"])

    def test_eval_error_labels_are_defined_by_the_skill(self) -> None:
        registry_paths = (
            "references/cross-language-transfer-taxonomy.md",
            "references/quality-rubric.md",
            "references/writing-failure-taxonomy.md",
            "references/ai-pattern-taxonomy.md",
            "references/ai-pattern-vietnamese.md",
        )
        definitions = "\n".join(
            (ROOT / path).read_text(encoding="utf-8") for path in registry_paths
        )
        for relative_path in (
            "evals/synthetic-cases.jsonl",
            "evals/humanize-cases.jsonl",
        ):
            for line in (ROOT / relative_path).read_text(
                encoding="utf-8"
            ).splitlines():
                record = json.loads(line)
                for error_type in record["expected_errors"]:
                    with self.subTest(case=record["id"], error_type=error_type):
                        self.assertIn(f"`{error_type}`", definitions)

    def test_every_capability_has_a_worked_example(self) -> None:
        cases = json.loads(
            (ROOT / "evals/capability-examples.json").read_text(encoding="utf-8")
        )
        capabilities = {
            "conceptualize",
            "outline",
            "argue",
            "synthesize",
            "draft",
            "develop",
            "compress",
            "expand",
            "paraphrase",
            "revise",
            "humanize",
            "audit",
            "translate",
        }
        self.assertEqual({case["capability"] for case in cases}, capabilities)
        self.assertEqual(len({case["id"] for case in cases}), len(cases))
        self.assertEqual({case["language"] for case in cases}, {"vi", "en"})
        for case in cases:
            with self.subTest(case=case["id"]):
                self.assertTrue(case["synthetic"])
                self.assertTrue(case["claim"])
                self.assertTrue(case["input"])
                self.assertTrue(case["output"])
                self.assertTrue(case["checks"])

    def test_capability_examples_reject_mutations(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/run_capability_examples.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("13 examples", result.stdout)
        self.assertIn("13 capabilities", result.stdout)
        match = re.search(r"(\d+) rejected mutations", result.stdout)
        assert match is not None, result.stdout
        self.assertGreaterEqual(int(match.group(1)), 60)

    def test_validator_accepts_repository(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate_skill.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("academic-prose validation passed", result.stdout)
        self.assertIn("4 translation/revision evals", result.stdout)
        self.assertIn("4 writing evals", result.stdout)
        self.assertIn("15 humanize evals", result.stdout)
        self.assertIn("7 usage simulations", result.stdout)
        self.assertIn("13 capability examples", result.stdout)
        self.assertIn("150 rejected mutations", result.stdout)


if __name__ == "__main__":
    unittest.main()
