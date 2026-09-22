---
title: Mount TiDB Cloud Filesystem in Docker
summary: Mount a TiDB Cloud Filesystem inside a Docker container on a Linux host by enabling FUSE and the required container permissions.
---

# Mount TiDB Cloud Filesystem in Docker

To mount a TiDB Cloud Filesystem inside a Docker container, the container must have access to FUSE on the Linux host. In addition to installing `fuse3` inside the container, you need to expose `/dev/fuse` and grant the container permission to create the mount.

This guide covers both Docker and Docker Compose on a Linux host. If your environment does not provide FUSE access or allow the required container privileges, use direct `ti fs` commands such as `copy-file`, `read-file`, and `list-files` instead.

> **Note:**
>
> TiDB Cloud Filesystem is currently in public preview. Its features and interfaces are subject to change without notice.

## Prerequisites

Before you begin:

- Use a Linux Docker host where `/dev/fuse` is available.
- Have permission to start containers with access to `/dev/fuse` and the capabilities required to create a mount.
- Have a Filesystem token and region code for an existing TiDB Cloud Filesystem. See [Access an Existing TiDB Cloud Filesystem](/tidb-cloud-filesystem/access-filesystem.md).

Docker Desktop and managed container or sandbox environments might not expose `/dev/fuse` or allow the required privileges.

> **Warning:**
>
> The examples in this guide grant the container `SYS_ADMIN` and disable its AppArmor profile with `apparmor=unconfined`. These settings give the container broader privileges than a standard Docker container.
>
> Use them only when permitted by your environment's security policy. Do not run untrusted code with these privileges unless your environment provides an appropriate additional isolation boundary. A scoped Filesystem token can restrict access to Filesystem data, but it does not reduce the privileges granted to the container by Docker.

## Provide Filesystem access to the container

On the Docker host, set the Filesystem token and region code:

```bash
export TI_FS_TOKEN="<filesystem-token>"
export TI_REGION_CODE="<filesystem-region-code>"
```

Treat the Filesystem token as a secret. Do not put it in a Dockerfile or commit it to source control.

The Docker and Docker Compose examples below pass these environment variables from the host into the container.

## Start the container

Choose either Docker or Docker Compose.

### Use Docker

On the Docker host, start an interactive Ubuntu container with access to FUSE:

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
- Passes the Filesystem token and region code into the container.

After the container starts, continue with [Install and mount inside the container](#install-and-mount-inside-the-container).

### Use Docker Compose

Alternatively, create the following `compose.yaml` file on the Docker host:

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

Start the container and open a shell in it:

```bash
docker compose up -d
docker compose exec agent bash
```

Then continue with the steps below inside the container.

## Install and mount inside the container

The following steps run inside the container. They use the `ubuntu:24.04` image from the preceding examples, which runs as `root` by default.

1. Install `fuse3` and the tools required to install `ti`:

    ```bash
    apt-get update
    apt-get install -y --no-install-recommends ca-certificates curl fuse3
    ```

2. Install TiDB Cloud CLI:

    ```bash
    curl -fsSL https://github.com/tidbcloud/ti-cli/releases/latest/download/install.sh | sh -s -- --yes
    ```

3. Add `ti` to the current shell and create a local directory for the mount:

    ```bash
    export PATH="$HOME/.ti/bin:$PATH"

    mkdir -p "$HOME/workspace"
    ```

4. Mount the Filesystem:

    ```bash
    ti fs mount-file-system --mount-path "$HOME/workspace"
    ```

    On Linux, `ti` uses FUSE by default. After the command succeeds, you can access the Filesystem through `$HOME/workspace`. If the mount fails to start, inspect the diagnostic log path reported by `ti`.

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

5. Verify that you can access the mounted Filesystem:

    ```bash
    ls "$HOME/workspace"
    ```

Run the mount and the application that accesses it as the same OS user. If your application image uses a non-root user, install the required packages when building the image and create the mount as the application user at runtime.

## Flush FUSE writes without unmounting

If you need pending writes to reach the Filesystem while keeping the mount running, stop applications from writing to the relevant files and close those files first. Then drain the mount inside the container:

```bash
ti fs drain-file-system \
  --mount-path "$HOME/workspace" \
  --timeout 30s
```

A successful drain confirms that pending writes have reached the Filesystem while leaving the mount running. If the drain times out or returns an error, keep the container and Docker host available, resolve the error, and verify the files before stopping or removing the container. For command syntax, see [`drain-file-system`](/ai/ti/reference/ti-fs-drain-file-system.md).

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

Stopping or removing the container does not delete the remote Filesystem or its data.

> **Warning:**
>
> If unmounting fails, do not stop or remove the container. Pending writes might still exist only inside the container. Keep the container running, resolve the error, and verify that the required files have reached the Filesystem first.

## What's next

- [Mount TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-mount.md) for read-only mounts, mounting layers or checkpoints, and other common mount options.
- [Share a TiDB Cloud Filesystem Across Machines](/tidb-cloud-filesystem/filesystem-sharing.md) to give another user or environment access to the same Filesystem.
- [Manage TiDB Cloud Filesystem Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md) to restrict access to specific paths and operations.
