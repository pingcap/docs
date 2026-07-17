---
title: Prepare a Git Workspace for Agents on TiDB Cloud Filesystem
summary: Mount a Filesystem, create a fast Git workspace and linked worktree, use Git normally, and clean up safely.
---

# Prepare a Git Workspace for Agents on TiDB Cloud Filesystem

This example prepares a repository and an isolated linked worktree for an agent.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

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

## Step 2. Clone and hydrate

```bash
tdc fs-git clone-git-workspace \
  --repo-url https://github.com/pingcap/tidb.git \
  --target-path /path/to/workspace/tidb \
  --blobless \
  --hydrate sync
```

Verify:

```bash
git -C /path/to/workspace/tidb status
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

tdc fs drain-file-system --mount-path /path/to/workspace
tdc fs unmount-file-system --mount-path /path/to/workspace
```

Use `--force` for worktree removal only when uncommitted changes can be discarded.

## Security and durability notes

- Repository credentials are managed by Git, not tdc.
- The coding-agent profile keeps `.git` and ignored generated files locally for performance.
- Preserve or pack local overlay state before deleting an ephemeral machine when it cannot be rebuilt.

## What's next

- [Use Git Workspaces on TiDB Cloud Filesystem](/ai/tdc/guides/tdc-filesystem-git.md)
- [Manage TiDB Cloud Filesystem with tdc](/ai/tdc/guides/tdc-filesystem.md)
