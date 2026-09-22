---
title: Mount TiDB Cloud Filesystem on Linux
summary: Install FUSE userspace tools, mount a TiDB Cloud Filesystem on Linux, verify access, and troubleshoot common mount permission issues.
---

# Mount TiDB Cloud Filesystem on Linux

On Linux, TiDB Cloud Filesystem uses FUSE to make Filesystem data available through a local directory. After mounting, your applications and tools can access the Filesystem by using ordinary local file paths.

> **Note:**
>
> TiDB Cloud Filesystem is currently in public preview. Its features and interfaces are subject to change without notice.

## Prerequisites

Before you begin:

- [Install TiDB Cloud CLI (`ti`)](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli).
- Make the Filesystem and its token available to `ti`. See [Access an Existing TiDB Cloud Filesystem](/tidb-cloud-filesystem/access-filesystem.md).
- Use a Linux host where you can install the `fuse3` package. For a container, follow [Docker and Docker Compose](/tidb-cloud-filesystem/filesystem-mount-docker.md) instead.

Run the mount and the application that accesses it as the same OS user.

## Install FUSE userspace tools

1. On Ubuntu or Debian, install the `fuse3` package:

    ```bash
    sudo apt-get update
    sudo apt-get install -y --no-install-recommends fuse3
    ```

2. Check that the FUSE mount helper is installed:

    ```bash
    command -v fusermount3
    ```

    The command prints the path to `fusermount3`, such as:

    ```text
    /usr/bin/fusermount3
    ```

3. Check that the FUSE device is available:

    ```bash
    ls -l /dev/fuse
    ```

    The command shows an entry for `/dev/fuse`.

If `fusermount3` is not found, make sure the `fuse3` package is installed. If `/dev/fuse` does not exist or you cannot use it when mounting, ask the host administrator to enable FUSE and grant your user access to the device.

On another Linux distribution, install the FUSE package that provides `fusermount3` and perform the same checks.

## Mount and verify the Filesystem

1. Create a local directory for the mount:

    ```bash
    mkdir -p "$HOME/workspace"
    ```

    Use a directory owned by the same OS user that will run the applications accessing the mount.

2. Mount the Filesystem:

    ```bash
    ti fs mount-file-system --mount-path "$HOME/workspace"
    ```

    On Linux, `ti` uses FUSE by default.

    The command waits until the mount is ready before returning. The mount continues running in the background after the command returns, so closing the terminal does not unmount it.

    After the mount succeeds, you can access the Filesystem through `$HOME/workspace`.

    If your Filesystem token grants access only to a specific remote path, use the following command instead of the preceding mount command:

    ```bash
    ti fs mount-file-system \
      --remote-path /workspace \
      --mount-path "$HOME/workspace"
    ```

    In this example, the remote `/workspace` directory becomes the root of the local mount. For more information, see [Mount only part of the Filesystem](/tidb-cloud-filesystem/filesystem-mount.md#mount-only-part-of-the-filesystem).

    To prevent writes through the local mount, add `--read-only` to the mount command. For example, to mount the Filesystem root as read-only:

    ```bash
    ti fs mount-file-system \
      --mount-path "$HOME/workspace" \
      --read-only
    ```

    The `--read-only` option affects this local mount only. Use a scoped token with read-only permissions to enforce read-only access at the Filesystem service.

3. Verify that you can access the mounted Filesystem:

    ```bash
    ls "$HOME/workspace"
    ```

    The command lists the files and directories at the root of the mounted path.

    If you used a writable mount and your token has write permission, you can also create and read a test file:

    ```bash
    TEST_FILE="mount-check-$(date +%s).txt"

    printf 'Hello from Linux\n' > "$HOME/workspace/$TEST_FILE"
    cat "$HOME/workspace/$TEST_FILE"
    ```

    Example output:

    ```text
    Hello from Linux
    ```

4. When you are finished, stop applications that are writing to the mounted directory, close open files, and unmount the Filesystem:

    ```bash
    ti fs unmount-file-system --mount-path "$HOME/workspace"
    ```

    A successful unmount flushes pending FUSE writes before stopping the mount.

    If you created the test file above, you can optionally verify after unmounting that the file is available directly from the Filesystem:

    ```bash
    ti fs read-file --path "/$TEST_FILE"
    ```

    Example output:

    ```text
    Hello from Linux
    ```

Unmounting removes the local mount but does not delete the Filesystem or its data.

> **Warning:**
>
> If unmounting fails, keep the mount and machine running until you resolve the error and verify that the required files have reached the Filesystem. Some pending writes might still exist only on that machine.

## Flush FUSE writes without unmounting

If you need pending writes to reach the Filesystem while keeping the mount running, stop applications from writing to the relevant files and close those files first. Then drain the mount:

```bash
ti fs drain-file-system \
  --mount-path "$HOME/workspace" \
  --timeout 30s
```

A successful drain confirms that pending writes have reached the Filesystem while leaving the mount running. If the drain times out or returns an error, keep the mount and machine available, resolve the error, and verify the files before ending the session or telling another user that the updates are ready. For command syntax, see [`drain-file-system`](/ai/ti/reference/ti-fs-drain-file-system.md).

## Troubleshoot mount permission errors

If the mount fails with `Permission denied`, check the following in order:

1. Make sure the mount directory is writable by the current user:

    ```bash
    ls -ld "$HOME/workspace"
    ```

2. Make sure `/dev/fuse` exists:

    ```bash
    ls -l /dev/fuse
    ```

3. Make sure you are creating the mount as the same OS user that will run the application.

    Do not create the FUSE mount as `root` and then try to give another user access by changing the ownership of the mount directory. Instead, create the mount as the application user.

4. Check whether another mount is already using the same path:

    ```bash
    mount | grep "$HOME/workspace"
    ```

    If a mount is listed, unmount it with `ti fs unmount-file-system --mount-path "$HOME/workspace"` or `fusermount3 -u "$HOME/workspace"` before creating a new mount.

5. If `ti` reports a diagnostic log path, inspect that log for the underlying error.

On systems with additional security controls, such as AppArmor, the operating system can reject a mount even when the directory permissions look correct.

For additional mount errors, see [Troubleshoot TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-troubleshooting.md).

## Ubuntu 26.04 mount-path restrictions

On Ubuntu 26.04, the AppArmor profile for `fusermount3` can prevent FUSE mounts at some paths. In particular, a top-level directory such as `/workspace` can fail with `Permission denied` even when its file permissions appear correct.

For the commands in this guide, use `$HOME/workspace` as the mount directory instead of `/workspace`.

Changing the owner of `/workspace` or running the mount as `root` does not bypass the AppArmor restriction.

If your application specifically requires `/workspace`, ask the host administrator to allow that path in `/etc/apparmor.d/local/fusermount3`:

```text
mount fstype=@{fuse_types} options=(nosuid,nodev) options in (ro,rw,noatime,dirsync,nodiratime,noexec,sync) -> /workspace/{,**/},
umount /workspace/{,**/},
```

The administrator can then reload the AppArmor profile:

```shell
sudo apparmor_parser -r /etc/apparmor.d/fusermount3
```

After the profile is updated, retry the mount at `/workspace`.

For help checking whether AppArmor caused the failure, see [Ubuntu 26.04 rejects a FUSE mount under `/workspace`](/tidb-cloud-filesystem/filesystem-troubleshooting.md#ubuntu-2604-rejects-a-fuse-mount-under-workspace).

## What's next

- [Mount TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-mount.md) for read-only mounts, mounting layers or checkpoints, and other common mount options.
- [Manage TiDB Cloud Filesystem Layers and Checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md) to mount and work with layers or checkpoints.
- [Share a TiDB Cloud Filesystem Across Machines](/tidb-cloud-filesystem/filesystem-sharing.md) to give another user or environment access to the Filesystem.
