---
title: tdc fs-journal create-journal
summary: Create an append-only Filesystem journal.
---

# tdc fs-journal create-journal

Creates a journal. If `--journal-id` is omitted, the service generates one.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs-journal create-journal
    [--actor <string>]
    [--dry-run]
    [--file-system-name <string>]
    [--fs-token <string>]
    [--help]
    [--journal-id <string>]
    [--journal-kind <string>]
    [--label <string>]
    [--title <string>]
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
tdc fs-journal create-journal --journal-id jrn-demo --journal-kind agent --title "demo task"
tdc fs-journal create-journal --journal-kind deployment --actor agent:tdc --label env=dev --dry-run
```
