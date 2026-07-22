---
title: tdc fs-journal search-journal-entries
summary: Search Filesystem journals and entries.
---

# tdc fs-journal search-journal-entries

Searches journals and optionally returns matching entries.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

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
    [--debug]
    [--output <string>]
    [--profile <string>]
    [--query <string>]
    [--region <string>]
```

Filesystem selection can come from `--file-system-name`, `TDC_FS_FILE_SYSTEM_NAME`, or the selected profile. For shared global flags, see [tdc CLI Reference](/ai/tdc/reference/tdc-cli-reference.md).

## Examples

```shell
tdc fs-journal search-journal-entries --entry-type task.started --include-entries
tdc fs-journal search-journal-entries --label env=dev --since 2026-07-01T00:00:00Z --limit 100
```
