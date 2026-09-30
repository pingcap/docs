---
title: ti fs-git add-git-worktree
summary: Add a linked Git worktree in a mounted TiDB Cloud Filesystem.
---

# ti fs-git add-git-worktree

Adds a linked Git worktree from a base workspace.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Syntax

```text
ti fs-git add-git-worktree
  --base-path <string>
  --worktree-path <string>
  [--blobless]
  [--branch-name <string>]
  [--commit-ish <string>]
  [--detach]
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--hydrate <string>]
  [--version]
```

## Options

- `--base-path <string>`: The mounted file system path of the base Git workspace. \[required]
- `--worktree-path <string>`: The mounted file system path for the linked worktree. \[required]
- `--blobless`: Verify that the base workspace uses blobless Git storage. This option does not convert a non-blobless workspace.
- `--branch-name <string>`: Create a branch for the linked worktree.
- `--commit-ish <string>`: Optional commit-ish for the linked worktree.
- `--detach`: Create a detached linked worktree.
- `--dry-run`: Validate the request without applying changes.
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the file system token. If omitted, the command uses the `TI_FS_TOKEN` environment variable. If neither is provided, the command uses the local token stored for the selected file system.
- `--help`: Display help information.
- `--hydrate <string>`: Clean-data hydration mode: `auto`, `background`, `sync`, or `off`. With `auto`, a worktree linked to a blobless base hydrates in the background, while a worktree linked to a non-blobless base does not run a separate hydration step. `background` and `sync` require a blobless base; `off` skips hydration. \[default: auto]
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Create a worktree on a new branch:

    ```bash
    # Give an agent an isolated branch while sharing the base Git object store.
    ti fs-git add-git-worktree --file-system-id <file-system-id> --base-path /path/to/workspace/tidb --worktree-path /path/to/workspace/tidb-feature --branch-name feature-x
    ```

- Create a detached worktree:

    ```bash
    # Inspect a commit without creating or switching a branch.
    ti fs-git add-git-worktree --file-system-id <file-system-id> --base-path /path/to/workspace/tidb --worktree-path /path/to/workspace/tidb-review --commit-ish origin/main --detach
    ```

## Related documentation

- [TiDB Cloud Filesystem Git CLI Command Reference](/ai/ti/reference/ti-filesystem-git.md)
