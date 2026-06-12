from __future__ import annotations

import re
import sys
import threading
import time
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .constants import GITHUB_ITEM_URL_RE
from .models import IssueInfo, PullInfo
from .utils import parse_github_url


def create_retry_policy() -> Retry:
    return Retry(
        total=3,
        connect=3,
        read=3,
        status=3,
        backoff_factor=1,
        status_forcelist=(500, 502, 503, 504),
        allowed_methods=frozenset(["GET"]),
        respect_retry_after_header=True,
        raise_on_status=False,
    )


class GitHubClient:
    def __init__(
        self,
        token: str | None,
        max_rate_limit_retries: int = 3,
        max_rate_limit_sleep: int = 600,
    ):
        self.max_rate_limit_retries = max_rate_limit_retries
        self.max_rate_limit_sleep = max_rate_limit_sleep
        self.headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if token:
            self.headers["Authorization"] = f"Bearer {token}"
        self._thread_local = threading.local()

    def get_session(self) -> requests.Session:
        session = getattr(self._thread_local, "session", None)
        if session is None:
            session = requests.Session()
            session.headers.update(self.headers)
            adapter = HTTPAdapter(max_retries=create_retry_policy())
            session.mount("https://", adapter)
            self._thread_local.session = session
        return session

    def get_json(self, api_path: str) -> dict[str, Any]:
        data = self.get_api_json(api_path)
        if not isinstance(data, dict):
            raise ValueError(f"Expected object response from {api_path}")
        return data

    def get_api_json(self, api_path: str, params: dict[str, Any] | None = None) -> Any:
        return self.get_url_json(f"https://api.github.com{api_path}", params=params)

    def get_url_json(self, url: str, params: dict[str, Any] | None = None) -> Any:
        last_response: requests.Response | None = None
        for attempt in range(self.max_rate_limit_retries + 1):
            response = self.get_session().get(url, params=params, timeout=30)
            last_response = response
            if self.is_rate_limited(response) and attempt < self.max_rate_limit_retries:
                sleep_seconds = self.rate_limit_sleep_seconds(response, attempt)
                print(
                    "GitHub API rate limit reached; retrying in "
                    f"{sleep_seconds} seconds: {url}",
                    file=sys.stderr,
                    flush=True,
                )
                time.sleep(sleep_seconds)
                continue
            response.raise_for_status()
            return response.json()
        if last_response is not None:
            last_response.raise_for_status()
        raise RuntimeError(f"GitHub API request failed: {url}")

    def is_rate_limited(self, response: requests.Response) -> bool:
        if response.status_code == 429:
            return True
        if response.status_code != 403:
            return False
        if response.headers.get("x-ratelimit-remaining") == "0":
            return True
        message = response.text.lower()
        return "rate limit" in message or "abuse detection" in message

    def rate_limit_sleep_seconds(self, response: requests.Response, attempt: int) -> int:
        retry_after = response.headers.get("retry-after")
        if retry_after and retry_after.isdigit():
            return min(max(int(retry_after), 1), self.max_rate_limit_sleep)
        reset = response.headers.get("x-ratelimit-reset")
        if reset and reset.isdigit():
            wait_seconds = int(reset) - int(time.time()) + 5
            return min(max(wait_seconds, 1), self.max_rate_limit_sleep)
        return min(2 ** attempt, self.max_rate_limit_sleep)

    def get_pull(self, pr_url: str) -> PullInfo:
        owner, repo, number = parse_github_url(pr_url, "pull")
        pull = self.get_json(f"/repos/{owner}/{repo}/pulls/{number}")
        files_summary = self.get_pull_files_summary(owner, repo, number)
        return PullInfo(
            url=pr_url,
            title=str(pull.get("title") or ""),
            body=str(pull.get("body") or ""),
            author=str((pull.get("user") or {}).get("login") or ""),
            head_ref=str((pull.get("head") or {}).get("ref") or ""),
            base_ref=str((pull.get("base") or {}).get("ref") or ""),
            files_summary=files_summary,
            merged_at=str(pull.get("merged_at") or ""),
            created_at=str(pull.get("created_at") or ""),
        )

    def get_issue(self, issue_url: str) -> IssueInfo:
        owner, repo, number = parse_github_url(issue_url, "issues")
        issue = self.get_json(f"/repos/{owner}/{repo}/issues/{number}")
        labels = [
            str(label.get("name"))
            for label in issue.get("labels", [])
            if isinstance(label, dict) and label.get("name")
        ]
        return IssueInfo(
            url=issue_url,
            title=str(issue.get("title") or ""),
            body=str(issue.get("body") or ""),
            labels=labels,
        )

    def get_pull_files_summary(
        self,
        owner: str,
        repo: str,
        number: str,
        max_files: int = 80,
        max_patch_chars: int = 1200,
        max_total_chars: int = 60000,
    ) -> str:
        lines: list[str] = []
        page = 1
        total_chars = 0
        while len(lines) < max_files:
            files = self.get_api_json(
                f"/repos/{owner}/{repo}/pulls/{number}/files",
                params={"per_page": 100, "page": page},
            )
            if not isinstance(files, list) or not files:
                break
            for item in files:
                if len(lines) >= max_files or total_chars >= max_total_chars:
                    break
                if not isinstance(item, dict):
                    continue
                patch = str(item.get("patch") or "")
                if len(patch) > max_patch_chars:
                    patch = patch[:max_patch_chars] + "\n...[patch truncated]"
                block = "\n".join(
                    [
                        f"file: {item.get('filename', '')}",
                        f"status: {item.get('status', '')}",
                        f"additions: {item.get('additions', 0)}",
                        f"deletions: {item.get('deletions', 0)}",
                        "patch:",
                        patch,
                    ]
                )
                lines.append(block)
                total_chars += len(block)
            page += 1
        if not lines:
            return "No changed-file information is available."
        if len(lines) >= max_files:
            lines.append("...[file list truncated]")
        return "\n\n".join(lines)

    def list_pulls_for_base(
        self,
        owner: str,
        repo: str,
        base: str,
        state: str = "closed",
        max_pages: int = 10,
    ) -> list[PullInfo]:
        pulls: list[PullInfo] = []
        for page in range(1, max_pages + 1):
            data = self.get_api_json(
                f"/repos/{owner}/{repo}/pulls",
                params={
                    "state": state,
                    "base": base,
                    "sort": "created",
                    "direction": "asc",
                    "per_page": 100,
                    "page": page,
                },
            )
            if not isinstance(data, list) or not data:
                break
            for pull in data:
                if not isinstance(pull, dict):
                    continue
                pulls.append(
                    PullInfo(
                        url=str(pull.get("html_url") or ""),
                        title=str(pull.get("title") or ""),
                        body=str(pull.get("body") or ""),
                        author=str((pull.get("user") or {}).get("login") or ""),
                        head_ref=str((pull.get("head") or {}).get("ref") or ""),
                        base_ref=str((pull.get("base") or {}).get("ref") or ""),
                        files_summary="",
                        merged_at=str(pull.get("merged_at") or ""),
                        created_at=str(pull.get("created_at") or ""),
                    )
                )
            if len(data) < 100:
                break
        return pulls

    def get_original_author_for_cherry_pick(
        self, row_number: int, cp_pr_link: str, cp_pr_title: str, current_author: str
    ) -> str:
        default_owner, default_repo, _cp_number = parse_github_url(cp_pr_link, "pull")
        target_ref = find_original_pr_reference(cp_pr_title, default_owner, default_repo)
        if not target_ref:
            try:
                cp_info = self.get_pull(cp_pr_link)
                target_ref = (
                    find_original_pr_reference(cp_info.head_ref, default_owner, default_repo)
                    or find_original_pr_reference(cp_info.title, default_owner, default_repo)
                    or find_original_pr_reference(cp_info.body, default_owner, default_repo)
                )
            except Exception as exc:  # noqa: BLE001
                print(
                    f"Row {row_number}: failed to inspect cherry-pick PR "
                    f"{cp_pr_link}: {exc}",
                    file=sys.stderr,
                )
                return current_author

        if not target_ref:
            print(
                f"Row {row_number}: failed to find the original PR for "
                f"{cp_pr_link} created by {current_author}.",
                file=sys.stderr,
            )
            return current_author

        target_owner, target_repo, target_number = target_ref
        target_pr_link = f"https://github.com/{target_owner}/{target_repo}/pull/{target_number}"
        try:
            return self.get_pull(target_pr_link).author or current_author
        except Exception as exc:  # noqa: BLE001
            print(
                f"Row {row_number}: failed to find the non-bot author for "
                f"{cp_pr_link}: {exc}",
                file=sys.stderr,
            )
            return current_author


def find_original_pr_reference(
    text: str,
    default_owner: str,
    default_repo: str,
) -> tuple[str, str, str] | None:
    text = text or ""
    marker_lines = [
        line
        for line in text.splitlines()
        if re.search(r"\b(backport|cherry[- ]?pick|original|source|from)\b", line, re.I)
    ]
    for line in marker_lines:
        reference = find_pr_reference_in_text(line, default_owner, default_repo)
        if reference:
            return reference

    same_repo = re.search(r"\(#(?P<number>\d+)\)\s*$", text)
    if same_repo:
        return default_owner, default_repo, same_repo.group("number")

    branch = re.search(r"(?:^|[/_-])cherry-pick-(?P<number>\d+)(?:\D|$)", text)
    if branch:
        return default_owner, default_repo, branch.group("number")

    if "\n" not in text and len(text) <= 300:
        return find_pr_reference_in_text(text, default_owner, default_repo)

    return None


def find_pr_reference_in_text(
    text: str,
    default_owner: str,
    default_repo: str,
) -> tuple[str, str, str] | None:
    for full_url in GITHUB_ITEM_URL_RE.finditer(text or ""):
        if full_url.group("kind") == "pull":
            return full_url.group("owner"), full_url.group("repo"), full_url.group("number")

    cross_repo = re.search(
        r"(?<![\w./-])(?P<owner>[\w.-]+)/(?P<repo>[\w.-]+)#(?P<number>\d+)\b",
        text or "",
    )
    if cross_repo:
        return cross_repo.group("owner"), cross_repo.group("repo"), cross_repo.group("number")

    same_repo = re.search(r"\(#(?P<number>\d+)\)\s*$", text or "")
    if same_repo:
        return default_owner, default_repo, same_repo.group("number")

    return None
