from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class ExistingNote:
    url: str
    line: str
    file_name: str
    note_level: str
    authors: list[str]
    note_type: str | None
    component: str | None

    @property
    def dup_text(self) -> str:
        return f"- (dup): {self.file_name} {self.note_level} {self.line}"


@dataclasses.dataclass
class PullInfo:
    url: str
    title: str
    body: str
    author: str
    head_ref: str
    base_ref: str
    files_summary: str
    merged_at: str = ""
    created_at: str = ""


@dataclasses.dataclass
class IssueInfo:
    url: str
    title: str
    body: str
    labels: list[str]


@dataclasses.dataclass
class GeneratedNote:
    note_type: str
    release_note: str
    needs_review: bool
    reason: str


@dataclasses.dataclass
class RowContext:
    row_number: int
    component: str
    raw_component: str
    issue_type: str
    pr_title: str
    pr_authors: list[str]
    pr_urls: list[str]
    issue_urls: list[str]
    formatted_release_note: str
    issues: list[IssueInfo]
    pulls: list[PullInfo]


@dataclasses.dataclass
class RowInput:
    row_number: int
    component: str
    raw_component: str
    issue_type: str
    pr_title: str
    pr_authors: list[str]
    pr_urls: list[str]
    issue_urls: list[str]
    formatted_release_note: str


@dataclasses.dataclass
class GitHubDataCache:
    issues: dict[str, IssueInfo]
    pulls: dict[str, PullInfo]


@dataclasses.dataclass
class MarkdownEntry:
    note_type: str
    component: str
    note: str
    raw_component: str = ""


@dataclasses.dataclass
class RowGenerationResult:
    row_number: int
    component: str
    raw_component: str
    note_type: str | None
    note: str | None
    error: str | None
    needs_review: bool = False
    reason: str = ""
