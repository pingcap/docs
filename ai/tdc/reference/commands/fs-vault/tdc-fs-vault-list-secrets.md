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
    [--debug]
    [--output <string>]
    [--profile <string>]
    [--query <string>]
    [--region <string>]
```

Filesystem selection can come from `--file-system-name`, `TDC_FS_FILE_SYSTEM_NAME`, or the selected profile. For shared global flags, see [tdc CLI Reference](/ai/tdc/reference/tdc-cli-reference.md).

## Examples

```shell
tdc fs-vault list-secrets
tdc fs-vault list-secrets --vault-token "$TDC_VAULT_TOKEN" --output text
```
