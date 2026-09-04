---
title: ti fs-vault replace-secret
summary: Replace all fields in a Filesystem Vault secret.
---

# ti fs-vault replace-secret

Replaces all fields in one secret from files in a local directory.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs-vault replace-secret
  --from-directory <string>
  --secret-path <string>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## Options

- `--from-directory <string>`: Directory whose files become secret fields. \[required]
- `--secret-path <string>`: Vault path in the form `/n/vault/<secret>`. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TI_FS_TOKEN`.
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Replace a secret from a directory:

    ```bash
    # Replace all fields with files loaded from the selected directory.
    ti fs-vault replace-secret --file-system-id <file-system-id> --secret-path /n/vault/db-prod --from-directory ./secret-fields
    ```

- Preview secret replacement:

    ```bash
    # Validate the replacement source without changing the stored secret.
    ti fs-vault replace-secret --file-system-id <file-system-id> --secret-path /n/vault/db-prod --from-directory ./secret-fields --dry-run
    ```

## Related documentation

- [TiDB Cloud Filesystem Vault CLI Command Reference](/ai/ti/reference/ti-filesystem-vault.md)
