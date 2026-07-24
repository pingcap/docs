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
    [--debug]
    [--output <string>]
    [--profile <string>]
    [--query <string>]
    [--region <string>]
```

Filesystem selection can come from `--file-system-name`, `TDC_FS_FILE_SYSTEM_NAME`, or the selected profile. For shared global flags, see [tdc CLI Reference](/ai/tdc/reference/tdc-cli-reference.md).

## Examples

```shell
tdc fs-vault run-with-secret --secret-path /n/vault/db-prod -- env
tdc fs-vault run-with-secret --secret-path /n/vault/db-prod -- sh -c 'test -n "$DB_URL"'
```
