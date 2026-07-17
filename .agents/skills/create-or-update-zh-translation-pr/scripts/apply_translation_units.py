#!/usr/bin/env python3

import argparse
import json
import re
import shlex
from pathlib import Path


def parse_meta_env(path):
    meta = {}
    for raw_line in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or "=" not in line:
            continue
        key, value = line.split("=", 1)
        meta[key] = shlex.split(value)[0] if value else ""
    return meta


def parse_sections(content):
    lines = content.splitlines(keepends=True)
    sections = []
    current = None
    in_fence = False

    for idx, raw_line in enumerate(lines, start=1):
        stripped = raw_line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence

        match = None if in_fence else re.match(r"^(#{1,10})\s+(.*)$", raw_line.rstrip("\n"))
        if match:
            if current:
                current["end_line"] = idx - 1
                current["text"] = "".join(current["content"])
                current["path_text"] = " > ".join(current["path"])
                sections.append(current)
            level = len(match.group(1))
            title = match.group(2).strip()
            parent = current["path"][: max(level - 1, 0)] if current else []
            path = [title] if level == 1 else parent + [title]
            current = {"path": path, "start_line": idx, "content": [raw_line]}
            continue

        if current is None:
            current = {"path": [], "start_line": 1, "content": [raw_line]}
        else:
            current["content"].append(raw_line)

    if current:
        current["end_line"] = len(lines)
        current["text"] = "".join(current["content"])
        current["path_text"] = " > ".join(current["path"])
        sections.append(current)

    return sections


def is_code_like_line(line):
    stripped = line.strip()
    if not stripped:
        return True
    if stripped.startswith(("```", "~~~", "{{<", "{{%", "|", "+---", "http://", "https://", "mysql>")):
        return True
    if re.fullmatch(r"[`~*_\-+=[\](){}<>:;\\/|,.!?'\"A-Za-z0-9% ]+", stripped) is None:
        return False

    alpha_words = re.findall(r"[A-Za-z]+", stripped)
    has_command_markers = any(
        token in stripped
        for token in (";", "`", "/", "::", "(", ")", "${", "@@", "_", ".md", ".txt", ".sql")
    )
    starts_with_command = bool(
        re.match(
            r"^(PLAN|SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP|EXPLAIN|SHOW|SET|USE|ANALYZE|curl|mysql>|http)",
            stripped,
            re.IGNORECASE,
        )
    )
    mostly_upper = stripped.upper() == stripped and bool(alpha_words)
    return has_command_markers or starts_with_command or mostly_upper or len(alpha_words) <= 3


def is_literal_safe_block(text):
    lines = [line for line in text.splitlines() if line.strip()]
    return bool(lines) and all(is_code_like_line(line) for line in lines)


def build_line_offsets(text):
    offsets = [0]
    total = 0
    for line in text.splitlines(keepends=True):
        total += len(line)
        offsets.append(total)
    return offsets


def find_block_span(section_text, block_text):
    start = section_text.find(block_text)
    if start == -1:
        return None
    return start, start + len(block_text)


def surrounding_literal_anchors(source_section_text, block_text):
    span = find_block_span(source_section_text, block_text)
    if span is None:
        return None, None

    start, end = span
    source_lines = source_section_text.splitlines(keepends=True)
    offsets = build_line_offsets(source_section_text)

    start_line = 0
    end_line = 0
    for idx in range(len(offsets) - 1):
        if offsets[idx] <= start < offsets[idx + 1]:
            start_line = idx
        if offsets[idx] < end <= offsets[idx + 1]:
            end_line = idx
            break

    prev_anchor = None
    next_anchor = None

    for idx in range(start_line - 1, -1, -1):
        candidate = source_lines[idx].strip()
        if candidate and is_code_like_line(candidate):
            prev_anchor = source_lines[idx]
            break

    for idx in range(end_line + 1, len(source_lines)):
        candidate = source_lines[idx].strip()
        if candidate and is_code_like_line(candidate):
            next_anchor = source_lines[idx]
            break

    return prev_anchor, next_anchor


def apply_insert_by_anchor(section_text, source_section_text, new_text):
    if new_text in section_text or not is_literal_safe_block(new_text):
        return None, "already-present-or-non-literal"

    prev_anchor, next_anchor = surrounding_literal_anchors(source_section_text, new_text)

    if prev_anchor and section_text.count(prev_anchor) == 1:
        anchor_index = section_text.find(prev_anchor) + len(prev_anchor)
        insertion = new_text
        if not insertion.endswith("\n"):
            insertion += "\n"
        return section_text[:anchor_index] + insertion + section_text[anchor_index:], "insert-after-anchor"

    if next_anchor and section_text.count(next_anchor) == 1:
        anchor_index = section_text.find(next_anchor)
        insertion = new_text
        if not insertion.endswith("\n"):
            insertion += "\n"
        return section_text[:anchor_index] + insertion + section_text[anchor_index:], "insert-before-anchor"

    return None, "no-unique-anchor"


def extract_token_replacements(old_text, new_text):
    replacements = []
    old_links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", old_text or "")
    new_links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", new_text or "")
    for old_label, old_url in old_links:
        for new_label, new_url in new_links:
            if old_url == new_url and old_label != new_label:
                replacements.append((old_label, new_label))

    old_tokens = re.findall(r"`([^`\n]+)`", old_text or "")
    new_tokens = re.findall(r"`([^`\n]+)`", new_text or "")
    if len(old_tokens) == len(new_tokens):
        for old_token, new_token in zip(old_tokens, new_tokens):
            if old_token != new_token and re.fullmatch(r"[A-Za-z0-9_./:-]+(?: [A-Z][A-Z0-9_./:-]+){0,3}", old_token) and re.fullmatch(r"[A-Za-z0-9_./:-]+(?: [A-Z][A-Z0-9_./:-]+){0,3}", new_token):
                replacements.append((old_token, new_token))

    old_paths = re.findall(r"/[A-Za-z0-9._/\-]+", old_text or "")
    new_paths = re.findall(r"/[A-Za-z0-9._/\-]+", new_text or "")
    if len(old_paths) == len(new_paths):
        for old_path, new_path in zip(old_paths, new_paths):
            if old_path != new_path:
                replacements.append((old_path, new_path))

    deduped = []
    seen = set()
    for old_value, new_value in replacements:
        if old_value and new_value and old_value != new_value and (old_value, new_value) not in seen:
            deduped.append((old_value, new_value))
            seen.add((old_value, new_value))
    return deduped


def apply_replace(section_text, old_text, new_text):
    if old_text and new_text and old_text in section_text and is_literal_safe_block(old_text) and is_literal_safe_block(new_text):
        return section_text.replace(old_text, new_text, 1), "replace-literal-block"

    updated = section_text
    applied = False
    for old_value, new_value in extract_token_replacements(old_text, new_text):
        if old_value in updated:
            updated = updated.replace(old_value, new_value)
            applied = True

    if applied:
        return updated, "replace-token"

    return None, "non-literal-replace"


def splice_section(full_text, section, new_section_text):
    lines = full_text.splitlines(keepends=True)
    start = section["start_line"] - 1
    end = section["end_line"]
    new_lines = new_section_text.splitlines(keepends=True)
    return "".join(lines[:start] + new_lines + lines[end:])


def normalize_block(text):
    return (text or "").strip().replace("\r\n", "\n")


def find_section_by_heading_line(target_excerpt, sections):
    first_heading = next(
        (line.strip() for line in (target_excerpt or "").splitlines() if re.match(r"^#{1,10}\s+\S", line)),
        "",
    )
    if not first_heading:
        return None
    matches = [candidate for candidate in sections if candidate["text"].lstrip().startswith(first_heading)]
    return matches[0] if len(matches) == 1 else None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--meta-env", required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    meta = parse_meta_env(args.meta_env)
    translation_input_path = Path(meta["TRANSLATION_INPUT_JSON"])
    target_repo_dir = Path(meta["TARGET_REPO_DIR"])
    workdir = Path(meta["WORKDIR"])
    report_path = workdir / "translation-apply-report.json"

    translation_input = json.loads(translation_input_path.read_text(encoding="utf-8"))
    report = {"files": [], "summary": {"applied_changes": 0, "pending_changes": 0, "modified_files": 0}}

    for file_entry in translation_input.get("files", []):
        if file_entry.get("processing_strategy") != "markdown-minimal-edit":
            continue

        target_path = target_repo_dir / file_entry["target_file_path"]
        if not target_path.exists():
            continue

        original_text = target_path.read_text(encoding="utf-8")
        current_text = original_text
        file_report = {"target_file_path": file_entry["target_file_path"], "applied": [], "pending": []}

        for index, change in enumerate(file_entry.get("changes", []), start=1):
            sections = parse_sections(current_text)
            section = None

            target_excerpt = change.get("target_section_excerpt") or ""
            if target_excerpt:
                for candidate in sections:
                    candidate_text = normalize_block(candidate["text"])
                    target_text = normalize_block(target_excerpt)
                    if (
                        candidate_text == target_text
                        or target_text in candidate_text
                        or candidate_text in target_text
                    ):
                        section = candidate
                        break

            if section is None:
                section = find_section_by_heading_line(target_excerpt, sections)

            if section is None:
                file_report["pending"].append({"change_index": index, "reason": "target-section-not-found"})
                report["summary"]["pending_changes"] += 1
                continue

            updated_section_text = None
            reason = ""
            action = change.get("action")
            old_text = change.get("old_source_excerpt") or ""
            new_text = change.get("new_source_excerpt") or ""
            source_section_text = change.get("source_section_excerpt") or ""

            if action == "insert":
                updated_section_text, reason = apply_insert_by_anchor(section["text"], source_section_text, new_text)
            elif action == "replace":
                updated_section_text, reason = apply_replace(section["text"], old_text, new_text)
            else:
                reason = "unsupported-action"

            if updated_section_text is None or updated_section_text == section["text"]:
                file_report["pending"].append({"change_index": index, "reason": reason})
                report["summary"]["pending_changes"] += 1
                continue

            current_text = splice_section(current_text, section, updated_section_text)
            file_report["applied"].append({"change_index": index, "reason": reason})
            report["summary"]["applied_changes"] += 1

        if current_text != original_text:
            report["summary"]["modified_files"] += 1
            if args.write:
                target_path.write_text(current_text, encoding="utf-8")

        if file_report["applied"] or file_report["pending"]:
            report["files"].append(file_report)

    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"TRANSLATION_APPLY_REPORT={report_path}")
    print(json.dumps(report["summary"], ensure_ascii=False))


if __name__ == "__main__":
    main()
