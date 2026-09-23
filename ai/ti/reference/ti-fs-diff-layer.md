---
title: ti fs diff-layer
summary: Show changes in a file system layer.
---

# ti fs diff-layer

Lists changes in one layer, optionally up to a sequence number.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Syntax

```text
ti fs diff-layer
  --layer-id <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--max-seq <int64>]
  [--version]
```

## Options

- `--layer-id <string>`: The ID of the layer. \[required]
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the file system token. If omitted, the command uses the `TI_FS_TOKEN` environment variable. If neither is provided, the command uses the local token stored for the selected file system.
- `--help`: Display help information.
- `--max-seq <int64>`: The highest layer sequence to include; 0 includes all sequences.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Show all layer changes:

    ```bash
    # Return the complete ordered change set for the selected layer.
    ti fs diff-layer --file-system-id <file-system-id> --layer-id "<layer-id>"
    ```

- Show an earlier layer view:

    ```bash
    # Limit the diff to changes at or before a sequence number.
    ti fs diff-layer --file-system-id <file-system-id> --layer-id "<layer-id>" --max-seq 100
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
