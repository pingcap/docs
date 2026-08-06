---
title: tdc fs read-file
summary: Read a file from a TiDB Cloud Filesystem.
---

# tdc fs read-file

Writes a remote file or byte range to stdout. The command alias is `tdc fs cat`.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `tdc` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs read-file
  --path <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--length <int64>]
  [--offset <int64>]
  [--version]
```

## Options

- `--path <string>`: File path in the selected file system. \[required]
- `--file-system-id <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--length <int64>`: Byte length for a ranged read.
- `--offset <int64>`: Zero-based byte offset for a ranged read.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

- Read a complete file:

    ```bash
    # Write the remote file contents directly to standard output.
    tdc fs read-file --file-system-id <file-system-id> --path /reports/report.md
    ```

- Read a byte range:

    ```bash
    # Fetch only the requested range from a large remote object.
    tdc fs read-file --file-system-id <file-system-id> --path /archives/large.bin --offset 1024 --length 4096
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/tdc/reference/tdc-filesystem.md)
