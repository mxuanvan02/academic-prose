#!/usr/bin/env python3
"""Measure a built DOCX against a journal's stated limits.

Why this exists: source-level word counts and the rendered DOCX disagree, and the
editor measures the DOCX. Markdown table delimiters are not words but rendered
cell text is; footnote markers vanish on render while footnote bodies count.
Measured divergence on identical content: 9,999 (Markdown) vs 10,138 (DOCX).

Counts three in-budget buckets SEPARATELY so an overage is attributable:
    main paragraphs (from the body-start heading onward) + table cells + footnotes

Usage:
    python verify_journal_docx.py FILE.docx
    python verify_journal_docx.py FILE.docx --limit 10000 --abstract-cap 250 \
        --body-start '# 1.' --min-refs 10 --bib-heading 'DANH MỤC TÀI LIỆU'

Requires: python-docx. `pdfinfo` (poppler-utils) is used opportunistically for
page count if a sibling PDF exists; absence is reported, not fatal.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import zipfile
from pathlib import Path

try:
    from docx import Document
    from docx.shared import Cm
except ImportError:
    sys.exit("python-docx not installed: pip install python-docx")

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def words(text: str) -> int:
    """Count words the way a word processor does: whitespace-delimited tokens
    that contain at least one alphanumeric character. Bare punctuation cells and
    table rule artifacts do not count."""
    return sum(1 for t in text.split() if any(ch.isalnum() for ch in t))


def footnote_bodies(path: Path) -> tuple[int, int]:
    """Return (footnote word count, footnote body count) from word/footnotes.xml.

    Skips the two Word-internal separator footnotes (id 0 and -1)."""
    with zipfile.ZipFile(path) as z:
        if "word/footnotes.xml" not in z.namelist():
            return 0, 0
        xml = z.read("word/footnotes.xml").decode("utf-8", "replace")

    total, count = 0, 0
    for chunk in re.findall(r"<w:footnote\b[^>]*>(.*?)</w:footnote>", xml, re.S):
        body = " ".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", chunk, re.S))
        if not body.strip():
            continue
        count += 1
        total += words(body)
    return total, count


def footnote_refs(path: Path) -> int:
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8", "replace")
    return len(re.findall(r"<w:footnoteReference\b", xml))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("docx")
    ap.add_argument("--limit", type=int, default=10000,
                    help="in-budget word ceiling (main+tables+footnotes+bib)")
    ap.add_argument("--floor", type=int, default=6000)
    ap.add_argument("--abstract-cap", type=int, default=250)
    ap.add_argument("--body-start", default="# 1.",
                    help="text prefix of the first in-budget heading")
    ap.add_argument("--min-refs", type=int, default=10)
    ap.add_argument("--bib-heading", default="DANH MỤC TÀI LIỆU")
    ap.add_argument("--abstract-labels", default="Tóm tắt,Abstract")
    ap.add_argument("--keyword-labels", default="Từ khóa,Keywords")
    args = ap.parse_args()

    path = Path(args.docx)
    doc = Document(path)

    # --- page geometry -------------------------------------------------------
    sec = doc.sections[0]
    def cm(v):
        return round(v / Cm(1), 2) if v is not None else None
    print(f"PAGE      {cm(sec.page_width)} x {cm(sec.page_height)} cm")
    print(f"MARGINS   top={cm(sec.top_margin)} bottom={cm(sec.bottom_margin)} "
          f"left={cm(sec.left_margin)} right={cm(sec.right_margin)} cm")

    # --- fonts / spacing actually present ------------------------------------
    with zipfile.ZipFile(path) as z:
        docxml = z.read("word/document.xml").decode("utf-8", "replace")
        has_footer = any(n.startswith("word/footer") for n in z.namelist())
        footer_page_field = False
        for n in z.namelist():
            if n.startswith("word/footer"):
                if "PAGE" in z.read(n).decode("utf-8", "replace"):
                    footer_page_field = True
    fonts = sorted(set(re.findall(r'w:ascii="([^"]+)"', docxml)))
    sizes = sorted({int(s) / 2 for s in re.findall(r'<w:sz w:val="(\d+)"', docxml)})
    spacing = sorted(set(re.findall(r'<w:spacing[^>]*w:line="(\d+)"', docxml)))
    print(f"FONTS     {fonts}")
    print(f"SIZES pt  {sizes}")
    print(f"SPACING   {spacing}  (240=1.0, 360=1.5)")
    print(f"FOOTER    present={has_footer} PAGE_field={footer_page_field}")

    # --- word buckets --------------------------------------------------------
    in_body = False
    main_words = 0
    bib_entries = 0
    in_bib = False
    abstracts: dict[str, int] = {}
    keywords: dict[str, int] = {}
    alabels = [s.strip() for s in args.abstract_labels.split(",") if s.strip()]
    klabels = [s.strip() for s in args.keyword_labels.split(",") if s.strip()]

    for p in doc.paragraphs:
        text = p.text.strip()
        if not text:
            continue

        for lab in alabels:
            if text.startswith(lab):
                abstracts[lab] = words(text) - words(lab)
        for lab in klabels:
            if text.startswith(lab):
                # keywords are separator-delimited, NOT whitespace-delimited.
                # A naive whitespace count reported 4 for a correct 5-item line.
                payload = text.split(":", 1)[-1]
                items = [x.strip(" .;") for x in payload.split(";")]
                keywords[lab] = len([x for x in items if x])

        if args.bib_heading.lower() in text.lower():
            in_bib = True
            continue
        if in_bib:
            bib_entries += 1

        if not in_body and text.startswith(args.body_start):
            in_body = True
        if in_body:
            main_words += words(text)

    table_words = sum(
        words(cell.text)
        for t in doc.tables for row in t.rows for cell in row.cells
    )
    fn_words, fn_bodies = footnote_bodies(path)
    refs = footnote_refs(path)

    total = main_words + table_words + fn_words

    print()
    print(f"main paragraphs   {main_words}")
    print(f"table cells       {table_words}")
    print(f"footnote bodies   {fn_words}")
    print(f"=> IN-BUDGET      {total}   [require {args.floor}-{args.limit}]")
    if total > args.limit:
        print(f"   OVERAGE        {total - args.limit}  <-- rewrite whole sections "
              f"to target; do NOT nibble")
    elif total < args.floor:
        print(f"   UNDER FLOOR    {args.floor - total}  <-- add scientific content only")

    for lab in alabels:
        v = abstracts.get(lab)
        flag = "" if v is None or v <= args.abstract_cap else "  <-- OVER CAP"
        print(f"{lab:<10} {v}   [<= {args.abstract_cap}]{flag}")
    for lab in klabels:
        print(f"{lab:<10} {keywords.get(lab)} items")

    print(f"TLTK entries      {bib_entries}   [>= {args.min_refs}]")
    print(f"footnote refs     {refs}")
    print(f"footnote bodies   {fn_bodies}")
    if refs != fn_bodies:
        print("   MISMATCH: every marker must have exactly one body")

    tbl_borders = len(re.findall(r"<w:tblBorders", docxml))
    print(f"tables            {len(doc.tables)}  bordered={tbl_borders}")

    pdf = path.with_suffix(".pdf")
    if pdf.exists():
        try:
            out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True,
                                 text=True, check=False).stdout
            for line in out.splitlines():
                if line.startswith(("Pages:", "Page size:")):
                    print(f"PDF {line}")
        except FileNotFoundError:
            print("PDF present; pdfinfo unavailable (install poppler-utils)")

    ok = (args.floor <= total <= args.limit) and refs == fn_bodies
    print()
    print("VERDICT", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
