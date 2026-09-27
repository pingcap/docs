---
title: Mount a File System on macOS
summary: Learn how to mount a TiDB Cloud file system on macOS, choose WebDAV or macFUSE, verify reads and writes, and unmount safely.
---

# Mount a File System on macOS

On macOS, you can mount a file system in TiDB Cloud Filesystem as a local directory and access its files with your usual applications and tools.

For general file access, WebDAV requires no additional mount software. Use FUSE with macFUSE to mount layers or checkpoints, or to flush pending writes while keeping the mount running.

For automatic driver selection, TiDB Cloud CLI (`ti`) prefers FUSE when macFUSE is installed and uses WebDAV otherwise. The examples specify a driver explicitly to make the choice clear.

> **Note:**
>
> TiDB Cloud Filesystem is currently in public preview. Its features and interfaces are subject to change without notice.

## Prerequisites

Before you begin:

- [Install TiDB Cloud CLI (`ti`)](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli).
- Make the file system and its token available to `ti`. See [Access an Existing File System](/tidb-cloud-filesystem/access-filesystem.md).

Use Bash or Zsh and keep the same shell open for each procedure.

## Mount with WebDAV

Use an owner token or a scoped token with `read,list,write,delete` permissions on the remote directory. These permissions cover both verification and cleanup. Upload a small file, update it through WebDAV, and verify the update after unmounting.

WebDAV does not support `--read-only`. Use a scoped token with only `read` and `list` permissions to enforce read-only access at the service. For a local read-only mount, use macFUSE with `--driver fuse --read-only`. See [Share a File System](/tidb-cloud-filesystem/filesystem-sharing.md#mount-the-shared-directory-optional).

1. Select the remote directory and create an empty local mount directory. For a token scoped to one directory, replace `/` with that directory's path:

    ```bash
    remote_path="/"
    mount_dir="$(mktemp -d "$HOME/ti-fs-webdav.XXXXXX")"
    ```

2. Upload a unique sample file to that remote directory:

    ```bash
    test_file="mount-check-$(date +%s)-$$.txt"
    printf 'Hello from the service\n' | ti fs copy-file \
      --from-stdin --to-remote "${remote_path%/}/$test_file"
    ```

3. Mount the directory with WebDAV:

    ```bash
    ti fs mount-file-system \
      --remote-path "$remote_path" \
      --mount-path "$mount_dir" \
      --driver webdav
    ```

    The remote directory becomes the mount root. The mount runs in the background until you unmount it.

4. Read the uploaded file:

    ```bash
    cat "$mount_dir/$test_file"
    ```

    Expected output: `Hello from the service`. If a file operation takes longer than 30 seconds, interrupt it with Ctrl+C and follow [mount troubleshooting](/tidb-cloud-filesystem/filesystem-troubleshooting.md#mount-succeeds-but-file-access-hangs) before continuing.

5. Update the file through the mount:

    ```bash
    printf 'Hello from macOS\n' > "$mount_dir/$test_file"
    ```

6. Close applications using the mount and unmount it normally:

    ```bash
    ti fs unmount-file-system --mount-path "$mount_dir"
    ```

    WebDAV does not support `drain-file-system`. If unmount fails, keep the machine and local mount data available and follow [Finish safely](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely).

7. After successful unmount, read the update directly from the service:

    ```bash
    ti fs read-file --path "${remote_path%/}/$test_file"
    ```

    Expected output: `Hello from macOS`.

8. Delete the sample file and empty mount directory:

    ```bash
    ti fs delete-file --path "${remote_path%/}/$test_file"
    rmdir "$mount_dir"
    ```

The file system remains available for reuse.

## Use macFUSE when you need FUSE features

Use FUSE instead of WebDAV when you need to:

- Mount a layer or checkpoint.
- Flush pending writes with `drain-file-system` while keeping the mount running.

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

3. Mount the file system with FUSE:

    ```bash
    ti fs mount-file-system \
      --mount-path "$HOME/workspace" \
      --driver fuse
    ```

    The mount continues running in the background after the command returns, so closing the terminal does not unmount it.

    Run the FUSE mount and the applications that access it as the same OS user.

    If your file system token grants access only to a specific remote path, add `--remote-path` as described in [Mount only part of the file system](/tidb-cloud-filesystem/filesystem-mount.md#mount-only-part-of-the-file-system) instead of mounting the file system root.

    Layer and checkpoint mounts require FUSE, and checkpoint mounts are always read-only. For details, see [Manage File System Layers and Checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md).

    If you need pending writes to reach the file system while keeping the mount running, see [FUSE write behavior](/tidb-cloud-filesystem/filesystem-mount.md#fuse-write-behavior). For command syntax, see [`drain-file-system`](/ai/ti/reference/ti-fs-drain-file-system.md).

4. When you are finished, stop applications from writing to the mount, close open files, and unmount it:

    ```bash
    ti fs unmount-file-system --mount-path "$HOME/workspace"
    ```

    A successful FUSE unmount flushes pending writes. You do not need to run `drain-file-system` before a normal unmount.

Unmounting removes the local mount but does not delete the file system or its data.

## Flush FUSE writes without unmounting

If you need pending writes to reach the file system while keeping the FUSE mount running, stop applications from writing to the relevant files and close those files first. Then drain the mount:

```bash
ti fs drain-file-system \
  --mount-path "$HOME/workspace" \
  --timeout 30s
```

A successful drain confirms that pending writes have reached the file system while leaving the mount running. If the drain times out or returns an error, keep the mount and machine available, resolve the error, and verify the files before ending the session or telling another user that the updates are ready. WebDAV does not support `drain-file-system`. For command syntax, see [`drain-file-system`](/ai/ti/reference/ti-fs-drain-file-system.md).

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

If unmounting fails, keep the mount process and machine running until you resolve the error and verify that required files have reached the file system. Do not remove local mount data while pending writes might remain.

For additional mount errors, see [Troubleshoot TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-troubleshooting.md).

## What's next

- [Mount a File System](/tidb-cloud-filesystem/filesystem-mount.md) for read-only mounts, mounting layers or checkpoints, and other common mount options.
- [Manage File System Layers and Checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md) to work with layers and checkpoints through FUSE.
- [Share a File System Across Machines](/tidb-cloud-filesystem/filesystem-sharing.md) to give another user or environment access to the file system.
