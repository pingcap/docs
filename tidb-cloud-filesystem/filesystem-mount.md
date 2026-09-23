---
title: Mount a File System
summary: Learn when to mount a file system, which mount method to use, and the capabilities and limitations of file system mounts.
aliases: ['/ai/mount-filesystem']
---

# Mount a File System

In TiDB Cloud Filesystem, you can work with files either by [using `ti fs` commands](/tidb-cloud-filesystem/work-with-filesystem-data.md) directly or by mounting the file system as a local directory.

Mount your file system when an editor, application, agent, or other tool needs to access its files through local file paths. After mounting, the file system appears as a local directory, so the tool can read and write its files using normal filesystem operations.

If you only need to perform file operations through the CLI, such as reading, copying, organizing, or searching files, use `ti fs` commands directly instead of mounting the file system.

> **Note:**
>
> TiDB Cloud Filesystem is currently in public preview. Its features and interfaces are subject to change without notice.

## Choose a mount method

The available mount method depends on your environment:

| Environment | Mount method | Detailed Guide |
| --- | --- | --- |
| Linux | FUSE | [Mount a File System on Linux](/tidb-cloud-filesystem/filesystem-mount-linux.md) |
| macOS | WebDAV for general file access, or FUSE with macFUSE for FUSE-specific features | [Mount a File System on macOS](/tidb-cloud-filesystem/filesystem-mount-macos.md) |
| Docker on Linux | FUSE with access to `/dev/fuse` and additional container privileges | [Mount a File System in Docker](/tidb-cloud-filesystem/filesystem-mount-docker.md) |

Native file system mounting is not supported on Windows. On Windows, use direct commands such as `ti fs copy-file`, `ti fs read-file`, and `ti fs list-files` instead.

On macOS, WebDAV is sufficient for general file access and does not require additional mount software. FUSE is required for features such as mounting layers or checkpoints and using `drain-file-system`.

## Use a token without configuring a profile

If another user or system administrator gives you a file system token, you can use that token from the current machine without configuring a `ti` profile or using the creator's API keys:

```bash
export TI_FS_TOKEN="<filesystem-token>"
export TI_REGION_CODE="<filesystem-region-code>"
```

Then follow the guide for your environment. The token identifies the file system and limits the paths and operations available to the current environment. Treat the token as a secret.

## Common mount capabilities

File system mounts support several options that change what is exposed through the local mount:

### Mount only part of the file system

By default, a mount exposes the file system root `/`. Use `--remote-path` to expose a specific remote directory instead. This is also useful when a scoped token grants access only to a specific path.

### Create a read-only mount

Use `--read-only` to prevent writes through a particular mount. This option does not change the permissions of the file system token. To enforce read-only access at the service level, use a scoped token with read-only permissions.

### Mount layers and checkpoints

Layers and checkpoints require FUSE. Checkpoint mounts are always read-only.

For layer and checkpoint workflows, see [Manage File System Layers and Checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md).

## Finish safely

### Unmount when you are finished

Stop applications from writing to the mounted directory, close open files, and follow your platform guide to run `ti fs unmount-file-system`. A successful FUSE unmount flushes pending writes before stopping the mount. Unmounting removes the local mount but does not delete the file system or its data.

### FUSE write behavior

FUSE mounts can temporarily have writes that have not yet reached the remote file system.

A normal successful unmount flushes pending writes, so you do not need to run `drain-file-system` before unmounting.

Use `drain-file-system` only when you need pending writes to reach the file system while keeping the mount running, such as before creating a checkpoint or making updated files available to another environment.

WebDAV mounts do not support `drain-file-system`.

> **Warning:**
>
> If a FUSE drain or unmount fails, keep the mount and machine available until you resolve the error and verify that required files have reached the file system. Some pending writes might still exist only on that machine.

## What's next

Choose the guide for your environment:

- [Mount a File System on Linux](/tidb-cloud-filesystem/filesystem-mount-linux.md)
- [Mount a File System on macOS](/tidb-cloud-filesystem/filesystem-mount-macos.md)
- [Mount a File System in Docker](/tidb-cloud-filesystem/filesystem-mount-docker.md)

For all mount options, see the [`mount-file-system` command reference](/ai/ti/reference/ti-fs-mount-file-system.md).
