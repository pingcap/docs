---
title: Prepare a Git Workspace for Agents on TiDB Cloud Filesystem
summary: Make a large Git workspace visible quickly, hydrate clean objects in the background, and let an agent start work before the full download finishes.
---

# Prepare a Git Workspace for Agents on TiDB Cloud Filesystem

This workflow removes a large repository clone from the critical path of starting an agent task. Use it when an ephemeral agent needs to inspect or change a large repository before a complete download would finish.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## How it works

`ti fs-git clone-git-workspace --blobless --hydrate background` registers a Git workspace that can be shared across replacement agent runtimes and exposes its file tree before all clean blobs finish downloading. The command returns so the agent can inspect paths and start working while `ti` hydrates the clean tree and local Git object database in the background. Unlike a normal clone, the initial object transfer does not block the complete workflow. Unlike a native blobless partial clone alone, background hydration reduces repeated on-demand fetches on the agent's critical path. Reads that arrive before hydration completes still fall back to Git's lazy fetch for correctness. Ordinary Git remains responsible for edits, commits, fetches, and pushes.

## Prerequisites

- Select a Filesystem.
- Use Linux FUSE or macOS with macFUSE and explicit `--driver fuse`. Git workspaces rely on FUSE to combine the remote Git tree and workspace changes into the mounted path; WebDAV mounts do not provide this integration.
- Install Git and configure repository authentication.

## Step 1. Mount a workspace

```bash
mkdir -p /path/to/workspace
ti fs mount-file-system \
  --mount-path /path/to/workspace \
  --driver fuse \
  --mount-profile coding-agent
```

## Step 2. Create the workspace and hydrate in the background

```bash
ti fs-git clone-git-workspace \
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
ti fs-git hydrate-git-workspace \
  --target-path /path/to/workspace/tidb \
  --timeout 30m
```

## Step 3. Create an agent worktree

```bash
ti fs-git add-git-worktree \
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
ti fs-git remove-git-worktree \
  --worktree-path /path/to/workspace/tidb-agent-task

ti fs unmount-file-system --mount-path /path/to/workspace
```

Use `--force` for worktree removal only when uncommitted changes can be discarded. Filesystem unmount performs a graceful drain automatically; use `ti fs drain-file-system` separately only when you need to flush remote work without unmounting.

## Security and operational notes

- Repository credentials are managed by Git, not `ti`.
- The `coding-agent` mount profile keeps Git metadata, dependency directories, caches, build output, and other generated files on the local machine for performance.
- Files kept locally by the `coding-agent` profile disappear with an ephemeral machine. Commit or push required Git changes, and use [`pack-file-system`](/ai/ti/reference/ti-fs-pack-file-system.md) with explicit `--path` values to preserve other local files that cannot be rebuilt.

## What's next

- [TiDB Cloud Filesystem Git CLI Command Reference](/ai/ti/reference/ti-filesystem-git.md)
- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
