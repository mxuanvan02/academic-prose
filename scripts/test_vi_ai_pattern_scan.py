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
import tempfile
import unittest
import zipfile
from pathlib import Path

import vi_ai_pattern_scan as module
from vi_ai_pattern_scan import read_input, scan

FIXTURES = Path(__file__).resolve().parent / "fixtures"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def codes(result: dict) -> set[str]:
    return {f["class"] for f in result["findings"]}


def actionable(result: dict) -> list[dict]:
    return [f for f in result["findings"] if not f["licensable"]]


def read(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def minimal_docx(path: Path, paragraphs: list[tuple[str, str | None]]) -> None:
    body: list[str] = []
    for text, style in paragraphs:
        safe = (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
        body.append(f'<w:p>{ppr}<w:r><w:t xml:space="preserve">{safe}</w:t></w:r></w:p>')
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


class TestDocxInput(unittest.TestCase):
    def test_docx_preserves_heading_and_detects_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.docx"
            minimal_docx(
                path,
                [
                    ("Kết quả", "Heading1"),
                    ("Có thể thấy rằng độ trễ tăng khi tải mạng tăng.", None),
                ],
            )
            text = read_input(path)
            result = scan(text)
        self.assertIn("# Kết quả", text)
        self.assertIn("empty_framing", codes(result))
        finding = next(f for f in result["findings"] if f["class"] == "empty_framing")
        self.assertEqual(finding["heading"], "Kết quả")

    def test_docx_cli_returns_revision_exit_code(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.docx"
            minimal_docx(path, [("Có thể thấy rằng độ trễ tăng.", None)])
            exit_code = module.main([str(path), "--quiet"])
        self.assertEqual(exit_code, 2)


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


class TestSelfReferenceRegister(unittest.TestCase):
    """Registry §11: Vietnamese self-reference and first-person register.

    Every case here was measured on a real Vietnamese manuscript. The
    "bài toán" case is a measured FALSE POSITIVE: the first draft of the
    detector excluded only "bài báo", so it flagged "Mục tiêu của bài toán là
    giảm thiểu sai số bám" — an ordinary Vietnamese compound naming an object,
    not the manuscript. A retracted finding costs more trust than the defect it
    hunts, so the compound exclusion is a regression test.
    """

    def test_self_reference_is_a_candidate(self) -> None:
        for sentence in (
            "Quy ước đếm của bài là độ sâu khai của mỗi lệnh.",
            "Mô phỏng của bài không rơi vào ô thứ hai.",
            "Bài không có dữ liệu thực địa để hiệu chỉnh vùng này.",
        ):
            with self.subTest(sentence=sentence):
                result = scan(sentence)
                self.assertIn("self_reference", codes(result))
                self.assertEqual(result["exit_code"], 2)

    def test_bare_first_person_ta_is_a_candidate(self) -> None:
        result = scan("Ta cần phải chuyển đổi chỉ báo của bài sang phát thải mê-tan.")
        self.assertIn("bare_first_person", codes(result))

    def test_bai_compound_naming_an_object_is_licensed(self) -> None:
        """`bài toán`, `bài báo`, `bài học` name an object, not the manuscript."""
        for sentence in (
            "Mục tiêu của bài toán là giảm thiểu sai số bám trên toàn tuyến.",
            "Bài báo này trình bày phương pháp dựa trên bản sao số FAO-56.",
            "Các bài học rút ra từ thực nghiệm cần được kiểm chứng lại.",
        ):
            with self.subTest(sentence=sentence):
                result = scan(sentence)
                self.assertNotIn("self_reference", codes(result))

    def test_ta_as_a_noun_is_licensed(self) -> None:
        """`héc-ta` and `đơn vị ta` are ordinary Vietnamese, not first person."""
        for sentence in (
            "Việt Nam cam kết một triệu héc-ta lúa phát thải thấp vào năm 2030.",
            "Đơn vị ta không đồng ý với kết luận của nhóm tác giả.",
        ):
            with self.subTest(sentence=sentence):
                result = scan(sentence)
                self.assertNotIn("bare_first_person", codes(result))

    def test_chung_ta_is_licensed(self) -> None:
        result = scan("Chúng ta đã biết điều này từ trước.")
        self.assertNotIn("bare_first_person", codes(result))

    def test_threshold_key_registered(self) -> None:
        result = scan("Quy ước đếm của bài là độ sâu khai.")
        checks = {c["check"] for c in result["thresholds"]}
        self.assertIn("self_reference", checks)
        self.assertIn("bare_first_person", checks)


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

    SELF_REFERENCE = (
        'của\\s+bài(?!\\s+(?:báo|học|toán|tập|viết|phát|thuyết|trình|kiểm|đề|'
        'nội\\s+dung|quan|trắc|đối|chiếu|song|hát|cổ|sử|thơ|tốn|phụ|lục|'
        'văn|nghệ|nghiên\\s+cứu))',
        '\\bbài(?!\\s+(?:báo|học|toán|tập|viết|phát|thuyết|trình|kiểm|đề|'
        'nội\\s+dung|quan|trắc|đối|chiếu|song|hát|cổ|sử|thơ|tốn|phụ|lục|'
        'văn|nghệ|nghiên\\s+cứu))\\s+(?:không|chưa|đã|được|có|đặt\\s+ra|'
        'trình\\s+bày|cung\\s+cấp|chỉ\\s+ra)\\b',
    )

    FIRST_PERSON_TA = (
        '(?<!chúng )(?<![\\w-])ta\\s+(?:cần|phải|thấy|đề\\s+xuất|cho\\s+rằng|'
        'khẳng\\s+định|có\\s+thể|cho\\s+thấy|quyết|định\\s+ý)\\b',
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
            "SELF_REFERENCE",
            "FIRST_PERSON_TA",
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
                     "DECORATIVE_PAIR", "ORNAMENT", "HEDGE", "SELF_REFERENCE",
                     "FIRST_PERSON_TA"):
            for pattern in getattr(module, name):
                with self.subTest(list=name, pattern=pattern):
                    re.compile(pattern)

class TestExplanatoryColon(unittest.TestCase):
    """Registry §2b: explanatory colons are a Vietnamese prose defect."""

    def _hits(self, text: str, genre: str = "manuscript") -> list[dict]:
        res = module.scan(text, genre)
        return [f for f in res["findings"] if f["class"] == "explanatory_colon"]

    def test_flags_explanatory_colon_in_vietnamese_prose(self) -> None:
        text = (
            "## 1. Đặt vấn đề\n\n"
            "Cơ chế thứ nhất là hiệu ứng quy mô: máy rút tiền làm giảm số giao dịch "
            "viên cần cho một chi nhánh nên các ngân hàng mở thêm chi nhánh.\n"
        )
        hits = self._hits(text)
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["verdict"], "recast")

    def test_flags_colon_in_heading(self) -> None:
        text = "## 3. Khung phân tích: vòng đời bốn pha của một công cụ lao động\n\nNội dung tiếng Việt ở đây.\n"
        self.assertEqual(len(self._hits(text)), 1)

    def test_licenses_venue_labels(self) -> None:
        text = (
            "**Từ khóa:** trí tuệ nhân tạo, công cụ lao động\n\n"
            "**Tóm tắt.** Bài viết khảo sát câu hỏi bằng tiếng Việt có dấu.\n"
        )
        self.assertEqual(self._hits(text), [])

    def test_licenses_bibliography_section(self) -> None:
        text = (
            "## Tài liệu tham khảo\n\n"
            "1. Allen R. C. Engels' pause. Explorations in Economic History, 46(4), "
            "418–435, 2009. DOI: 10.1016/j.eeh.2009.04.004\n"
        )
        self.assertEqual(self._hits(text), [])

    def test_licenses_url_and_doi_in_body(self) -> None:
        text = (
            "## 2. Phương pháp\n\n"
            "Nguồn được truy xuất tại https://example.org/a và có mã DOI: 10.1000/x "
            "trong bài viết tiếng Việt này.\n"
        )
        self.assertEqual(self._hits(text), [])

    def test_licenses_ratio_and_time(self) -> None:
        text = "## 2. Kết quả\n\nTỷ lệ pha loãng là 10:1 và ca đo lúc 08:30 trong báo cáo tiếng Việt.\n"
        self.assertEqual(self._hits(text), [])

    def test_licenses_english_only_sentence(self) -> None:
        text = (
            "## Abstract\n\n"
            "A FRAMEWORK FOR ANALYSIS: COMPARISON AND IMPLICATIONS.\n"
        )
        self.assertEqual(self._hits(text), [])

    def test_ignores_english_manuscript_entirely(self) -> None:
        text = (
            "## 1. Introduction\n\n"
            "The mechanism is a scale effect: the machine reduced the number of tellers "
            "required per branch, so banks opened more branches.\n"
        )
        self.assertEqual(self._hits(text), [])

    def test_acknowledgement_genre_is_licensed(self) -> None:
        text = (
            "## Lời cảm ơn\n\n"
            "Nhóm tác giả xin gửi lời cảm ơn đến đơn vị đã hỗ trợ: phòng thí nghiệm "
            "và quỹ tài trợ đề tài tiếng Việt.\n"
        )
        self.assertEqual(self._hits(text, genre="acknowledgement"), [])

    def test_counts_every_colon_not_one_per_sentence(self) -> None:
        text = (
            "## 1. Đặt vấn đề\n\n"
            "Nghịch lý thứ nhất: máy thay người. Nghịch lý thứ hai: người mất kỹ năng.\n"
        )
        self.assertEqual(len(self._hits(text)), 2)

    def test_licenses_author_block_labels(self) -> None:
        """`Tác giả liên hệ:` / `Email tác giả chính:` are venue front-matter labels."""
        # Fixture uses invented names and a generic affiliation: the point is the
        # LABELS (`Tác giả liên hệ:`, `Email tác giả chính:`), not any real identity.
        text = (
            "Trần Thị A\u00b9, Lê Văn B\u00b2 \u00b3 *\n\n"
            "\u00b9 Khoa Mẫu, Trường Đại học Mẫu\n"
            "* Tác giả liên hệ: Lê Văn B. Email: a@b.edu.vn\n"
            "Email tác giả chính: c@d.edu.vn\n"
        )
        self.assertEqual(self._hits(text), [])

    def test_threshold_key_registered(self) -> None:
        self.assertIn("explanatory_colon", module.THRESHOLDS)
        self.assertEqual(module.THRESHOLDS["explanatory_colon"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
