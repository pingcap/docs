"""Check dependency pinning in GitHub Actions workflows."""

from pathlib import Path
import re
import shlex
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_DIR = ROOT / ".github/workflows"
LOCK = "scripts/ai-translator-requirements.lock"


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

    def test_translation_workflows_use_the_hash_locked_install(self):
        for name, job, prefix in (
            ("translation-cron.yml", "translate-ja", "workflow-dependencies/"),
            ("translation-zh.yaml", "translate", "workflow-dependencies/"),
            ("sync-doc-pr-zh-to-en.yml", "sync-docs", ""),
        ):
            with self.subTest(workflow=name):
                workflow = yaml.safe_load((WORKFLOW_DIR / name).read_text())
                steps = workflow["jobs"][job]["steps"]
                installs = [
                    line.strip()
                    for step in steps
                    for line in step.get("run", "").replace("\\\n", " ").splitlines()
                    if re.search(r"\bpip install\b", line)
                ]
                self.assertEqual(len(installs), 1)
                self.assertEqual(
                    shlex.split(installs[0]),
                    ["python", "-m", "pip", "install", "--require-hashes",
                     "--only-binary=:all:", "-r", prefix + LOCK],
                )
                if prefix:
                    checkout = next(step for step in steps if step.get("with", {}).get("path") == prefix.rstrip("/"))
                    self.assertEqual(checkout["with"]["ref"], "${{ github.sha }}")
                    self.assertEqual(checkout["with"]["sparse-checkout"], LOCK)

        requirements = (ROOT / LOCK).read_text().replace("\\\n", " ")
        entries = [line for line in requirements.splitlines() if line and not line.startswith("#")]
        self.assertTrue(entries)
        for entry in entries:
            self.assertRegex(entry, r"^[\w.-]+==\S+\s+--hash=sha256:[0-9a-f]{64}$")


if __name__ == "__main__":
    unittest.main()
