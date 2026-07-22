---
title: tdc fs-vault mount-vault
summary: Mount a read-only Filesystem Vault view.
---

# tdc fs-vault mount-vault

Mounts readable vault fields as a local read-only FUSE filesystem.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs-vault mount-vault
    --mount-path <string>
    [--dry-run]
    [--file-system-name <string>]
    [--foreground]
    [--fs-token <string>]
    [--help]
    [--ready-timeout <duration>]
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
tdc fs-vault mount-vault --mount-path ./vault --vault-token "$TDC_VAULT_TOKEN"
tdc fs-vault mount-vault --mount-path ./vault --foreground --ready-timeout 60s
```
