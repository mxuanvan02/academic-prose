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
    "references/academic-english-standard.md",
    "references/cross-language-transfer-taxonomy.md",
    "references/ai-pattern-taxonomy.md",
    "references/ai-pattern-vietnamese.md",
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
    "references/terminology-localization.md",
    "references/internal-register-gate.md",
    "references/skill-repository-maintenance.md",
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
    "evals/capability-examples.json",
    "scripts/run_usage_simulations.py",
    "scripts/run_capability_examples.py",
    "scripts/internal_register_scan.py",
    "scripts/process_logic_scan.py",
    "scripts/test_process_logic_scan.py",
    "scripts/vi_ai_pattern_scan.py",
    "scripts/test_vi_ai_pattern_scan.py",
    "references/vi-ai-pattern-gate.md",
    "scripts/fixtures/vi_ai_pattern_dirty.md",
    "scripts/fixtures/vi_ai_pattern_dirty_en.md",
    "scripts/fixtures/vi_ai_pattern_clean.md",
    "scripts/fixtures/vi_ai_pattern_licensed.md",
    "scripts/fixtures/vi_ai_pattern_acknowledgement.md",
    "references/process-logic-gate.md",
    "scripts/fixtures/process_logic_dirty.md",
    "scripts/fixtures/process_logic_dirty_en.md",
    "scripts/fixtures/process_logic_clean.md",
    "scripts/fixtures/process_logic_licensed.md",
    "scripts/test_internal_register_scan.py",
    "scripts/fixtures/internal_register_dirty.md",
    "scripts/fixtures/internal_register_dirty_en.md",
    "scripts/fixtures/internal_register_clean.md",
    "scripts/fixtures/internal_register_clean_en.md",
)

CAPABILITIES = {
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

VERDICTS = {"apply", "guard", "redirect", "restrict", "defer"}
LANGUAGES = {"vi", "en"}
DECISIONS = {"revise", "human_review"}


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def validate_humanize_cases(
    defined_errors: set[str], blocking_errors: set[str]
) -> int:
    lines = read("evals/humanize-cases.jsonl").splitlines()
    if not lines:
        raise SystemExit("humanize eval set is empty")

    ids: set[str] = set()
    for number, line in enumerate(lines, 1):
        record = json.loads(line)
        case_id = record.get("id")
        if not isinstance(case_id, str) or not case_id:
            raise SystemExit(f"humanize eval line {number} needs a nonempty id")
        if case_id in ids:
            raise SystemExit(f"humanize eval line {number} duplicates id {case_id}")
        ids.add(case_id)
        if record.get("synthetic") is not True or record.get("mode") != "humanize":
            raise SystemExit(f"humanize eval line {number} is not a synthetic humanize case")
        if record.get("language") not in LANGUAGES:
            raise SystemExit(f"humanize eval line {number} needs language vi or en")
        if not isinstance(record.get("pattern"), int) or not 1 <= record["pattern"] <= 35:
            raise SystemExit(f"humanize eval line {number} needs a pattern number from 1 to 35")
        if record.get("verdict") not in VERDICTS:
            raise SystemExit(f"humanize eval line {number} uses an unknown verdict")
        for field in ("source", "expected_output", "expected_errors", "minimum_decision"):
            if field not in record:
                raise SystemExit(f"humanize eval line {number} needs {field}")
        if not isinstance(record["expected_errors"], list) or not record["expected_errors"]:
            raise SystemExit(f"humanize eval line {number} needs nonempty expected_errors")
        unknown = set(record["expected_errors"]) - defined_errors
        if unknown:
            raise SystemExit(
                f"humanize eval line {number} uses undefined errors: "
                + ", ".join(sorted(unknown))
            )
        if blocking_errors.intersection(record["expected_errors"]):
            if record["minimum_decision"] not in DECISIONS:
                raise SystemExit(
                    f"humanize eval line {number} has a blocking error without a blocking decision"
                )
    return len(lines)


def main() -> int:
    missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
    if missing:
        raise SystemExit("missing required files: " + ", ".join(missing))

    skill = read("SKILL.md")
    if not skill.startswith("---\nname: academic-prose\n"):
        raise SystemExit("invalid SKILL.md frontmatter")

    capability_matrix = read("references/capability-matrix.md")
    defined_capabilities = set(
        re.findall(r"^\| `([a-z][a-z0-9_]+)` \|", capability_matrix, re.MULTILINE)
    )
    if defined_capabilities != CAPABILITIES:
        raise SystemExit("capability matrix does not define the canonical capability set")
    missing_routes = {
        capability for capability in CAPABILITIES if f"`{capability}`" not in skill
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
        schema = json.loads(read(path))
        if schema.get("additionalProperties") is not False:
            raise SystemExit(f"{path} must reject unknown properties")

    taxonomy = read("references/cross-language-transfer-taxonomy.md")
    rubric = read("references/quality-rubric.md")
    failure_registry = read("references/writing-failure-taxonomy.md")
    ai_taxonomy = read("references/ai-pattern-taxonomy.md")
    ai_vietnamese = read("references/ai-pattern-vietnamese.md")
    defined_errors = set(
        re.findall(
            r"`([a-z][a-z0-9_]*)`",
            "\n".join((taxonomy, rubric, failure_registry, ai_taxonomy, ai_vietnamese)),
        )
    )
    blocking_errors = set(
        re.findall(r"^- `([a-z][a-z0-9_]*)`:", rubric, flags=re.MULTILINE)
    )

    cases = read("evals/synthetic-cases.jsonl").splitlines()
    if not cases:
        raise SystemExit("eval set is empty")
    for number, line in enumerate(cases, 1):
        record = json.loads(line)
        if record.get("synthetic") is not True:
            raise SystemExit(f"eval line {number} is not marked synthetic")
        unknown = set(record.get("expected_errors", [])) - defined_errors
        if unknown:
            raise SystemExit(
                f"eval line {number} uses undefined errors: ", ", ".join(sorted(unknown))
            )
        if blocking_errors.intersection(record.get("expected_errors", [])):
            if record.get("minimum_decision") not in DECISIONS:
                raise SystemExit(
                    f"eval line {number} has a blocking error without a blocking decision"
                )

    writing_cases = read("evals/writing-cases.jsonl").splitlines()
    if not writing_cases:
        raise SystemExit("writing eval set is empty")
    move_registry = read("references/rhetorical-moves.md")
    allowed_moves = set(re.findall(r"^\| `([a-z][a-z0-9_]+)` \|", move_registry, re.MULTILINE))
    allowed_failures = set(
        re.findall(r"^\| `([a-z][a-z0-9_]+)` \|", failure_registry, re.MULTILINE)
    )
    paragraph_schema = json.loads(read("schemas/paragraph-plan.schema.json"))
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

    humanize_count = validate_humanize_cases(defined_errors, blocking_errors)

    usage_cases = json.loads(read("evals/usage-claim-cases.json"))
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
            "usage claim simulations failed:\n" + simulation.stdout + simulation.stderr
        )
    mutation_match = re.search(
        r"(\d+) scenarios, (\d+) rejected mutations", simulation.stdout
    )
    if mutation_match is None or int(mutation_match.group(1)) != len(usage_cases):
        raise SystemExit("usage simulation summary does not match the case matrix")
    rejected_mutations = int(mutation_match.group(2))
    if rejected_mutations < 40:
        raise SystemExit("usage simulations do not exercise enough atomic mutations")

    capability_examples = json.loads(read("evals/capability-examples.json"))
    documented_capabilities = {case.get("capability") for case in capability_examples}
    if documented_capabilities != CAPABILITIES:
        raise SystemExit(
            "capability examples do not cover every capability: missing "
            + ", ".join(sorted(CAPABILITIES - documented_capabilities))
        )

    examples = subprocess.run(
        [sys.executable, str(ROOT / "scripts/run_capability_examples.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if examples.returncode != 0:
        raise SystemExit(
            "capability examples failed:\n" + examples.stdout + examples.stderr
        )
    example_match = re.search(
        r"(\d+) examples, (\d+) capabilities, (\d+) rejected mutations",
        examples.stdout,
    )
    if example_match is None:
        raise SystemExit("capability example summary is unreadable")
    if int(example_match.group(1)) != len(capability_examples):
        raise SystemExit("capability example summary does not match the example set")
    if int(example_match.group(2)) != len(CAPABILITIES):
        raise SystemExit("capability example run does not cover every capability")
    example_mutations = int(example_match.group(3))
    if example_mutations < 60:
        raise SystemExit("capability examples do not exercise enough atomic mutations")

    register_scan = subprocess.run(
        [sys.executable, str(ROOT / "scripts/test_internal_register_scan.py")],
        cwd=ROOT / "scripts",
        text=True,
        capture_output=True,
        check=False,
    )
    process_logic = subprocess.run(
        [sys.executable, str(ROOT / "scripts/test_process_logic_scan.py")],
        cwd=ROOT / "scripts",
        text=True,
        capture_output=True,
        check=False,
    )
    vi_pattern = subprocess.run(
        [sys.executable, str(ROOT / "scripts/test_vi_ai_pattern_scan.py")],
        cwd=ROOT / "scripts",
        text=True,
        capture_output=True,
        check=False,
    )
    if vi_pattern.returncode != 0:
        raise SystemExit(
            "vietnamese ai-pattern gate tests failed:\n"
            + vi_pattern.stdout
            + vi_pattern.stderr
        )
    if "FAILED" in vi_pattern.stdout or "ERROR" in vi_pattern.stdout:
        raise SystemExit(
            "vietnamese ai-pattern gate tests reported failures:\n" + vi_pattern.stdout
        )
    if process_logic.returncode != 0:
        raise SystemExit(
            "process-logic gate tests failed:\n"
            + process_logic.stdout
            + process_logic.stderr
        )
    if register_scan.returncode != 0:
        raise SystemExit(
            "internal register scan tests failed:\n"
            + register_scan.stdout
            + register_scan.stderr
        )
    if "FAILED" in register_scan.stdout or "ERROR" in register_scan.stdout:
        raise SystemExit(
            "internal register scan tests reported failures:\n" + register_scan.stdout
        )

    print(
        "academic-prose validation passed "
        f"({len(cases)} translation/revision evals, {len(writing_cases)} writing evals, "
        f"{humanize_count} humanize evals, {len(usage_cases)} usage simulations, "
        f"{len(capability_examples)} capability examples, "
        f"{rejected_mutations + example_mutations} rejected mutations, "
        "internal-register + vietnamese ai-pattern bilingual scans)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
