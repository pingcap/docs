---
title: tdc fs list-file-systems
summary: List locally registered TiDB Cloud Filesystems.
---

# tdc fs list-file-systems

Lists Filesystems registered in the selected local profile.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs list-file-systems
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
tdc fs list-file-systems --output text
tdc fs list-file-systems --query 'file_systems[].file_system_name'
```
