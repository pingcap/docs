---
title: ti fs create-hardlink
summary: Create a hard link in a TiDB Cloud Filesystem.
---

# ti fs create-hardlink

Creates a hard link to an existing remote path. The command alias is `ti fs hardlink`.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

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
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TI_FS_TOKEN`.
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
