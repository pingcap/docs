---
title: tdc fs unpack-file-system
summary: Restore local Filesystem overlay state.
---

# tdc fs unpack-file-system

Restores local overlay state from a remote archive.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs unpack-file-system
  [--archive-path <string>]
  [--dry-run]
  [--file-system-name <string>]
  [--fs-token <string>]
  [--help]
  [--local-root <string>]
  [--mount-path <string>]
  [--mount-profile <string>]
  [--no-replace]
  [--remote-root <string>]
  [--version]
```

## Options

- `--archive-path <string>`: The path for the packed archive.
- `--dry-run`: Validate the request without applying changes.
- `--file-system-name <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_NAME`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--local-root <string>`: The local overlay root to restore into.
- `--mount-path <string>`: The local mounted path.
- `--mount-profile <string>`: Mount profile: `coding-agent`, `portable`, or `none`. If omitted, uses `none`.
- `--no-replace`: Merge archive entries instead of replacing them.
- `--remote-root <string>`: Find the packed archive under the specified root path when `--archive-path` is omitted. \[default: /]
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Unpack into a mounted workspace

```bash
tdc fs unpack-file-system --file-system-name workspace --mount-path /path/to/workspace
```

### Unpack explicit roots without replacing files

```bash
tdc fs unpack-file-system --file-system-name workspace --local-root ./overlay --remote-root /workspace --mount-profile portable --no-replace
```
