---
title: tdc fs create-directory
summary: Create a directory in a TiDB Cloud Filesystem.
---

# tdc fs create-directory

Creates a remote directory. The command alias is `tdc fs mkdir`.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs create-directory
    --path <string>
    [--dry-run]
    [--file-system-name <string>]
    [--fs-token <string>]
    [--help]
    [--mode <string>]
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
tdc fs create-directory --path /reports/archive --mode 0755
tdc fs mkdir --path /reports/review --dry-run
```
