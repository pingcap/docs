---
title: tdc fs-vault read-secret
summary: Read a secret from Filesystem Vault.
---

# tdc fs-vault read-secret

Reads a complete secret or one field using an owner or delegated credential.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs-vault read-secret
    --secret-name <string>
    [--field <string>]
    [--file-system-name <string>]
    [--format <string>]
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
tdc fs-vault read-secret --secret-name db-prod --field PASSWORD --format raw
tdc fs-vault read-secret --secret-name db-prod --field DB_URL --format env
```
