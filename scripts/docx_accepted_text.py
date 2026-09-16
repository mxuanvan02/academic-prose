#!/usr/bin/env python3
"""Read a DOCX in *accepted view* and check definition-before-first-use ordering.

Why this exists
---------------
Three DOCX text-extraction traps cost repeated debugging cycles, and all three
are silent — they produce plausible-looking output that fails an assertion much
later:

1. ``python-docx``'s ``paragraph.text`` returns ``''`` for text wrapped in
   ``<w:ins>`` (a tracked insertion). A freshly inserted paragraph therefore
   looks empty in the tracked copy while being correct in the clean copy.
2. A tab is ``<w:tab/>``, a sibling element, not ``<w:t>`` text. Concatenating
   only ``w:t`` nodes turns the heading ``\\t3.7\\tTitle`` into ``3.7Title``, so
   ``startswith('3.7\\t')`` and ``startswith('4\\t')`` both fail.
3. ``document.paragraphs`` skips table cells entirely. Numbers that live in a
   table are invisible to a paragraph-only parity or first-use scan.

``accepted_text`` handles all three: it walks the body in document order,
includes table cells, keeps ``<w:ins>`` content, drops ``<w:del>`` content, and
renders ``<w:tab/>`` as a tab.

Usage
-----
    python docx_accepted_text.py FILE.docx
    python docx_accepted_text.py FILE.docx --define '3.7' --uses 'Acc = ' 'McNemar' 'Jaccard'

Exit codes: 0 ordering holds (or no --define given), 1 a use precedes the
definition, 2 the definition or a use string was not found.
"""
from __future__ import annotations

import argparse
import sys

try:
    from docx import Document
    from docx.oxml.ns import qn
except ImportError:  # pragma: no cover
    sys.exit('python-docx is required: pip install python-docx')

W_P = 'w:p'
W_TBL = 'w:tbl'


def _inside_del(node) -> bool:
    parent = node.getparent()
    while parent is not None:
        if parent.tag == qn('w:del'):
            return True
        parent = parent.getparent()
    return False


def paragraph_text(p_element) -> str:
    """Accepted-view text of one <w:p>: keeps w:ins, drops w:del, renders w:tab."""
    parts = []
    for node in p_element.iter():
        if node.tag == qn('w:t'):
            if not _inside_del(node):
                parts.append(node.text or '')
        elif node.tag == qn('w:tab'):
            if not _inside_del(node):
                parts.append('\t')
        elif node.tag == qn('w:br'):
            if not _inside_del(node):
                parts.append('\n')
    return ''.join(parts)


def accepted_blocks(path: str) -> list[str]:
    """Body blocks in document order. Table rows are flattened to ' | '-joined cells."""
    document = Document(path)
    body = document.element.body
    blocks: list[str] = []
    for child in body.iterchildren():
        if child.tag == qn(W_P):
            blocks.append(paragraph_text(child))
        elif child.tag == qn(W_TBL):
            for tr in child.findall(qn('w:tr')):
                cells = [
                    ''.join(paragraph_text(p) for p in tc.findall(qn('w:p')))
                    for tc in tr.findall(qn('w:tc'))
                ]
                blocks.append(' | '.join(cells))
    return blocks


def first_index(blocks: list[str], needle: str, strip: bool = False) -> int | None:
    for i, block in enumerate(blocks):
        haystack = block.strip() if strip else block
        if strip and haystack.startswith(needle):
            return i
        if not strip and needle in haystack:
            return i
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('docx')
    ap.add_argument('--define', help='heading prefix of the definition block, e.g. "3.7"')
    ap.add_argument('--uses', nargs='*', default=[], help='substrings whose first use must follow --define')
    ap.add_argument('--dump', action='store_true', help='print indexed blocks and exit')
    args = ap.parse_args()

    blocks = accepted_blocks(args.docx)

    if args.dump or not args.define:
        for i, block in enumerate(blocks):
            print(f'{i:4d} | {block[:110]}')
        print(f'\nblocks: {len(blocks)}')
        return 0

    # headings carry a leading numbering tab, so compare against stripped text
    def_idx = first_index(blocks, args.define, strip=True)
    if def_idx is None:
        print(f'NOT FOUND: definition heading {args.define!r}')
        return 2

    failed = False
    print(f'definition {args.define!r} at block {def_idx}')
    for needle in args.uses:
        use_idx = first_index(blocks, needle)
        if use_idx is None:
            print(f'  NOT FOUND: {needle!r}')
            failed = True
            continue
        ok = def_idx < use_idx
        print(f'  {"OK " if ok else "FAIL"} first use of {needle!r} at {use_idx}')
        if not ok:
            failed = True

    if failed:
        print('\nordering violated: a metric is used before it is defined')
        return 1
    print('\nordering holds: every listed use follows the definition block')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
