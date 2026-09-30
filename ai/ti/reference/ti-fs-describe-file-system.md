---
title: ti fs describe-file-system
summary: Describe a remote TiDB Cloud Filesystem.
---

# ti fs describe-file-system

Shows detailed information about a file system, including its display name, labels, placement, status, quota, and usage. This command requires TiDB Cloud API credentials and does not use a file system token.

The output includes `has_local_token`, which indicates whether this machine has a matching local token. When available, quota data includes media and video extraction limits and usage.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Syntax

```text
ti fs describe-file-system
  --file-system-id <string>
  [--help]
  [--version]
```

## Options

- `--file-system-id <string>`: Set the immutable file system ID. \[required]
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Describe a file system:

    ```bash
    # Return remote status and whether this machine has a matching local token.
    ti fs describe-file-system --file-system-id <file-system-id>
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
