#!/usr/bin/env python3
"""Apply docs-cn updates for one source PR candidate."""

from __future__ import annotations

import argparse
import json
import pathlib
import re
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

SECTION_PREF_CONFIG_FILE = "section-preferences.json"


def resolve_target_docs(repo: str, changed_files: List[str]) -> List[str]:
    targets = set(REPO_TO_DOCS.get(repo, []))
    for file_path in changed_files:
        for prefix, docs_list in PATH_TO_DOCS.items():
            if file_path.startswith(prefix):
                targets.update(docs_list)
    return sorted(targets)


def build_note_block(marker: str, lines: List[str]) -> List[str]:
    block = ["", marker, "## Source PR sync note", ""]
    block.extend(lines)
    block.append("")
    return block


def load_section_preferences(script_dir: pathlib.Path) -> Dict:
    config_path = script_dir / SECTION_PREF_CONFIG_FILE
    if not config_path.exists():
        return {
            "path_to_preferred_sections": {},
            "default_preferred_sections": ["Prerequisites", "Overview", "Usage", "Reference"],
        }
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    path_map = payload.get("path_to_preferred_sections", {})
    default_sections = payload.get("default_preferred_sections", ["Prerequisites", "Overview", "Usage", "Reference"])
    if not isinstance(path_map, dict):
        path_map = {}
    if not isinstance(default_sections, list):
        default_sections = ["Prerequisites", "Overview", "Usage", "Reference"]
    return {
        "path_to_preferred_sections": path_map,
        "default_preferred_sections": [str(x) for x in default_sections],
    }


def choose_preferred_sections(rel_path: str, section_prefs: Dict) -> List[str]:
    path_map = section_prefs.get("path_to_preferred_sections", {})
    default_sections = section_prefs.get("default_preferred_sections", ["Prerequisites", "Overview", "Usage", "Reference"])
    for prefix, sections in path_map.items():
        if rel_path.startswith(prefix):
            return [str(x) for x in sections]
    return [str(x) for x in default_sections]


def find_section_insert_line(content_lines: List[str], preferred_sections: List[str]) -> int:
    # Match markdown headings like "## Permissions", case-insensitive.
    heading_re = re.compile(r"^(##+)\s+(.+?)\s*$")
    candidates = []
    preferred_lower = [x.casefold() for x in preferred_sections]
    for idx, line in enumerate(content_lines):
        m = heading_re.match(line)
        if not m:
            continue
        level = len(m.group(1))
        title = m.group(2).strip().casefold()
        if title in preferred_lower:
            rank = preferred_lower.index(title)
            candidates.append((rank, level, idx))
    if not candidates:
        return -1
    # First by preferred rank, then by heading level, then by position.
    candidates.sort()
    target_idx = candidates[0][2]
    return target_idx + 1


def append_pr_note(file_path: pathlib.Path, rel_path: str, marker: str, lines: List[str], section_prefs: Dict) -> bool:
    if not file_path.exists():
        return False
    content = file_path.read_text(encoding="utf-8")
    if marker in content:
        return False
    content_lines = content.splitlines()
    block = build_note_block(marker, lines)
    insert_at = find_section_insert_line(content_lines, choose_preferred_sections(rel_path, section_prefs))
    if insert_at >= 0:
        new_lines = content_lines[:insert_at] + block + content_lines[insert_at:]
        file_path.write_text("\n".join(new_lines).rstrip() + "\n", encoding="utf-8")
        return True
    # Fallback: append to the end if no preferred section is found.
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
    script_dir = pathlib.Path(__file__).resolve().parent
    section_prefs = load_section_preferences(script_dir)
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
        changed = append_pr_note(abs_path, rel_path, marker, note_lines, section_prefs)
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
