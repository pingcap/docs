#!/usr/bin/env python3
"""Apply concrete docs-cn updates from weekly code PR scan results.

This script reads the JSON produced by check_tidb_prs_and_create_docs_cn_pr.py
and directly updates matched docs files in docs-cn by appending a short
"weekly code sync" section for each impacted page.
"""

from __future__ import annotations

import argparse
import json
import pathlib
from collections import defaultdict
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


def append_section(file_path: pathlib.Path, section_title: str, lines: List[str]) -> bool:
    if not file_path.exists():
        return False

    content = file_path.read_text(encoding="utf-8")
    marker = f"<!-- weekly-code-sync: {section_title} -->"
    if marker in content:
        return False

    block = [""]
    block.append(marker)
    block.append(f"## {section_title}")
    block.append("")
    block.extend(lines)
    block.append("")
    file_path.write_text(content.rstrip() + "\n" + "\n".join(block), encoding="utf-8")
    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report-json", required=True)
    parser.add_argument("--docs-cn-dir", required=True)
    args = parser.parse_args()

    report_json = pathlib.Path(args.report_json).resolve()
    docs_cn_dir = pathlib.Path(args.docs_cn_dir).resolve()
    payload = json.loads(report_json.read_text(encoding="utf-8"))

    start = payload["time_window"]["start"][:10]
    end = payload["time_window"]["end"][:10]
    section_title = f"每周代码变更同步（{start} 到 {end}）"

    doc_to_items: Dict[str, List[Dict]] = defaultdict(list)
    for pr in payload.get("pull_requests", []):
        if not pr.get("needs_docs_update"):
            continue
        targets = resolve_target_docs(pr.get("repo", ""), pr.get("changed_files", []))
        for target in targets:
            doc_to_items[target].append(pr)

    changed_files: List[str] = []
    missing_files: List[str] = []
    for rel_path, items in sorted(doc_to_items.items()):
        abs_path = docs_cn_dir / rel_path
        lines = []
        for item in items:
            lines.append(
                f"- [{item['repo']}#{item['number']}]({item['url']}): {item['title']}"
            )
        ok = append_section(abs_path, section_title, lines)
        if ok:
            changed_files.append(rel_path)
        elif not abs_path.exists():
            missing_files.append(rel_path)

    print("Changed docs files:")
    for path in changed_files:
        print(f"- {path}")

    if missing_files:
        print("Missing mapped files:")
        for path in sorted(set(missing_files)):
            print(f"- {path}")

    summary = {
        "changed_docs_files": changed_files,
        "missing_mapped_files": sorted(set(missing_files)),
        "mapped_docs_count": len(doc_to_items),
    }
    (docs_cn_dir / "weekly-doc-sync").mkdir(parents=True, exist_ok=True)
    (docs_cn_dir / "weekly-doc-sync" / "applied-doc-updates.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
