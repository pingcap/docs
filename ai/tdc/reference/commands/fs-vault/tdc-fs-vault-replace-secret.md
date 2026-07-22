---
title: tdc fs-vault replace-secret
summary: Replace all fields in a Filesystem Vault secret.
---

# tdc fs-vault replace-secret

Replaces all fields in one secret from files in a local directory.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs-vault replace-secret
    --from-directory <string>
    --secret-path <string>
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
tdc fs-vault replace-secret --secret-path /n/vault/db-prod --from-directory ./secret-fields
tdc fs-vault replace-secret --secret-path /n/vault/db-prod --from-directory ./secret-fields --dry-run
```
