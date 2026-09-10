---
title: ti fs-vault list-audit-events
summary: List Filesystem Vault audit events.
---

# ti fs-vault list-audit-events

Lists vault audit events with optional agent, secret, and time filters.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs-vault list-audit-events
  [--agent-id <string>]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--limit <int32>]
  [--secret-name <string>]
  [--since <duration>]
  [--version]
```

## Options

- `--agent-id <string>`: Filter by agent ID.
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TI_FS_TOKEN`.
- `--help`: Display help information.
- `--limit <int32>`: Maximum events to return. \[default: 100]
- `--secret-name <string>`: Filter by Vault secret name.
- `--since <duration>`: Client-side relative time filter, for example, `24h`.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- List events for one secret:

    ```bash
    # Inspect recent access and mutation events for the selected secret.
    ti fs-vault list-audit-events --file-system-id <file-system-id> --secret-name db-prod --limit 20
    ```

- List recent events for an agent:

    ```bash
    # Filter the audit trail to one delegated identity and time range.
    ti fs-vault list-audit-events --file-system-id <file-system-id> --agent-id deploy-agent --since 24h
    ```

## Related documentation

- [TiDB Cloud Filesystem Vault CLI Command Reference](/ai/ti/reference/ti-filesystem-vault.md)
