---
title: tdc fs-git add-git-worktree
summary: Add a linked Git worktree in a mounted TiDB Cloud Filesystem.
---

# tdc fs-git add-git-worktree

Adds a linked Git worktree from a base workspace.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs-git add-git-worktree
    --base-path <string>
    --worktree-path <string>
    [--blobless]
    [--branch-name <string>]
    [--commit-ish <string>]
    [--detach]
    [--dry-run]
    [--file-system-name <string>]
    [--fs-token <string>]
    [--help]
    [--hydrate <string>]
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
tdc fs-git add-git-worktree --base-path /path/to/workspace/tidb --worktree-path /path/to/workspace/tidb-feature --branch-name feature-x
tdc fs-git add-git-worktree --base-path /path/to/workspace/tidb --worktree-path /path/to/workspace/tidb-review --commit-ish origin/main --detach
```
