---
title: tdc fs create-directory
summary: Create a directory in a TiDB Cloud Filesystem.
---

# tdc fs create-directory

Creates a remote directory. The command alias is `tdc fs mkdir`.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs create-directory
  --path <string>
  [--dry-run]
  [--file-system-name <string>]
  [--fs-token <string>]
  [--help]
  [--mode <string>]
  [--version]
```

## Options

- `--path <string>`: The file system path of the directory to create. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--file-system-name <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_NAME`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--mode <string>`: The directory mode as an octal value such as 0755.
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Create a directory

```bash
tdc fs create-directory --file-system-name workspace --path /reports/archive --mode 0755
```

### Preview directory creation with the alias

```bash
tdc fs mkdir --file-system-name workspace --path /reports/review --dry-run
```
