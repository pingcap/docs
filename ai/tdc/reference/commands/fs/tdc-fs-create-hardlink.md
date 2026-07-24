---
title: tdc fs create-hardlink
summary: Create a hard link in a TiDB Cloud Filesystem.
---

# tdc fs create-hardlink

Creates a hard link to an existing remote path. The command alias is `tdc fs hardlink`.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs create-hardlink
    --link-path <string>
    --source-path <string>
    [--dry-run]
    [--file-system-name <string>]
    [--fs-token <string>]
    [--help]
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
tdc fs create-hardlink --source-path /reports/final.md --link-path /reports/final-copy.md
tdc fs hardlink --source-path /reports/final.md --link-path /reports/backup.md --dry-run
```
