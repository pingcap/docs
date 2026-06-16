from __future__ import annotations

import copy
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

from .excel_workbook import get_header
from .models import PullInfo
from .utils import parse_github_url, str_value


OUT_OF_SCOPE_SHEET = "PRs_not_in_scope"
REASON_HEADER = "Reason"
SCOPE_REQUIRED_HEADERS = {"pr_status", "pr_merge_time", "pr_link"}


@dataclass(frozen=True)
class Version:
    major: int
    minor: int
    patch: int

    @property
    def release_branch(self) -> str:
        return f"release-{self.major}.{self.minor}"

    @property
    def text(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    @property
    def previous_patch_text(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch - 1}"


@dataclass(frozen=True)
class TimelineRelease:
    version: Version
    display_version: str
    release_date: date


@dataclass
class ScopeContext:
    version: Version
    releases_dir: Path
    github: Any
    base_branch_start_date: date | None = None
    timeline: list[TimelineRelease] | None = None
    release_branch_pulls: dict[str, list[PullInfo]] | None = None

    def __post_init__(self) -> None:
        if self.timeline is None:
            self.timeline = parse_release_timeline(self.releases_dir / "release-timeline.md")
        if self.release_branch_pulls is None:
            self.release_branch_pulls = {}


def move_prs_not_in_scope(
    workbook: Any,
    sheet: Any,
    version: str,
    releases_dir: Path,
    github: Any,
    base_branch_start_date: date | None = None,
    target_sheet_name: str = OUT_OF_SCOPE_SHEET,
) -> int:
    header = get_header(sheet)
    missing = sorted(SCOPE_REQUIRED_HEADERS - set(header))
    if missing:
        raise ValueError(
            "Missing required Excel columns for scope preprocessing: "
            + ", ".join(missing)
        )

    context = ScopeContext(
        version=parse_version(version),
        releases_dir=releases_dir,
        github=github,
        base_branch_start_date=base_branch_start_date,
    )
    target = ensure_out_of_scope_sheet(workbook, sheet, target_sheet_name)

    rows_to_move: list[tuple[int, str]] = []
    for row_number in range(2, sheet.max_row + 1):
        reason = out_of_scope_reason(sheet, header, row_number, context)
        if reason:
            rows_to_move.append((row_number, reason))

    for row_number, reason in rows_to_move:
        append_row_with_reason(sheet, target, row_number, reason)

    for row_number, _reason in reversed(rows_to_move):
        sheet.delete_rows(row_number, 1)

    if rows_to_move:
        print(
            f"Moved {len(rows_to_move)} row(s) to {target_sheet_name} before release-note generation",
            flush=True,
        )
    return len(rows_to_move)


def ensure_out_of_scope_sheet(workbook: Any, source_sheet: Any, target_sheet_name: str) -> Any:
    if target_sheet_name in workbook.sheetnames:
        target = workbook[target_sheet_name]
        if target.max_row == 0 or not target.cell(row=1, column=1).value:
            copy_header(source_sheet, target)
        else:
            ensure_reason_header(source_sheet, target)
        return target

    target = workbook.create_sheet(target_sheet_name)
    copy_header(source_sheet, target)
    return target


def copy_header(source_sheet: Any, target_sheet: Any) -> None:
    for column in range(1, source_sheet.max_column + 1):
        copy_cell(source_sheet.cell(row=1, column=column), target_sheet.cell(row=1, column=column))
    ensure_reason_header(source_sheet, target_sheet)


def ensure_reason_header(source_sheet: Any, target_sheet: Any) -> None:
    target_sheet.cell(row=1, column=source_sheet.max_column + 1, value=REASON_HEADER)


def append_row_with_reason(source_sheet: Any, target_sheet: Any, row_number: int, reason: str) -> None:
    target_row = target_sheet.max_row + 1
    for column in range(1, source_sheet.max_column + 1):
        copy_cell(
            source_sheet.cell(row=row_number, column=column),
            target_sheet.cell(row=target_row, column=column),
        )
    target_sheet.cell(row=target_row, column=source_sheet.max_column + 1, value=reason)


def copy_cell(source_cell: Any, target_cell: Any) -> None:
    target_cell.value = source_cell.value
    if source_cell.has_style:
        target_cell._style = copy.copy(source_cell._style)
    if source_cell.number_format:
        target_cell.number_format = source_cell.number_format
    if source_cell.hyperlink:
        target_cell._hyperlink = copy.copy(source_cell.hyperlink)
    if source_cell.comment:
        target_cell.comment = copy.copy(source_cell.comment)


def out_of_scope_reason(
    sheet: Any,
    header: dict[str, int],
    row_number: int,
    context: ScopeContext,
) -> str | None:
    status = str_value(sheet.cell(row=row_number, column=header["pr_status"]).value).lower()
    if status != "merged":
        return f"PR status is {status or 'empty'}, not merged"

    merge_date = parse_date_value(sheet.cell(row=row_number, column=header["pr_merge_time"]).value)
    if not merge_date:
        return None

    if context.version.patch >= 1:
        previous_date = release_date_for_version(context.timeline or [], context.version.previous_patch_text)
        if not previous_date:
            raise ValueError(
                f"Cannot find release date for previous version {context.version.previous_patch_text} "
                "in releases/release-timeline.md"
            )
        if merge_date < previous_date:
            return (
                f"PR merged on {merge_date.isoformat()}, before previous release "
                f"{context.version.previous_patch_text} date {previous_date.isoformat()}"
            )
        return None

    return major_release_out_of_scope_reason(sheet, header, row_number, merge_date, context)


def major_release_out_of_scope_reason(
    sheet: Any,
    header: dict[str, int],
    row_number: int,
    merge_date: date,
    context: ScopeContext,
) -> str | None:
    latest_zero = latest_released_zero_patch(context.timeline or [], context.version.text)
    if not latest_zero:
        raise ValueError("Cannot find a previously released x.y.0 version in releases/release-timeline.md")

    if merge_date >= latest_zero.release_date:
        return None

    branch_start = context.base_branch_start_date or estimated_release_branch_start_date(context, latest_zero)
    if not branch_start:
        return None
    if merge_date < branch_start:
        return (
            f"PR merged on {merge_date.isoformat()}, before estimated {latest_zero.version.release_branch} "
            f"branch start date {branch_start.isoformat()}"
        )

    pr_link = str_value(sheet.cell(row=row_number, column=header["pr_link"]).value)
    cherry_pick = find_release_branch_cherry_pick(context, latest_zero, pr_link)
    if not cherry_pick:
        return None
    cherry_pick_date = parse_date_value(cherry_pick.merged_at)
    if cherry_pick_date and cherry_pick_date < latest_zero.release_date:
        return (
            f"Cherry-pick PR {cherry_pick.url} merged on {cherry_pick_date.isoformat()} "
            f"before {latest_zero.display_version} release date {latest_zero.release_date.isoformat()}"
        )
    return None


def estimated_release_branch_start_date(
    context: ScopeContext,
    latest_zero: TimelineRelease,
) -> date | None:
    branch_pulls = release_branch_pulls(context, latest_zero.version.release_branch)
    created_dates = [parse_date_value(pull.created_at) for pull in branch_pulls]
    created_dates = [value for value in created_dates if value]
    return min(created_dates) if created_dates else None


def find_release_branch_cherry_pick(
    context: ScopeContext,
    latest_zero: TimelineRelease,
    pr_link: str,
) -> PullInfo | None:
    try:
        owner, repo, number = parse_github_url(pr_link, "pull")
    except ValueError:
        return None
    if (owner, repo) != ("pingcap", "tidb"):
        return None

    candidates = []
    for pull in release_branch_pulls(context, latest_zero.version.release_branch):
        haystack = "\n".join([pull.title, pull.body, pull.head_ref, pull.url])
        if references_original_pr(haystack, owner, repo, number, pr_link):
            candidates.append(pull)

    merged_candidates = [
        pull for pull in candidates if parse_date_value(pull.merged_at)
    ]
    if not merged_candidates:
        return None
    return min(
        merged_candidates,
        key=lambda pull: parse_date_value(pull.merged_at) or date.max,
    )


def references_original_pr(
    text: str,
    owner: str,
    repo: str,
    number: str,
    pr_link: str,
) -> bool:
    text = text or ""
    patterns = [
        re.escape(pr_link),
        rf"(?<![\w./-]){re.escape(owner)}/{re.escape(repo)}#{re.escape(number)}\b",
        rf"\(#{re.escape(number)}\)",
        rf"(?:^|[/_-])cherry-pick-{re.escape(number)}(?:\D|$)",
    ]
    if any(re.search(pattern, text) for pattern in patterns):
        return True

    marker = re.compile(r"\b(backport|cherry[- ]?pick|original|source|from)\b", re.I)
    same_repo_ref = re.compile(rf"(?<![\w./-])#{re.escape(number)}\b")
    return any(
        marker.search(line) and same_repo_ref.search(line)
        for line in text.splitlines()
    )


def release_branch_pulls(context: ScopeContext, branch: str) -> list[PullInfo]:
    assert context.release_branch_pulls is not None
    if branch not in context.release_branch_pulls:
        context.release_branch_pulls[branch] = context.github.list_pulls_for_base(
            "pingcap",
            "tidb",
            branch,
            state="closed",
        )
    return context.release_branch_pulls[branch]


def parse_release_timeline(path: Path) -> list[TimelineRelease]:
    releases: list[TimelineRelease] = []
    if not path.exists():
        raise FileNotFoundError(f"Cannot find release timeline: {path}")
    pattern = re.compile(
        r"\|\s*\[(?P<version>[^\]]+)\]\([^)]+\)\s*\|\s*(?P<date>\d{4}-\d{2}-\d{2})\s*\|"
    )
    for line in path.read_text(encoding="utf-8").splitlines():
        match = pattern.search(line)
        if not match:
            continue
        try:
            version = parse_version(match.group("version"))
        except ValueError:
            continue
        release_date = date.fromisoformat(match.group("date"))
        releases.append(TimelineRelease(version, match.group("version"), release_date))
    return releases


def release_date_for_version(timeline: list[TimelineRelease], version_text: str) -> date | None:
    for release in timeline:
        if release.version.text == version_text:
            return release.release_date
    return None


def latest_released_zero_patch(
    timeline: list[TimelineRelease],
    target_version_text: str,
) -> TimelineRelease | None:
    zero_patch_releases = [
        release
        for release in timeline
        if release.version.patch == 0 and release.version.text != target_version_text
    ]
    if not zero_patch_releases:
        return None
    return max(zero_patch_releases, key=lambda release: release.release_date)


def parse_version(version: str) -> Version:
    match = re.match(r"^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)", version)
    if not match:
        raise ValueError(f"Invalid TiDB version: {version}")
    return Version(
        major=int(match.group("major")),
        minor=int(match.group("minor")),
        patch=int(match.group("patch")),
    )


def parse_date_value(value: Any) -> date | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    text = str_value(value)
    if not text:
        return None
    text = text.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(text).date()
    except ValueError:
        pass
    match = re.search(r"\d{4}-\d{2}-\d{2}", text)
    if match:
        return date.fromisoformat(match.group())
    return None
