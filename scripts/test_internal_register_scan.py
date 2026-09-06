#!/usr/bin/env python3
"""Verification suite for the internal register gate.

Each test names the gate criterion it verifies, so a failure points at a rule in
references/internal-register-gate.md rather than at an opaque regex.

Run: python3 scripts/test_internal_register_scan.py
"""
from __future__ import annotations

import unittest
from pathlib import Path

from internal_register_scan import BLOCKING, THRESHOLDS, read_input, scan, split_sections, strip_protected

FIXTURES = Path(__file__).parent / "fixtures"


def scan_fixture(name: str, genre: str = "manuscript") -> dict:
    return scan(read_input(FIXTURES / name), genre)


def classes(result: dict) -> set[str]:
    return {f["class"] for f in result["findings"]}


def actionable_classes(result: dict) -> set[str]:
    return {f["class"] for f in result["findings"] if not f["licensable"]}


class TestDetection(unittest.TestCase):
    """Criterion 1-2: every prohibited class is detected and graded."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.dirty = scan_fixture("internal_register_dirty.md")
        cls.dirty_en = scan_fixture("internal_register_dirty_en.md")

    def test_all_prohibited_classes_detected(self) -> None:
        expected = {
            "self_reminder_prose",
            "document_as_subject",
            "progress_state_limitation",
            "verification_log_prose",
            "internal_artifact_reference",
            "assistant_residue",
            "placeholder_residue",
            "revision_response_leak",
            "defensive_disclaimer_stack",
            "venue_ambition_leak",
        }
        self.assertTrue(expected.issubset(classes(self.dirty)), classes(self.dirty))

    def test_english_dirty_fixture_detects_the_same_classes(self) -> None:
        expected = {
            "self_reminder_prose",
            "document_as_subject",
            "progress_state_limitation",
            "verification_log_prose",
            "internal_artifact_reference",
            "assistant_residue",
            "placeholder_residue",
            "revision_response_leak",
            "defensive_disclaimer_stack",
            "venue_ambition_leak",
        }
        self.assertTrue(expected.issubset(classes(self.dirty_en)), classes(self.dirty_en))
        self.assertEqual(self.dirty_en["exit_code"], 1)
        self.assertEqual(self.dirty_en["gate"], "block")

    def test_blocking_classes_force_exit_1(self) -> None:
        self.assertEqual(self.dirty["exit_code"], 1)
        self.assertEqual(self.dirty["gate"], "block")
        self.assertEqual(set(self.dirty["blocking"]), BLOCKING)

    def test_every_threshold_reported(self) -> None:
        reported = {c["check"] for c in self.dirty["thresholds"]}
        self.assertEqual(reported, set(THRESHOLDS))

    def test_disclaimer_stack_needs_three_markers(self) -> None:
        two = scan("Kết quả chỉ thiết lập X. Chúng không chứng minh Y. Dữ liệu gồm 500 bản ghi.")
        self.assertNotIn("defensive_disclaimer_stack", classes(two))
        three = scan(
            "Kết quả chỉ thiết lập X. Chúng không chứng minh Y. Chúng không bảo đảm Z."
        )
        self.assertIn("defensive_disclaimer_stack", classes(three))
        three_en = scan(
            "The results only establish X. They do not prove Y. They cannot guarantee Z."
        )
        self.assertIn("defensive_disclaimer_stack", classes(three_en))


class TestCleanText(unittest.TestCase):
    """Criterion 3: recast prose passes; the scan does not fire on repairs."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.clean = scan_fixture("internal_register_clean.md")
        cls.clean_en = scan_fixture("internal_register_clean_en.md")

    def test_clean_fixture_scans_clean(self) -> None:
        self.assertEqual(self.clean["findings"], [], self.clean["findings"])
        self.assertEqual(self.clean["exit_code"], 0)
        self.assertEqual(self.clean["gate"], "scan_clean")

    def test_english_clean_fixture_scans_clean(self) -> None:
        self.assertEqual(self.clean_en["findings"], [], self.clean_en["findings"])
        self.assertEqual(self.clean_en["exit_code"], 0)

    def test_clean_report_still_demands_manual_pass(self) -> None:
        self.assertTrue(self.clean["manual_pass_required"])
        self.assertIn("partial verification", self.clean["note"])


class TestFalsePositives(unittest.TestCase):
    """Criterion 4: licensed slots must not be reported as defects."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.fp = scan_fixture("internal_register_licensed.md")

    def test_licensed_slots_produce_no_actionable_finding(self) -> None:
        self.assertEqual(actionable_classes(self.fp), set(), self.fp["findings"])
        self.assertEqual(self.fp["exit_code"], 0)

    def test_resolved_cross_reference_is_not_a_hit(self) -> None:
        r = scan("Bảng 2 cho thấy độ chính xác 55,43%. Hình 4 trình bày ma trận nhầm lẫn.")
        self.assertEqual(r["findings"], [])

    def test_public_identifiers_are_not_internal_artifacts(self) -> None:
        r = scan(
            "Dữ liệu công bố tại https://doi.org/10.1234/example và bộ SQuAD được dùng để đối chiếu."
        )
        self.assertNotIn("internal_artifact_reference", classes(r))

    def test_vietnamese_first_person_in_methods_is_allowed(self) -> None:
        r = scan("Chúng tôi lấy mẫu 500 bản ghi theo phương pháp phân tầng.")
        self.assertEqual(r["findings"], [])

    def test_correlative_not_only_is_not_a_disclaimer_stack(self) -> None:
        # "không chỉ … mà còn" is an intensifier, not a claim denial. Measured on
        # a real manuscript, this construction produced five false stack hits.
        text = (
            "Ưu thế của mô hình không chỉ đến từ biểu diễn mạnh mà còn từ tầng chọn lọc. "
            "Ý nghĩa không chỉ nằm ở chỉ số mà còn ở thiết kế. "
            "Kết quả không chỉ đúng trên một tập mà còn trên tập thứ hai."
        )
        self.assertNotIn("defensive_disclaimer_stack", classes(scan(text)))
        text_en = (
            "The advantage comes not only from representation but also from selection. "
            "The implication lies not only in the scores but also in the design. "
            "The result holds not only on one set but also on the second."
        )
        self.assertNotIn("defensive_disclaimer_stack", classes(scan(text_en)))

    def test_latex_preamble_is_not_prose(self) -> None:
        text = (
            "\\documentclass{article}\n"
            "\\newif\\ifFinal\n\\InputIfFileExists{publication_metadata.validated.tex}{}{}\n"
            "\\begin{document}\nDữ liệu gồm 500 bản ghi.\n\\end{document}\n"
        )
        self.assertEqual(actionable_classes(scan(text)), set(), scan(text)["findings"])


class TestArtifactSeverity(unittest.TestCase):
    """Criterion 9: a machine-local path blocks; a repo script name is revision-level."""

    def test_local_path_is_blocking(self) -> None:
        r = scan("Kết quả trong tệp /Users/van/ket_qua.csv cho thấy X.")
        self.assertIn("internal_artifact_reference", r["blocking"])
        self.assertEqual(r["exit_code"], 1)

    def test_repo_script_in_reproducibility_statement_is_revision_not_block(self) -> None:
        r = scan("Prompt construction is versioned in scripts/anchored_judge.py.")
        self.assertIn("repo_artifact_reference", classes(r))
        self.assertEqual(r["blocking"], [])
        self.assertEqual(r["exit_code"], 2)


class TestRoadmapQuota(unittest.TestCase):
    """Criterion 5: one roadmap is licensable; a second is a finding."""

    def test_first_roadmap_is_licensable(self) -> None:
        r = scan("Phần này sẽ trình bày quy trình xây dựng dữ liệu.")
        docsub = [f for f in r["findings"] if f["class"] == "document_as_subject"]
        self.assertEqual(len(docsub), 1)
        self.assertTrue(docsub[0]["licensable"])
        self.assertEqual(r["exit_code"], 0)

    def test_second_roadmap_in_later_section_is_actionable(self) -> None:
        text = (
            "# Mở đầu\n\nPhần này sẽ trình bày quy trình xây dựng dữ liệu.\n\n"
            "# Phương pháp\n\nPhần này sẽ mô tả các tham số.\n\n"
            "# Kết quả\n\nMục này sẽ giới thiệu số liệu.\n"
        )
        r = scan(text)
        docsub = [f for f in r["findings"] if f["class"] == "document_as_subject"]
        self.assertGreaterEqual(len(docsub), 3)
        self.assertEqual(sum(1 for f in docsub if f["licensable"]), 1)
        self.assertEqual(r["exit_code"], 2)
        check = next(c for c in r["thresholds"] if c["check"] == "document_as_subject")
        self.assertFalse(check["pass"])


class TestGenreProfiles(unittest.TestCase):
    """Criterion 6: the genre decides which register is licensed."""

    def test_response_letter_licenses_its_own_register(self) -> None:
        r = scan_fixture("internal_register_response_letter.md", genre="response_letter")
        self.assertNotIn("revision_response_leak", classes(r))
        self.assertNotIn("assistant_residue", classes(r))

    def test_same_text_as_manuscript_is_a_finding(self) -> None:
        r = scan_fixture("internal_register_response_letter.md", genre="manuscript")
        self.assertIn("revision_response_leak", classes(r))

    def test_teaching_genre_licenses_forward_reference(self) -> None:
        text = "Ở phần sau chúng ta sẽ xét ví dụ thứ hai."
        self.assertIn("document_as_subject", classes(scan(text, "manuscript")))
        self.assertNotIn("document_as_subject", classes(scan(text, "teaching")))


class TestProtectedZones(unittest.TestCase):
    """Criterion 7: protected zones are exempt (policy section 7)."""

    def test_latex_protected_zones_are_stripped(self) -> None:
        r = scan_fixture("internal_register_protected.tex")
        self.assertEqual(actionable_classes(r), set(), r["findings"])

    def test_verbatim_block_is_exempt(self) -> None:
        text = (
            "\\documentclass{article}\n"
            "\\begin{verbatim}\nTODO: chạy lại /Users/van/main.tex\n\\end{verbatim}\n"
            "Dữ liệu gồm 500 bản ghi.\n"
        )
        self.assertEqual(scan(text)["findings"], [])

    def test_comment_is_exempt_but_body_is_not(self) -> None:
        text = "\\section{Kết quả}\n% TODO: sửa lại đoạn này\nDữ liệu gồm 500 bản ghi.\n"
        self.assertEqual(scan(text)["findings"], [])
        leaked = "\\section{Kết quả}\nTODO: sửa lại đoạn này.\n"
        self.assertIn("placeholder_residue", classes(scan(leaked)))

    def test_math_and_citation_arguments_are_exempt(self) -> None:
        text = "\\section{A}\nTa có $v_1 = 0$ và \\cite{main.tex2020} cho kết quả tương tự.\n"
        self.assertNotIn("internal_artifact_reference", classes(scan(text)))


class TestInvariants(unittest.TestCase):
    """Criterion 8: the scan's own contract."""

    def test_lexical_hit_is_never_a_verdict(self) -> None:
        for name in ("internal_register_dirty.md", "internal_register_clean.md"):
            self.assertTrue(scan_fixture(name)["manual_pass_required"])

    def test_empty_input_is_clean_not_crashing(self) -> None:
        r = scan("")
        self.assertEqual(r["exit_code"], 0)
        self.assertEqual(r["sentences"], 0)

    def test_sections_are_split_on_headings(self) -> None:
        chunks = split_sections("# A\n\nx.\n\n# B\n\ny.\n")
        self.assertEqual(len(chunks), 2)

    def test_strip_protected_preserves_plain_prose(self) -> None:
        text = "Dữ liệu gồm 500 bản ghi."
        self.assertIn("500 bản ghi", strip_protected(text))



class TestVenueAmbition(unittest.TestCase):
    """Criterion: the publication target is a planning decision, not a finding.

    This class is licensed by genre rather than by wording, so the same sentences
    must block in a manuscript and pass in a cover letter. Both directions are
    pinned: a detector that only ever fires proves nothing about its licensing,
    and one that never fires proves nothing at all.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.vi = scan_fixture("internal_register_venue_dirty.md")
        cls.en = scan_fixture("internal_register_venue_dirty_en.md")
        cls.clean = scan_fixture("internal_register_venue_clean.md")
        cls.letter_text = read_input(FIXTURES / "internal_register_cover_letter.md")

    def test_vietnamese_leak_blocks(self) -> None:
        self.assertIn("venue_ambition_leak", classes(self.vi))
        self.assertEqual(self.vi["exit_code"], 1)
        self.assertEqual(self.vi["gate"], "block")

    def test_english_leak_blocks(self) -> None:
        self.assertIn("venue_ambition_leak", classes(self.en))
        self.assertEqual(self.en["exit_code"], 1)
        self.assertEqual(self.en["gate"], "block")

    def test_legitimate_statistics_do_not_fire(self) -> None:
        """Interquartile range, fiscal quarter, and Scopus-in-Methods are correct prose."""
        self.assertNotIn("venue_ambition_leak", classes(self.clean))
        self.assertEqual(self.clean["exit_code"], 0)

    def test_venue_substring_inside_another_word_does_not_match(self) -> None:
        """Calibration case: `Revenue` contains `venue` and cost a real edit."""
        result = scan("Revenue in Q1 of the observation window was excluded.")
        self.assertNotIn("venue_ambition_leak", classes(result))

    def test_quantitative_vocabulary_is_not_a_venue_claim(self) -> None:
        for sentence in (
            "The interquartile range of per-item scores is 0.12.",
            "The first quartile falls at 0.79.",
            "The impact of annotator disagreement is bounded by the estimate.",
            "Records were retrieved from Scopus and Web of Science.",
            "Kho\u1ea3ng t\u1ee9 ph\u00e2n v\u1ecb c\u1ee7a \u0111i\u1ec3m s\u1ed1 l\u00e0 0,12.",
        ):
            with self.subTest(sentence=sentence):
                self.assertNotIn("venue_ambition_leak", classes(scan(sentence)))

    def test_genre_licensing_is_bidirectional(self) -> None:
        as_letter = scan(self.letter_text, "cover_letter")
        as_manuscript = scan(self.letter_text, "manuscript")
        self.assertNotIn("venue_ambition_leak", actionable_classes(as_letter))
        self.assertEqual(as_letter["exit_code"], 0)
        self.assertIn("venue_ambition_leak", classes(as_manuscript))
        self.assertEqual(as_manuscript["exit_code"], 1)

    def test_referee_anticipation_fires_in_both_languages(self) -> None:
        for sentence in (
            "Reviewers will likely ask for an additional ablation.",
            "An extra baseline was added to satisfy the reviewers.",
            "Ph\u1ea7n n\u00e0y \u0111\u01b0\u1ee3c b\u1ed5 sung nh\u1eb1m thuy\u1ebft ph\u1ee5c ph\u1ea3n bi\u1ec7n.",
        ):
            with self.subTest(sentence=sentence):
                self.assertIn("venue_ambition_leak", classes(scan(sentence)))

    def test_publication_intent_fires_in_both_languages(self) -> None:
        for sentence in (
            "We aim to publish this work in a high-impact journal.",
            "M\u1ee5c ti\u00eau l\u00e0 c\u00f4ng b\u1ed1 tr\u00ean t\u1ea1p ch\u00ed thu\u1ed9c nh\u00f3m Q1.",
        ):
            with self.subTest(sentence=sentence):
                self.assertIn("venue_ambition_leak", classes(scan(sentence)))

    def test_venue_ambition_is_registered_as_blocking(self) -> None:
        self.assertIn("venue_ambition_leak", BLOCKING)
        self.assertIn("venue_ambition_leak", THRESHOLDS)
        self.assertEqual(THRESHOLDS["venue_ambition_leak"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
