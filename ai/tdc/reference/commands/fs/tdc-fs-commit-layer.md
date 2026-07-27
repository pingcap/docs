---
title: tdc fs commit-layer
summary: Commit a TiDB Cloud Filesystem layer.
---

# tdc fs commit-layer

Applies one layer to its base Filesystem.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs commit-layer
  --layer-id <string>
  [--dry-run]
  [--file-system-name <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## Options

- `--layer-id <string>`: Layer ID. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--file-system-name <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_NAME`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Preview a layer commit

```bash
tdc fs commit-layer --file-system-name workspace --layer-id "<layer-id>" --dry-run
```

### Commit a layer

```bash
tdc fs commit-layer --file-system-name workspace --layer-id "<layer-id>"
```
