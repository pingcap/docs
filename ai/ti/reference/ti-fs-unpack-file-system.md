---
title: ti fs unpack-file-system
summary: Restore local Filesystem overlay state.
---

# ti fs unpack-file-system

Restores [local overlay state](/ai/ti/reference/ti-filesystem.md#mount-profiles-and-local-overlays) from a remote archive.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Syntax

```text
ti fs unpack-file-system
  [--archive-path <string>]
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--local-root <string>]
  [--mount-path <string>]
  [--mount-profile <string>]
  [--no-replace]
  [--remote-root <string>]
  [--version]
```

## Options

- `--archive-path <string>`: The path for the packed archive.
- `--dry-run`: Validate the request without applying changes.
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the Filesystem token. If omitted, the command uses the `TI_FS_TOKEN` environment variable. If neither is provided, the command uses the local token stored for the selected Filesystem.
- `--help`: Display help information.
- `--local-root <string>`: The local overlay root to restore into.
- `--mount-path <string>`: The local mounted path.
- `--mount-profile <string>`: Select a [mount profile](/ai/ti/reference/ti-filesystem.md#mount-profiles-and-local-overlays): `coding-agent`, `portable`, or `none`. If omitted, uses `none`.
- `--no-replace`: Merge archive entries instead of replacing them.
- `--remote-root <string>`: Find the packed archive under the specified root path when `--archive-path` is omitted. \[default: /]
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Unpack into a mounted workspace:

    ```bash
    # Restore the portable archive associated with an existing mount.
    ti fs unpack-file-system --file-system-id <file-system-id> --mount-path /path/to/workspace
    ```

- Unpack explicit roots without replacement:

    ```bash
    # Restore missing files while preserving existing destination entries.
    ti fs unpack-file-system --file-system-id <file-system-id> --local-root /path/to/local-root --remote-root /workspace --mount-profile portable --no-replace
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
