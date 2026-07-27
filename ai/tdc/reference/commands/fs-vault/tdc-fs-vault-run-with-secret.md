---
title: tdc fs-vault run-with-secret
summary: Run a process with a Filesystem Vault secret.
---

# tdc fs-vault run-with-secret

Runs a command with one secret injected into its environment. Arguments after `--` are passed to the child command.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

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
- `--vault-token <string>`: Delegated tdc fs-vault token; prefer `TDC_VAULT_TOKEN`.
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Run a command with secret fields

```bash
tdc fs-vault run-with-secret --file-system-name workspace --secret-path /n/vault/db-prod -- env
```

### Use an injected secret in a shell command

```bash
tdc fs-vault run-with-secret --file-system-name workspace --secret-path /n/vault/db-prod -- sh -c 'test -n "$DB_URL"'
```
