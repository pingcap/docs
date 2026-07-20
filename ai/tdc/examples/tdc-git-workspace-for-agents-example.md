---
title: Prepare a Git Workspace for Agents on TiDB Cloud Filesystem
summary: Make a large Git workspace visible quickly, hydrate clean objects in the background, and let an agent start work before the full download finishes.
---

# Prepare a Git Workspace for Agents on TiDB Cloud Filesystem

This example removes a large repository clone from the critical path of starting an agent task.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## The agent problem

An ephemeral agent normally waits for `git clone` and checkout to download a repository before it can inspect the tree or begin work. For a large monorepo, that startup delay is paid again for every replacement sandbox. The agent appears idle even when its first task needs only a small part of the repository.

## Why a normal clone or partial clone is not enough

A normal clone blocks until the initial object transfer and checkout finish. A native blobless partial clone reduces the first transfer, but later Git commands and file reads can still trigger many on-demand fetches on the agent's critical path. Neither approach by itself provides a shared Filesystem workspace that can be restored across agent runtimes.

## How tdc changes the workflow

`tdc fs-git clone-git-workspace --blobless --hydrate background` registers the Git workspace and exposes its file tree before all clean blobs finish downloading. The command returns so the agent can inspect paths and start working while tdc hydrates the clean tree and local Git object database in the background. Reads that arrive before hydration completes fall back to Git's lazy fetch for correctness. Ordinary Git remains responsible for edits, commits, fetches, and pushes.

## Prerequisites

- Select a Filesystem.
- Use Linux FUSE or macOS with macFUSE and explicit `--driver fuse`.
- Install Git and configure repository authentication.

## Step 1. Mount a workspace

```bash
mkdir -p /path/to/workspace
tdc fs mount-file-system \
  --mount-path /path/to/workspace \
  --driver fuse
```

## Step 2. Create the workspace and hydrate in the background

```bash
tdc fs-git clone-git-workspace \
  --repo-url https://github.com/pingcap/tidb.git \
  --target-path /path/to/workspace/tidb \
  --blobless \
  --hydrate background
```

The workspace tree is now available, and hydration continues in the background. Let the agent start with ordinary commands:

```bash
find /path/to/workspace/tidb -maxdepth 2 -type f | head
git -C /path/to/workspace/tidb status
```

Before a deterministic benchmark or before draining the mount, you can wait for hydration explicitly:

```bash
tdc fs-git hydrate-git-workspace \
  --target-path /path/to/workspace/tidb \
  --timeout 30m
```

## Step 3. Create an agent worktree

```bash
tdc fs-git add-git-worktree \
  --base-path /path/to/workspace/tidb \
  --worktree-path /path/to/workspace/tidb-agent-task \
  --branch-name agent-task
```

The agent can now use ordinary tools:

```bash
git -C /path/to/workspace/tidb-agent-task status
```

Commit or push required changes before removing the worktree.

## Cleanup

```bash
tdc fs-git remove-git-worktree \
  --worktree-path /path/to/workspace/tidb-agent-task

tdc fs unmount-file-system --mount-path /path/to/workspace
```

Use `--force` for worktree removal only when uncommitted changes can be discarded. Filesystem unmount performs a graceful drain automatically; use `tdc fs drain-file-system` separately only when you need to flush remote work without unmounting.

## Security and durability notes

- Repository credentials are managed by Git, not tdc.
- The coding-agent profile keeps `.git` and ignored generated files locally for performance.
- Preserve or pack local overlay state before deleting an ephemeral machine when it cannot be rebuilt.

## What's next

- [Use Git Workspaces on TiDB Cloud Filesystem](/ai/tdc/guides/tdc-filesystem-git.md)
- [Manage TiDB Cloud Filesystem with tdc](/ai/tdc/guides/tdc-filesystem.md)
