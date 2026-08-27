#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "evals/usage-claim-cases.json"


def resolve(data: Any, path: str) -> Any:
    value = data
    for part in path.split("."):
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def flattened(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def check(case: dict[str, Any], rule: dict[str, Any]) -> bool:
    kind = rule["type"]
    if kind == "contains":
        text = flattened(resolve(case, rule["path"]))
        return all(item in text for item in rule["values"])
    if kind == "excludes":
        text = flattened(resolve(case, rule["path"]))
        return all(item not in text for item in rule["values"])
    if kind == "equals":
        return resolve(case, rule["path"]) == resolve(case, rule["source_path"])
    if kind == "claim_status":
        claims = resolve(case, rule["path"])
        allowed = {"supported", "author_input", "inference", "needs_source", "contested"}
        return bool(claims) and all(
            claim.get("status") in allowed
            and ((claim["status"] != "supported") or bool(claim.get("evidence_refs")))
            and ((claim["status"] != "needs_source") or not claim.get("evidence_refs"))
            for claim in claims
        )
    if kind == "paired_fields":
        left_items = resolve(case, rule["left_path"])
        right_items = resolve(case, rule["right_path"])
        left = {item[rule["key"]]: item for item in left_items}
        right = {item[rule["key"]]: item for item in right_items}
        return (
            bool(left_items)
            and len(left) == len(left_items)
            and len(right) == len(right_items)
            and left.keys() == right.keys()
            and all(
                left[key].get(field) == right[key].get(field)
                for key in left
                for field in rule["fields"]
            )
        )
    if kind == "alignment":
        outcomes = {item["id"] for item in resolve(case, rule["outcomes_path"])}
        linked_groups = [resolve(case, path) for path in rule["linked_paths"]]
        return bool(outcomes) and all(
            bool(group)
            and all(item.get("outcome_refs") for item in group)
            and {ref for item in group for ref in item["outcome_refs"]} == outcomes
            for group in linked_groups
        )
    if kind == "protected_tokens":
        source = resolve(case, rule["source_path"])
        target = resolve(case, rule["target_path"])
        counts_match = all(
            source.count(token) == target.count(token) > 0
            for token in rule["patterns"]
        )
        if not counts_match:
            return False
        source_order = [source.index(token) for token in rule["patterns"]]
        target_order = [target.index(token) for token in rule["patterns"]]
        return _relative_order(source_order) == _relative_order(target_order)
    raise ValueError(f"unknown check type: {kind}")


def mutations(case: dict[str, Any], rule: dict[str, Any]) -> list[dict[str, Any]]:
    kind = rule["type"]
    if kind == "contains":
        changed_cases = []
        for value in rule["values"]:
            changed = copy.deepcopy(case)
            parent, key = _parent(changed, rule["path"])
            if isinstance(parent[key], str):
                parent[key] = parent[key].replace(value, "")
            else:
                parent[key] = []
            changed_cases.append(changed)
        return changed_cases
    if kind == "excludes":
        changed_cases = []
        for value in rule["values"]:
            changed = copy.deepcopy(case)
            parent, key = _parent(changed, rule["path"])
            parent[key] = flattened(parent[key]) + " " + value
            changed_cases.append(changed)
        return changed_cases
    changed = copy.deepcopy(case)
    if kind == "equals":
        parent, key = _parent(changed, rule["path"])
        parent[key] = []
        return [changed]
    if kind == "claim_status":
        claims = resolve(changed, rule["path"])
        claims[0]["status"] = "unknown"
        missing_ref = copy.deepcopy(case)
        resolve(missing_ref, rule["path"])[0]["evidence_refs"] = []
        false_ref = copy.deepcopy(case)
        resolve(false_ref, rule["path"])[1]["evidence_refs"] = ["E-X"]
        return [changed, missing_ref, false_ref]
    if kind == "paired_fields":
        resolve(changed, rule["right_path"])[0][rule["fields"][0]] = "certain"
        missing_pair = copy.deepcopy(case)
        resolve(missing_pair, rule["right_path"]).clear()
        return [changed, missing_pair]
    if kind == "alignment":
        changed_cases = []
        for path in rule["linked_paths"]:
            invalid = copy.deepcopy(case)
            resolve(invalid, path)[0]["outcome_refs"] = ["LO-X"]
            changed_cases.append(invalid)
            empty = copy.deepcopy(case)
            resolve(empty, path).clear()
            changed_cases.append(empty)
        return changed_cases
    if kind == "protected_tokens":
        changed_cases = []
        for token in rule["patterns"]:
            missing = copy.deepcopy(case)
            parent, key = _parent(missing, rule["target_path"])
            parent[key] = parent[key].replace(token, "", 1)
            changed_cases.append(missing)
        reordered = copy.deepcopy(case)
        parent, key = _parent(reordered, rule["target_path"])
        first, second = rule["patterns"][:2]
        parent[key] = parent[key].replace(first, "__FIRST__", 1).replace(
            second, first, 1
        ).replace("__FIRST__", second, 1)
        changed_cases.append(reordered)
        return changed_cases
    raise ValueError(f"unknown mutation type: {kind}")


def _relative_order(positions: list[int]) -> list[int]:
    return sorted(range(len(positions)), key=positions.__getitem__)


def _parent(data: dict[str, Any], path: str) -> tuple[Any, Any]:
    parts = path.split(".")
    parent = data
    for part in parts[:-1]:
        parent = parent[int(part)] if isinstance(parent, list) else parent[part]
    key: Any = int(parts[-1]) if isinstance(parent, list) else parts[-1]
    return parent, key


def run() -> tuple[int, int]:
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    failures: list[str] = []
    mutation_count = 0
    for case in cases:
        for index, rule in enumerate(case["checks"], 1):
            if not check(case, rule):
                failures.append(f'{case["id"]}: baseline check {index} failed')
            for mutation_index, changed in enumerate(mutations(case, rule), 1):
                mutation_count += 1
                if check(changed, rule):
                    failures.append(
                        f'{case["id"]}: mutation {index}.{mutation_index} survived'
                    )
    if failures:
        raise SystemExit("\n".join(failures))
    return len(cases), mutation_count


if __name__ == "__main__":
    case_count, mutation_count = run()
    print(
        "usage claim simulations passed "
        f"({case_count} scenarios, {mutation_count} rejected mutations)"
    )
