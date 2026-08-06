from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from .constants import TOOL_COMPONENTS, TOP_LEVEL_COMPONENTS
from .models import MarkdownEntry
from .utils import normalize_component, str_value


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
            lines.append(f"    {note_with_component_marker(entry)}")
        lines.append("")

    if tool_components:
        lines.append("+ Tools")
        lines.append("")
        for component in tool_components:
            lines.append(f"    + {component}")
            lines.append("")
            for entry in entries_by_component[component]:
                lines.append(f"        {note_with_component_marker(entry)}")
            lines.append("")

    while lines and lines[-1] == "":
        lines.pop()
    return lines


def note_with_component_marker(entry: MarkdownEntry) -> str:
    note = ensure_release_note_bullet(entry.note)
    raw_component = sanitize_component_marker(entry.raw_component)
    if not raw_component or "<!-- component:" in note:
        return note
    return f"{note} <!-- component: {raw_component} -->"


def ensure_release_note_bullet(note: str) -> str:
    note = str_value(note)
    if note.startswith("- "):
        return note
    if note.startswith(("+ ", "* ")):
        return "- " + note[2:].lstrip()
    return f"- {note}"


def sanitize_component_marker(component: str) -> str:
    return " ".join(str_value(component).replace("--", "- -").split())
