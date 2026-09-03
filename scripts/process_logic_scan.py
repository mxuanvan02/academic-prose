#!/usr/bin/env python3
"""Flag process-logic candidates in academic prose; report only, never rewrite.

A finding means a human must apply the three-proposition test from
references/process-logic-gate.md: what already existed, what happened later, and
what role the later procedure served. A lexical hit is a candidate, never a
verdict, and absence of hits is a partial verification only.

Exit: 0 no candidate, 2 candidates present, 3 input error.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# A state asserted to precede something the sentence may or may not name.
PRIOR_STATE = re.compile(
    r"(?:hình\s+thành|được\s+xây\s+dựng|xây\s+dựng|được\s+xác\s+lập|xác\s+lập"
    r"|được\s+thiết\s+lập|thiết\s+lập|đã\s+có|tồn\s+tại)\s+trước\b"
    r"|(?:assembled|formed|built|established|constructed|compiled)\s+"
    r"(?:beforehand|earlier|first|in\s+advance)\b",
    re.I,
)

# The comparison event is named, so the chronology is anchored for the reader.
ANCHOR = re.compile(
    r"trước\s+(?:khi|bước|giai\s+đoạn|vòng|lần|thời\s+điểm|truy\s+vấn|tìm\s+kiếm)"
    r"|trước\s+đó\b"
    r"|\bprior\s+to\b"
    r"|\bbefore\s+(?:running|conducting|executing|performing|the|any|these)",
    re.I,
)

# Ordering markers that introduce a later procedure. `bổ sung` alone is not an
# ordering marker: it is an adjective and fires on unrelated sentences.
SEQUENCE = re.compile(
    r"\b(?:sau\s+đó|tiếp\s+theo|kế\s+tiếp|trước\s+khi|trước\s+đó)\b"
    r"|\b(?:later|subsequently|afterwards|thereafter)\b",
    re.I,
)

# The role the later procedure serves is stated, including a negative role.
ROLE = re.compile(
    r"(?:để|nhằm)\s+\S+"
    r"|\bchỉ\s+(?:dùng|được\s+dùng|sử\s+dụng|nhằm|để|kiểm\s+tra)\b"
    r"|(?:được\s+)?đối\s+chiếu\s+với"
    r"|(?:giữ|đóng)\s+vai\s+trò"
    r"|không\s+(?:tạo|sinh|bổ\s+sung|làm\s+tăng|thay\s+thế|phát\s+sinh"
    r"|chứng\s+minh|loại\s+trừ)\b"
    r"|\bthu\s+(?:về|được)\b"
    r"|\btách\s+(?:tập\s+)?\S+\s+thành\b"
    r"|\btrước\s+khi\s+(?:quyết\s+định|gộp|kết\s+luận|áp\s+dụng)\b"
    r"|\bused\s+(?:only\s+)?to\b|\bin\s+order\s+to\b"
    r"|\bto\s+(?:check|assess|verify|identify|test|evaluate)\b"
    r"|\bdid\s+not\s+(?:add|generate|produce|introduce)\b"
    r"|\byield(?:ed|ing)?\b|\breturned\b",
    re.I,
)

# A later procedure whose role a reader may need in order to read the numbers.
LATER_PROCEDURE = re.compile(
    r"\b(?:truy\s+vấn|tìm\s+kiếm|rà\s+soát|khảo\s+sát)\b"
    r"|\b(?:search|searches|query|queries)\b",
    re.I,
)

COMBINING = re.compile(r"\b(?:kết\s+hợp|tích\s+hợp)\b|\bcombin(?:ed|ing)\b", re.I)

# Reminder framing standing in for a stated evidence boundary.
REMINDER_BOUNDARY = re.compile(
    r"(?:cần\s+(?:lưu\s+ý|nêu\s+thẳng|thận\s+trọng)|it\s+should\s+be\s+noted"
    r"|care\s+must\s+be\s+taken)"
    r"[^.]{0,240}?"
    r"(?:hạn\s+chế|giới\s+hạn|thiên\s+lệch|\bbias\b|\blimitation)",
    re.I,
)

SENTENCE = re.compile(r"(?<=[.!?;])\s+|\n{2,}")

VERDICTS = ("recast_with_named_anchor", "split_into_three_propositions", "state_role", "state_boundary")


def clean(text: str) -> str:
    """Blank out zones that are notation or configuration, not prose."""
    body = re.split(r"\\begin\{document\}", text, maxsplit=1)
    if len(body) > 1:
        text = re.split(r"\\end\{document\}", body[1], maxsplit=1)[0]
    text = re.sub(r"(?<!\\)%[^\n]*", " ", text)
    text = re.sub(r"(?s)```.*?```", " ", text)
    text = re.sub(r"(?s)\$\$.*?\$\$|(?<!\\)\$[^$\n]*\$", " ", text)
    text = re.sub(r"\\(?:cite[a-z]*|ref|eqref|label|url|href|input|include)\s*\{[^}]*\}", " ", text)
    text = re.sub(r"\\[A-Za-z@]+\*?(?:\[[^\]]*\])?", " ", text)
    return text.replace("{", " ").replace("}", " ")


def scan(text: str) -> dict:
    """Return process-logic candidates. Never edits text."""
    sentences = [" ".join(s.split()) for s in SENTENCE.split(clean(text))]
    sentences = [s for s in sentences if s]
    findings: list[dict] = []

    for idx, sentence in enumerate(sentences, start=1):
        following = sentences[idx] if idx < len(sentences) else ""
        # The role may legitimately be stated in the next sentence.
        context = f"{sentence} {following}"

        anchored = bool(ANCHOR.search(sentence))
        ordered_with_role = bool(SEQUENCE.search(sentence)) and bool(ROLE.search(sentence))

        if PRIOR_STATE.search(sentence) and not anchored and not ordered_with_role:
            findings.append(
                {
                    "sentence": idx,
                    "class": "chronology_anchor_omitted",
                    "span": sentence[:400],
                    "verdict": "recast_with_named_anchor",
                    "why": "a prior state is asserted without naming the event it precedes",
                }
            )

        if (
            COMBINING.search(sentence)
            and PRIOR_STATE.search(sentence)
            and LATER_PROCEDURE.search(sentence)
            and not anchored
        ):
            findings.append(
                {
                    "sentence": idx,
                    "class": "compressed_process_chain",
                    "span": sentence[:400],
                    "verdict": "split_into_three_propositions",
                    "why": "pre-existing corpus, later procedure, and its purpose are compressed into one chain",
                }
            )

        if (
            SEQUENCE.search(sentence)
            and LATER_PROCEDURE.search(sentence)
            and not anchored
            and not ROLE.search(context)
        ):
            findings.append(
                {
                    "sentence": idx,
                    "class": "opaque_procedure_role",
                    "span": sentence[:400],
                    "verdict": "state_role",
                    "why": "a later procedure is ordered but its role is not stated here or in the next sentence",
                }
            )

        if REMINDER_BOUNDARY.search(sentence):
            findings.append(
                {
                    "sentence": idx,
                    "class": "reminder_instead_of_boundary",
                    "span": sentence[:400],
                    "verdict": "state_boundary",
                    "why": "reminder framing stands in for a stated evidence boundary",
                }
            )

    return {
        "sentences": len(sentences),
        "findings": findings,
        "counts": {c: sum(1 for f in findings if f["class"] == c) for c in {f["class"] for f in findings}},
        "manual_pass_required": True,
        "note": (
            "Candidates require the state -> later action -> role test; no automated rewrite "
            "is licensed, and a clean scan is a partial verification only."
        ),
        "exit_code": 2 if findings else 0,
    }


def render_report(result: dict) -> str:
    lines = [
        "# Process-logic scan",
        "",
        f"- sentences: {result['sentences']}",
        f"- candidates: {len(result['findings'])}",
        "",
    ]
    if not result["findings"]:
        lines.append("No lexical candidates. The manual pass is still required.")
    for f in result["findings"]:
        lines.append(f"- `{f['class']}` s{f['sentence']} → {f['verdict']}: {f['span']}")
    lines += ["", f"> {result['note']}"]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", type=Path)
    ap.add_argument("--json", dest="json_path", type=Path, help="write the raw findings")
    ap.add_argument("--report", type=Path, help="write a Markdown report")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)
    try:
        result = scan(args.input.read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"input error: {exc}", file=sys.stderr)
        return 3
    if args.json_path:
        args.json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.report:
        args.report.write_text(render_report(result), encoding="utf-8")
    if not args.quiet:
        print(render_report(result))
    return result["exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())
