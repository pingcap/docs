---
title: ti fs commit-layer
summary: Commit a TiDB Cloud Filesystem layer.
---

# ti fs commit-layer

Applies one layer to its base Filesystem.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs commit-layer
  --layer-id <string>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## Options

- `--layer-id <string>`: Layer ID. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TI_FS_TOKEN`.
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Commit a layer:

    ```bash
    # Apply the selected layer's changes to its base Filesystem view.
    ti fs commit-layer --file-system-id <file-system-id> --layer-id "<layer-id>"
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
