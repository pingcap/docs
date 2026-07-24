---
title: tdc fs read-file
summary: Read a file from a TiDB Cloud Filesystem.
---

# tdc fs read-file

Writes a remote file or byte range to stdout. The command alias is `tdc fs cat`.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs read-file
    --path <string>
    [--file-system-name <string>]
    [--fs-token <string>]
    [--help]
    [--length <int64>]
    [--offset <int64>]
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
tdc fs read-file --path /reports/report.md
tdc fs read-file --path /archives/large.bin --offset 1024 --length 4096
```
