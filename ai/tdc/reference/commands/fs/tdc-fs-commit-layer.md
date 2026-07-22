---
title: tdc fs commit-layer
summary: Commit a TiDB Cloud Filesystem layer.
---

# tdc fs commit-layer

Applies one layer to its base Filesystem.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs commit-layer
    --layer-id <string>
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
tdc fs commit-layer --layer-id "<layer-id>" --dry-run
tdc fs commit-layer --layer-id "<layer-id>"
```
