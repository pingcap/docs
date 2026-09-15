---
title: Mount TiDB Cloud Filesystem in Docker
summary: Configure Docker or Docker Compose with a FUSE device, mount permissions, and a Filesystem token to use persistent remote files.
---

# Mount TiDB Cloud Filesystem in Docker

A container needs both FUSE userspace tools and permission to use the Linux host's FUSE device. Installing `fuse3` inside an otherwise restricted container is not sufficient.

> **Note:**
>
> TiDB Cloud Filesystem is currently in public preview. Its features and interfaces are subject to change without notice.

## Prerequisites

- A Linux Docker host with an accessible `/dev/fuse` device.
- An FS token for the existing Filesystem and its region code.
- Permission to start a container with the device and capabilities below.

These examples target a Linux Docker host. Do not assume Docker Desktop's VM or a managed sandbox exposes the same device and security controls. If mounting is unavailable, use direct `ti fs` file commands instead.

> **Warning:**
>
> `SYS_ADMIN` grants broad privileges, and `apparmor=unconfined` disables the container's AppArmor profile. Use these settings only in an environment whose security policy permits them. A scoped FS token limits remote data access but does not restore container isolation. Do not grant these privileges to untrusted agent code without an appropriate isolation boundary.

## Start with Docker

On the host, provide the token through your secret manager and set the matching region:

```bash
# Do not put a real token in a Dockerfile or commit it to source control.
export TI_FS_TOKEN="<filesystem-token>"
export TI_REGION_CODE="aws-us-east-1"
```

Start an interactive container:

```bash
# Expose FUSE and the permissions needed to create the mount.
docker run --rm -it \
  --device /dev/fuse \
  --cap-add SYS_ADMIN \
  --security-opt apparmor=unconfined \
  --env TI_FS_TOKEN \
  --env TI_REGION_CODE \
  ubuntu:24.04 bash
```

The device option exposes `/dev/fuse`; `SYS_ADMIN` permits the mount operation; the security option removes AppArmor restrictions that could otherwise reject it. A host's other security controls can still prohibit mounting.

Continue with [Install and mount inside the container](/tidb-cloud-filesystem/filesystem-mount-docker.md#install-and-mount-inside-the-container).

## Start with Docker Compose

As an alternative to `docker run`, use the following `compose.yaml`. It reads the same two environment variables from the host:

```yaml
services:
  agent:
    image: ubuntu:24.04
    command: ["sleep", "infinity"]
    devices:
      - /dev/fuse:/dev/fuse
    cap_add:
      - SYS_ADMIN
    security_opt:
      - apparmor=unconfined
    environment:
      TI_FS_TOKEN: ${TI_FS_TOKEN:?Set TI_FS_TOKEN}
      TI_REGION_CODE: ${TI_REGION_CODE:?Set TI_REGION_CODE}
```

```bash
# Start the container, then open its shell.
docker compose up -d
docker compose exec agent bash
```

## Install and mount inside the container

Run these commands inside the container. This Ubuntu image starts as root, so no `sudo` is needed for package installation:

```bash
# Install HTTPS download support and the FUSE3 mount helper.
apt-get update
apt-get install -y --no-install-recommends ca-certificates curl fuse3
```

Install the CLI:

```bash
# The installer includes the Filesystem mount runtime.
curl -fsSL https://github.com/tidbcloud/ti-cli/releases/latest/download/install.sh | sh -s -- --yes
```

After installation, prepare the current shell and mount:

```bash
# The token identifies the Filesystem; no profile configuration is needed.
export PATH="$HOME/.ti/bin:$PATH"
mkdir -p "$HOME/workspace"
ti fs mount-file-system --mount-path "$HOME/workspace" --driver fuse
ls "$HOME/workspace"
```

For a token restricted to a subtree, add the matching `--remote-path`, for example `/workspace`. Add `--read-only` for a read-only token. Keep the application and mount under the same OS user. If your application image uses a non-root user, install dependencies while building the image and mount as the application user at runtime.

## Stop the container safely

Stop application writes, close files, and unmount inside the container:

```bash
# Wait for a successful unmount before destroying the container.
ti fs unmount-file-system --mount-path "$HOME/workspace" && exit
```

The `docker run --rm` container is removed after its shell exits. For Compose, run the following on the host only after the unmount succeeds:

```bash
# Remove the container after the mount has stopped cleanly.
docker compose down
```

The remote Filesystem remains available. Removing the container before pending writes reach the service can lose those writes; an automatic container timeout is not a graceful unmount.

## What's next

- [Share data with the next sandbox](/tidb-cloud-filesystem/filesystem-sharing.md).
- [Restrict tokens to the required paths and operations](/tidb-cloud-filesystem/filesystem-authorization.md).
