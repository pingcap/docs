---
title: Manage TiDB Cloud Filesystem Tokens
summary: Learn how to import, generate, scope, inspect, disable, refresh, and revoke access tokens for a TiDB Cloud Filesystem.
---

# Manage TiDB Cloud Filesystem Tokens

You can use Filesystem tokens to give users or automation access to a TiDB Cloud Filesystem without sharing TiDB Cloud API credentials.

## Prerequisites

- [Install and configure TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md).
- For owner-token generation and TiDB Cloud-authenticated token management, configure TiDB Cloud API credentials and obtain the Filesystem ID.
- For scoped-token generation or bearer-authenticated token management, obtain an owner FS token. You can pass it through `--fs-token`, set `TI_FS_TOKEN`, or use the local token stored for an explicitly selected Filesystem.

> **Note:**
>
> To avoid security risks, treat token plaintext as a secret. Token creation and rotation commands return plaintext only once when the token is issued. You cannot retrieve the plaintext later.

## Import an existing token

When you run `import-file-system-token`, the CLI validates the token format, extracts the Filesystem ID embedded in it, verifies connectivity by making a remote stat request, and stores the token in the local credential directory:

```shell
ti fs import-file-system-token --from-file ./fs-token --region aws-us-east-1
```

## Generate a token

Generate another owner token by using TiDB Cloud API credentials. The CLI does not store the generated token locally by default, so you must capture its one-time plaintext response securely:

```shell
umask 077
ti fs generate-file-system-token \
  --file-system-id "<file-system-id>" \
  --token-name ci \
  --ttl 24h > ./ci-token.json
```

To have the CLI store the generated token locally, add `--store-locally`. Use `--replace` if a different token is already stored for this Filesystem.

For least-privilege access, generate a path-and-operation-limited token from an owner token:

```shell
ti fs generate-file-system-scoped-token \
  --file-system-id "<file-system-id>" \
  --ttl 24h \
  --allow /workspace:read,list > ./scoped-token.json
```

## Inspect and change token status

List non-secret token metadata:

```shell
ti fs list-file-system-tokens --file-system-id "<file-system-id>"
```

Use [`disable-file-system-token`](/ai/ti/reference/ti-fs-disable-file-system-token.md) to suspend a token temporarily and [`enable-file-system-token`](/ai/ti/reference/ti-fs-enable-file-system-token.md) to restore it.

## Rotate or revoke a token

Use [`refresh-file-system-token`](/ai/ti/reference/ti-fs-refresh-file-system-token.md) to rotate a token. When you refresh the locally stored token, the CLI automatically updates the local credential file. When you refresh a token provided through `--fs-token` or `TI_FS_TOKEN`, the CLI returns the new token in the command output without storing it.

> **Note:**
>
> Refresh is non-idempotent. If a request might have succeeded but its response was lost, do not retry with the old token. Instead, generate a new owner token using TiDB Cloud credentials.

Use [`delete-file-system-token`](/ai/ti/reference/ti-fs-delete-file-system-token.md) to revoke a token permanently. If the deleted token matches the locally stored token, the CLI automatically removes the local credential.

> **Note:**
>
> Before you rotate, disable, or delete a token used by an active local mount, run [`drain-file-system`](/ai/ti/guides/mount-filesystem.md#drain-or-unmount) and then [`unmount-file-system`](/ai/ti/guides/mount-filesystem.md#drain-or-unmount). The CLI checks for known active mounts and refuses the operation if the token is still in use.

## What's next

- [Share a TiDB Cloud Filesystem Across Machines](/ai/ti/guides/ti-share-filesystem-across-machines-example.md)
- [Use TiDB Cloud Filesystem in an Agent Sandbox](/ai/ti/guides/ti-agent-sandbox-example.md)
- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
