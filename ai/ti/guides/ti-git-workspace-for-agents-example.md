---
title: Prepare a Git Workspace for Agents on TiDB Cloud Filesystem
summary: Learn how to start agent tasks before a large Git repository finishes downloading and preserve work before removing the machine.
---

# Prepare a Git Workspace for Agents on TiDB Cloud Filesystem

Start an agent task before a large repository finishes downloading. Use a blobless Git workspace with background hydration when an agent on a temporary machine needs to inspect or edit files immediately.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## How it works

`ti fs-git clone-git-workspace --blobless --hydrate background` registers a Git workspace and exposes its file tree before all clean blobs finish downloading. The agent can start working while `ti` downloads the remaining clean file contents and populates the local Git object database. This background process, called hydration, reduces repeated on-demand fetches. Reads before hydration completes use Git's lazy fetch to retrieve missing data.

Replacement agent runtimes can access the registered workspace. Preserve local Git history before discarding the original machine, as described in the cleanup guidance below. Use your usual tools to edit files and Git commands to commit, fetch, and push.

## Prerequisites

- Select a file system.
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

Commit required changes before removing the worktree. Before discarding the machine, [preserve and verify the Git history](/tidb-cloud-filesystem/manage-git-workspaces.md#preserve-work-before-leaving-a-machine) with a push or a verified backup of local Git metadata.

## Cleanup

```bash
ti fs-git remove-git-worktree \
  --worktree-path /path/to/workspace/tidb-agent-task

ti fs unmount-file-system --mount-path /path/to/workspace
```

Use `--force` for worktree removal only when uncommitted changes can be discarded. File system unmount performs a graceful drain automatically; use `ti fs drain-file-system` separately only when you need to flush remote work without unmounting.

## Security and operational notes

- Repository credentials are managed by Git, not `ti`.
- The `coding-agent` mount profile keeps Git metadata, dependency directories, caches, build output, and other generated files on the local machine for performance.
- Files kept locally by the `coding-agent` profile disappear with an ephemeral machine. A local commit alone does not preserve Git history across machines. Push and verify required commits, and use [`pack-file-system`](/ai/ti/reference/ti-fs-pack-file-system.md) with explicit `--path` values to preserve other local files that cannot be rebuilt.

## What's next

- [TiDB Cloud Filesystem Git CLI Command Reference](/ai/ti/reference/ti-filesystem-git.md)
- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
