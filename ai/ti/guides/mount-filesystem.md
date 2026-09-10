---
title: Mount a TiDB Cloud Filesystem
summary: Learn how to safely mount, use, drain, and unmount a TiDB Cloud Filesystem on macOS, Linux, Windows, or in a container.
---

# Mount a TiDB Cloud Filesystem

Mount a TiDB Cloud Filesystem when an application needs to access remote data through a local filesystem path.

## Prerequisites

- Obtain access to a TiDB Cloud Filesystem.
- On Linux, install FUSE3 and provide access to `/dev/fuse`.
- On Windows, enable the Windows WebClient service.

## Choose a mount driver

| Platform | `--driver auto` | Notes |
|---|---|---|
| macOS | WebDAV | Install macFUSE and select `--driver fuse` for FUSE support. |
| Linux | FUSE | Install `davfs2` to select WebDAV explicitly. |
| Windows | WebDAV | Use a drive letter such as `X:`. FUSE is unavailable. |

## Mount the Filesystem

Create a local path and mount the Filesystem in the background:

```shell
mkdir -p /path/to/workspace
ti fs mount-file-system \
  --file-system-id "<file-system-id>" \
  --mount-path /path/to/workspace
```

Use `--remote-path` to expose a subtree or `--read-only` to prevent writes. To mount a layer or checkpoint, select the FUSE driver and pass the appropriate layer options described in the [`mount-file-system` reference](/ai/ti/reference/commands/fs/ti-fs-mount-file-system.md).

## Mount in a container

Installing FUSE3 in an image is not sufficient. The host must expose `/dev/fuse`, and the container must be allowed to perform the mount. For Docker, provide settings equivalent to the following:

```shell
docker run --rm -it \
  --device /dev/fuse \
  --cap-add SYS_ADMIN \
  --security-opt apparmor=unconfined \
  --env TI_FS_TOKEN \
  --env TI_REGION_CODE \
  <image>
```

For Docker Compose, pass the same device, capability, security, and environment settings:

```yaml
services:
  agent:
    image: <image>
    devices:
      - /dev/fuse:/dev/fuse
    cap_add:
      - SYS_ADMIN
    security_opt:
      - apparmor=unconfined
    environment:
      TI_FS_TOKEN: ${TI_FS_TOKEN}
      TI_REGION_CODE: ${TI_REGION_CODE}
      TI_FS_FILE_SYSTEM_ID: ${TI_FS_FILE_SYSTEM_ID}
```

> **Warning:**
>
> `SYS_ADMIN` and an unconfined AppArmor profile weaken container isolation. Use them only for a dedicated, trusted container. When FUSE access is unavailable, use `ti fs` data commands without a mount.

## Ubuntu 26.04 mount paths

Ubuntu 26.04 applies an AppArmor profile to `/usr/bin/fusermount3`. By default, use a path under the current user's home directory, `/mnt`, `/media`, `/tmp`, or `/run/user/<uid>` instead of `/workspace`.

For example:

```shell
mkdir -p "$HOME/workspace"
ti fs mount-file-system \
  --file-system-id "<file-system-id>" \
  --mount-path "$HOME/workspace"
```

If an application requires `/workspace`, add the following rules to `/etc/apparmor.d/local/fusermount3`:

```text
mount fstype=@{fuse_types} options=(nosuid,nodev) options in (ro,rw,noatime,dirsync,nodiratime,noexec,sync) -> /workspace/{,**/},
umount /workspace/{,**/},
```

Then reload the profile:

```shell
sudo apparmor_parser -r /etc/apparmor.d/fusermount3
```

For related errors, see [Troubleshoot TiDB Cloud CLI](/ai/ti/reference/ti-troubleshooting.md).

## Drain or unmount

A normal unmount flushes open handles and pending FUSE work before stopping the mount:

```shell
ti fs unmount-file-system --mount-path /path/to/workspace
```

Use drain when you need a durability barrier while keeping a FUSE mount online:

```shell
ti fs drain-file-system --mount-path /path/to/workspace --timeout 30s
```

Drain is not supported for WebDAV.

> **Warning:**
>
> Do not terminate a machine while writes remain pending or after unmount returns an error. In-memory writes and local-only overlay files can be lost.

## What's next

- [Manage Filesystem Layers and Checkpoints](/ai/ti/guides/manage-filesystem-layers.md)
- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
