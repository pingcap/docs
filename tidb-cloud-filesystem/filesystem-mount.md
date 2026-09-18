---
title: Mount TiDB Cloud Filesystem Locally
summary: Mount an existing TiDB Cloud Filesystem as a local directory, use its files with local tools, and unmount it safely.
aliases: ['/ai/mount-filesystem']
---

# Mount TiDB Cloud Filesystem Locally

Mount a TiDB Cloud Filesystem when your editor, application, or agent needs to access Filesystem data through local file paths.

After mounting, you can use ordinary local tools to read and write files in the mounted directory. Unmounting removes the local access point but does not delete the Filesystem or its data.

> **Note:**
>
> TiDB Cloud Filesystem is currently in public preview. Its features and interfaces are subject to change without notice.

## Before you begin

Before mounting a Filesystem:

- [Install TiDB Cloud CLI (`ti`)](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-the-cli).
- Make the Filesystem and its token available to `ti`. See [Access an Existing TiDB Cloud Filesystem](/tidb-cloud-filesystem/access-filesystem.md).
- Complete the mount setup for your environment: [Linux](/tidb-cloud-filesystem/filesystem-mount-linux.md), [macOS](/tidb-cloud-filesystem/filesystem-mount-macos.md), or [Docker and Docker Compose](/tidb-cloud-filesystem/filesystem-mount-docker.md).

Native Filesystem mounting is not supported on Windows. On Windows, use direct commands such as `ti fs copy-file`, `ti fs read-file`, and `ti fs list-files` instead.

You normally do not need to choose a mount driver manually. `ti` uses FUSE on Linux. On macOS without macFUSE, `ti` uses WebDAV; if macFUSE is installed, `ti` prefers FUSE in automatic driver selection. On macOS, use FUSE when you need layers, checkpoints, or the drain operation.

## Mount and use the Filesystem

To mount the Filesystem:

1. Create a local directory for the mount:

    ```bash
    mkdir -p "$HOME/workspace"
    ```

2. Mount the Filesystem:

    ```bash
    ti fs mount-file-system --mount-path "$HOME/workspace"
    ```

    The command waits until the mount is ready before returning. The mount continues running in the background, so closing the terminal does not unmount it.

    If the mount fails to start, check the diagnostic log path reported by the CLI.

3. Access the Filesystem through the mounted directory using ordinary local tools:

    ```bash
    ls "$HOME/workspace"

    printf 'Written through the mount\n' > "$HOME/workspace/mounted.txt"

    cat "$HOME/workspace/mounted.txt"
    ```

    The write example requires a token with write permission and a writable mount.

If you use FUSE, run the mount and the applications that access it as the same OS user. Changing the ownership of the mount directory does not give another user access through an existing FUSE mount.

### Mount only part of the Filesystem

By default, the Filesystem root `/` is mounted.

To mount only a specific directory, use `--remote-path`. For example:

```bash
ti fs mount-file-system \
  --remote-path /workspace \
  --mount-path "$HOME/workspace"
```

In this example, the remote `/workspace` directory becomes the root of the local mount. For example, `/workspace/project.md` is available locally as `$HOME/workspace/project.md`.

If you use a scoped token that grants access only to a specific path, mount that path rather than the Filesystem root.

### Create a read-only mount

To prevent writes through the local mount, add `--read-only`:

```bash
ti fs mount-file-system \
  --mount-path "$HOME/workspace" \
  --read-only
```

The `--read-only` option prevents writes through this mount, but it does not change the permissions of the Filesystem token. To enforce read-only access at the service, use a scoped token that grants only the required read access.

### Mount a layer or checkpoint

Layer and checkpoint mounts require FUSE. On macOS, install macFUSE and specify `--driver fuse`.

Checkpoint mounts are always read-only.

For layer and checkpoint workflows, see [Manage TiDB Cloud Filesystem Layers and Checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md). For all mount options, see the [`mount-file-system` command reference](/ai/ti/reference/ti-fs-mount-file-system.md).

## Finish safely

In most cases, simply stop writing and unmount the Filesystem. You only need to drain a FUSE mount when you want pending writes to reach the Filesystem while keeping the mount running.

### Unmount when you are finished

When you no longer need the mount:

1. Stop applications from writing to the mounted directory and close any open files.

2. Unmount the Filesystem:

    ```bash
    ti fs unmount-file-system --mount-path "$HOME/workspace"
    ```

A successful FUSE unmount flushes pending writes before stopping the mount. You do not need to run `drain-file-system` before a normal unmount.

For a WebDAV mount, close open files and unmount normally. WebDAV does not support the drain operation.

Unmounting removes the local mount but does not delete the Filesystem or its data.

### Make FUSE writes available without unmounting

If you want to keep a FUSE mount running but need pending writes to reach the Filesystem—for example, before creating a checkpoint or sharing updated files with another machine:

1. Stop applications from writing to the relevant files and close those files.

2. Drain the mount:

    ```bash
    ti fs drain-file-system \
      --mount-path "$HOME/workspace" \
      --timeout 30s
    ```

A successful drain confirms that pending writes have reached the service while leaving the mount running.

If the drain times out or returns an error, some writes might not have reached the Filesystem. Keep the mount and machine available, resolve the error, and verify the files before ending the session or telling another user that the updates are ready.

> **Warning:**
>
> If a drain or unmount fails, do not shut down or destroy the machine or sandbox, stop the mount process, or delete its local data. Some pending writes might still exist only on that machine. Resolve the error and verify that the required files have reached the Filesystem first.

## What's next

- [Share a TiDB Cloud Filesystem Across Machines](/tidb-cloud-filesystem/filesystem-sharing.md) to give another user or environment access to the same Filesystem.
- [Manage TiDB Cloud Filesystem Layers and Checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md) to make and review isolated changes before applying them to the base Filesystem.
- See the [`mount-file-system` command reference](/ai/ti/reference/ti-fs-mount-file-system.md) for all mount options.
