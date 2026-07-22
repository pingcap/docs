---
title: tdc fs create-layer
summary: Create a layer in a TiDB Cloud Filesystem.
---

# tdc fs create-layer

Creates an isolated change layer over a base root. If `--layer-id` is omitted, the service generates one.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs create-layer
    --base-root-path <string>
    [--actor-id <string>]
    [--dry-run]
    [--durability-mode <string>]
    [--file-system-name <string>]
    [--fs-token <string>]
    [--help]
    [--layer-id <string>]
    [--layer-name <string>]
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
tdc fs create-layer --base-root-path /workspace --layer-name agent-task
tdc fs create-layer --base-root-path /workspace --durability-mode restore-safe --tag task=review --dry-run
```
