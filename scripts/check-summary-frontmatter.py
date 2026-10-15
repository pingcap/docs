#!/usr/bin/env python3

import argparse
from pathlib import Path
import sys

import yaml


SPECIAL_START_CHARS = set("-?:,[]{}#&*!|>'\"%@`")


def iter_markdown_files(paths):
    for path in paths:
        if path.is_dir():
            for markdown_file in path.rglob("*.md"):
                if ".git" not in markdown_file.parts:
                    yield markdown_file
        elif path.suffix == ".md":
            yield path


def has_special_unquoted_summary(line):
    if not line.startswith("summary:"):
        return False

    value = line[len("summary:") :].lstrip()
    if not value:
        return False

    if value[0] in ("'", '"', "|", ">"):
        return False

    first_char = value[0]
    if first_char not in SPECIAL_START_CHARS:
        return False

    if first_char in ("-", "?", ":") and len(value) > 1 and not value[1].isspace():
        return False

    return True


def check_file(path):
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        print(f"Skip non-UTF-8 file: {path}", file=sys.stderr)
        return []

    if not lines or lines[0].strip() != "---":
        return []

    issues = []
    frontmatter_end = None
    for line_number, line in enumerate(lines[1:], start=2):
        if line.strip() == "---":
            frontmatter_end = line_number - 1
            break
        if has_special_unquoted_summary(line):
            issues.append((line_number, f"quote the summary value: {line}"))

    if frontmatter_end is None:
        issues.append((1, "missing closing frontmatter delimiter"))
        return issues

    # Parse every field to catch invalid YAML beyond the summary's first character.
    try:
        yaml.safe_load("\n".join(lines[1:frontmatter_end]))
    except yaml.YAMLError as error:
        mark = getattr(error, "problem_mark", None)
        line_number = mark.line + 2 if mark is not None else 1
        problem = getattr(error, "problem", None) or str(error)
        issues.append((line_number, f"invalid YAML frontmatter: {problem}"))

    return issues


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Validate Markdown YAML frontmatter and check that summary values "
            "beginning with YAML special characters are quoted."
        )
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=[Path(".")],
        help="Markdown files or directories to check. Defaults to the current directory.",
    )
    args = parser.parse_args()

    has_issue = False
    for markdown_file in sorted(set(iter_markdown_files(args.paths))):
        for line_number, message in check_file(markdown_file):
            has_issue = True
            print(f"{markdown_file}:{line_number}: {message}")

    if has_issue:
        print(
            "\nFound invalid YAML frontmatter or unquoted special-leading summaries. "
            'Quote full values when needed, for example: summary: "Scenario: ...". '
            "Escape double quotes inside double-quoted values.",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
