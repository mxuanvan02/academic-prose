#!/usr/bin/env python3
"""Extract author prose from a LaTeX manuscript for the academic-prose scanners.

Why: run on raw `.tex`, `academic_discourse_scan.py` counts preamble lines,
title blocks, and `tabular` rows as sentences and reports `clause_overload`
false positives (measured on an 11-page Vietnamese XeLaTeX build: 7 hits, all markup —
`\\documentclass…\\usepackage` chains, author blocks, table bodies). The other
three scanners can fire on macro names too. This filter produces prose-only
text so scan results are adjudicated on real sentences.

Usage:
    python3 tex_prose_extract.py main.tex -o /tmp/prose.txt
    python3 academic_discourse_scan.py --genre manuscript /tmp/prose.txt --report r.md

What it removes: everything before \\begin{document} / after \\end{document};
table, figure, tabular(x), longtable, center environments; thebibliography
(immutable citation zone); remaining \\commands and math/brace debris.
\\caption{...} text is harvested before floats are dropped and re-appended as
standalone paragraphs (captions are author prose). itemize/enumerate and
abstract environments are kept.

Known loss: braced arguments of inline commands (\\section{Title},
\\textbf{x}) are dropped with the command; scanners exclude headings anyway.
A raw-`.tex` hit that quotes markup is recorded as a false positive and
adjudicated away — never auto-rewrite markup to satisfy a scanner.
"""
import argparse
import re
import sys


def extract_prose(tex: str, keep_captions: bool = True) -> str:
    m = re.search(r"\\begin\{document\}(.*)\\end\{document\}", tex, re.S)
    body = m.group(1) if m else tex

    captions = []
    if keep_captions:
        captions = re.findall(r"\\caption\{((?:[^{}]|\{[^{}]*\})*)\}", body)

    for env in ("table", "table*", "figure", "figure*", "tabular", "tabularx",
                "longtable", "center", "thebibliography"):
        body = re.sub(
            r"\\begin\{" + re.escape(env) + r"\}.*?\\end\{" + re.escape(env) + r"\}",
            " ", body, flags=re.S)

    # drop commands (and their optional/simple-brace args); keep surrounding prose
    body = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?(\{[^{}]*\})?", " ", body)
    body = body.replace("\\\\", "\n")
    body = re.sub(r"[{}$~%&]", " ", body)

    parts = [body]
    for cap in captions:
        cap = re.sub(r"\\[a-zA-Z]+\*?(\{[^{}]*\})?", " ", cap)
        cap = re.sub(r"[{}$~%&]", " ", cap)
        if cap.strip():
            parts.append(cap.strip())

    text = "\n\n".join(parts)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return text.strip()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("input", help="LaTeX source file")
    ap.add_argument("-o", "--output", help="write prose here (default: stdout)")
    ap.add_argument("--no-captions", action="store_true",
                    help="drop float captions instead of re-appending them")
    args = ap.parse_args()

    with open(args.input, encoding="utf-8") as fh:
        tex = fh.read()
    prose = extract_prose(tex, keep_captions=not args.no_captions)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(prose + "\n")
        print(f"wrote {len(prose.split())} words to {args.output}")
    else:
        sys.stdout.write(prose + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
