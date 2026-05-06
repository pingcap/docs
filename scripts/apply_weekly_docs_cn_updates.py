#!/usr/bin/env python3
"""Apply docs-cn updates for one source PR candidate."""

from __future__ import annotations

import argparse
import json
import pathlib
from typing import Dict, List


PATH_TO_DOCS = {
    "pkg/sessionctx/variable/": ["system-variables.md"],
    "pkg/config/": ["tidb-configuration-file.md"],
    "pkg/parser/": ["sql-statements/sql-statement-overview.md"],
    "pkg/ddl/": ["ddl-introduction.md"],
    "pkg/planner/": ["sql-optimization-concepts.md"],
    "pkg/executor/": ["sql-optimization-concepts.md"],
    "br/": ["br/backup-and-restore-overview.md"],
    "lightning/": ["tidb-lightning/tidb-lightning-overview.md"],
    "dumpling/": ["dumpling-overview.md"],
}

REPO_TO_DOCS = {
    "pingcap/tiflow": ["ticdc/ticdc-overview.md"],
    "pingcap/tikv": ["tikv-overview.md"],
    "pingcap/pd": ["pd-overview.md"],
    "pingcap/tidb-binlog": ["tidb-binlog/tidb-binlog-overview.md"],
    "pingcap/tiup": ["tiup/tiup-overview.md"],
}


def resolve_target_docs(repo: str, changed_files: List[str]) -> List[str]:
    targets = set(REPO_TO_DOCS.get(repo, []))
    for file_path in changed_files:
        for prefix, docs_list in PATH_TO_DOCS.items():
            if file_path.startswith(prefix):
                targets.update(docs_list)
    return sorted(targets)


def append_pr_note(file_path: pathlib.Path, marker: str, lines: List[str]) -> bool:
    if not file_path.exists():
        return False
    content = file_path.read_text(encoding="utf-8")
    if marker in content:
        return False
    block = ["", marker, "## Weekly code sync note", ""]
    block.extend(lines)
    block.append("")
    file_path.write_text(content.rstrip() + "\n" + "\n".join(block), encoding="utf-8")
    return True


def load_candidate(report: Dict, repo: str, number: int) -> Dict:
    for pr in report.get("pull_requests", []):
        if pr.get("repo") == repo and int(pr.get("number", -1)) == number:
            return pr
    raise SystemExit(f"Candidate not found in report: {repo}#{number}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report-json", required=True)
    parser.add_argument("--docs-cn-dir", required=True)
    parser.add_argument("--source-repo", required=True)
    parser.add_argument("--source-pr-number", required=True, type=int)
    args = parser.parse_args()

    report_json = pathlib.Path(args.report_json).resolve()
    docs_cn_dir = pathlib.Path(args.docs_cn_dir).resolve()
    payload = json.loads(report_json.read_text(encoding="utf-8"))
    pr = load_candidate(payload, args.source_repo, args.source_pr_number)

    if not pr.get("needs_docs_update"):
        return

    targets = resolve_target_docs(pr.get("repo", ""), pr.get("changed_files", []))
    marker = f"<!-- weekly-code-sync: {pr['repo']}#{pr['number']} -->"
    note_lines = [
        f"- Source PR: [{pr['repo']}#{pr['number']}]({pr['url']})",
        f"- Title: {pr['title']}",
        f"- Merged at: `{pr['merged_at']}`",
        f"- Reasons: {'; '.join(pr.get('reasons', []))}",
    ]

    changed_files: List[str] = []
    missing_files: List[str] = []
    for rel_path in targets:
        abs_path = docs_cn_dir / rel_path
        changed = append_pr_note(abs_path, marker, note_lines)
        if changed:
            changed_files.append(rel_path)
        elif not abs_path.exists():
            missing_files.append(rel_path)

    out_dir = docs_cn_dir / "weekly-doc-sync"
    out_dir.mkdir(parents=True, exist_ok=True)
    summary_path = out_dir / f"applied-{pr['repo'].replace('/', '_')}-{pr['number']}.json"
    summary = {
        "source_repo": pr["repo"],
        "source_pr_number": pr["number"],
        "target_docs_files": targets,
        "changed_docs_files": changed_files,
        "missing_mapped_files": sorted(set(missing_files)),
    }
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Changed docs files for {pr['repo']}#{pr['number']}:")
    for item in changed_files:
        print(f"- {item}")


if __name__ == "__main__":
    main()
