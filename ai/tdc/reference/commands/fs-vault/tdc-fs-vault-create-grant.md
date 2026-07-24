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
    [--debug]
    [--output <string>]
    [--profile <string>]
    [--query <string>]
    [--region <string>]
```

Filesystem selection can come from `--file-system-name`, `TDC_FS_FILE_SYSTEM_NAME`, or the selected profile. For shared global flags, see [tdc CLI Reference](/ai/tdc/reference/tdc-cli-reference.md).

## Examples

```shell
tdc fs-vault create-grant --agent-id deploy-agent --scope db-prod/DB_URL --permission read --ttl 10m
tdc fs-vault create-grant --agent-id ci-agent --scope api-dev/TOKEN --permission read --ttl 5m --token-only
```
