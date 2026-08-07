---
title: tdc fs diff-layer
summary: Show changes in a TiDB Cloud Filesystem layer.
---

# tdc fs diff-layer

Lists changes in one layer, optionally up to a sequence number.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `tdc` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs diff-layer
  --layer-id <string>
  [--file-system-name <string>]
  [--fs-token <string>]
  [--help]
  [--max-seq <int64>]
  [--version]
```

## Options

- `--layer-id <string>`: The ID of the layer. \[required]
- `--file-system-name <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_NAME`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--max-seq <int64>`: The highest layer sequence to include; 0 includes all layers.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

- Show all layer changes:

    ```bash
    # Return the complete ordered change set for the selected layer.
    tdc fs diff-layer --file-system-name workspace --layer-id "<layer-id>"
    ```

- Show an earlier layer view:

    ```bash
    # Limit the diff to changes at or before a sequence number.
    tdc fs diff-layer --file-system-name workspace --layer-id "<layer-id>" --max-seq 100
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/tdc/reference/tdc-filesystem.md)
