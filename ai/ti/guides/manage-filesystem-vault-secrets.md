---
title: Manage TiDB Cloud Filesystem Vault Secrets
summary: Learn how to store, read, delegate, inject, audit, revoke, and mount secrets securely with TiDB Cloud Filesystem Vault.
---

# Manage TiDB Cloud Filesystem Vault Secrets

Use `ti fs-vault` to manage secrets and give users or agents narrowly scoped, time-limited access.

## Prerequisites

Select a Filesystem through a profile or Filesystem environment variables. Never print, log, or commit owner or delegated tokens.

## Create and read a secret

```shell
ti fs-vault create-secret \
  --secret-name db-prod \
  --field DB_URL=mysql://example \
  --field PASSWORD=@./password.txt

ti fs-vault read-secret --secret-name db-prod
```

Raw and environment output contains plaintext. Direct it only to the intended process.

## Delegate limited access

Create a short-lived read grant and capture its token:

```shell
export TI_VAULT_TOKEN="$(ti fs-vault create-grant \
  --agent-id deploy-agent \
  --scope db-prod/DB_URL \
  --permission read \
  --ttl 10m \
  --token-only)"
```

Prefer `TI_VAULT_TOKEN` to a command-line token because command-line values can remain in process listings or shell history.

## Inject a secret into a process

```shell
ti fs-vault run-with-secret --secret-path /n/vault/db-prod -- <command>
```

Prefer process injection to writing plaintext to disk.

## Audit and revoke access

```shell
ti fs-vault list-audit-events \
  --secret-name db-prod \
  --agent-id deploy-agent \
  --since 24h \
  --limit 20

ti fs-vault delete-grant \
  --grant-id "<grant-id>" \
  --revoked-by operator \
  --reason rotated
```

Revocation prevents new authorized operations but cannot erase a value that a process already read.

## Mount a read-only Vault view

On macOS or Linux with FUSE support:

```shell
mkdir -p /path/to/vault
ti fs-vault mount-vault \
  --mount-path /path/to/vault \
  --vault-token "$TI_VAULT_TOKEN"
```

Stop processes that use the mount before unmounting it:

```shell
ti fs-vault unmount-vault --mount-path /path/to/vault
```

Vault mounts are unavailable on Windows. Direct secret reads and process injection do not require a mount.

## Security recommendations

- Grant the narrowest field scope and shortest practical TTL.
- Do not store delegated tokens in CLI configuration or operation logs.
- Revoke grants after their tasks finish.

## What's next

- [Delegate TiDB Cloud Filesystem Vault Secrets to an Agent](/ai/ti/reference/ti-vault-agent-secrets-example.md)
- [TiDB Cloud Filesystem Vault CLI Command Reference](/ai/ti/reference/ti-filesystem-vault.md)
