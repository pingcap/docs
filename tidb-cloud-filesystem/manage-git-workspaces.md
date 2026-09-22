---
title: Manage Git Workspaces on TiDB Cloud Filesystem
summary: Learn how to clone Git repositories into a mounted TiDB Cloud Filesystem, speed up large repository setup, and manage linked worktrees.
aliases: ['/ai/manage-git-workspaces']
---

# Manage Git Workspaces on TiDB Cloud Filesystem

If you want to work with a Git repository directly on a mounted TiDB Cloud Filesystem, you can follow this guide to set up and manage the Git workspace.

This is especially useful for large repositories, where you can start working before all file contents finish downloading, or when you need separate working directories for different branches without cloning the repository multiple times. This guide covers cloning a repository, completing background downloads when needed, and creating and removing linked Git worktrees.

After the workspace is set up, you can continue to use ordinary Git commands such as `git status`, `git add`, `git commit`, `git fetch`, and `git push` for your daily Git work.

## Prerequisites

Before you begin:

- [Install TiDB Cloud CLI](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli).
- [Mount a TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-mount.md) through FUSE. Git workspaces are not supported on WebDAV mounts.
- Make the mounted Filesystem and a token with the required permissions available to `ti`. See [Access an Existing TiDB Cloud Filesystem](/tidb-cloud-filesystem/access-filesystem.md).
- Install Git and configure authentication for the repository you want to use.

All Git workspaces in this guide are created inside the mounted Filesystem path.

## Clone a Git repository

To clone a Git repository into your mounted Filesystem directory, use the `ti fs-git clone-git-workspace` command and specify the repository URL and target path as follows:

```shell
ti fs-git clone-git-workspace \
  --repo-url https://github.com/pingcap/tidb.git \
  --target-path /path/to/workspace/tidb
```

The repository is cloned to `/path/to/workspace/tidb`.

For a large repository, you can start working before all file contents finish downloading by specifying `--blobless`:

```shell
ti fs-git clone-git-workspace \
  --repo-url https://github.com/pingcap/tidb.git \
  --target-path /path/to/workspace/tidb \
  --blobless
```

With `--blobless`, `ti` downloads the repository structure and Git metadata first. When `--hydrate` is `auto` (the default), `ti` then continues downloading the remaining file contents in the background. You can start working with the repository while this download continues. To disable background hydration, specify `--hydrate off`.

If you need all file contents to finish downloading before the clone command returns, also specify `--hydrate sync`:

```shell
ti fs-git clone-git-workspace \
  --repo-url https://github.com/pingcap/tidb.git \
  --target-path /path/to/workspace/tidb \
  --blobless \
  --hydrate sync
```

## Finish downloading a blobless workspace

If you created a workspace with `--blobless`, you can later wait for any remaining file contents to finish downloading:

```shell
ti fs-git hydrate-git-workspace \
  --target-path /path/to/workspace/tidb \
  --timeout 30m
```

Run this command when you want to make sure the remaining Git file data has finished downloading before you continue. For example, you might do this before a task that needs repository file contents to be available.

This process, called hydration, downloads the Git data that is still missing from the workspace without discarding changes you have already made to files.

If cloning or hydration fails, check the CLI error and diagnostic log before retrying. See [Troubleshoot TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-troubleshooting.md).

## Create a linked worktree

Use a linked worktree when you want a separate working directory for another branch without cloning the repository again. The new worktree shares Git data with the base workspace.

For example, create a worktree for a new `feature-x` branch:

```shell
ti fs-git add-git-worktree \
  --base-path /path/to/workspace/tidb \
  --worktree-path /path/to/workspace/tidb-feature \
  --branch-name feature-x
```

After the worktree is created, use ordinary Git commands in `/path/to/workspace/tidb-feature`:

```shell
git -C /path/to/workspace/tidb-feature status
```

For other options, such as creating a detached worktree at a specific commit, see the [`add-git-worktree` command reference](/ai/ti/reference/ti-fs-git-add-git-worktree.md).

## Remove a linked worktree

When you no longer need a linked worktree, remove it:

```shell
ti fs-git remove-git-worktree \
  --worktree-path /path/to/workspace/tidb-feature
```

Removing a linked worktree does not remove the base workspace or the Git data shared by other worktrees.

If the worktree contains uncommitted changes, the command refuses to remove it. Commit or preserve any changes you need before removing the worktree.

Use `--force` only when you are sure that the uncommitted changes can be discarded:

```shell
ti fs-git remove-git-worktree \
  --worktree-path /path/to/workspace/tidb-feature \
  --force
```

When you are finished using the mounted Filesystem, commit or push any Git changes you want to preserve and [unmount the Filesystem safely](/tidb-cloud-filesystem/filesystem-mount.md#unmount-when-you-are-finished).

## What's next

- [Prepare a Git Workspace for Agents on TiDB Cloud Filesystem](/ai/ti/guides/ti-git-workspace-for-agents-example.md) for an agent workflow that uses blobless cloning and background hydration.
- [TiDB Cloud Filesystem Git CLI Command Reference](/ai/ti/reference/ti-filesystem-git.md) for all `ti fs-git` commands and options.
