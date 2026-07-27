---
title: tdc fs-vault list-secrets
summary: List secrets visible to a Filesystem Vault credential.
---

# tdc fs-vault list-secrets

Lists secrets visible to the active owner or delegated credential.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs-vault list-secrets
  [--file-system-name <string>]
  [--fs-token <string>]
  [--help]
  [--vault-token <string>]
  [--version]
```

## Options

- `--file-system-name <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_NAME`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--vault-token <string>`: Delegated tdc fs-vault token; prefer `TDC_VAULT_TOKEN`.
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### List secrets

```bash
tdc fs-vault list-secrets --file-system-name workspace
```

### List secrets with a delegated Vault token

```bash
tdc fs-vault list-secrets --file-system-name workspace --vault-token "$TDC_VAULT_TOKEN" --output text
```
