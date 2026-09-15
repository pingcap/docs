---
title: ti fs check-file-system
summary: Check TiDB Cloud Filesystem connectivity.
---

# ti fs check-file-system

Verifies that the selected Filesystem is correctly configured and accessible, including its region, credentials, and file access.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Syntax

```text
ti fs check-file-system
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## Options

- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the Filesystem token. If omitted, the command uses the `TI_FS_TOKEN` environment variable. If neither is provided, the command uses the local token stored for the selected Filesystem.
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Check Filesystem connectivity:

    ```bash
    # Verify that the selected token can reach and read the Filesystem root.
    ti fs check-file-system --file-system-id <file-system-id>
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
