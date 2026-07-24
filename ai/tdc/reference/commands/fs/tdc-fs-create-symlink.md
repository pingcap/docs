---
title: tdc fs create-symlink
summary: Create a symbolic link in a TiDB Cloud Filesystem.
---

# tdc fs create-symlink

Creates a symbolic link. The command alias is `tdc fs symlink`.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs create-symlink
    --link-path <string>
    --target <string>
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
tdc fs create-symlink --target final.md --link-path /reports/latest.md
tdc fs symlink --target archive/report.md --link-path /reports/archive-link --dry-run
```
