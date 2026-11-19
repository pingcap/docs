"""Test the actual exclusion helper embedded in the Japanese translation workflow."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = yaml.safe_load((ROOT / ".github/workflows/translation-cron.yml").read_text())
STEPS = WORKFLOW["jobs"]["translate-ja"]["steps"]
PREPARE = next(step for step in STEPS if step.get("id") == "prepare_tocs")
HELPER = PREPARE["run"].split("<<'PY'\n", 1)[1].split("\nPY\n", 1)[0]
MODULE = {"__name__": "toc_exclusions_test"}
exec(compile(HELPER, "translation-toc-exclusions.py", "exec"), MODULE)
REMOVE = MODULE["remove_exclusions"]
RESTORE = MODULE["restore_exclusions"]
FILES = ["tidb-cloud-log-redaction.md"]
TRANSLATIONS = {"Data Access Control": "データアクセス制御"}
BASE = """# TOC
- Security
  - Network
    - [TLS](/tls.md)
  - Data Access Control
    - [Redaction](/tidb-cloud/tidb-cloud-log-redaction.md)
  - Audit
    - [Audit](/audit.md)
- Billing
  - [Billing](/billing.md)
"""
TARGET = """# 目次
- セキュリティ
  - ネットワーク
    - [TLS](/tls.md)
  - 監査管理
    - [監査](/audit.md)
- 請求
  - [請求](/billing.md)
"""


class TocExclusionsTest(unittest.TestCase):
    def test_restoration_preserves_existing_labels_and_round_trips(self):
        restored = RESTORE(BASE, TARGET, FILES, TRANSLATIONS)
        self.assertIn("  - データアクセス制御\n    - [Redaction]", restored)
        self.assertIn("  - 監査管理\n    - [監査]", restored)
        self.assertEqual(REMOVE(restored, FILES), TARGET)
        self.assertEqual(RESTORE(BASE, restored, FILES, TRANSLATIONS), restored)

    def test_link_only_exclusion_reuses_existing_parent(self):
        target = TARGET.replace("  - 監査管理", "  - 既存のアクセス制御\n  - 監査管理")
        restored = RESTORE(BASE, target, FILES, TRANSLATIONS)
        self.assertIn("  - 既存のアクセス制御\n    - [Redaction]", restored)

    def test_shared_parent_and_sibling_links_survive(self):
        content = "- Group\n  - [Hide](/tidb-cloud-log-redaction.md#example)\n  - [Keep](/keep.md)\n"
        self.assertEqual(REMOVE(content, FILES), "- Group\n  - [Keep](/keep.md)\n")

    def test_nested_empty_groups_are_removed_but_other_empty_groups_remain(self):
        content = "# Section\n- Outer\n  - Inner\n    - [Hide](/tidb-cloud-log-redaction.md)\n- Already empty\n"
        self.assertEqual(REMOVE(content, FILES), "# Section\n- Already empty\n")

    def test_cleanup_is_idempotent_and_does_not_match_similar_names(self):
        content = "- [Keep](/not-tidb-cloud-log-redaction.md)\n"
        self.assertEqual(REMOVE(content, FILES), content)
        self.assertEqual(REMOVE(TARGET, FILES), TARGET)

    def test_multiple_excluded_children_empty_the_parent(self):
        content = "- Group\n  - [A](/a.md)\n  - [B](/b.md)\n"
        self.assertEqual(REMOVE(content, ["a.md", "b.md"]), "")

    def test_head_new_sibling_keeps_japanese_group(self):
        restored = RESTORE(BASE, TARGET, FILES, TRANSLATIONS)
        updated = restored.replace("  - 監査管理", "    - [新規](/new.md)\n  - 監査管理")
        cleaned = REMOVE(updated, FILES)
        self.assertIn("  - データアクセス制御\n    - [新規](/new.md)", cleaned)

    def test_missing_group_translation_or_unrelated_drift_fails(self):
        with self.assertRaisesRegex(ValueError, "Missing Japanese translation"):
            RESTORE(BASE, TARGET, FILES, {})
        with self.assertRaisesRegex(ValueError, "Cannot uniquely align"):
            RESTORE(BASE, TARGET.replace("/tls.md", "/other.md"), FILES, TRANSLATIONS)

    def test_absent_source_exclusion_does_not_restore_anything(self):
        self.assertEqual(RESTORE(TARGET, TARGET, FILES, TRANSLATIONS), TARGET)

    def test_renamed_hidden_group_reuses_translation_in_later_rounds(self):
        head = BASE.replace("Data Access Control", "Log Management")
        translated = RESTORE(BASE, TARGET, FILES, TRANSLATIONS).replace(
            "データアクセス制御", "ログ管理")
        remembered = MODULE["remember_group_translations"](head, translated, FILES)
        self.assertEqual(remembered, {"Log Management": "ログ管理"})
        first = REMOVE(translated, FILES)
        second = RESTORE(head, first, FILES, remembered)
        self.assertEqual(second, translated)
        second_with_sibling = second.replace("  - 監査管理", "    - [Other](/other.md)\n  - 監査管理")
        self.assertIn("  - ログ管理\n    - [Other]", REMOVE(second_with_sibling, FILES))

    def test_incomplete_translation_structure_does_not_supply_cached_titles(self):
        self.assertEqual(MODULE["remember_group_translations"](BASE, TARGET, FILES), {})

    def test_english_removes_link_but_leaves_its_empty_parent(self):
        head = BASE.replace("    - [Redaction](/tidb-cloud/tidb-cloud-log-redaction.md)\n", "")
        translated = RESTORE(BASE, TARGET, FILES, TRANSLATIONS).replace(
            "    - [Redaction](/tidb-cloud/tidb-cloud-log-redaction.md)\n", "")
        self.assertEqual(REMOVE(translated, FILES, TRANSLATIONS.values()), TARGET)
        restored_next_round = RESTORE(head, TARGET, FILES, TRANSLATIONS)
        self.assertEqual(restored_next_round, translated)

    def test_cleanup_runs_after_sync_failure_and_gates_pr_preparation(self):
        cleanup = next(step for step in STEPS if step.get("id") == "cleanup_tocs")
        changes = next(step for step in STEPS if step.get("id") == "changes")
        self.assertIn("always()", cleanup["if"])
        self.assertNotIn("continue-on-error", cleanup)
        self.assertIn("steps.cleanup_tocs.outcome == 'success'", changes["if"])

    def test_shell_prepare_and_cleanup_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            target = root / "target"
            (root / "bin").mkdir()
            (root / "bin/python").symlink_to(sys.executable)
            source.mkdir()
            target.mkdir()
            subprocess.run(["git", "init", "-q", str(source)], check=True)
            subprocess.run(["git", "init", "-q", str(target)], check=True)
            (source / "TOC.md").write_text(BASE)
            subprocess.run(["git", "-C", str(source), "add", "TOC.md"], check=True)
            subprocess.run([
                "git", "-C", str(source), "-c", "user.name=Test", "-c",
                "user.email=test@example.com", "commit", "-qm", "base",
            ], check=True)
            (target / "TOC.md").write_text(TARGET)
            cursor = target / "latest_translation_commit.json"
            cursor.write_text('{"target": "release-8.5", "sha": "old"}')
            env = {**os.environ, "PATH": str(root / "bin") + os.pathsep + os.environ["PATH"],
                   "RUNNER_TEMP": directory, "BASE_REF": "HEAD", "HEAD_REF": "HEAD",
                   "SYNC_OUTCOME": "success",
                   "DOCS_SOURCE_PATH": str(source), "DOCS_TARGET_PATH": str(target),
                   "SOURCE_FILES": "TOC.md", "TOC_EXCLUSIONS":
                   '{"tidb-cloud-log-redaction.md": ["TOC.md"]}',
                   "TOC_EXCLUSION_GROUP_TRANSLATIONS":
                   '{"Data Access Control": "データアクセス制御"}'}
            subprocess.run(["bash", "-c", PREPARE["run"]], env=env, check=True,
                           capture_output=True, text=True)
            self.assertIn("データアクセス制御", (target / "TOC.md").read_text())
            cleanup = next(step for step in STEPS if step.get("id") == "cleanup_tocs")
            subprocess.run(["bash", "-c", cleanup["run"]], env=env, check=True,
                           capture_output=True, text=True)
            self.assertEqual((target / "TOC.md").read_text(), TARGET)

            self.assertEqual(json.loads(cursor.read_text())["sha"], "old")
            remembered = json.loads(cursor.read_text())["toc_exclusion_group_translations"]
            self.assertEqual(remembered["TOC.md"], TRANSLATIONS)

            # Even matching structure cannot justify caching labels after failure
            # or when this TOC was outside the selected translation scope.
            for extra_env in ({"SYNC_OUTCOME": "failure"}, {"SOURCE_FILES": "other.md"}):
                with self.subTest(cache_guard=extra_env):
                    (target / "TOC.md").write_text(
                        RESTORE(BASE, TARGET, FILES, TRANSLATIONS).replace(
                            "データアクセス制御", "SHOULD NOT BE CACHED"))
                    subprocess.run(["bash", "-c", cleanup["run"]],
                                   env={**env, **extra_env}, check=True,
                                   capture_output=True, text=True)
                    self.assertEqual(json.loads(cursor.read_text())[
                        "toc_exclusion_group_translations"], remembered)
                    self.assertEqual((target / "TOC.md").read_text(), TARGET)

            for extra_env in ({"SOURCE_FILES": "other.md"},
                              {"SOURCE_FILES_TRANSLATION_MODE": "full"}):
                with self.subTest(extra_env=extra_env):
                    subprocess.run(["bash", "-c", PREPARE["run"]],
                                   env={**env, **extra_env}, check=True,
                                   capture_output=True, text=True)
                    self.assertEqual((target / "TOC.md").read_text(), TARGET)

            # One bad TOC must prevent temporary edits to all configured TOCs.
            (target / "bad.md").write_text(TARGET.replace("/tls.md", "/wrong.md"))
            (source / "bad.md").write_text(BASE)
            subprocess.run(["git", "-C", str(source), "add", "bad.md"], check=True)
            subprocess.run([
                "git", "-C", str(source), "-c", "user.name=Test", "-c",
                "user.email=test@example.com", "commit", "-qm", "second TOC",
            ], check=True)
            failed = subprocess.run(["bash", "-c", PREPARE["run"]],
                env={**env, "SOURCE_FILES": "TOC.md,bad.md", "TOC_EXCLUSIONS":
                     '{"tidb-cloud-log-redaction.md": ["TOC.md", "bad.md"]}'},
                capture_output=True, text=True)
            self.assertNotEqual(failed.returncode, 0)
            self.assertIn("bad.md: Cannot uniquely align", failed.stderr)
            self.assertEqual((target / "TOC.md").read_text(), TARGET)

            changes = next(step for step in STEPS if step.get("id") == "changes")
            subprocess.run(["bash", "-c", changes["run"]], cwd=target,
                env={**env, "GITHUB_OUTPUT": str(root / "outputs"),
                     "SOURCE_BRANCH": "release-8.5", "COMMIT_SYNC_RUN_TYPE": "schedule",
                     "FAILURE_REPORT": str(root / "absent-failure-report")},
                check=True, capture_output=True, text=True)
            saved = json.loads(cursor.read_text())
            self.assertEqual(saved["sha"], "HEAD")
            self.assertEqual(saved["toc_exclusion_group_translations"], remembered)


if __name__ == "__main__":
    unittest.main()
