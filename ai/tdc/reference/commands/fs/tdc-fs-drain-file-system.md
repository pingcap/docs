---
title: tdc fs drain-file-system
summary: Drain a mounted TiDB Cloud Filesystem.
---

# tdc fs drain-file-system

Flushes dirty FUSE state while leaving the mount online. The command alias is `tdc fs drain`.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs drain-file-system
    --mount-path <string>
    [--dry-run]
    [--help]
    [--timeout <duration>]
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
tdc fs drain-file-system --mount-path /path/to/workspace
tdc fs drain --mount-path /path/to/workspace --timeout 30s
```
