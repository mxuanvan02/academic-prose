#!/usr/bin/env python3
"""Public-hygiene gate for one tool directory in this repository.

Ships byte-identically in every tool that CI validates; TOOL_DIR is derived from __file__, so the
same text works wherever it is copied. Keep the copies identical -- a tool whose gate drifted is a
tool whose PASS means something different from its neighbour's.

Scans every text file in the tool directory for tokens that must never appear
in the public repo: personal identifiers, internal host paths, codenames of
UNPUBLISHED papers, institution names, secret-shaped strings, leftover
sanitizer placeholders.

Forbidden patterns are assembled by concatenation so this script does not
flag itself.

Matching runs on whitespace-normalised text, so a forbidden token split across a line break is
still caught; offsets are mapped back to the original file for the reported context and for the
allowlist's same-line check.

Exit 0 = clean, exit 1 = findings printed.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

TOOL_DIR = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()

# Any separator, or none. A token whose canonical form carries a hyphen also appears
# with an en dash, an em dash, an underscore, or nothing between the halves: measured,
# 15 of the 69 identifier occurrences in one tool used U+2013 EN DASH and were invisible
# to a pattern built from the hyphen. Whitespace is in the class because normalise()
# turns a line break between the halves into a single space. Written with \uXXXX escapes
# so this file stays ASCII in the pattern definitions.
SEP = r"[-\u2010-\u2015_\s]*"


def joined(*parts: str, flags: int = re.I) -> "re.Pattern[str]":
    """Compile the parts with SEP allowed between each pair."""
    return re.compile(SEP.join(re.escape(p) for p in parts), flags)


# Per-token boundary policy. One global rule is measurably wrong in both directions:
#
#   \b alone            misses `_STAIS_clean`, `rabs_summary.csv`, `logoDHH`, `HOEITBlue`
#                       because '_' and adjacent letters are word characters
#   letter-boundary     catches those, but MISSES `logoDHH`, `TMDHH`, `DHH2026`,
#                       `HOEITBlue` -- a letter is adjacent
#   plain substring     catches everything, but `grabs`, `crabs`, `drabs`, `arabs` and
#                       `subrabs` all CONTAIN a codename, so an ordinary English word
#                       would fail the gate forever
#
# So each token takes the form its own collision risk allows:
#   joined(...)                 hyphenated/multi-word identifiers no ordinary word contains
#   LETTER_BOUNDARY             short ASCII tokens that occur inside ordinary words
#   case-SENSITIVE substring    short UPPERCASE abbreviations whose real leaks are glued
#                               to other letters; case-insensitive here would flag prose
LETTER_BOUNDARY = r"(?<![A-Za-z]){}(?![A-Za-z])"

# LETTER_BOUNDARY is not enough for a Vietnamese token, because it only guards ASCII
# letters and '\b' stops at any non-word byte. Measured: `anh\s+văn` matched INSIDE the
# ordinary legal term `định dANH VĂN bản quy phạm` (identify the governing document),
# so a reference file quoting that term failed the gate forever. This class covers
# precomposed Latin letters with diacritics, which is what Vietnamese prose uses.
VN_LETTER = r"A-Za-z\u00C0-\u1EFF"
VN_BOUNDARY = rf"(?<![{VN_LETTER}]){{}}(?![{VN_LETTER}])"

FORBIDDEN: list[tuple[str, re.Pattern[str]]] = [
    # personal identifiers. The vocative takes VN_BOUNDARY so a word ending in
    # "-anh văn" cannot match; `môn anh văn` (the English subject) still does, which is
    # the accepted cost of guarding a two-word lowercase token.
    ("personal-name", re.compile(
        VN_BOUNDARY.format(r"anh\s+văn") + r"|người dùng Van\b|\bVan's\b", re.I)),
    ("host-username", re.compile("hito" + "kiri")),
    ("old-skill-name", re.compile("anh-van-" + r"research-workflow")),
    # internal paths / storage
    # EVERY concatenated half must be a raw string. A plain "BS\b" is the backspace
    # character 0x08, not a word boundary, so the pattern silently never matches --
    # measured: five of these were dead and the gate printed PASS on real leaks.
    ("internal-path", re.compile(r"/media/" + r"SAS|/home/van\b|/Users/van\b")),
    # UNPUBLISHED project/paper codenames (must stay genericized)
    ("codename-1", joined("CAW", "VoU")),
    ("codename-2", re.compile(LETTER_BOUNDARY.format(re.escape("RA" + "BS")), re.I)),
    # codename-3 WAS exempt from separator flexibility, and the reason it no longer is
    # matters more than the pattern. Its approved descriptor used to be the same string
    # as the codename modulo case and separator, so a separator-flexible pattern flagged
    # 36 occurrences of legitimate prose -- measured. No boundary or case rule can
    # separate two strings that differ only by case and separator, so the descriptor was
    # renamed (to the wording the project's own reference file already used for it) and
    # only then was this pattern strengthened. Order is the lesson: renaming a descriptor
    # is a one-time cost, accepting false positives is permanent, and weakening a pattern
    # to dodge them teaches the next person that the gate negotiates.
    #
    # It is the ONE joined token that needs a letter boundary, for the opposite reason
    # from the others: `Probe` and `Transmit` are both common English words and this
    # project's domain is IoT sensing, so a bare SEP-joined form (correct for
    # codename-1/-4/-6, whose tokens are not English words) flagged "probe transmitter",
    # "probe transmits", "probe transmitted", "probe transmitting" and "subprobe" -- 5
    # false positives, measured. The boundary at the end rejects the inflected and
    # compound forms; at the start it rejects "subprobe".
    ("codename-3", re.compile(
        LETTER_BOUNDARY.format(SEP.join([re.escape("Probe"), re.escape("Transmit")])),
        re.I)),
    ("codename-4", joined("ECM", "TQAG")),
    ("codename-5", re.compile(LETTER_BOUNDARY.format(re.escape("ST" + "AIS")), re.I)),
    ("codename-6", joined("Mekong", "Trace")),
    ("codename-7", re.compile(
        SEP.join([re.escape("HOEIT"), re.escape("LegalQA")]) + "|" +
        SEP.join([re.escape("VDTM"), re.escape("LegalQA")]), re.I)),
    # institution identifiers. The two short uppercase abbreviations below are
    # deliberately case-SENSITIVE substrings: their real leaks are glued to other
    # letters (a LaTeX logo macro, a grant-code prefix, a colour macro name), so any
    # boundary assertion misses them, while case-insensitive matching would flag
    # ordinary prose containing those three letters. The narrow allowlist below is the
    # escape hatch if a legitimate uppercase form ever needs to ship.
    ("institution-1", re.compile(r"ĐH" + r"SP|ĐHSP", re.I)),
    ("institution-2", re.compile(
        SEP.join([re.escape("ĐH"), re.escape("Huế")]) + "|" +
        SEP.join([re.escape("Đại học"), re.escape("Huế")]), re.I)),
    ("institution-3", joined("Hue", "University")),
    ("institution-4", re.compile("DH" + "H")),
    ("institution-5", re.compile("HO" + "EIT")),
    ("institution-6", joined("Thu", "Dau", "Mot")),
    # institution and venue DOMAINS. A hostname identifies an employer or a
    # submission target as precisely as its name does, and it survives every
    # rewrite of the prose around it, so a name-only pattern list leaves the
    # strongest identifier uncovered. Measured: six occurrences across two tools
    # shipped while every gate printed PASS, because no pattern matched a domain.
    # Both halves raw -- see the note above internal-path.
    ("institution-7", re.compile(r"dhsphue" + r"\.edu\.vn")),
    ("venue-1", re.compile(r"(?:jos\.)?hueuni" + r"\.edu\.vn")),
    # secret shapes
    ("secret-token", re.compile(r"gh[oprsu]_[A-Za-z0-9]{10,}|sk-[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16}")),
    ("secret-key", re.compile("BEGIN [A-Z ]*PRIVATE KEY")),
    # sanitizer leftovers
    ("placeholder", re.compile(r"\x00")),
]


# Narrow allowlist for scholarly citations. A public institution named as the AUTHORITY for a
# measured convention is evidence a reader can go and check, not identity leakage -- the same
# distinction that lets a rights notice name its copyright holder. Each entry pins the file, the
# exact matched literal, and a context substring that must appear on the same line, so the
# allowance dies the moment the citation framing is removed or the name is reused anywhere else.
# Literals are assembled by concatenation for the same reason FORBIDDEN patterns are: this file
# sits inside a scanned tool directory in every copy and must not flag itself.
ALLOWED_CITATIONS: list[tuple[str, str, str, str]] = [
    # Decision 1418/QD-DHSP is the authority for the decimal-point convention documented here;
    # the surrounding lines argue FROM it, they do not name an employer.
    ("references/academic-vietnamese-standard.md", "institution-1", "ĐH" + "SP", "Decision 1418"),
    # Same sentence, second institution pattern: the English name wraps across the line break,
    # which is exactly the case normalised matching was added to see.
    ("references/academic-vietnamese-standard.md", "institution-3",
     "Hue " + "University", "Decision 1418"),
    # The journal and its faculty are the source of the word-limit rule quoted verbatim below it.
    ("references/word-budget-and-rendered-artifact-compliance.md", "institution-2",
     "Đại học " + "Huế", "Tạp chí"),
]


def normalise(text: str) -> tuple[str, list[int]]:
    """Collapse each whitespace run to one space; return it plus norm-index -> original-index.

    Collapsing to a single space cannot invent a match for the secret-shaped patterns, because a
    space breaks every character class they use. It can only reveal matches that a line break was
    hiding, which is the point.
    """
    out: list[str] = []
    mp: list[int] = []
    i, n = 0, len(text)
    while i < n:
        if text[i].isspace():
            j = i
            while j < n and text[j].isspace():
                j += 1
            out.append(" ")
            mp.append(j - 1)
            i = j
        else:
            out.append(text[i])
            mp.append(i)
            i += 1
    return "".join(out), mp


def allowed(label: str, rel: str, text: str, mp: list[int], m: "re.Match[str]") -> bool:
    """True only when file, matched literal AND same-line citation context all agree.

    The context line is taken from the ORIGINAL text, not the normalised copy: after normalisation
    a whole file is one line, so a "same line" test there silently degrades into a "same file"
    test and the allowlist becomes far wider than the three citations it was written for.
    """
    a = mp[m.start()]
    b = mp[m.end() - 1] + 1
    line_start = text.rfind("\n", 0, a) + 1
    line_end = text.find("\n", b)
    line = text[line_start:line_end if line_end > 0 else len(text)]
    for a_rel, a_label, a_literal, a_ctx in ALLOWED_CITATIONS:
        if a_rel == rel and a_label == label and m.group(0) == a_literal and a_ctx in line:
            return True
    return False


def main() -> int:
    findings: list[str] = []
    n_files = 0
    for path in sorted(TOOL_DIR.rglob("*")):
        if not path.is_file() or path.resolve() == SELF:
            continue
        # Byte-code caches are gitignored, so they can never be a committed binary -- but they are
        # undecodable, and the validation block in README.md runs test suites before this gate, so
        # a second run used to fail on litter the first run created. Skipping them cannot hide a
        # real binary; that check still applies to every other file.
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(f"binary-file\t{path.relative_to(TOOL_DIR)}")
            continue
        n_files += 1
        rel = path.relative_to(TOOL_DIR).as_posix()
        norm, mp = normalise(text)
        for label, pat in FORBIDDEN:
            for m in pat.finditer(norm):
                if allowed(label, rel, text, mp, m):
                    continue
                a = mp[m.start()]
                b = mp[m.end() - 1] + 1
                ctx = text[max(0, a - 40):b + 40].replace("\n", " ")
                findings.append(f"{label}\t{rel}\t…{ctx}…")

    print(f"scanned {n_files} files under {TOOL_DIR}")
    if findings:
        print(f"FAIL: {len(findings)} finding(s)")
        for f in findings[:40]:
            print(" ", f[:180])
        if len(findings) > 40:
            print(f"  … and {len(findings) - 40} more")
        return 1
    print("PASS: no forbidden tokens found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
