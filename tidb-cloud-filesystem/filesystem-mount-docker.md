---
title: Mount TiDB Cloud Filesystem in Docker
summary: Mount a TiDB Cloud Filesystem inside a Docker container by giving the container access to FUSE and the required mount permissions.
---

# Mount TiDB Cloud Filesystem in Docker

To mount a TiDB Cloud Filesystem inside a Docker container, the container must be able to use FUSE on the Linux host. In addition to installing `fuse3` inside the container, you need to expose `/dev/fuse` and grant the container the permissions required to create a mount.

These steps are for Docker running on a Linux host. If your environment does not allow FUSE access or the required container privileges, use direct `ti fs` commands such as `copy-file`, `read-file`, and `list-files` instead.

> **Note:**
>
> TiDB Cloud Filesystem is currently in public preview. Its features and interfaces are subject to change without notice.

## Prerequisites

Before you begin:

- Use a Linux Docker host with `/dev/fuse` available.
- Have permission to start containers with access to `/dev/fuse` and the required mount capabilities.
- Have a Filesystem token and the region code for an existing TiDB Cloud Filesystem. See [Access an Existing TiDB Cloud Filesystem](/tidb-cloud-filesystem/access-filesystem.md).

Docker Desktop and managed container or sandbox platforms might not expose `/dev/fuse` or allow the required privileges.

> **Warning:**
>
> The examples in this guide grant the container `SYS_ADMIN` and disable its AppArmor profile with `apparmor=unconfined`. These settings give the container broader access than a standard Docker container.
>
> Use them only when permitted by your environment's security policy. Do not run untrusted code with these privileges unless your environment provides an appropriate additional isolation boundary. A scoped Filesystem token can restrict access to Filesystem data, but it does not reduce the container privileges granted by Docker.

## Provide Filesystem access to the container

On the Docker host, set the Filesystem token and region:

```bash
export TI_FS_TOKEN="<filesystem-token>"
export TI_REGION_CODE="<filesystem-region-code>"
```

Treat the Filesystem token as a secret. Do not put it in a Dockerfile or commit it to source control.

The Docker and Docker Compose examples below pass these values from the host into the container.

## Start the container

Choose either Docker or Docker Compose.

### Option 1: Use Docker

Start an interactive Ubuntu container with access to FUSE:

```bash
docker run --rm -it \
  --device /dev/fuse \
  --cap-add SYS_ADMIN \
  --security-opt apparmor=unconfined \
  --env TI_FS_TOKEN \
  --env TI_REGION_CODE \
  ubuntu:24.04 bash
```

This command does the following:

- Exposes the host's `/dev/fuse` device to the container;
- Grants the capability required to create the mount; and
- Passes the Filesystem token and region into the container.

After the container starts, continue with [Install and mount inside the container](#install-and-mount-inside-the-container).

### Option 2: Use Docker Compose

Alternatively, create a `compose.yaml` file:

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

On the Docker host, start the container and open a shell in it:

```bash
docker compose up -d
docker compose exec agent bash
```

Then continue with the steps below inside the container.

## Install and mount inside the container

The following commands use the `ubuntu:24.04` image from the examples above, which runs as `root` by default.

1. Install `fuse3` and the tools required to install `ti`:

    ```bash
    apt-get update
    apt-get install -y --no-install-recommends ca-certificates curl fuse3
    ```

2. Install TiDB Cloud CLI:

    ```bash
    curl -fsSL https://github.com/tidbcloud/ti-cli/releases/latest/download/install.sh | sh -s -- --yes
    ```

3. Add `ti` to the current shell, create a local mount directory, and mount the Filesystem:

    ```bash
    export PATH="$HOME/.ti/bin:$PATH"

    mkdir -p "$HOME/workspace"

    ti fs mount-file-system --mount-path "$HOME/workspace"
    ```

    On Linux, `ti` uses the FUSE driver by default.

4. Verify that you can access the Filesystem through the mounted directory:

    ```bash
    ls "$HOME/workspace"
    ```

If your Filesystem token grants access only to a specific path, mount that path with `--remote-path`. For example:

```bash
ti fs mount-file-system \
  --remote-path /workspace \
  --mount-path "$HOME/workspace"
```

To prevent writes through the local mount, add `--read-only`. To enforce read-only access at the Filesystem service, use a scoped token with read-only permissions.

Run the mount and the application that accesses it as the same OS user. If your application image uses a non-root user, install the required packages when building the image and create the mount as the application user at runtime.

## Stop the container safely

Before stopping or removing the container:

1. Inside the container, stop applications that are writing to the mounted directory and close open files.

2. Unmount the Filesystem:

    ```bash
    ti fs unmount-file-system --mount-path "$HOME/workspace"
    ```

    Wait for the unmount to succeed before stopping or removing the container. A successful FUSE unmount flushes pending writes.

3. Stop the container:

    - If you started it with `docker run --rm -it`, exit the shell after the unmount succeeds:

        ```bash
        exit
        ```

        Docker removes the container automatically because it was started with `--rm`.

    - If you used Docker Compose, exit the container shell, and then run the following command on the Docker host:

        ```bash
        docker compose down
        ```

Stopping or removing the container does not delete the remote Filesystem.

> **Warning:**
>
> Do not remove the container after an unmount error. Pending writes might still exist only inside the container. Keep the container running, resolve the error, and verify that the required files have reached the Filesystem first.

## What's next

- [Mount TiDB Cloud Filesystem Locally](/tidb-cloud-filesystem/filesystem-mount.md) for read-only mounts, mounting part of a Filesystem, and safe unmount behavior.
- [Share a TiDB Cloud Filesystem Across Machines](/tidb-cloud-filesystem/filesystem-sharing.md) to give another user or environment access to the same Filesystem.
- [Manage TiDB Cloud Filesystem Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md) to restrict access to specific paths and operations.
