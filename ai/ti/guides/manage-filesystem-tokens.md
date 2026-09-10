---
title: Manage TiDB Cloud Filesystem Tokens
summary: Learn how to import, generate, scope, inspect, disable, refresh, and revoke access tokens for a TiDB Cloud Filesystem.
---

# Manage TiDB Cloud Filesystem Tokens

You can use Filesystem tokens to give users or automation access to a TiDB Cloud Filesystem without sharing TiDB Cloud API credentials.

## Prerequisites

- [Install and configure TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md).
- Obtain the Filesystem ID and an owner token when the operation requires one.

Treat token plaintext as a secret. Token creation and rotation commands return plaintext only when the token is issued.

## Import an existing token

Validate and store an existing token under the Filesystem ID embedded in it:

```shell
ti fs import-file-system-token --from-file ./fs-token --region aws-us-east-1
```

## Generate a token

Generate another owner token by using TiDB Cloud API credentials, and save its one-time plaintext response securely:

```shell
umask 077
ti fs generate-file-system-token \
  --file-system-id "<file-system-id>" \
  --token-name ci \
  --ttl 24h > ./ci-token.json
```

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

Use [`disable-file-system-token`](/ai/ti/reference/commands/fs/ti-fs-disable-file-system-token.md) to suspend a token temporarily and [`enable-file-system-token`](/ai/ti/reference/commands/fs/ti-fs-enable-file-system-token.md) to restore it.

## Rotate or revoke a token

Use [`refresh-file-system-token`](/ai/ti/reference/commands/fs/ti-fs-refresh-file-system-token.md) to rotate a token. Refresh is non-idempotent: if a request might have succeeded but its response was lost, do not retry with the old token. Generate another owner token with TiDB Cloud credentials instead.

Use [`delete-file-system-token`](/ai/ti/reference/commands/fs/ti-fs-delete-file-system-token.md) to revoke a token permanently. Before rotating, disabling, or deleting a token used by a known local mount, drain and unmount that Filesystem.

## What's next

- [Share a TiDB Cloud Filesystem Across Machines](/ai/ti/reference/ti-share-filesystem-across-machines-example.md)
- [Use TiDB Cloud Filesystem in an Agent Sandbox](/ai/ti/reference/ti-agent-sandbox-example.md)
- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
