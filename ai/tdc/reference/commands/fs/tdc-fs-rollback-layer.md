---
title: tdc fs rollback-layer
summary: Roll back a TiDB Cloud Filesystem layer.
---

# tdc fs rollback-layer

Rolls back changes in one layer without committing them to the base.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `tdc` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs rollback-layer
  --layer-id <string>
  [--dry-run]
  [--file-system-name <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## Options

- `--layer-id <string>`: The ID of the layer. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--file-system-name <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_NAME`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

- Roll back a layer:

    ```bash
    # Discard uncommitted changes and restore the layer's base view.
    tdc fs rollback-layer --file-system-name workspace --layer-id "<layer-id>"
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/tdc/reference/tdc-filesystem.md)
