---
title: ti fs find-files
summary: Find files in a TiDB Cloud Filesystem.
---

# ti fs find-files

Finds remote paths by name, type, tag, size, or modification time. The command alias is `ti fs find`.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs find-files
  [--file-name-pattern <string>]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--layer-id <string>]
  [--limit <int32>]
  [--max-size-bytes <int64>]
  [--min-size-bytes <int64>]
  [--newer <string>]
  [--older <string>]
  [--path <string>]
  [--resource-type <string>]
  [--tag <string>]
  [--version]
```

## Options

- `--file-name-pattern <string>`: File name pattern filter, such as `*.md`.
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TI_FS_TOKEN`.
- `--help`: Display help information.
- `--layer-id <string>`: Search files and directories within a specific file system layer.
- `--limit <int32>`: Maximum number of results; 0 uses the service default.
- `--max-size-bytes <int64>`: Maximum file size in bytes.
- `--min-size-bytes <int64>`: Minimum file size in bytes.
- `--newer <string>`: Only return files newer than the filter.
- `--older <string>`: Only return files older than the filter.
- `--path <string>`: File path prefix. \[default: /]
- `--resource-type <string>`: Resource type filter: `file` or `directory`.
- `--tag <string>`: Tag filter.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Find files by name:

    ```bash
    # Locate Markdown files recursively under the selected remote path.
    ti fs find-files --file-system-id <file-system-id> --path /workspace --file-name-pattern "*.md"
    ```

- Find files by metadata:

    ```bash
    # Select tagged files that also meet a minimum size threshold.
    ti fs find-files --file-system-id <file-system-id> --path /workspace --tag stage=review --min-size-bytes 1024
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
