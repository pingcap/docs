---
title: tdc fs-journal read-journal-entries
summary: Read entries from a Filesystem journal.
---

# tdc fs-journal read-journal-entries

Reads entries from one journal in sequence order.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs-journal read-journal-entries
    --journal-id <string>
    [--after-seq <int64>]
    [--file-system-name <string>]
    [--fs-token <string>]
    [--help]
    [--limit <int32>]
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
tdc fs-journal read-journal-entries --journal-id jrn-demo
tdc fs-journal read-journal-entries --journal-id jrn-demo --after-seq 100 --limit 50
```
