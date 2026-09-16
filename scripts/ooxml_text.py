#!/usr/bin/env python3
"""Safely extract prose and logical headings from DOCX OOXML.

DOCX input is untrusted. Parsing uses defusedxml. A logical heading is either a
Heading1--Heading6 paragraph or a numbered paragraph whose text-bearing runs
are all directly bold. The latter covers manuscripts that visually format
headings while leaving their paragraph style as Normal.
"""
from __future__ import annotations

import re
import zipfile
from pathlib import Path
from typing import Iterable

from defusedxml import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
NUMBERED_HEADING = re.compile(r"^\s*(\d+(?:\.\d+){0,5})\s*(?:\t|\u00a0| +)\S")


def _on(node: ET.Element | None) -> bool:
    if node is None:
        return False
    return node.get(W + "val", "true").lower() not in {"0", "false", "off", "no"}


def _paragraph_text(paragraph: ET.Element) -> str:
    parts: list[str] = []
    for node in paragraph.iter():
        if node.tag == W + "t":
            parts.append(node.text or "")
        elif node.tag == W + "tab":
            parts.append("\t")
        elif node.tag in {W + "br", W + "cr"}:
            parts.append("\n")
    return "".join(parts).strip()


def _direct_bold_heading_level(paragraph: ET.Element, text: str) -> int | None:
    match = NUMBERED_HEADING.match(text)
    if not match:
        return None
    text_runs = [
        run
        for run in paragraph.iter(W + "r")
        if any((node.text or "").strip() for node in run.iter(W + "t"))
    ]
    if not text_runs:
        return None
    if not all(_on(run.find(f"./{W}rPr/{W}b")) for run in text_runs):
        return None
    return min(6, match.group(1).count(".") + 1)


def _heading_level(paragraph: ET.Element, text: str) -> int | None:
    style_node = paragraph.find(f"./{W}pPr/{W}pStyle")
    style = style_node.get(W + "val", "") if style_node is not None else ""
    styled = re.fullmatch(r"Heading\s*([1-6])", style, re.I)
    if styled:
        return int(styled.group(1))
    return _direct_bold_heading_level(paragraph, text)


def docx_paragraphs(path: Path, promote_labels: Iterable[str] = ()) -> list[str]:
    """Return DOCX paragraphs, converting logical headings to Markdown.

    A promoted label such as ``Mã nguồn và dữ liệu.`` is split from the
    paragraph body and represented as a level-one heading. This preserves the
    scientific content while giving section-aware gates the intended context.
    """
    with zipfile.ZipFile(path) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    labels = tuple(promote_labels)
    paragraphs: list[str] = []
    for paragraph in root.iter(W + "p"):
        text = _paragraph_text(paragraph)
        if not text:
            continue
        level = _heading_level(paragraph, text)
        if level is not None:
            paragraphs.append("#" * level + " " + text)
            continue
        promoted = next((label for label in labels if text.casefold().startswith(label.casefold())), None)
        if promoted:
            paragraphs.append("# " + promoted.rstrip(". "))
            remainder = text[len(promoted) :].strip()
            if remainder:
                paragraphs.append(remainder)
            continue
        paragraphs.append(text)
    return paragraphs


def read_text(path: Path, promote_labels: Iterable[str] = ()) -> str:
    if path.suffix.lower() == ".docx":
        return "\n\n".join(docx_paragraphs(path, promote_labels))
    return path.read_text(encoding="utf-8")
