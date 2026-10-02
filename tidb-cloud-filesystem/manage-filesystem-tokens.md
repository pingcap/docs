---
title: Manage File System Tokens
summary: Learn how to import, create, scope, inspect, rotate, and revoke file system tokens to control access for users and automation.
aliases: ['/ai/manage-filesystem-tokens']
---

# Manage File System Tokens

In TiDB Cloud Filesystem, you can use file system tokens to give users, applications, and automation access to a file system without sharing your TiDB Cloud API credentials.

- An [owner token](/tidb-cloud-filesystem/filesystem-authorization.md#owner-tokens) grants full access to a file system.
- A [scoped token](/tidb-cloud-filesystem/filesystem-authorization.md#scoped-tokens) limits access to specific paths and operations.

## Prerequisites

Before you begin:

- Have access to an existing file system in TiDB Cloud Filesystem. If you do not have one, follow [Quick Start via Console](/tidb-cloud-filesystem/filesystem-quick-start-console.md) or [Quick Start via CLI](/tidb-cloud-filesystem/filesystem-quick-start.md) to create one.
- For CLI operations, [install TiDB Cloud CLI](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli).

To list, enable, disable, or delete tokens with the CLI, provide an owner token through `TI_FS_TOKEN` or `--fs-token`, or use TiDB Cloud API credentials with an explicit `--file-system-id`. These operations do not automatically use a locally stored token. Scoped-token generation can use a locally stored owner token. Each section below explains any additional requirements.

> **Note:**
>
> Store file system tokens securely. When you create or refresh a token, its plaintext is returned only once and cannot be retrieved later.

## Import an existing token

If you already have a file system token, including the default owner token shown when you create a file system in the TiDB Cloud console, save its plaintext to a secure file and import it to the local CLI credential store:

```shell
ti fs import-file-system-token --from-file ./fs-token --region "<file-system-region>"
```

The CLI validates the token, extracts the file system ID from it, verifies connectivity, and stores the token locally. If the token is still available through `TI_FS_TOKEN`, you can use it for CLI commands without importing it.

## Generate an owner token

<SimpleTab>

<div label="Console">

The TiDB Cloud console creates a default owner token when you create a file system. Its plaintext appears only in the **Your File System is Ready!** dialog.

For an additional owner token, use the **CLI** tab.

</div>

<div label="CLI">

When you create a file system with the CLI, it returns a non-expiring owner token, stores it locally, and uses it for later commands.

Generate an additional owner token when another trusted environment needs full access.

To generate an additional owner token, configure TiDB Cloud API credentials and obtain the file system ID.

Generate the token and save its one-time plaintext response securely:

```shell
umask 077
ti fs generate-file-system-token \
  --file-system-id "<file-system-id>" \
  --token-name ci \
  --ttl 24h \
  --query fs_token \
  --output text > ./ci-token
```

`--query fs_token --output text` writes the token value on its own, which is the format that `import-file-system-token --from-file` expects. Without those options the command writes its full JSON response, and importing that file fails with `invalid FS token format`. The token ID that you need in order to revoke the token later is available at any time from `ti fs list-file-system-tokens`.

The CLI does not store the generated token locally by default. To store it locally, add `--store-locally` to the preceding command. If a different token is already stored for this file system, also add `--replace`.

</div>

</SimpleTab>

## Generate and delegate a scoped token

<SimpleTab>

<div label="Console">

If you want to restrict a token to a specific directory, create that directory before generating the token.

1. In the TiDB Cloud console, navigate to the [**File Systems**](https://tidbcloud.com/filesystems) page, select the cloud provider and region, and then click the name of your target file system.
2. On the overview page of the file system, click **Access Tokens** in the left navigation pane.
3. In the upper-right corner, click **Create Token**.
4. Configure the token by providing the following information:

    - **Token name**: enter a name for the token.
    - **Access path (optional)**: specify an access path to limit the token's access to a specific directory. If you leave the path empty, the token applies to `/`.
    - **Expiration**: choose when the token expires. The default is one hour.
    - **Permission**: select only the operations the token needs. For details, see [Authorization](/tidb-cloud-filesystem/filesystem-authorization.md#scoped-tokens).

5. Click **Create**.
6. In the displayed dialog, copy the token and store it securely before clicking **Done**. Its plaintext is shown only once.

Provide the token and file system region to the receiving environment. When mounting with a token restricted to a directory, set the CLI `--remote-path` option to that directory.

</div>

<div label="CLI">

On a trusted machine, use an owner token to generate a scoped token. Supply the owner token through `--fs-token` or `TI_FS_TOKEN`, or use the owner token stored locally for the selected file system.

Before using this example, create the remote `/workspace` directory if it does not exist. Use the locally stored owner token to grant an agent permission to read, list, and write files in that directory:

```shell
SCOPED_TOKEN="$(ti fs generate-file-system-scoped-token \
  --file-system-id "<file-system-id>" \
  --subject report-agent \
  --ttl 24h \
  --allow /workspace:read,list,write \
  --query fs_token --output text)"
```

Transfer the token through a secret manager. In the receiving environment, provide the scoped token and the file system region:

```shell
export TI_FS_TOKEN="<scoped-token>"
export TI_REGION_CODE="<filesystem-region-code>"

ti fs list-files --path /workspace
```

The `--allow` value uses the format `<path>:<comma-separated-operations>`. Supported operations are `read`, `list`, `search`, `write`, and `delete`; `search` requires `read`. In this example, the token permits `read`, `list`, and `write` operations under `/workspace`.

To mount the directory with this token, specify `--remote-path /workspace`. A token restricted to `/workspace` cannot mount the file system root `/`.

For more information about scoped permissions and credential selection, see [Authorization](/tidb-cloud-filesystem/filesystem-authorization.md).

</div>

</SimpleTab>

## Inspect and change token status

> **Warning:**
>
> Before deactivating, rotating, or deleting a token used by an active mount, stop applications that are writing to the mount and successfully unmount it. The CLI can detect known local mounts but cannot discover mounts on other machines. Coordinate with those machines before changing the token. For more information, see [Finish safely](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely).

<SimpleTab>

<div label="Console">

1. In the TiDB Cloud console, navigate to the [**File Systems**](https://tidbcloud.com/filesystems) page, select the cloud provider and region, and then click the name of your target file system.
2. On the overview page of the file system, click **Access Tokens** in the left navigation pane.
3. On the **Access Tokens** page, you can view each token's ID, status, access path, permissions, expiration, and creation time.
4. To suspend a token, click **...** in the row of the target token, and then select **Deactivate**. To restore a deactivated token, click **...**, and then select **Activate**.

</div>

<div label="CLI">

For an owner-token-only environment, set `TI_FS_TOKEN` to the owner token and `TI_REGION_CODE` to the file system's region before running the commands below. Keep management credentials separate from the scoped token you give to the recipient. A scoped token cannot manage other tokens.

List non-secret metadata for file system tokens:

```shell
ti fs list-file-system-tokens \
  --file-system-id "<file-system-id>" \
  --output text
```

The output does not include token plaintext. If you lose an owner token, generate a replacement using TiDB Cloud API credentials. You cannot recover the original token by listing tokens.

Use [`disable-file-system-token`](/ai/ti/reference/ti-fs-disable-file-system-token.md) to temporarily suspend a token, and [`enable-file-system-token`](/ai/ti/reference/ti-fs-enable-file-system-token.md) to restore it. These correspond to **Deactivate** and **Activate** in the console.

With owner token authentication, these two commands can change only scoped tokens. To enable or disable an owner token, use TiDB Cloud API credentials, specify `--file-system-id`, and unset `TI_FS_TOKEN` so it does not override the API credentials. Do not supply `--fs-token` for that request. Allow approximately 10 seconds for the change to take effect before verifying access.

</div>

</SimpleTab>

## Rotate or revoke a token

To rotate or revoke a token, it is recommended to use the CLI commands. The TiDB Cloud console does not offer the `refresh-file-system-token` operation of the CLI.

<SimpleTab>

<div label="Console">

To replace a scoped token in the TiDB Cloud console, [create a new token](#generate-and-delegate-a-scoped-token) with the required path, permissions, and expiration. Distribute and validate the new token before retiring the old one. Then, go to the **Access Tokens** page of the target file system, locate the row of the old token, click **...**, and then select **Delete**.

To replace an owner token, [generate another owner token with the CLI](#generate-an-owner-token) before deleting the old one in the TiDB Cloud console.

</div>

<div label="CLI">

Use [`refresh-file-system-token`](/ai/ti/reference/ti-fs-refresh-file-system-token.md) to rotate a file system token.

When you refresh a locally stored token, the CLI automatically updates the local credential. When you refresh a token provided through `--fs-token` or `TI_FS_TOKEN`, the CLI returns the new token in the command output without storing it locally.

> **Note:**
>
> If a refresh request times out, the service might have rotated the token without returning the new value to you. Do not retry with the old token. Generate a new owner token using TiDB Cloud API credentials.

Before retiring a token, distribute and validate its replacement. Then revoke the old token by its token ID:

```shell
ti fs delete-file-system-token \
  --file-system-id "<file-system-id>" \
  --token-id "<token-id>"
```

If the deleted token matches the locally stored token, the CLI automatically removes the local credential. Token changes can take time to propagate through authorization caches.

Disabling or revoking an owner token does not automatically revoke scoped tokens generated from it. Review and revoke those scoped tokens separately when necessary.

</div>

</SimpleTab>

## What's next

- [Share a File System](/tidb-cloud-filesystem/filesystem-sharing.md)
- [Explore automation and AI agent workflows](/tidb-cloud-filesystem/use-filesystem-for-automation-and-ai-agents.md)
- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
