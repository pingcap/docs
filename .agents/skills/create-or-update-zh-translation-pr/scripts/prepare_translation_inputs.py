#!/usr/bin/env python3

import argparse
import base64
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
from urllib.parse import quote


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp", ".ico"}
SKIP_PREFIXES = ("tidb-cloud/",)
SKIP_FILES = {"TOC-tidb-cloud.md"}
LABEL_EXCLUDES = (
    "size",
    "translation",
    "status",
    "first-time-contributor",
    "contribution",
    "lgtm",
    "approved",
)


def run(cmd):
    return subprocess.run(cmd, check=True, text=True, capture_output=True).stdout


def gh_api(api_path, *, headers=None):
    cmd = ["gh", "api"]
    if headers:
        for header in headers:
            cmd.extend(["-H", header])
    cmd.append(api_path)
    return run(cmd)


def normalize_pr_url(url):
    url = url.rstrip("/")
    if url.endswith("/files"):
        url = url[:-6]
    return url


def parse_pr_url(url):
    parts = normalize_pr_url(url).split("/")
    return parts[3], parts[4], parts[6]


def normalize_sha(value):
    sha = value.strip()
    if not re.fullmatch(r"[a-f0-9]{7,40}", sha):
        raise SystemExit(f"Invalid commit SHA: {value}")
    return sha


def parse_update_range(value):
    raw = value.strip()
    commit_url_match = re.fullmatch(
        r"https://github\.com/([^/\s]+)/([^/\s]+)/pull/(\d+)/commits/([a-f0-9]{7,40})/?",
        raw,
    )
    if commit_url_match:
        owner, repo, pr_number, commit_sha = commit_url_match.groups()
        return {
            "mode": "single_commit",
            "raw": raw,
            "commit_sha": normalize_sha(commit_sha),
            "source_pr_url": f"https://github.com/{owner}/{repo}/pull/{pr_number}",
        }
    if ".." in raw:
        parts = [part.strip() for part in raw.split("..", 1)]
        if len(parts) != 2 or not parts[0] or not parts[1]:
            raise SystemExit(f"Invalid commit range: {value}")
        return {
            "mode": "commit_range",
            "raw": raw,
            "base_sha": normalize_sha(parts[0]),
            "head_sha": normalize_sha(parts[1]),
        }
    return {
        "mode": "single_commit",
        "raw": raw,
        "commit_sha": normalize_sha(raw),
    }


def extract_source_pr_url_from_translation_body(body):
    line_match = re.search(r"(?im)^\s*(?:[-*]\s+)?This PR is translated from:\s*(.+)$", body or "")
    if not line_match:
        return None
    url_match = re.search(r"https://github\.com/[^/\s,]+/[^/\s,]+/pull/\d+", line_match.group(1))
    return normalize_pr_url(url_match.group(0)) if url_match else None


def encode_repo_path(path):
    return "/".join(quote(part, safe="") for part in path.split("/"))


def load_content(owner, repo, file_path, ref):
    api_path = f"repos/{owner}/{repo}/contents/{encode_repo_path(file_path)}?ref={ref}"
    try:
        data = json.loads(gh_api(api_path))
    except subprocess.CalledProcessError:
        return None
    if data.get("encoding") != "base64":
        return None
    return base64.b64decode(data["content"]).decode("utf-8")


def load_target_content(owner, repo, file_path, ref):
    return load_content(owner, repo, file_path, ref)


def parse_sections(content):
    lines = content.splitlines()
    sections = []
    current = None
    in_fence = False

    for idx, line in enumerate(lines, start=1):
        if line.strip().startswith("```") or line.strip().startswith("~~~"):
            in_fence = not in_fence

        match = None if in_fence else re.match(r"^(#{1,10})\s+(.*)$", line)
        if match:
            if current:
                sections.append(current)
            level = len(match.group(1))
            heading = match.group(2).strip()
            parent = current["path"][: max(level - 1, 0)] if current else []
            path = [heading] if level == 1 else parent + [heading]
            current = {
                "path": path,
                "start_line": idx,
                "content": [line],
            }
            continue

        if current is None:
            current = {"path": [], "start_line": 1, "content": [line]}
        else:
            current["content"].append(line)

    if current:
        sections.append(current)

    for section in sections:
        section["end_line"] = section["start_line"] + len(section["content"]) - 1
        section["text"] = "\n".join(section["content"])
        section["path_text"] = " > ".join(section["path"])

    return sections


def clean_title_for_matching(title):
    if not title:
        return ""
    title = re.sub(r"<span[^>]*>.*?</span>", "", title)
    title = re.sub(r"^#{1,10}\s*", "", title.strip())
    title = title.replace("`", "")
    return title.strip()


def is_system_variable_or_config(title):
    cleaned = clean_title_for_matching(title)
    if not cleaned:
        return False

    original_has_backticks = "`" in title
    allowed = re.match(r"^[a-zA-Z0-9_\-\.%]+$", cleaned)
    has_separator = any(ch in cleaned for ch in ("_", "-", ".", "%"))
    no_spaces = " " not in cleaned
    is_alert_rule = (
        cleaned.startswith("PD_")
        or cleaned.startswith("TiDB_")
        or cleaned.startswith("TiKV_")
        or cleaned.endswith("_alert")
        or "%" in cleaned
    )
    is_single_backticked_word = original_has_backticks and allowed and no_spaces and len(cleaned.split()) == 1
    return bool(allowed and (has_separator or is_alert_rule or is_single_backticked_word) and no_spaces)


def extract_heading_level(section):
    if not section or not section.get("content"):
        return None
    first_line = section["content"][0].strip()
    match = re.match(r"^(#{1,10})\s+\S", first_line)
    return len(match.group(1)) if match else None


def extract_source_tokens(text):
    if not text:
        return set()

    tokens = set()
    tokens.update(re.findall(r"`([^`]+)`", text))
    tokens.update(re.findall(r"/[A-Za-z0-9._/\-]+(?:\.[A-Za-z0-9]+)?", text))
    tokens.update(re.findall(r"[A-Z][A-Z0-9_.-]{2,}", text))
    tokens.update(re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_.-]{2,}\b", text))

    stop_words = {
        "the",
        "and",
        "for",
        "with",
        "from",
        "that",
        "this",
        "into",
        "when",
        "then",
        "sql",
        "zip",
        "file",
        "files",
    }
    return {token for token in tokens if token.lower() not in stop_words}


def score_section_tokens(source_tokens, target_section):
    if not source_tokens or not target_section:
        return 0
    target_text = target_section.get("text", "")
    return sum(1 for token in source_tokens if token in target_text)


def choose_same_level_by_order(source_section, source_sections, target_sections):
    level = extract_heading_level(source_section)
    if level is None:
        return None

    source_same_level = [section for section in source_sections if extract_heading_level(section) == level]
    target_same_level = [section for section in target_sections if extract_heading_level(section) == level]
    if not source_same_level or not target_same_level:
        return None

    try:
        ordinal = next(idx for idx, section in enumerate(source_same_level) if section["path_text"] == source_section["path_text"])
    except StopIteration:
        return None

    return target_same_level[min(ordinal, len(target_same_level) - 1)]


def choose_best_title_match(source_section, target_sections):
    level = extract_heading_level(source_section)
    source_leaf = source_section["path"][-1] if source_section.get("path") else ""
    source_clean = clean_title_for_matching(source_leaf)
    if not source_clean:
        return None

    candidates = []
    for target in target_sections:
        if extract_heading_level(target) != level:
            continue
        target_leaf = target["path"][-1] if target.get("path") else ""
        target_clean = clean_title_for_matching(target_leaf)
        if source_clean == target_clean:
            candidates.append(target)

    if len(candidates) == 1:
        return candidates[0]

    if len(candidates) > 1:
        source_parent = [clean_title_for_matching(part) for part in source_section.get("path", [])[:-1]]
        best = None
        best_score = -1
        for candidate in candidates:
            target_parent = [clean_title_for_matching(part) for part in candidate.get("path", [])[:-1]]
            score = 0
            for src, dst in zip(reversed(source_parent), reversed(target_parent)):
                if src == dst:
                    score += 1
                else:
                    break
            if score > best_score:
                best_score = score
                best = candidate
        return best

    if is_system_variable_or_config(source_leaf):
        source_lower = source_clean.lower()
        for target in target_sections:
            if extract_heading_level(target) != level:
                continue
            target_leaf = target["path"][-1] if target.get("path") else ""
            target_clean = clean_title_for_matching(target_leaf)
            target_lower = target_clean.lower()
            len_diff = abs(len(source_lower) - len(target_lower))
            if len_diff <= 2 and (source_lower in target_lower or target_lower in source_lower):
                return target

    return None


def match_target_section(source_section, source_sections, target_sections):
    if not source_section or not target_sections:
        return None

    level = extract_heading_level(source_section)

    if level == 1:
        for target in target_sections:
            if extract_heading_level(target) == 1:
                return target

    exact = choose_best_title_match(source_section, target_sections)
    if exact:
        return exact

    source_tokens = extract_source_tokens(source_section.get("text", ""))
    if source_tokens:
        scored = [
            (score_section_tokens(source_tokens, target), target)
            for target in target_sections
            if extract_heading_level(target) == level
        ]
        scored = [item for item in scored if item[0] > 0]
        if scored:
            scored.sort(key=lambda item: item[0], reverse=True)
            return scored[0][1]

    return choose_same_level_by_order(source_section, source_sections, target_sections)


def find_section_by_line(sections, line_no):
    for section in sections:
        if section["start_line"] <= line_no <= section["end_line"]:
            return section
    return sections[-1] if sections else None


def find_section_by_path(sections, path_text):
    for section in sections:
        if section["path_text"] == path_text:
            return section
    return None


def parse_patch_to_changes(patch):
    if not patch:
        return []

    changes = []
    old_line = 0
    new_line = 0
    block = None

    def flush():
        nonlocal block
        if not block:
            return
        old_text = "\n".join(block["old_lines"]).rstrip()
        new_text = "\n".join(block["new_lines"]).rstrip()
        action = "replace" if old_text and new_text else "delete" if old_text else "insert"
        changes.append(
            {
                "action": action,
                "old_source_excerpt": old_text,
                "new_source_excerpt": new_text,
                "old_start_line": block["old_start_line"],
                "new_start_line": block["new_start_line"],
            }
        )
        block = None

    for line in patch.splitlines():
        if line.startswith("@@"):
            flush()
            match = re.match(r"^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@", line)
            if match:
                old_line = int(match.group(1))
                new_line = int(match.group(2))
            continue

        if not line or line.startswith("\\"):
            continue

        marker = line[0]
        text = line[1:]

        if marker == " ":
            flush()
            old_line += 1
            new_line += 1
            continue

        if block is None:
            block = {
                "old_lines": [],
                "new_lines": [],
                "old_start_line": old_line,
                "new_start_line": new_line,
            }

        if marker == "-":
            block["old_lines"].append(text)
            old_line += 1
        elif marker == "+":
            block["new_lines"].append(text)
            new_line += 1

    flush()
    return [change for change in changes if change["old_source_excerpt"] or change["new_source_excerpt"]]


def build_translation_body(source_body, source_pr_url):
    body = source_body.replace(
        "https://cla-assistant.io/pingcap/docs",
        "https://cla-assistant.io/pingcap/docs-cn",
    )
    if "This PR is translated from:" in body:
        body = body.replace("This PR is translated from:", f"This PR is translated from: {source_pr_url}")
    elif body.strip():
        body = f"This PR is translated from: {source_pr_url}\n\n{body}"
    else:
        body = f"This PR is translated from: {source_pr_url}\n"

    body = re.sub(
        r"(?ims)^\*\*tips for choosing the affected version\(s\):\*\*(?:\r?\n){2}.*?(?:\r?\n){2}(?=- \[[ xX]\])",
        "",
        body,
        count=1,
    )
    return re.sub(r"\n{3,}", "\n\n", body)


def shell_quote(value):
    return shlex.quote("" if value is None else str(value))


def write_meta_env(path, meta):
    with open(path, "w", encoding="utf-8") as fh:
        for key, value in meta.items():
            fh.write(f"{key}={shell_quote(value)}\n")


def should_skip(path):
    return path in SKIP_FILES or any(path.startswith(prefix) for prefix in SKIP_PREFIXES)


def processing_strategy(file_path, status):
    lower = Path(file_path).suffix.lower()
    name = Path(file_path).name
    if lower in IMAGE_EXTENSIONS:
        return "binary-copy"
    if name == "TOC.md":
        return "toc-structure-aware"
    if name == "keywords.md":
        return "keywords-structure-aware"
    if not file_path.endswith(".md"):
        return "non-markdown"
    if status == "added":
        return "markdown-add-batched"
    if status == "removed":
        return "delete-target-file"
    return "markdown-minimal-edit"


def list_pr_files(owner, repo, pr_number):
    pages = json.loads(
        run(
            [
                "gh",
                "api",
                "--paginate",
                "--slurp",
                f"repos/{owner}/{repo}/pulls/{pr_number}/files?per_page=100",
            ]
        )
    )
    pr_files = []
    for page in pages:
        pr_files.extend(page)
    return pr_files


def list_update_files(owner, repo, update_range):
    if update_range["mode"] == "single_commit":
        commit_data = json.loads(gh_api(f"repos/{owner}/{repo}/commits/{update_range['commit_sha']}"))
        return {
            "files": commit_data.get("files", []),
            "base_sha": commit_data["parents"][0]["sha"] if commit_data.get("parents") else "",
            "head_sha": commit_data["sha"],
            "single_commit_sha": commit_data["sha"],
        }

    compare_data = json.loads(gh_api(f"repos/{owner}/{repo}/compare/{update_range['base_sha']}...{update_range['head_sha']}"))
    return {
        "files": compare_data.get("files", []),
        "base_sha": update_range["base_sha"],
        "head_sha": update_range["head_sha"],
        "single_commit_sha": "",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("create", "update"), default="create")
    parser.add_argument("--source-pr-url")
    parser.add_argument("--target-translation-pr-url")
    parser.add_argument("--source-update-range")
    parser.add_argument("--target-repo-dir", required=True)
    parser.add_argument("--workdir")
    args = parser.parse_args()

    if args.mode == "create":
        if not args.source_pr_url:
            raise SystemExit("--source-pr-url is required in create mode.")
        if args.source_update_range:
            raise SystemExit("--source-update-range is only supported in update mode.")
    else:
        if not args.target_translation_pr_url:
            raise SystemExit("--target-translation-pr-url is required in update mode.")
        if not args.source_update_range:
            raise SystemExit("--source-update-range is required in update mode.")

    source_pr_url = normalize_pr_url(args.source_pr_url) if args.source_pr_url else None
    target_translation_pr_url = (
        normalize_pr_url(args.target_translation_pr_url) if args.target_translation_pr_url else None
    )
    update_range = parse_update_range(args.source_update_range) if args.source_update_range else None
    if source_pr_url is None and update_range and update_range.get("source_pr_url"):
        source_pr_url = normalize_pr_url(update_range["source_pr_url"])

    target_pr_data = None
    if args.mode == "update":
        target_owner, target_repo, target_pr_number = parse_pr_url(target_translation_pr_url)
        target_pr_data = json.loads(gh_api(f"repos/{target_owner}/{target_repo}/pulls/{target_pr_number}"))
        if source_pr_url is None:
            source_pr_url = extract_source_pr_url_from_translation_body(target_pr_data.get("body", ""))
        if source_pr_url is None:
            raise SystemExit(
                "Could not infer the source PR URL from the target translation PR body. "
                "Add a 'This PR is translated from: <source-pr-url>' line or rerun with --source-pr-url."
            )

    source_owner, source_repo, source_pr_number = parse_pr_url(source_pr_url)

    if source_owner != "pingcap" or source_repo != "docs":
        raise SystemExit("This script currently supports pingcap/docs only.")

    target_repo_dir = Path(args.target_repo_dir).expanduser().resolve()
    workdir = Path(args.workdir).expanduser().resolve() if args.workdir else Path(
        run(["mktemp", "-d", f"{os.environ.get('TMPDIR', '/tmp')}/docs-translation.XXXXXX"]).strip()
    )
    workdir.mkdir(parents=True, exist_ok=True)

    pr_data = json.loads(gh_api(f"repos/{source_owner}/{source_repo}/pulls/{source_pr_number}"))
    if args.mode == "create" and any(label["name"] == "translation/done" for label in pr_data.get("labels", [])):
        raise SystemExit("The source PR already has translation/done.")

    my_login = json.loads(gh_api("user"))["login"]
    source_body = pr_data.get("body") or ""
    if args.mode == "create":
        pr_files = list_pr_files(source_owner, source_repo, source_pr_number)
        base_sha = pr_data["base"]["sha"]
        head_sha = pr_data["head"]["sha"]
        source_update = {
            "mode": "pull_request",
            "range": "",
            "base_sha": base_sha,
            "head_sha": head_sha,
        }
    else:
        update_files = list_update_files(source_owner, source_repo, update_range)
        pr_files = update_files["files"]
        base_sha = update_files["base_sha"]
        head_sha = update_files["head_sha"]
        source_update = {
            "mode": update_range["mode"],
            "range": update_range["raw"],
            "base_sha": base_sha,
            "head_sha": head_sha,
        }
        if update_range["mode"] == "single_commit":
            source_update["commit_sha"] = update_files["single_commit_sha"]

    translation_body = build_translation_body(source_body, source_pr_url)
    labels = sorted(
        {
            label["name"]
            for label in pr_data.get("labels", [])
            if not any(excluded in label["name"] for excluded in LABEL_EXCLUDES)
        }
        | {"translation/from-docs"}
    )

    translation_input = {
        "mode": args.mode,
        "source_pr": {
            "url": source_pr_url,
            "number": int(source_pr_number),
            "title": pr_data["title"],
            "base_branch": pr_data["base"]["ref"],
            "base_sha": pr_data["base"]["sha"],
            "head_branch": pr_data["head"]["ref"],
            "head_sha": pr_data["head"]["sha"],
        },
        "source_update": source_update,
        "files": [],
    }
    if target_pr_data is not None:
        translation_input["target_translation_pr"] = {
            "url": target_translation_pr_url,
            "number": target_pr_data["number"],
            "base_branch": target_pr_data["base"]["ref"],
            "head_branch": target_pr_data["head"]["ref"],
            "head_repo_owner": target_pr_data["head"]["repo"]["owner"]["login"],
            "head_repo_name": target_pr_data["head"]["repo"]["name"],
        }

    target_files = []
    if target_pr_data is not None:
        target_content_owner = target_pr_data["head"]["repo"]["owner"]["login"]
        target_content_repo = target_pr_data["head"]["repo"]["name"]
        target_content_ref = target_pr_data["head"]["ref"]
        new_branch_name = target_pr_data["head"]["ref"]
    else:
        target_content_owner = "pingcap"
        target_content_repo = "docs-cn"
        target_content_ref = pr_data["base"]["ref"]
        new_branch_name = f"translate/{pr_data['head']['ref']}"

    for file_info in pr_files:
        source_file = file_info["filename"]
        if should_skip(source_file):
            continue

        target_file_path = source_file
        entry = {
            "source_file": source_file,
            "target_file_path": target_file_path,
            "status": file_info["status"],
            "processing_strategy": processing_strategy(source_file, file_info["status"]),
            "patch": file_info.get("patch", ""),
            "changes": [],
        }

        if not source_file.endswith(".md"):
            translation_input["files"].append(entry)
            target_files.append(target_file_path)
            continue

        head_content = load_content(source_owner, source_repo, source_file, head_sha)
        base_content = None if file_info["status"] == "added" else load_content(source_owner, source_repo, source_file, base_sha)
        target_content = load_target_content(target_content_owner, target_content_repo, target_file_path, target_content_ref)

        head_sections = parse_sections(head_content) if head_content else []
        base_sections = parse_sections(base_content) if base_content else []
        target_sections = parse_sections(target_content) if target_content else []
        section_match_cache = {}

        for change in parse_patch_to_changes(file_info.get("patch", "")):
            lookup_line = max(change["new_start_line"], 1) if change["new_source_excerpt"] else max(change["old_start_line"], 1)
            source_section = find_section_by_line(head_sections if change["new_source_excerpt"] else base_sections, lookup_line)
            section_path = source_section["path_text"] if source_section else ""
            target_section = None
            if section_path:
                target_section = find_section_by_path(target_sections, section_path)
                if target_section is None:
                    if section_path in section_match_cache:
                        target_section = section_match_cache[section_path]
                    else:
                        target_section = match_target_section(
                            source_section,
                            head_sections if change["new_source_excerpt"] else base_sections,
                            target_sections,
                        )
                        section_match_cache[section_path] = target_section
            entry["changes"].append(
                {
                    "action": change["action"],
                    "section_path": section_path,
                    "old_source_excerpt": change["old_source_excerpt"],
                    "new_source_excerpt": change["new_source_excerpt"],
                    "source_section_excerpt": source_section["text"] if source_section else "",
                    "target_section_excerpt": target_section["text"] if target_section else "",
                }
            )

        translation_input["files"].append(entry)
        target_files.append(target_file_path)

    translation_input_json = workdir / "translation-input.json"
    translation_body_md = workdir / "translation-body.md"
    translation_labels_txt = workdir / "translation-labels.txt"
    target_files_txt = workdir / "target-files.txt"
    translation_meta_env = workdir / "translation-meta.env"

    translation_input_json.write_text(json.dumps(translation_input, ensure_ascii=False, indent=2), encoding="utf-8")
    translation_body_md.write_text(translation_body, encoding="utf-8")
    translation_labels_txt.write_text("".join(f"{label}\n" for label in labels), encoding="utf-8")
    target_files_txt.write_text("".join(f"{path}\n" for path in sorted(set(target_files))), encoding="utf-8")

    write_meta_env(
        translation_meta_env,
        {
            "MODE": args.mode,
            "SOURCE_PR_URL": source_pr_url,
            "SOURCE_OWNER": source_owner,
            "SOURCE_REPO": source_repo,
            "SOURCE_PR_NUMBER": source_pr_number,
            "SOURCE_TITLE": pr_data["title"],
            "BASE_BRANCH": pr_data["base"]["ref"],
            "BASE_SHA": base_sha,
            "HEAD_BRANCH": pr_data["head"]["ref"],
            "HEAD_SHA": head_sha,
            "MY_LOGIN": my_login,
            "TARGET_REPO_OWNER": "pingcap",
            "TARGET_REPO_NAME": "docs-cn",
            "TRANSLATION_LABEL": "translation/from-docs",
            "NEW_BRANCH_NAME": new_branch_name,
            "TARGET_TRANSLATION_PR_URL": target_translation_pr_url or "",
            "SOURCE_UPDATE_RANGE": source_update["range"],
            "SOURCE_UPDATE_MODE": source_update["mode"],
            "TARGET_REPO_DIR": str(target_repo_dir),
            "WORKDIR": str(workdir),
            "TRANSLATION_INPUT_JSON": str(translation_input_json),
            "SECTION_INFO_JSON": str(translation_input_json),
            "TARGET_FILES_TXT": str(target_files_txt),
            "TRANSLATION_BODY_MD": str(translation_body_md),
            "TRANSLATION_LABELS_TXT": str(translation_labels_txt),
        },
    )

    print(f"WORKDIR={workdir}")
    print(f"TRANSLATION_INPUT_JSON={translation_input_json}")
    print(f"TARGET_FILES_TXT={target_files_txt}")
    print(f"TRANSLATION_META_ENV={translation_meta_env}")
    print(f"NEW_BRANCH_NAME={new_branch_name}")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        if exc.stderr:
            sys.stderr.write(exc.stderr)
        raise
