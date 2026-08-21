---
title: ti fs create-symlink
summary: Create a symbolic link in a TiDB Cloud Filesystem.
---

# ti fs create-symlink

Creates a symbolic link. The command alias is `ti fs symlink`.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs create-symlink
  --link-path <string>
  --target <string>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## Options

- `--link-path <string>`: The file path for the created symbolic link. \[required]
- `--target <string>`: The actual file path being linked to. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TI_FS_TOKEN`.
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Create a symbolic link:

    ```bash
    # Create a relative symbolic link inside the remote namespace.
    ti fs create-symlink --file-system-id <file-system-id> --target final.md --link-path /reports/latest.md
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
