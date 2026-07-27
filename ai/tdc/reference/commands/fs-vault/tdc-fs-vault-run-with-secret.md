---
title: tdc fs-vault run-with-secret
summary: Run a process with a Filesystem Vault secret.
---

# tdc fs-vault run-with-secret

Runs a command with one secret injected into its environment. Arguments after `--` are passed to the child command.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `tdc` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs-vault run-with-secret
  --secret-path <string>
  [--file-system-name <string>]
  [--fs-token <string>]
  [--help]
  [--vault-token <string>]
  [--version]
```

## Options

- `--secret-path <string>`: Vault path in the form `/n/vault/<secret>`. \[required]
- `--file-system-name <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_NAME`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--vault-token <string>`: Delegated `tdc fs-vault` token; prefer `TDC_VAULT_TOKEN`.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

- Run a process with secret fields:

    ```bash
    # Inject all fields into the child process environment without printing them.
    tdc fs-vault run-with-secret --file-system-name workspace --secret-path /n/vault/db-prod -- env
    ```

- Use an injected field in a shell command:

    ```bash
    # Verify that the child process receives DB_URL without exposing its value.
    tdc fs-vault run-with-secret --file-system-name workspace --secret-path /n/vault/db-prod -- sh -c 'test -n "$DB_URL"'
    ```

## Related documentation

- [TiDB Cloud Filesystem Vault CLI Command Reference](/ai/tdc/reference/tdc-filesystem-vault.md)
