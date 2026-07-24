---
title: tdc fs check-file-system
summary: Check TiDB Cloud Filesystem connectivity.
---

# tdc fs check-file-system

Checks Filesystem selection, endpoint resolution, credentials, and companion access.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs check-file-system
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
tdc fs check-file-system --file-system-name workspace
tdc fs check-file-system --file-system-name workspace --output text
```
