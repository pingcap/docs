---
title: tdc fs-git Command Reference
summary: Reference every tdc fs-git command for cloning, hydrating, and managing linked Git worktrees.
---

# tdc fs-git Command Reference

`tdc fs-git` accelerates Git workspace setup on mounted TiDB Cloud Filesystem paths. It augments Git; you continue to use ordinary `git` commands for status, edit, add, commit, fetch, and push.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Command tree

```text
tdc fs-git
├── clone-git-workspace
├── hydrate-git-workspace
├── add-git-worktree
└── remove-git-worktree
```

| Command | Purpose and key inputs | Example |
| --- | --- | --- |
| `clone-git-workspace` | Clones into a mounted Filesystem path. `--blobless` and `--hydrate background` expose the tree before all clean data finishes hydrating. | `tdc fs-git clone-git-workspace --repo-url https://github.com/pingcap/tidb.git --target-path /workspace/tidb --blobless --hydrate background` |
| `hydrate-git-workspace` | Materializes clean Git data for an existing fast or blobless workspace. | `tdc fs-git hydrate-git-workspace --target-path /workspace/tidb --timeout 30m` |
| `add-git-worktree` | Creates a linked worktree from a base workspace. | `tdc fs-git add-git-worktree --base-path /workspace/tidb --worktree-path /workspace/feature --branch-name feature-x` |
| `remove-git-worktree` | Removes a linked worktree; dirty worktrees require explicit `--force`. | `tdc fs-git remove-git-worktree --worktree-path /workspace/feature` |

## Prerequisites

- Mount a Filesystem through FUSE. Git workspace acceleration relies on the mounted Filesystem runtime.
- Install `git` and configure any repository credentials independently.
- Ensure the FS owner token or selected profile can access the Filesystem.

## Clone a workspace

```bash
tdc fs-git clone-git-workspace \
  --repo-url https://github.com/pingcap/tidb.git \
  --target-path /path/to/workspace/tidb
```

For a large repository, create a blobless workspace and hydrate in the background:

```bash
tdc fs-git clone-git-workspace \
  --repo-url https://github.com/pingcap/tidb.git \
  --target-path /path/to/workspace/tidb \
  --blobless \
  --hydrate background
```

The command returns after registering the workspace, so the file tree becomes available while clean content and Git objects continue to hydrate. Reads before hydration finishes use Git lazy fetch for correctness. This moves most repository download work out of the agent startup path.

`--hydrate` accepts `auto`, `background`, `sync`, or `off`. Use `sync` when the caller must wait for hydration before continuing, such as a deterministic benchmark.

## Hydrate an existing workspace

```bash
tdc fs-git hydrate-git-workspace \
  --target-path /path/to/workspace/tidb \
  --timeout 30m
```

Hydration materializes clean Git objects for a fast or blobless workspace. It does not discard working-tree changes.

## Add a linked worktree

```bash
tdc fs-git add-git-worktree \
  --base-path /path/to/workspace/tidb \
  --worktree-path /path/to/workspace/tidb-feature \
  --branch-name feature-x
```

Use `--detach` for a detached worktree, `--commit-ish` to select a starting revision, and `--blobless` with `--hydrate` when the base workspace uses the blobless mode.

Use Git normally:

```bash
git -C /path/to/workspace/tidb-feature status
git -C /path/to/workspace/tidb-feature add .
git -C /path/to/workspace/tidb-feature commit -m "Implement feature x"
```

## Remove a worktree

```bash
tdc fs-git remove-git-worktree \
  --worktree-path /path/to/workspace/tidb-feature
```

The command refuses a dirty worktree by default. Use `--force` only after deciding that local changes can be discarded:

```bash
tdc fs-git remove-git-worktree \
  --worktree-path /path/to/workspace/tidb-feature \
  --force
```

## Lifecycle guidance

Before terminating an ephemeral machine:

1. Commit or otherwise preserve required working-tree changes.
2. Remove linked worktrees you no longer need.
3. Unmount the Filesystem. Graceful unmount automatically drains pending FUSE work.

The default coding-agent mount profile keeps `.git` and rebuildable generated files in local overlay storage. Preserve or pack that local state when it must survive machine deletion.

## What's next

- [Prepare a Git Workspace for Agents](/ai/tdc/reference/tdc-git-workspace-for-agents-example.md)
- [tdc fs Command Reference](/ai/tdc/reference/tdc-filesystem.md)
