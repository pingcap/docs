---
title: tdc fs list-layers
summary: List layers in a TiDB Cloud Filesystem.
---

# tdc fs list-layers

Lists layers for the selected Filesystem.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs list-layers
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
tdc fs list-layers
tdc fs list-layers --output text
```
