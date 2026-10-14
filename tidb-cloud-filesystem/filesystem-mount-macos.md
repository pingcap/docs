---
title: Mount a File System on macOS
summary: Learn how to mount a TiDB Cloud file system on macOS using WebDAV or macFUSE, verify file access, and safely unmount it.
---

# Mount a File System on macOS

On macOS, you can mount a TiDB Cloud file system as a local directory and access its files with your usual applications and tools. Choose one of the following mount methods:

- **WebDAV**: Recommended for most workflows. It requires no additional mount software.
- **macFUSE**: Supports mounting layers or checkpoints, creating a local read-only mount, and flushing pending writes without unmounting the file system. It requires you to install [macFUSE](https://macfuse.github.io/).

If you do not specify the `--driver` option, TiDB Cloud CLI (`ti`) mounts the file system with WebDAV on macOS, even when macFUSE is installed. To use FUSE, specify `--driver fuse`. Layer and checkpoint mounts always require FUSE. The examples in this guide specify `--driver` explicitly so that you know which mount method is used.

> **Note:**
>
> TiDB Cloud Filesystem is currently in public preview. Its features and interfaces are subject to change without notice.

## Prerequisites

Before you begin:

- [Install TiDB Cloud CLI (`ti`)](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli).
- Have an existing TiDB Cloud file system. If you don't have one, see [Create and use a file system](/tidb-cloud-filesystem/filesystem-quick-start.md#step-3-create-and-use-a-file-system).
- Make sure `ti` is configured to access the file system using a valid token. See [Access an Existing File System](/tidb-cloud-filesystem/access-filesystem.md).

    To list and read files, your token needs `list` and `read` permissions on the remote directory. Creating or modifying files also requires `write`; deleting files requires `delete`. The WebDAV verification procedure below uses an owner token or a scoped token with all four permissions. For read-only access, see [Use WebDAV for read-only access](/tidb-cloud-filesystem/filesystem-mount-macos.md#use-webdav-for-read-only-access).

## Mount with WebDAV

For most workflows, use WebDAV to mount the file system without installing additional mount software.

Use Bash or Zsh and keep the same shell open throughout the WebDAV procedure so that the example variables remain available.

1. Prepare the local mount directory. If a file system is already mounted at `$HOME/workspace`, unmount it before reusing the directory:

    ```bash
    ti fs unmount-file-system --mount-path "$HOME/workspace"
    ```

    Then create the directory if it does not exist:

    ```bash
    mkdir -p "$HOME/workspace"
    ```

2. Select the remote directory and upload a small sample file to verify remote reads. If your token grants access only to a specific remote directory, replace `/` below with that directory, such as `/workspace`:

    ```bash
    remote_path="/"
    test_file="mount-check-$(date +%s)-$$.txt"
    printf 'Hello from the service\n' | ti fs copy-file \
      --from-stdin --to-remote "${remote_path%/}/$test_file"
    ```

    The generated file name helps avoid overwriting existing files. Continue only after the upload succeeds.

3. Mount the file system with WebDAV:

    ```bash
    ti fs mount-file-system \
      --remote-path "$remote_path" \
      --mount-path "$HOME/workspace" \
      --driver webdav
    ```

    The selected remote directory becomes the root of the local mount. For example, if `remote_path="/workspace"`, the remote `/workspace` directory is accessible through `$HOME/workspace`. For details, see [Mount only part of the file system](/tidb-cloud-filesystem/filesystem-mount.md#mount-only-part-of-the-file-system).

    The mount runs in the background until you unmount it. Closing the terminal does not unmount it.

4. List files and read the uploaded sample through the local mount:

    ```bash
    ls "$HOME/workspace"
    cat "$HOME/workspace/$test_file"
    ```

    Expected output from `cat`:

    ```text
    Hello from the service
    ```

    A directory listing alone does not confirm that file reads work. If a file operation takes longer than 30 seconds, interrupt it with Ctrl+C and follow [Mount succeeds but file access hangs](/tidb-cloud-filesystem/filesystem-troubleshooting.md#mount-succeeds-but-file-access-hangs) before continuing.

    After the read succeeds, update the sample file through the mount:

    ```bash
    printf 'Hello from macOS\n' > "$HOME/workspace/$test_file"
    ```

5. When you are finished, stop applications from writing to the mount, close open files, and unmount the file system:

    ```bash
    ti fs unmount-file-system --mount-path "$HOME/workspace"
    ```

    WebDAV does not support `drain-file-system`. If unmounting fails, keep the machine and local mount data available and follow [Finish safely](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely) before continuing.

6. After successful unmounting, verify that the update reached the service:

    ```bash
    ti fs read-file --path "${remote_path%/}/$test_file"
    ```

    Expected output:

    ```text
    Hello from macOS
    ```

    After verification succeeds, delete the sample file:

    ```bash
    ti fs delete-file --path "${remote_path%/}/$test_file"
    ```

Unmounting removes the local mount but does not delete the file system or its data.

> **Note:**
>
> Browsing a mount in Finder, with either WebDAV or FUSE, can create `.DS_Store` files and `._` companion files in the file system. These files remain after you unmount, consume storage, appear in the file count, and are visible to users who have access to the same path.
>
> If you do not want to keep them, delete them from the corresponding remote directory. For example, for the file system root:
>
> ```bash
> ti fs delete-file --path "/.DS_Store"
> ti fs delete-file --path "/._.DS_Store"
> ```

### Use WebDAV for read-only access

WebDAV does not support the `--read-only` option.

To enforce read-only access through WebDAV, use a scoped token with only `read` and `list` permissions, and mount normally without `--read-only`. The token enforces read-only access at the service.

For an example, see [Mount the shared directory](/tidb-cloud-filesystem/filesystem-sharing.md#mount-the-shared-directory-optional).

If you need the local mount itself to be read-only, use macFUSE with `--driver fuse --read-only`.

## Mount with macFUSE

Use FUSE instead of WebDAV when you need the following FUSE features:

- Mount a layer or checkpoint.
- Create a local read-only mount.
- Flush pending writes with `drain-file-system` while keeping the mount running.

To mount a file system with macFUSE on macOS, take the following steps:

1. Install [macFUSE](https://macfuse.github.io/) and complete any installation or security approval steps required by your macOS version.

    Installing `ti` does not install macFUSE.

2. Prepare the local mount directory. If a file system is already mounted at `$HOME/workspace`, unmount it before reusing the directory:

    ```bash
    ti fs unmount-file-system --mount-path "$HOME/workspace"
    ```

    Then create the directory if it does not exist:

    ```bash
    mkdir -p "$HOME/workspace"
    ```

3. Choose a FUSE mount command based on the remote directory and access mode you need. Run only the command that matches your needs.

    To mount the file system root with FUSE:

    ```bash
    ti fs mount-file-system \
      --mount-path "$HOME/workspace" \
      --driver fuse
    ```

    The mount runs in the background until you unmount it. Closing the terminal does not unmount it.

    Run the FUSE mount and applications that access it as the same OS user.

    If your token grants access only to a specific remote directory, specify it with `--remote-path`. For example, to mount `/workspace` instead of the file system root, use:

    ```bash
    ti fs mount-file-system \
      --remote-path /workspace \
      --mount-path "$HOME/workspace" \
      --driver fuse
    ```

    For details, see [Mount only part of the file system](/tidb-cloud-filesystem/filesystem-mount.md#mount-only-part-of-the-file-system).

    To make the local mount read-only, add `--read-only` to your chosen mount command. For a read-only mount of the file system root, use:

    ```bash
    ti fs mount-file-system \
      --mount-path "$HOME/workspace" \
      --driver fuse \
      --read-only
    ```

    Layer and checkpoint mounts require FUSE, and checkpoint mounts are always read-only. For details, see [Manage File System Layers and Checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md).

4. When you are finished, stop applications from writing to the mount, close open files, and unmount it:

    ```bash
    ti fs unmount-file-system --mount-path "$HOME/workspace"
    ```

    A successful FUSE unmount flushes pending writes. You do not need to run `drain-file-system` before a normal unmount. If the mount log reports `force_quit` or pending writes, see [FUSE write behavior](/tidb-cloud-filesystem/filesystem-mount.md#fuse-write-behavior).

Unmounting removes the local mount but does not delete the file system or its data.

> **Note:**
>
> Browsing a mount in Finder, with either WebDAV or FUSE, can create `.DS_Store` files and `._` companion files in the file system. These files remain after you unmount, consume storage, appear in the file count, and are visible to users who have access to the same path.
>
> If you do not want to keep them, delete them from the corresponding remote directory. For example, for the file system root:
>
> ```bash
> ti fs delete-file --path "/.DS_Store"
> ti fs delete-file --path "/._.DS_Store"
> ```

### Flush FUSE writes without unmounting

If you need pending writes to reach the file system while keeping the FUSE mount running, stop applications from writing to the relevant files and close those files first. Then drain the mount:

```bash
ti fs drain-file-system \
  --mount-path "$HOME/workspace" \
  --timeout 30s
```

A successful drain confirms that pending writes have reached the file system while leaving the mount running.

If the drain times out or returns an error, keep the mount and machine available, resolve the error, and verify the files before ending the session or making the updates available to another user or environment.

WebDAV does not support `drain-file-system`. For command syntax, see [`drain-file-system`](/ai/ti/reference/ti-fs-drain-file-system.md).

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

If a file operation takes longer than 30 seconds, interrupt it with Ctrl+C and see [Mount succeeds but file access hangs](/tidb-cloud-filesystem/filesystem-troubleshooting.md#mount-succeeds-but-file-access-hangs).

If unmounting fails, keep the mount process and machine running until you resolve the error and verify that required files have reached the file system. Do not remove local mount data while pending writes might remain.

For additional mount errors, see [Troubleshoot TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-troubleshooting.md).

## What's next

- [Mount a File System](/tidb-cloud-filesystem/filesystem-mount.md) for read-only mounts, mounting only part of a file system, and other common mount options.
- [Manage File System Layers and Checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md) to work with layers and checkpoints through FUSE.
- [Share a File System Across Machines](/tidb-cloud-filesystem/filesystem-sharing.md) to give another user or environment access to the file system.
