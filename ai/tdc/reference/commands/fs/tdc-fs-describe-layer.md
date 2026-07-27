---
title: tdc fs describe-layer
summary: Describe a layer in a TiDB Cloud Filesystem.
---

# tdc fs describe-layer

Describes one Filesystem layer.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs describe-layer
  --layer-id <string>
  [--file-system-name <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## Options

- `--layer-id <string>`: The ID of the specified file system layer. \[required]
- `--file-system-name <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_NAME`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Describe a layer

```bash
tdc fs describe-layer --file-system-name workspace --layer-id "<layer-id>"
```

### Render layer details as text

```bash
tdc fs describe-layer --file-system-name workspace --layer-id "<layer-id>" --output text
```
