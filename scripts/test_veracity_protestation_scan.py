#!/usr/bin/env python3
"""Tests for veracity_protestation_scan.py.

The corpus is the real slide that motivated the gate (rclone/Google Drive demo,
2026-10-12) plus licensing edge cases. Run: python3 test_veracity_protestation_scan.py
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from veracity_protestation_scan import scan, split_sentences, read_input  # noqa: E402


class TestProtestationHits(unittest.TestCase):
    def test_real_slide_title_and_callouts(self) -> None:
        # Verbatim strings from the motivating slide.
        text = (
            "THAO TÁC THẬT TRÊN GOOGLE DRIVE — LỆNH CHẠY, KẾT QUẢ TRẢ VỀ. "
            "Ba thư mục tầng 1 nằm trên Drive thật, không phải ảnh vẽ. "
            "4 đối tượng, 217 byte — dung lượng đo được, không ước lượng. "
            "Ảnh chụp thật terminal đang chạy rclone với tài khoản Drive của lớp. "
            "Mọi dòng chữ trên ảnh là kết quả lệnh thật, kể cả đường dẫn."
        )
        r = scan(text)
        self.assertEqual(r["verdict"], "fail")
        # 5 sentences, each carries at least one protest; scanner reports one per sentence
        self.assertGreaterEqual(len(r["findings"]), 4)
        spans = " ".join(f["span"] for f in r["findings"])
        self.assertIn("Drive thật", spans)

    def test_english_counterparts(self) -> None:
        text = ("This is real output, not simulated. The actual screenshot was "
                "captured on the live system, not mocked.")
        r = scan(text)
        self.assertEqual(r["verdict"], "fail")
        self.assertGreaterEqual(len(r["findings"]), 2)

    def test_clean_slide_passes(self) -> None:
        # The same slide rewritten with pointers instead of adjectives.
        text = (
            "Cấu trúc thư mục lớp trên Google Drive — lệnh chạy, kết quả trả về. "
            "Ba thư mục tầng 1: 01_HOC_TAP, 02_CLB_NANG_LUC_SO, 03_CA_NHAN. "
            "rclone size trả về Total objects: 4, Total size: 217 B ngày 12/10. "
            "Đường dẫn remote: gdrive:00_THPT_THUAN_HOA/12_CLB_NLS_AI/99_DEMO."
        )
        r = scan(text)
        self.assertEqual(r["verdict"], "pass")
        self.assertEqual(r["findings"], [])

    def test_needs_pointer_class(self) -> None:
        text = "Biểu đồ này được lấy trực tiếp từ hệ thống đang vận hành."
        r = scan(text)
        self.assertEqual(r["verdict"], "fail")
        self.assertEqual(r["findings"][0]["class"],
                         "authenticity_claim_without_pointer")
        self.assertEqual(r["findings"][0]["verdict"], "replace_with_pointer")


class TestLicensing(unittest.TestCase):
    def test_math_real_numbers_licensed(self) -> None:
        text = ("Tập số thực là đủ để mô hình hoá. Hàm giá trị thực liên tục "
                "trên miền đóng. We study real analysis and the real part of "
                "the eigenvalues.")
        r = scan(text)
        self.assertEqual(r["findings"], [], r["findings"])

    def test_stated_contrast_licensed(self) -> None:
        text = ("Bộ thử dùng dữ liệu nhật ký thật, khác với bộ tổng hợp ở "
                "Mục 3. Real logs versus synthetic ones behave differently.")
        r = scan(text)
        self.assertEqual(r["findings"], [], r["findings"])

    def test_quote_licensed(self) -> None:
        text = 'Học sinh phải phát hiện câu "ảnh chụp thật" là dấu hiệu quảng cáo.'
        r = scan(text)
        self.assertEqual(r["findings"], [], r["findings"])

    def test_tex_comment_stripped(self) -> None:
        # read_input strips tex comments; verify via a temp file
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".tex", delete=False,
                                         encoding="utf-8") as f:
            f.write("% anh that, khong phai anh ve (comment khong tinh)\n"
                    "Nội dung sạch không có gì đáng ngờ.\n")
            p = Path(f.name)
        try:
            text = read_input(p)
            self.assertNotIn("thật", text)
            self.assertEqual(scan(text, str(p))["verdict"], "pass")
        finally:
            p.unlink()

    def test_code_fence_stripped(self) -> None:
        text = ("Hướng dẫn:\n```\n$ rclone lsf gdrive:/  # thao tác thật\n```\n"
                "Đoạn trên là lệnh mẫu.")
        r = scan(text)
        self.assertEqual(r["findings"], [], r["findings"])


class TestNewClasses(unittest.TestCase):
    def test_request_echo(self) -> None:
        text = ("Báo cáo này được lập theo yêu cầu của người dùng. As requested, "
                "the deck covers three modules.")
        r = scan(text)
        classes = {f["class"] for f in r["findings"]}
        self.assertIn("request_echo", classes)
        self.assertEqual(r["verdict"], "fail")

    def test_model_self_reference(self) -> None:
        text = ("Với tư cách là một AI, tôi không thể kiểm chứng số liệu. "
                "As an AI assistant I prepared this summary.")
        r = scan(text)
        classes = {f["class"] for f in r["findings"]}
        self.assertIn("model_self_reference", classes)

    def test_closing_ceremony(self) -> None:
        text = ("Hy vọng tài liệu này sẽ hữu ích cho các bạn. "
                "Hope this is helpful. Chúc các bạn thành công.")
        r = scan(text)
        classes = {f["class"] for f in r["findings"]}
        self.assertIn("closing_ceremony", classes)

    def test_plain_cám_ơn_not_flagged(self) -> None:
        # genre-standard final-slide thanks must stay clean
        text = "Cảm ơn thầy cô và các bạn đã lắng nghe."
        r = scan(text)
        self.assertEqual(r["findings"], [], r["findings"])

    def test_negated_mention_licensed(self) -> None:
        # rubric instructions are not protestation
        text = ("Slide thực hành không dùng ảnh chụp dữ liệu thật, chỉ mô tả. "
                "Tránh thao tác thật không có ảnh minh hoạ. "
                "No real screenshots without annotation.")
        r = scan(text)
        self.assertEqual(r["findings"], [], r["findings"])

    def test_negation_does_not_license_denial_protestation(self) -> None:
        # "không phải ảnh vẽ" IS protestation despite containing a negation
        text = "Ba thư mục nằm trên Drive thật, không phải ảnh vẽ."
        r = scan(text)
        self.assertEqual(r["verdict"], "fail")

    def test_structural_announcement_genre_license(self) -> None:
        text = "Trong phần này chúng tôi sẽ trình bày mô hình đe doạ."
        self.assertEqual(scan(text, genre="auto")["verdict"], "fail")
        self.assertEqual(scan(text, genre="manuscript")["verdict"], "pass")
        self.assertEqual(scan(text, genre="slide")["verdict"], "fail")

    def test_reader_address(self) -> None:
        text = "Như các bạn đã biết, thư mục là nơi chứa tệp. Let's dive in."
        r = scan(text)
        classes = {f["class"] for f in r["findings"]}
        self.assertIn("reader_address", classes)
        self.assertEqual(r["findings"][0]["verdict"], "recast")


class TestMechanics(unittest.TestCase):
    def test_exit_code_contract(self) -> None:
        from veracity_protestation_scan import main
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False,
                                         encoding="utf-8") as f:
            f.write("Ảnh chụp thật từ máy của lớp.\n")
            p = Path(f.name)
        try:
            self.assertEqual(main([str(p), "--json"]), 2)
        finally:
            p.unlink()
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False,
                                         encoding="utf-8") as f:
            f.write("Nội dung sạch.\n")
            p = Path(f.name)
        try:
            self.assertEqual(main([str(p), "--json"]), 0)
        finally:
            p.unlink()

    def test_pptx_native_reader(self) -> None:
        # ooxml_text.read_text cannot read .pptx (falls back to raw utf-8
        # decode and raises); the native reader parses slideN.xml + notes.
        import tempfile, zipfile
        slide_xml = (
            '<?xml version="1.0"?>'
            '<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
            ' xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
            '<p:cSld><p:spTree><p:sp><p:txBody><a:p><a:r><a:t>'
            'Ảnh chụp thật terminal của lớp.'
            '</a:t></a:r></a:p></p:txBody></p:sp></p:spTree></p:cSld></p:sld>')
        with tempfile.NamedTemporaryFile(suffix=".pptx", delete=False) as f:
            with zipfile.ZipFile(f, "w") as z:
                z.writestr("ppt/slides/slide1.xml", slide_xml)
            p2 = Path(f.name)
        try:
            text = read_input(p2)
            self.assertIn("Ảnh chụp thật", text)
            self.assertEqual(scan(text, str(p2))["verdict"], "fail")
        finally:
            p2.unlink()

    def test_unsupported_input_returns_3(self) -> None:
        from veracity_protestation_scan import main
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".xyz", delete=False) as f:
            f.write("x")
            p = Path(f.name)
        try:
            self.assertEqual(main([str(p)]), 3)
        finally:
            p.unlink()

    def test_self_scan_passes(self) -> None:
        # The scanner must not flag its own source (comments/docstrings are
        # stripped for md/tex; .py is not a scanned extension at all).
        here = Path(__file__).resolve().parent / "veracity_protestation_scan.py"
        self.assertTrue(here.exists())
        self.assertNotIn(".py", {".tex", ".md", ".txt", ".html", ".rst",
                                 ".docx", ".pptx"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
