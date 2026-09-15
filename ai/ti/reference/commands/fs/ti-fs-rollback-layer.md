---
title: ti fs rollback-layer
summary: Roll back a TiDB Cloud Filesystem layer.
---

# ti fs rollback-layer

Rolls back changes in one layer without committing them to the base.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Syntax

```text
ti fs rollback-layer
  --layer-id <string>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## Options

- `--layer-id <string>`: The ID of the layer. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the Filesystem token. If omitted, the command uses the `TI_FS_TOKEN` environment variable. If neither is provided, the command uses the local token stored for the selected Filesystem.
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Roll back a layer:

    ```bash
    # Discard uncommitted changes and restore the layer's base view.
    ti fs rollback-layer --file-system-id <file-system-id> --layer-id "<layer-id>"
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
