from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
IMPROVEMENTS_REFERENCE = (
    REPO_ROOT
    / ".ai"
    / "skills"
    / "write-review-translate-release-notes"
    / "references"
    / "improvements.md"
)
BUG_FIXES_REFERENCE = (
    REPO_ROOT
    / ".ai"
    / "skills"
    / "write-review-translate-release-notes"
    / "references"
    / "bug-fixes.md"
)
GENERATION_PROMPT_TEMPLATE = (
    REPO_ROOT / "scripts" / "release-notes-ai-generator" / "prompts" / "generation.md"
)

BOT_AUTHORS = {"ti-chi-bot", "ti-srebot"}
# Keep the misspelled source column name because release note excel file exports it this way.
REQUIRED_HEADERS = {
    "pr_author",
    "pr_link",
    "pr_title",
    "formated_release_note",
    "issue_type",
}
COMPONENT_HEADERS = ("component", "components")

GITHUB_ITEM_URL_RE = re.compile(
    r"https://github\.com/(?P<owner>[^/\s]+)/(?P<repo>[\w.-]+)/"
    r"(?P<kind>issues|pull)/(?P<number>\d+)"
)
ISSUE_URL_RE = re.compile(
    r"https://github\.com/(?P<owner>[^/\s]+)/(?P<repo>[\w.-]+)/issues/(?P<number>\d+)"
)
PR_URL_RE = re.compile(
    r"https://github\.com/(?P<owner>[^/\s]+)/(?P<repo>[\w.-]+)/pull/(?P<number>\d+)"
)
AUTHOR_RE = re.compile(r"@\[([^\]]+)\]")

TOP_LEVEL_COMPONENTS = ["TiDB", "TiKV", "PD", "TiFlash", "TiProxy"]
TOOL_COMPONENTS = [
    "Backup & Restore (BR)",
    "TiCDC",
    "TiDB Data Migration (DM)",
    "TiDB Lightning",
    "Dumpling",
    "TiUP",
    "TiDB Binlog",
    "sync-diff-inspector",
]
COMPONENT_ALIASES = {
    "tidb": "TiDB",
    "tikv": "TiKV",
    "pd": "PD",
    "tiflash": "TiFlash",
    "tiproxy": "TiProxy",
    "br": "Backup & Restore (BR)",
    "backup & restore": "Backup & Restore (BR)",
    "backup & restore (br)": "Backup & Restore (BR)",
    "cdc": "TiCDC",
    "ticdc": "TiCDC",
    "dm": "TiDB Data Migration (DM)",
    "tidb data migration": "TiDB Data Migration (DM)",
    "tidb data migration (dm)": "TiDB Data Migration (DM)",
    "tidb lightning": "TiDB Lightning",
    "lightning": "TiDB Lightning",
    "dumpling": "Dumpling",
    "tiup": "TiUP",
    "tidb binlog": "TiDB Binlog",
    "ng monitoring": "TiDB",
    "sync_diff": "sync-diff-inspector",
    "sync-diff-inspector": "sync-diff-inspector",
    "sync diff inspector": "sync-diff-inspector",
    "planner": "TiDB",
    "execution": "TiDB",
    "sql-infra": "TiDB",
    "transaction": "TiDB",
    "engine": "TiDB",
    "observability": "TiDB",
    "dxf": "TiDB",
    "storage": "TiDB",
    "tidb-dashboard": "TiDB",
    "tidb dashboard": "TiDB",
    "ddl": "TiDB",
    "coprocessor": "TiDB",
    "compute": "TiDB",
    "scheduling": "TiDB",
    "spm": "TiDB",
    "ng-monitoring": "TiDB",
}
