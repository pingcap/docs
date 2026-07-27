---
title: tdc fs drain-file-system
summary: Drain a mounted TiDB Cloud Filesystem.
---

# tdc fs drain-file-system

Flushes dirty FUSE state while leaving the mount online. The command alias is `tdc fs drain`.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs drain-file-system
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
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Drain pending writes

```bash
tdc fs drain-file-system --mount-path /path/to/workspace
```

### Drain with the alias and an explicit timeout

```bash
tdc fs drain --mount-path /path/to/workspace --timeout 30s
```
