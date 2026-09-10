---
title: ti fs chmod-file
summary: Change file permissions in a TiDB Cloud Filesystem.
---

# ti fs chmod-file

Changes POSIX mode metadata for a remote path. The command alias is `ti fs chmod`.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs chmod-file
  --mode <string>
  --path <string>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## Options

- `--mode <string>`: The permission mode as an octal value such as 0644. \[required]
- `--path <string>`: File or directory path. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TI_FS_TOKEN`.
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Change remote permission metadata:

    ```bash
    # Restrict the selected file to owner read and write access.
    ti fs chmod-file --file-system-id <file-system-id> --path /reports/final.md --mode 0600
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
