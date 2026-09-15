---
title: ti fs-vault create-grant
summary: Create a delegated Filesystem Vault grant.
---

# ti fs-vault create-grant

Creates a time-limited delegated grant for one agent and scope.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

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
- `--permission <string>`: Grant permission: `read` or `write`. For the current permission behavior, see [Grant permissions](#grant-permissions). \[required]
- `--scope <string>`: Secret scope in the form `<secret-name>` for all fields or `<secret-name>/<field-name>` for one field; repeatable. The equivalent canonical Vault paths `/n/vault/<secret-name>` and `/n/vault/<secret-name>/<field-name>` are also accepted. \[required]
- `--ttl <duration>`: Grant time to live, for example, `1h`. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the Filesystem token. If omitted, the command uses the `TI_FS_TOKEN` environment variable. If neither is provided, the command uses the local token stored for the selected Filesystem.
- `--help`: Display help information.
- `--label-hint <string>`: Optional grant label hint.
- `--token-only`: Print only the delegated bearer token.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Grant permissions

| Permission | Current `ti` behavior |
| --- | --- |
| `read` | Allows delegated `list-secrets`, `read-secret`, `run-with-secret`, and `mount-vault` operations within the grant scopes. |
| `write` | The service accepts this permission, but it does not include read authority. The current `ti` command surface does not expose an operation that writes a secret with a delegated token. |

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
