---
title: ti fs delete-file-system
summary: Delete a TiDB Cloud Filesystem.
---

# ti fs delete-file-system

Requests asynchronous Filesystem deletion and removes its local registration.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs delete-file-system
  --file-system-name <string>
  [--dry-run]
  [--fs-token <string>]
  [--help]
  [--version]
```

## Options

- `--file-system-name <string>`: Set the file system name. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TI_FS_TOKEN`.
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Delete a Filesystem:

    ```bash
    # Request asynchronous deletion and remove its local registration after acceptance.
    ti fs delete-file-system --file-system-name workspace
    ```

- Preview Filesystem deletion:

    ```bash
    # Validate the selected Filesystem without sending the deletion request.
    ti fs delete-file-system --file-system-name workspace --dry-run
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
