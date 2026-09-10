---
title: ti fs delete-layer
summary: Abandon a TiDB Cloud Filesystem layer.
---

# ti fs delete-layer

Logically abandons a layer. The command does not physically erase layer history and never enables cascade implicitly.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs delete-layer
  --layer-ref <string>
  [--cascade]
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## Options

- `--layer-ref <string>`: Layer ID, unique name, or supported tag reference. \[required]
- `--cascade`: Abandon live descendants before abandoning the selected layer.
- `--dry-run`: Validate the request without applying changes.
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TI_FS_TOKEN`.
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Abandon a rejected leaf timeline:

    ```bash
    # Deletion fails when the selected layer still has live descendants.
    ti fs delete-layer --file-system-id <file-system-id> --layer-ref experiment-a
    ```

- Abandon a test-owned subtree:

    ```bash
    # Cascade is explicit and abandons descendants before the selected layer.
    ti fs delete-layer --file-system-id <file-system-id> --layer-ref experiment-root --cascade
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
- [`ti fs list-layer-chain`](/ai/ti/reference/commands/fs/ti-fs-list-layer-chain.md)
