#!/usr/bin/env python3
"""Tests for the process-logic gate.

Run from scripts/: python3 test_process_logic_scan.py
"""
from __future__ import annotations

import unittest

from pathlib import Path

from process_logic_scan import scan

FIXTURES = Path(__file__).parent / "fixtures"


def scan_fixture(name: str) -> dict:
    return scan((FIXTURES / name).read_text(encoding="utf-8"))


def codes(result: dict) -> set[str]:
    return {item["class"] for item in result["findings"]}


class TestProcessChronology(unittest.TestCase):
    def test_unspecified_prior_event_is_a_candidate_in_vietnamese(self) -> None:
        result = scan(
            "Tập tham chiếu được hình thành trước qua quá trình đọc chuyên sâu; "
            "các truy vấn OpenAlex được dùng bổ sung để kiểm tra độ bao phủ."
        )
        self.assertIn("chronology_anchor_omitted", codes(result))
        self.assertEqual(result["exit_code"], 2)

    def test_unspecified_prior_event_is_a_candidate_in_english(self) -> None:
        result = scan(
            "The reference corpus was assembled beforehand through close reading; "
            "OpenAlex searches were used later to assess coverage."
        )
        self.assertIn("chronology_anchor_omitted", codes(result))

    def test_explicit_three_proposition_process_passes(self) -> None:
        result = scan(
            "Tập tham chiếu được xây dựng trước khi chạy truy vấn OpenAlex. "
            "Các truy vấn được thực hiện sau đó và chỉ dùng để kiểm tra độ bao phủ của tập này."
        )
        self.assertEqual(result["findings"], [])
        self.assertEqual(result["exit_code"], 0)

    def test_later_search_is_not_misreported_as_corpus_origin(self) -> None:
        result = scan(
            "Tập lõi được xác lập trước khi chạy truy vấn. "
            "Truy vấn bổ sung chỉ kiểm tra độ bao phủ, không tạo ra tập lõi."
        )
        self.assertEqual(result["findings"], [])

    def test_ordinary_temporal_language_is_not_a_hit(self) -> None:
        result = scan(
            "Nhiệt độ giảm trước khi bơm được bật. "
            "Sau đó, hệ chuyển sang chế độ duy trì."
        )
        self.assertEqual(result["findings"], [])


class TestFixtures(unittest.TestCase):
    """A gate is not implemented until its fixture executes."""

    def test_dirty_vietnamese_fixture_yields_candidates(self) -> None:
        result = scan_fixture("process_logic_dirty.md")
        self.assertEqual(result["exit_code"], 2)
        self.assertTrue(
            {"chronology_anchor_omitted", "reminder_instead_of_boundary"} & codes(result),
            codes(result),
        )

    def test_dirty_english_fixture_yields_candidates(self) -> None:
        result = scan_fixture("process_logic_dirty_en.md")
        self.assertEqual(result["exit_code"], 2)
        self.assertIn("chronology_anchor_omitted", codes(result))

    def test_clean_fixture_is_silent(self) -> None:
        result = scan_fixture("process_logic_clean.md")
        self.assertEqual(result["findings"], [], result["findings"])
        self.assertEqual(result["exit_code"], 0)

    def test_licensed_constructions_stay_silent(self) -> None:
        result = scan_fixture("process_logic_licensed.md")
        self.assertEqual(result["findings"], [], result["findings"])

    def test_clean_scan_still_requires_manual_pass(self) -> None:
        result = scan_fixture("process_logic_clean.md")
        self.assertTrue(result["manual_pass_required"])
        self.assertIn("partial verification", result["note"])


class TestCalibration(unittest.TestCase):
    """False positives measured on a real thesis, now locked by tests."""

    def test_dated_supplementary_search_is_not_a_role_gap(self) -> None:
        text = "Dữ liệu tìm kiếm bổ sung được chốt vào tháng 05/2026 theo nguyên tắc báo cáo minh bạch."
        self.assertEqual(scan(text)["findings"], [])

    def test_negative_role_counts_as_a_stated_role(self) -> None:
        text = "Truy vấn bổ sung chỉ kiểm tra độ bao phủ, không tạo ra tập lõi."
        self.assertEqual(scan(text)["findings"], [])

    def test_anchored_prior_state_is_not_a_candidate(self) -> None:
        text = "Tập lõi đã được hình thành trước khi chạy truy vấn, nên 10 nhánh giữ vai trò kiểm tra độ bao phủ."
        self.assertEqual(scan(text)["findings"], [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
