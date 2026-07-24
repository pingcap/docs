---
title: tdc fs chmod-file
summary: Change file permissions in a TiDB Cloud Filesystem.
---

# tdc fs chmod-file

Changes POSIX mode metadata for a remote path. The command alias is `tdc fs chmod`.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs chmod-file
    --mode <string>
    --path <string>
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
tdc fs chmod-file --path /reports/final.md --mode 0600
tdc fs chmod --path /reports/final.md --mode 0644 --dry-run
```
