"""Check dependency pinning in GitHub Actions workflows."""

from pathlib import Path
import re
import shlex
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_DIR = ROOT / ".github/workflows"
LOCK = "scripts/ai-translator-requirements.lock"
HASHED_REQUIREMENT = re.compile(
    r"[A-Za-z0-9][A-Za-z0-9._-]*==[0-9][A-Za-z0-9.!+_-]*"
    r"(?:\s+--hash=sha256:[0-9a-f]{64})+"
)


class WorkflowDependenciesTest(unittest.TestCase):
    def test_external_uses_are_pinned(self):
        for path in sorted(WORKFLOW_DIR.iterdir()):
            if path.suffix not in {".yaml", ".yml"}:
                continue
            workflow = yaml.safe_load(path.read_text())
            for job in workflow["jobs"].values():
                for entry in [job, *job.get("steps", [])]:
                    uses = entry.get("uses")
                    if not uses or uses.startswith("./"):
                        continue
                    with self.subTest(workflow=path.name, uses=uses):
                        if uses.startswith("docker://"):
                            self.assertRegex(uses, r"@sha256:[0-9a-f]{64}$")
                        else:
                            self.assertRegex(uses, r"^[^@]+@[0-9a-f]{40}$")

    def test_checkouts_do_not_persist_credentials(self):
        for path in sorted(WORKFLOW_DIR.iterdir()):
            if path.suffix not in {".yaml", ".yml"}:
                continue
            workflow = yaml.safe_load(path.read_text())
            for job_name, job in workflow["jobs"].items():
                for step in job.get("steps", []):
                    if step.get("uses", "").startswith("actions/checkout@"):
                        with self.subTest(workflow=path.name, job=job_name, step=step.get("name")):
                            self.assertIs(step.get("with", {}).get("persist-credentials"), False)

    def assert_hash_locked_install(self, script, lock_path):
        commands = [
            shlex.split(line)
            for line in script.replace("\\\n", "").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
        if commands and commands[0] == ["set", "-euo", "pipefail"]:
            commands = commands[1:]
        self.assertEqual(commands, [[
            "python", "-m", "pip", "install", "--require-hashes",
            "--only-binary=:all:", "-r", lock_path,
        ]])

    def test_translation_workflows_use_the_hash_locked_install(self):
        for name, job, prefix, install_name in (
            ("translation-cron.yml", "translate-ja", "workflow-dependencies/", "Install Python dependencies"),
            ("translation-zh.yaml", "translate", "workflow-dependencies/", "Install Python dependencies"),
            ("sync-doc-pr-zh-to-en.yml", "sync-docs", "", "Install dependencies"),
        ):
            with self.subTest(workflow=name):
                workflow = yaml.safe_load((WORKFLOW_DIR / name).read_text())
                self.assertEqual(workflow["permissions"], {})
                translation_job = workflow["jobs"][job]
                self.assertEqual(
                    translation_job["permissions"], {"contents": "write", "pull-requests": "write"},
                )
                steps = translation_job["steps"]
                install = next(step for step in steps if step.get("name") == install_name)
                self.assert_hash_locked_install(install["run"], prefix + LOCK)
                other_commands = "\n".join(
                    line
                    for step in steps if step is not install
                    for line in step.get("run", "").replace("\\\n", "").splitlines()
                    if not line.lstrip().startswith("#")
                )
                self.assertNotRegex(other_commands, r"\bpip\s+install\b")
                if prefix:
                    checkout = next(step for step in steps if step.get("with", {}).get("path") == prefix.rstrip("/"))
                    self.assertEqual(checkout["with"]["ref"], "${{ github.sha }}")
                    self.assertEqual(checkout["with"]["sparse-checkout"], LOCK)
                    setup = next(step for step in steps if step.get("name") == "Setup Python")
                    self.assertEqual(setup["with"]["cache-dependency-path"], prefix + LOCK)
                    self.assertLess(steps.index(checkout), steps.index(setup))
                    self.assertLess(steps.index(setup), steps.index(install))

    def assert_hash_locked_requirements(self, content):
        entries = [
            line.strip()
            for line in content.replace("\\\n", "").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
        self.assertTrue(entries)
        for entry in entries:
            self.assertIsNotNone(HASHED_REQUIREMENT.fullmatch(entry), entry)

    def test_translation_lock_entries_have_exact_versions_and_hashes(self):
        self.assert_hash_locked_requirements((ROOT / LOCK).read_text())

    def test_requirements_reject_unattached_hashes_and_wildcard_versions(self):
        digest = "--hash=sha256:" + "a" * 64
        for content in (
            f"first==1.0 \\\nsecond==2.0 \\\n    {digest}\n    {digest}\n",
            f"first==1.* \\\n    {digest}\n",
        ):
            with self.subTest(content=content), self.assertRaises(AssertionError):
                self.assert_hash_locked_requirements(content)

    def test_install_rejects_security_flags_only_in_comments(self):
        command = f"python -m pip install -r {LOCK}"
        comment = "# --require-hashes --only-binary=:all:"
        for script in (f"{comment}\n{command}", f"{command} {comment}"):
            with self.subTest(script=script), self.assertRaises(AssertionError):
                self.assert_hash_locked_install(script, LOCK)


if __name__ == "__main__":
    unittest.main()
