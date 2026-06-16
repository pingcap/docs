#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Generate TiDB improvements and bug fixes for release notes according to PRs and issues in a specified excel file.

Typical usage (run from the scripts/ directory):

    python3 -m release-notes-ai-generator \
        --version 8.5.7 \
        --excel /path/to/release-note-excel.xlsx \
        --releases-dir releases
        --ai-provider azure

For detailed usage and options, see release-notes-generator-readme.md in this directory.
"""

from .cli import main

raise SystemExit(main())
