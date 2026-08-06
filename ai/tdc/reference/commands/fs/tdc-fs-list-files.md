---
title: tdc fs list-files
summary: List files in a TiDB Cloud Filesystem.
---

# tdc fs list-files

Lists entries below a remote path. The command alias is `tdc fs ls`.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `tdc` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs list-files
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--path <string>]
  [--version]
```

## Options

- `--file-system-id <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--path <string>`: File system directory path. \[default: /]
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

- List a remote directory:

    ```bash
    # Return the entries under a specific Filesystem path.
    tdc fs list-files --file-system-id <file-system-id> --path /reports
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/tdc/reference/tdc-filesystem.md)
