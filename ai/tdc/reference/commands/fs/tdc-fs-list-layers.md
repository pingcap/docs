---
title: tdc fs list-layers
summary: List layers in a TiDB Cloud Filesystem.
---

# tdc fs list-layers

Lists layers for the selected Filesystem.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs list-layers
  [--file-system-name <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## Options

- `--file-system-name <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_NAME`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### List layers

```bash
tdc fs list-layers --file-system-name workspace
```

### List layers as text

```bash
tdc fs list-layers --file-system-name workspace --output text
```
