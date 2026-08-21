---
title: ti fs list-layer-chain
summary: List the ancestry chain for a TiDB Cloud Filesystem layer.
---

# ti fs list-layer-chain

Lists the pinned ancestry from the root layer to a selected child, including each frame's sequence boundary.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

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

- `--layer-ref <string>`: Layer ID, unique name, or supported tag reference. \[required]
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TI_FS_TOKEN`.
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
- [`ti fs fork-layer`](/ai/ti/reference/commands/fs/ti-fs-fork-layer.md)
