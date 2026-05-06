#!/usr/bin/env python3
"""Weekly checker for merged PingCAP code PRs that might require docs updates.

This script:
1. Collects merged PRs in PingCAP source repositories during the previous
   Monday-to-Monday window in Asia/Shanghai timezone.
2. Uses lightweight heuristics to decide whether a PR likely needs docs updates.
3. Writes a markdown report and json summary for downstream CI steps.
4. Exposes outputs for GitHub Actions via GITHUB_OUTPUT.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import pathlib
import re
import urllib.error
import urllib.parse
import urllib.request
from typing import Dict, List, Pattern, Tuple


SOURCE_ORG = os.environ.get("SOURCE_ORG", "pingcap")
EXCLUDED_REPOS = {
    item.strip() for item in os.environ.get("EXCLUDED_REPOS", "pingcap/docs,pingcap/docs-cn").split(",") if item.strip()
}
OUTPUT_DIR = pathlib.Path(os.environ.get("OUTPUT_DIR", "tmp/tidb-doc-check")).resolve()
DOCS_CN_BASE_BRANCH = os.environ.get("DOCS_CN_BASE_BRANCH", "master")
TOKEN = os.environ.get("GITHUB_TOKEN", "").strip()


POSITIVE_LABELS = {
    "type/compatibility",
    "type/compatibility or feature change",
    "type/feature",
    "type/enhancement",
    "release-note",
}

NEGATIVE_LABELS = {
    "type/ci",
    "type/chore",
    "type/refactor",
    "type/test",
    "type/build",
}

POSITIVE_KEYWORDS = [
    "compatibility",
    "deprecated",
    "new feature",
    "sql",
    "syntax",
    "default value",
    "system variable",
    "configuration",
    "api",
    "planner",
    "optimizer",
    "ddl",
]

WATCH_PATH_PREFIXES = [
    "pkg/sessionctx/variable/",
    "pkg/config/",
    "pkg/parser/",
    "pkg/ddl/",
    "pkg/planner/",
    "pkg/executor/",
    "br/",
    "lightning/",
    "dumpling/",
]


def gh_api_json(url: str) -> Dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "tidb-doc-weekly-checker",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API HTTP error {exc.code} for {url}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"GitHub API network error for {url}: {exc.reason}") from exc


def list_search_results(query: str) -> List[Dict]:
    all_items: List[Dict] = []
    page = 1
    while True:
        params = urllib.parse.urlencode(
            {
                "q": query,
                "sort": "updated",
                "order": "desc",
                "per_page": 100,
                "page": page,
            }
        )
        data = gh_api_json(f"https://api.github.com/search/issues?{params}")
        items = data.get("items", [])
        if not items:
            break
        all_items.extend(items)
        if len(items) < 100:
            break
        page += 1
    return all_items


def list_source_repos(org: str) -> List[str]:
    repos: List[str] = []
    page = 1
    while True:
        url = (
            f"https://api.github.com/orgs/{org}/repos"
            f"?type=all&sort=updated&per_page=100&page={page}"
        )
        data = gh_api_json(url)
        if not data:
            break
        for repo in data:
            full_name = repo.get("full_name", "")
            if not full_name:
                continue
            if repo.get("fork", False):
                continue
            if repo.get("archived", False) or repo.get("disabled", False):
                continue
            if full_name in EXCLUDED_REPOS:
                continue
            repos.append(full_name)
        if len(data) < 100:
            break
        page += 1
    return sorted(set(repos))


def list_pr_files(repo: str, number: int) -> List[str]:
    files: List[str] = []
    page = 1
    while True:
        url = (
            f"https://api.github.com/repos/{repo}/pulls/{number}/files"
            f"?per_page=100&page={page}"
        )
        data = gh_api_json(url)
        if not data:
            break
        files.extend(item.get("filename", "") for item in data)
        if len(data) < 100:
            break
        page += 1
    return [f for f in files if f]


def weekly_window_shanghai(now_utc: dt.datetime) -> Tuple[dt.datetime, dt.datetime]:
    utc8 = dt.timezone(dt.timedelta(hours=8))
    now_sh = now_utc.astimezone(utc8)
    monday_this_week = (now_sh - dt.timedelta(days=now_sh.weekday())).date()
    end_sh = dt.datetime.combine(monday_this_week, dt.time(0, 0), tzinfo=utc8)
    start_sh = end_sh - dt.timedelta(days=7)
    return start_sh, end_sh


def format_iso8601_with_colon_offset(ts: dt.datetime) -> str:
    return ts.isoformat(timespec="seconds")


def parse_merged_at(merged_at: str) -> dt.datetime:
    if merged_at.endswith("Z"):
        merged_at = merged_at.replace("Z", "+00:00")
    return dt.datetime.fromisoformat(merged_at)


def build_keyword_patterns(keywords: List[str]) -> List[Tuple[str, Pattern[str]]]:
    patterns: List[Tuple[str, Pattern[str]]] = []
    for keyword in keywords:
        escaped = re.escape(keyword).replace(r"\ ", r"\s+")
        pattern = re.compile(rf"\b{escaped}\b")
        patterns.append((keyword, pattern))
    return patterns


KEYWORD_PATTERNS = build_keyword_patterns(POSITIVE_KEYWORDS)


def classify_pr(pr: Dict, pr_files: List[str]) -> Tuple[bool, List[str], int]:
    score = 0
    reasons: List[str] = []

    labels = {label.get("name", "").lower() for label in pr.get("labels", [])}
    title = (pr.get("title") or "").lower()
    body = (pr.get("body") or "").lower()
    text = f"{title}\n{body}"

    hit_positive_labels = sorted(POSITIVE_LABELS.intersection(labels))
    hit_negative_labels = sorted(NEGATIVE_LABELS.intersection(labels))

    if hit_positive_labels:
        score += 2
        reasons.append(f"Hit labels: {', '.join(hit_positive_labels)}")
    if hit_negative_labels and not hit_positive_labels:
        score -= 1
        reasons.append(f"Only maintenance labels: {', '.join(hit_negative_labels)}")

    kw_hits = sorted({keyword for keyword, pattern in KEYWORD_PATTERNS if pattern.search(text)})
    if kw_hits:
        score += 1
        reasons.append(f"Keyword hints: {', '.join(kw_hits[:5])}")

    path_hits = sorted(
        {
            path
            for path in pr_files
            if any(path.startswith(prefix) for prefix in WATCH_PATH_PREFIXES)
        }
    )
    if path_hits:
        score += 1
        reasons.append(f"Core behavior paths touched (count={len(path_hits)})")

    only_tests_or_tools = bool(pr_files) and all(
        path.startswith("tests/")
        or path.startswith("pkg/util/")
        or path.startswith(".github/")
        for path in pr_files
    )
    if only_tests_or_tools and not hit_positive_labels:
        score -= 1
        reasons.append("Files look test/tooling-only")

    needs_docs_update = score >= 2
    if not reasons:
        reasons.append("No clear doc-impact signal found")
    return needs_docs_update, reasons, score


def write_github_output(kv: Dict[str, str]) -> None:
    output_path = os.environ.get("GITHUB_OUTPUT", "").strip()
    if not output_path:
        return
    with open(output_path, "a", encoding="utf-8") as f:
        for k, v in kv.items():
            f.write(f"{k}={v}\n")


def main() -> None:
    if not TOKEN:
        raise SystemExit("GITHUB_TOKEN is required.")

    now_utc = dt.datetime.now(dt.timezone.utc)
    start_sh, end_sh = weekly_window_shanghai(now_utc)
    start_date = start_sh.date().isoformat()
    end_date = end_sh.date().isoformat()
    start_iso = format_iso8601_with_colon_offset(start_sh)
    end_iso = format_iso8601_with_colon_offset(end_sh)

    results: List[Dict] = []
    needs_update_prs: List[Dict] = []
    source_repos = list_source_repos(SOURCE_ORG)
    for source_repo in source_repos:
        query = f"repo:{source_repo} is:pr is:merged merged:{start_iso}..{end_iso}"
        merged_prs = list_search_results(query)
        for item in merged_prs:
            number = item["number"]
            pr_detail = gh_api_json(f"https://api.github.com/repos/{source_repo}/pulls/{number}")
            merged_at_raw = pr_detail.get("merged_at", "")
            if not merged_at_raw:
                continue
            merged_at = parse_merged_at(merged_at_raw).astimezone(start_sh.tzinfo)
            if not (start_sh <= merged_at < end_sh):
                continue
            pr_files = list_pr_files(source_repo, number)

            needs_docs_update, reasons, score = classify_pr(pr_detail, pr_files)
            row = {
                "repo": source_repo,
                "number": number,
                "title": pr_detail.get("title", ""),
                "url": pr_detail.get("html_url", ""),
                "merged_at": pr_detail.get("merged_at", ""),
                "labels": [x.get("name", "") for x in pr_detail.get("labels", [])],
                "score": score,
                "needs_docs_update": needs_docs_update,
                "reasons": reasons,
            }
            results.append(row)
            if needs_docs_update:
                needs_update_prs.append(row)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    window_tag = f"{start_date}_to_{end_date}"
    report_filename = f"tidb-weekly-doc-check-{window_tag}.md"
    json_filename = f"tidb-weekly-doc-check-{window_tag}.json"

    report_path = OUTPUT_DIR / report_filename
    json_path = OUTPUT_DIR / json_filename

    lines: List[str] = []
    lines.append("# TiDB weekly merged PR doc-impact check")
    lines.append("")
    lines.append(f"- Source org: `{SOURCE_ORG}`")
    lines.append(f"- Repositories scanned: `{len(source_repos)}`")
    lines.append(f"- Excluded repositories: `{', '.join(sorted(EXCLUDED_REPOS))}`")
    lines.append(f"- Time window (Asia/Shanghai): `{start_date} 00:00` to `{end_date} 00:00`")
    lines.append(f"- Total merged PRs found: `{len(results)}`")
    lines.append(f"- PRs judged as docs-update-needed: `{len(needs_update_prs)}`")
    lines.append("")

    if needs_update_prs:
        lines.append("## PRs that likely need docs updates")
        lines.append("")
        for pr in needs_update_prs:
            lines.append(f"### {pr['repo']}#{pr['number']} {pr['title']}")
            lines.append(f"- PR: {pr['url']}")
            lines.append(f"- Merged at: `{pr['merged_at']}`")
            lines.append(f"- Labels: `{', '.join(pr['labels']) if pr['labels'] else 'none'}`")
            lines.append(f"- Heuristic score: `{pr['score']}`")
            lines.append(f"- Reasons: {'; '.join(pr['reasons'])}")
            lines.append("")
        lines.append("## Suggested next action")
        lines.append("")
        lines.append("- Confirm each candidate PR and update matching docs pages in `pingcap/docs-cn`.")
        lines.append("- This report is heuristic-based and should be reviewed by a maintainer.")
        lines.append("")
    else:
        lines.append("## Result")
        lines.append("")
        lines.append("No PR reached the docs-update threshold in this window.")
        lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")

    json_payload = {
        "source_org": SOURCE_ORG,
        "scanned_repositories": source_repos,
        "excluded_repositories": sorted(EXCLUDED_REPOS),
        "time_window": {
            "timezone": "Asia/Shanghai",
            "start": start_sh.isoformat(),
            "end": end_sh.isoformat(),
        },
        "total_merged_prs": len(results),
        "docs_update_needed_count": len(needs_update_prs),
        "pull_requests": results,
    }
    json_path.write_text(json.dumps(json_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    branch_tag = end_date.replace("-", "")
    branch_name = f"weekly/tidb-doc-check-{branch_tag}"

    write_github_output(
        {
            "needs_update": "true" if needs_update_prs else "false",
            "report_path": str(report_path),
            "json_path": str(json_path),
            "report_filename": report_filename,
            "branch_name": branch_name,
            "docs_cn_base_branch": DOCS_CN_BASE_BRANCH,
            "window_start_date": start_date,
            "window_end_date": end_date,
        }
    )

    print(f"Report: {report_path}")
    print(f"Summary JSON: {json_path}")
    print(f"Needs update: {'yes' if needs_update_prs else 'no'}")


if __name__ == "__main__":
    main()
