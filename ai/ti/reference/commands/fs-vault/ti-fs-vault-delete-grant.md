---
title: ti fs-vault delete-grant
summary: Revoke a delegated Filesystem Vault grant.
---

# ti fs-vault delete-grant

Revokes one delegated Filesystem Vault grant.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs-vault delete-grant
  --grant-id <string>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--reason <string>]
  [--revoked-by <string>]
  [--version]
```

## Options

- `--grant-id <string>`: Vault grant ID. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TI_FS_TOKEN`.
- `--help`: Display help information.
- `--reason <string>`: Optional revoke reason.
- `--revoked-by <string>`: Actor label for the revoke audit entry. \[default: `ti`]
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Revoke a grant:

    ```bash
    # Invalidate the delegated token and record the revocation reason.
    ti fs-vault delete-grant --file-system-id <file-system-id> --grant-id "<grant-id>" --reason rotated
    ```

## Related documentation

- [TiDB Cloud Filesystem Vault CLI Command Reference](/ai/ti/reference/ti-filesystem-vault.md)
