---
title: Mount a File System
summary: Learn when to mount a file system, which mount method to use, and the capabilities and limitations of file system mounts.
aliases: ['/ai/mount-filesystem']
---

# Mount a File System

In TiDB Cloud Filesystem, you can mount a file system as a local directory when an editor, application, agent, or other tool needs local file paths. The mount lets these tools read and write remote files using local file operations.

For CLI-only access, use [`ti fs` commands](/tidb-cloud-filesystem/work-with-filesystem-data.md) to read, copy, organize, and search files without mounting.

> **Note:**
>
> TiDB Cloud Filesystem is currently in public preview. Its features and interfaces are subject to change without notice.

## Choose a mount method

The available mount method depends on your environment:

| Environment | Mount method | Guide |
| --- | --- | --- |
| Linux | FUSE | [Mount a File System on Linux](/tidb-cloud-filesystem/filesystem-mount-linux.md) |
| macOS | WebDAV for general file access, or FUSE with macFUSE for FUSE-specific features | [Mount a File System on macOS](/tidb-cloud-filesystem/filesystem-mount-macos.md) |
| Docker on Linux | FUSE with access to `/dev/fuse` and additional container privileges | [Mount a File System in Docker](/tidb-cloud-filesystem/filesystem-mount-docker.md) |

Native file system mounting is not supported on Windows. On Windows, use direct commands such as `ti fs copy-file`, `ti fs read-file`, and `ti fs list-files` instead.

On macOS, WebDAV is sufficient for general file access and does not require additional mount software. FUSE is required for features such as mounting layers or checkpoints and using `drain-file-system`.

## Use a token without configuring a profile

With a file system token and region, you can access files without configuring a `ti` profile or supplying TiDB Cloud API keys:

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

Use `--driver fuse --read-only` to prevent writes through a FUSE mount. WebDAV does not support this option. To enforce read-only access across mounts and CLI commands, use a scoped token with only `read` and `list` permissions. The mount option does not change token permissions.

### Mount layers and checkpoints

Layers and checkpoints require FUSE. Checkpoint mounts are always read-only.

For layer and checkpoint workflows, see [Manage File System Layers and Checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md).

## Verify a mount before using it

A successful mount command or directory listing does not confirm that file reads and writes work. Read a known small file uploaded through `ti fs copy-file`. For a writable mount, write a new test file, close it, and unmount successfully. Then read the file through `ti fs read-file` to confirm that the write reached the service. For a complete example, follow the [Quick Start verification steps](/tidb-cloud-filesystem/filesystem-quick-start.md#step-4-mount-and-verify-file-access-optional).

If a small-file check has not returned after 30 seconds, interrupt it and follow [Mount succeeds but file access hangs](/tidb-cloud-filesystem/filesystem-troubleshooting.md#mount-succeeds-but-file-access-hangs). Do not start applications on the mount until verification passes.

## Finish safely

### Unmount when you are finished

Stop applications from writing to the mounted directory, close open files, and follow your platform guide to run `ti fs unmount-file-system`. Normal FUSE unmount drains pending writes before stopping the mount. Before removing the machine or its local cache, verify required files through direct CLI reads. Unmounting removes the local mount but does not delete the file system or its data.

### FUSE write behavior

FUSE mounts can buffer writes locally before sending them to the service. Normal unmount includes a drain, so you do not need to run `drain-file-system` first. If the mount log reports `force_quit` or pending writes after unmount, follow [Unmount returns success but the mount process exits abnormally](/tidb-cloud-filesystem/filesystem-troubleshooting.md#unmount-returns-success-but-the-mount-process-exits-abnormally).

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
