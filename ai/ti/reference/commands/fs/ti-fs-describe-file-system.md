---
title: ti fs describe-file-system
summary: Describe a remote TiDB Cloud Filesystem.
---

# ti fs describe-file-system

Describes one remote Filesystem by its server-assigned ID. The response includes its authoritative display name, labels, placement, status, quota and usage, and the non-secret `has_local_token` hint. The command requires TiDB Cloud API credentials and does not use an FS token for authorization.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs describe-file-system
  --file-system-id <string>
  [--help]
  [--version]
```

## Options

- `--file-system-id <string>`: Set the immutable Filesystem ID. \[required]
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Describe a Filesystem:

    ```bash
    # Return remote status and whether this machine has a matching local token.
    ti fs describe-file-system --file-system-id <file-system-id>
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
