#!/usr/bin/env python3
"""Read a DOCX back in its *accepted* view and verify a revision delivery.

Why this exists
---------------
Four python-docx behaviours make a correct tracked-changes document look broken:

1. ``Paragraph.text`` / ``_Cell.text`` build from *direct* ``w:r`` children, so any
   run wrapped in ``<w:ins>`` is invisible. A tracked copy then fails the exact
   assertion its clean twin passes.
2. ``document.paragraphs`` skips tables, so any number/verdict living in a table
   disappears from word counts and bilingual parity checks.
3. Table indices shift when a table is inserted, so positional assertions rot.
4. Asserting against raw ``word/document.xml`` cannot distinguish accepted text
   from superseded text, because deleted prose legitimately survives in ``w:del``.

This module walks the body in document order, keeps ``w:ins`` content, drops
``w:del`` content, and includes table cells.

Usage
-----
    # dump the accepted text
    python docx_accepted_view.py FILE.docx

    # full delivery gate
    python docx_accepted_view.py FILE.docx \
        --require "no N/A in any run" --require "Table 3" \
        --forbid "must be completed before submission" \
        --expect-tracked            # or --expect-clean
        --parity-split "PHẦN B"     # EN/VI numeric parity around this marker

Exit 0 = every check passed. Exit 1 = a check failed (reason on stderr).
Requires: python-docx. Uses defusedxml for the raw-XML read when available.
"""
from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn

W_P = qn('w:p')
W_TBL = qn('w:tbl')
W_T = qn('w:t')
W_DEL = qn('w:del')
W_TR = qn('w:tr')
W_TC = qn('w:tc')


# --------------------------------------------------------------- accepted view
def accepted_element_text(element) -> str:
    """Text of an element in the accepted view.

    Keeps ``w:ins`` content (an insertion is accepted text) and drops anything
    with a ``w:del`` ancestor (a deletion is not). ``w:delText`` nodes are
    ignored outright since only ``w:t`` is collected.
    """
    parts = []
    for node in element.iter():
        if node.tag != W_T:
            continue
        parent = node.getparent()
        inside_del = False
        while parent is not None:
            if parent.tag == W_DEL:
                inside_del = True
                break
            parent = parent.getparent()
        if not inside_del:
            parts.append(node.text or '')
    return ''.join(parts)


def body_blocks(document):
    """Yield ('p'|'tbl', element) for every top-level body block, in order."""
    for child in document.element.body:
        if child.tag == W_P:
            yield 'p', child
        elif child.tag == W_TBL:
            yield 'tbl', child


def table_rows(tbl) -> list[list[str]]:
    return [
        [accepted_element_text(tc) for tc in tr.findall(W_TC)]
        for tr in tbl.findall(W_TR)
    ]


def accepted_text(path: Path) -> str:
    """Full accepted text, in document order, INCLUDING table cell text."""
    document = Document(str(path))
    chunks = []
    for kind, element in body_blocks(document):
        if kind == 'p':
            chunks.append(accepted_element_text(element))
        else:
            for row in table_rows(element):
                chunks.append('\t'.join(row))
    return '\n'.join(chunks)


def find_table_by_header(path: Path, header_cell: str):
    """Locate a table by its first header cell instead of by index.

    Table indices shift whenever a table is inserted; header text does not.
    Returns (index, rows) or (None, None).
    """
    document = Document(str(path))
    index = 0
    for kind, element in body_blocks(document):
        if kind != 'tbl':
            continue
        rows = table_rows(element)
        if rows and rows[0] and rows[0][0].strip() == header_cell.strip():
            return index, rows
        index += 1
    return None, None


# ------------------------------------------------------------- revision markup
def revision_markup(path: Path) -> dict:
    with zipfile.ZipFile(path) as archive:
        assert archive.testzip() is None, 'corrupt ZIP container'
        names = archive.namelist()
        for part in ('word/document.xml', 'word/settings.xml', '[Content_Types].xml'):
            if part not in names:
                raise AssertionError(f'missing OOXML part: {part}')
        xml = archive.read('word/document.xml').decode('utf-8')
        settings = archive.read('word/settings.xml').decode('utf-8')
    return {
        'insertions': xml.count('<w:ins '),
        'deletions': xml.count('<w:del '),
        'track_revisions': 'trackRevisions' in settings,
    }


# ---------------------------------------------------------------- number parity
def numbers(text: str) -> set[str]:
    """Numeric tokens with decimal separators folded so EN 0.47 == VI 0,47.

    Also folds thousands separators (1.163 / 1,163 -> 1163) so the two language
    conventions compare equal. DOIs keep their dots and are excluded by the
    caller if needed.
    """
    folded = re.sub(r'(\d)[.,](\d{3})\b', r'\1\2', text)
    folded = re.sub(r'(\d),(\d)', r'\1.\2', folded)
    return set(re.findall(r'\d+(?:\.\d+)?', folded))


def parity_report(text: str, marker: str) -> dict:
    if marker not in text:
        raise AssertionError(f'parity marker not found: {marker!r}')
    first, second = text.split(marker, 1)
    a, b = numbers(first), numbers(second)
    return {
        'first_only': sorted(a - b),
        'second_only': sorted(b - a),
        'words_first': len(first.split()),
        'words_second': len(second.split()),
    }


# ------------------------------------------------------------------------ main
def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('docx', type=Path)
    parser.add_argument('--require', action='append', default=[],
                        help='string that MUST appear in the accepted view')
    parser.add_argument('--forbid', action='append', default=[],
                        help='string that must NOT appear in the accepted view')
    parser.add_argument('--expect-clean', action='store_true',
                        help='assert no w:ins / w:del anywhere')
    parser.add_argument('--expect-tracked', action='store_true',
                        help='assert w:ins, w:del and trackRevisions all present')
    parser.add_argument('--table-header', default=None,
                        help='locate a table by its first header cell and print its rows')
    parser.add_argument('--parity-split', default=None,
                        help='marker splitting two language halves for numeric parity')
    parser.add_argument('--dump', action='store_true', help='print the accepted text')
    args = parser.parse_args(argv)

    if not args.docx.exists():
        print(f'FAIL: no such file: {args.docx}', file=sys.stderr)
        return 1

    text = accepted_text(args.docx)
    markup = revision_markup(args.docx)
    failures = []

    for needle in args.require:
        if needle not in text:
            failures.append(f'required string absent from accepted view: {needle!r}')
    for needle in args.forbid:
        if needle in text:
            failures.append(f'forbidden string present in accepted view: {needle!r}')

    if args.expect_clean:
        if markup['insertions'] or markup['deletions']:
            failures.append('clean copy carries revision markup '
                            f'({markup["insertions"]} ins, {markup["deletions"]} del)')
    if args.expect_tracked:
        if not markup['insertions']:
            failures.append('tracked copy has no insertions')
        if not markup['deletions']:
            failures.append('tracked copy has no deletions')
        if not markup['track_revisions']:
            failures.append('tracked copy does not enable w:trackRevisions')

    if args.table_header:
        index, rows = find_table_by_header(args.docx, args.table_header)
        if rows is None:
            failures.append(f'no table whose first header cell is {args.table_header!r}')
        else:
            print(f'table index {index} (positional index is NOT stable across inserts)')
            for row in rows:
                print(' | '.join(row))

    if args.parity_split:
        try:
            report = parity_report(text, args.parity_split)
        except AssertionError as exc:
            failures.append(str(exc))
        else:
            print(f'words: {report["words_first"]} / {report["words_second"]}')
            if report['first_only'] or report['second_only']:
                failures.append(
                    'numeric parity broken between language halves: '
                    f'first-only={report["first_only"]} second-only={report["second_only"]}')

    if args.dump:
        print(text)

    print(f'markup: {markup}')
    if failures:
        for failure in failures:
            print(f'FAIL: {failure}', file=sys.stderr)
        return 1
    print('OK: all accepted-view checks passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
