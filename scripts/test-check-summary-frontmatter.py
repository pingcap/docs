#!/usr/bin/env python3

import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("check-summary-frontmatter.py")
SPEC = importlib.util.spec_from_file_location("frontmatter_checker", SCRIPT)
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class FrontmatterTests(unittest.TestCase):
    def check(self, text):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "page.md"
            path.write_text(text, encoding="utf-8")
            return CHECKER.check_file(path)

    def test_colon_inside_unquoted_summary(self):
        issues = self.check("---\ntitle: JSON & Search\nsummary: シナリオ: CityDrive\n---\n")
        self.assertTrue(any(line == 3 and "invalid YAML" in message for line, message in issues))

    def test_unquoted_template_title(self):
        issues = self.check("---\ntitle: {{{ .starter }}} 移行ガイド\nsummary: API migration\n---\n")
        self.assertTrue(any("invalid YAML" in message for _, message in issues))

    def test_unescaped_inner_double_quotes(self):
        issues = self.check('---\ntitle: Guide\nsummary: "Create an "IAM Role" source."\n---\n')
        self.assertTrue(any(line == 3 and "invalid YAML" in message for line, message in issues))

    def test_existing_special_leading_summary_guard(self):
        for value in ("`COPY INTO` command", "{{{ .lake }}} guide", "[start, end]", "*date1* value"):
            with self.subTest(value=value):
                issues = self.check(f"---\ntitle: Guide\nsummary: {value}\n---\n")
                self.assertTrue(any("quote the summary value" in message for _, message in issues))

    def test_valid_quoted_values_and_body(self):
        text = (
            '---\ntitle: "{{{ .starter }}} guide"\n'
            'summary: "Scenario: Create an \\"IAM Role\\" source."\n---\n'
            'summary: Body text: is not frontmatter\n'
        )
        self.assertEqual(self.check(text), [])

    def test_valid_multiline_summary(self):
        self.assertEqual(self.check("---\ntitle: Guide\nsummary: >\n  Scenario: CityDrive\n---\n"), [])

    def test_missing_closing_delimiter(self):
        self.assertTrue(self.check("---\ntitle: Guide\nsummary: Text\n"))

    def test_no_frontmatter(self):
        self.assertEqual(self.check("# Guide\nsummary: Scenario: CityDrive\n"), [])

    def test_cli_failure_and_line_number(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "page.md"
            path.write_text("---\ntitle: Guide\nsummary: Scenario: CityDrive\n---\n", encoding="utf-8")
            result = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn(f"{path}:3: invalid YAML frontmatter", result.stdout)


if __name__ == "__main__":
    unittest.main()
