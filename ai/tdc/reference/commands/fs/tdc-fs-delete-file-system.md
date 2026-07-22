---
title: tdc fs delete-file-system
summary: Delete a TiDB Cloud Filesystem.
---

# tdc fs delete-file-system

Requests asynchronous Filesystem deletion and removes its local registration.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs delete-file-system
    --file-system-name <string>
    [--dry-run]
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
tdc fs delete-file-system --file-system-name workspace --dry-run
tdc fs delete-file-system --file-system-name workspace
```
