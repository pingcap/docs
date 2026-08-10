---
title: ti fs describe-file-system
summary: Describe a locally registered TiDB Cloud Filesystem.
---

# ti fs describe-file-system

Describes one locally registered Filesystem.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs describe-file-system
  --file-system-name <string>
  [--help]
  [--version]
```

## Options

- `--file-system-name <string>`: Set the file system name. \[required]
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Describe a Filesystem:

    ```bash
    # Return registration, endpoint, and region details for one Filesystem.
    ti fs describe-file-system --file-system-name workspace
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
