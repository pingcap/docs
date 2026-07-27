---
title: tdc fs describe-file-system
summary: Describe a locally registered TiDB Cloud Filesystem.
---

# tdc fs describe-file-system

Describes one locally registered Filesystem.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `tdc` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs describe-file-system
  --file-system-name <string>
  [--help]
  [--version]
```

## Options

- `--file-system-name <string>`: Set the file system name. \[required]
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

- Describe a Filesystem:

    ```bash
    # Return registration, endpoint, and region details for one Filesystem.
    tdc fs describe-file-system --file-system-name workspace
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/tdc/reference/tdc-filesystem.md)
