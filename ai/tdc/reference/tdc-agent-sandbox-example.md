---
title: Use TiDB Cloud Filesystem in an Agent Sandbox
summary: Provision a Filesystem on a trusted machine and give a clean agent sandbox config-free access without TiDB Cloud API keys.
---

# Use TiDB Cloud Filesystem in an Agent Sandbox

This example gives an ephemeral coding agent a durable workspace without copying a user's complete TiDB Cloud CLI configuration into the sandbox.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `tdc` — is currently in preview. Its features and command-line interface might change without prior notice.

## The agent problem

Coding agents often start in clean, short-lived sandboxes. The local disk disappears when the sandbox is replaced, but the agent still needs previous artifacts, repository state, and files produced by other workers. Rebuilding that state wastes task time, while copying `~/.tdc/` or injecting TiDB Cloud API keys gives the sandbox control-plane credentials it does not need.

## Limitations of local storage and full cloud credentials

A sandbox-local directory is fast but not durable or shared. Generic object-storage APIs require application-specific download and upload logic instead of ordinary file operations. Giving every sandbox the user's complete cloud credentials solves access at the cost of a broader security boundary.

## How TiDB Cloud CLI changes the workflow

A trusted machine provisions the Filesystem once. The sandbox receives only the Filesystem owner token and region code, and can immediately use data-plane, mount, Git, journal, and vault workflows without `tdc configure`. The token identifies the Filesystem. When an agent needs only selected secrets, use a delegated vault token instead of the owner token.

## Prerequisites

- Install and configure the TiDB Cloud CLI on a trusted machine.
- Install the TiDB Cloud CLI in the sandbox. The release installer includes `tdc-drive9`.
- Use a secure secret manager or encrypted sandbox input for token transfer.

## Step 1. Provision on the trusted machine

```bash
umask 077
tdc fs create-file-system --wait > ./filesystem.json
export FILE_SYSTEM_ID="$(jq -r '.file_system_id' ./filesystem.json)"
export TDC_FS_TOKEN="$(jq -r '.fs_token' ./filesystem.json)"
```

Store the token in a secret manager, record `FILE_SYSTEM_ID` for control-plane cleanup, and record the canonical region code used by the profile, for example `aws-us-east-1`. Delete `filesystem.json` after storing the token securely.

## Step 2. Inject the minimum sandbox environment

Configure the sandbox secret/environment mechanism with:

```bash
TDC_FS_TOKEN=<owner-token>
TDC_REGION_CODE=aws-us-east-1
```

The sandbox does not need `TDC_PUBLIC_KEY`, `TDC_PRIVATE_KEY`, `tdc configure`, or files copied from `~/.tdc/`.

## Step 3. Verify direct access

In the sandbox:

```bash
printf 'sandbox ready\n' | tdc fs copy-file \
  --from-stdin \
  --to-remote /sandbox/status.txt

tdc fs read-file --path /sandbox/status.txt
```

Expected output:

```text
sandbox ready
```

## Step 4. Optionally mount the Filesystem

On Linux with FUSE:

```bash
mkdir -p "$HOME/workspace"
tdc fs mount-file-system \
  --mount-path "$HOME/workspace" \
  --driver fuse

cat "$HOME/workspace/sandbox/status.txt"
```

Using a path under `$HOME` also avoids the default `fusermount3` AppArmor mount-path restriction on Ubuntu 26.04. On macOS, omit `--driver fuse` to use the default WebDAV path. Use FUSE only after installing macFUSE.

After mounting, you can use `tdc fs-git`, `tdc fs-journal`, and owner-authorized `tdc fs-vault` commands with the same FS environment. Give agents a delegated `TDC_VAULT_TOKEN` instead of the owner token when they need only selected secret fields.

## Cleanup

Stop writers and unmount. A graceful FUSE unmount automatically flushes and drains pending work:

```bash
tdc fs unmount-file-system --mount-path "$HOME/workspace"
```

Use `tdc fs drain-file-system --mount-path "$HOME/workspace"` separately when you need to verify remote durability while keeping the mount online. Back on the trusted machine:

```bash
tdc fs delete-file-system \
  --file-system-id "$FILE_SYSTEM_ID"
```

## Security notes

- Treat `TDC_FS_TOKEN` as an owner credential.
- Do not place it in an image, repository, command flag, or operation log.
- Deleting the sandbox does not delete the remote Filesystem.
- Graceful unmount drains pending FUSE writes; deleting the sandbox without unmounting does not.

## What's next

- [TiDB Cloud Filesystem CLI Command Reference](/ai/tdc/reference/tdc-filesystem.md)
- [TiDB Cloud CLI Configuration and Credentials](/ai/tdc/reference/tdc-configuration-and-credentials.md)
