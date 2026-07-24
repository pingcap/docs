---
title: tdc fs describe-file-system
summary: Describe a locally registered TiDB Cloud Filesystem.
---

# tdc fs describe-file-system

Describes one locally registered Filesystem.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs describe-file-system
    --file-system-name <string>
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
tdc fs describe-file-system --file-system-name workspace
tdc fs describe-file-system --file-system-name workspace --output text
```
