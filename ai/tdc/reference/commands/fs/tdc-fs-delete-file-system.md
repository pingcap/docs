---
title: tdc fs delete-file-system
summary: Delete a TiDB Cloud Filesystem.
---

# tdc fs delete-file-system

Requests asynchronous Filesystem deletion and removes its local registration.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs delete-file-system
  --file-system-name <string>
  [--dry-run]
  [--fs-token <string>]
  [--help]
  [--version]
```

## Options

- `--file-system-name <string>`: Set the file system name. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Preview file system deletion

```bash
tdc fs delete-file-system --file-system-name workspace --dry-run
```

### Delete a file system

```bash
tdc fs delete-file-system --file-system-name workspace
```
