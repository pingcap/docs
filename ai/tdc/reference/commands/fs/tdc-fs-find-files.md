---
title: tdc fs find-files
summary: Find files in a TiDB Cloud Filesystem.
---

# tdc fs find-files

Finds remote paths by name, type, tag, size, or modification time. The command alias is `tdc fs find`.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs find-files
    [--file-name-pattern <string>]
    [--file-system-name <string>]
    [--fs-token <string>]
    [--help]
    [--layer-id <string>]
    [--limit <int32>]
    [--max-size-bytes <int64>]
    [--min-size-bytes <int64>]
    [--newer <string>]
    [--older <string>]
    [--path <string>]
    [--resource-type <string>]
    [--tag <string>]
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
tdc fs find-files --path /workspace --file-name-pattern "*.md"
tdc fs find --path /workspace --tag stage=review --min-size-bytes 1024
```
