---
title: tdc fs describe-file
summary: Describe a file in a TiDB Cloud Filesystem.
---

# tdc fs describe-file

Describes metadata for one remote path. The command alias is `tdc fs stat`.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs describe-file
    --path <string>
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
tdc fs describe-file --path /reports/report.md
tdc fs stat --path /reports/report.md --output text
```
