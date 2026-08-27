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


if __name__ == "__main__":
    unittest.main()
