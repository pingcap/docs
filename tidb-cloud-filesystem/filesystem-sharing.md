---
title: Share a File System Across Machines
summary: Learn how to share files across machines with a separate scoped token for each recipient, verify permissions, and revoke access independently.
aliases: ['/ai/ti-share-filesystem-across-machines-example']
---

# Share a File System Across Machines

In TiDB Cloud Filesystem, you can share files with another user, machine, CI job, or agent without copying them between environments. Give each recipient a separate scoped token to limit access by path and operation, and revoke one recipient's access without affecting others.

This guide shows you how to grant read-only access to a directory for 24 hours, verify the recipient's permissions, and then revoke the token.

> **Note:**
>
> TiDB Cloud Filesystem is currently in public preview. Its features and interfaces are subject to change without notice.

## Prerequisites

Before you begin:

- Have an owner token for an existing file system and know its region.
- [Install TiDB Cloud CLI (`ti`)](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli) in both the owner and recipient environments.
- Have a secure channel, such as a secret manager, for transferring the scoped token.

Use Bash or Zsh. Keep two separate shells open throughout the tutorial: an **owner shell** on a trusted machine for creating and revoking the token, and a **recipient shell** for testing access. The recipient does not need your owner token or TiDB Cloud API keys.

For CI or agents, inject the appropriate token into each environment's `TI_FS_TOKEN` instead of running the input prompts. Set the region and clear `TI_FS_FILE_SYSTEM_ID` as shown. Preserve `share_path` in both environments and `reviewer_token_id` in the owner environment through cleanup.

In the owner shell, set the region and load the owner token at the prompt. Input is hidden:

```bash
unset TI_FS_FILE_SYSTEM_ID
export TI_REGION_CODE="<filesystem-region-code>"
printf 'Owner token: '
read -rs TI_FS_TOKEN && export TI_FS_TOKEN && printf '\n'
```

Keep the owner token in `TI_FS_TOKEN` until you finish revoking access. It authenticates both file operations and token management. For other authentication methods, see [Manage File System Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md#inspect-and-change-token-status).

## Give access to specific files

In the owner shell:

1. Create a unique directory and upload the sample file:

    ```bash
    share_path="/sharing-example-$(date +%s)-$$"
    ti fs create-directory --path "$share_path"
    printf 'Shared review sample\n' | ti fs copy-file \
      --from-stdin --to-remote "$share_path/summary.txt"
    ti fs read-file --path "$share_path/summary.txt"
    ```

    Expected output from `read-file`: `Shared review sample`. Resolve any error before continuing.

2. Create a token that permits only reading and listing this directory:

    ```bash
    ti fs generate-file-system-scoped-token \
      --subject reviewer \
      --ttl 24h \
      --allow "$share_path:read,list"
    ```

    Save the returned `fs_token` securely; it is shown only when issued. Save the returned `token_id` for revocation:

    ```bash
    reviewer_token_id="<returned-token-id>"
    ```

3. Send the scoped token, region code, and exact value of `share_path` to the recipient through your secure channel. Keep the owner token private.

Create a separate scoped token for each recipient so you can revoke access independently. For other permission combinations, see [Manage File System Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md).

## Access the shared files from another machine

In the recipient shell:

1. Set the region and shared path, and load the scoped token at the prompt:

    ```bash
    unset TI_FS_FILE_SYSTEM_ID
    export TI_REGION_CODE="<filesystem-region-code>"
    share_path="<shared-directory-path>"
    printf 'Scoped token: '
    read -rs TI_FS_TOKEN && export TI_FS_TOKEN && printf '\n'
    ```

    Use the region and exact directory path provided by the owner. The token identifies the file system; no file system ID or CLI profile needs to be copied.

2. List the directory and read the file:

    ```bash
    ti fs list-files --path "$share_path"
    ti fs read-file --path "$share_path/summary.txt"
    ```

    Expected output from `read-file`: `Shared review sample`.

3. Check that writing and access outside the directory are denied:

    ```bash
    printf 'This write must be rejected\n' | ti fs copy-file \
      --from-stdin --to-remote "$share_path/denied-write.txt"
    ti fs list-files --path /
    ```

    Expect an authorization error from each command. Other errors do not verify the permissions. If either operation succeeds, revoke the token before continuing.

In the owner shell, confirm that `ti fs describe-file --path "$share_path/denied-write.txt"` reports that the file does not exist.

### Mount the shared directory (optional)

The command below uses Linux FUSE or macOS with macFUSE. On a Mac without macFUSE, use `--driver webdav` and omit `--read-only` from this command: WebDAV rejects that option. The scoped token still enforces read-only access at the service. See [mount prerequisites](/tidb-cloud-filesystem/filesystem-mount.md#choose-a-mount-method).

In the recipient shell, mount the shared directory:

```bash
review_mount="$(mktemp -d "$HOME/ti-fs-review.XXXXXX")"
ti fs mount-file-system \
  --remote-path "$share_path" \
  --mount-path "$review_mount" \
  --driver fuse \
  --read-only
```

Read the sample file:

```bash
cat "$review_mount/summary.txt"
```

Expected output: `Shared review sample`. If the read takes longer than 30 seconds, interrupt it and follow [mount troubleshooting](/tidb-cloud-filesystem/filesystem-troubleshooting.md#mount-succeeds-but-file-access-hangs).

The scoped token enforces read-only access at the service. The FUSE `--read-only` option also blocks writes through this local mount.

## Stop sharing access

Complete these steps in order:

1. **Recipient:** stop applications using the shared files. If you mounted the directory, unmount it:

    ```bash
    ti fs unmount-file-system --mount-path "$review_mount"
    ```

    Keep the scoped token set for the verification in step 3.

2. **Owner:** in the original owner shell, revoke the token using the ID saved at creation:

    ```bash
    ti fs delete-file-system-token --token-id "$reviewer_token_id"
    ```

    This command uses the owner token in `TI_FS_TOKEN`. To inspect token metadata, use `ti fs list-file-system-tokens --output text`.

3. **Recipient:** allow approximately 10 seconds for authentication caches to update, then repeat the read with the same scoped token:

    ```bash
    ti fs read-file --path "$share_path/summary.txt"
    ```

    Expect an authentication or authorization error. If the read still succeeds, verify the revoked token ID and retry after the cache interval. A network error does not confirm revocation.

    After confirming revocation, clear the token:

    ```bash
    unset TI_FS_TOKEN TI_REGION_CODE
    ```

    If you mounted the example, remove its empty local directory with `rmdir "$review_mount"`.

4. **Owner:** delete the sample directory and confirm it is gone:

    ```bash
    ti fs delete-file --path "${share_path:?Set the example directory first}" --recursive
    ti fs describe-file --path "$share_path"
    ```

    Expect a not-found error from `describe-file`.

Revocation leaves the file system and other tokens intact. It cannot erase files the recipient has already downloaded or cached. Clearing an environment variable alone does not revoke a token.

## Make sure updates are ready to share

For later workflows that write through a mount, close the files and [finish the writes safely](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely) before handing them to another user. For FUSE, drain the mount or unmount it successfully. For WebDAV, unmount normally; drain is not supported. Verify the updated file with a direct `ti fs read-file` request.

Avoid concurrent writes to the same file: changes are not automatically merged. Use [Layers and Checkpoints](/tidb-cloud-filesystem/filesystem-layers-checkpoints.md) when users need isolated workspaces.

## What's next

- [Manage File System Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md) to create, rotate, disable, or revoke tokens.
- [TiDB Cloud Filesystem Layers and Checkpoints](/tidb-cloud-filesystem/filesystem-layers-checkpoints.md) to make changes independently before applying them to the base file system.
- [Automation and AI Agent Workflows](/tidb-cloud-filesystem/use-filesystem-for-automation-and-ai-agents.md) for workflows that use shared file system data.
