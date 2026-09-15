---
title: ti fs-vault run-with-secret
summary: Run a process with a Filesystem Vault secret.
---

# ti fs-vault run-with-secret

Runs a command with one secret injected into its environment. Arguments after `--` are passed to the child command.

Each secret field name becomes an environment variable with the same name in the child process. Field names must match `[A-Z_][A-Z0-9_]*`, so create fields that you intend to inject with uppercase names. The command rejects the entire injection if any field name, including a name that contains lowercase letters, does not match this pattern or if a value contains an unsupported control character.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Syntax

```text
ti fs-vault run-with-secret
  --secret-path <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--vault-token <string>]
  [--version]
  -- <command> [args...]
```

## Options

- `--secret-path <string>`: Canonical Vault path in the form `/n/vault/<secret-name>`. For example, the secret created as `db-prod` has the path `/n/vault/db-prod`. \[required]
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the owner Filesystem token. If omitted, the command uses the `TI_FS_TOKEN` environment variable. If neither is provided, the command uses the local token stored for the selected Filesystem. For delegated authentication, use `--vault-token` or `TI_VAULT_TOKEN` instead.
- `--help`: Display help information.
- `--vault-token <string>`: Delegated `ti fs-vault` token; prefer `TI_VAULT_TOKEN`.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Run a process with secret fields:

    ```bash
    # Verify that the child process receives DB_URL without printing its value.
    ti fs-vault run-with-secret --file-system-id <file-system-id> --secret-path /n/vault/db-prod -- sh -c 'test -n "$DB_URL" && printf "DB_URL is set\n"'
    ```

- Run an application with injected fields:

    ```bash
    # Make all fields available only to the child process and its descendants.
    ti fs-vault run-with-secret --file-system-id <file-system-id> --secret-path /n/vault/db-prod -- ./deploy.sh
    ```

## Related documentation

- [TiDB Cloud Filesystem Vault CLI Command Reference](/ai/ti/reference/ti-filesystem-vault.md)
