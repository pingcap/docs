#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This script generates English TiDB release notes from a workbook with PR links and issue links of a specific release.

What does this script do?

 - Filter out the PRs and issues that are not in the target release scope. For example, PRs that were merged before this previous path release.
 - Move the issues that already appeared in earlier notes from the same major.minor series to a separate worksheet.
 - Mark the release notes that are already published in other series as ``(dup)`` and reuse the release notes for the same issue.
 - Generate the English release note using AI according to the release note draft provided in the PR, the description and code changes of the PR, the descriptions of the issue
 - Map components in the workbook to the corresponding release note components.
 - Generate the release note file for the target release according to the release note template file.

Typical usage:

    python3 scripts/release_notes_generate_ai.py \
        --version 8.5.7 \
        --excel /path/to/tirelease.xlsx \
        --releases-dir releases \
        --github-token-file /path/to/github-token.txt

Useful options:

    --involve-ai-generation OFF
        Skip AI generation and use the source ``formated_release_note`` values
        for non-duplicate rows.

    --force-regenerate
        Clear existing AI-generated notes in the processed workbook and generate
        them again.

    --output-release-file /path/to/release-8.5.7.md
        Write the generated Markdown to a custom path. By default, the output
        under ``--releases-dir`` is ``release-<version>-updated-by-ai.md`` if
        ``release-<version>.md`` already exists, otherwise
        ``release-<version>.md``.

Run ``python3 scripts/release_notes_generate_ai.py --help`` for the full option
list.
"""

from release_notes_ai.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
