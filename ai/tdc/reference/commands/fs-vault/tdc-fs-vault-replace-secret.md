---
title: tdc fs-vault replace-secret
summary: Replace all fields in a Filesystem Vault secret.
---

# tdc fs-vault replace-secret

Replaces all fields in one secret from files in a local directory.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `tdc` — is currently in preview. Its features and command-line interface might change without prior notice.

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
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

- Replace a secret from a directory:

    ```bash
    # Replace all fields with files loaded from the selected directory.
    tdc fs-vault replace-secret --file-system-name workspace --secret-path /n/vault/db-prod --from-directory ./secret-fields
    ```

- Preview secret replacement:

    ```bash
    # Validate the replacement source without changing the stored secret.
    tdc fs-vault replace-secret --file-system-name workspace --secret-path /n/vault/db-prod --from-directory ./secret-fields --dry-run
    ```

## Related documentation

- [TiDB Cloud Filesystem Vault CLI Command Reference](/ai/tdc/reference/tdc-filesystem-vault.md)
