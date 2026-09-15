---
title: Mount TiDB Cloud Filesystem on Linux
summary: Set up FUSE3 on Linux, mount a TiDB Cloud Filesystem as the application user, and troubleshoot mount permission errors.
---

# Mount TiDB Cloud Filesystem on Linux

Linux mounts use FUSE to route local filesystem operations to TiDB Cloud Filesystem. Applications can use the mounted directory without adopting a storage SDK.

> **Note:**
>
> TiDB Cloud Filesystem is currently in public preview. Its features and interfaces are subject to change without notice.

## Prerequisites

- Install `ti` and select a Filesystem using [a local credential or an FS token](/tidb-cloud-filesystem/filesystem-mount.md#select-a-filesystem).
- Use a Linux host with FUSE support. For a container, follow [Docker and Docker Compose](/tidb-cloud-filesystem/filesystem-mount-docker.md) instead.
- Run the mount and application as the same OS user.

## Install FUSE3

On Ubuntu or Debian:

```bash
# Install the mount helper; this administrative step might require sudo.
sudo apt-get update
sudo apt-get install -y --no-install-recommends fuse3
```

Check the helper and device:

```bash
# Both the helper and the kernel device must be available.
command -v fusermount3
ls -l /dev/fuse
```

On another distribution, install its FUSE3 package. If `/dev/fuse` is missing or inaccessible, have the host administrator enable FUSE and grant the mounting user access. Installing a library alone does not provide a usable mount environment.

## Mount and verify

Use an empty directory under your home directory:

```bash
# Keep the mount owned and used by the current OS user.
mkdir -p "$HOME/workspace"
ti fs mount-file-system --mount-path "$HOME/workspace" --driver fuse
```

With a writable token, write a test file and confirm it has reached the remote Filesystem:

```bash
# Use a unique filename so the test does not overwrite an existing file.
TEST_FILE="mount-check-$(date +%s).txt"
printf 'Hello from Linux\n' > "$HOME/workspace/$TEST_FILE"
ti fs drain-file-system --mount-path "$HOME/workspace" --timeout 30s
ti fs read-file --path "/$TEST_FILE"
```

This example mounts the remote root `/`. If you mounted a subtree, include that remote prefix in the `read-file` path.

When finished, stop writers and unmount:

```bash
# Stop the mount without deleting the remote Filesystem.
ti fs unmount-file-system --mount-path "$HOME/workspace"
```

## Diagnose permission errors

If `fusermount3` reports `Permission denied`, check the local mount path, `/dev/fuse` access, and the host's security policy. This error is not necessarily a TiDB Cloud credential failure.

Ubuntu 26.04 can apply an AppArmor profile to `fusermount3` that allows paths under home directories but rejects a top-level path such as `/workspace`. Becoming root or running `chown` on `/workspace` does not bypass that policy. Prefer `$HOME/workspace`; if the application requires another path, ask the administrator to update the narrow AppArmor rule described in [Ubuntu mount-path restrictions](/ai/ti/guides/mount-filesystem.md#ubuntu-2604-mount-paths).

A root-created FUSE mount is also not automatically usable by an application running as a different user. Mount as the user that will run the application rather than trying to repair access with `chown` afterward.

For startup failures, inspect the diagnostic log path shown by the CLI. Do not repeatedly start mounts at the same path without checking whether a previous mount is still present.

## What's next

- [Use layers and checkpoints](/tidb-cloud-filesystem/filesystem-branches-checkpoints.md).
- [Share files with another machine](/tidb-cloud-filesystem/filesystem-sharing.md).
