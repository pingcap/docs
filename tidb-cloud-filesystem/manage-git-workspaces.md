---
title: Manage Git Workspaces on TiDB Cloud Filesystem
summary: Learn how to clone, hydrate, create linked worktrees, and remove Git workspaces on a mounted TiDB Cloud Filesystem.
aliases: ['/ai/manage-git-workspaces']
---

# Manage Git Workspaces on TiDB Cloud Filesystem

Use `ti fs-git` when you want a Git workspace on a mounted TiDB Cloud Filesystem without waiting for all file content to download before work begins. Unlike a regular `git clone` into the mount, the CLI can combine a blobless clone with background hydration. Continue to use ordinary Git commands for daily work after setup.

## Prerequisites

- [Install TiDB Cloud CLI](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-the-cli).
- [Mount a TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-mount.md) through FUSE.
- For the commands below, set `TI_FS_FILE_SYSTEM_ID` to the mounted Filesystem ID and use its locally stored FS token. Alternatively, set `TI_FS_TOKEN` and `TI_REGION_CODE` for token-only access; the token identifies the Filesystem. To select a Filesystem per command instead, add `--file-system-id "<file-system-id>"` to each command. Use a token with Git workspace permissions. See [Authorization](/tidb-cloud-filesystem/filesystem-authorization.md#understand-local-selection) for selection details.
- Install Git and configure repository credentials independently.

## Clone a workspace

```shell
ti fs-git clone-git-workspace \
  --repo-url https://github.com/pingcap/tidb.git \
  --target-path /path/to/workspace/tidb
```

For a large repository, add `--blobless --hydrate background` to make the directory tree available immediately. A blobless clone initially fetches Git history and tree metadata without downloading all file contents. The CLI starts a background process that downloads clean file content and Git objects after the clone command returns. Use `--hydrate sync` when your workflow requires hydration to finish before the command returns.

## Hydrate an existing workspace

If a workspace was cloned with `--blobless`, you can explicitly fetch the missing Git objects by running `hydrate-git-workspace`:

```shell
ti fs-git hydrate-git-workspace \
  --target-path /path/to/workspace/tidb \
  --timeout 30m
```

Hydration fetches missing blob data from the remote repository without discarding your working-tree changes.

If cloning or hydration fails, inspect the CLI error and diagnostic log before retrying. See [Troubleshoot TiDB Cloud CLI](/ai/ti/reference/ti-troubleshooting.md) for common Filesystem and companion issues.

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
