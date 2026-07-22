---
title: tdc fs mount-file-system
summary: Mount a TiDB Cloud Filesystem.
---

# tdc fs mount-file-system

Mounts a Filesystem through automatic, FUSE, or WebDAV mode. The command alias is `tdc fs mount`.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs mount-file-system
    --mount-path <string>
    [--cache-dir <string>]
    [--driver <string>]
    [--dry-run]
    [--file-system-name <string>]
    [--foreground]
    [--fs-token <string>]
    [--help]
    [--local-root <string>]
    [--mount-profile <string>]
    [--no-auto-unpack]
    [--pack-path <string>]
    [--read-cache-max-file-mb <int64>]
    [--read-cache-size-mb <int64>]
    [--read-cache-ttl <duration>]
    [--read-only]
    [--ready-timeout <duration>]
    [--remote-path <string>]
    [--unpack-archive-path <string>]
    [--version]
    [--write-back-cache]
    [--debug]
    [--output <string>]
    [--profile <string>]
    [--query <string>]
    [--region <string>]
```

Filesystem selection can come from `--file-system-name`, `TDC_FS_FILE_SYSTEM_NAME`, or the selected profile. For shared global flags, see [tdc CLI Reference](/ai/tdc/reference/tdc-cli-reference.md).

## Examples

```shell
tdc fs mount-file-system --file-system-name workspace --mount-path /path/to/workspace
tdc fs mount --mount-path /path/to/workspace --driver fuse --read-only
```
