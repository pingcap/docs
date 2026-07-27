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
```

## Options

- `--grant-id <string>`: Vault grant ID. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--file-system-name <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_NAME`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--reason <string>`: Optional revoke reason.
- `--revoked-by <string>`: Actor label for the revoke audit entry. \[default: tdc]
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Revoke a grant with a reason

```bash
tdc fs-vault delete-grant --file-system-name workspace --grant-id "<grant-id>" --reason rotated
```

### Preview grant revocation

```bash
tdc fs-vault delete-grant --file-system-name workspace --grant-id "<grant-id>" --revoked-by operator --dry-run
```
