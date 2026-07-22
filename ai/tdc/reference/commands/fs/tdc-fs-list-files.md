---
title: tdc fs list-files
summary: List files in a TiDB Cloud Filesystem.
---

# tdc fs list-files

Lists entries below a remote path. The command alias is `tdc fs ls`.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs list-files
    [--file-system-name <string>]
    [--fs-token <string>]
    [--help]
    [--path <string>]
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
tdc fs list-files --path /reports
tdc fs list-files --path /reports --output text
```
