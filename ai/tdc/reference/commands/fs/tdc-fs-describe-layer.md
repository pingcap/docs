---
title: tdc fs describe-layer
summary: Describe a layer in a TiDB Cloud Filesystem.
---

# tdc fs describe-layer

Describes one Filesystem layer.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs describe-layer
    --layer-id <string>
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
tdc fs describe-layer --layer-id "<layer-id>"
tdc fs describe-layer --layer-id "<layer-id>" --output text
```
