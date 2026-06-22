# Readme: Release Notes AI Generator

`python3 -m release-notes-ai-generator` (run from the `scripts/` directory) generates English TiDB release notes for the `Improvements` and `Bug fixes` sections according to PRs and issues in an Excel workbook.

The generator uses a two-phase workflow:

1. **`generate`** (Phase 1): Processes the source Excel workbook — runs preprocessing, calls AI to generate release notes, and writes results back to Excel. Supports row-range arguments (`--start-row` / `--end-row`) for resuming after interruptions.
2. **`export-markdown`** (Phase 2): Reads the processed Excel and exports a Markdown release note file. Does not call AI or modify the Excel.

The source workbook is never overwritten. All processing results are written to a processed workbook (`<original-name>_processed.xlsx`).

## What it does

**Scope filtering**

- Filters out rows of PRs and issues that are not in the target release scope.
- Moves issues that already appeared in earlier release notes from the same major.minor series to a separate worksheet for review.

**Author correction**

- Resolves bot-authored cherry-pick rows to the original PR author when possible.

**Duplicate handling**

- Reuses already-published release note entries as `(dup)` entries when appropriate.

**Release note generation**

- Generates English release notes with AI from workbook data, GitHub PR and issue context, changed-file summaries, and repo-local release note writing references.

**Component mapping**

- Maps workbook components to the corresponding release note Markdown components.

**Markdown generation**

- Writes `Improvements` and `Bug fixes` entries to a Markdown release note draft.

The generator does not create a complete formal release note. It does not generate sections such as compatibility changes, known issues, deprecations, or upgrade notes.

## Prerequisites

- Install Python dependencies:

    ```bash
    python3 -m pip install -r scripts/release-notes-ai-generator/requirements.txt
    ```

- Prepare a GitHub token with access to the public repositories and set the GitHub token in the `GITHUB_TOKEN` environment variable:

    ```bash
    export GITHUB_TOKEN=<your-github-token>
    ```

- Prepare the AI settings in your environment.

    - If you use `--ai-provider azure` instead, set the following environment variables:

    ```bash
    export AZURE_OPENAI_KEY=<your-key>
    export AZURE_OPENAI_BASE_URL=<your-endpoint>
    ```

    - If you use Codex CLI, install and log in to Codex CLI. The default `--ai-command` uses `codex exec`, so the installed Codex CLI must support `exec`, `--sandbox read-only`, `--ephemeral`, `--output-schema`, `--output-last-message`, and `-m <model>`.

## Typical usage examples

The generator uses two subcommands that run independently:

- `generate` (Phase 1): processes the Excel workbook, calls AI, writes results back to Excel.
- `export-markdown` (Phase 2): reads the processed Excel and outputs a Markdown file.

### Phase 1: Generate release notes into Excel

Use Azure OpenAI:

```bash
cd scripts
python3 -m release-notes-ai-generator generate \
    --version 8.5.7 \
    --excel </path/to/release-note-excel.xlsx> \
    --releases-dir </path/to/releases-folder> \
    --ai-provider azure
```

Use Codex CLI:

```bash
cd scripts
python3 -m release-notes-ai-generator generate \
    --version 8.5.7 \
    --excel /path/to/release-note-excel.xlsx \
    --releases-dir </path/to/releases-folder>
```

### Phase 1: Resume from interruption

If the first run is interrupted (e.g. API quota exhausted), resume from where it left off using `--start-row`:

```bash
cd scripts
python3 -m release-notes-ai-generator generate \
    --version 8.5.7 \
    --excel /path/to/release-note-excel_processed.xlsx \
    --releases-dir ../releases \
    --ai-provider azure \
    --start-row 51
```

You can also limit to a specific range with `--end-row`:

```bash
python3 -m release-notes-ai-generator generate \
    --version 8.5.7 \
    --excel /path/to/release-note-excel_processed.xlsx \
    --releases-dir ../releases \
    --ai-provider azure \
    --start-row 51 --end-row 100
```

When `--start-row` or `--end-row` is specified, preprocessing steps (sort, merge, scope filter, same-series move) are skipped because they were completed in the first run.

### Phase 2: Export Markdown from processed Excel

After Phase 1 is fully complete, export the Markdown:

```bash
cd scripts
python3 -m release-notes-ai-generator export-markdown \
    --version <tidb-version, for example 8.5.7> \
    --excel </path/to/release-note-excel_processed.xlsx> \
    --releases-dir </path/to/releases-folder> \
    --release-date "<release date>"
```

## Option descriptions

### `generate` subcommand options

| Option | Required | Default value | Description |
| --- | --- | --- | --- |
| `--version <tidb-version>` | Yes | None | Target TiDB version. Used for scope filtering, existing release-note lookup, and the default output file name. |
| `--excel <workbook-path>` | Yes | None | Path to the source release note Excel file. The source workbook is not overwritten. The processed workbook is written to `<original-name>_processed.xlsx` (or the path specified by `--output-excel`). |
| `--releases-dir <releases-dir>` | Yes | None | Path to the existing English release notes directory. Used for historical release note scanning and scope filtering. |
| `--sheet <sheet-name>` | No | `pr_for_release_note` | Workbook sheet to process. |
| `--ai-provider <provider>` | No | `codex` | AI provider to use. `codex` runs the Codex CLI as a subprocess. `azure` calls Azure OpenAI via the OpenAI Python SDK. |
| `--ai-command <command>` | No | `codex --ask-for-approval never exec --sandbox read-only --ephemeral` | Command used to invoke the AI generator (only used with `--ai-provider codex`). |
| `--ai-model <model>` | No | `gpt-5.4` | Model name. Passed to `codex exec` with `-m`, or used as the model parameter for Azure OpenAI. |
| `--involve-ai-generation <ON\|OFF>` | No | `ON` | Whether to generate non-duplicate release notes with AI. Use `OFF` to skip AI generation and only run preprocessing. |
| `--ai-timeout <seconds>` | No | `600` | Timeout in seconds for each AI command invocation. |
| `--ai-workers <count>` | No | `3` | Number of concurrent AI command invocations. |
| `--github-workers <count>` | No | `8` | Number of concurrent GitHub API prefetch workers. |
| `--author-workers <count>` | No | `3` | Number of concurrent workers used to resolve bot-authored cherry-pick PR authors. |
| `--checkpoint-interval <count>` | No | `1` | Save the processed workbook after every N completed AI rows. Use `0` to disable. |
| `--force-regenerate` | No | Disabled | Clear existing AI-generated notes and regenerate all non-duplicate rows. |
| `--skip-scope-preprocess` | No | Disabled | Skip moving not-in-scope PR rows to the `PRs_not_in_scope` sheet. |
| `--scope-base-branch-start-date <YYYY-MM-DD>` | No | Estimated from release history | Override the estimated release-m.n branch start date for x.y.0 scope preprocessing. |
| `--start-row <row>` | No | First data row | Excel row number to start processing from (1-indexed, row 1 is the header). When specified, preprocessing steps are skipped. Use this to resume after an interruption. |
| `--end-row <row>` | No | Last row | Excel row number to stop processing at (inclusive, 1-indexed). |
| `--output-excel <path>` | No | `<original-name>_processed.xlsx` | Path for the processed Excel output. |

### `export-markdown` subcommand options

| Option | Required | Default value | Description |
| --- | --- | --- | --- |
| `--version <tidb-version>` | Yes | None | Target TiDB version. Used for the Markdown front matter and default output file name. |
| `--excel <workbook-path>` | Yes | None | Path to the processed Excel workbook (output of the `generate` phase). |
| `--sheet <sheet-name>` | No | `pr_for_release_note` | Workbook sheet to read entries from. |
| `--releases-dir <releases-dir>` | Yes | None | Path to the existing English release notes directory (used to determine the default output path). |
| `--output-release-file <path>` | No | `release-<version>-updated-by-ai.md` | Output Markdown file. The default never writes the canonical `release-<version>.md`, because the generator produces only `Improvements` and `Bug fixes`, not a complete release note. |
| `--release-date <date>` | No | `TBD` | Release date text for the generated Markdown header. |

## Generated files

**Phase 1 (`generate`):**

- The source Excel file passed to `--excel` is not overwritten (unless `--output-excel` points to the same file, which is useful for resume scenarios).
- The processed Excel file is written to `<original-name>_processed.xlsx` next to the source workbook, or to the path specified by `--output-excel`.
- Rows where AI determines no release note is needed are moved to a separate `release_note_not_needed` sheet in the processed workbook. This move is skipped when `--start-row` or `--end-row` is used, so that deleting rows does not shift the row numbers a later segment relies on; such rows stay in the main sheet but are still excluded from Markdown.

**Phase 2 (`export-markdown`):**

- The generated Markdown file is written to `--output-release-file` when that option is specified.
- If `--output-release-file` is omitted, the generated Markdown file is written to `release-<version>-updated-by-ai.md` under `--releases-dir`. The default never overwrites the canonical `release-<version>.md`, because the generated file is an incomplete draft (only `Improvements` and `Bug fixes`).
- The Excel workbook is not modified during this phase.

## Reference: processing rules

The following sections describe the main processing logic and rules used by the generator.

### Processing pipeline

| Stage | What happens | Review value |
| --- | --- | --- |
| Scope filtering | Out-of-scope rows are moved to `PRs_not_in_scope` with a reason. | Reviewers can see why a row was excluded. |
| Workbook setup | Rows are sorted by component, and output columns are added or reset. | Related rows are easier to inspect, and generated data stays separate from source data. |
| Historical scan | Existing release notes are indexed by GitHub URL, contributor, section, and component. | The generator can reuse published wording instead of drafting duplicate text. |
| Same-series quarantine | Issues already published in the same major.minor series are moved to a separate sheet. | Repeated issues in the same series are visible for manual review. |
| Duplicate marking | Reusable historical entries are written to `published_release_notes` and rendered as `(dup)` entries. | The output keeps the reviewed published note and its source location. |
| Author replacement | Bot-authored cherry-pick rows are resolved to the original PR author when possible. | Contributor suffixes and duplicate matching use the real author. |
| Row merging | Rows with the same first issue URL and raw Excel component are merged. | Multiple PRs for one issue produce one release note entry. |
| Entry generation | Non-duplicate rows are generated by AI or copied from `formated_release_note` in non-AI mode. | The same preprocessing works for both drafting and dry-run workflows. |
| Markdown rendering | Entries are grouped by type and Markdown component. | The draft follows the expected release note structure. |

### Scope filtering

Scope filtering removes rows that should not appear in the target release note. Removed rows are copied to `PRs_not_in_scope`, receive a `Reason` value, and are deleted from the main sheet in the processed workbook.

General rules:

| Condition | Result | Why |
| --- | --- | --- |
| `pr_status` is not `merged` | Move the row to `PRs_not_in_scope`. | Unmerged changes should not be documented as released. |
| `pr_merge_time` is empty or cannot be parsed | Keep the row. | The generator cannot prove that the row is out of scope. |

Patch-release rules:

For a patch release such as `8.5.7`, the generator finds the previous patch release date in `releases/release-timeline.md`. When parsing `release-timeline.md`, the generator skips non-semver entries such as `Pre-GA`.

| Condition | Result | Why |
| --- | --- | --- |
| The PR was merged before the previous patch release date. | Move the row to `PRs_not_in_scope`. | The PR should already have been considered for the previous patch release. |
| The PR was merged on or after the previous patch release date. | Keep the row. | The PR falls into the target patch-release window. |

`x.y.0` release rules:

For an `x.y.0` release, the generator uses `releases/release-timeline.md` and release-branch PR data to avoid including changes that were already shipped in the latest previous major.minor release.

| Condition | Result | Why |
| --- | --- | --- |
| The PR was merged on or after the latest previously released `x.y.0` date. | Keep the row. | The PR is newer than that previous release boundary. |
| The PR was merged before the estimated start date of the previous release branch. | Move the row to `PRs_not_in_scope`. | The PR is older than the branch window for the previous major.minor release. |
| The PR was merged during the previous release-branch window, and a cherry-pick PR for the previous release branch was merged before that previous release date. | Move the row to `PRs_not_in_scope`. | The change was already included through that cherry-pick. |
| No earlier-release evidence is found. | Keep the row. | The generator keeps the row when it cannot prove that the change is out of scope. |

The estimated release-branch start date comes from the earliest closed PR that targets the previous release branch. You can override it with `--scope-base-branch-start-date`.

When matching a cherry-pick PR to the original PR, the generator recognizes:

- The full original PR URL.
- A cross-repository reference such as `pingcap/tidb#12345`.
- A same-repository suffix such as `(#12345)`.
- A branch or text pattern such as `cherry-pick-12345`.
- A line that contains `backport`, `cherry-pick`, `original`, `source`, or `from` together with `#12345`.

### Historical release note index

The generator scans existing Markdown files under `--releases-dir` before it decides whether a workbook row is a duplicate.

The scanner:

- Ignores generated drafts whose file name contains `updated-by-ai`.
- Ignores release-note files whose version is greater than or equal to the target version.
- Tracks the current release-note section and component from headings and component bullets.
- Extracts every GitHub issue or PR URL from a release note line.
- Extracts contributors from `@[user](https://github.com/user)` suffixes.
- Classifies each historical line as `improvement` or `bug_fix` from its surrounding section.
- Records the surrounding Markdown component when possible.

Each historical entry can later be reused in this format:

```markdown
- (dup): <release-file> <section-and-component-path> <published-release-note-line>
```

This preserves the published wording and shows the source file and component path.

### Repeated issues and duplicates

The generator handles repeated issues in two different ways:

- Same-series repeats are moved to a separate worksheet for review.
- Reusable duplicates from other series are rendered as `(dup)` entries.

This separation is intentional. If the same issue appears again in the same major.minor series, it is often a sign that the row needs human judgment. If the issue has already been documented elsewhere and the author check passes, reusing the published note is usually safer than drafting a new sentence.

For target version `8.5.7`, the same-series quarantine sheet is named:

```text
issue_already_in_earlier_v8.5
```

A row is moved to this sheet when all of the following are true:

- The row has an issue URL in `issue_url` or `formated_release_note`.
- The same issue URL appears in an existing release-note file.
- The existing release-note file is from the same major.minor series.
- The existing release-note file version is earlier than the target version.

Rows in this sheet are not rendered to Markdown.

After same-series rows are moved out, the generator marks remaining rows as duplicates when their issue URLs match reusable historical entries.

| Rule | Behavior |
| --- | --- |
| Issue URL source | The generator reads issue URLs from `issue_url`, if present, and from `formated_release_note`. |
| PR URL source | PR URLs are not used for duplicate matching. They are used for AI context and component inference. |
| Author check | If a historical note has contributors, at least one current row author must match a historical contributor. If the historical note has no contributors, the URL match is enough. |
| Workbook output | Matching historical notes are written to `published_release_notes`, and the row is filled in gray. |
| Markdown output | Duplicate rows are rendered from `published_release_notes`; they do not go through AI generation. |
| Type selection | The generator uses the historical section when possible. Otherwise, it falls back to the current row `issue_type`. |
| Component selection | The generator uses the historical component path when possible. Otherwise, it falls back to the current row component. |

### Author and row normalization

Cherry-pick PRs are often authored by `ti-chi-bot` or `ti-srebot`. For rows with those authors, the generator tries to find the original PR from the cherry-pick PR title, branch name, or body.

When the original PR is found, the generator:

- Replaces `pr_author` with the original PR author.
- Updates author Markdown in `formated_release_note` from the bot account to the original author.

If the original PR cannot be found, the row keeps the bot author. This avoids blocking the whole run because of one incomplete cherry-pick reference.

Rows are then merged when they have the same first issue URL and the same raw Excel component. For each merged group, the first row is kept. The kept row receives:

- The union of `pr_link` values.
- The union of `pr_author` values.
- The union of duplicate notes from `published_release_notes`.
- The first available non-empty value for other empty cells.

Rows are grouped by the raw Excel component, not the normalized Markdown component. This keeps workbook distinctions intact until the final component mapping stage.

### Entry generation

With `--involve-ai-generation ON`, the generator calls the configured AI command for non-duplicate rows that do not already have reusable text in `release_notes_written_by_ai`.

The prompt includes:

- The raw Excel component and normalized Markdown component.
- Workbook fields such as `issue_type`, `pr_title`, `formated_release_note`, expected links, and contributors.
- GitHub issue titles, bodies, and labels.
- GitHub PR titles, bodies, authors, branches, merge times, and changed-file summaries.
- The repository-local writing references for improvements and bug fixes.
- The prompt template in `scripts/release-notes-ai-generator/prompts/generation.md`.

The AI command must return a JSON object with these fields:

| Field | Rule |
| --- | --- |
| `type` | Must be `improvement` or `bug_fix`. |
| `release_note` | Must be one Markdown bullet that starts with a hyphen followed by a space. |
| `needs_review` | Must be a boolean. |
| `reason` | Must explain the type and wording choice. |

The generator validates that the release note:

- Starts with a hyphen followed by a space.
- Does not end with a period.
- Includes every expected issue or PR link.
- Includes every non-bot contributor as `@[user](https://github.com/user)`.

If validation fails, the generator sends one repair prompt. If the repaired output still fails, the row is marked as:

```text
AI_GENERATION_FAILED: <error>
```

Failed rows are not rendered to Markdown.

If `release_notes_written_by_ai` already contains a value and does not start with `AI_GENERATION_FAILED:`, the generator reuses it instead of calling AI again. Use `--force-regenerate` to clear existing AI output and regenerate all non-duplicate rows.

With `--involve-ai-generation OFF`, the generator does not call the AI command. For non-duplicate rows, it splits `formated_release_note` into non-empty lines and renders those lines as Markdown entries. The preprocessing pipeline still runs in non-AI mode.

### Component mapping

The generator maps each workbook component to a Markdown release-note component before rendering. It also keeps the original workbook component in an HTML comment after each generated entry:

```markdown
- Improve ... [#12345](https://github.com/pingcap/tidb/issues/12345) @[user](https://github.com/user) <!-- component: planner -->
```

This marker lets reviewers trace the generated component back to the workbook value without changing the visible release-note text.

The generator resolves components in this order:

1. If the raw workbook value is already a known release-note component or alias, use that value.
2. If the raw workbook value contains multiple comma-separated or newline-separated values, apply the multi-value priority rules.
3. If the workbook value still cannot be resolved, infer the component from the GitHub repositories in the issue and PR URLs.
4. If no rule matches, use the normalized raw workbook value.
5. If the final value is empty, render the entry under `Other`.

Direct aliases:

| Excel component value | Markdown component |
| --- | --- |
| `tidb` | `TiDB` |
| `tikv` | `TiKV` |
| `pd` | `PD` |
| `tiflash` | `TiFlash` |
| `tiproxy` | `TiProxy` |
| `br`, `backup & restore`, `backup & restore (br)` | `Backup & Restore (BR)` |
| `cdc`, `ticdc` | `TiCDC` |
| `dm`, `tidb data migration`, `tidb data migration (dm)` | `TiDB Data Migration (DM)` |
| `tidb lightning`, `lightning` | `TiDB Lightning` |
| `dumpling` | `Dumpling` |
| `tiup` | `TiUP` |
| `tidb binlog` | `TiDB Binlog` |
| `sync_diff`, `sync-diff-inspector`, `sync diff inspector` | `sync-diff-inspector` |

TiDB subcomponent aliases:

| Excel component value | Markdown component |
| --- | --- |
| `ng monitoring`, `ng-monitoring` | `TiDB` |
| `planner` | `TiDB` |
| `execution` | `TiDB` |
| `sql-infra` | `TiDB` |
| `transaction` | `TiDB` |
| `engine` | `TiDB` |
| `observability` | `TiDB` |
| `dxf` | `TiDB` |
| `storage` | `TiDB` |
| `tidb-dashboard`, `tidb dashboard` | `TiDB` |
| `ddl` | `TiDB` |
| `coprocessor` | `TiDB` |
| `compute` | `TiDB` |
| `scheduling` | `TiDB` |
| `spm` | `TiDB` |

When a workbook cell contains multiple component values, the generator applies this priority:

1. Tool components with stronger source meaning: `Backup & Restore (BR)`, `TiDB Lightning`, `Dumpling`, `TiUP`, and `sync-diff-inspector`.
2. Top-level components: `TiDB`, `TiKV`, `PD`, `TiFlash`, and `TiProxy`.
3. `TiDB Data Migration (DM)`.
4. `TiCDC`.

Repository fallback rules:

| Repository evidence | Markdown component |
| --- | --- |
| `pd` | `PD` |
| `tikv` | `TiKV` |
| `tiflash` | `TiFlash` |
| `ng-monitoring` | `TiDB` |
| `tiup` | `TiUP` |
| `tiflow` or `ticdc`, and the raw component contains `dm` but not `cdc` | `TiDB Data Migration (DM)` |
| `tiflow` or `ticdc`, otherwise | `TiCDC` |
| `tidb`, and the raw component contains `br` | `Backup & Restore (BR)` |
| `tidb`, and the raw component contains `lightning` | `TiDB Lightning` |
| `tidb`, and the raw component contains `dumpling` | `Dumpling` |
| `tidb`, otherwise | `TiDB` |
| `tidb-dashboard` | `TiDB` |

### Markdown rendering and safe saving

The generated file contains front matter, the `# TiDB <version> Release Notes` heading, release metadata, quick access links, `## Improvements`, and `## Bug fixes`.

Entries are grouped by type and component. Top-level components are rendered in this order:

```text
TiDB, TiKV, PD, TiFlash, TiProxy
```

Tool components are rendered under `+ Tools` in this order:

```text
Backup & Restore (BR), TiCDC, TiDB Data Migration (DM), TiDB Lightning, Dumpling, TiUP, TiDB Binlog, sync-diff-inspector
```

Known top-level components are rendered first. Unknown non-tool components are rendered next in alphabetical order. Tool components are rendered last under `Tools`.

Before writing an entry, the renderer normalizes its bullet marker to a hyphen followed by a space. If the entry does not already contain a component marker, the renderer appends the raw workbook component as an HTML comment.

The processed workbook is saved to `<source-name>_processed.xlsx`. During AI generation, `--checkpoint-interval` controls how often the processed workbook is saved:

- The default value `1` saves after every completed AI row.
- `0` disables checkpoint saves.

Workbook saves are atomic. The generator first writes a temporary file in the target directory and then replaces the processed workbook. If replacement fails after a complete temporary workbook has been written, the error message includes the temporary file path.

