---
title: tdc fs create-file-system
summary: Create a TiDB Cloud Filesystem.
---

# tdc fs create-file-system

Creates a Filesystem. `--wait` waits until data-plane access is ready.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs create-file-system
  --file-system-name <string>
  [--dry-run]
  [--help]
  [--version]
  [--wait]
```

## Options

- `--file-system-name <string>`: Set the file system name. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--help`: Display help information.
- `--version`: Display tdc version information.
- `--wait`: Wait until the created file system is active.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Create a file system and wait until it is ready

```bash
tdc fs create-file-system --file-system-name workspace --wait
```

### Preview file system creation

```bash
tdc fs create-file-system --file-system-name workspace --dry-run
```
