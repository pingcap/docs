---
title: tdc fs describe-layer
summary: Describe a layer in a TiDB Cloud Filesystem.
---

# tdc fs describe-layer

Describes one Filesystem layer.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `tdc` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs describe-layer
  --layer-id <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## Options

- `--layer-id <string>`: The ID of the specified file system layer. \[required]
- `--file-system-id <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

- Describe a layer:

    ```bash
    # Inspect one layer's base root, state, durability, and metadata.
    tdc fs describe-layer --file-system-id <file-system-id> --layer-id "<layer-id>"
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/tdc/reference/tdc-filesystem.md)
