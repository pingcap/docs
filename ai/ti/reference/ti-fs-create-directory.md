---
title: ti fs create-directory
summary: Create a directory in a file system.
---

# ti fs create-directory

Creates a remote directory. The command alias is `ti fs mkdir`.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Syntax

```text
ti fs create-directory
  --path <string>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--mode <string>]
  [--version]
```

## Options

- `--path <string>`: The file system path of the directory to create. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the file system token. If omitted, the command uses the `TI_FS_TOKEN` environment variable. If neither is provided, the command uses the local token stored for the selected file system.
- `--help`: Display help information.
- `--mode <string>`: The directory mode as an octal value such as 0755.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Create a remote directory:

    ```bash
    # Create the directory with explicit POSIX permission metadata.
    ti fs create-directory --file-system-id <file-system-id> --path /reports/archive --mode 0755
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
