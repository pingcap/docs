"""Test actor guards on write-privileged workflows that consume secrets."""

import os
import re
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]


def load_workflow(workflow_name):
    """Load a workflow without evaluating any GitHub expressions."""
    workflow_path = ROOT / ".github/workflows" / workflow_name
    return yaml.safe_load(workflow_path.read_text())


def load_job(workflow_name, job_name):
    """Load a job definition from a workflow."""
    return load_workflow(workflow_name)["jobs"][job_name]


class PrivilegedWorkflowActorTest(unittest.TestCase):
    def test_shared_authorization_allowlists_exactly_the_expected_accounts(self):
        step = load_job("authorize-privileged-workflow.yml", "authorize")["steps"][0]
        allowed_ids = re.findall(r"^\s+([0-9]+(?:\|[0-9]+)*)\) ;;$", step["run"], re.MULTILINE)
        self.assertEqual(len(allowed_ids), 1)
        self.assertCountEqual(allowed_ids[0].split("|"), ["30922556", "79440533", "47792576"])

    def test_gate_checks_current_permission_and_rerun_initiator(self):
        gate = load_job("authorize-privileged-workflow.yml", "authorize")["steps"][0]
        mock_api = """
gh() {
    case "$2" in
        */attempts/2)
            printf '{"triggering_actor":{"login":"rerunner","id":%s}}' "$RERUN_ID"
            ;;
        */collaborators/renamed/permission)
            printf '{"user":{"id":%s},"permission":"%s"}' "$API_ID" "$ROLE"
            ;;
        */collaborators/rerunner/permission)
            printf '{"user":{"id":%s},"permission":"%s"}' "$RERUN_ID" "$RERUN_ROLE"
            ;;
        *) return 1 ;;
    esac
}
"""
        cases = (
            ("authorized renamed commenter", {}, True),
            ("authorized manual dispatch", {"GITHUB_EVENT_NAME": "workflow_dispatch"}, True),
            ("authorized repository dispatch", {"GITHUB_EVENT_NAME": "repository_dispatch"}, True),
            ("unauthorized manual dispatch", {
                "GITHUB_EVENT_NAME": "workflow_dispatch", "ACTOR_ID": "42",
            }, False),
            ("unauthorized repository dispatch", {
                "GITHUB_EVENT_NAME": "repository_dispatch", "ACTOR_ID": "42",
            }, False),
            ("read-only repository dispatcher", {
                "GITHUB_EVENT_NAME": "repository_dispatch", "ROLE": "read",
            }, False),
            ("fork manual dispatch", {
                "GITHUB_EVENT_NAME": "workflow_dispatch", "GITHUB_REPOSITORY": "fork/docs-cn",
            }, False),
            ("fork repository dispatch", {
                "GITHUB_EVENT_NAME": "repository_dispatch", "GITHUB_REPOSITORY": "fork/docs-cn",
            }, False),
            ("fork scheduled run", {
                "GITHUB_EVENT_NAME": "schedule", "GITHUB_REPOSITORY": "fork/docs-cn",
            }, False),
            ("public commenter", {"ACTOR_ID": "42", "COMMENT_AUTHOR_ID": "42"}, False),
            ("read-only allowlisted account", {
                "ACTOR_ID": "47792576", "COMMENT_AUTHOR_ID": "47792576",
                "API_ID": "47792576", "ROLE": "read",
            }, False),
            ("reassigned login", {"API_ID": "42"}, False),
            ("different comment author", {"COMMENT_AUTHOR_ID": "42"}, False),
            ("non-master dispatch", {
                "GITHUB_EVENT_NAME": "workflow_dispatch", "GITHUB_REF": "refs/heads/test",
            }, False),
            ("first scheduled run", {"GITHUB_EVENT_NAME": "schedule", "ACTOR_ID": "42"}, True),
            ("non-master scheduled run", {
                "GITHUB_EVENT_NAME": "schedule", "GITHUB_REF": "refs/heads/test",
            }, False),
            ("non-master repository dispatch", {
                "GITHUB_EVENT_NAME": "repository_dispatch", "GITHUB_REF": "refs/heads/test",
            }, False),
            ("tag dispatch", {
                "GITHUB_EVENT_NAME": "workflow_dispatch", "GITHUB_REF": "refs/tags/master",
            }, False),
            ("unexpected event", {"GITHUB_EVENT_NAME": "push"}, False),
            ("authorized rerun", {"GITHUB_RUN_ATTEMPT": "2"}, True),
            ("unauthorized rerun", {"GITHUB_RUN_ATTEMPT": "2", "RERUN_ROLE": "read"}, False),
            ("original actor loses access", {"GITHUB_RUN_ATTEMPT": "2", "ROLE": "read"}, False),
            ("unauthorized scheduled rerun", {
                "GITHUB_EVENT_NAME": "schedule", "GITHUB_RUN_ATTEMPT": "2", "RERUN_ID": "42",
            }, False),
            ("unauthorized repository dispatch rerun", {
                "GITHUB_EVENT_NAME": "repository_dispatch", "GITHUB_RUN_ATTEMPT": "2",
                "RERUN_ID": "42",
            }, False),
        )
        with TemporaryDirectory() as directory:
            output = Path(directory) / "output"
            for name, overrides, allowed in cases:
                with self.subTest(case=name):
                    output.write_text("")
                    env = {
                        **os.environ,
                        "GITHUB_REPOSITORY": "pingcap/docs",
                        "GITHUB_REF": "refs/heads/master",
                        "GITHUB_EVENT_NAME": "issue_comment",
                        "GITHUB_ACTOR": "renamed",
                        "GITHUB_RUN_ID": "123",
                        "GITHUB_RUN_ATTEMPT": "1",
                        "GITHUB_OUTPUT": str(output),
                        "ACTOR_ID": "30922556",
                        "COMMENT_AUTHOR_ID": "30922556",
                        "API_ID": "30922556",
                        "ROLE": "admin",
                        "RERUN_ID": "79440533",
                        "RERUN_ROLE": "write",
                        **overrides,
                    }
                    result = subprocess.run(
                        ["bash", "-c", mock_api + gate["run"]],
                        env=env,
                        capture_output=True,
                        text=True,
                        timeout=5,
                    )
                    self.assertEqual(result.returncode == 0, allowed, result.stderr)
                    expected = f"attempt={env['GITHUB_RUN_ATTEMPT']}\n" if allowed else ""
                    self.assertEqual(output.read_text(), expected)

    def test_privileged_jobs_require_the_shared_authorization_workflow(self):
        for filename, job_name in (
            ("sync-doc-pr-zh-to-en.yml", "sync-docs"),
            ("link.yaml", "linkChecker"),
            ("keywords.yaml", "check-keywords"),
        ):
            with self.subTest(workflow=filename):
                workflow = load_workflow(filename)
                gate = workflow["jobs"]["authorize"]
                self.assertEqual(
                    gate["uses"],
                    "./.github/workflows/authorize-privileged-workflow.yml",
                )
                self.assertEqual(gate["permissions"], {"actions": "read"})
                self.assertNotIn("secrets", gate)
                self.assertEqual(workflow["jobs"][job_name]["needs"], "authorize")
                self.assertEqual(
                    workflow["jobs"][job_name]["if"],
                    "needs.authorize.outputs.attempt == github.run_attempt",
                )

    def test_keywords_uses_branch_data_without_switching_worktrees(self):
        workflow = load_workflow("keywords.yaml")
        self.assertEqual(workflow["permissions"], {})
        job = workflow["jobs"]["check-keywords"]
        self.assertEqual(job["permissions"], {"contents": "read", "issues": "write"})
        checkout = job["steps"][0]
        self.assertTrue(checkout["uses"].startswith("actions/checkout@"))
        self.assertIs(checkout["with"]["persist-credentials"], False)
        check = next(step["run"] for step in job["steps"] if step.get("id") == "check")
        self.assertIn('git show "refs/remotes/origin/${branch}:keywords.md"', check)
        self.assertIn('python3 -I ./scripts/check-keywords.py', check)
        self.assertIn('--keywords-file "$keywords_file"', check)
        self.assertNotRegex(check, r"\bgit\s+(?:checkout|switch|worktree)\b")
        self.assertNotIn("pip install", "\n".join(step.get("run", "") for step in job["steps"]))

    def test_keyword_checker_reads_the_explicit_data_file(self):
        with TemporaryDirectory() as directory:
            fixture = Path(directory)
            parser = fixture / "parser.y"
            parser.write_text('The following tokens belong to ReservedKeyword\n\tSELECT "SELECT"\n')
            branch_keywords = fixture / "release-keywords.md"
            branch_keywords.write_text("- SELECT (R)\n")
            (fixture / "keywords.md").write_text("- SELECT\n")
            command = [
                "python3", "-I", str(ROOT / "scripts/check-keywords.py"),
                "--download_from_url", "--parser_url", parser.as_uri(),
            ]
            for arguments, expected in (([], 1), (["--keywords-file", str(branch_keywords)], 0)):
                result = subprocess.run(
                    command + arguments, cwd=fixture, capture_output=True, text=True, timeout=5,
                )
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_ci_uses_read_only_repository_permissions(self):
        permissions = load_workflow("ci.yaml")["permissions"]
        self.assertEqual(permissions, {"contents": "read"})


if __name__ == "__main__":
    unittest.main()
