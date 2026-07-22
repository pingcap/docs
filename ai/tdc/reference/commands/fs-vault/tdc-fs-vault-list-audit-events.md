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
    [--debug]
    [--output <string>]
    [--profile <string>]
    [--query <string>]
    [--region <string>]
```

Filesystem selection can come from `--file-system-name`, `TDC_FS_FILE_SYSTEM_NAME`, or the selected profile. For shared global flags, see [tdc CLI Reference](/ai/tdc/reference/tdc-cli-reference.md).

## Examples

```shell
tdc fs-vault list-audit-events --secret-name db-prod --limit 20
tdc fs-vault list-audit-events --agent-id deploy-agent --since 24h --output text
```
