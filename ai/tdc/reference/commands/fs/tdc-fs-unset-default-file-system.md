---
title: tdc fs unset-default-file-system
summary: Clear the default Filesystem for a tdc profile.
---

# tdc fs unset-default-file-system

Clears the profile default without deleting a Filesystem.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs unset-default-file-system
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
tdc fs unset-default-file-system
tdc fs unset-default-file-system --dry-run
```
