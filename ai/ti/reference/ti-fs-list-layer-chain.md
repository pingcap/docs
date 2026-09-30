---
title: ti fs list-layer-chain
summary: List the ancestry chain for a file system layer.
---

# ti fs list-layer-chain

Lists the parent-child layer chain from the root layer to a selected child layer, including each layer's sequence boundary.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Syntax

```text
ti fs list-layer-chain
  --layer-ref <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## Options

- `--layer-ref <string>`: Layer ID, unique name, or [tag reference](/ai/ti/reference/ti-filesystem.md#layer-references). \[required]
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the file system token. If omitted, the command uses the `TI_FS_TOKEN` environment variable. If neither is provided, the command uses the local token stored for the selected file system.
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Inspect a child timeline:

    ```bash
    # Render the root-to-tip ancestry as stable text columns.
    ti fs list-layer-chain --file-system-id <file-system-id> --layer-ref experiment-a --output text
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
- [`ti fs fork-layer`](/ai/ti/reference/ti-fs-fork-layer.md)
