---
title: ti fs create-hardlink
summary: Create a hard link in a TiDB Cloud Filesystem.
---

# ti fs create-hardlink

Creates a hard link to an existing remote path. The command alias is `ti fs hardlink`.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Syntax

```text
ti fs create-hardlink
  --link-path <string>
  --source-path <string>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## Options

- `--link-path <string>`: The file path for the hard link being created in the TiDB Cloud file system. \[required]
- `--source-path <string>`: The existing file path in the TiDB Cloud file system. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the Filesystem token. If omitted, the command uses the `TI_FS_TOKEN` environment variable. If neither is provided, the command uses the local token stored for the selected Filesystem.
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Create a hard link:

    ```bash
    # Expose the same remote file content at a second path.
    ti fs create-hardlink --file-system-id <file-system-id> --source-path /reports/final.md --link-path /reports/final-copy.md
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
