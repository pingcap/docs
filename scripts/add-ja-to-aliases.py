#!/usr/bin/env python3
"""
For all .md docs in the target_doc_path (including all subdirectories),
locate the line starting with 'aliases:'. In the line, do the following:
1. Remove all aliases that not starts with '/tidb/stable/' or '/tidbcloud/'.
2. Add the '/ja' prefix to each alias that starts with '/tidb/stable/' or '/tidbcloud/'.

Example:
  Before: aliases: ['/tidb/stable/foo/','/tidb/dev/foo/','/tidbcloud/foo/','/tidb/other/foo/']
  After:  aliases: ['/ja/tidb/stable/foo/','/ja/tidbcloud/foo/']
"""

import os
import re

TARGET_DOC_PATH = "/Users/grcai/Documents/GitHub/docs"
PREFIXES_TO_ADD_JA = ("/tidb/stable/", "/tidbcloud/")


def should_keep(alias: str) -> bool:
    """Return True if the alias starts with one of the target prefixes."""
    return alias.startswith(PREFIXES_TO_ADD_JA)


def process_aliases_line(line: str) -> str:
    """Process a line starting with 'aliases:' and return the updated line.

    1. Remove aliases that don't start with a target prefix.
    2. Add '/ja' prefix to each remaining alias.
    """
    # Match: aliases: ['/path1','/path2', ...]
    match = re.match(r"^(aliases:\s*\[)(.*?)(\]\s*)$", line)
    if not match:
        return line

    prefix = match.group(1)   # 'aliases: ['
    body = match.group(2)     # the comma-separated aliases
    suffix = match.group(3)   # ']' (possibly with trailing whitespace)

    # Split individual aliases, preserving original quoting style
    aliases_raw = re.findall(r"""'[^']*'|"[^"]*"|[^,\s]+""", body)

    new_aliases = []
    for raw in aliases_raw:
        # Extract the inner value and determine the quote character
        if raw.startswith("'") and raw.endswith("'"):
            inner = raw[1:-1]
            quote = "'"
        elif raw.startswith('"') and raw.endswith('"'):
            inner = raw[1:-1]
            quote = '"'
        else:
            inner = raw
            quote = ""

        # Step 1: skip aliases that don't match the target prefixes
        if not should_keep(inner):
            continue

        # Step 2: add '/ja' prefix
        if not inner.startswith("/ja/"):
            inner = f"/ja{inner}"

        new_aliases.append(f"{quote}{inner}{quote}")

    return prefix + ",".join(new_aliases) + suffix


def process_file(filepath: str) -> bool:
    """Process a single markdown file. Returns True if the file was modified."""
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    modified = False
    new_lines = []
    for line in lines:
        if line.lstrip().startswith("aliases:"):
            new_line = process_aliases_line(line.rstrip("\n")) + "\n"
            if new_line != line:
                modified = True
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

    return modified


def main():
    modified_count = 0
    scanned_count = 0

    for root, _dirs, files in os.walk(TARGET_DOC_PATH):
        for filename in files:
            if not filename.endswith(".md"):
                continue
            filepath = os.path.join(root, filename)
            scanned_count += 1
            if process_file(filepath):
                rel_path = os.path.relpath(filepath, TARGET_DOC_PATH)
                print(f"  Modified: {rel_path}")
                modified_count += 1

    print(f"\nDone. Scanned {scanned_count} files, modified {modified_count} files.")


if __name__ == "__main__":
    main()
