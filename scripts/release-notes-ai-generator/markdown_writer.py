from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from .constants import TOOL_COMPONENTS, TOP_LEVEL_COMPONENTS
from .models import MarkdownEntry
from .utils import normalize_component, parse_github_url, str_value, unique_ordered


def write_release_file(
    output_file: Path,
    version: str,
    release_date: str,
    entries: list[MarkdownEntry],
) -> None:
    major_minor = ".".join(version.split(".")[:2])
    grouped = group_markdown_entries(entries)
    content: list[str] = [
        "---",
        f"title: TiDB {version} Release Notes",
        f"summary: Learn about the improvements and bug fixes in TiDB {version}.",
        "---",
        "",
        f"# TiDB {version} Release Notes",
        "",
        f"Release date: {release_date}",
        "",
        f"TiDB version: {version}",
        "",
        "Quick access: "
        f"[Quick start](https://docs.pingcap.com/tidb/v{major_minor}/quick-start-with-tidb) | "
        f"[Production deployment](https://docs.pingcap.com/tidb/v{major_minor}/production-deployment-using-tiup)",
        "",
    ]

    content.extend(render_section("## Improvements", grouped["improvement"]))
    content.append("")
    content.extend(render_section("## Bug fixes", grouped["bug_fix"]))
    content.append("")
    while content and content[-1] == "":
        content.pop()

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text("\n".join(content) + "\n", encoding="utf-8")


def duplicate_pr_report_path(release_file: Path) -> Path:
    return release_file.with_name(f"{release_file.stem}-duplicate-pr-report.md")


def write_duplicate_pr_report(
    output_file: Path,
    version: str,
    entries: list[MarkdownEntry],
) -> int:
    entries_by_pr: dict[str, list[MarkdownEntry]] = {}
    for entry in entries:
        for pr_url in unique_ordered(entry.pr_urls):
            entries_by_pr.setdefault(pr_url, []).append(entry)

    duplicates = {
        pr_url: pr_entries
        for pr_url, pr_entries in entries_by_pr.items()
        if len(pr_entries) > 1
    }
    if not duplicates:
        output_file.unlink(missing_ok=True)
        return 0

    content = [
        f"# Duplicate PR Report for TiDB {version} Release Notes",
        "",
        (
            "The following PRs are referenced by more than one release note entry. "
            "Review the entries to determine whether they should be merged or kept separate."
        ),
        "",
    ]
    for pr_url, pr_entries in duplicates.items():
        content.extend(
            [
                f"## [{pr_report_label(pr_url)}]({pr_url})",
                "",
                f"Referenced by {len(pr_entries)} release note entries:",
                "",
            ]
        )
        content.extend(note_with_metadata_markers(entry) for entry in pr_entries)
        content.append("")

    while content and content[-1] == "":
        content.pop()
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text("\n".join(content) + "\n", encoding="utf-8")
    return len(duplicates)


def pr_report_label(pr_url: str) -> str:
    try:
        owner, repo, number = parse_github_url(pr_url, "pull")
    except ValueError:
        return pr_url
    return f"{owner}/{repo}#{number}"


def group_markdown_entries(entries: list[MarkdownEntry]) -> dict[str, dict[str, list[MarkdownEntry]]]:
    grouped: dict[str, dict[str, list[MarkdownEntry]]] = {
        "improvement": defaultdict(list),
        "bug_fix": defaultdict(list),
    }
    for entry in entries:
        if entry.note_type not in grouped:
            continue
        component = normalize_component(entry.component) or "Other"
        grouped[entry.note_type][component].append(entry)
    return grouped


def render_section(title: str, entries_by_component: dict[str, list[MarkdownEntry]]) -> list[str]:
    lines = [title, ""]
    top_components = [
        component
        for component in TOP_LEVEL_COMPONENTS
        if component in entries_by_component and entries_by_component[component]
    ]
    unknown_top_components = sorted(
        component
        for component in entries_by_component
        if component not in TOP_LEVEL_COMPONENTS
        and component not in TOOL_COMPONENTS
        and entries_by_component[component]
    )
    tool_components = [
        component
        for component in TOOL_COMPONENTS
        if component in entries_by_component and entries_by_component[component]
    ]

    for component in top_components + unknown_top_components:
        lines.append(f"+ {component}")
        lines.append("")
        for entry in entries_by_component[component]:
            lines.append(f"    {note_with_metadata_markers(entry)}")
        lines.append("")

    if tool_components:
        lines.append("+ Tools")
        lines.append("")
        for component in tool_components:
            lines.append(f"    + {component}")
            lines.append("")
            for entry in entries_by_component[component]:
                lines.append(f"        {note_with_metadata_markers(entry)}")
            lines.append("")

    while lines and lines[-1] == "":
        lines.pop()
    return lines


def note_with_metadata_markers(entry: MarkdownEntry) -> str:
    note = ensure_release_note_bullet(entry.note)
    markers: list[str] = []
    raw_component = sanitize_component_marker(entry.raw_component)
    if raw_component and "<!-- component:" not in note:
        markers.append(f"<!-- component: {raw_component} -->")

    for pr_url in unique_ordered(entry.pr_urls):
        marker = f"<!-- pr: {pr_url} -->"
        if marker not in note:
            markers.append(marker)

    return " ".join([note, *markers])


def ensure_release_note_bullet(note: str) -> str:
    note = str_value(note)
    if note.startswith("- "):
        return note
    if note.startswith(("+ ", "* ")):
        return "- " + note[2:].lstrip()
    return f"- {note}"


def sanitize_component_marker(component: str) -> str:
    return " ".join(str_value(component).replace("--", "- -").split())
