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
```

## Options

- `--field <string>`: Secret field assignment `key=value`, `key=@file`, or `key=-`; repeatable. \[required]
- `--secret-name <string>`: Vault secret name. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--file-system-name <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_NAME`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Create a secret from values and a file

```bash
tdc fs-vault create-secret --file-system-name workspace --secret-name db-prod --field DB_URL=mysql://example --field PASSWORD=@./password.txt
```

### Preview secret creation

```bash
tdc fs-vault create-secret --file-system-name workspace --secret-name api-dev --field TOKEN=@./token.txt --dry-run
```
