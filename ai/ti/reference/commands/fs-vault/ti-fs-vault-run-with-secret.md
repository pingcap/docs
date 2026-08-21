---
title: ti fs-vault run-with-secret
summary: Run a process with a Filesystem Vault secret.
---

# ti fs-vault run-with-secret

Runs a command with one secret injected into its environment. Arguments after `--` are passed to the child command.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs-vault run-with-secret
  --secret-path <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--vault-token <string>]
  [--version]
```

## Options

- `--secret-path <string>`: Vault path in the form `/n/vault/<secret>`. \[required]
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TI_FS_TOKEN`.
- `--help`: Display help information.
- `--vault-token <string>`: Delegated `ti fs-vault` token; prefer `TI_VAULT_TOKEN`.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Run a process with secret fields:

    ```bash
    # Inject all fields into the child process environment without printing them.
    ti fs-vault run-with-secret --file-system-id <file-system-id> --secret-path /n/vault/db-prod -- env
    ```

- Use an injected field in a shell command:

    ```bash
    # Verify that the child process receives DB_URL without exposing its value.
    ti fs-vault run-with-secret --file-system-id <file-system-id> --secret-path /n/vault/db-prod -- sh -c 'test -n "$DB_URL"'
    ```

## Related documentation

- [TiDB Cloud Filesystem Vault CLI Command Reference](/ai/ti/reference/ti-filesystem-vault.md)
