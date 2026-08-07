---
title: tdc fs-journal search-journal-entries
summary: Search Filesystem journals and entries.
---

# tdc fs-journal search-journal-entries

Searches journals and optionally returns matching entries.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `tdc` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs-journal search-journal-entries
  [--actor <string>]
  [--cursor <string>]
  [--entry-type <string>]
  [--file-system-name <string>]
  [--fs-token <string>]
  [--help]
  [--include-entries]
  [--journal-kind <string>]
  [--label <string>]
  [--limit <int32>]
  [--since <string>]
  [--status <string>]
  [--subject <string>]
  [--until <string>]
  [--version]
```

## Options

- `--actor <string>`: Actor in the form `type:id`.
- `--cursor <string>`: Pagination cursor.
- `--entry-type <string>`: Entry type filter.
- `--file-system-name <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_NAME`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--include-entries`: Include full entry payloads in matches.
- `--journal-kind <string>`: Journal kind filter.
- `--label <string>`: Label filter `key=value`; repeatable.
- `--limit <int32>`: Maximum matches to read. \[default: 100]
- `--since <string>`: Relative duration or RFC3339 lower time bound.
- `--status <string>`: Entry status filter.
- `--subject <string>`: Subject filter; repeatable.
- `--until <string>`: RFC3339 upper time bound.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

- Search by entry type:

    ```bash
    # Find journals containing task-start events and include their payloads.
    tdc fs-journal search-journal-entries --file-system-name workspace --entry-type task.started --include-entries
    ```

- Search by label and time:

    ```bash
    # Limit deployment journal matches to one environment and time window.
    tdc fs-journal search-journal-entries --file-system-name workspace --label env=dev --since 2026-07-01T00:00:00Z --limit 100
    ```

- Search by actor and subject:

    ```bash
    # Find events produced by one agent for a specific task subject.
    tdc fs-journal search-journal-entries --file-system-name workspace --actor agent:tdc --subject issue-42 --include-entries
    ```

## Related documentation

- [TiDB Cloud Filesystem Journal CLI Command Reference](/ai/tdc/reference/tdc-filesystem-journal.md)
