---
title: Manage TiDB Cloud Filesystem Tokens
summary: Learn how to import, generate, scope, inspect, disable, refresh, and revoke access tokens for a TiDB Cloud Filesystem.
aliases: ['/ai/manage-filesystem-tokens']
---

# Manage TiDB Cloud Filesystem Tokens

Filesystem tokens let you give users, applications, and automation access to a TiDB Cloud Filesystem without sharing your TiDB Cloud API credentials.

You can use an [owner token](/tidb-cloud-filesystem/filesystem-authorization.md#owner-tokens) for full access to a Filesystem, or create [scoped tokens](/tidb-cloud-filesystem/filesystem-authorization.md#scoped-tokens) that limit access to specific paths and operations. For more information about token types and permissions, see [Authorization](/tidb-cloud-filesystem/filesystem-authorization.md).

## Prerequisites

Before you begin:

- [Install TiDB Cloud CLI](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli).
- Have access to an existing TiDB Cloud Filesystem. If you do not have one, follow [Get Started with TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-quick-start.md) to create one.

Some token management operations require TiDB Cloud API credentials or an existing owner token. The relevant requirements are described in each section of this guide.

> **Note:**
>
> Treat Filesystem tokens as secrets. When a command creates or refreshes a token, the token plaintext is returned only once and cannot be retrieved later.

## Import an existing token

If you already have a Filesystem token, import it to the local CLI credential store:

```shell
ti fs import-file-system-token --from-file ./fs-token --region aws-us-east-1
```

The CLI validates the token, extracts the Filesystem ID from it, verifies connectivity, and stores the token locally.

## Generate an owner token

When you create a Filesystem, TiDB Cloud creates an owner token for it and returns it to you. You can generate additional owner tokens when another trusted environment or workflow needs full access to the Filesystem.

To generate an additional owner token, configure TiDB Cloud API credentials and obtain the Filesystem ID.

Generate the token and save its one-time plaintext response securely:

```shell
umask 077
ti fs generate-file-system-token \
  --file-system-id "<file-system-id>" \
  --token-name ci \
  --ttl 24h > ./ci-token.json
```

The CLI does not store the generated token locally by default. To store it locally, add `--store-locally` to the preceding command. If a different token is already stored for this Filesystem, also add `--replace`.

## Generate and delegate a scoped token

To generate a scoped token, use an existing owner token on a trusted machine. Provide the owner token through `--fs-token` or `TI_FS_TOKEN`, or use the token stored locally for the selected Filesystem.

The following example uses the locally stored owner token and creates a scoped token that allows an agent to read, list, and write files under `/workspace`:

```shell
SCOPED_TOKEN="$(ti fs generate-file-system-scoped-token \
  --file-system-id "<file-system-id>" \
  --subject report-agent \
  --ttl 24h \
  --allow /workspace:read,list,write \
  --query fs_token --output text)"
```

Transfer the token through a secret manager. In the receiving environment, provide the scoped token and the Filesystem region:

```shell
export TI_FS_TOKEN="<scoped-token>"
export TI_REGION_CODE="<filesystem-region-code>"

ti fs list-files --path /workspace
```

The `--allow` value uses the format `<path>:<comma-separated-operations>`. Supported operations are `read`, `list`, `search`, `write`, and `delete`; `search` requires `read`. In this example, the token permits `read`, `list`, and `write` operations under `/workspace`.

The remote `/workspace` directory must already exist. To use this token for a mount, specify `--remote-path /workspace`. A token restricted to `/workspace` cannot mount the Filesystem root `/`.

For more information about scoped permissions and credential selection, see [Authorization](/tidb-cloud-filesystem/filesystem-authorization.md).

## Inspect and change token status

List non-secret metadata for Filesystem tokens:

```shell
ti fs list-file-system-tokens \
  --file-system-id "<file-system-id>" \
  --output text
```

The output does not include token plaintext. If you lose an owner token, generate a replacement using TiDB Cloud API credentials. You cannot recover the original token by listing tokens.

Use [`disable-file-system-token`](/ai/ti/reference/ti-fs-disable-file-system-token.md) to temporarily suspend a token, and [`enable-file-system-token`](/ai/ti/reference/ti-fs-enable-file-system-token.md) to restore it.

## Rotate or revoke a token

Use [`refresh-file-system-token`](/ai/ti/reference/ti-fs-refresh-file-system-token.md) to rotate a Filesystem token.

When you refresh a locally stored token, the CLI automatically updates the local credential. When you refresh a token provided through `--fs-token` or `TI_FS_TOKEN`, the CLI returns the new token in the command output without storing it locally.

> **Note:**
>
> Refresh is non-idempotent. For example, after a network timeout, the service might have rotated the token even though you did not receive the new value. Do not retry the refresh with the old token. Instead, generate a new owner token using TiDB Cloud API credentials.

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

- [Share a TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-sharing.md)
- [Explore automation and AI agent workflows](/tidb-cloud-filesystem/use-filesystem-for-automation-and-ai-agents.md)
- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
