---
title: tdc fs-vault delete-grant
summary: Revoke a delegated Filesystem Vault grant.
---

# tdc fs-vault delete-grant

Revokes one delegated Filesystem Vault grant.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs-vault delete-grant
    --grant-id <string>
    [--dry-run]
    [--file-system-name <string>]
    [--fs-token <string>]
    [--help]
    [--reason <string>]
    [--revoked-by <string>]
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
tdc fs-vault delete-grant --grant-id "<grant-id>" --reason rotated
tdc fs-vault delete-grant --grant-id "<grant-id>" --revoked-by operator --dry-run
```
