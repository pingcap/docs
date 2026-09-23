---
title: ti fs delete-file
summary: Delete a file from a file system.
---

# ti fs delete-file

Deletes a remote file or directory. The command alias is `ti fs rm`.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Syntax

```text
ti fs delete-file
  --path <string>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--recursive]
  [--version]
```

## Options

- `--path <string>`: File or directory path in the TiDB Cloud file system. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the file system token. If omitted, the command uses the `TI_FS_TOKEN` environment variable. If neither is provided, the command uses the local token stored for the selected file system.
- `--help`: Display help information.
- `--recursive`: Delete a directory recursively.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Delete a remote file:

    ```bash
    # Remove one object from the selected file system.
    ti fs delete-file --file-system-id <file-system-id> --path /reports/obsolete.md
    ```

- Delete a directory recursively:

    ```bash
    # Remove a directory and all of its descendants in one request.
    ti fs delete-file --file-system-id <file-system-id> --path /scratch --recursive
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
