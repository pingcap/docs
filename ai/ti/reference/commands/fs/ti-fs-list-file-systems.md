---
title: ti fs list-file-systems
summary: List locally registered TiDB Cloud Filesystems.
---

# ti fs list-file-systems

Lists Filesystems registered in the selected local profile.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs list-file-systems
  [--help]
  [--version]
```

## Options

- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- List locally registered Filesystems:

    ```bash
    # Return the Filesystems registered under the selected local profile.
    ti fs list-file-systems
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
