---
title: ti fs-journal search-journal-entries
summary: Search Filesystem journals and entries.
---

# ti fs-journal search-journal-entries

Searches journals and optionally returns matching entries.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Syntax

```text
ti fs-journal search-journal-entries
  [--actor <string>]
  [--cursor <string>]
  [--entry-type <string>]
  [--file-system-id <string>]
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
- `--cursor <string>`: Cursor returned by a previous page. When continuing, repeat the filters from the original request.
- `--entry-type <string>`: Entry type filter.
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the Filesystem token. If omitted, the command uses the `TI_FS_TOKEN` environment variable. If neither is provided, the command uses the local token stored for the selected Filesystem.
- `--help`: Display help information.
- `--include-entries`: Include full entry payloads in matches.
- `--journal-kind <string>`: Journal kind filter.
- `--label <string>`: Label filter `key=value`; repeatable.
- `--limit <int32>`: Maximum matches to read. \[default: 100]
- `--since <string>`: Lower time bound as a relative duration, such as `24h`, or an RFC3339 timestamp.
- `--status <string>`: Entry status filter.
- `--subject <string>`: Subject filter; repeatable.
- `--until <string>`: Upper time bound as an RFC3339 timestamp. Relative durations are not accepted.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Search by entry type:

    ```bash
    # Find journals containing task-start events and include their payloads.
    ti fs-journal search-journal-entries --file-system-id <file-system-id> --entry-type task.started --include-entries
    ```

- Search by label and time:

    ```bash
    # Limit deployment journal matches to one environment and time window.
    ti fs-journal search-journal-entries --file-system-id <file-system-id> --label env=dev --since 2026-07-01T00:00:00Z --limit 100
    ```

- Search by actor and subject:

    ```bash
    # Find events produced by one agent for a specific task subject.
    ti fs-journal search-journal-entries --file-system-id <file-system-id> --actor agent:ti --subject issue-42 --include-entries
    ```

## Related documentation

- [TiDB Cloud Filesystem Journal CLI Command Reference](/ai/ti/reference/ti-filesystem-journal.md)
