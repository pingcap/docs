---
title: ti fs-vault create-grant
summary: Create a delegated Filesystem Vault grant.
---

# ti fs-vault create-grant

Creates a time-limited delegated grant for one agent and scope.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs-vault create-grant
  --agent-id <string>
  --permission <string>
  --scope <string>
  --ttl <duration>
  [--dry-run]
  [--file-system-id <string>]
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
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TI_FS_TOKEN`.
- `--help`: Display help information.
- `--label-hint <string>`: Optional grant label hint.
- `--token-only`: Print only the delegated bearer token.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Create a temporary read grant:

    ```bash
    # Limit an agent to one secret field for ten minutes.
    ti fs-vault create-grant --file-system-id <file-system-id> --agent-id deploy-agent --scope db-prod/DB_URL --permission read --ttl 10m
    ```

- Return only the delegated token:

    ```bash
    # Produce token-only output for injection into an isolated CI job.
    ti fs-vault create-grant --file-system-id <file-system-id> --agent-id ci-agent --scope api-dev/TOKEN --permission read --ttl 5m --token-only
    ```

## Related documentation

- [TiDB Cloud Filesystem Vault CLI Command Reference](/ai/ti/reference/ti-filesystem-vault.md)
