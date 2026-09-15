---
title: ti fs drain-file-system
summary: Drain a mounted TiDB Cloud Filesystem.
---

# ti fs drain-file-system

Flushes pending writes from a FUSE mount to the remote Filesystem while keeping the mount online. The command alias is `ti fs drain`. For a WebDAV mount, stop writers and use `ti fs unmount-file-system`; running `drain-file-system` for it returns an error.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Syntax

```text
ti fs drain-file-system
  --mount-path <string>
  [--dry-run]
  [--help]
  [--timeout <duration>]
  [--version]
```

## Options

- `--mount-path <string>`: Local FUSE mount path. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--help`: Display help information.
- `--timeout <duration>`: The time to wait for dirty handles and pending writes to drain. \[default: `30s`]
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Drain pending writes:

    ```bash
    # Flush queued FUSE writes while leaving the Filesystem mounted.
    ti fs drain-file-system --mount-path /path/to/workspace --timeout 30s
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
