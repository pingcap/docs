---
title: tdc fs create-file-system
summary: Create a TiDB Cloud Filesystem.
---

# tdc fs create-file-system

Creates a Filesystem. `--wait` waits until data-plane access is ready.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs create-file-system
    --file-system-name <string>
    [--dry-run]
    [--help]
    [--set-default]
    [--version]
    [--wait]
    [--debug]
    [--output <string>]
    [--profile <string>]
    [--query <string>]
    [--region <string>]
```

Filesystem selection can come from `--file-system-name`, `TDC_FS_FILE_SYSTEM_NAME`, or the selected profile. For shared global flags, see [tdc CLI Reference](/ai/tdc/reference/tdc-cli-reference.md).

## Examples

```shell
tdc fs create-file-system --file-system-name workspace --set-default --wait
tdc fs create-file-system --file-system-name workspace --dry-run
```
