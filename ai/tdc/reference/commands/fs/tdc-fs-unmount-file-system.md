---
title: tdc fs unmount-file-system
summary: Unmount a TiDB Cloud Filesystem.
---

# tdc fs unmount-file-system

Gracefully flushes and unmounts a background mount. The command alias is `tdc fs umount`.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `tdc` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs unmount-file-system
  --mount-path <string>
  [--dry-run]
  [--force]
  [--help]
  [--ignore-absent]
  [--no-auto-pack]
  [--pack-archive-path <string>]
  [--timeout <duration>]
  [--version]
```

## Options

- `--mount-path <string>`: The local mounted path. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--force`: Kill the mount process if graceful unmount times out.
- `--help`: Display help information.
- `--ignore-absent`: Return success when no file system mount state exists for the specified path.
- `--no-auto-pack`: Skip the portable mount profile's default auto-pack action.
- `--pack-archive-path <string>`: Pack archive to write after unmount.
- `--timeout <duration>`: Time to wait for the mount process to exit. \[default: `30s`]
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

- Unmount a Filesystem:

    ```bash
    # Gracefully flush pending writes and detach the Filesystem mount.
    tdc fs unmount-file-system --mount-path /path/to/workspace
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/tdc/reference/tdc-filesystem.md)
