#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "SKILL.md",
    "README.md",
    "LICENSE",
    "agents/openai.yaml",
    "references/academic-vietnamese-standard.md",
    "references/en-vi-transfer-taxonomy.md",
    "references/domain-profiles.md",
    "references/quality-rubric.md",
    "references/pdf-translate-integration.md",
    "schemas/audit-record.schema.json",
    "schemas/glossary-entry.schema.json",
    "evals/synthetic-cases.jsonl",
)


def main() -> int:
    missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
    if missing:
        raise SystemExit("missing required files: " + ", ".join(missing))

    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    if not skill.startswith("---\nname: academic-vi\n"):
        raise SystemExit("invalid SKILL.md frontmatter")

    for path in ("schemas/audit-record.schema.json", "schemas/glossary-entry.schema.json"):
        schema = json.loads((ROOT / path).read_text(encoding="utf-8"))
        if schema.get("additionalProperties") is not False:
            raise SystemExit(f"{path} must reject unknown properties")

    cases = (ROOT / "evals/synthetic-cases.jsonl").read_text(encoding="utf-8").splitlines()
    if not cases:
        raise SystemExit("eval set is empty")
    taxonomy = (ROOT / "references/en-vi-transfer-taxonomy.md").read_text(encoding="utf-8")
    rubric = (ROOT / "references/quality-rubric.md").read_text(encoding="utf-8")
    defined_errors = set(re.findall(r"`([a-z][a-z0-9_]*)`", taxonomy + rubric))
    blocking_errors = set(
        re.findall(r"^- `([a-z][a-z0-9_]*)`:", rubric, flags=re.MULTILINE)
    )

    for number, line in enumerate(cases, 1):
        record = json.loads(line)
        if record.get("synthetic") is not True:
            raise SystemExit(f"eval line {number} is not marked synthetic")
        unknown = set(record.get("expected_errors", [])) - defined_errors
        if unknown:
            raise SystemExit(
                f"eval line {number} uses undefined errors: {', '.join(sorted(unknown))}"
            )
        if blocking_errors.intersection(record.get("expected_errors", [])):
            if record.get("minimum_decision") not in {"revise", "human_review"}:
                raise SystemExit(
                    f"eval line {number} has a blocking error without a blocking decision"
                )

    print(f"academic-vi validation passed ({len(cases)} synthetic evals)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
