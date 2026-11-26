#!/usr/bin/env python3
"""Regression tests for the paragraph-level academic-discourse gate."""
from __future__ import annotations

import tempfile
import unittest
import zipfile
from pathlib import Path

from academic_discourse_scan import read_paragraphs, scan, scan_paragraphs

FIXTURES = Path(__file__).resolve().parent / "fixtures"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def read(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def classes(result: dict) -> set[str]:
    return {finding["class"] for finding in result["findings"]}


def minimal_docx(path: Path, paragraphs: list[tuple[str, str | None]]) -> None:
    body: list[str] = []
    for text, style in paragraphs:
        ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
        body.append(
            f'<w:p>{ppr}<w:r><w:t xml:space="preserve">{text}</w:t></w:r></w:p>'
        )
    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<w:document xmlns:w="{W}"><w:body>{"".join(body)}</w:body></w:document>'
    )
    content_types = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '</Types>'
    )
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("[Content_Types].xml", content_types)
        archive.writestr("word/document.xml", document)


class TestDirtyFixtures(unittest.TestCase):
    EXPECTED = {
        "deficit_centered_paragraph",
        "caveat_saturation",
        "research_agenda_as_task_list",
        "clause_overload",
    }

    def test_dirty_vietnamese_exercises_all_classes(self) -> None:
        result = scan(read("academic_discourse_dirty.md"))
        self.assertEqual(classes(result), self.EXPECTED)
        self.assertEqual(result["exit_code"], 2)

    def test_dirty_english_exercises_all_classes(self) -> None:
        result = scan(read("academic_discourse_dirty_en.md"))
        self.assertEqual(classes(result), self.EXPECTED)
        self.assertEqual(result["exit_code"], 2)


class TestCleanFixtures(unittest.TestCase):
    def test_clean_vietnamese_is_silent(self) -> None:
        result = scan(read("academic_discourse_clean.md"))
        self.assertEqual(result["findings"], [])
        self.assertEqual(result["exit_code"], 0)

    def test_clean_english_is_silent(self) -> None:
        result = scan(read("academic_discourse_clean_en.md"))
        self.assertEqual(result["findings"], [])
        self.assertEqual(result["exit_code"], 0)

    def test_one_real_limitation_is_not_a_stack(self) -> None:
        text = (
            "# Hạn chế\n\nNhãn Bloom được gán tự động, nên phân tích theo bậc nhận thức "
            "không ước lượng độ tin cậy phân loại."
        )
        self.assertEqual(scan(text)["findings"], [])

    def test_long_simple_sentence_is_not_clause_overload(self) -> None:
        text = " ".join(["Dữ liệu gồm các bản ghi pháp luật tiếng Việt"] * 10) + "."
        self.assertNotIn("clause_overload", classes(scan(text)))


class TestDocxInput(unittest.TestCase):
    def test_docx_heading_and_paragraph_are_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.docx"
            minimal_docx(
                path,
                [
                    ("Hạn chế", "Heading1"),
                    (
                        "Nhãn chưa được thẩm định và độ tin cậy chưa được định lượng. "
                        "Dữ liệu chưa được kiểm tra gần trùng, nên kết quả không chứng minh "
                        "tính hợp lệ của nhãn.",
                        None,
                    ),
                ],
            )
            paragraphs = read_paragraphs(path)
        self.assertEqual(paragraphs[0], "# Hạn chế")
        result = scan_paragraphs(paragraphs)
        self.assertIn("deficit_centered_paragraph", classes(result))
        finding = next(f for f in result["findings"] if f["class"] == "deficit_centered_paragraph")
        self.assertEqual(finding["heading"], "Hạn chế")


class TestContract(unittest.TestCase):
    def test_clean_scan_still_requires_manual_review(self) -> None:
        result = scan(read("academic_discourse_clean.md"))
        self.assertTrue(result["manual_pass_required"])
        self.assertIn("partial verification", result["note"])

    def test_empty_input_is_clean(self) -> None:
        result = scan("")
        self.assertEqual(result["exit_code"], 0)
        self.assertEqual(result["paragraphs"], 0)


class TestOpeningFrontLoading(unittest.TestCase):
    def test_dirty_english_intro_notation_triggers(self) -> None:
        text = (
            "# Introduction\n\n"
            "Our method maps $X_i(t)$ to $(\\mu_i(t), \\sigma_i^2(t))$ under budget $B_1$ and $B_2$, "
            "proving $O(1/\\sqrt{N})$ convergence and $R(\\pi, N) \\le R_{\\mathrm{LP}}$ across runs."
        )
        res = scan(text, genre="manuscript")
        self.assertIn("opening_front_loading", classes(res))
        self.assertEqual(res["exit_code"], 2)

    def test_dirty_vietnamese_contributions_telemetry_triggers(self) -> None:
        text = (
            "# Đóng góp chính\n\n"
            "Thuật toán giảm 79.8% sai số và 87.8% tổn thất với N=30, p=0.466, chi phí 0.23 ms/khe, "
            "nhanh hơn 184x và thu hẹp độ lệch 12.75%→1.39%."
        )
        res = scan(text, genre="manuscript")
        self.assertIn("opening_front_loading", classes(res))
        self.assertEqual(res["exit_code"], 2)

    def test_clean_concise_abstract_stays_silent(self) -> None:
        text = (
            "# Abstract\n\n"
            "This study proposes a two-stage scheduling index that prioritizes threshold exits under "
            "burst-loss channels and proves worst-case fairness bounds. On held-out multi-site traces, "
            "the approach reduces missed excursions by 79.8% at real-time gateway speed, though gains "
            "narrow on quiescent intervals without recalibration."
        )
        res = scan(text, genre="abstract")
        self.assertEqual(res["findings"], [])
        self.assertEqual(res["exit_code"], 0)

    def test_technical_body_section_heavy_math_stays_silent(self) -> None:
        text = (
            "# Methods and Results\n\n"
            "Given $X_i(t)$ and $(\\mu_i(t), \\sigma_i^2(t))$ with $B_1=4$ and $B_2=4$, the rule "
            "achieves $O(\\log m)$ complexity, reduces loss by 79.8% and 87.8% at N=30, p=0.0012, "
            "0.23 ms runtime, 184x speedup, and 12.75%→1.39% gap convergence."
        )
        res = scan(text, genre="manuscript")
        self.assertNotIn("opening_front_loading", classes(res))


if __name__ == "__main__":
    unittest.main(verbosity=2)
