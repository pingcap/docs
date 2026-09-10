---
title: ti fs-vault list-secrets
summary: List secrets visible to a Filesystem Vault credential.
---

# ti fs-vault list-secrets

Lists secrets visible to the active owner or delegated credential.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

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
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TI_FS_TOKEN`.
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
    # Restrict the result to secrets within the token's granted scope.
    ti fs-vault list-secrets --file-system-id <file-system-id> --vault-token "$TI_VAULT_TOKEN"
    ```

## Related documentation

- [TiDB Cloud Filesystem Vault CLI Command Reference](/ai/ti/reference/ti-filesystem-vault.md)
