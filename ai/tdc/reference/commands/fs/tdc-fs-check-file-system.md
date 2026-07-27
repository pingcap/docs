---
title: tdc fs check-file-system
summary: Check TiDB Cloud Filesystem connectivity.
---

# tdc fs check-file-system

Checks Filesystem selection, endpoint resolution, credentials, and companion access.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs check-file-system
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

### Check file system connectivity

```bash
tdc fs check-file-system --file-system-name workspace
```

### Render the check result as text

```bash
tdc fs check-file-system --file-system-name workspace --output text
```
