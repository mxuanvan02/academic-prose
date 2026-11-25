#!/usr/bin/env python3
"""Tests for the unified automatic Writing gate runner (5-scanner orchestrator)."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from run_writing_gates import detect_language, main, scan_paths, scan_text  # noqa: E402

FIXTURES = _SCRIPTS_DIR / "fixtures"


class TestLanguageAndCleanRuns(unittest.TestCase):
    def test_auto_language_detection(self) -> None:
        self.assertEqual(detect_language("Nghiên cứu phân tích tác động của chính sách thuế."), "vi")
        self.assertEqual(detect_language("The experiment measured thermal conductivity across five samples."), "en")

    def test_clean_fixtures_pass_all_five_scanners(self) -> None:
        res = scan_paths([FIXTURES / "vi_ai_pattern_clean.md", FIXTURES / "internal_register_clean_en.md"])
        self.assertEqual(res["exit_code"], 0)
        self.assertEqual(res["summary"]["gate"], "scan_clean")
        self.assertEqual(res["summary"]["total_files"], 2)
        self.assertEqual(res["summary"]["blocking_findings"], 0)
        self.assertEqual(res["summary"]["revision_findings"], 0)
        self.assertEqual(
            set(res["files"][0]["scanners"].keys()),
            {"internal_register", "process_logic", "ai_pattern", "academic_discourse", "veracity_protestation"},
        )
        self.assertTrue(res["manual_pass_required"])
        self.assertGreaterEqual(len(res["manual_pass_checklist"]), 5)


class TestBlockingAndRevisionExitCodes(unittest.TestCase):
    def test_blocking_internal_register_returns_exit_1(self) -> None:
        text = "Theo yêu cầu của anh, bản thảo đã sửa phần kết luận để nộp tạp chí Q1."
        res = scan_text(text, genre="manuscript")
        self.assertEqual(res["gate"], "block")
        self.assertIn("assistant_residue", res["blocking_classes"])
        self.assertIn("venue_ambition_leak", res["blocking_classes"])

        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "draft.md"
            p.write_text(text, encoding="utf-8")
            agg = scan_paths([p], genre="manuscript")
            self.assertEqual(agg["exit_code"], 1)
            self.assertEqual(agg["summary"]["gate"], "block")

    def test_revision_level_calque_returns_exit_2(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "draft.md"
            p.write_text(
                "Dưới các giả định tuyến tính, ước lượng cho thấy sự gia tăng của việc tiêu thụ điện năng.",
                encoding="utf-8",
            )
            agg = scan_paths([p], genre="manuscript")
            self.assertEqual(agg["exit_code"], 2)
            self.assertEqual(agg["summary"]["gate"], "revise")
            self.assertEqual(agg["summary"]["blocking_findings"], 0)
            self.assertGreater(agg["summary"]["revision_findings"], 0)

    def test_veracity_and_discourse_scanners_contribute_to_revision_exit_2(self) -> None:
        ver_res = scan_text("Đây là ảnh chụp thật từ hệ thống trong phòng thí nghiệm.", genre="slides")
        self.assertEqual(ver_res["gate"], "revise")
        self.assertGreater(len(ver_res["scanners"]["veracity_protestation"]["findings"]), 0)

        disc_res = scan_paths([FIXTURES / "academic_discourse_dirty.md"], genre="manuscript")
        self.assertEqual(disc_res["exit_code"], 2)
        self.assertGreater(
            len(disc_res["files"][0]["scanners"]["academic_discourse"]["findings"]),
            0,
        )


class TestGenreLicensingTexExtractionAndSweep(unittest.TestCase):
    def test_genre_licensing_routes_across_scanners(self) -> None:
        cover_res = scan_paths([FIXTURES / "internal_register_cover_letter.md"], genre="cover_letter")
        self.assertEqual(cover_res["exit_code"], 0)

        as_manuscript = scan_paths([FIXTURES / "internal_register_cover_letter.md"], genre="manuscript")
        self.assertEqual(as_manuscript["exit_code"], 1)

        ack_res = scan_paths([FIXTURES / "vi_ai_pattern_acknowledgement.md"], genre="acknowledgement")
        self.assertEqual(ack_res["exit_code"], 0)

    def test_latex_extraction_prevents_false_clause_overload_on_preamble(self) -> None:
        tex = (
            "\\documentclass{article}\n"
            "\\usepackage{amsmath,amssymb,booktabs,geometry,hyperref,xcolor,graphicx,listings}\n"
            "\\begin{document}\n"
            "Mẫu mô được quan sát dưới kính hiển vi điện tử ở độ phóng đại 400 lần.\n"
            "\\end{document}\n"
        )
        res = scan_text(tex, genre="manuscript", source="paper.tex")
        self.assertEqual(res["gate"], "scan_clean")
        self.assertEqual(res["scanners"]["academic_discourse"]["findings"], [])

    def test_directory_sweep_ignores_hidden_dirs_and_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "clean.md").write_text(
                "Mẫu mô được quan sát dưới kính hiển vi điện tử với độ phóng đại 400 lần.",
                encoding="utf-8",
            )
            sub = root / "sections"
            sub.mkdir()
            (sub / "part.tex").write_text(
                "Kết quả thử nghiệm dưới các giả định chuẩn vẫn cần kiểm chứng thêm.",
                encoding="utf-8",
            )
            hidden = root / ".hidden"
            hidden.mkdir()
            (hidden / "ignored.md").write_text("TODO: must be ignored", encoding="utf-8")

            json_out = root / "out.json"
            md_out = root / "out.md"
            code = main([str(root), "--genre", "report", "--json", str(json_out), "--report", str(md_out), "--quiet"])
            self.assertEqual(code, 2)
            payload = json.loads(json_out.read_text(encoding="utf-8"))
            self.assertEqual(payload["summary"]["total_files"], 2)
            self.assertIn("Unified Academic-Prose Writing Gate", md_out.read_text(encoding="utf-8"))

    def test_missing_path_returns_exit_3(self) -> None:
        code = main(["/nonexistent/academic_prose_missing_file.md", "--quiet"])
        self.assertEqual(code, 3)


if __name__ == "__main__":
    unittest.main()
