---
title: tdc fs pack-file-system
summary: Pack local Filesystem overlay state.
---

# tdc fs pack-file-system

Packs selected local overlay state into a remote archive.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs pack-file-system
    [--archive-path <string>]
    [--dry-run]
    [--file-system-name <string>]
    [--fs-token <string>]
    [--help]
    [--local-root <string>]
    [--mount-path <string>]
    [--mount-profile <string>]
    [--path <string>]
    [--remote-root <string>]
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
tdc fs pack-file-system --mount-path /path/to/workspace
tdc fs pack-file-system --local-root ./overlay --remote-root /workspace --mount-profile portable
```
