---
title: tdc fs-git remove-git-worktree
summary: Remove a linked Git worktree from a mounted TiDB Cloud Filesystem.
---

# tdc fs-git remove-git-worktree

Removes a linked worktree without recursively deleting shared clean-tree data.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs-git remove-git-worktree
  --worktree-path <string>
  [--dry-run]
  [--file-system-name <string>]
  [--force]
  [--fs-token <string>]
  [--help]
  [--version]
```

## Options

- `--worktree-path <string>`: Mounted tdc fs path of the linked worktree. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--file-system-name <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_NAME`.
- `--force`: Remove even when the linked worktree has local changes.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Preview worktree removal

```bash
tdc fs-git remove-git-worktree --file-system-name workspace --worktree-path /path/to/workspace/tidb-feature --dry-run
```

### Force worktree removal

```bash
tdc fs-git remove-git-worktree --file-system-name workspace --worktree-path /path/to/workspace/tidb-feature --force
```
