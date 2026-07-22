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
    [--debug]
    [--output <string>]
    [--profile <string>]
    [--query <string>]
    [--region <string>]
```

Filesystem selection can come from `--file-system-name`, `TDC_FS_FILE_SYSTEM_NAME`, or the selected profile. For shared global flags, see [tdc CLI Reference](/ai/tdc/reference/tdc-cli-reference.md).

## Examples

```shell
tdc fs-git remove-git-worktree --worktree-path /path/to/workspace/tidb-feature --dry-run
tdc fs-git remove-git-worktree --worktree-path /path/to/workspace/tidb-feature --force
```
