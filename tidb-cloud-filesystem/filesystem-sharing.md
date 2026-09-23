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

## Give access to specific files

To share part of a file system with another user or environment:

1. Decide which paths they need to access and what they need to do with those paths.

2. If the path you want to share does not already exist, create it. The following example creates `/reports`:

    ```bash
    ti fs create-directory \
      --file-system-id "<file-system-id>" \
      --path /reports
    ```

3. Create a scoped token for the user or environment.

    The following example gives a reviewer read-only access to `/reports` for 24 hours:

    ```bash
    REVIEW_TOKEN="$(ti fs generate-file-system-scoped-token \
      --file-system-id "<file-system-id>" \
      --subject reviewer \
      --ttl 24h \
      --allow /reports:read,list \
      --query fs_token \
      --output text)"
    ```

    This token lets the reviewer read and list files under `/reports`, but does not give access to other paths in the file system.

    If the reviewer also needs to add or update files, include `write` for that path. For example, `--allow /reports:read,list,write` lets the reviewer read, list, and write files under `/reports` without giving them owner access to the file system.

4. Send the token and the file system region code through a secure channel or secret manager.

    The other user or environment does not need your TiDB Cloud API credentials or a copy of your local `~/.ti/` directory.

    The token remains valid until it expires or you revoke it. Saving the token in an environment variable does not extend its lifetime.

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
    ```

    The token identifies the file system, so you do not need to provide the file system ID.

2. Verify that you can access the shared path:

    ```bash
    ti fs list-files --path /reports
    ti fs read-file --path /reports/summary.txt
    ```

    The token can be used only for the paths and actions included in its scope. Other access is rejected by the file system service.

For other ways to access an existing file system, see [Access an Existing File System](/tidb-cloud-filesystem/access-filesystem.md).

### Mount the shared directory (optional)

On a supported platform, you can also mount the shared directory and access its files through a local path:

```bash
mkdir -p "$HOME/reports"

ti fs mount-file-system \
  --remote-path /reports \
  --mount-path "$HOME/reports" \
  --read-only
```

The remote `/reports` directory becomes the root of the local mount. For example, `/reports/summary.txt` is available locally at:

```text
$HOME/reports/summary.txt
```

The scoped token limits what you can do in the file system. The `--read-only` option also prevents writes through this local mount.

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
    ti fs read-file --path /reports/summary.txt
    ```

For a WebDAV mount, close open files and unmount normally. WebDAV does not support drain. See [Finish safely](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely).

If multiple users or environments have write access, avoid writing to the same files at the same time. TiDB Cloud Filesystem does not automatically merge conflicting changes.

If different users or workflows need to make changes independently before applying them to the base file system, see [Layers and Checkpoints](/tidb-cloud-filesystem/filesystem-layers-checkpoints.md).

## Stop sharing access

### On the machine using the shared file system

1. Stop applications that use the shared files.

2. If the file system is mounted, unmount it:

    ```bash
    ti fs unmount-file-system --mount-path "$HOME/reports"
    ```

3. Remove the token from the local environment:

    ```bash
    unset TI_FS_TOKEN TI_REGION_CODE
    ```

Removing the token from the local environment prevents that environment from using the saved value, but does not revoke the token itself. Anyone who still has the token can continue using it until it expires or is revoked.

### On the machine where you manage the file system

1. Find the token you want to revoke:

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

Revoking one token removes that user's or environment's access without affecting other tokens or deleting the file system.

Do not delete the file system just to stop sharing it with one user or environment. Deleting the file system removes the shared file system and its data for everyone.

## What's next

- [Manage File System Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md) to create, rotate, disable, or revoke tokens.
- [TiDB Cloud Filesystem Layers and Checkpoints](/tidb-cloud-filesystem/filesystem-layers-checkpoints.md) to make changes independently before applying them to the base file system.
- [Automation and AI Agent Workflows](/tidb-cloud-filesystem/use-filesystem-for-automation-and-ai-agents.md) for workflows that use shared file system data.
