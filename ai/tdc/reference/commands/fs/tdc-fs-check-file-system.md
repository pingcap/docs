---
title: tdc fs check-file-system
summary: Check TiDB Cloud Filesystem connectivity.
---

# tdc fs check-file-system

Checks Filesystem selection, endpoint resolution, credentials, and companion access.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `tdc` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs check-file-system
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## Options

- `--file-system-id <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

- Check Filesystem connectivity:

    ```bash
    # Verify that the selected token can reach and read the Filesystem root.
    tdc fs check-file-system --file-system-id <file-system-id>
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/tdc/reference/tdc-filesystem.md)
