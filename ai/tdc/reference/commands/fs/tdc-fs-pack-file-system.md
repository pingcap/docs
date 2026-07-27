---
title: tdc fs pack-file-system
summary: Pack local Filesystem overlay state.
---

# tdc fs pack-file-system

Packs selected local overlay state into a remote archive.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `tdc` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs pack-file-system
  [--archive-path <string>]
  [--dry-run]
  [--file-system-name <string>]
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
- `--file-system-name <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_NAME`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--local-root <string>`: Local overlay root containing the overlay directory.
- `--mount-path <string>`: The local mounted path.
- `--mount-profile <string>`: The mount profile: `coding-agent`, `portable`, or `none`. If omitted, uses `none`.
- `--path <string>`: Local overlay path for packing; repeatable.
- `--remote-root <string>`: The TiDB Cloud file system root represented by the local overlay. \[default: /]
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

- Pack a mounted workspace:

    ```bash
    # Persist the local overlay associated with an existing mount.
    tdc fs pack-file-system --file-system-name workspace --mount-path /path/to/workspace
    ```

- Pack explicit roots:

    ```bash
    # Create a portable archive from selected local and remote roots.
    tdc fs pack-file-system --file-system-name workspace --local-root ./overlay --remote-root /workspace --mount-profile portable
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/tdc/reference/tdc-filesystem.md)
