---
title: ti fs-git remove-git-worktree
summary: Remove a linked Git worktree from a mounted TiDB Cloud Filesystem.
---

# ti fs-git remove-git-worktree

Removes a linked Git worktree while preserving the shared Git data used by other worktrees.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

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
- `--fs-token <string>`: Set the file system token. If omitted, the command uses the `TI_FS_TOKEN` environment variable. If neither is provided, the command uses the local token stored for the selected file system.
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Remove a Git worktree:

    ```bash
    # Remove a clean linked worktree.
    ti fs-git remove-git-worktree --file-system-id <file-system-id> --worktree-path /path/to/workspace/tidb-feature
    ```

- Force removal of a Git worktree:

    ```bash
    # Discard local changes only after deciding that they are no longer needed.
    ti fs-git remove-git-worktree --file-system-id <file-system-id> --worktree-path /path/to/workspace/tidb-feature --force
    ```

## Related documentation

- [TiDB Cloud Filesystem Git CLI Command Reference](/ai/ti/reference/ti-filesystem-git.md)
