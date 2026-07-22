---
title: tdc fs search-file-content
summary: Search file content in a TiDB Cloud Filesystem.
---

# tdc fs search-file-content

Searches remote file content, optionally in a layer. The command alias is `tdc fs grep`.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs search-file-content
    --pattern <string>
    [--file-system-name <string>]
    [--fs-token <string>]
    [--help]
    [--layer-id <string>]
    [--limit <int32>]
    [--path <string>]
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
tdc fs search-file-content --path /workspace --pattern "TODO" --limit 50
tdc fs grep --path /workspace --pattern "deprecated" --layer-id "<layer-id>"
```
