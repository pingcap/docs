---
title: tdc fs chmod-file
summary: Change file permissions in a TiDB Cloud Filesystem.
---

# tdc fs chmod-file

Changes POSIX mode metadata for a remote path. The command alias is `tdc fs chmod`.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `tdc` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs chmod-file
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
- `--file-system-id <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

- Change remote permission metadata:

    ```bash
    # Restrict the selected file to owner read and write access.
    tdc fs chmod-file --file-system-id <file-system-id> --path /reports/final.md --mode 0600
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/tdc/reference/tdc-filesystem.md)
