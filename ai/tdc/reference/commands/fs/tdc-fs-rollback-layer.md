---
title: tdc fs rollback-layer
summary: Roll back a TiDB Cloud Filesystem layer.
---

# tdc fs rollback-layer

Rolls back changes in one layer without committing them to the base.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs rollback-layer
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
tdc fs rollback-layer --layer-id "<layer-id>" --dry-run
tdc fs rollback-layer --layer-id "<layer-id>"
```
