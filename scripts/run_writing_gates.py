#!/usr/bin/env python3
"""Run all mechanical academic-prose writing gates across files or directories.

Combines all five non-destructive scanners (internal register, process logic,
bilingual AI-pattern / calque detection, paragraph-level academic discourse, and
veracity protestation) into one entry point for every text-producing capability
(draft, develop, compress, expand, paraphrase, revise, humanize, translate, and
audit). Reports candidates and the mandatory manual syntactic-realization
checklist; never edits input files.

Exit codes:
  0  all mechanical checks clean (manual pass still required)
  1  at least one blocking finding (e.g., assistant/placeholder/artifact/venue leak)
  2  revision-level findings present, no blocking findings
  3  missing, unreadable, or unsupported input
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

import academic_discourse_scan  # noqa: E402
import internal_register_scan  # noqa: E402
import process_logic_scan  # noqa: E402
import tex_prose_extract  # noqa: E402
import veracity_protestation_scan  # noqa: E402
import vi_ai_pattern_scan  # noqa: E402

SUPPORTED_SUFFIXES = {".md", ".tex", ".txt", ".docx"}

GENRE_CHOICES = (
    "manuscript",
    "thesis",
    "report",
    "abstract",
    "slides",
    "teaching",
    "speaker_notes",
    "grant",
    "cover_letter",
    "response_letter",
    "revision_notes",
    "acknowledgement",
)

VI_DIACRITIC = re.compile(
    r"[ăâđêôơưàáảãạằắẳẵặầấẩẫậèéẻẽẹềếểễệìíỉĩịòóỏõọồốổỗộờớởỡợùúủũụừứửữựỳýỷỹỵ]",
    re.I,
)

MANUAL_PASS_CHECKLIST = [
    "Predicate-modifier binding: attach manner, method, or epistemic modifiers to the governing verb rather than trailing after a long noun phrase.",
    "Explicit subordination: unpack bare Noun + Verb/Negation chains with explicit linkers (`được`, `mà`, `khi`, `nếu chưa`, `do`) so agency and conditions remain recoverable.",
    "Referent-type precision: verify every head noun matches the operational object (sample vector vs distribution, score vs construct, draft vs enacted statute).",
    "Preposition and polysemy alignment: reserve `dưới` for physical position or causal force and resolve cross-discipline terms via `references/terminology-localization.md` §4.",
    "Proposition-density ceiling: split sentences cramming three or more independent claims or comparisons along natural analytical boundaries.",
    "Macro-to-micro framing: keep Abstract, Introduction, Contributions, and Conclusion conceptual—defer internal notation and table/p-value dumps to Model/Results and avoid repeating identical metric blocks across framing sections.",
    "Mathematical presentation and proof rigor: keep theorem statements free of inline proof justifications, structure proofs as setup -> aligned symbolic steps (align*) -> conclusion with verified foundational citations, and preserve equation numbering with zero Overfull \\hbox.",
    "Prose and visual scannability: strip stacked parenthetical asides and raw code/hyperparameter clutter, split Discussion/Limitations/Conclusion into one-idea paragraphs, promote dense multi-panel figures to figure*, and state a clear one-sentence takeaway for each table and figure.",
    "Uncaptured semantic checks: inspect hedge survival (no `stance_upgrade`), locked term identity (no `terminology_drift`), and quantitative bounds.",
]


def detect_language(text: str) -> str:
    """Detect whether prose uses Vietnamese diacritics ('vi') or defaults to 'en'."""
    return "vi" if VI_DIACRITIC.search(text) else "en"


def map_internal_genre(genre: str) -> str:
    """Map unified CLI genre to a genre accepted by internal_register_scan."""
    if genre in internal_register_scan.GENRE_LICENSED:
        return genre
    return "manuscript"


def map_vi_pattern_genre(genre: str) -> str:
    """Map unified CLI genre to a genre accepted by vi_ai_pattern_scan."""
    if genre in vi_ai_pattern_scan.GENRE_LICENSED:
        return genre
    if genre == "revision_notes":
        return "response_letter"
    return "manuscript"


def map_veracity_genre(genre: str) -> str:
    """Map unified CLI genre to a genre accepted by veracity_protestation_scan."""
    if genre == "slides":
        return "slide"
    if genre in {"manuscript", "thesis", "abstract"}:
        return "manuscript"
    if genre == "report":
        return "report"
    return "auto"


def collect_targets(paths: list[Path]) -> list[Path]:
    """Resolve input files or directories into sorted supported document paths."""
    collected: list[Path] = []
    seen: set[Path] = set()
    for raw in paths:
        if not raw.exists():
            raise FileNotFoundError(f"path not found: {raw}")
        if raw.is_file():
            if raw.suffix.lower() not in SUPPORTED_SUFFIXES:
                raise ValueError(f"unsupported file type: {raw}")
            resolved = raw.resolve()
            if resolved not in seen:
                seen.add(resolved)
                collected.append(raw)
        elif raw.is_dir():
            for child in sorted(raw.rglob("*")):
                if not child.is_file():
                    continue
                if child.suffix.lower() not in SUPPORTED_SUFFIXES:
                    continue
                rel_parts = child.relative_to(raw).parts
                if any(part.startswith(".") or part == "__pycache__" for part in rel_parts):
                    continue
                resolved = child.resolve()
                if resolved not in seen:
                    seen.add(resolved)
                    collected.append(child)
        else:
            raise ValueError(f"unsupported path type: {raw}")
    if not collected:
        raise FileNotFoundError("no supported (.md, .tex, .txt, .docx) files found")
    return collected


def _is_tex_source(text: str, source: str) -> bool:
    return source.lower().endswith(".tex") or "\\begin{" in text or "\\section" in text or "\\documentclass" in text


def scan_text(text: str, *, lang: str = "auto", genre: str = "manuscript", source: str = "<text>") -> dict:
    """Run all five mechanical gates on an in-memory text buffer."""
    resolved_lang = detect_language(text) if lang == "auto" else lang
    reg_genre = map_internal_genre(genre)
    vi_genre = map_vi_pattern_genre(genre)
    ver_genre = map_veracity_genre(genre)

    reg_res = internal_register_scan.scan(text, genre=reg_genre)
    proc_res = process_logic_scan.scan(text)
    vi_res = vi_ai_pattern_scan.scan(text, genre=vi_genre)

    discourse_input = tex_prose_extract.extract_prose(text) if _is_tex_source(text, source) else text
    disc_res = academic_discourse_scan.scan(discourse_input, genre=genre)
    ver_res = veracity_protestation_scan.scan(text, source=source, genre=ver_genre)

    reg_actionable = [f for f in reg_res["findings"] if not f["licensable"]]
    blocking_items = [f for f in reg_actionable if f["blocking"]]
    reg_rev = [f for f in reg_actionable if not f["blocking"]]
    proc_rev = list(proc_res["findings"])
    vi_rev = list(vi_res["findings"])
    disc_rev = [f for f in disc_res["findings"] if not f.get("licensable")]
    ver_rev = list(ver_res["findings"])

    blocking_count = len(blocking_items)
    revision_count = len(reg_rev) + len(proc_rev) + len(vi_rev) + len(disc_rev) + len(ver_rev)
    gate = "block" if blocking_count else ("revise" if revision_count else "scan_clean")

    return {
        "source": source,
        "language": resolved_lang,
        "genre": genre,
        "blocking_count": blocking_count,
        "revision_count": revision_count,
        "blocking_classes": sorted({f["class"] for f in blocking_items}),
        "gate": gate,
        "scanners": {
            "internal_register": reg_res,
            "process_logic": proc_res,
            "ai_pattern": vi_res,
            "academic_discourse": disc_res,
            "veracity_protestation": ver_res,
        },
    }


def scan_paths(paths: list[Path], *, lang: str = "auto", genre: str = "manuscript") -> dict:
    """Run unified writing gates across all resolved files and aggregate summary."""
    targets = collect_targets(paths)
    file_results: list[dict] = []
    for path in targets:
        text = internal_register_scan.read_input(path)
        file_results.append(scan_text(text, lang=lang, genre=genre, source=str(path)))

    blocking_total = sum(r["blocking_count"] for r in file_results)
    revision_total = sum(r["revision_count"] for r in file_results)
    gate = "block" if blocking_total else ("revise" if revision_total else "scan_clean")
    exit_code = 1 if blocking_total else (2 if revision_total else 0)

    return {
        "genre": genre,
        "language_mode": lang,
        "files": file_results,
        "summary": {
            "total_files": len(file_results),
            "blocking_findings": blocking_total,
            "revision_findings": revision_total,
            "gate": gate,
        },
        "manual_pass_required": True,
        "manual_pass_checklist": MANUAL_PASS_CHECKLIST,
        "exit_code": exit_code,
    }


def render_report(result: dict) -> str:
    """Render a compact Markdown report for one or more scanned files."""
    summary = result["summary"]
    lines = [
        "# Unified Academic-Prose Writing Gate",
        "",
        f"- genre: `{result['genre']}`",
        f"- files scanned: {summary['total_files']}",
        f"- blocking findings: {summary['blocking_findings']}",
        f"- revision findings: {summary['revision_findings']}",
        f"- overall gate: **{summary['gate']}**",
        "",
        "## Per-file Summary",
        "",
        "| File | Lang | Blocking | Revision | Gate |",
        "| --- | :---: | ---: | ---: | --- |",
    ]
    for item in result["files"]:
        lines.append(
            f"| `{item['source']}` | `{item['language']}` | {item['blocking_count']} | {item['revision_count']} | `{item['gate']}` |"
        )

    lines += ["", "## Findings", ""]
    has_any = False
    for item in result["files"]:
        src = item["source"]
        for f in item["scanners"]["internal_register"]["findings"]:
            if f["licensable"]:
                continue
            has_any = True
            tag = "BLOCK" if f["blocking"] else "REVISE"
            lines.append(f"- [{tag}] `{src}` `{f['class']}` §{f['section']} s{f['sentence']}: {f['span']}")
        for f in item["scanners"]["process_logic"]["findings"]:
            has_any = True
            lines.append(f"- [REVISE] `{src}` `{f['class']}` s{f['sentence']} → {f['verdict']}: {f['span']}")
        for f in item["scanners"]["ai_pattern"]["findings"]:
            has_any = True
            lines.append(f"- [REVISE] `{src}` `{f['class']}` §{f['section']} s{f['sentence']} → {f['verdict']}: {f['span']}")
        for f in item["scanners"]["academic_discourse"]["findings"]:
            if f.get("licensable"):
                continue
            has_any = True
            loc = f"p{f['paragraph']}" + (f" s{f['sentence']}" if f.get("sentence") else "")
            lines.append(f"- [REVISE] `{src}` `{f['class']}` {loc} → {f['verdict']}: {f['span']}")
        for f in item["scanners"]["veracity_protestation"]["findings"]:
            has_any = True
            lines.append(f"- [REVISE] `{src}` `{f['class']}` s{f['sentence_no']} → {f['verdict']}: {f['span']}")
    if not has_any:
        lines.append("No lexical candidates flagged across the scanned files.")

    lines += ["", "## Mandatory Manual Pass Checklist", ""]
    for check in result["manual_pass_checklist"]:
        lines.append(f"- [ ] {check}")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("inputs", nargs="+", type=Path, help="file(s) or directory(ies) to scan")
    ap.add_argument("--lang", default="auto", choices=("auto", "vi", "en"))
    ap.add_argument("--genre", default="manuscript", choices=GENRE_CHOICES)
    ap.add_argument("--json", dest="json_path", type=Path, help="write raw JSON report")
    ap.add_argument("--report", type=Path, help="write Markdown summary report")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    try:
        result = scan_paths(args.inputs, lang=args.lang, genre=args.genre)
    except (OSError, ValueError, KeyError, zipfile.BadZipFile, ET.ParseError) as exc:
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
