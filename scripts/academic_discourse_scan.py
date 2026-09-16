#!/usr/bin/env python3
"""Report paragraph-level academic-discourse candidates in text, Markdown, or DOCX.

This scanner catches defects that sentence-level watched-word lists miss: a
paragraph organised around missing work, a stack of defensive boundaries, a
research agenda written as a task list, and a sentence whose clause structure
hides claim boundaries. Findings are candidates for manual adjudication, never
automatic proof that prose is defective and never instructions to delete a
scientific limitation.

Exit: 0 no candidates, 2 revision candidates, 3 input error.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

# DOCX is untrusted input. defusedxml rejects entity expansion and external
# entities before the OOXML tree is traversed.
from defusedxml import ElementTree as ET

from ooxml_text import docx_paragraphs

HEADING_TEXT = re.compile(r"^\s*#{1,6}\s+[^\n]{1,100}$")
BIB_ENTRY = re.compile(r"^\s*\[\d+\]\s+")
SENTENCE = re.compile(r"(?<=[.!?])\s+|(?<=;)\s+(?=[A-ZÀ-Ỹ])")

MISSING_WORK = re.compile(
    r"(?:"
    r"\bchưa\s+(?:được\s+)?(?:báo\s+cáo|xác\s+định|định\s+lượng|thực\s+hiện|thẩm\s+định|"
    r"kiểm\s+chứng|đánh\s+giá|cung\s+cấp|kèm|lưu|phân\s+rã|ghi\s+lại|xác\s+lập|loại\s+trừ)"
    r"|\bthiếu\s+(?:đối\s+chiếu|bằng\s+chứng|thẩm\s+định|dữ\s+liệu|kiểm\s+tra|ước\s+lượng)"
    r"|\bkhông\s+(?:có|qua)\s+(?:nhãn\s+tham\s+chiếu|thẩm\s+định|đối\s+chiếu|kiểm\s+tra)"
    r"|\b(?:has|have)\s+not\s+(?:yet\s+)?been\s+(?:reported|established|quantified|performed|"
    r"validated|evaluated|assessed|checked|quantified|reported|recorded|provided)"
    r"|\b(?:is|are)\s+not\s+(?:yet\s+)?(?:available|reported|established|quantified|validated)"
    r"|\black(?:s|ing)?\s+(?:independent\s+)?(?:validation|evaluation|evidence|annotation|estimates?)"
    r")",
    re.I,
)

BOUNDARY = re.compile(
    r"(?:"
    r"\bkhông\s+(?:chứng\s+minh|đồng\s+nghĩa|hàm\s+ý|xác\s+lập|bảo\s+đảm|thay\s+thế|"
    r"cho\s+phép\s+(?:kết\s+luận|suy\s+rộng)|phải\s+là)"
    r"|\bchỉ\s+(?:mang|có|phản\s+ánh|mô\s+tả|áp\s+dụng|giới\s+hạn)"
    r"|\btrong\s+phạm\s+vi\b|\bgiới\s+hạn\s+trong\b"
    r"|\bdo(?:es)?\s+not\s+(?:prove|imply|establish|guarantee|validate|support)"
    r"|\bcannot\s+(?:prove|imply|establish|guarantee|validate|support|be\s+generalized)"
    r"|\bonly\s+(?:describes?|reflects?|establishes?|applies?\s+to)"
    r"|\bwithin\s+(?:the\s+)?(?:scope|sample|conditions)\b"
    r")",
    re.I,
)

TASK = re.compile(
    r"(?:"
    r"\b(?:cần|phải)\s+(?:được\s+)?(?:công\s+bố|định\s+danh|phân\s+rã|kiểm\s+tra|thẩm\s+định|"
    r"báo\s+cáo|dùng|loại\s+trừ|xem\s+xét|khai\s+báo)"
    r"|\bmột\s+[^.]{0,50}\s+đầy\s+đủ\s+cần\b"
    r"|\b(?:future|subsequent)\s+(?:work|research|analysis)\s+(?:should|must|needs?\s+to)"
    r"|\b(?:should|must|needs?\s+to)\s+(?:validate|assess|check|report|quantify|examine|release|identify)"
    r"|\b(?:should|must|needs?\s+to)\s+be\s+(?:reported|validated|examined|released|identified)"
    r")",
    re.I,
)

PIVOT = re.compile(
    r"\b(?:nhưng|tuy\s+nhiên|do\s+đó|vì\s+vậy|trong\s+khi|mặc\s+dù|đồng\s+thời|"
    r"whereas|although|however|therefore|while|because|but)\b|[,;:]",
    re.I,
)

THRESHOLDS = {
    "deficit_centered_paragraph": 0,
    "caveat_saturation": 0,
    "research_agenda_as_task_list": 0,
    "clause_overload": 0,
}


def _docx_paragraphs(path: Path) -> list[str]:
    return docx_paragraphs(path)


def read_paragraphs(path: Path) -> list[str]:
    if path.suffix.lower() == ".docx":
        return _docx_paragraphs(path)
    text = path.read_text(encoding="utf-8")
    return [" ".join(block.split()) for block in re.split(r"\n\s*\n", text) if block.strip()]


def _sentences(paragraph: str) -> list[str]:
    return [s.strip() for s in SENTENCE.split(paragraph) if s.strip()]


def _word_count(text: str) -> int:
    return len(re.findall(r"\b[\wÀ-ỹ]+\b", text, re.UNICODE))


def _counts(pattern: re.Pattern[str], text: str) -> int:
    return len(list(pattern.finditer(text)))


def scan_paragraphs(paragraphs: list[str], genre: str = "manuscript") -> dict:
    findings: list[dict] = []
    current_heading = ""
    scanned = 0

    for index, paragraph in enumerate(paragraphs, 1):
        if HEADING_TEXT.match(paragraph) and _word_count(paragraph) <= 14:
            current_heading = re.sub(r"^#{1,6}\s+", "", paragraph).strip()
            continue
        if BIB_ENTRY.match(paragraph) or _word_count(paragraph) < 8:
            continue
        scanned += 1
        sentences = _sentences(paragraph)
        missing = _counts(MISSING_WORK, paragraph)
        boundaries = _counts(BOUNDARY, paragraph)
        tasks = _counts(TASK, paragraph)

        # Two independent missing-work statements plus another defensive/task
        # move indicate that the paragraph is organised by the revision backlog,
        # not merely that it states one legitimate limitation.
        if missing >= 2 and missing + boundaries + tasks >= 3:
            findings.append({
                "paragraph": index,
                "heading": current_heading,
                "class": "deficit_centered_paragraph",
                "span": paragraph[:600],
                "matched": {"missing_work": missing, "boundaries": boundaries, "tasks": tasks},
                "verdict": "recast_from_inference",
                "licensable": False,
            })

        if boundaries >= 3 and len(sentences) >= 2:
            findings.append({
                "paragraph": index,
                "heading": current_heading,
                "class": "caveat_saturation",
                "span": paragraph[:600],
                "matched": {"boundaries": boundaries, "sentences": len(sentences)},
                "verdict": "retain_one_bounded_claim",
                "licensable": False,
            })

        # Future-work prose may name a design, but three obligations in one
        # paragraph read as an author task tracker. One or two remain licensed.
        if tasks >= 3:
            findings.append({
                "paragraph": index,
                "heading": current_heading,
                "class": "research_agenda_as_task_list",
                "span": paragraph[:600],
                "matched": {"tasks": tasks},
                "verdict": "recast_as_question_design_payoff",
                "licensable": False,
            })

        for sentence_index, sentence in enumerate(sentences, 1):
            words = _word_count(sentence)
            pivots = _counts(PIVOT, sentence)
            # High threshold by design: length alone is not a defect. The rule
            # requires enough structural pivots to obscure independent claims.
            if words >= 65 and pivots >= 7:
                findings.append({
                    "paragraph": index,
                    "sentence": sentence_index,
                    "heading": current_heading,
                    "class": "clause_overload",
                    "span": sentence[:600],
                    "matched": {"words": words, "pivots": pivots},
                    "verdict": "split_preserving_relations",
                    "licensable": False,
                })

    counts = {code: 0 for code in THRESHOLDS}
    for finding in findings:
        counts[finding["class"]] += 1
    return {
        "genre": genre,
        "paragraphs": scanned,
        "counts": counts,
        "findings": findings,
        "thresholds": [
            {"check": code, "observed": counts[code], "threshold": limit,
             "pass": counts[code] <= limit}
            for code, limit in THRESHOLDS.items()
        ],
        "gate": "revise" if findings else "scan_clean",
        "blocking": [],
        "manual_pass_required": True,
        "note": (
            "Paragraph-level heuristics report candidates only. A clean scan is partial "
            "verification; adjudicate paragraph function, evidence status, and section role manually."
        ),
        "exit_code": 2 if findings else 0,
    }


def scan(text: str, genre: str = "manuscript") -> dict:
    paragraphs = [" ".join(block.split()) for block in re.split(r"\n\s*\n", text) if block.strip()]
    return scan_paragraphs(paragraphs, genre)


def render_report(result: dict) -> str:
    lines = [
        "# Academic discourse scan", "",
        f"- genre: `{result['genre']}`",
        f"- paragraphs scanned: {result['paragraphs']}",
        f"- candidates: {len(result['findings'])}",
        f"- gate: **{result['gate']}**", "",
        "## Thresholds", "",
        "| check | observed | limit | pass |",
        "| --- | --- | --- | --- |",
    ]
    for check in result["thresholds"]:
        lines.append(
            f"| `{check['check']}` | {check['observed']} | {check['threshold']} | "
            f"{'yes' if check['pass'] else 'NO'} |"
        )
    lines += ["", "## Findings", ""]
    if not result["findings"]:
        lines.append("No heuristic candidates. The manual paragraph-function pass is still required.")
    for finding in result["findings"]:
        location = f"p{finding['paragraph']}"
        if finding.get("sentence"):
            location += f" s{finding['sentence']}"
        lines.append(
            f"- `{finding['class']}` — {location} → {finding['verdict']}: {finding['span']}"
        )
    lines += ["", f"> {result['note']}"]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--genre", default="manuscript")
    parser.add_argument("--json", dest="json_path", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = scan_paragraphs(read_paragraphs(args.input), args.genre)
    except (OSError, UnicodeError, KeyError, zipfile.BadZipFile, ET.ParseError) as exc:
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
