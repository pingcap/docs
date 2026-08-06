---
title: tdc fs list-file-systems
summary: List remote TiDB Cloud Filesystems in a region.
---

# tdc fs list-file-systems

Lists every Filesystem that the selected TiDB Cloud credentials can access in the effective region. `has_local_token` indicates whether this machine has a matching data-plane token.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `tdc` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs list-file-systems
  [--help]
  [--version]
```

## Options

- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

- List remotely managed Filesystems:

    ```bash
    # Return the remote inventory for the profile's region without exposing tokens.
    tdc fs list-file-systems
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/tdc/reference/tdc-filesystem.md)
