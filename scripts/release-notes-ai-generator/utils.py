from __future__ import annotations

from typing import Any, Iterable

from .constants import (
    COMPONENT_ALIASES,
    GITHUB_ITEM_URL_RE,
    ISSUE_URL_RE,
    PR_URL_RE,
    TOOL_COMPONENTS,
    TOP_LEVEL_COMPONENTS,
)


def parse_github_url(url: str, expected_kind: str) -> tuple[str, str, str]:
    match = GITHUB_ITEM_URL_RE.search(url)
    if not match:
        raise ValueError(f"Invalid GitHub URL: {url}")
    if match.group("kind") != expected_kind:
        raise ValueError(f"Expected a GitHub {expected_kind} URL, got: {url}")
    return match.group("owner"), match.group("repo"), match.group("number")


def extract_issue_urls(text: str) -> list[str]:
    return unique_ordered(match.group() for match in ISSUE_URL_RE.finditer(text or ""))


def extract_pr_urls(text: str) -> list[str]:
    return unique_ordered(match.group() for match in PR_URL_RE.finditer(text or ""))


def replace_author_markdown(text: str, old_author: str, new_author: str) -> str:
    text = text or ""
    return text.replace(
        f"[{old_author}](https://github.com/{old_author}",
        f"[{new_author}](https://github.com/{new_author}",
    )


def normalize_component(component: str) -> str:
    cleaned = " ".join(str_value(component).split())
    if not cleaned:
        return ""
    return COMPONENT_ALIASES.get(cleaned.lower(), cleaned)


def normalize_raw_component(component: Any) -> str:
    return " ".join(str_value(component).split())


def normalized_release_component(component: str) -> str | None:
    normalized = normalize_component(component)
    if normalized in TOP_LEVEL_COMPONENTS or normalized in TOOL_COMPONENTS:
        return normalized
    return None


def split_multi_value(value: Any) -> list[str]:
    text = str_value(value)
    if not text:
        return []
    return [item.strip() for item in text.replace("\n", ",").split(",") if item.strip()]


def split_lines(value: Any) -> list[str]:
    text = str_value(value)
    if not text:
        return []
    return [line.strip() for line in text.splitlines() if line.strip()]


def unique_ordered(values: Iterable[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        cleaned = str_value(value)
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        result.append(cleaned)
    return result


def str_value(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()
