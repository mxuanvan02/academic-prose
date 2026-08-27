from __future__ import annotations

import json
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
            "references/composition-workflow.md",
            "references/capability-matrix.md",
            "references/argument-and-evidence.md",
            "references/genre-playbooks.md",
            "references/rhetorical-moves.md",
            "references/writing-failure-taxonomy.md",
            "references/en-vi-transfer-taxonomy.md",
            "references/domain-profiles.md",
            "references/quality-rubric.md",
            "references/pdf-translate-integration.md",
            "schemas/audit-record.schema.json",
            "schemas/glossary-entry.schema.json",
            "schemas/claim-ledger.schema.json",
            "schemas/rhetorical-brief.schema.json",
            "schemas/paragraph-plan.schema.json",
            "evals/writing-cases.jsonl",
        )
        for relative_path in required:
            with self.subTest(path=relative_path):
                self.assertTrue((ROOT / relative_path).is_file())

    def test_skill_frontmatter_is_narrow_and_vietnamese_specific(self) -> None:
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\nname: academic-vi\n"))
        frontmatter = text.split("---", 2)[1]
        self.assertIn("Vietnamese", frontmatter)
        self.assertIn("academic", frontmatter.lower())
        self.assertIn("English-to-Vietnamese", frontmatter)

    def test_rubric_declares_six_dimensions_and_blocking_failures(self) -> None:
        rubric = (ROOT / "references/quality-rubric.md").read_text(encoding="utf-8")
        for dimension in ("SEM", "TERM", "STANCE", "LOGIC", "VI", "CONS"):
            self.assertIn(f"`{dimension}`", rubric)
        for blocking_error in (
            "meaning_reversal",
            "negation_loss",
            "causal_upgrade",
            "unsupported_claim",
            "numeric_corruption",
            "citation_corruption",
        ):
            self.assertIn(blocking_error, rubric)

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

    def test_capability_matrix_covers_all_academic_vietnamese_work(self) -> None:
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
            "audit",
            "translate",
        )
        for capability in capabilities:
            with self.subTest(capability=capability):
                self.assertIn(f"`{capability}`", matrix)
        self.assertIn("composition engine", matrix.lower())
        self.assertIn("adapter", matrix.lower())

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

    def test_examples_are_synthetic_and_do_not_contain_private_markers(self) -> None:
        eval_text = (ROOT / "evals/synthetic-cases.jsonl").read_text(encoding="utf-8")
        self.assertNotIn("PRIVATE_MANUSCRIPT", eval_text)
        self.assertNotIn("CONFIDENTIAL_SOURCE", eval_text)
        for line in eval_text.splitlines():
            record = json.loads(line)
            self.assertTrue(record["synthetic"])

    def test_eval_error_labels_are_defined_by_the_skill(self) -> None:
        taxonomy = (ROOT / "references/en-vi-transfer-taxonomy.md").read_text(
            encoding="utf-8"
        )
        rubric = (ROOT / "references/quality-rubric.md").read_text(encoding="utf-8")
        definitions = taxonomy + rubric
        for line in (ROOT / "evals/synthetic-cases.jsonl").read_text(
            encoding="utf-8"
        ).splitlines():
            record = json.loads(line)
            for error_type in record["expected_errors"]:
                with self.subTest(case=record["id"], error_type=error_type):
                    self.assertIn(f"`{error_type}`", definitions)

    def test_validator_accepts_repository(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate_skill.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("academic-vi validation passed", result.stdout)
        self.assertIn("4 translation/revision evals", result.stdout)
        self.assertIn("4 writing evals", result.stdout)


if __name__ == "__main__":
    unittest.main()
