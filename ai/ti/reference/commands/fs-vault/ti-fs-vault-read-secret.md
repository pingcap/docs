---
title: ti fs-vault read-secret
summary: Read a secret from Filesystem Vault.
---

# ti fs-vault read-secret

Reads a complete secret or one field using an owner or delegated credential.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs-vault read-secret
  --secret-name <string>
  [--field <string>]
  [--file-system-id <string>]
  [--format <string>]
  [--fs-token <string>]
  [--help]
  [--vault-token <string>]
  [--version]
```

## Options

- `--secret-name <string>`: Vault secret name. \[required]
- `--field <string>`: Optional field name to read.
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--format <string>`: Read output format: `json`, `raw`, or `env`. \[default: json]
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TI_FS_TOKEN`.
- `--help`: Display help information.
- `--vault-token <string>`: Delegated `ti fs-vault` token; prefer `TI_VAULT_TOKEN`.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Read one secret field as raw text:

    ```bash
    # Write only the selected field value for direct consumption by a process.
    ti fs-vault read-secret --file-system-id <file-system-id> --secret-name db-prod --field PASSWORD --format raw
    ```

- Format a field as an environment assignment:

    ```bash
    # Emit an exportable environment-variable representation of the field.
    ti fs-vault read-secret --file-system-id <file-system-id> --secret-name db-prod --field DB_URL --format env
    ```

- Read with a delegated Vault token:

    ```bash
    # Access only the scope granted to an agent without using the owner token.
    ti fs-vault read-secret --file-system-id <file-system-id> --secret-name db-prod --field DB_URL --vault-token "$TI_VAULT_TOKEN" --format raw
    ```

## Related documentation

- [TiDB Cloud Filesystem Vault CLI Command Reference](/ai/ti/reference/ti-filesystem-vault.md)
