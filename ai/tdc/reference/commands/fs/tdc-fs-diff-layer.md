---
title: tdc fs diff-layer
summary: Show changes in a TiDB Cloud Filesystem layer.
---

# tdc fs diff-layer

Lists changes in one layer, optionally up to a sequence number.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs diff-layer
    --layer-id <string>
    [--file-system-name <string>]
    [--fs-token <string>]
    [--help]
    [--max-seq <int64>]
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
tdc fs diff-layer --layer-id "<layer-id>"
tdc fs diff-layer --layer-id "<layer-id>" --max-seq 100
```
