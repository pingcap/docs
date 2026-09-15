---
title: ti fs-vault list-secrets
summary: List secrets visible to a Filesystem Vault credential.
---

# ti fs-vault list-secrets

Lists secrets visible to the active owner or delegated credential.

The command returns the complete visible list. It does not paginate the result.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Syntax

```text
ti fs-vault list-secrets
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--vault-token <string>]
  [--version]
```

## Options

- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the owner Filesystem token. If omitted, the command uses the `TI_FS_TOKEN` environment variable. If neither is provided, the command uses the local token stored for the selected Filesystem. For delegated authentication, use `--vault-token` or `TI_VAULT_TOKEN` instead.
- `--help`: Display help information.
- `--vault-token <string>`: Delegated `ti fs-vault` token; prefer `TI_VAULT_TOKEN`.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- List owner-visible secrets:

    ```bash
    # Return secret metadata without exposing field values.
    ti fs-vault list-secrets --file-system-id <file-system-id>
    ```

- List secrets visible to a delegated token:

    ```bash
    # Read the delegated token without echoing it or storing it in shell history.
    printf 'Delegated Vault token: ' >&2
    read -r -s TI_VAULT_TOKEN
    printf '\n' >&2
    export TI_VAULT_TOKEN

    # Restrict results to the token's granted scope.
    ti fs-vault list-secrets --file-system-id <file-system-id>
    unset TI_VAULT_TOKEN
    ```

## Related documentation

- [TiDB Cloud Filesystem Vault CLI Command Reference](/ai/ti/reference/ti-filesystem-vault.md)
