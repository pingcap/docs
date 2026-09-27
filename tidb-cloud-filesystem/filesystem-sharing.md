---
title: Share a File System Across Machines
summary: Learn how to share part of an existing file system with another user, machine, CI job, or agent, and remove that access when it is no longer needed.
aliases: ['/ai/ti-share-filesystem-across-machines-example']
---

# Share a File System Across Machines

You can share files in a file system with another user, machine, CI job, or agent without copying the files between environments.

Create a separate scoped token for each user or environment you want to share with. Each token can limit access to specific paths and actions, so you can give only the access that is needed and revoke it later without affecting anyone else.

> **Note:**
>
> TiDB Cloud Filesystem is currently in public preview. Its features and interfaces are subject to change without notice.

## Prerequisites

Before you begin:

- Have access to an existing file system in TiDB Cloud Filesystem.
- On a machine you trust, have an owner token for the file system. You need an owner token to create scoped tokens.
- [Install TiDB Cloud CLI (`ti`)](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli) on the machine or environment that needs access to the shared file system.
- Have a secure way, such as a secret manager, to transfer file system tokens.

For information about owner and scoped tokens, see [Authorization](/tidb-cloud-filesystem/filesystem-authorization.md).

On the trusted management machine, set the owner token and the file system's region for the entire workflow, including revocation:

```bash
export TI_FS_TOKEN="<owner-token>"
export TI_REGION_CODE="<filesystem-region-code>"
```

Scoped-token generation can also use a locally stored owner token. However, token listing and revocation require an explicitly supplied owner token (`TI_FS_TOKEN` or `--fs-token`) or TiDB Cloud API keys with the file system ID. Do not assume that a locally stored token alone is sufficient for those management commands.

Use a separate shell or machine for the recipient steps below. Keep the owner token in the management environment; do not replace it with the reviewer's scoped token.

## Give access to specific files

To share part of a file system with another user or environment:

1. Decide which paths they need to access and what they need to do with those paths.

2. Prepare a new example directory and the file that the recipient will read. Run these commands in Bash or Zsh:

    ```bash
    share_path="/sharing-example-$(date +%s)-$$"
    ti fs create-directory --path "$share_path"
    printf 'Shared review sample\n' | ti fs copy-file \
      --from-stdin --to-remote "$share_path/summary.txt"
    ti fs read-file --path "$share_path/summary.txt"
    ```

    The read must print `Shared review sample`. Retain `share_path` for token creation and cleanup. Stop if preparation fails.

3. Create a scoped token for the recipient. This example gives read-only access to the example directory for 24 hours:

    ```bash
    ti fs generate-file-system-scoped-token \
      --subject reviewer \
      --ttl 24h \
      --allow "$share_path:read,list"
    ```

    Securely retain both `fs_token` and the immutable `token_id` from this response. You will give the token to the recipient and use its ID for revocation. Do not identify the token only by its subject or name, which might not be unique.

    This token permits reading and listing under `share_path`, but not writing or access to other paths. If a different workflow needs writes, include `write`, for example `--allow "$share_path:read,list,write"`.

4. Send the scoped token, file system region code, and exact value of `share_path` through a secure channel or secret manager.

    The recipient does not need your owner token, TiDB Cloud API credentials, or a copy of your local `~/.ti/` directory. The token remains valid until it expires or you revoke it; saving it in an environment variable does not extend its lifetime.

> **Note:**
>
> The token value is shown only when the token is created. Treat it as a secret and do not expose it in logs, issues, chat messages, or source control.

For more information about token permissions and expiration, see [Manage File System Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md).

## Access the shared files from another machine

On the machine or environment that needs access:

1. Set the scoped token and file system region:

    ```bash
    export TI_FS_TOKEN="<reviewer-token>"
    export TI_REGION_CODE="<filesystem-region-code>"
    share_path="<shared-directory-path>"
    ```

    The token identifies the file system, so you do not need to provide the file system ID. Unset `TI_FS_FILE_SYSTEM_ID` if it selects a different file system. Set `share_path` to the exact directory provided by the owner, such as `/sharing-example-...`.

2. Verify that you can access the shared path:

    ```bash
    ti fs list-files --path "$share_path"
    ti fs read-file --path "$share_path/summary.txt"
    ```

    The read must print `Shared review sample`.

3. Verify the read-only and path boundaries:

    ```bash
    printf 'This write must be rejected\n' | ti fs copy-file \
      --from-stdin --to-remote "$share_path/denied-write.txt"
    ti fs list-files --path /
    ```

    Both commands must fail with an authorization error. A timeout, missing credential, or unsupported-region error does not verify permission isolation. On the owner machine, confirm with `ti fs describe-file --path "$share_path/denied-write.txt"` that no file was created. If either forbidden operation succeeds, stop and revoke the scoped token.

For other ways to access an existing file system, see [Access an Existing File System](/tidb-cloud-filesystem/access-filesystem.md).

### Mount the shared directory (optional)

On Linux with FUSE or macOS with macFUSE, mount the shared directory explicitly with FUSE:

```bash
review_mount="$(mktemp -d "$HOME/ti-fs-review.XXXXXX")"

ti fs mount-file-system \
  --remote-path "$share_path" \
  --mount-path "$review_mount" \
  --driver fuse \
  --read-only
```

The shared directory becomes the root of the mount. Verify its known file:

```bash
cat "$review_mount/summary.txt"
```

The read must print `Shared review sample`. If it has not returned after 30 seconds, interrupt it and follow [Mount succeeds but file access hangs](/tidb-cloud-filesystem/filesystem-troubleshooting.md#mount-succeeds-but-file-access-hangs).

The scoped token enforces permissions at the service. The `--read-only` option additionally prevents writes through this FUSE mount. WebDAV rejects `--read-only`. On a Mac without macFUSE, use the direct CLI reads above; do not reuse this mount command with `--driver webdav --read-only`.

Direct `ti fs` commands and mounts access the same files in the file system. For example, a file uploaded with `ti fs copy-file` is also available through a mount. Changes made through a mount become available to direct commands and other users after the writes reach the service.

For mount requirements and platform-specific setup, see [Mount a File System](/tidb-cloud-filesystem/filesystem-mount.md).

## Make sure updates are ready to share

When multiple users or environments access the same file system, they work with the same files rather than separate copies.

If files are written through a mount, make sure the latest changes have reached the file system before telling someone else that they are ready.

For a FUSE mount:

1. Stop applications from writing to the files and close any files that are still open.

2. Make sure pending writes reach the file system:

    - To keep the mount running, drain it.
    - If you are finished with the mount, unmount it successfully.

3. If you need to verify the handoff, read the updated file directly from the file system:

    ```bash
    ti fs read-file --path "$share_path/summary.txt"
    ```

For a WebDAV mount, close open files and unmount normally. WebDAV does not support drain. See [Finish safely](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely).

If multiple users or environments have write access, avoid writing to the same files at the same time. TiDB Cloud Filesystem does not automatically merge conflicting changes.

If different users or workflows need to make changes independently before applying them to the base file system, see [Layers and Checkpoints](/tidb-cloud-filesystem/filesystem-layers-checkpoints.md).

## Stop sharing access

### On the machine using the shared file system

1. Stop applications that use the shared files.

2. If the file system is mounted, unmount it:

    ```bash
    ti fs unmount-file-system --mount-path "$review_mount"
    ```

3. After the owner revokes the token in the next section and you verify that access is rejected, remove it from the local environment:

    ```bash
    unset TI_FS_TOKEN TI_REGION_CODE
    ```

Removing the token from the local environment prevents that environment from using the saved value, but does not revoke the token itself. Anyone who still has the token can continue using it until it expires or is revoked.

### On the machine where you manage the file system

Use the owner-token management environment from the prerequisites, with the original region and `TI_FS_TOKEN` still set to the owner token.

1. Use the `token_id` saved when you issued the scoped token. To inspect its metadata:

    ```bash
    ti fs list-file-system-tokens \
      --file-system-id "<file-system-id>" \
      --output text
    ```

2. Revoke that token:

    ```bash
    ti fs delete-file-system-token \
      --file-system-id "<file-system-id>" \
      --token-id "<reviewer-token-id>"
    ```

3. Allow approximately 10 seconds for authentication caches to converge. In the recipient environment, repeat the read with the same scoped token:

    ```bash
    ti fs read-file --path "$share_path/summary.txt"
    ```

    This must now fail with an authentication or authorization error. A network failure does not confirm revocation. If the read still succeeds, verify the token ID and retry after the convergence interval before declaring access revoked. Revocation cannot erase files that the recipient already downloaded or cached.

4. On the owner machine, after unmounting any example mounts, remove only the example directory you created:

    ```bash
    ti fs delete-file --path "${share_path:?Set the example directory first}" --recursive
    ti fs describe-file --path "$share_path/summary.txt"
    ```

    The describe command must report that the file does not exist. Remove an empty local example mount directory with `rmdir "$review_mount"` on the recipient machine after successful unmount.

Revoking one token removes that user's or environment's access without affecting other tokens or deleting the file system.

Do not delete the file system just to stop sharing it with one user or environment. Deleting the file system removes the shared file system and its data for everyone.

## What's next

- [Manage File System Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md) to create, rotate, disable, or revoke tokens.
- [TiDB Cloud Filesystem Layers and Checkpoints](/tidb-cloud-filesystem/filesystem-layers-checkpoints.md) to make changes independently before applying them to the base file system.
- [Automation and AI Agent Workflows](/tidb-cloud-filesystem/use-filesystem-for-automation-and-ai-agents.md) for workflows that use shared file system data.
