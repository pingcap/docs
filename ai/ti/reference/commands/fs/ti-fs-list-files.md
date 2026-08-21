---
title: ti fs list-files
summary: List files in a TiDB Cloud Filesystem.
---

# ti fs list-files

Lists entries below a remote path. The command alias is `ti fs ls`.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs list-files
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--path <string>]
  [--version]
```

## Options

- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TI_FS_TOKEN`.
- `--help`: Display help information.
- `--path <string>`: File system directory path. \[default: /]
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- List a remote directory:

    ```bash
    # Return the entries under a specific Filesystem path.
    ti fs list-files --file-system-id <file-system-id> --path /reports
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
