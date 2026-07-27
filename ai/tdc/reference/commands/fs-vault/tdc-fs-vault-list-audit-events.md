---
title: tdc fs-vault list-audit-events
summary: List Filesystem Vault audit events.
---

# tdc fs-vault list-audit-events

Lists vault audit events with optional agent, secret, and time filters.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs-vault list-audit-events
  [--agent-id <string>]
  [--file-system-name <string>]
  [--fs-token <string>]
  [--help]
  [--limit <int32>]
  [--secret-name <string>]
  [--since <duration>]
  [--version]
```

## Options

- `--agent-id <string>`: Filter by agent ID.
- `--file-system-name <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_NAME`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--limit <int32>`: Maximum events to return. \[default: 100]
- `--secret-name <string>`: Filter by Vault secret name.
- `--since <duration>`: Client-side relative time filter, for example, `24h`.
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### List audit events for a secret

```bash
tdc fs-vault list-audit-events --file-system-name workspace --secret-name db-prod --limit 20
```

### List recent events for an agent

```bash
tdc fs-vault list-audit-events --file-system-name workspace --agent-id deploy-agent --since 24h --output text
```
