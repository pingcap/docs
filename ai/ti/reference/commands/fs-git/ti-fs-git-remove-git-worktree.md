---
title: ti fs-git remove-git-worktree
summary: Remove a linked Git worktree from a mounted TiDB Cloud Filesystem.
---

# ti fs-git remove-git-worktree

Removes a linked worktree without recursively deleting shared clean-tree data.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs-git remove-git-worktree
  --worktree-path <string>
  [--dry-run]
  [--file-system-id <string>]
  [--force]
  [--fs-token <string>]
  [--help]
  [--version]
```

## Options

- `--worktree-path <string>`: Mounted `ti fs` path of the linked worktree. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--force`: Remove even when the linked worktree has local changes.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TI_FS_TOKEN`.
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Remove a Git worktree:

    ```bash
    # Force removal when the isolated worktree still contains local changes.
    ti fs-git remove-git-worktree --file-system-id <file-system-id> --worktree-path /path/to/workspace/tidb-feature --force
    ```

## Related documentation

- [TiDB Cloud Filesystem Git CLI Command Reference](/ai/ti/reference/ti-filesystem-git.md)
