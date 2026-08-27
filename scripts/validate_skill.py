#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
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
    "references/composition-workflow.md",
    "references/capability-matrix.md",
    "references/argument-and-evidence.md",
    "references/genre-playbooks.md",
    "references/deliverable-playbooks.md",
    "references/rhetorical-moves.md",
    "references/writing-failure-taxonomy.md",
    "schemas/audit-record.schema.json",
    "schemas/glossary-entry.schema.json",
    "schemas/claim-ledger.schema.json",
    "schemas/rhetorical-brief.schema.json",
    "schemas/paragraph-plan.schema.json",
    "evals/synthetic-cases.jsonl",
    "evals/writing-cases.jsonl",
    "evals/usage-claim-cases.json",
    "scripts/run_usage_simulations.py",
)


def main() -> int:
    missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
    if missing:
        raise SystemExit("missing required files: " + ", ".join(missing))

    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    if not skill.startswith("---\nname: academic-vi\n"):
        raise SystemExit("invalid SKILL.md frontmatter")

    capability_matrix = (ROOT / "references/capability-matrix.md").read_text(
        encoding="utf-8"
    )
    required_capabilities = {
        "conceptualize", "outline", "argue", "synthesize", "draft", "develop",
        "compress", "expand", "paraphrase", "revise", "audit", "translate",
    }
    defined_capabilities = set(
        re.findall(r"^\| `([a-z][a-z0-9_]+)` \|", capability_matrix, re.MULTILINE)
    )
    if defined_capabilities != required_capabilities:
        raise SystemExit("capability matrix does not define the canonical capability set")
    missing_routes = {
        capability
        for capability in required_capabilities
        if f"`{capability}`" not in skill
    }
    if missing_routes:
        raise SystemExit(
            "SKILL.md does not route capabilities: " + ", ".join(sorted(missing_routes))
        )

    for path in (
        "schemas/audit-record.schema.json",
        "schemas/glossary-entry.schema.json",
        "schemas/claim-ledger.schema.json",
        "schemas/rhetorical-brief.schema.json",
        "schemas/paragraph-plan.schema.json",
    ):
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

    writing_cases = (ROOT / "evals/writing-cases.jsonl").read_text(
        encoding="utf-8"
    ).splitlines()
    if not writing_cases:
        raise SystemExit("writing eval set is empty")
    move_registry = (ROOT / "references/rhetorical-moves.md").read_text(encoding="utf-8")
    failure_registry = (ROOT / "references/writing-failure-taxonomy.md").read_text(
        encoding="utf-8"
    )
    allowed_moves = set(re.findall(r"^\| `([a-z][a-z0-9_]+)` \|", move_registry, re.MULTILINE))
    allowed_failures = set(
        re.findall(r"^\| `([a-z][a-z0-9_]+)` \|", failure_registry, re.MULTILINE)
    )
    paragraph_schema = json.loads(
        (ROOT / "schemas/paragraph-plan.schema.json").read_text(encoding="utf-8")
    )
    schema_moves = set(paragraph_schema["properties"]["moves"]["items"]["enum"])
    if schema_moves != allowed_moves:
        raise SystemExit("paragraph-plan move enum differs from rhetorical move registry")
    for number, line in enumerate(writing_cases, 1):
        record = json.loads(line)
        if record.get("synthetic") is not True or record.get("mode") != "write":
            raise SystemExit(f"writing eval line {number} is not a synthetic write case")
        for field in ("notes", "evidence", "expected_moves", "forbidden"):
            value = record.get(field)
            if not isinstance(value, list) or not value:
                raise SystemExit(f"writing eval line {number} needs nonempty {field}")
        unknown_moves = set(record["expected_moves"]) - allowed_moves
        if unknown_moves:
            raise SystemExit(
                f"writing eval line {number} uses undocumented moves: "
                + ", ".join(sorted(unknown_moves))
            )
        unknown_failures = set(record["forbidden"]) - allowed_failures
        if unknown_failures:
            raise SystemExit(
                f"writing eval line {number} uses undocumented failures: "
                + ", ".join(sorted(unknown_failures))
            )

    usage_cases = json.loads(
        (ROOT / "evals/usage-claim-cases.json").read_text(encoding="utf-8")
    )
    expected_usage_ids = {
        "usage-discussion-from-evidence",
        "usage-argument-outline",
        "usage-en-vi-translation",
        "usage-vietnamese-revision",
        "usage-research-slides",
        "usage-university-lesson",
        "usage-pdf-handoff",
    }
    actual_usage_ids = {case.get("id") for case in usage_cases}
    if actual_usage_ids != expected_usage_ids:
        raise SystemExit("usage simulation matrix does not cover the canonical README claims")
    for number, case in enumerate(usage_cases, 1):
        if case.get("synthetic") is not True:
            raise SystemExit(f"usage case {number} is not marked synthetic")
        if not case.get("claim") or not isinstance(case.get("input"), dict):
            raise SystemExit(f"usage case {number} needs a claim and structured input")
        if not isinstance(case.get("output"), dict) or not case.get("checks"):
            raise SystemExit(f"usage case {number} needs output and checks")

    simulation = subprocess.run(
        [sys.executable, str(ROOT / "scripts/run_usage_simulations.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if simulation.returncode != 0:
        raise SystemExit(
            "usage claim simulations failed:\n"
            + simulation.stdout
            + simulation.stderr
        )
    mutation_match = re.search(
        r"(\d+) scenarios, (\d+) rejected mutations", simulation.stdout
    )
    if mutation_match is None or int(mutation_match.group(1)) != len(usage_cases):
        raise SystemExit("usage simulation summary does not match the case matrix")
    rejected_mutations = int(mutation_match.group(2))
    if rejected_mutations < 40:
        raise SystemExit("usage simulations do not exercise enough atomic mutations")

    print(
        "academic-vi validation passed "
        f"({len(cases)} translation/revision evals, {len(writing_cases)} writing evals, "
        f"{len(usage_cases)} usage simulations, {rejected_mutations} rejected mutations)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
