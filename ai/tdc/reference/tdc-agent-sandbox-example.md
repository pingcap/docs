---
title: Use TiDB Cloud Filesystem in an Agent Sandbox
summary: Provision a Filesystem on a trusted machine and give a clean agent sandbox config-free access without TiDB Cloud API keys.
---

# Use TiDB Cloud Filesystem in an Agent Sandbox

This example gives an ephemeral coding agent a durable workspace without copying a user's complete tdc configuration into the sandbox.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## The agent problem

Coding agents often start in clean, short-lived sandboxes. The local disk disappears when the sandbox is replaced, but the agent still needs previous artifacts, repository state, and files produced by other workers. Rebuilding that state wastes task time, while copying `~/.tdc/` or injecting TiDB Cloud API keys gives the sandbox control-plane credentials it does not need.

## Why local storage and full cloud credentials are not enough

A sandbox-local directory is fast but not durable or shared. Generic object-storage APIs require application-specific download and upload logic instead of ordinary file operations. Giving every sandbox the user's complete cloud credentials solves access at the cost of a much broader security boundary.

## How tdc changes the workflow

A trusted machine provisions the Filesystem once. The sandbox receives only the Filesystem owner token, region code, and Filesystem name, and can immediately use data-plane, mount, Git, journal, and vault workflows without `tdc configure`. When an agent needs only selected secrets, use a delegated vault token instead of the owner token.

## Prerequisites

- Install and configure tdc on a trusted machine.
- Install tdc in the sandbox. The release installer includes `tdc-drive9`.
- Use a secure secret manager or encrypted sandbox input for token transfer.

## Step 1. Provision on the trusted machine

```bash
export TDC_FS_TOKEN="$(tdc fs create-file-system \
  --file-system-name agent-sandbox \
  --wait \
  --query fs_token \
  --output text)"
```

Record the canonical region code used by the profile, for example `aws-us-east-1`. Do not print the token.

## Step 2. Inject the minimum sandbox environment

Configure the sandbox secret/environment mechanism with:

```bash
TDC_FS_TOKEN=<owner-token>
TDC_REGION_CODE=aws-us-east-1
TDC_FS_FILE_SYSTEM_NAME=agent-sandbox
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
  --file-system-name agent-sandbox \
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
  --file-system-name agent-sandbox
```

## Security notes

- Treat `TDC_FS_TOKEN` as an owner credential.
- Do not place it in an image, repository, command flag, or operation log.
- Deleting the sandbox does not delete the remote Filesystem.
- Graceful unmount drains pending FUSE writes; deleting the sandbox without unmounting does not.

## What's next

- [tdc fs Command Reference](/ai/tdc/reference/tdc-filesystem.md)
- [tdc Configuration and Credentials](/ai/tdc/reference/tdc-configuration-and-credentials.md)
