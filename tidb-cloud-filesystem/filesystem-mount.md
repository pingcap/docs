---
title: Mount TiDB Cloud Filesystem Locally
summary: Select a Filesystem and mount driver, access remote files from a local directory, and stop a mount without losing pending writes.
aliases: ['/ai/mount-filesystem']
---

# Mount TiDB Cloud Filesystem Locally

A mount makes remote files available at a local directory. Use it when your editor, application, or agent expects filesystem paths instead of file-transfer commands. The remote Filesystem persists independently of the mount process.

> **Note:**
>
> TiDB Cloud Filesystem is currently in public preview. Its features and interfaces are subject to change without notice.

## Choose your environment

- [Linux](/tidb-cloud-filesystem/filesystem-mount-linux.md): use FUSE3 and an accessible `/dev/fuse` device.
- [macOS](/tidb-cloud-filesystem/filesystem-mount-macos.md): use the default WebDAV driver, or install macFUSE and explicitly select FUSE for layers and checkpoints.
- [Docker and Docker Compose](/tidb-cloud-filesystem/filesystem-mount-docker.md): expose the Linux host's FUSE device and allow mounting inside the container.

Native Windows mounting is not supported by `ti`. Use direct commands such as `ti fs copy-file`, `ti fs read-file`, and `ti fs list-files` instead.

With `--driver auto`, the CLI selects WebDAV on macOS and FUSE on Linux. To mount a layer or checkpoint on macOS, install macFUSE and select `--driver fuse`. WebDAV mounting is not supported on Linux.

## Select a Filesystem

### Use a locally stored token

After creating a Filesystem with the CLI, select its ID:

```bash
# Select the Filesystem whose token is already stored locally.
export TI_FS_FILE_SYSTEM_ID="<file-system-id>"
```

The CLI uses the selected resource's stored token and region information. You can pass `--file-system-id` on each command instead. There is no default Filesystem selected merely because only one resource exists.

### Use a token without configuring a profile

On a machine with `ti` installed, provide the token through a secret manager or the environment:

```bash
# Inject these values from your secret manager in automation.
export TI_FS_TOKEN="<filesystem-token>"
export TI_REGION_CODE="aws-us-east-1"
```

Set the region to where this Filesystem was created. `ti` derives the Filesystem ID from the token; neither `ti configure` nor `TI_FS_FILE_SYSTEM_ID` is required. A supplied ID must match the token. If your shell already has an ID for another Filesystem, clear it before using the token-only workflow.

Use an owner token for full Filesystem access, or a scoped token with the operations required by the application. For a token restricted to `/workspace`, mount that subtree rather than `/`. See [Authorization](/tidb-cloud-filesystem/filesystem-authorization.md).

## Mount and use the files

After installing the platform dependencies, mount the selected Filesystem:

```bash
# Use an empty directory owned by the user who will access the mount.
mkdir -p "$HOME/workspace"
ti fs mount-file-system --mount-path "$HOME/workspace"
```

The command waits for readiness and returns a structured result with `status: mounted`. A background companion process keeps the mount alive. Closing the terminal does not unmount it, but terminating that process or the machine interrupts access.

To expose only one remote directory, pass `--remote-path /workspace`. To make a mount read-only, add `--read-only`. These are client-side mount settings, not substitutes for a scoped token's server-enforced permissions.

To mount a layer or a read-only checkpoint, select the FUSE driver and use the layer options in the [`mount-file-system` command reference](/ai/ti/reference/ti-fs-mount-file-system.md).

```bash
# These are ordinary local filesystem commands, not CLI subcommands.
ls "$HOME/workspace"
printf 'Written through the mount\n' > "$HOME/workspace/mounted.txt"
cat "$HOME/workspace/mounted.txt"
```

The write example requires a writable mount and token. Use the same OS user for mounting and file access; changing a directory's ownership does not grant another user access through an existing FUSE mount.

## Finish safely

Stop applications writing to the mount and close their files. If you need pending writes to reach the service while keeping a FUSE mount online, such as before creating a checkpoint or handing work to another machine, drain it:

```bash
# FUSE only: wait for pending remote writes without unmounting.
ti fs drain-file-system --mount-path "$HOME/workspace" --timeout 30s
```

When finished, unmount:

```bash
# Graceful unmount flushes pending FUSE work before stopping the mount.
ti fs unmount-file-system --mount-path "$HOME/workspace"
```

An explicit drain is not required before every normal unmount. WebDAV does not support drain: close application files and complete a normal unmount before a handoff. Drain and unmount use the local mount locator and do not require you to provide the region or token again. The running mount still needs valid credentials to finish remote work.

> **Warning:**
>
> Do not destroy a sandbox, stop its mount process, or delete its local cache after a drain or unmount error. Pending writes might exist only on that machine. Resolve the error and verify remote data before removing the environment. Unmounting does not delete the remote Filesystem.

## What's next

- [Share a Filesystem across environments](/tidb-cloud-filesystem/filesystem-sharing.md).
- [Manage layers and checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md).
- [Look up mount options](/ai/ti/reference/ti-fs-mount-file-system.md).
