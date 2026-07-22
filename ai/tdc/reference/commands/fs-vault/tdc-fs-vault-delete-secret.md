---
title: tdc fs-vault delete-secret
summary: Delete a secret from Filesystem Vault.
---

# tdc fs-vault delete-secret

Deletes one Filesystem Vault secret.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs-vault delete-secret
    --secret-name <string>
    [--dry-run]
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
tdc fs-vault delete-secret --secret-name db-prod --dry-run
tdc fs-vault delete-secret --secret-name db-prod
```
