---
title: Manage Git Workspaces on TiDB Cloud Filesystem
summary: Learn how to clone, hydrate, create linked worktrees, and remove Git workspaces on a mounted TiDB Cloud Filesystem.
---

# Manage Git Workspaces on TiDB Cloud Filesystem

Use `ti fs-git` to accelerate Git workspace setup on a mounted TiDB Cloud Filesystem while continuing to use ordinary Git commands for daily work.

## Prerequisites

- Mount a Filesystem through FUSE.
- Install Git and configure repository credentials independently.
- Ensure that the selected profile or Filesystem owner token can access the Filesystem.

## Clone a workspace

```shell
ti fs-git clone-git-workspace \
  --repo-url https://github.com/pingcap/tidb.git \
  --target-path /path/to/workspace/tidb
```

For a large repository, add `--blobless --hydrate background` to expose the tree while clean content and Git objects hydrate in the background. Use synchronous hydration when a caller must wait for deterministic completion.

## Hydrate an existing workspace

```shell
ti fs-git hydrate-git-workspace \
  --target-path /path/to/workspace/tidb \
  --timeout 30m
```

Hydration materializes clean Git data and does not discard working-tree changes.

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

The command rejects a dirty worktree by default. Use `--force` only after deciding that its local changes can be discarded.

Before terminating an ephemeral machine, preserve required changes, remove unused worktrees, and gracefully unmount the Filesystem.

## What's next

- [Prepare a Git Workspace for Agents on TiDB Cloud Filesystem](/ai/ti/reference/ti-git-workspace-for-agents-example.md)
- [TiDB Cloud Filesystem Git CLI Command Reference](/ai/ti/reference/ti-filesystem-git.md)
