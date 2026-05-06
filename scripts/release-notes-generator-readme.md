# Release notes generator

`scripts/release_notes_generate_ai.py` generates English TiDB release notes according to PRs and issues in a specified excel file.

## What it does

**Scope filtering:**

- Filters out PRs and issues that are not in the target release scope. For example, it filters out PRs that were merged before the previous patch release.
- Moves issues that already appeared in earlier notes from the same major.minor series to a separate worksheet.

**Duplicate handling:**

- Marks release notes that are already published in other series as `(dup)` and reuses the release notes for the same issue.

**Release note generation:**

- Generates English release notes using AI according to the release note draft provided in the PR, the PR description and code changes, and the issue description.
- Maps components in the workbook to the corresponding release note components.

**File output in Markdown:**

- Generates the release note file for the target release according to the release note template file.
- Add the improvements and bug fixes of each component to the corresponding sections of the release note file.

## Prerequisites

- Install Python dependencies:

    ```bash
    python3 -m pip install -r scripts/release_notes_ai/requirements.txt
    ```

- Prepare a GitHub token with access to the public repositories and set the GitHub token in the `GITHUB_TOKEN` environment variable:

    ```bash
    export GITHUB_TOKEN=<your-github-token>
    ```

- Install and log in to Codex CLI. The default `--ai-command` uses `codex exec`, so the installed Codex CLI must support `exec`, `--sandbox read-only`, `--ephemeral`, `--output-schema`, `--output-last-message`, and `-m <model>`.

## Typical usage

```bash
python3 scripts/release_notes_generate_ai.py \
    --version 8.5.7 \
    --excel /path/to/release-note-excel.xlsx \
    --releases-dir releases
```

## Option descriptions

| Option | Required | Default value | Usage example | Description |
| --- | --- | --- | --- | --- |
| `--version <tidb-version>` | Yes | None | `--version 8.5.7` | Target TiDB version. This value is used for scope filtering, existing release-note lookup, generated Markdown front matter, and the default output file name. |
| `--excel <workbook-path>` | Yes | None | `--excel /path/to/release-note-excel.xlsx` | Path to the source release note excel file. The source workbook is not overwritten. The processed workbook is written to `<original-name>_processed.xlsx`. |
| `--releases-dir <releases-dir>` | Yes | None | `--releases-dir releases` | Path to the existing English release notes directory. The script scans this directory for historical release notes and writes the generated Markdown under this directory unless `--output-release-file` is specified. |
| `--sheet <sheet-name>` | No | `pr_for_release_note` | `--sheet pr_for_release_note` | Workbook sheet to process. |
| `--ai-command <command>` | No | `codex --ask-for-approval never exec --sandbox read-only --ephemeral` | `--ai-command "codex --ask-for-approval never exec --sandbox read-only --ephemeral"` | Command used to invoke the AI generator. The prompt is passed through standard input. When the command is `codex exec`, the script also passes `--output-schema` and `--output-last-message`. |
| `--ai-model <model>` | No | `gpt-5.4` | `--ai-model gpt-5.4` | Model name passed to `codex exec` with `-m`. |
| `--involve-ai-generation <ON-or-OFF>` | No | `ON` | `--involve-ai-generation OFF` | Whether to generate non-duplicate release notes with AI. Use `ON` to invoke AI, or `OFF` to use the source `formated_release_note` values. |
| `--output-release-file <markdown-file>` | No | Conditional | `--output-release-file /path/to/release-8.5.7.md` | Write the generated Markdown to a custom path. By default, the output under `--releases-dir` is `release-<version>-updated-by-ai.md` if `release-<version>.md` already exists, otherwise `release-<version>.md`. |
| `--ai-timeout <seconds>` | No | `600` | `--ai-timeout 600` | Timeout in seconds for each AI command invocation. |
| `--ai-workers <count>` | No | `3` | `--ai-workers 3` | Number of concurrent AI command invocations. |
| `--github-workers <count>` | No | `8` | `--github-workers 8` | Number of concurrent GitHub API prefetch workers. |
| `--author-workers <count>` | No | `3` | `--author-workers 3` | Number of concurrent workers used to resolve bot-authored cherry-pick PR authors. |
| `--checkpoint-interval <count>` | No | `1` | `--checkpoint-interval 1` | Save the processed workbook after every N completed AI rows. Use `0` to disable checkpoint saves. |
| `--force-regenerate` | No | Disabled | `--force-regenerate` | Clear existing AI-generated notes in the processed workbook and generate all non-duplicate rows again. |
| `--release-date <release-date>` | No | `TBD` | `--release-date "August 14, 2025"` | Release date text for the generated Markdown header. |
| `--skip-scope-preprocess` | No | Disabled | `--skip-scope-preprocess` | Skip moving not-in-scope PR rows to the `PRs_not_in_scope` sheet. |
| `--scope-base-branch-start-date <YYYY-MM-DD>` | No | Estimated from release history | `--scope-base-branch-start-date 2025-01-01` | Override the estimated release-m.n branch start date for x.y.0 scope preprocessing. The value must use the `YYYY-MM-DD` format. |

## Generated files

- The source excel file passed to `--excel` is not overwritten.
- The processed excel file is written to `<original-name>_processed.xlsx` next to the source workbook.
- The generated Markdown file is written to `--output-release-file` when that option is specified.
- If `--output-release-file` is omitted and `release-<version>.md` already exists under `--releases-dir`, the generated Markdown file is written to `release-<version>-updated-by-ai.md`.
- If `--output-release-file` is omitted and `release-<version>.md` does not exist under `--releases-dir`, the generated Markdown file is written to `release-<version>.md`.
