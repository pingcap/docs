---
title: tdc fs set-default-file-system
summary: Set the default Filesystem for a tdc profile.
---

# tdc fs set-default-file-system

Sets the default Filesystem for the selected profile.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs set-default-file-system
    --file-system-name <string>
    [--dry-run]
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
tdc fs set-default-file-system --file-system-name workspace
tdc fs set-default-file-system --file-system-name workspace --dry-run
```
