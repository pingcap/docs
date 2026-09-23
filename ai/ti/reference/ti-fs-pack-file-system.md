---
title: ti fs pack-file-system
summary: Pack local file system overlay state.
---

# ti fs pack-file-system

Packs selected [local overlay state](/ai/ti/reference/ti-filesystem.md#mount-profiles-and-local-overlays) into a remote archive.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Syntax

```text
ti fs pack-file-system
  [--archive-path <string>]
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--local-root <string>]
  [--mount-path <string>]
  [--mount-profile <string>]
  [--path <string>]
  [--remote-root <string>]
  [--version]
```

## Options

- `--archive-path <string>`: The path for the packed archive.
- `--dry-run`: Validate the request without applying changes.
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the file system token. If omitted, the command uses the `TI_FS_TOKEN` environment variable. If neither is provided, the command uses the local token stored for the selected file system.
- `--help`: Display help information.
- `--local-root <string>`: Local overlay root containing the overlay directory.
- `--mount-path <string>`: The local mounted path.
- `--mount-profile <string>`: Select a [mount profile](/ai/ti/reference/ti-filesystem.md#mount-profiles-and-local-overlays): `coding-agent`, `portable`, or `none`. If omitted, uses `none`.
- `--path <string>`: Local overlay path for packing; repeatable.
- `--remote-root <string>`: The TiDB Cloud file system root represented by the local overlay. \[default: /]
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Pack a mounted workspace:

    ```bash
    # Persist the local overlay associated with an existing mount.
    ti fs pack-file-system --file-system-id <file-system-id> --mount-path /path/to/workspace
    ```

- Pack explicit roots:

    ```bash
    # Create a portable archive from selected local and remote roots.
    ti fs pack-file-system --file-system-id <file-system-id> --local-root /path/to/local-root --remote-root /workspace --mount-profile portable
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
