---
title: Use TiDB Cloud Filesystem in an Agent Sandbox
summary: Provision a file system on a trusted machine and give a clean agent sandbox config-free access without TiDB Cloud API keys.
---

# Use TiDB Cloud Filesystem in an Agent Sandbox

This workflow gives an ephemeral coding agent a durable, shared workspace without copying a user's complete TiDB Cloud CLI configuration into the sandbox. Use it when the sandbox's local disk is disposable but the agent needs artifacts, repository state, or files from previous sessions or other workers without rebuilding that state for every sandbox.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

> **Note:**
>
> For a hands-on version of this workflow, open the [TiDB Cloud Filesystem for Agent Sandbox Lab](https://labs.tidb.io/labs/demo_901). This interactive Lab Guide walks you through using a persistent file system in an agent sandbox.

## How it works

A trusted machine provisions the file system once. The sandbox receives only the file system owner token and region code, so it can use ordinary file operations and data-plane, mount, Git, journal, and vault workflows without `ti configure`, a copied `~/.ti/` directory, or TiDB Cloud API keys. This also avoids the application-specific upload and download logic required by generic object-storage APIs. The token identifies the file system. When an agent needs only selected secrets, use a delegated vault token instead of the owner token.

## Prerequisites

- Install and configure the TiDB Cloud CLI on a trusted machine.
- Install the TiDB Cloud CLI in the sandbox by using the release installer.
- Install `jq` on the trusted machine.
- Use a secure secret manager or encrypted sandbox input for token transfer.

## Step 1. Provision on the trusted machine

```bash
umask 077
ti fs create-file-system --wait > ./filesystem.json
export FILE_SYSTEM_ID="$(jq -r '.file_system_id' ./filesystem.json)"
export TI_FS_TOKEN="$(jq -r '.fs_token' ./filesystem.json)"
```

Store the token in a secret manager, record `FILE_SYSTEM_ID` for control-plane cleanup, and record the region code used to create the file system. Delete `filesystem.json` after storing the token securely.

## Step 2. Inject the minimum sandbox environment

Configure the sandbox secret/environment mechanism with:

```bash
TI_FS_TOKEN=<owner-token>
TI_REGION_CODE=<filesystem-region-code>
```

The sandbox does not need `TIDB_CLOUD_PUBLIC_KEY`, `TIDB_CLOUD_PRIVATE_KEY`, `ti configure`, or files copied from `~/.ti/`.

## Step 3. Verify direct access

In the sandbox:

```bash
printf 'sandbox ready\n' | ti fs copy-file \
  --from-stdin \
  --to-remote /sandbox/status.txt

ti fs read-file --path /sandbox/status.txt
```

Expected output:

```text
sandbox ready
```

## Step 4. Optionally mount the file system

On Linux with FUSE:

```bash
mkdir -p "$HOME/workspace"
ti fs mount-file-system \
  --mount-path "$HOME/workspace" \
  --driver fuse

cat "$HOME/workspace/sandbox/status.txt"
```

On macOS, omit `--driver fuse` to use WebDAV, which requires no FUSE installation. Install macFUSE and select FUSE when you need FUSE-specific capabilities such as Git workspaces, layers, or online drain. For platform requirements and mount-path restrictions, see [Mount a File System](/tidb-cloud-filesystem/filesystem-mount.md).

After mounting, you can use `ti fs-git`, `ti fs-journal`, and owner-authorized `ti fs-vault` commands with the same FS environment. Give agents a delegated `TI_VAULT_TOKEN` instead of the owner token when they need only selected secret fields.

## Cleanup

Stop writers and unmount. A graceful FUSE unmount automatically flushes and drains pending work:

```bash
ti fs unmount-file-system --mount-path "$HOME/workspace"
```

For a FUSE mount, use `ti fs drain-file-system --mount-path "$HOME/workspace"` separately when you need to verify remote durability while keeping the mount online. `drain-file-system` is not supported for WebDAV. For more information, see [Finish safely](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely). Back on the trusted machine:

```bash
ti fs delete-file-system \
  --file-system-id "$FILE_SYSTEM_ID"
```

## Security and operational notes

- Treat `TI_FS_TOKEN` as an owner credential.
- Do not place it in an image, repository, command flag, or operation log.
- Deleting the sandbox does not delete the remote file system.
- Graceful unmount drains pending FUSE writes; deleting the sandbox without unmounting does not.

## What's next

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
- [TiDB Cloud CLI Configuration and Credentials](/ai/ti/reference/ti-configuration-and-credentials.md)
