---
title: Mount TiDB Cloud Filesystem on macOS
summary: Mount a TiDB Cloud Filesystem with macOS WebDAV, or choose macFUSE when your workflow needs layers and historical checkpoints.
---

# Mount TiDB Cloud Filesystem on macOS

On macOS, `ti` uses WebDAV by default, so you can start with a local directory without installing FUSE. Install macFUSE and explicitly select the FUSE driver when you need layer mounts, checkpoint mounts, or the FUSE drain operation.

> **Note:**
>
> TiDB Cloud Filesystem is currently in public preview. Its features and interfaces are subject to change without notice.

## Prerequisites

Install `ti` and select a Filesystem using [a local credential or an FS token](/tidb-cloud-filesystem/filesystem-mount.md#select-a-filesystem). Use a writable owner or scoped token for the write examples below.

## Mount with the default WebDAV driver

```bash
# Mount under your home directory, not at a root-level path such as /workspace.
mkdir -p "$HOME/workspace"
ti fs mount-file-system --mount-path "$HOME/workspace"
```

The successful result identifies the `webdav` driver. You can explicitly request the same mode with `--driver webdav`.

```bash
# Verify a write through the local mount.
TEST_FILE="mount-check-$(date +%s).txt"
printf 'Hello from macOS\n' > "$HOME/workspace/$TEST_FILE"
cat "$HOME/workspace/$TEST_FILE"
```

Before a handoff or shutdown, close application files and unmount:

```bash
# WebDAV has no drain command; finish file operations and unmount normally.
ti fs unmount-file-system --mount-path "$HOME/workspace"
ti fs read-file --path "/$TEST_FILE"
```

The final command reads from the remote service, independently of the mount. WebDAV and FUSE are different filesystem interfaces; do not assume WebDAV has every FUSE or POSIX capability.

## Use macFUSE for layers and checkpoints

Install [macFUSE](https://macfuse.github.io/) and complete the installation and security approvals required for your macOS version. Installing `ti` does not install macFUSE. Follow the macFUSE installation guidance for your system; do not assume every macFUSE backend is supported by the bundled Filesystem runtime.

Unmount an existing WebDAV mount before reusing its directory with FUSE:

```bash
# Select FUSE explicitly after installing macFUSE.
ti fs mount-file-system --mount-path "$HOME/workspace" --driver fuse
```

To keep a FUSE mount online while waiting for pending writes to reach the service:

```bash
# Use this durability barrier before a layer checkpoint or cross-machine handoff.
ti fs drain-file-system --mount-path "$HOME/workspace" --timeout 30s
```

For writable layer and read-only checkpoint examples, see [Branches and Checkpoints](/tidb-cloud-filesystem/filesystem-branches-checkpoints.md). They cannot run through WebDAV.

When finished with the FUSE mount, stop writers and unmount it:

```bash
# Release the mount after pending writes have been flushed.
ti fs unmount-file-system --mount-path "$HOME/workspace"
```

## Troubleshoot startup

- Use an empty directory you can write to, such as `$HOME/workspace`. A root-level path might not be writable on macOS.
- For FUSE, verify that macFUSE installation and required approvals are complete.
- If startup fails, inspect the diagnostic log path in the CLI error. The top-level background-process error does not by itself identify the cause.
- If unmount fails, keep the process, local cache, and machine available until you resolve the failure and verify remote data.

## What's next

- [Understand mount lifecycle and durability](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely).
- [Share a read-only workspace](/tidb-cloud-filesystem/filesystem-sharing.md).
