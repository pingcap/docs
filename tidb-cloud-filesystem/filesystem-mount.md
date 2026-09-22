---
title: Mount TiDB Cloud Filesystem
summary: Learn when to mount a TiDB Cloud Filesystem, which mount method to use, and the capabilities and limitations of Filesystem mounts.
aliases: ['/ai/mount-filesystem']
---

# Mount TiDB Cloud Filesystem

You can work with files in TiDB Cloud Filesystem either by [using `ti fs` commands](/tidb-cloud-filesystem/work-with-filesystem-data.md) directly or by mounting the Filesystem as a local directory.

Mount your TiDB Cloud Filesystem when an editor, application, agent, or other tool needs to access its files through local file paths. After mounting, the Filesystem appears as a local directory, so the tool can read and write its files using normal filesystem operations.

If you only need to perform file operations through the CLI, such as reading, copying, organizing, or searching files, use `ti fs` commands directly instead of mounting the Filesystem.

> **Note:**
>
> TiDB Cloud Filesystem is currently in public preview. Its features and interfaces are subject to change without notice.

## Choose a mount method

The available mount method depends on your environment:

| Environment | Mount method | Detailed Guide |
| --- | --- | --- |
| Linux | FUSE | [Mount TiDB Cloud Filesystem on Linux](/tidb-cloud-filesystem/filesystem-mount-linux.md) |
| macOS | WebDAV for general file access, or FUSE with macFUSE for FUSE-specific features | [Mount TiDB Cloud Filesystem on macOS](/tidb-cloud-filesystem/filesystem-mount-macos.md) |
| Docker on Linux | FUSE with access to `/dev/fuse` and additional container privileges | [Mount TiDB Cloud Filesystem in Docker](/tidb-cloud-filesystem/filesystem-mount-docker.md) |

Native Filesystem mounting is not supported on Windows. On Windows, use direct commands such as `ti fs copy-file`, `ti fs read-file`, and `ti fs list-files` instead.

On macOS, WebDAV is sufficient for general file access and does not require additional mount software. FUSE is required for features such as mounting layers or checkpoints and using `drain-file-system`.

## Use a token without configuring a profile

If another user or system administrator gives you a Filesystem token, you can use that token from the current machine without configuring a `ti` profile or using the creator's API keys:

```bash
export TI_FS_TOKEN="<filesystem-token>"
export TI_REGION_CODE="<filesystem-region-code>"
```

Then follow the guide for your environment. The token identifies the Filesystem and limits the paths and operations available to the current environment. Treat the token as a secret.

## Common mount capabilities

Filesystem mounts support several options that change what is exposed through the local mount:

### Mount only part of the Filesystem

By default, a mount exposes the Filesystem root `/`. Use `--remote-path` to expose a specific remote directory instead. This is also useful when a scoped token grants access only to a specific path.

### Create a read-only mount

Use `--read-only` to prevent writes through a particular mount. This option does not change the permissions of the Filesystem token. To enforce read-only access at the service level, use a scoped token with read-only permissions.

### Mount layers and checkpoints

Layers and checkpoints require FUSE. Checkpoint mounts are always read-only.

For layer and checkpoint workflows, see [Manage TiDB Cloud Filesystem Layers and Checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md).

## Finish safely

### Unmount when you are finished

Stop applications from writing to the mounted directory, close open files, and follow your platform guide to run `ti fs unmount-file-system`. A successful FUSE unmount flushes pending writes before stopping the mount. Unmounting removes the local mount but does not delete the Filesystem or its data.

### FUSE write behavior

FUSE mounts can temporarily have writes that have not yet reached the remote Filesystem.

A normal successful unmount flushes pending writes, so you do not need to run `drain-file-system` before unmounting.

Use `drain-file-system` only when you need pending writes to reach the Filesystem while keeping the mount running, such as before creating a checkpoint or making updated files available to another environment.

WebDAV mounts do not support `drain-file-system`.

> **Warning:**
>
> If a FUSE drain or unmount fails, keep the mount and machine available until you resolve the error and verify that required files have reached the Filesystem. Some pending writes might still exist only on that machine.

## What's next

Choose the guide for your environment:

- [Mount TiDB Cloud Filesystem on Linux](/tidb-cloud-filesystem/filesystem-mount-linux.md)
- [Mount TiDB Cloud Filesystem on macOS](/tidb-cloud-filesystem/filesystem-mount-macos.md)
- [Mount TiDB Cloud Filesystem in Docker](/tidb-cloud-filesystem/filesystem-mount-docker.md)

For all mount options, see the [`mount-file-system` command reference](/ai/ti/reference/ti-fs-mount-file-system.md).
