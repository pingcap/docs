---
title: Manage Git Workspaces on TiDB Cloud Filesystem
summary: Learn how to clone, hydrate, create linked worktrees, and remove Git workspaces on a mounted TiDB Cloud Filesystem.
---

# Manage Git Workspaces on TiDB Cloud Filesystem

Use `ti fs-git` to accelerate Git workspace setup on a mounted TiDB Cloud Filesystem while continuing to use ordinary Git commands for daily work.

## Prerequisites

- [Install and configure TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md).
- [Mount a TiDB Cloud Filesystem](/ai/ti/guides/mount-filesystem.md) through FUSE.
- Select the mounted Filesystem by passing `--file-system-id`, setting `TI_FS_FILE_SYSTEM_ID`, or supplying an FS token that identifies it. Provide an FS token with Git workspace permissions.
- Install Git and configure repository credentials independently.

## Clone a workspace

```shell
ti fs-git clone-git-workspace \
  --repo-url https://github.com/pingcap/tidb.git \
  --target-path /path/to/workspace/tidb
```

For a large repository, add `--blobless --hydrate background` to make the directory tree available immediately. The CLI starts a background process that downloads clean file content and Git objects after the clone command returns. Use `--hydrate sync` when your workflow requires hydration to finish before the command returns.

## Hydrate an existing workspace

If a workspace was cloned with `--blobless`, you can explicitly fetch the missing Git objects by running `hydrate-git-workspace`:

```shell
ti fs-git hydrate-git-workspace \
  --target-path /path/to/workspace/tidb \
  --timeout 30m
```

Hydration fetches missing blob data from the remote repository without discarding your working-tree changes.

## Add and use a linked worktree

```shell
ti fs-git add-git-worktree \
  --base-path /path/to/workspace/tidb \
  --worktree-path /path/to/workspace/tidb-feature \
  --branch-name feature-x
```

After creation, use ordinary Git commands in the linked worktree.

## Remove a worktree

```shell
ti fs-git remove-git-worktree \
  --worktree-path /path/to/workspace/tidb-feature
```

The CLI checks for uncommitted changes and rejects the removal if the worktree is dirty. Use `--force` only after you decide that local changes in the worktree can be discarded.

> **Note:**
>
> Before terminating an ephemeral machine, preserve required changes, remove unused worktrees, and gracefully unmount the Filesystem.

## What's next

- [Prepare a Git Workspace for Agents on TiDB Cloud Filesystem](/ai/ti/guides/ti-git-workspace-for-agents-example.md)
- [TiDB Cloud Filesystem Git CLI Command Reference](/ai/ti/reference/ti-filesystem-git.md)
