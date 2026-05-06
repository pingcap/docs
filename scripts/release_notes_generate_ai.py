#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Generate TiDB improvements and bug fixes for release notes according to PRs and issues in a specified excel file.

Typical usage:

    python3 scripts/release_notes_generate_ai.py \
        --version 8.5.7 \
        --excel /path/to/release-note-excel.xlsx \
        --releases-dir releases

For detailed usage and options, see scripts/release-notes-generator-readme.md.
"""

from release_notes_ai.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
