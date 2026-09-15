---
title: ti fs move-file
summary: Move a file in a TiDB Cloud Filesystem.
---

# ti fs move-file

Moves or renames a remote path. The command alias is `ti fs mv`.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Syntax

```text
ti fs move-file
  --from-remote <string>
  --to-remote <string>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--overwrite]
  [--version]
```

## Options

- `--from-remote <string>`: Source file path. \[required]
- `--to-remote <string>`: Destination file path. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the Filesystem token. If omitted, the command uses the `TI_FS_TOKEN` environment variable. If neither is provided, the command uses the local token stored for the selected Filesystem.
- `--help`: Display help information.
- `--overwrite`: Replace an existing destination file.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Move a remote file:

    ```bash
    # Rename or relocate an object entirely within the selected Filesystem.
    ti fs move-file --file-system-id <file-system-id> --from-remote /draft.md --to-remote /reports/final.md
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
