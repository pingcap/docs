---
title: tdc fs unmount-file-system
summary: Unmount a TiDB Cloud Filesystem.
---

# tdc fs unmount-file-system

Gracefully flushes and unmounts a background mount. The command alias is `tdc fs umount`.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs unmount-file-system
    --mount-path <string>
    [--dry-run]
    [--force]
    [--help]
    [--ignore-absent]
    [--no-auto-pack]
    [--pack-archive-path <string>]
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
tdc fs unmount-file-system --mount-path /path/to/workspace
tdc fs umount --mount-path /path/to/workspace --ignore-absent
```
