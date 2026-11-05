from __future__ import annotations

import importlib
import sys
import tempfile
import unittest
from pathlib import Path

from openpyxl import Workbook


SCRIPTS_DIR = Path(__file__).resolve().parents[2]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

excel_workbook = importlib.import_module("release-notes-ai-generator.excel_workbook")
markdown_writer = importlib.import_module("release-notes-ai-generator.markdown_writer")
models = importlib.import_module("release-notes-ai-generator.models")


class MarkdownExportTest(unittest.TestCase):
    def test_export_appends_component_and_all_unique_pr_comments(self):
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "pr_for_release_note"
        sheet.append(
            [
                "component",
                "pr_author",
                "pr_link",
                "pr_title",
                "formated_release_note",
                "issue_type",
                "release_notes_written_by_ai",
                "ai_note_type",
            ]
        )
        first_pr = "https://github.com/pingcap/tidb/pull/101"
        second_pr = "https://github.com/pingcap/tidb/pull/102"
        sheet.append(
            [
                "execution",
                "contributor",
                f"{first_pr}\n{second_pr}\n{first_pr}",
                "Improve join memory usage",
                "",
                "type/enhancement",
                (
                    "- Improve memory efficiency for joins "
                    "[#100](https://github.com/pingcap/tidb/issues/100) "
                    "@[contributor](https://github.com/contributor)"
                ),
                "improvement",
            ]
        )
        header = excel_workbook.get_header(sheet)

        entries = excel_workbook.collect_markdown_entries_from_sheet(sheet, header)

        self.assertEqual([first_pr, second_pr], entries[0].pr_urls)
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "release-8.5.8.md"
            markdown_writer.write_release_file(output, "8.5.8", "TBD", entries)
            content = output.read_text(encoding="utf-8")

        expected_suffix = (
            "<!-- component: execution --> "
            f"<!-- pr: {first_pr} --> "
            f"<!-- pr: {second_pr} -->"
        )
        self.assertIn(expected_suffix, content)
        self.assertEqual(1, content.count(f"<!-- pr: {first_pr} -->"))
        self.assertEqual(1, content.count(f"<!-- pr: {second_pr} -->"))

    def test_existing_metadata_comments_are_not_duplicated(self):
        pr_url = "https://github.com/pingcap/tidb/pull/101"
        entry = models.MarkdownEntry(
            note_type="improvement",
            component="TiDB",
            note=(
                "- Improve join memory usage "
                "<!-- component: execution --> "
                f"<!-- pr: {pr_url} -->"
            ),
            raw_component="execution",
            pr_urls=[pr_url],
        )

        rendered = markdown_writer.note_with_metadata_markers(entry)

        self.assertEqual(1, rendered.count("<!-- component: execution -->"))
        self.assertEqual(1, rendered.count(f"<!-- pr: {pr_url} -->"))

    def test_duplicate_pr_report_groups_all_affected_entries(self):
        duplicate_pr = "https://github.com/tikv/tikv/pull/19973"
        other_pr = "https://github.com/tikv/tikv/pull/19926"
        unrelated_pr = "https://github.com/tikv/tikv/pull/20001"
        entries = [
            models.MarkdownEntry(
                "improvement",
                "TiKV",
                "- Add a background Analyze concurrency limit [#19623](issue-19623)",
                "tikv",
                [duplicate_pr, other_pr],
            ),
            models.MarkdownEntry(
                "improvement",
                "TiKV",
                "- Add the optional TiKV concurrency parameter [#19969](issue-19969)",
                "tikv",
                [duplicate_pr],
            ),
            models.MarkdownEntry(
                "bug_fix",
                "TiDB",
                "- Fix an unrelated issue [#20000](issue-20000)",
                "execution, planner, execution",
                [unrelated_pr],
            ),
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            release_file = Path(temp_dir) / "release-8.5.8-updated-by-ai.md"
            report_file = markdown_writer.duplicate_pr_report_path(release_file)
            duplicate_count = markdown_writer.write_duplicate_pr_report(
                report_file,
                "8.5.8",
                entries,
            )
            content = report_file.read_text(encoding="utf-8")

        self.assertEqual(1, duplicate_count)
        self.assertIn(
            "## Components\n\n- `tikv`\n- `execution`\n- `planner`",
            content,
        )
        self.assertEqual(1, content.count("- `tikv`"))
        self.assertEqual(1, content.count("- `execution`"))
        self.assertEqual(1, content.count("- `planner`"))
        self.assertNotIn("- `execution, planner, execution`", content)
        self.assertIn("## Duplicated PR References", content)
        self.assertIn(f"### [tikv/tikv#19973]({duplicate_pr})", content)
        self.assertIn("Referenced by 2 release note entries:", content)
        self.assertIn("[#19623](issue-19623)", content)
        self.assertIn("[#19969](issue-19969)", content)
        self.assertNotIn("[#20000](issue-20000)", content)

    def test_report_is_written_with_all_components_when_no_pr_is_duplicated(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            report_file = Path(temp_dir) / "release-duplicate-pr-report.md"
            duplicate_count = markdown_writer.write_duplicate_pr_report(
                report_file,
                "8.5.8",
                [
                    models.MarkdownEntry(
                        "improvement",
                        "TiDB",
                        "- Improve query execution",
                        "execution",
                        ["https://github.com/pingcap/tidb/pull/101"],
                    )
                ],
            )

            self.assertEqual(0, duplicate_count)
            self.assertTrue(report_file.exists())
            content = report_file.read_text(encoding="utf-8")
            self.assertIn("## Components\n\n- `execution`", content)
            self.assertIn(
                "## Duplicated PR References\n\n"
                "No duplicated PR references were found.",
                content,
            )


if __name__ == "__main__":
    unittest.main()
