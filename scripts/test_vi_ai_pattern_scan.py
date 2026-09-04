#!/usr/bin/env python3
"""Tests for the Vietnamese AI-pattern gate.

Run from scripts/: python3 test_vi_ai_pattern_scan.py

Three test groups, and each exists for a different reason:

* `TestDetection` — the registry classes in
  references/ai-pattern-vietnamese.md must actually fire, in both languages.
* `TestLicensedFalsePositives` — the §7 licensed list must stay silent. Every
  case here was measured on a real Vietnamese thesis, where a naive regex
  reported it and a human retracted the finding. A retracted finding costs more
  trust than the defect it hunts, so these are regression tests.
* `TestFixtures` — the shipped fixtures keep the gate honest in CI.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

import vi_ai_pattern_scan as module
from vi_ai_pattern_scan import scan

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def codes(result: dict) -> set[str]:
    return {f["class"] for f in result["findings"]}


def actionable(result: dict) -> list[dict]:
    return [f for f in result["findings"] if not f["licensable"]]


def read(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


class TestDetection(unittest.TestCase):
    def test_ceremonial_vocabulary_is_a_candidate(self) -> None:
        result = scan("Phương pháp đề xuất mang tính đột phá và cho kết quả vượt trội.")
        self.assertIn("ceremonial_padding", codes(result))
        self.assertEqual(result["exit_code"], 2)

    def test_unquantified_intensifier_is_a_candidate(self) -> None:
        result = scan("Phương pháp đề xuất cải thiện đáng kể hiệu năng bám.")
        self.assertIn("unquantified_intensifier", codes(result))

    def test_intensifier_with_a_number_is_not_a_candidate(self) -> None:
        result = scan("Phương pháp đề xuất giảm đáng kể 65,3% năng lượng truyền thông.")
        self.assertNotIn("unquantified_intensifier", codes(result))

    def test_statistical_significance_is_not_padding(self) -> None:
        result = scan("Khác biệt có ý nghĩa thống kê đáng kể (p < 0,05) giữa hai nhóm.")
        self.assertNotIn("unquantified_intensifier", codes(result))

    def test_empty_framing_is_a_candidate(self) -> None:
        result = scan("Có thể thấy rằng độ trễ tăng khi tải mạng tăng.")
        self.assertIn("empty_framing", codes(result))

    def test_translation_calque_is_a_candidate(self) -> None:
        result = scan("Kết quả này đã mở đường cho một hướng nghiên cứu mới.")
        self.assertIn("translation_calque", codes(result))

    def test_english_ceremonial_vocabulary_is_a_candidate(self) -> None:
        result = scan("This method plays an important role and is a testament to the design.")
        self.assertIn("ceremonial_padding", codes(result))

    def test_english_empty_framing_is_a_candidate(self) -> None:
        result = scan("It should be noted that it can be seen that the latency grows.")
        self.assertIn("empty_framing", codes(result))

    def test_hedge_stack_is_a_candidate(self) -> None:
        result = scan(
            "Kết quả có thể có khả năng phần nào gợi ý rằng phương pháp này "
            "dường như hiệu quả hơn."
        )
        self.assertIn("hedge_stack", codes(result))

    def test_single_hedge_is_not_a_candidate(self) -> None:
        result = scan("Kết quả gợi ý phương pháp này hiệu quả hơn trong phạm vi dữ liệu hiện có.")
        self.assertNotIn("hedge_stack", codes(result))

    def test_symmetric_padding_is_a_candidate(self) -> None:
        result = scan("Hệ thống đáp ứng đầy đủ và toàn diện các yêu cầu phong phú và đa dạng.")
        self.assertIn("symmetric_padding", codes(result))

    def test_co_occurrence_marks_a_passage(self) -> None:
        """§8: several independent signals in one sentence, not one word."""
        result = scan(
            "Có thể thấy rằng nghiên cứu này đóng vai trò then chốt và mang tính "
            "đột phá, cho kết quả vượt trội đáng kể."
        )
        self.assertIn("machine_marked_passage", codes(result))

    def test_one_ceremonial_word_alone_does_not_mark_a_passage(self) -> None:
        """§8 threshold: one signal proves nothing."""
        result = scan("Vấn đề an ninh lương thực là vấn đề quan trọng của nhiều quốc gia.")
        self.assertNotIn("machine_marked_passage", codes(result))


class TestLicensedFalsePositives(unittest.TestCase):
    """§7 of the registry. Each case was retracted on a real thesis."""

    def test_ceremonial_word_inside_a_negation_is_licensed(self) -> None:
        """`vượt trội` inside `không tồn tại ngưỡng mà tại đó …` states the claim."""
        result = scan("Như vậy không tồn tại ngưỡng mà tại đó ET vượt trội tuyệt đối.")
        self.assertEqual(actionable(result), [])

    def test_method_step_name_is_licensed(self) -> None:
        """`đọc chuyên sâu` is the name of a PRISMA screening step."""
        result = scan(
            "Tập lõi được xây dựng qua quá trình đọc nền tảng và đọc chuyên sâu "
            "theo khung PNCE trước khi chạy 10 nhánh truy vấn."
        )
        self.assertEqual(actionable(result), [])

    def test_acknowledgement_convention_is_licensed(self) -> None:
        result = scan("Tôi xin bày tỏ lòng biết ơn sâu sắc đến TS. Nguyễn Văn A.", genre="acknowledgement")
        self.assertEqual(actionable(result), [])

    def test_intensifier_with_a_citation_is_licensed(self) -> None:
        """Attributed magnitude: the source carries the number, not this sentence."""
        result = scan(
            "Một số nghiên cứu báo cáo mức giảm truyền tin đáng kể [12], nhưng "
            "không phải bài nào cũng báo cáo chất lượng điều khiển tương ứng."
        )
        self.assertEqual(actionable(result), [])

    def test_topic_comment_structure_is_not_a_dummy_subject(self) -> None:
        result = scan("Về phương pháp, nghiên cứu sử dụng thiết kế cắt ngang.")
        self.assertEqual(actionable(result), [])

    def test_sino_vietnamese_terminology_is_not_ceremonial(self) -> None:
        result = scan(
            "Bài toán được đưa về dạng tối ưu hóa lồi, sau đó chuẩn hóa và "
            "phân tầng theo miền tham số khả thi."
        )
        self.assertEqual(actionable(result), [])

    def test_decimal_comma_and_en_dash_survive(self) -> None:
        result = scan("Mức giảm nằm trong khoảng 58,8–75,3% với giai đoạn 2015–2025.")
        self.assertEqual(actionable(result), [])

    def test_genre_mandated_vietnamese_section_is_licensed(self) -> None:
        """`Tính cấp thiết của đề tài` is required by the Vietnamese thesis template."""
        result = scan("## Tính cấp thiết của đề tài\n\nNhu cầu bảo đảm an ninh lương thực tăng.")
        self.assertEqual(actionable(result), [])

    def test_protected_tokens_are_not_scanned(self) -> None:
        result = scan(
            r"Kết quả trong \cite{vuottroi2020} và \texttt{mang_tinh_dot_pha.py} "
            r"được giữ nguyên, xem $\sigma_{\text{toàn diện}}$."
        )
        self.assertEqual(actionable(result), [])


class TestFixtures(unittest.TestCase):
    def test_dirty_vietnamese_fixture_is_flagged(self) -> None:
        result = scan(read("vi_ai_pattern_dirty.md"))
        self.assertEqual(result["exit_code"], 2)
        self.assertGreaterEqual(len(actionable(result)), 5)
        self.assertIn("ceremonial_padding", codes(result))

    def test_dirty_english_fixture_is_flagged(self) -> None:
        result = scan(read("vi_ai_pattern_dirty_en.md"))
        self.assertEqual(result["exit_code"], 2)
        self.assertIn("ceremonial_padding", codes(result))

    def test_clean_fixture_is_silent(self) -> None:
        result = scan(read("vi_ai_pattern_clean.md"))
        self.assertEqual(result["findings"], [])
        self.assertEqual(result["exit_code"], 0)

    def test_licensed_fixture_is_silent(self) -> None:
        result = scan(read("vi_ai_pattern_licensed.md"))
        self.assertEqual(actionable(result), [])
        self.assertEqual(result["exit_code"], 0)

    def test_acknowledgement_fixture_is_silent(self) -> None:
        result = scan(read("vi_ai_pattern_acknowledgement.md"), genre="acknowledgement")
        self.assertEqual(actionable(result), [])

    def test_clean_scan_still_requires_manual_pass(self) -> None:
        result = scan(read("vi_ai_pattern_clean.md"))
        self.assertTrue(result["manual_pass_required"])
        self.assertIn("partial verification", result["note"])


class TestPatternInventoryIsPinned(unittest.TestCase):
    """Every regex is pinned by identity.

    Rationale earned by a mutation test: deleting a single Vietnamese or English
    pattern from the module left all behavioural tests green, because a class-level
    test only needs ONE of its patterns to fire. A gate whose patterns can be
    silently removed has no stopping power, so the inventory itself is the contract.
    """

    CEREMONIAL = (
        'đóng\\s+vai\\s+trò\\s+then\\s+chốt',
        'giữ\\s+vai\\s+trò\\s+(?:quan\\s+trọng|đặc\\s+biệt\\s+quan\\s+trọng)',
        'có\\s+ý\\s+nghĩa\\s+(?:vô\\s+cùng\\s+|hết\\s+sức\\s+)?quan\\s+trọng',
        'mang\\s+tính\\s+đột\\s+phá',
        '\\bvượt\\s+trội\\b',
        '\\btoàn\\s+diện\\b',
        '\\bsâu\\s+sắc\\b',
        '\\bmạnh\\s+mẽ\\b',
        '\\bphong\\s+phú\\b',
        '\\bsinh\\s+động\\b',
        '\\bnổi\\s+bật\\b',
        '\\btiên\\s+tiến\\b',
        '\\bhàng\\s+đầu\\b',
        '\\buy\\s+tín\\b',
        '\\bchuyên\\s+sâu\\b',
        '\\bthiết\\s+thực\\b',
        'hiệu\\s+quả\\s+cao\\b',
        'chất\\s+lượng\\s+cao\\b',
        'không\\s+ngừng\\s+(?:tăng|phát\\s+triển|mở\\s+rộng|hoàn\\s+thiện)',
        'mở\\s+ra\\s+hướng\\s+đi\\s+mới',
        'tạo\\s+tiền\\s+đề',
        'góp\\s+phần\\s+không\\s+nhỏ',
        'khẳng\\s+định\\s+vị\\s+thế',
        'dấu\\s+mốc\\s+quan\\s+trọng',
        'bước\\s+tiến\\s+quan\\s+trọng',
        'plays?\\s+an?\\s+(?:important|crucial|vital|key|pivotal)\\s+role',
        '\\bgroundbreaking\\b|\\brevolutionary\\b|\\bremarkable\\b|\\bunprecedented\\b',
        '\\bdelve\\s+into\\b',
        'paves?\\s+the\\s+way\\s+for|paved\\s+the\\s+way\\s+for',
        'a\\s+testament\\s+to',
    )

    UNQUANTIFIED = (
        '\\bđáng\\s+kể\\b',
        '\\brất\\s+lớn\\b',
        '\\bsignificantly\\b',
        '\\bsubstantially\\b',
        '\\bdramatically\\b',
    )

    EMPTY_FRAMING = (
        'có\\s+thể\\s+(?:thấy|nhận\\s+thấy)\\s+rằng',
        'như\\s+đã\\s+đề\\s+cập\\s+ở\\s+trên',
        'như\\s+chúng\\s+ta\\s+đã\\s+biết',
        'nói\\s+chung\\s+là\\b',
        'về\\s+cơ\\s+bản\\s+(?:thì|là)\\b',
        'trong\\s+(?:bối\\s+cảnh\\s+hiện\\s+nay|thời\\s+đại\\s+ngày\\s+nay)',
        'việc\\s+tiến\\s+hành\\s+thực\\s+hiện',
        'nhằm\\s+mục\\s+đích\\s+để',
        'có\\s+một\\s+nhu\\s+cầu\\s+cần\\s+thiết\\s+phải',
        'mang\\s+tính\\s+chất\\s+\\S+',
        'đóng\\s+vai\\s+trò\\s+là\\b',
        'thực\\s+hiện\\s+việc\\s+\\S+',
        'một\\s+trong\\s+những\\s+[^.;]{0,60}\\s+nhất\\b',
        'không\\s+thể\\s+phủ\\s+nhận\\s+rằng',
        'it\\s+can\\s+be\\s+seen\\s+that',
        'as\\s+(?:mentioned|stated)\\s+above',
        'carry\\s+out\\s+the\\s+process\\s+of',
    )

    CALQUE = (
        'đóng\\s+một\\s+vai\\s+trò\\s+quan\\s+trọng\\s+trong',
        'nó\\s+được\\s+phát\\s+hiện\\s+ra\\s+rằng',
        'có\\s+một\\s+số\\s+lượng\\s+lớn\\s+các',
        'điều\\s+quan\\s+trọng\\s+cần\\s+lưu\\s+ý\\s+là',
        'trong\\s+điều\\s+khoản\\s+của',
        'dựa\\s+trên\\s+một\\s+cơ\\s+sở\\s+hàng\\s+ngày',
        'đối\\s+chiếu\\s+chống\\s+lại',
        'cam\\s+kết\\s+với\\s+chất\\s+lượng',
        'cung\\s+cấp\\s+một\\s+cái\\s+nhìn\\s+sâu\\s+sắc',
        'mở\\s+đường\\s+cho',
        'bức\\s+tranh\\s+toàn\\s+cảnh\\s+về',
        'theo\\s+cách\\s+mà\\b',
    )

    DECORATIVE_PAIR = (
        'toàn\\s+diện\\s+(?:và\\s+)?sâu\\s+sắc',
        'phong\\s+phú\\s+(?:và\\s+)?đa\\s+dạng',
        'đa\\s+dạng\\s+(?:và\\s+)?phong\\s+phú',
        'nhanh\\s+chóng\\s+(?:và\\s+)?hiệu\\s+quả',
        'chính\\s+xác\\s+(?:và\\s+)?kịp\\s+thời',
        'kịp\\s+thời\\s+(?:và\\s+)?chính\\s+xác',
        'đầy\\s+đủ\\s+và\\s+toàn\\s+diện',
    )

    ORNAMENT = (
        'nhanh\\s+chóng',
        'hiệu\\s+quả',
        'chính\\s+xác',
        'đầy\\s+đủ',
        'toàn\\s+diện',
        'đa\\s+dạng',
        'phong\\s+phú',
        'linh\\s+hoạt',
        'mạnh\\s+mẽ',
        'sâu\\s+sắc',
        'vượt\\s+trội',
        'tối\\s+ưu',
        'sinh\\s+động',
    )

    HEDGE = (
        'có\\s+thể',
        'có\\s+khả\\s+năng',
        'dường\\s+như',
        'phần\\s+nào',
        'gợi\\s+ý',
        'nhìn\\s+chung',
        'tương\\s+đối',
        'hầu\\s+như',
        'có\\s+xu\\s+hướng',
    )

    def test_inventory_matches_module(self) -> None:
        for name in (
            "CEREMONIAL",
            "UNQUANTIFIED",
            "EMPTY_FRAMING",
            "CALQUE",
            "DECORATIVE_PAIR",
            "ORNAMENT",
            "HEDGE",
        ):
            with self.subTest(list=name):
                self.assertEqual(
                    list(getattr(module, name)),
                    list(getattr(self, name)),
                    f"{name} changed: a pattern was added or removed. "
                    "Update this pinned inventory deliberately, never to make a test pass.",
                )

    def test_every_pattern_compiles(self) -> None:
        for name in ("CEREMONIAL", "UNQUANTIFIED", "EMPTY_FRAMING", "CALQUE",
                     "DECORATIVE_PAIR", "ORNAMENT", "HEDGE"):
            for pattern in getattr(module, name):
                with self.subTest(list=name, pattern=pattern):
                    re.compile(pattern)

if __name__ == "__main__":
    unittest.main(verbosity=2)
