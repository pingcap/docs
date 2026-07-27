---
title: tdc fs list-files
summary: List files in a TiDB Cloud Filesystem.
---

# tdc fs list-files

Lists entries below a remote path. The command alias is `tdc fs ls`.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs list-files
  [--file-system-name <string>]
  [--fs-token <string>]
  [--help]
  [--path <string>]
  [--version]
```

## Options

- `--file-system-name <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_NAME`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--path <string>`: File system directory path. \[default: /]
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### List files

```bash
tdc fs list-files --file-system-name workspace --path /reports
```

### List files as text

```bash
tdc fs list-files --file-system-name workspace --path /reports --output text
```
