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
```

## Options

- `--secret-name <string>`: Vault secret name. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--file-system-name <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_NAME`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Preview secret deletion

```bash
tdc fs-vault delete-secret --file-system-name workspace --secret-name db-prod --dry-run
```

### Delete a secret

```bash
tdc fs-vault delete-secret --file-system-name workspace --secret-name db-prod
```
