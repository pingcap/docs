---
title: Mount TiDB Cloud Filesystem on macOS
summary: Mount a TiDB Cloud Filesystem as a local directory on macOS, and use macFUSE when you need advanced mount features.
---

# Mount TiDB Cloud Filesystem on macOS

On macOS, you can mount a TiDB Cloud Filesystem as a local directory and access its files with your usual applications and tools.

For most workflows, no additional mount software is required. Without macFUSE, TiDB Cloud CLI (`ti`) uses WebDAV. If macFUSE is installed, `ti` prefers FUSE in automatic driver selection.

If you need features that require FUSE, such as mounting layers or checkpoints or using `drain-file-system`, install macFUSE and use the FUSE driver instead.

> **Note:**
>
> TiDB Cloud Filesystem is currently in public preview. Its features and interfaces are subject to change without notice.

## Prerequisites

Before you begin:

- [Install TiDB Cloud CLI (`ti`)](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-the-cli).
- Make the Filesystem and its token available to `ti`. See [Access an Existing TiDB Cloud Filesystem](/tidb-cloud-filesystem/access-filesystem.md).

The write examples below require a token with write permission.

## Mount with WebDAV

To explicitly use WebDAV, pass `--driver webdav`.

1. Create a local directory for the mount:

    ```bash
    mkdir -p "$HOME/workspace"
    ```

2. Mount the Filesystem:

    ```bash
    ti fs mount-file-system \
      --mount-path "$HOME/workspace" \
      --driver webdav
    ```

    This command explicitly selects WebDAV.

3. Access the Filesystem through the mounted directory:

    ```bash
    ls "$HOME/workspace"
    ```

    If your token has write permission, you can also create and read a test file:

    ```bash
    TEST_FILE="mount-check-$(date +%s).txt"

    printf 'Hello from macOS\n' > "$HOME/workspace/$TEST_FILE"
    cat "$HOME/workspace/$TEST_FILE"
    ```

4. When you are finished, close files that are open in applications and unmount the Filesystem:

    ```bash
    ti fs unmount-file-system --mount-path "$HOME/workspace"
    ```

    WebDAV does not support `drain-file-system`. Complete a normal unmount before shutting down the machine or handing updated files to another user or environment.

    If you created the test file above, you can optionally confirm that it is available directly from the Filesystem:

    ```bash
    ti fs read-file --path "/$TEST_FILE"
    ```

Unmounting removes the local mount but does not delete the Filesystem or its data.

## Use macFUSE when you need FUSE features

Use FUSE instead of WebDAV when you need to:

- mount a layer or checkpoint, or
- make pending writes reach the Filesystem while keeping the mount running with `drain-file-system`.

To use FUSE on macOS:

1. Install [macFUSE](https://macfuse.github.io/) and complete any installation or security approval steps required by your macOS version.

    Installing `ti` does not install macFUSE.

2. Prepare the local mount directory:

    - If a mount is already active at `$HOME/workspace`, unmount it before reusing the same directory:

        ```bash
        ti fs unmount-file-system --mount-path "$HOME/workspace"
        ```

    - Ensure that `$HOME/workspace` exists:

        ```bash
        mkdir -p "$HOME/workspace"
        ```

3. Mount the Filesystem with FUSE:

    ```bash
    ti fs mount-file-system \
      --mount-path "$HOME/workspace" \
      --driver fuse
    ```

    Layer and checkpoint mounts require FUSE, and checkpoint mounts are always read-only. For details, see [Manage TiDB Cloud Filesystem Layers and Checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md).

    If you need pending writes to reach the Filesystem while keeping the mount running, see [Make FUSE writes available without unmounting](/tidb-cloud-filesystem/filesystem-mount.md#make-fuse-writes-available-without-unmounting).

4. When you are finished, stop applications from writing to the mount, close open files, and unmount it:

    ```bash
    ti fs unmount-file-system --mount-path "$HOME/workspace"
    ```

    A successful FUSE unmount flushes pending writes. You do not need to run `drain-file-system` before a normal unmount.

## Troubleshoot mount issues

If a WebDAV mount fails to start:

- Make sure the local mount directory exists and is writable.
- Check the diagnostic log path reported by `ti` for the underlying error.
- Make sure another mount is not already using the same local directory.

If a FUSE mount fails to start:

- Make sure macFUSE is installed.
- Complete any macOS security approvals required by macFUSE.
- Check the diagnostic log path reported by `ti`.

If unmounting fails, keep the mount process and machine running until you resolve the error and verify that required files have reached the Filesystem. Do not remove local mount data while pending writes might remain.

For additional mount errors, see [Troubleshoot TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-troubleshooting.md).

## What's next

- [Mount TiDB Cloud Filesystem Locally](/tidb-cloud-filesystem/filesystem-mount.md) for read-only mounts, mounting part of a Filesystem, and safe unmount behavior.
- [Manage TiDB Cloud Filesystem Layers and Checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md) to work with layers and checkpoints through FUSE.
- [Share a TiDB Cloud Filesystem Across Machines](/tidb-cloud-filesystem/filesystem-sharing.md) to give another user or environment access to the Filesystem.
