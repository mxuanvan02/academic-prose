#!/usr/bin/env python3
"""Detect publication-internal register in text, LaTeX, Markdown, or DOCX.

A lexical hit is a candidate, never a verdict: the gate document requires each
finding to be resolved by the referent, permanence, and outsider-verifiability
tests, and the resolution recorded as delete / recast / relocate / license.
Absence of hits is not a pass either -- paraphrases of the paraphrasable classes
have no lexical signature.

Exit: 0 clean, 1 blocking class present, 2 revision-level findings, 3 input error.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

# --- classes -----------------------------------------------------------------

BLOCKING = {
    "assistant_residue",
    "placeholder_residue",
    "internal_artifact_reference",
    "venue_ambition_leak",
}

PATTERNS: dict[str, list[str]] = {
    "self_reminder_prose": [
        r"cần\s+(?:nêu|lưu\s+ý|thận\s+trọng|được\s+nêu|phải\s+nêu|được\s+diễn\s+giải)",
        r"được\s+nêu\s+(?:dưới\s+đây|ở\s+dưới)",
        r"(?:xin|cần)\s+lưu\s+ý\s+rằng",
        r"it\s+should\s+be\s+noted",
        r"care\s+must\s+be\s+taken",
        r"the\s+following\s+must\s+be\s+stated",
    ],
    "document_as_subject": [
        r"(?:phần|mục|chương)\s+này\s+(?:sẽ|trình\s+bày|mô\s+tả|giới\s+thiệu)",
        r"như\s+đã\s+(?:đề\s+cập|trình\s+bày|nói)\s+(?:ở\s+)?(?:trên|dưới|phần\s+trước)",
        r"ở\s+(?:đoạn|phần)\s+(?:trên|dưới|trước|sau)\b",
        r"this\s+(?:section|paper|article|chapter)\s+(?:will|presents\s+below)",
        r"as\s+(?:mentioned|discussed)\s+above",
    ],
    "progress_state_limitation": [
        r"chưa\s+(?:kịp|hoàn\s+tất|bổ\s+sung|thực\s+hiện|được\s+thẩm\s+định)",
        r"sẽ\s+(?:bổ\s+sung|hoàn\s+thiện|cập\s+nhật)\s+(?:sau|trong\s+thời\s+gian\s+tới)",
        r"đang\s+trong\s+quá\s+trình",
        r"nhóm\s+(?:nghiên\s+cứu\s+)?chưa\b",
        r"remains?\s+to\s+be\s+done",
        r"(?:has\s+not|have\s+not|hasn't|haven't)\s+(?:yet\s+)?(?:been\s+)?(?:completed|finished|added|validated|annotated)",
        r"(?:will|is\s+planned\s+to)\s+(?:be\s+)?(?:added|completed|updated)\s+(?:later|in\s+future\s+work|in\s+a\s+future\s+release)",
        r"(?:is|are)\s+still\s+(?:in\s+progress|underway|pending)",
    ],
    "verification_log_prose": [
        r"(?:chúng\s+tôi\s+)?đã\s+(?:kiểm\s+tra|biên\s+dịch|chạy|xác\s+nhận|rà\s+soát)",
        r"checksum\s+(?:khớp|match)",
        r"\b0\s*lỗi\b",
        r"\bkhông\s+phát\s+hiện\s+lỗi\b",
        r"đã\s+được\s+kiểm\s+tra\s+lại",
        r"(?:we\s+)?(?:checked|verified|confirmed|reran|re-ran|compiled)\b",
        r"(?:the\s+)?checksum\s+(?:matched|matches)",
        r"\b(?:zero|0)\s+(?:errors|failures)\b",
        r"(?:no\s+(?:errors|failures)\s+(?:were\s+)?found|passed\s+all\s+checks)",
    ],
    # Blocking: no reader of the published artifact can reach these.
    "internal_artifact_reference": [
        r"(?:/Users|/home|/tmp|/var/folders|[A-Z]:\\\\)[^\s,;)`'\"}]*",
        r"\b(?:main|draft|manuscript|ban_thao)\.(?:tex|docx?)\b",
        r"\bv\d+(?:[._-]?final|[._-]?rev\d*)\b",
        r"\b(?:commit|sha)\s+[0-9a-f]{7,40}\b",
        r"(?:^|\s)#\d{2,}\b",
        r"\b(?:cột|sheet|tab)\s+[\"'`][^\"'`]+[\"'`]",
    ],
    # Revision-level: a repo-relative artifact name is licensed inside a data or
    # reproducibility statement and a leak anywhere else.
    "repo_artifact_reference": [
        r"\b[\w./-]*\w+\.(?:py|ipynb|csv|tsv|jsonl?|xlsx|log|sh|yaml|yml)\b",
        r"\bscripts?/[\w./-]+",
    ],
    "assistant_residue": [
        r"theo\s+(?:yêu\s+cầu|đề\s+nghị)\s+của\s+(?:anh|chị|bạn|ông|bà)",
        r"như\s+(?:anh|chị|bạn)\s+(?:đã\s+)?(?:yêu\s+cầu|nói)",
        r"as\s+(?:you\s+)?requested",
        r"\bthe\s+assistant\b",
        r"chúng\s+ta\s+đã\s+(?:sửa|viết|thống\s+nhất)",
    ],
    "placeholder_residue": [
        r"\b(?:TODO|TBD|FIXME|XXX)\b",
        r"\[\s*\.\.\.\s*\]",
        r"\[(?:điền|cần\s+bổ\s+sung|chưa\s+có)[^\]]*\]",
        r"\?{3,}",
        r"\bLorem\s+ipsum\b",
    ],
    "revision_response_leak": [
        r"theo\s+(?:góp\s+ý|yêu\s+cầu|nhận\s+xét)\s+của\s+(?:phản\s+biện|người\s+phản\s+biện|reviewer)",
        r"as\s+the\s+reviewer\s+(?:requested|suggested)",
        r"trong\s+bản\s+(?:sửa|hiệu\s+đính)\s+này,?\s+chúng\s+tôi\s+đã",
    ],
    # Blocking: the submission strategy is a private matter between the authors
    # and, at most, the editor. A manuscript that argues its own venue tier is
    # asking the reader to accept prestige in place of evidence.
    # Publication strategy: true of the project, never a finding about the world.
    # Ranking vocabulary only fires when it qualifies a *venue*; `Q1-Q3`,
    # `first quartile of severity`, `Q1 2023`, and a Scopus *search* are
    # legitimate scientific prose and must stay silent.
    "venue_ambition_leak": [
        r"(?:thuộc\s+)?(?:nhóm|hạng)\s*Q[1-4]\b",
        r"\bQ[1-4]\s*(?:journal|venue|tạp\s+chí)",
        r"\b(?:journal|venue|tạp\s+chí)\b[^.;]{0,40}\bQ[1-4]\b",
        r"\btạp\s+chí\s+(?:uy\s+tín|hàng\s+đầu|top|danh\s+giá)",
        r"\b(?:top[-\s]?tier|high[-\s]?impact|prestigious|flagship)\s+(?:journal|venue|conference|publication|outlet)",
        r"\bimpact\s+factor\s+(?:of\s+(?:the\s+)?)?(?:journal|venue)",
        r"(?:journal|venue)[^.;]{0,30}\bimpact\s+factor\b",
        r"\bchỉ\s+số\s+ảnh\s+hưởng\s+(?:của\s+)?tạp\s+chí",
        r"\b(?:Scopus|Web\s+of\s+Science|WoS|ISI)[-\s]?(?:indexed\s+)?(?:journal|venue|tạp\s+chí)",
        r"\b(?:aim|aims|aiming|intend|intends|plan|plans)\s+to\s+(?:publish|submit)",
        r"\bmục\s+tiêu\s+(?:công\s+bố|nộp|đăng)",
        r"\bđủ\s+điều\s+kiện\s+(?:công\s+bố|đăng|nộp)",
        r"\b(?:submitted|submission)\s+to\s+(?:a\s+)?(?:top|high|Q[1-4])",
        r"\breviewers?\s+(?:will|would|may|might)\s+(?:likely\s+)?(?:ask|expect|demand|require|object)",
        r"\bto\s+satisfy\s+(?:the\s+)?reviewers?\b",
        r"(?:để|nhằm|hòng)\s+(?:thuyết\s+phục|làm\s+hài\s+lòng|xoa\s+dịu|đáp\s+ứng)\s+(?:được\s+)?(?:người\s+)?(?:phản\s+biện|reviewer)",
        r"\btránh\s+(?:bị\s+)?(?:từ\s+chối|loại)\s+(?:sớm|ngay|từ\s+vòng)",
        r"\bdesk\s+reject",
        r"\b(?:avoid|prevent)\s+(?:a\s+)?(?:rejection|desk\s+reject)",
        r"\btránh\s+bị\s+(?:từ\s+chối|loại)\b",
    ],
}

# Claim-denial markers only. A bare `chỉ` or `không` is ordinary Vietnamese; the
# defect is a stack of sentences that deny a claim nobody made.
CLAIM_DENIAL = re.compile(
    r"(?:^|[\s,;(])(?:"
    r"không\s+(?:chứng\s+minh|bảo\s+đảm|hàm\s+ý|thiết\s+lập|khẳng\s+định|"
    r"cho\s+phép\s+(?:kết\s+luận|suy\s+rộng)|đủ\s+để\s+kết\s+luận)"
    r"|không\s+phải\s+là"
    r"|chỉ\s+(?:thiết\s+lập|cho\s+thấy|mang\s+tính|có\s+giá\s+trị|phản\s+ánh|áp\s+dụng)"
    r"|do(?:es)?\s+not\s+(?:prove|guarantee|imply|establish|validate|support|demonstrate)"
    r"|cannot\s+(?:prove|guarantee|imply|establish|validate|support|demonstrate)"
    r"|only\s+(?:establish(?:es)?|show(?:s)?|reflect(?:s)?|appl(?:y|ies)\s+to|has\s+diagnostic\s+value)"
    r")",
    re.I,
)
# `không chỉ ... mà còn` is emphatic, the opposite of a disclaimer.
DENIAL_EXCLUDE = re.compile(r"không\s+chỉ|not\s+only", re.I)

# Sections where a repo-relative artifact name is the licensed register.
ARTIFACT_LICENSED_SECTION = re.compile(
    r"(?:tái\s+lập|khả\s+năng\s+tái\s+lập|tuyên\s+bố\s+dữ\s+liệu|dữ\s+liệu\s+và\s+mã|"
    r"phụ\s+lục|reproducib|data\s+(?:and\s+code\s+)?availab|code\s+availab|"
    r"artifact|appendix|supplementary)",
    re.I,
)

GENRE_LICENSED: dict[str, set[str]] = {
    "manuscript": set(),
    "thesis": set(),
    "report": set(),
    "abstract": set(),
    "response_letter": {"revision_response_leak", "assistant_residue", "document_as_subject"},
    # The cover letter argues venue fit to the editor by design, and revision
    # notes discuss the referees. Neither is publication-facing prose.
    "cover_letter": {
        "venue_ambition_leak",
        "revision_response_leak",
        "assistant_residue",
        "document_as_subject",
    },
    "revision_notes": {
        "revision_response_leak",
        "assistant_residue",
        "document_as_subject",
        "venue_ambition_leak",
    },
    "teaching": {"document_as_subject"},
    "slides": {"document_as_subject"},
    "speaker_notes": {"document_as_subject"},
}

SENTENCE = re.compile(r"(?<=[.!?;])\s+|\n{2,}")
HEADING = re.compile(r"^(?:#{1,6}\s+\S|\\(?:sub)*section\*?\{)", re.M)
HEADING_TITLE = re.compile(r"^(?:#{1,6}\s+(?P<md>.+)|\\(?:sub)*section\*?\{(?P<tex>[^}]*)\})")

# Thresholds mirror references/internal-register-gate.md section 5.
THRESHOLDS = {
    "self_reminder_prose": 0,
    "assistant_residue": 0,
    "placeholder_residue": 0,
    "internal_artifact_reference": 0,
    "repo_artifact_reference": 0,
    "progress_state_limitation": 0,
    "verification_log_prose": 0,
    "revision_response_leak": 0,
    "venue_ambition_leak": 0,
    "document_as_subject": 1,  # one roadmap per document
    "defensive_disclaimer_stack": 0,
}


def read_input(path: Path) -> str:
    if path.suffix.lower() == ".docx":
        with zipfile.ZipFile(path) as zf:
            root = ET.fromstring(zf.read("word/document.xml"))
        parts: list[str] = []
        for node in root.iter():
            if node.tag.endswith("}p"):
                parts.append("\n\n")
            elif node.tag.endswith("}t"):
                parts.append(node.text or "")
        return "".join(parts)
    return path.read_text(encoding="utf-8")


def strip_protected(text: str) -> str:
    """Blank out the zones the policy exempts (gate document section 7)."""
    is_tex = "\\begin{" in text or "\\section" in text or "\\documentclass" in text
    if is_tex:
        # The preamble is configuration, not publication-facing prose.
        body = re.split(r"\\begin\{document\}", text, maxsplit=1)
        text = body[1] if len(body) > 1 else text
        text = re.split(r"\\end\{document\}", text, maxsplit=1)[0]
        text = re.sub(r"(?<!\\)%[^\n]*", " ", text)
        text = re.sub(
            r"(?s)\\begin\{(verbatim|lstlisting|minted|Verbatim|tabular\*?|tabularx)\}.*?"
            r"\\end\{\1\}",
            " ",
            text,
        )
        text = re.sub(r"\\(?:verb|lstinline|path)\|[^|]*\|", " ", text)
        text = re.sub(r"\\(?:cite[a-z]*|ref|eqref|label|url|href|bibitem|input|include)\s*\{[^}]*\}", " ", text)
        text = re.sub(r"(?s)\\begin\{thebibliography\}.*?\\end\{thebibliography\}", " ", text)
    text = re.sub(r"(?s)```.*?```", " ", text)
    text = re.sub(r"(?s)~~~.*?~~~", " ", text)
    text = re.sub(r"(?s)\$\$.*?\$\$", " ", text)
    text = re.sub(r"(?<!\\)\$[^$\n]*\$", " ", text)
    text = re.sub(r"https?://doi\.org/\S+|\bdoi:\s*\S+|\bDOI\s+10\.\S+", " ", text, flags=re.I)
    text = re.sub(r"https?://\S+", " ", text)
    return text


def flatten_markup(text: str) -> str:
    """Drop LaTeX command names but keep their textual argument."""
    protected_heads = re.sub(r"\\((?:sub)*section)\*?\{", r"\n\n@@HEAD:\1@@ ", text)
    stripped = re.sub(r"\\[a-zA-Z@]+\*?(?:\[[^\]]*\])?", " ", protected_heads)
    stripped = stripped.replace("{", " ").replace("}", " ")
    return re.sub(r"@@HEAD:((?:sub)*section)@@", r"\\\1{", stripped)


def _heading_title(chunk: str) -> str:
    match = HEADING_TITLE.match(chunk.strip())
    if not match:
        return ""
    return (match.group("md") or match.group("tex") or "").strip()


def split_sections(text: str) -> list[tuple[int, str, str]]:
    """Return (index, heading_title, section_text). Index 0 is front matter."""
    bounds = [m.start() for m in HEADING.finditer(text)]
    if not bounds:
        return [(0, "", text)]
    chunks: list[tuple[int, str, str]] = []
    if bounds[0] > 0:
        chunks.append((0, "", text[: bounds[0]]))
    for i, start in enumerate(bounds, start=1):
        end = bounds[i] if i < len(bounds) else len(text)
        chunk = text[start:end]
        chunks.append((i, _heading_title(chunk), chunk))
    return chunks


def scan(text: str, genre: str = "manuscript") -> dict:
    licensed = GENRE_LICENSED.get(genre, set())
    clean = flatten_markup(strip_protected(text))
    findings: list[dict] = []
    total_sentences = 0

    for section_idx, heading, section_text in split_sections(clean):
        sentences = [s.strip() for s in SENTENCE.split(section_text) if s.strip()]
        total_sentences += len(sentences)
        artifact_slot = bool(ARTIFACT_LICENSED_SECTION.search(heading))
        per_section_doc_subject = 0

        for local_idx, sentence in enumerate(sentences, 1):
            for code, patterns in PATTERNS.items():
                if code in licensed:
                    continue
                matched = [p for p in patterns if re.search(p, sentence, re.I)]
                if not matched:
                    continue
                finding = {
                    "section": section_idx,
                    "heading": heading,
                    "sentence": local_idx,
                    "class": code,
                    "span": sentence[:300],
                    "matched": matched,
                    "blocking": code in BLOCKING,
                    "licensable": False,
                }
                if code == "document_as_subject":
                    per_section_doc_subject += 1
                    # The first such sentence in the opening section may be the
                    # licensed roadmap; the author records `license` as verdict.
                    finding["licensable"] = section_idx <= 1 and per_section_doc_subject == 1
                elif code == "repo_artifact_reference":
                    finding["licensable"] = artifact_slot
                findings.append(finding)

        for i in range(max(0, len(sentences) - 2)):
            window = sentences[i : i + 3]
            count = sum(len(CLAIM_DENIAL.findall(DENIAL_EXCLUDE.sub(" ", s))) for s in window)
            if count >= 3:
                findings.append(
                    {
                        "section": section_idx,
                        "heading": heading,
                        "sentence": i + 1,
                        "class": "defensive_disclaimer_stack",
                        "span": " ".join(window)[:500],
                        "matched": [f"{count} claim-denial markers in 3 sentences"],
                        "blocking": False,
                        "licensable": False,
                    }
                )

    counts: dict[str, int] = {}
    for f in findings:
        counts[f["class"]] = counts.get(f["class"], 0) + 1

    checks = []
    for code, limit in THRESHOLDS.items():
        if code in licensed:
            continue
        observed = sum(1 for f in findings if f["class"] == code and not f["licensable"])
        checks.append(
            {"check": code, "observed": observed, "threshold": limit, "pass": observed <= limit}
        )

    actionable = [f for f in findings if not f["licensable"]]
    blocking = sorted({f["class"] for f in actionable if f["blocking"]})
    exit_code = 1 if blocking else (2 if actionable else 0)

    return {
        "genre": genre,
        "sentences": total_sentences,
        "counts": counts,
        "findings": findings,
        "thresholds": checks,
        "blocking": blocking,
        "gate": "block" if blocking else ("revise" if actionable else "scan_clean"),
        "manual_pass_required": True,
        "note": "A lexical hit is a candidate; absence of hits is a partial verification only.",
        "exit_code": exit_code,
    }


def render_report(result: dict) -> str:
    lines = [
        "# Internal register scan",
        "",
        f"- genre: `{result['genre']}`",
        f"- sentences: {result['sentences']}",
        f"- gate: **{result['gate']}**",
        "",
    ]
    if result["blocking"]:
        lines += ["## Blocking classes", ""] + [f"- `{c}`" for c in result["blocking"]] + [""]
    lines += ["## Thresholds", "", "| check | observed | limit | pass |", "| --- | --- | --- | --- |"]
    for c in result["thresholds"]:
        lines.append(
            f"| `{c['check']}` | {c['observed']} | {c['threshold']} | {'yes' if c['pass'] else 'NO'} |"
        )
    lines += ["", "## Findings", ""]
    if not result["findings"]:
        lines.append("No lexical candidates. The manual pass is still required.")
    for f in result["findings"]:
        tag = " (licensable)" if f["licensable"] else ""
        lines.append(f"- `{f['class']}`{tag} — §{f['section']} s{f['sentence']}: {f['span']}")
    lines += ["", f"> {result['note']}"]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", type=Path)
    ap.add_argument("--genre", default="manuscript", choices=sorted(GENRE_LICENSED))
    ap.add_argument("--report", type=Path, help="write a Markdown report")
    ap.add_argument("--json", dest="json_path", type=Path, help="write the raw findings")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)
    try:
        result = scan(read_input(args.input), args.genre)
    except (OSError, KeyError, zipfile.BadZipFile, ET.ParseError) as exc:
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
