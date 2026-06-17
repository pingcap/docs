#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Generate TiDB improvements and bug fixes for release notes according to PRs and issues in a specified excel file.

Two-phase workflow (run from the scripts/ directory):

    # Phase 1: Process Excel, call AI, write results to Excel
    python3 -m release-notes-ai-generator generate \
        --version 8.5.7 \
        --excel /path/to/release-note-excel.xlsx \
        --releases-dir releases \
        --ai-provider azure

    # Phase 2: Export Markdown from the processed Excel
    python3 -m release-notes-ai-generator export-markdown \
        --version 8.5.7 \
        --excel /path/to/release-note-excel_processed.xlsx \
        --releases-dir releases \
        --release-date "August 14, 2025"

For detailed usage and options, see release-notes-generator-readme.md in this directory.
"""

from .cli import main

raise SystemExit(main())
