#!/usr/bin/env python3
"""Build a journal-ready DOCX from Markdown and measure compliance IN THE ARTIFACT.

Why this exists
---------------
Source-format word counts do not match what a venue's Word counter sees. Markdown
overcounts table delimiters (`|`, `|---|`) and footnote markers (`[^n12]`) under a
naive `\\S+` split, and a compliance claim made against the source is therefore not
evidence. Measured divergence in practice: source 9,999 vs built DOCX 10,138.

The venue counts three buckets that must be summed:
  1. body paragraphs from the first numbered section onward
  2. table cell text  -- python-docx paragraph iteration does NOT reach this
  3. footnote bodies  -- these live in word/footnotes.xml, not in document.xml

Usage
-----
    python docx_journal_build.py SOURCE.md OUT.docx [--config cfg.json]

Defaults target a Vietnamese law-journal house style (Times New Roman 13pt,
line spacing 1.5, A4, margins T/B/R 2.0cm + L 2.5cm, page number bottom-centre).
Override any of it with --config; see DEFAULTS below for the schema.

Requires: pandoc on PATH, python-docx. Optional: pdftoppm/libreoffice for PDF.

Pitfalls this script already handles
------------------------------------
* A minimal reference.docx has NO table styles, so `table.style = "Table Grid"`
  raises KeyError. Borders are written as raw tblBorders XML instead.
* Pandoc emits footnotes into word/footnotes.xml; python-docx cannot see them, so
  they are counted by parsing the XML directly.
* Heading levels map to the venue's own convention (1. bold / 1.1. bold-italic /
  1.1.1. italic) rather than to Word's built-in Heading styles.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

try:
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Cm, Pt
except ImportError:  # pragma: no cover
    sys.exit("need python-docx:  pip install python-docx")

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

DEFAULTS = {
    "font": "Times New Roman",
    "size_pt": 13.0,
    "line_spacing": 1.5,
    "page_w_cm": 21.0,
    "page_h_cm": 29.7,
    "margin_top_cm": 2.0,
    "margin_bottom_cm": 2.0,
    "margin_left_cm": 2.5,
    "margin_right_cm": 2.0,
    "page_number": True,
    # compliance targets; set any to null to skip the check
    "body_min": 6000,
    "body_max": 10000,
    "abstract_max": 250,
    "refs_min": 10,
    # body counting starts at the first paragraph matching this pattern
    "body_start_re": r"^\s*1\.\s",
    # bibliography heading, used to count reference entries
    "bib_heading_re": r"(?i)danh\s*m[uụ]c\s*t[aà]i\s*li[eệ]u|references|bibliography",
}


def sh(args: list[str]) -> str:
    """Run argv list without a shell so filenames cannot be reinterpreted."""
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"FAILED {args}\n{r.stderr[:2000]}")
    return r.stdout


# ---------------------------------------------------------------- formatting


def _set_borders(table) -> None:
    """Apply single-line borders via raw XML.

    A minimal reference.docx carries no table styles, so assigning
    table.style = 'Table Grid' raises KeyError: no style with name 'Table Grid'.
    """
    tblPr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "4")
        el.set(qn("w:color"), "000000")
        borders.append(el)
    tblPr.append(borders)


def _add_page_number_footer(section, cfg) -> None:
    p = section.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    run._r.append(fld)
    run.font.name = cfg["font"]
    run.font.size = Pt(cfg["size_pt"])


def _style_heading(par, text: str, cfg) -> bool:
    """Apply venue heading convention. Returns True if the paragraph is a heading.

    1.      -> bold
    1.1.    -> bold italic
    1.1.1.  -> italic
    """
    depth = None
    if re.match(r"^\s*\d+\.\s", text):
        depth = 1
    elif re.match(r"^\s*\d+\.\d+\.\s", text):
        depth = 2
    elif re.match(r"^\s*\d+\.\d+\.\d+\.\s", text):
        depth = 3
    if depth is None:
        return False
    for r in par.runs:
        r.bold = depth in (1, 2)
        r.italic = depth in (2, 3)
    return True


def build(src: Path, dst: Path, cfg: dict) -> Path:
    if not shutil.which("pandoc"):
        raise SystemExit("pandoc not on PATH")
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.parent / "_pandoc_stage.docx"

    # markdown+footnotes is required for [^n1] to become real Word footnotes
    sh(["pandoc", str(src), "-f", "markdown+footnotes", "-t", "docx", "-o", str(tmp)])

    doc = Document(tmp)

    for section in doc.sections:
        section.page_width = Cm(cfg["page_w_cm"])
        section.page_height = Cm(cfg["page_h_cm"])
        section.top_margin = Cm(cfg["margin_top_cm"])
        section.bottom_margin = Cm(cfg["margin_bottom_cm"])
        section.left_margin = Cm(cfg["margin_left_cm"])
        section.right_margin = Cm(cfg["margin_right_cm"])
        if cfg["page_number"]:
            _add_page_number_footer(section, cfg)

    for par in doc.paragraphs:
        par.paragraph_format.line_spacing = cfg["line_spacing"]
        for r in par.runs:
            r.font.name = cfg["font"]
            r.font.size = Pt(cfg["size_pt"])
        _style_heading(par, par.text, cfg)

    for table in doc.tables:
        _set_borders(table)
        for row in table.rows:
            for cell in row.cells:
                for par in cell.paragraphs:
                    par.paragraph_format.line_spacing = cfg["line_spacing"]
                    for r in par.runs:
                        r.font.name = cfg["font"]
                        r.font.size = Pt(cfg["size_pt"])

    doc.save(dst)
    tmp.unlink(missing_ok=True)
    return dst


# ----------------------------------------------------------------- measuring


def _words(text: str) -> int:
    """Count words the way a word processor does: alphanumeric tokens only.

    Deliberately ignores standalone punctuation so table delimiters and stray
    symbols cannot inflate the count.
    """
    return len(re.findall(r"[0-9A-Za-z\u00C0-\u1EF9]+", text))


def _footnote_words(path: Path) -> tuple[int, int]:
    """Return (word count, footnote count) from word/footnotes.xml.

    python-docx cannot reach footnotes, so parse the part directly. Pandoc emits
    two boilerplate separator footnotes with no text; those contribute 0 words
    and are excluded from the count.
    """
    with zipfile.ZipFile(path) as z:
        if "word/footnotes.xml" not in z.namelist():
            return 0, 0
        xml = z.read("word/footnotes.xml").decode("utf-8", "ignore")
    notes = re.findall(r"<w:footnote[ >].*?</w:footnote>", xml, re.S)
    total, real = 0, 0
    for n in notes:
        text = "".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", n, re.S))
        wc = _words(text)
        if wc:
            real += 1
            total += wc
    return total, real


def measure(path: Path, cfg: dict) -> dict:
    doc = Document(path)
    body_start = re.compile(cfg["body_start_re"])
    bib_head = re.compile(cfg["bib_heading_re"])

    main = 0
    started = False
    in_bib = False
    refs = 0
    abstract_caps: list[int] = []

    for par in doc.paragraphs:
        t = par.text.strip()
        if not t:
            continue
        if not started and body_start.match(t):
            started = True
        if bib_head.search(t):
            in_bib = True
            continue
        if started:
            main += _words(t)
            if in_bib and len(t) > 40:
                refs += 1
        else:
            # pre-body region holds title, abstracts, keywords
            if re.match(r"(?i)^\**\s*(t[oó]m t[aắ]t|abstract)", t):
                abstract_caps.append(_words(t))

    tables = 0
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                tables += _words(cell.text)

    fn_words, fn_count = _footnote_words(path)
    sec = doc.sections[0]

    return {
        "main": main,
        "tables": tables,
        "footnotes": fn_words,
        "footnote_count": fn_count,
        "body_total": main + tables + fn_words,
        "abstracts": abstract_caps,
        "refs": refs,
        "page_cm": (round(sec.page_width.cm, 1), round(sec.page_height.cm, 1)),
        "margins_cm": (
            round(sec.top_margin.cm, 2),
            round(sec.bottom_margin.cm, 2),
            round(sec.left_margin.cm, 2),
            round(sec.right_margin.cm, 2),
        ),
    }


def report(m: dict, cfg: dict) -> int:
    def flag(ok: bool | None) -> str:
        return "  " if ok is None else ("OK" if ok else "!!")

    lo, hi = cfg.get("body_min"), cfg.get("body_max")
    body_ok = None if (lo is None or hi is None) else (lo <= m["body_total"] <= hi)
    amax = cfg.get("abstract_max")
    abs_ok = None if amax is None else all(a <= amax for a in m["abstracts"])
    rmin = cfg.get("refs_min")
    refs_ok = None if rmin is None else m["refs"] >= rmin

    print(f"page        {m['page_cm'][0]} x {m['page_cm'][1]} cm")
    print("margins     T{} B{} L{} R{} cm".format(*m["margins_cm"]))
    print(f"{flag(body_ok)} body      {m['body_total']}   [{lo}-{hi}]")
    print(f"     main {m['main']} + tables {m['tables']} + footnotes {m['footnotes']}")
    print(f"   footnotes {m['footnote_count']}")
    print(f"{flag(abs_ok)} abstracts {m['abstracts']}   [<= {amax}]")
    print(f"{flag(refs_ok)} refs      {m['refs']}   [>= {rmin}]")

    fails = [x for x in (body_ok, abs_ok, refs_ok) if x is False]
    return 1 if fails else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("src", type=Path)
    ap.add_argument("dst", type=Path)
    ap.add_argument("--config", type=Path)
    ap.add_argument("--measure-only", action="store_true")
    a = ap.parse_args()

    cfg = dict(DEFAULTS)
    if a.config:
        cfg.update(json.loads(a.config.read_text()))

    out = a.dst if a.measure_only else build(a.src, a.dst, cfg)
    print(f"artifact    {out}  ({out.stat().st_size} bytes)")
    return report(measure(out, cfg), cfg)


if __name__ == "__main__":
    sys.exit(main())
