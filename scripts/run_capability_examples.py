#!/usr/bin/env python3
"""Execute the per-capability worked examples as machine-checkable cases.

Each example in evals/capability-examples.json documents one capability from the
capability matrix. The example is not prose: it carries an input, the expected
output, and checks. Every check is also mutated so that a passing check proves
the check can fail.
"""
from __future__ import annotations

import json
from pathlib import Path

from run_usage_simulations import check, mutations


ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "evals/capability-examples.json"
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


def run() -> tuple[int, int, set[str]]:
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    failures: list[str] = []
    mutation_count = 0
    covered: set[str] = set()

    identifiers = [case["id"] for case in cases]
    if len(set(identifiers)) != len(identifiers):
        raise SystemExit("capability examples contain a duplicate id")

    for case in cases:
        capability = case.get("capability")
        if capability not in CAPABILITIES:
            raise SystemExit(f'{case["id"]}: unknown capability {capability!r}')
        if case.get("language") not in {"vi", "en"}:
            raise SystemExit(f'{case["id"]}: language must be vi or en')
        if case.get("synthetic") is not True:
            raise SystemExit(f'{case["id"]}: examples must be marked synthetic')
        for field in ("claim", "input", "output", "checks"):
            if not case.get(field):
                raise SystemExit(f'{case["id"]}: missing {field}')
        covered.add(capability)

        for index, rule in enumerate(case["checks"], 1):
            if not check(case, rule):
                failures.append(f'{case["id"]}: baseline check {index} failed')
            for mutation_index, changed in enumerate(mutations(case, rule), 1):
                mutation_count += 1
                if check(changed, rule):
                    failures.append(
                        f'{case["id"]}: mutation {index}.{mutation_index} survived'
                    )

    uncovered = CAPABILITIES - covered
    if uncovered:
        failures.append(
            "capabilities without a worked example: " + ", ".join(sorted(uncovered))
        )

    if failures:
        raise SystemExit("\n".join(failures))
    return len(cases), mutation_count, covered


if __name__ == "__main__":
    case_count, mutation_count, covered = run()
    print(
        "capability examples passed "
        f"({case_count} examples, {len(covered)} capabilities, "
        f"{mutation_count} rejected mutations)"
    )
