---
title: Manage File System Tokens
summary: Learn how to import, create, scope, inspect, rotate, and revoke file system tokens to control access for users and automation.
aliases: ['/ai/manage-filesystem-tokens']
---

# Manage File System Tokens

In TiDB Cloud Filesystem, you can use file system tokens to give users, applications, and automation access to a file system without sharing your TiDB Cloud API credentials.

An [owner token](/tidb-cloud-filesystem/filesystem-authorization.md#owner-tokens) grants full access to a file system. A [scoped token](/tidb-cloud-filesystem/filesystem-authorization.md#scoped-tokens) limits access to specific paths and operations. For details, see [Authorization](/tidb-cloud-filesystem/filesystem-authorization.md).

## Prerequisites

Before you begin:

- [Install TiDB Cloud CLI](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli).
- Have access to an existing file system in TiDB Cloud Filesystem. If you do not have one, follow [Get Started with TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-quick-start.md) to create one.

Listing, enabling, disabling, and deleting tokens require either an owner token supplied through `TI_FS_TOKEN` or `--fs-token`, or TiDB Cloud API credentials with an explicit `--file-system-id`. These operations do not use a locally stored token automatically. Scoped-token generation can use a locally stored owner token. Each section below explains any additional requirements.

> **Note:**
>
> Store file system tokens securely. Commands that create or refresh a token return its value only once; you cannot retrieve it later.

## Import an existing token

If you already have a file system token, import it to the local CLI credential store:

```shell
ti fs import-file-system-token --from-file ./fs-token --region aws-us-east-1
```

The CLI validates the token, extracts the file system ID from it, verifies connectivity, and stores the token locally.

## Generate an owner token

Creating a file system returns an owner token. Generate an additional owner token when another trusted environment needs full access.

To generate an additional owner token, configure TiDB Cloud API credentials and obtain the file system ID.

Generate the token and save its one-time plaintext response securely:

```shell
umask 077
ti fs generate-file-system-token \
  --file-system-id "<file-system-id>" \
  --token-name ci \
  --ttl 24h > ./ci-token.json
```

The CLI does not store the generated token locally by default. To store it locally, add `--store-locally` to the preceding command. If a different token is already stored for this file system, also add `--replace`.

## Generate and delegate a scoped token

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

## Inspect and change token status

For an owner-token-only environment, set `TI_FS_TOKEN` to the owner token and `TI_REGION_CODE` to the file system's region before running the commands below. Keep management credentials separate from the scoped token you give to the recipient. A scoped token cannot manage other tokens.

List non-secret metadata for file system tokens:

```shell
ti fs list-file-system-tokens \
  --file-system-id "<file-system-id>" \
  --output text
```

The output does not include token plaintext. If you lose an owner token, generate a replacement using TiDB Cloud API credentials. You cannot recover the original token by listing tokens.

Use [`disable-file-system-token`](/ai/ti/reference/ti-fs-disable-file-system-token.md) to temporarily suspend a token, and [`enable-file-system-token`](/ai/ti/reference/ti-fs-enable-file-system-token.md) to restore it.

With owner token authentication, these two commands can change only scoped tokens. To enable or disable an owner token, use TiDB Cloud API credentials, specify `--file-system-id`, and unset `TI_FS_TOKEN` so it does not override the API credentials. Do not supply `--fs-token` for that request. Allow approximately 10 seconds for the change to take effect before verifying access.

## Rotate or revoke a token

Use [`refresh-file-system-token`](/ai/ti/reference/ti-fs-refresh-file-system-token.md) to rotate a file system token.

When you refresh a locally stored token, the CLI automatically updates the local credential. When you refresh a token provided through `--fs-token` or `TI_FS_TOKEN`, the CLI returns the new token in the command output without storing it locally.

> **Note:**
>
> If a refresh request times out, the service might have rotated the token without returning the new value to you. Do not retry with the old token. Generate a new owner token using TiDB Cloud API credentials.

> **Warning:**
>
> Before rotating, disabling, or deleting a token used by an active mount, stop applications that are writing to the mount and successfully unmount it. The CLI can detect known local mounts but cannot discover mounts on other machines. Coordinate with those machines before changing the token. For more information, see [Finish safely](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely).

Before retiring a token, distribute and validate its replacement. Then revoke the old token by its token ID:

```shell
ti fs delete-file-system-token \
  --file-system-id "<file-system-id>" \
  --token-id "<token-id>"
```

If the deleted token matches the locally stored token, the CLI automatically removes the local credential. Token changes can take time to propagate through authorization caches.

Disabling or revoking an owner token does not automatically revoke scoped tokens generated from it. Review and revoke those scoped tokens separately when necessary.

## What's next

- [Share a File System](/tidb-cloud-filesystem/filesystem-sharing.md)
- [Explore automation and AI agent workflows](/tidb-cloud-filesystem/use-filesystem-for-automation-and-ai-agents.md)
- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
