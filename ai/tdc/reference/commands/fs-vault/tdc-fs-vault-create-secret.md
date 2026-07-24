---
title: tdc fs-vault create-secret
summary: Create a secret in Filesystem Vault.
---

# tdc fs-vault create-secret

Creates a secret from one or more `NAME=value` or `NAME=@file` fields.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs-vault create-secret
    --field <string>
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
tdc fs-vault create-secret --secret-name db-prod --field DB_URL=mysql://example --field PASSWORD=@./password.txt
tdc fs-vault create-secret --secret-name api-dev --field TOKEN=@./token.txt --dry-run
```
