#!/usr/bin/env python3
"""Regression tests for safe DOCX text and logical-heading extraction."""
from __future__ import annotations

import tempfile
import unittest
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

from ooxml_text import docx_paragraphs, read_text

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def minimal_docx(
    path: Path,
    paragraphs: list[tuple[str, str | None, bool]],
) -> None:
    body: list[str] = []
    for text, style, bold in paragraphs:
        ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
        rpr = "<w:rPr><w:b/></w:rPr>" if bold else ""
        body.append(
            f'<w:p>{ppr}<w:r>{rpr}<w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>'
        )
    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<w:document xmlns:w="{W}"><w:body>{"".join(body)}</w:body></w:document>'
    )
    content_types = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="xml" ContentType="application/xml"/>'
        "</Types>"
    )
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("[Content_Types].xml", content_types)
        archive.writestr("word/document.xml", document)


class TestLogicalHeadings(unittest.TestCase):
    def test_heading_style_is_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.docx"
            minimal_docx(path, [("Hạn chế", "Heading2", False)])
            paragraphs = docx_paragraphs(path)
        self.assertEqual(paragraphs, ["## Hạn chế"])

    def test_directly_bold_numbered_heading_is_promoted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.docx"
            minimal_docx(
                path,
                [
                    ("4.3\tHạn chế", None, True),
                    ("Nhãn Bloom được gán tự động.", None, False),
                ],
            )
            paragraphs = docx_paragraphs(path)
        self.assertEqual(paragraphs[0], "## 4.3\tHạn chế")
        self.assertEqual(paragraphs[1], "Nhãn Bloom được gán tự động.")

    def test_unbold_numbered_body_is_not_promoted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.docx"
            minimal_docx(path, [("2026 kết quả được ghi nhận.", None, False)])
            paragraphs = docx_paragraphs(path)
        self.assertEqual(paragraphs, ["2026 kết quả được ghi nhận."])

    def test_data_and_code_label_can_supply_section_context(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.docx"
            minimal_docx(
                path,
                [
                    (
                        "Mã nguồn và dữ liệu. Mã nguồn tại https://github.com/example/legalqa "
                        "được cố định ở commit abc1234.",
                        None,
                        False,
                    )
                ],
            )
            text = read_text(path, promote_labels=("Mã nguồn và dữ liệu.",))
        self.assertIn("# Mã nguồn và dữ liệu", text)
        self.assertIn("commit abc1234", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
