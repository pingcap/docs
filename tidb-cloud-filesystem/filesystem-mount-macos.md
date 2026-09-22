---
title: Mount TiDB Cloud Filesystem on macOS
summary: Mount a TiDB Cloud Filesystem as a local directory on macOS, and use macFUSE when you need FUSE-specific features.
---

# Mount TiDB Cloud Filesystem on macOS

On macOS, you can mount a TiDB Cloud Filesystem as a local directory and access its files with your usual applications and tools.

For most workflows, you can mount a TiDB Cloud Filesystem with WebDAV. It lets you access Filesystem files through normal local file paths and does not require additional mount software.

Use FUSE with macFUSE when you also need FUSE-specific features, such as mounting a layer or checkpoint, or making pending writes reach the Filesystem without unmounting it.

Without macFUSE, TiDB Cloud CLI (`ti`) uses WebDAV. If macFUSE is installed, `ti` prefers FUSE when the mount driver is selected automatically. The commands in this guide specify the driver explicitly so that you know which mount method is being used.

> **Note:**
>
> TiDB Cloud Filesystem is currently in public preview. Its features and interfaces are subject to change without notice.

## Prerequisites

Before you begin:

- [Install TiDB Cloud CLI (`ti`)](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli).
- Make the Filesystem and its token available to `ti`. See [Access an Existing TiDB Cloud Filesystem](/tidb-cloud-filesystem/access-filesystem.md).

The write examples below require a token with write permission.

## Mount with WebDAV

For most workflows, you can use WebDAV without installing additional mount software.

1. Create a local directory for the mount:

    ```bash
    mkdir -p "$HOME/workspace"
    ```

2. Mount the Filesystem with WebDAV:

    ```bash
    ti fs mount-file-system \
      --mount-path "$HOME/workspace" \
      --driver webdav
    ```

    The mount continues running in the background after the command returns, so closing the terminal does not unmount it.

    After the command succeeds, you can access the Filesystem through `$HOME/workspace`.

    If your Filesystem token grants access only to a specific remote path, use the following command instead of the preceding mount command:

    ```bash
    ti fs mount-file-system \
      --remote-path /workspace \
      --mount-path "$HOME/workspace" \
      --driver webdav
    ```

    In this example, the remote `/workspace` directory becomes the root of the local mount. For more information, see [Mount only part of the Filesystem](/tidb-cloud-filesystem/filesystem-mount.md#mount-only-part-of-the-filesystem).

    To prevent writes through the local mount, add `--read-only` to the mount command. For example, to mount the Filesystem root as read-only:

    ```bash
    ti fs mount-file-system \
      --mount-path "$HOME/workspace" \
      --driver webdav \
      --read-only
    ```

    The `--read-only` option affects this local mount only. Use a scoped token with read-only permissions to enforce read-only access at the Filesystem service.

3. Verify that you can access the mounted Filesystem:

    ```bash
    ls "$HOME/workspace"
    ```

    If you used a writable mount and your token has write permission, you can also create and read a test file:

    ```bash
    TEST_FILE="mount-check-$(date +%s).txt"

    printf 'Hello from macOS\n' > "$HOME/workspace/$TEST_FILE"
    cat "$HOME/workspace/$TEST_FILE"
    ```

    Example output:

    ```text
    Hello from macOS
    ```

4. When you are finished, close files that are open in applications and unmount the Filesystem:

    ```bash
    ti fs unmount-file-system --mount-path "$HOME/workspace"
    ```

    WebDAV does not support `drain-file-system`. Complete a normal unmount before shutting down the machine or handing updated files to another user or environment.

    If you created the test file above, you can optionally verify after unmounting that the file is available directly from the Filesystem:

    ```bash
    ti fs read-file --path "/$TEST_FILE"
    ```

    Example output:

    ```text
    Hello from macOS
    ```

Unmounting removes the local mount but does not delete the Filesystem or its data.

## Use macFUSE when you need FUSE features

Use FUSE instead of WebDAV when you need to:

- mount a layer or checkpoint; or
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

    The mount continues running in the background after the command returns, so closing the terminal does not unmount it.

    Run the FUSE mount and the applications that access it as the same OS user.

    If your Filesystem token grants access only to a specific remote path, add `--remote-path` as described in [Mount only part of the Filesystem](/tidb-cloud-filesystem/filesystem-mount.md#mount-only-part-of-the-filesystem) instead of mounting the Filesystem root.

    Layer and checkpoint mounts require FUSE, and checkpoint mounts are always read-only. For details, see [Manage TiDB Cloud Filesystem Layers and Checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md).

    If you need pending writes to reach the Filesystem while keeping the mount running, see [FUSE write behavior](/tidb-cloud-filesystem/filesystem-mount.md#fuse-write-behavior). For command syntax, see [`drain-file-system`](/ai/ti/reference/ti-fs-drain-file-system.md).

4. When you are finished, stop applications from writing to the mount, close open files, and unmount it:

    ```bash
    ti fs unmount-file-system --mount-path "$HOME/workspace"
    ```

    A successful FUSE unmount flushes pending writes. You do not need to run `drain-file-system` before a normal unmount.

Unmounting removes the local mount but does not delete the Filesystem or its data.

## Flush FUSE writes without unmounting

If you need pending writes to reach the Filesystem while keeping the FUSE mount running, stop applications from writing to the relevant files and close those files first. Then drain the mount:

```bash
ti fs drain-file-system \
  --mount-path "$HOME/workspace" \
  --timeout 30s
```

A successful drain confirms that pending writes have reached the Filesystem while leaving the mount running. If the drain times out or returns an error, keep the mount and machine available, resolve the error, and verify the files before ending the session or telling another user that the updates are ready. WebDAV does not support `drain-file-system`. For command syntax, see [`drain-file-system`](/ai/ti/reference/ti-fs-drain-file-system.md).

## Troubleshoot mount issues

If a WebDAV mount fails to start:

- Make sure the local mount directory exists and is writable.
- Make sure another mount is not already using the same local directory.
- Check the diagnostic log path reported by `ti` for the underlying error.

If a FUSE mount fails to start:

- Make sure macFUSE is installed.
- Complete any macOS security approvals required by macFUSE.
- Make sure the mount and the application that accesses it run as the same OS user.
- Make sure another mount is not already using the same local directory.
- Check the diagnostic log path reported by `ti`.

If unmounting fails, keep the mount process and machine running until you resolve the error and verify that required files have reached the Filesystem. Do not remove local mount data while pending writes might remain.

For additional mount errors, see [Troubleshoot TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-troubleshooting.md).

## What's next

- [Mount TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-mount.md) for read-only mounts, mounting layers or checkpoints, and other common mount options.
- [Manage TiDB Cloud Filesystem Layers and Checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md) to work with layers and checkpoints through FUSE.
- [Share a TiDB Cloud Filesystem Across Machines](/tidb-cloud-filesystem/filesystem-sharing.md) to give another user or environment access to the Filesystem.
