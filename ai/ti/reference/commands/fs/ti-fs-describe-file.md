---
title: ti fs describe-file
summary: Describe a file in a TiDB Cloud Filesystem.
---

# ti fs describe-file

Describes metadata for one remote path. The command alias is `ti fs stat`.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs describe-file
  --path <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## Options

- `--path <string>`: File or directory path in the TiDB Cloud file system. \[required]
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TI_FS_TOKEN`.
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Describe a remote file:

    ```bash
    # Inspect file size, metadata, tags, and revision information.
    ti fs describe-file --file-system-id <file-system-id> --path /reports/report.md
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
