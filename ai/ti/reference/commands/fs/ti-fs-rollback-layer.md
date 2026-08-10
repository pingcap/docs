---
title: ti fs rollback-layer
summary: Roll back a TiDB Cloud Filesystem layer.
---

# ti fs rollback-layer

Rolls back changes in one layer without committing them to the base.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

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
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TI_FS_TOKEN`.
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
