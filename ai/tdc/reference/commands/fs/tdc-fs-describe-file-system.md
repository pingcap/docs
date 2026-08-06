---
title: tdc fs describe-file-system
summary: Describe a remote TiDB Cloud Filesystem.
---

# tdc fs describe-file-system

Describes one remote Filesystem by its server-assigned ID. The command does not require a locally stored FS token.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `tdc` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs describe-file-system
  --file-system-id <string>
  [--help]
  [--version]
```

## Options

- `--file-system-id <string>`: Set the file system ID. \[required]
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

- Describe a Filesystem:

    ```bash
    # Return remote status and whether this machine has a matching local token.
    tdc fs describe-file-system --file-system-id <file-system-id>
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/tdc/reference/tdc-filesystem.md)
