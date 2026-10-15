---
title: ti fs-vault read-secret
summary: Read a secret from file system Vault.
---

# ti fs-vault read-secret

Reads a complete secret or one field using an owner or delegated credential.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

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
- `--fs-token <string>`: Set the file system owner token. If omitted, the command uses the `TI_FS_TOKEN` environment variable. If neither is provided, the command uses the local token stored for the selected file system. For delegated authentication, use `--vault-token` or `TI_VAULT_TOKEN` instead.
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
    # Read the delegated token without echoing it or storing it in shell history.
    printf 'Delegated Vault token: ' >&2
    read -r -s TI_VAULT_TOKEN
    printf '\n' >&2
    export TI_VAULT_TOKEN

    # Access only the field allowed by the delegated token.
    ti fs-vault read-secret --file-system-id <file-system-id> --secret-name db-prod --field DB_URL --format raw
    unset TI_VAULT_TOKEN
    ```

## Related documentation

- [TiDB Cloud Filesystem Vault CLI Command Reference](/ai/ti/reference/ti-filesystem-vault.md)
