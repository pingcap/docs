---
title: tdc fs-git hydrate-git-workspace
summary: Hydrate clean Git objects in a tdc Git workspace.
---

# tdc fs-git hydrate-git-workspace

Hydrates clean Git objects for an existing tdc Git workspace.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs-git hydrate-git-workspace
  --target-path <string>
  [--file-system-name <string>]
  [--fs-token <string>]
  [--help]
  [--timeout <duration>]
  [--version]
```

## Options

- `--target-path <string>`: Mounted tdc fs workspace path. \[required]
- `--file-system-name <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_NAME`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--timeout <duration>`: Maximum hydrate duration. \[default: `30m0s`]
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Hydrate a Git workspace

```bash
tdc fs-git hydrate-git-workspace --file-system-name workspace --target-path /path/to/workspace/tidb
```

### Hydrate with an explicit timeout

```bash
tdc fs-git hydrate-git-workspace --file-system-name workspace --target-path /path/to/workspace/tidb --timeout 30m
```
