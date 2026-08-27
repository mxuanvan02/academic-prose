from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SchemaContractTests(unittest.TestCase):
    def test_audit_schema_requires_traceable_revision_fields(self) -> None:
        schema = json.loads(
            (ROOT / "schemas/audit-record.schema.json").read_text(encoding="utf-8")
        )
        required = set(schema["required"])
        self.assertTrue(
            {
                "segment_id",
                "source_text",
                "draft_vi",
                "revised_vi",
                "error_types",
                "severity",
                "rationale",
                "semantic_change",
                "confidence",
                "decision",
            }.issubset(required)
        )
        self.assertFalse(schema["additionalProperties"])

    def test_glossary_schema_encodes_domain_and_avoid_terms(self) -> None:
        schema = json.loads(
            (ROOT / "schemas/glossary-entry.schema.json").read_text(encoding="utf-8")
        )
        required = set(schema["required"])
        self.assertTrue({"source", "preferred", "domain", "definition", "status"}.issubset(required))
        self.assertIn("avoid", schema["properties"])
        self.assertIn("context_rules", schema["properties"])

    def test_claim_ledger_separates_claims_from_evidence(self) -> None:
        schema = json.loads(
            (ROOT / "schemas/claim-ledger.schema.json").read_text(encoding="utf-8")
        )
        required = set(schema["required"])
        self.assertTrue(
            {
                "claim_id",
                "claim_text",
                "claim_type",
                "evidence_status",
                "evidence_refs",
                "scope",
                "stance",
                "section_role",
            }.issubset(required)
        )
        self.assertIn("needs_source", schema["properties"]["evidence_status"]["enum"])
        conditions = json.dumps(schema.get("allOf", []), ensure_ascii=False)
        self.assertIn('"const": "supported"', conditions)
        self.assertIn('"minItems": 1', conditions)
        self.assertIn('"const": "needs_source"', conditions)
        self.assertIn('"maxItems": 0', conditions)
        self.assertFalse(schema["additionalProperties"])

    def test_rhetorical_brief_captures_the_writing_decision_horizon(self) -> None:
        schema = json.loads(
            (ROOT / "schemas/rhetorical-brief.schema.json").read_text(encoding="utf-8")
        )
        required = set(schema["required"])
        self.assertTrue(
            {
                "discipline",
                "genre",
                "section",
                "audience",
                "communicative_purpose",
                "central_question",
                "length_constraint",
                "unresolved_inputs",
            }.issubset(required)
        )
        self.assertFalse(schema["additionalProperties"])

    def test_paragraph_plan_requires_moves_and_claim_links(self) -> None:
        schema = json.loads(
            (ROOT / "schemas/paragraph-plan.schema.json").read_text(encoding="utf-8")
        )
        required = set(schema["required"])
        self.assertTrue(
            {
                "paragraph_id",
                "dominant_function",
                "claim_ids",
                "moves",
                "transition_basis",
            }.issubset(required)
        )
        self.assertEqual(schema["properties"]["claim_ids"]["minItems"], 1)
        self.assertFalse(schema["additionalProperties"])


if __name__ == "__main__":
    unittest.main()
