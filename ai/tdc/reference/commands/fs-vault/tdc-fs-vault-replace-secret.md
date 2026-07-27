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
```

## Options

- `--from-directory <string>`: Directory whose files become secret fields. \[required]
- `--secret-path <string>`: Vault path in the form `/n/vault/<secret>`. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--file-system-name <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_NAME`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Replace a secret from a directory

```bash
tdc fs-vault replace-secret --file-system-name workspace --secret-path /n/vault/db-prod --from-directory ./secret-fields
```

### Preview secret replacement

```bash
tdc fs-vault replace-secret --file-system-name workspace --secret-path /n/vault/db-prod --from-directory ./secret-fields --dry-run
```
