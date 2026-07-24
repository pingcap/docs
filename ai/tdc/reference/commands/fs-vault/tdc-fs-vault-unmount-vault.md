---
title: tdc fs-vault unmount-vault
summary: Unmount a Filesystem Vault view.
---

# tdc fs-vault unmount-vault

Unmounts a local Filesystem Vault filesystem.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs-vault unmount-vault
    --mount-path <string>
    [--dry-run]
    [--force]
    [--help]
    [--ignore-absent]
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
tdc fs-vault unmount-vault --mount-path ./vault
tdc fs-vault unmount-vault --mount-path ./vault --ignore-absent
```
