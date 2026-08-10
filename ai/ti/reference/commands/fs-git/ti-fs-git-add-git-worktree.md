---
title: ti fs-git add-git-worktree
summary: Add a linked Git worktree in a mounted TiDB Cloud Filesystem.
---

# ti fs-git add-git-worktree

Adds a linked Git worktree from a base workspace.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

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
- `--blobless`: Require the base workspace to use blobless Git storage.
- `--branch-name <string>`: Create a branch for the linked worktree.
- `--commit-ish <string>`: Optional commit-ish for the linked worktree.
- `--detach`: Create a detached linked worktree.
- `--dry-run`: Validate the request without applying changes.
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TI_FS_TOKEN`.
- `--help`: Display help information.
- `--hydrate <string>`: Blobless hydrate mode: `auto`, `background`, `sync`, or `off`. \[default: auto]
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
