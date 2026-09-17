---
title: Manage TiDB Cloud Filesystem Tokens
summary: Learn how to import, generate, scope, inspect, disable, refresh, and revoke access tokens for a TiDB Cloud Filesystem.
aliases: ['/ai/manage-filesystem-tokens']
---

# Manage TiDB Cloud Filesystem Tokens

You can use Filesystem tokens to give users or automation access to a TiDB Cloud Filesystem without sharing TiDB Cloud API credentials.

## Prerequisites

- [Install TiDB Cloud CLI](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-the-cli).
- For owner-token generation and TiDB Cloud-authenticated token management, [configure TiDB Cloud API credentials](/tidb-cloud-filesystem/filesystem-quick-start.md#step-2-configure-access) and obtain the Filesystem ID.
- For scoped-token generation or bearer-authenticated token management, obtain an [owner FS token](/tidb-cloud-filesystem/filesystem-authorization.md#owner-fs-tokens). You can pass it through `--fs-token`, set `TI_FS_TOKEN`, or use the local token stored for an explicitly selected Filesystem.

> **Note:**
>
> To avoid security risks, treat token plaintext as a secret. Token creation and rotation commands return plaintext only once when the token is issued. You cannot retrieve the plaintext later.

## Import an existing token

When you run `import-file-system-token`, the CLI validates the token format, extracts the Filesystem ID embedded in it, verifies connectivity by making a remote stat request, and stores the token in the local credential directory:

```shell
ti fs import-file-system-token --from-file ./fs-token --region aws-us-east-1
```

## Generate an owner token

Generate another owner token by using TiDB Cloud API credentials. The CLI does not store the generated token locally by default, so you must capture its one-time plaintext response securely:

```shell
umask 077
ti fs generate-file-system-token \
  --file-system-id "<file-system-id>" \
  --token-name ci \
  --ttl 24h > ./ci-token.json
```

To have the CLI store the generated token locally, add `--store-locally`. Use `--replace` if a different token is already stored for this Filesystem.

## Generate and delegate a scoped token

On a trusted machine with an owner token, generate a path-and-operation-limited token for an agent:

```shell
SCOPED_TOKEN="$(ti fs generate-file-system-scoped-token \
  --file-system-id "<file-system-id>" \
  --subject report-agent \
  --ttl 24h \
  --allow /workspace:read,list,write \
  --query fs_token --output text)"
```

Transfer the token through a secret manager. In the agent's environment, inject the token and the Filesystem's region:

```shell
export TI_FS_TOKEN="<scoped-token>"
export TI_REGION_CODE="<filesystem-region-code>"
ti fs list-files --path /workspace
```

The `--allow` value uses `<path>:<comma-separated-operations>`. In this example, the token permits `read`, `list`, and `write` under `/workspace`.

The remote `/workspace` directory must already exist. For a mount, select the allowed subtree with `--remote-path /workspace`; a token restricted to `/workspace` cannot mount the root `/`. For the permission model and credential precedence, see [Authorization](/tidb-cloud-filesystem/filesystem-authorization.md).

## Inspect and change token status

List non-secret token metadata:

```shell
ti fs list-file-system-tokens --file-system-id "<file-system-id>" --output text
```

The list does not return token plaintext. Preserve newly generated or refreshed tokens in a secret manager. If you lose an owner token, generate a replacement using TiDB Cloud API credentials; you cannot recover the original secret by listing tokens.

Use [`disable-file-system-token`](/ai/ti/reference/ti-fs-disable-file-system-token.md) to suspend a token temporarily and [`enable-file-system-token`](/ai/ti/reference/ti-fs-enable-file-system-token.md) to restore it.

## Rotate or revoke a token

Use [`refresh-file-system-token`](/ai/ti/reference/ti-fs-refresh-file-system-token.md) to rotate a token. When you refresh the locally stored token, the CLI automatically updates the local credential file. When you refresh a token provided through `--fs-token` or `TI_FS_TOKEN`, the CLI returns the new token in the command output without storing it.

> **Note:**
>
> Refresh is non-idempotent. For example, after a network timeout, the service might have rotated the token even though you did not receive the new value. Do not retry with the old token. Instead, generate a new owner token using TiDB Cloud credentials.

> **Warning:**
>
> Before you rotate, disable, or delete a token used by an active local mount, [stop writers and unmount it safely](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely). Drain a FUSE mount before unmounting; WebDAV does not support drain. The CLI checks known local mounts but cannot discover every remote machine using the token. Stop writes and unmount consumers on those machines before changing it.

Before retiring a token, distribute and validate a replacement. Then use [`delete-file-system-token`](/ai/ti/reference/ti-fs-delete-file-system-token.md) to revoke the retired token by its token ID:

```shell
ti fs delete-file-system-token --file-system-id "<file-system-id>" --token-id "<token-id>"
```

If the deleted token matches the locally stored token, the CLI automatically removes the local credential. Token changes can take time to propagate through authorization caches. Disabling an owner token does not replace reviewing and revoking scoped tokens that it issued.

## What's next

- [Share a TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-sharing.md).
- [Explore automation and AI agent workflows](/tidb-cloud-filesystem/use-filesystem-for-automation-and-ai-agents.md).
- [TiDB Cloud Filesystem CLI Command Reference (in TiDB for AI documentation)](/ai/ti/reference/ti-filesystem.md).
