#!/usr/bin/env python3
"""Validate TiDB docs RelatedResources blocks."""

from __future__ import annotations

import argparse
import re
import sys
import urllib.parse
from pathlib import Path


HEADING_RE = re.compile(r"^## (Related resources|相关资源|関連リソース(?: \{#related-resources\})?)$")
CARD_RE = re.compile(r'^  <ResourceCard (.+) />$')
ATTR_RE = re.compile(r'([A-Za-z][A-Za-z0-9]*)="([^"]*)"')
YOUTUBE_RE = re.compile(r"https://i\.ytimg\.com/vi/([^/]+)/hqdefault\.jpg$")


def language_from_heading(heading: str) -> str:
    if heading == "## Related resources":
        return "en"
    if heading == "## 相关资源":
        return "zh"
    if heading == "## 関連リソース {#related-resources}":
        return "ja"
    return "unknown"


def youtube_id(url: str) -> str | None:
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc.endswith("youtu.be"):
        return parsed.path.strip("/").split("/")[0] or None
    if "youtube.com" in parsed.netloc:
        values = urllib.parse.parse_qs(parsed.query).get("v")
        return values[0] if values else None
    return None


def parse_attrs(raw: str) -> tuple[dict[str, str], list[str]]:
    attrs: dict[str, str] = {}
    errors: list[str] = []
    consumed = ""
    for match in ATTR_RE.finditer(raw):
        key, value = match.groups()
        attrs[key] = value
        consumed += match.group(0) + " "
    if consumed.strip() != raw.strip():
        errors.append("card has malformed attributes or non-double-quoted values")
    return attrs, errors


def validate_file(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    errors: list[str] = []
    headings = [(index, line) for index, line in enumerate(lines) if HEADING_RE.match(line)]

    if len(headings) > 1:
        errors.append("has multiple Related resources headings")

    for start, heading in headings:
        lang = language_from_heading(heading)
        if heading == "## 関連リソース":
            errors.append(f"line {start + 1}: Japanese heading must include {{#related-resources}}")

        if start + 1 >= len(lines) or lines[start + 1] != "":
            errors.append(f"line {start + 1}: heading must be followed by one blank line")
        if start > 0 and lines[start - 1] != "":
            errors.append(f"line {start + 1}: heading must be preceded by one blank line")
        if start + 2 >= len(lines) or lines[start + 2] != "<RelatedResources>":
            errors.append(f"line {start + 3}: expected <RelatedResources>")
            continue

        end = None
        for index in range(start + 3, len(lines)):
            if lines[index] == "</RelatedResources>":
                end = index
                break
        if end is None:
            errors.append(f"line {start + 3}: missing </RelatedResources>")
            continue
        if end == start + 3:
            errors.append(f"line {start + 3}: RelatedResources block has no cards")

        for index in range(start + 3, end):
            line = lines[index]
            if line == "":
                errors.append(f"line {index + 1}: blank lines are not allowed inside RelatedResources")
                continue
            if "<ResourceCard" in line and not CARD_RE.match(line):
                errors.append(f"line {index + 1}: ResourceCard must be one line, indented two spaces, and self-closed with a space before />")
                continue
            match = CARD_RE.match(line)
            if not match:
                errors.append(f"line {index + 1}: unexpected content inside RelatedResources")
                continue

            attrs, attr_errors = parse_attrs(match.group(1))
            for attr_error in attr_errors:
                errors.append(f"line {index + 1}: {attr_error}")

            for key in ("title", "type", "link", "imgSrc"):
                if not attrs.get(key):
                    errors.append(f"line {index + 1}: missing required attribute {key}")

            if attrs.get("type") not in {"blog", "video", "lab"}:
                errors.append(f"line {index + 1}: type must be blog, video, or lab")

            date = attrs.get("date")
            if date and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
                errors.append(f"line {index + 1}: date must be YYYY-MM-DD")

            duration = attrs.get("duration")
            if duration:
                if lang == "en" and not re.fullmatch(r"\d+ mins", duration):
                    errors.append(f"line {index + 1}: English duration must look like '8 mins'")
                if lang == "zh" and not re.fullmatch(r"\d+ 分钟", duration):
                    errors.append(f"line {index + 1}: Chinese duration must look like '8 分钟'")
                if lang == "ja" and not re.fullmatch(r"\d+ 分", duration):
                    errors.append(f"line {index + 1}: Japanese duration must look like '8 分'")

            if attrs.get("type") == "video":
                link_id = youtube_id(attrs.get("link", ""))
                image_match = YOUTUBE_RE.fullmatch(attrs.get("imgSrc", ""))
                image_id = image_match.group(1) if image_match else None
                if not image_id:
                    errors.append(f"line {index + 1}: YouTube imgSrc must be https://i.ytimg.com/vi/<ID>/hqdefault.jpg")
                if link_id and image_id and link_id != image_id:
                    errors.append(f"line {index + 1}: YouTube link ID and imgSrc ID do not match")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+")
    args = parser.parse_args()

    all_errors: list[str] = []
    for filename in args.files:
        path = Path(filename)
        errors = validate_file(path)
        all_errors.extend(f"{path}: {error}" for error in errors)

    if all_errors:
        for error in all_errors:
            print(error, file=sys.stderr)
        return 1

    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
