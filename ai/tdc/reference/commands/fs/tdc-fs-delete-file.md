---
title: tdc fs delete-file
summary: Delete a file from a TiDB Cloud Filesystem.
---

# tdc fs delete-file

Deletes a remote file or directory. The command alias is `tdc fs rm`.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs delete-file
    --path <string>
    [--dry-run]
    [--file-system-name <string>]
    [--fs-token <string>]
    [--help]
    [--recursive]
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
tdc fs delete-file --path /reports/obsolete.md
tdc fs delete-file --path /scratch --recursive --dry-run
```
