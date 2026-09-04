#!/usr/bin/env python3
"""Flag Vietnamese AI-pattern candidates in academic prose; report only, never rewrite.

The registry behind this gate is `references/ai-pattern-vietnamese.md`. A lexical
hit is a candidate, never a verdict: §8 of that registry requires several
independent signals to co-occur before a passage may be called machine-marked,
and §7 lists correct Vietnamese constructions that an English-trained rule
misreads. Absence of hits is a partial verification only -- paraphrased padding
has no lexical signature.

This gate is revision-level: it never returns a blocking class. Two failures the
registry treats as blocking cannot be detected lexically and stay with the human
reviewer: reducing hedges to zero (`stance_upgrade`) and introducing an
ornamental synonym for a locked term (`terminology_drift`).

Design notes that matter for correctness:

* Math and citation groups are replaced by the placeholders `<NUM>` / `<CITE>`
  rather than deleted, because "does this sentence carry a quantity or a source"
  is exactly what licenses an intensifier such as `đáng kể`.
* Reminder framing (`cần lưu ý rằng`, `đáng chú ý là`) is owned by
  `internal_register_scan.py`; it is deliberately absent here so one sentence is
  not reported twice by two gates.
* `tối ưu`, `ngày càng` and `đa dạng` are excluded as standalone ceremonial words:
  in control engineering `điều khiển tối ưu` / `tối ưu hóa` are terminology
  (registry §7), so a standalone rule produces more noise than signal. They are
  still counted for the ornamental-triad rule.

Exit: 0 no candidate, 2 candidates present, 3 input error.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

NUM = "<NUM>"
CITE = "<CITE>"

# --- markup handling ---------------------------------------------------------

COMMENT = re.compile(r"(?<!\\)%[^\n]*")
CITE_GROUP = re.compile(r"\\(?:cite[a-z]*|footcite|textcite)\s*(?:\[[^\]]*\])?\{[^}]*\}", re.I)
REF_GROUP = re.compile(r"\\(?:ref|eqref|autoref|pageref|label|url|href|doi)\s*\{[^}]*\}", re.I)
MATH = re.compile(r"(?s)\$\$.*?\$\$|(?<!\\)\$[^$\n]*\$")
FENCE = re.compile(r"(?s)```.*?```")
MACRO = re.compile(r"\\[A-Za-z@]+\*?(?:\[[^\]]*\])?")
HEADING = re.compile(
    r"\\(?:part|chapter|section|subsection|subsubsection|frontmatterheading)\*?\{([^}]*)\}"
    r"|^\s{0,3}#{1,6}\s+(.+)$",
    re.M,
)
SENTENCE = re.compile(r"(?<=[.!?;])\s+|\n{2,}")

ACK_SECTION = re.compile(r"lời\s+cảm\s+ơn|acknowledg", re.I)

# --- pattern classes ---------------------------------------------------------

CEREMONIAL = [
    r"đóng\s+vai\s+trò\s+then\s+chốt",
    r"giữ\s+vai\s+trò\s+(?:quan\s+trọng|đặc\s+biệt\s+quan\s+trọng)",
    r"có\s+ý\s+nghĩa\s+(?:vô\s+cùng\s+|hết\s+sức\s+)?quan\s+trọng",
    r"mang\s+tính\s+đột\s+phá",
    r"\bvượt\s+trội\b",
    r"\btoàn\s+diện\b",
    r"\bsâu\s+sắc\b",
    r"\bmạnh\s+mẽ\b",
    r"\bphong\s+phú\b",
    r"\bsinh\s+động\b",
    r"\bnổi\s+bật\b",
    r"\btiên\s+tiến\b",
    r"\bhàng\s+đầu\b",
    r"\buy\s+tín\b",
    r"\bchuyên\s+sâu\b",
    r"\bthiết\s+thực\b",
    r"hiệu\s+quả\s+cao\b",
    r"chất\s+lượng\s+cao\b",
    r"không\s+ngừng\s+(?:tăng|phát\s+triển|mở\s+rộng|hoàn\s+thiện)",
    r"mở\s+ra\s+hướng\s+đi\s+mới",
    r"tạo\s+tiền\s+đề",
    r"góp\s+phần\s+không\s+nhỏ",
    r"khẳng\s+định\s+vị\s+thế",
    r"dấu\s+mốc\s+quan\s+trọng",
    r"bước\s+tiến\s+quan\s+trọng",
    # English counterparts (ai-pattern-taxonomy §1)
    r"plays?\s+an?\s+(?:important|crucial|vital|key|pivotal)\s+role",
    r"\bgroundbreaking\b|\brevolutionary\b|\bremarkable\b|\bunprecedented\b",
    r"\bdelve\s+into\b",
    r"paves?\s+the\s+way\s+for|paved\s+the\s+way\s+for",
    r"a\s+testament\s+to",
]

UNQUANTIFIED = [
    r"\bđáng\s+kể\b",
    r"\brất\s+lớn\b",
    r"\bsignificantly\b",
    r"\bsubstantially\b",
    r"\bdramatically\b",
]

EMPTY_FRAMING = [
    r"có\s+thể\s+(?:thấy|nhận\s+thấy)\s+rằng",
    r"như\s+đã\s+đề\s+cập\s+ở\s+trên",
    r"như\s+chúng\s+ta\s+đã\s+biết",
    r"nói\s+chung\s+là\b",
    r"về\s+cơ\s+bản\s+(?:thì|là)\b",
    r"trong\s+(?:bối\s+cảnh\s+hiện\s+nay|thời\s+đại\s+ngày\s+nay)",
    r"việc\s+tiến\s+hành\s+thực\s+hiện",
    r"nhằm\s+mục\s+đích\s+để",
    r"có\s+một\s+nhu\s+cầu\s+cần\s+thiết\s+phải",
    r"mang\s+tính\s+chất\s+\S+",
    r"đóng\s+vai\s+trò\s+là\b",
    r"thực\s+hiện\s+việc\s+\S+",
    r"một\s+trong\s+những\s+[^.;]{0,60}\s+nhất\b",
    r"không\s+thể\s+phủ\s+nhận\s+rằng",
    r"it\s+can\s+be\s+seen\s+that",
    r"as\s+(?:mentioned|stated)\s+above",
    r"carry\s+out\s+the\s+process\s+of",
]

CALQUE = [
    r"đóng\s+một\s+vai\s+trò\s+quan\s+trọng\s+trong",
    r"nó\s+được\s+phát\s+hiện\s+ra\s+rằng",
    r"có\s+một\s+số\s+lượng\s+lớn\s+các",
    r"điều\s+quan\s+trọng\s+cần\s+lưu\s+ý\s+là",
    r"trong\s+điều\s+khoản\s+của",
    r"dựa\s+trên\s+một\s+cơ\s+sở\s+hàng\s+ngày",
    r"đối\s+chiếu\s+chống\s+lại",
    r"cam\s+kết\s+với\s+chất\s+lượng",
    r"cung\s+cấp\s+một\s+cái\s+nhìn\s+sâu\s+sắc",
    r"mở\s+đường\s+cho",
    r"bức\s+tranh\s+toàn\s+cảnh\s+về",
    r"theo\s+cách\s+mà\b",
]

DECORATIVE_PAIR = [
    r"toàn\s+diện\s+(?:và\s+)?sâu\s+sắc",
    r"phong\s+phú\s+(?:và\s+)?đa\s+dạng",
    r"đa\s+dạng\s+(?:và\s+)?phong\s+phú",
    r"nhanh\s+chóng\s+(?:và\s+)?hiệu\s+quả",
    r"chính\s+xác\s+(?:và\s+)?kịp\s+thời",
    r"kịp\s+thời\s+(?:và\s+)?chính\s+xác",
    r"đầy\s+đủ\s+và\s+toàn\s+diện",
]

# Ornament words counted only for the triad rule (registry §3).
ORNAMENT = [
    r"nhanh\s+chóng",
    r"hiệu\s+quả",
    r"chính\s+xác",
    r"đầy\s+đủ",
    r"toàn\s+diện",
    r"đa\s+dạng",
    r"phong\s+phú",
    r"linh\s+hoạt",
    r"mạnh\s+mẽ",
    r"sâu\s+sắc",
    r"vượt\s+trội",
    r"tối\s+ưu",
    r"sinh\s+động",
]

# Hedge markers (registry §6). One marker is correct; a stack is the defect.
HEDGE = [
    r"có\s+thể",
    r"có\s+khả\s+năng",
    r"dường\s+như",
    r"phần\s+nào",
    r"gợi\s+ý",
    r"nhìn\s+chung",
    r"tương\s+đối",
    r"hầu\s+như",
    r"có\s+xu\s+hướng",
]

PATTERNS: dict[str, list[str]] = {
    "ceremonial_padding": CEREMONIAL,
    "unquantified_intensifier": UNQUANTIFIED,
    "empty_framing": EMPTY_FRAMING,
    "translation_calque": CALQUE,
    "symmetric_padding": DECORATIVE_PAIR,
}

# --- licences (registry §7 and measured false positives) ---------------------

NEGATION = re.compile(
    r"không|chưa|thiếu|phủ\s+định|\bno\b|\bnot\b|cannot|does\s+not|fails?\s+to", re.I
)
NEGATION_WINDOW = 60

# `sâu`/`chuyên sâu` inside a named procedure or model family is terminology.
METHOD_TERM = re.compile(
    r"đọc\s+chuyên\s+sâu|phỏng\s+vấn\s+(?:chuyên\s+)?sâu|học\s+(?:máy\s+)?sâu"
    r"|mạng\s+(?:nơ-?ron|neural)\s+sâu|deep\s+learning",
    re.I,
)

QUANTITY = re.compile(re.escape(NUM) + r"|\d")
SOURCE = re.compile(re.escape(CITE))

GENRE_LICENSED = {
    "manuscript": set(),
    "thesis": set(),
    "acknowledgement": {"ceremonial_padding", "symmetric_padding"},
    "response_letter": {"empty_framing"},
}

THRESHOLDS = {
    "ceremonial_padding": 0,
    "unquantified_intensifier": 0,
    "empty_framing": 0,
    "translation_calque": 0,
    "symmetric_padding": 0,
    "ornamental_triad": 0,
    "hedge_stack": 0,
    "machine_marked_passage": 0,
}

VERDICTS = ("replace_with_measurement", "delete", "recast", "license")


def flatten(text: str) -> str:
    """Blank out notation, keep quantities and sources as placeholders."""
    text = COMMENT.sub(" ", text)
    text = FENCE.sub(" ", text)
    text = CITE_GROUP.sub(f" {CITE} ", text)
    text = REF_GROUP.sub(" ", text)
    text = MATH.sub(lambda m: f" {NUM} " if re.search(r"\d", m.group(0)) else " ", text)
    text = MACRO.sub(" ", text)
    return text.replace("{", " ").replace("}", " ")


def split_sections(text: str) -> list[tuple[int, str, str]]:
    """Return (index, heading, body) so a heading can license its own section."""
    marks = [(m.start(), m.end(), (m.group(1) or m.group(2) or "").strip()) for m in HEADING.finditer(text)]
    if not marks:
        return [(0, "", text)]
    sections: list[tuple[int, str, str]] = []
    if marks[0][0] > 0:
        sections.append((0, "", text[: marks[0][0]]))
    for idx, (_, end, title) in enumerate(marks, start=1):
        stop = marks[idx][0] if idx < len(marks) else len(text)
        sections.append((idx, title, text[end:stop]))
    return sections


def _licensed(code: str, sentence: str, hit_start: int, in_ack: bool) -> bool:
    """Return True when a lexical hit is a licensed construction, not a defect."""
    if in_ack and code in {"ceremonial_padding", "symmetric_padding"}:
        return True
    window = sentence[max(0, hit_start - NEGATION_WINDOW) : hit_start]
    if code == "ceremonial_padding":
        if NEGATION.search(window):
            return True
        if METHOD_TERM.search(sentence):
            return True
    if code == "unquantified_intensifier":
        if QUANTITY.search(sentence) or SOURCE.search(sentence):
            return True
    return False


def _count_distinct(sentence: str, patterns: list[str]) -> int:
    return sum(1 for p in patterns if re.search(p, sentence, re.I))


def scan(text: str, genre: str = "manuscript") -> dict:
    """Return Vietnamese AI-pattern candidates. Never edits text."""
    genre_licensed = GENRE_LICENSED.get(genre, set())
    findings: list[dict] = []
    total = 0

    for section_idx, heading, body in split_sections(text):
        in_ack = bool(ACK_SECTION.search(heading))
        sentences = [" ".join(s.split()) for s in SENTENCE.split(flatten(body))]
        sentences = [s for s in sentences if s]
        total += len(sentences)
        per_sentence_classes: list[set[str]] = []

        for local_idx, sentence in enumerate(sentences, start=1):
            classes: set[str] = set()
            for code, patterns in PATTERNS.items():
                if code in genre_licensed:
                    continue
                for pattern in patterns:
                    match = re.search(pattern, sentence, re.I)
                    if not match:
                        continue
                    if _licensed(code, sentence, match.start(), in_ack):
                        continue
                    classes.add(code)
                    findings.append(
                        {
                            "section": section_idx,
                            "heading": heading,
                            "sentence": local_idx,
                            "class": code,
                            "span": sentence[:300],
                            "matched": [pattern],
                            "verdict": "replace_with_measurement"
                            if code in {"ceremonial_padding", "unquantified_intensifier"}
                            else "delete",
                        }
                    )
                    break

            # Ornamental triad: three or more decorative adjectives and no measurement.
            if (
                "symmetric_padding" not in genre_licensed
                and not in_ack
                and not QUANTITY.search(sentence)
                and _count_distinct(sentence, ORNAMENT) >= 3
            ):
                classes.add("ornamental_triad")
                findings.append(
                    {
                        "section": section_idx,
                        "heading": heading,
                        "sentence": local_idx,
                        "class": "ornamental_triad",
                        "span": sentence[:300],
                        "matched": ["3+ ornamental adjectives, no measurement"],
                        "verdict": "replace_with_measurement",
                    }
                )

            # Hedge stack: one calibrated marker must survive, three is padding.
            if _count_distinct(sentence, HEDGE) >= 3:
                classes.add("hedge_stack")
                findings.append(
                    {
                        "section": section_idx,
                        "heading": heading,
                        "sentence": local_idx,
                        "class": "hedge_stack",
                        "span": sentence[:300],
                        "matched": ["3+ distinct hedge markers in one sentence"],
                        "verdict": "recast",
                    }
                )

            per_sentence_classes.append(classes)

        # Registry §8: a passage is machine-marked only when several independent
        # signals co-occur. One sentence carrying three distinct classes already
        # is co-occurrence, so the window must also cover documents shorter than
        # three sentences. Windows do not overlap: otherwise a single passage is
        # reported three times and the count stops meaning anything.
        cursor = 0
        while cursor < len(per_sentence_classes):
            window = per_sentence_classes[cursor : cursor + 3]
            union: set[str] = set()
            for classes_in_sentence in window:
                union |= classes_in_sentence
            if len(union) >= 3:
                findings.append(
                    {
                        "section": section_idx,
                        "heading": heading,
                        "sentence": cursor + 1,
                        "class": "machine_marked_passage",
                        "span": " ".join(sentences[cursor : cursor + 3])[:500],
                        "matched": [
                            f"{len(union)} distinct classes across "
                            f"{len(window)} sentence(s): " + ", ".join(sorted(union))
                        ],
                        "verdict": "recast",
                    }
                )
                cursor += len(window)
            else:
                cursor += 1

    # Uniform finding schema across gates: internal_register_scan.py emits
    # `licensable`, and licensed hits here are skipped at detection time, so
    # every finding this gate emits is actionable.
    for f in findings:
        f.setdefault("licensable", False)

    counts: dict[str, int] = {}
    for f in findings:
        counts[f["class"]] = counts.get(f["class"], 0) + 1

    checks = [
        {
            "check": code,
            "observed": counts.get(code, 0),
            "threshold": limit,
            "pass": counts.get(code, 0) <= limit,
        }
        for code, limit in THRESHOLDS.items()
        if code not in genre_licensed
    ]

    return {
        "genre": genre,
        "sentences": total,
        "counts": counts,
        "findings": findings,
        "thresholds": checks,
        "gate": "revise" if findings else "scan_clean",
        "blocking": [],
        "manual_pass_required": True,
        "note": (
            "A lexical hit is a candidate, never a verdict; absence of hits is a partial "
            "verification only. Hedge deletion and terminology drift are not detectable here."
        ),
        "exit_code": 2 if findings else 0,
    }


def render_report(result: dict) -> str:
    lines = [
        "# Vietnamese AI-pattern scan",
        "",
        f"- genre: `{result['genre']}`",
        f"- sentences: {result['sentences']}",
        f"- candidates: {len(result['findings'])}",
        f"- gate: **{result['gate']}**",
        "",
        "## Thresholds",
        "",
        "| check | observed | limit | pass |",
        "| --- | --- | --- | --- |",
    ]
    for c in result["thresholds"]:
        lines.append(
            f"| `{c['check']}` | {c['observed']} | {c['threshold']} | {'yes' if c['pass'] else 'NO'} |"
        )
    lines += ["", "## Findings", ""]
    if not result["findings"]:
        lines.append("No lexical candidates. The manual pass is still required.")
    for f in result["findings"]:
        lines.append(f"- `{f['class']}` §{f['section']} s{f['sentence']} → {f['verdict']}: {f['span']}")
    lines += ["", f"> {result['note']}"]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", type=Path)
    ap.add_argument("--genre", default="manuscript", choices=sorted(GENRE_LICENSED))
    ap.add_argument("--json", dest="json_path", type=Path, help="write the raw findings")
    ap.add_argument("--report", type=Path, help="write a Markdown report")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)
    try:
        result = scan(args.input.read_text(encoding="utf-8"), args.genre)
    except OSError as exc:
        print(f"input error: {exc}", file=sys.stderr)
        return 3
    if args.json_path:
        args.json_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    if args.report:
        args.report.write_text(render_report(result), encoding="utf-8")
    if not args.quiet:
        print(render_report(result))
    return result["exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())
