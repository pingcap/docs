---
title: tdc fs-vault create-grant
summary: Create a delegated Filesystem Vault grant.
---

# tdc fs-vault create-grant

Creates a time-limited delegated grant for one agent and scope.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs-vault create-grant
  --agent-id <string>
  --permission <string>
  --scope <string>
  --ttl <duration>
  [--dry-run]
  [--file-system-name <string>]
  [--fs-token <string>]
  [--help]
  [--label-hint <string>]
  [--token-only]
  [--version]
```

## Options

- `--agent-id <string>`: Agent ID for the delegated grant. \[required]
- `--permission <string>`: Grant permission: `read` or `write`. \[required]
- `--scope <string>`: Vault scope such as secret or secret/field; repeatable. \[required]
- `--ttl <duration>`: Grant time to live, for example, `1h`. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--file-system-name <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_NAME`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--label-hint <string>`: Optional grant label hint.
- `--token-only`: Print only the delegated bearer token.
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Create a read grant

```bash
tdc fs-vault create-grant --file-system-name workspace --agent-id deploy-agent --scope db-prod/DB_URL --permission read --ttl 10m
```

### Create a token-only grant for CI

```bash
tdc fs-vault create-grant --file-system-name workspace --agent-id ci-agent --scope api-dev/TOKEN --permission read --ttl 5m --token-only
```
