---
title: Manage Git Workspaces on TiDB Cloud Filesystem
summary: Learn how to clone Git repositories into a mounted TiDB Cloud Filesystem, speed up large repository setup, and manage linked worktrees.
aliases: ['/ai/manage-git-workspaces']
---

# Manage Git Workspaces on TiDB Cloud Filesystem

Clone a Git repository into a FUSE mount and use ordinary Git commands to work with it. For large repositories, blobless cloning lets you begin before all file contents finish downloading. Linked worktrees provide separate working directories for branches without cloning again.

## Prerequisites

Before you begin:

- [Install TiDB Cloud CLI](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli).
- [Mount a File System](/tidb-cloud-filesystem/filesystem-mount.md) through FUSE. Git workspaces are not supported on WebDAV mounts.
- Make the mounted file system and a token with the required permissions available to `ti`. See [Access an Existing File System](/tidb-cloud-filesystem/access-filesystem.md).
- Install Git and configure authentication for the repository you want to use.

All Git workspaces in this guide are created inside the mounted file system path.

## Clone a Git repository

Specify the repository URL and a target path inside the mounted directory:

```shell
ti fs-git clone-git-workspace \
  --repo-url https://github.com/pingcap/tidb.git \
  --target-path /path/to/workspace/tidb
```

The repository is cloned to `/path/to/workspace/tidb`.

For a large repository, use `--blobless` to start working before all file contents finish downloading:

```shell
ti fs-git clone-git-workspace \
  --repo-url https://github.com/pingcap/tidb.git \
  --target-path /path/to/workspace/tidb \
  --blobless
```

With `--blobless`, `ti` downloads the repository structure and Git metadata first. By default, `--hydrate auto` downloads the remaining file contents in the background while you work. To disable background hydration, specify `--hydrate off`.

If you need all file contents to finish downloading before the clone command returns, also specify `--hydrate sync`:

```shell
ti fs-git clone-git-workspace \
  --repo-url https://github.com/pingcap/tidb.git \
  --target-path /path/to/workspace/tidb \
  --blobless \
  --hydrate sync
```

## Finish downloading a blobless workspace

Before a task that needs all repository file contents, wait for any remaining downloads in a blobless workspace:

```shell
ti fs-git hydrate-git-workspace \
  --target-path /path/to/workspace/tidb \
  --timeout 30m
```

This process, called hydration, downloads missing Git data without discarding your file changes.

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

## Preserve work before leaving a machine

With `--mount-profile coding-agent`, Git metadata such as `.git` stays on the local machine. A local commit alone does not make that history recoverable on another machine. Draining or unmounting does not transfer this local Git metadata either. Preserve the history using a push to a Git remote or the metadata archive workflow below.

Before deleting an ephemeral machine:

1. Preserve the Git history using one of these methods:
    - Commit and push to a writable Git remote. From an independent clone or fetch, verify that the expected commit ID is available.
    - If you cannot push, use [`pack-file-system`](/ai/ti/reference/ti-fs-pack-file-system.md) with explicit `--path` values for the required local Git metadata, including the base repository's metadata for linked worktrees. Restore with [`unpack-file-system`](/ai/ti/reference/ti-fs-unpack-file-system.md) in a separate environment and compare the commit ID and working files. If paths change, first [repair the worktree connections with `git worktree repair`](https://git-scm.com/docs/git-worktree). See [Recover an unpushed workspace to another machine](#recover-an-unpushed-workspace-to-another-machine) for a runnable example.
2. Preserve any required untracked or ignored files separately; a push preserves only committed content.
3. [Unmount safely](/tidb-cloud-filesystem/filesystem-mount.md#unmount-when-you-are-finished). Keep the original disk until recovery checks pass.

See [mount profiles and local overlays](/ai/ti/reference/ti-filesystem.md#mount-profiles-and-local-overlays) for the data kept locally by each profile.

## Recover an unpushed workspace to another machine

This example moves an in-progress Git workspace with a linked worktree to another machine without pushing to a remote. It packs both the base repository's Git metadata and the linked worktree's per-worktree metadata into a remote archive, restores them on a second machine, repairs the worktree link, and compares commit IDs to confirm the transfer.

The example assumes the source machine used `--mount-profile coding-agent` and produced the layout described earlier in this page:

```text
/path/to/workspace/tidb              (base repository, contains .git/)
/path/to/workspace/tidb-feature      (linked worktree, contains .git file pointing at the base)
```

### On the source machine

1. Record the commit IDs to compare against later:

    ```shell
    (cd /path/to/workspace/tidb && git rev-parse HEAD) | tee /tmp/tidb-base.sha
    (cd /path/to/workspace/tidb-feature && git rev-parse HEAD) | tee /tmp/tidb-feature.sha
    ```

2. Stop writers and drain pending writes so cached blobs are durable before packing:

    ```shell
    ti fs drain-file-system --mount-path /path/to/workspace
    ```

3. Pack the Git metadata that lives only in the local overlay. `coding-agent` keeps `.git` off the remote namespace, so both the base repository's `.git` directory and each linked worktree's `.git/worktrees/<name>` subdirectory must be listed explicitly. Include untracked or ignored files you need to keep, such as `.env` or a virtual environment, in the same archive. `--archive-path` is a path inside the remote file system where the archive is stored; pick a location outside your working tree, such as `/packs/`:

    ```shell
    ti fs pack-file-system \
      --mount-path /path/to/workspace \
      --mount-profile coding-agent \
      --archive-path /packs/tidb-workspace.tar.zst \
      --path tidb/.git \
      --path tidb/.git/worktrees/tidb-feature \
      --path tidb-feature/.git \
      --path tidb/.env
    ```

    `--path` values are relative to the mount path. Repeat `--path` for every directory or file you want to preserve. Untracked or ignored files that are not listed are not restored on the target machine.

4. [Unmount safely](/tidb-cloud-filesystem/filesystem-mount.md#unmount-when-you-are-finished). Keep the source disk available until the target machine confirms recovery.

### On the target machine

1. Mount the same file system with the same profile at the destination path. The destination path may differ from the source; the repair step below fixes the linked worktree's stored path.

    ```shell
    mkdir -p /new/path/to/workspace
    ti fs mount-file-system \
      --mount-path /new/path/to/workspace \
      --mount-profile coding-agent \
      --driver fuse
    ```

2. Restore the packed metadata into the local overlay of the new mount:

    ```shell
    ti fs unpack-file-system \
      --mount-path /new/path/to/workspace \
      --mount-profile coding-agent \
      --archive-path /packs/tidb-workspace.tar.zst
    ```

3. If the mount path changed from the source, repair the linked worktree's back-reference before running any Git command inside it. Run this from the base repository:

    ```shell
    cd /new/path/to/workspace/tidb
    git worktree repair /new/path/to/workspace/tidb-feature
    git worktree list
    ```

    `git worktree list` should list both `tidb` and `tidb-feature` with the new paths and no `prunable` marker. If the base repository moved as well, run `git worktree repair` without an argument from inside the base repository to update every registered worktree.

4. Verify the commit IDs match what you recorded on the source machine:

    ```shell
    (cd /new/path/to/workspace/tidb && git rev-parse HEAD)
    (cd /new/path/to/workspace/tidb-feature && git rev-parse HEAD)
    ```

    Both outputs must match the corresponding `.sha` files captured on the source machine. If either differs, do not delete the source disk: the archive is incomplete, and additional `--path` values are usually the cause. Rerun `pack-file-system` on the source with the missing paths listed and unpack again.

5. Only after both commit IDs match, and any untracked files you preserved are readable in the target workspace, delete the source machine.

> **Warning:**
>
> `pack-file-system` packs only the paths you list. It does not detect linked worktrees or `.gitignore`d files on its own. If you add or remove linked worktrees before packing, update the `--path` list to match, and always include each worktree's own `.git` file and its matching `.git/worktrees/<name>` subdirectory under the base repository.

## What's next

- [Prepare a Git Workspace for Agents on TiDB Cloud Filesystem](/ai/ti/guides/ti-git-workspace-for-agents-example.md) for an agent workflow that uses blobless cloning and background hydration.
- [TiDB Cloud Filesystem Git CLI Command Reference](/ai/ti/reference/ti-filesystem-git.md) for all `ti fs-git` commands and options.
