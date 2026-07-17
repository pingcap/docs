---
title: Use TiDB Cloud Filesystem Vault
summary: Store Filesystem secrets, delegate limited access, inject secrets into processes, audit access, and mount a read-only vault.
---

# Use TiDB Cloud Filesystem Vault

`tdc fs-vault` stores structured secrets and delegates limited, expiring access to agents. Owner operations use the Filesystem owner credential; delegated reads use a vault token scoped to selected secrets or fields.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Prerequisites

Select a Filesystem through a profile or the config-free FS environment variables. Never print, log, or commit owner or delegated tokens.

## Create and replace secrets

Create a secret with repeatable fields:

```bash
tdc fs-vault create-secret \
  --secret-name db-prod \
  --field DB_URL=mysql://example \
  --field PASSWORD=@./password.txt
```

`key=value` uses a literal value, `key=@file` reads a file, and `key=-` reads the value from stdin.

Replace all fields with files from a directory:

```bash
tdc fs-vault replace-secret \
  --secret-path /n/vault/db-prod \
  --from-directory ./secret-fields
```

## Read, list, and delete

```bash
tdc fs-vault list-secrets
tdc fs-vault read-secret --secret-name db-prod
tdc fs-vault read-secret --secret-name db-prod --field DB_URL --format raw
tdc fs-vault read-secret --secret-name db-prod --field DB_URL --format env
```

Delete an owner-visible secret:

```bash
tdc fs-vault delete-secret --secret-name db-prod
```

Raw and environment output contains plaintext. Direct it only to the intended process.

## Delegate limited access

Create a short-lived read grant and capture its token:

```bash
export TDC_VAULT_TOKEN="$(tdc fs-vault create-grant \
  --agent-id deploy-agent \
  --scope db-prod/DB_URL \
  --permission read \
  --ttl 10m \
  --token-only)"
```

Scopes are repeatable. `--label-hint` can add non-secret operator context.

Use the delegated token:

```bash
tdc fs-vault read-secret \
  --secret-name db-prod \
  --field DB_URL \
  --format raw
```

`TDC_VAULT_TOKEN` is preferred over `--vault-token` because command-line values can remain in process listings or shell history.

## Inject a secret into a process

```bash
tdc fs-vault run-with-secret \
  --secret-path /n/vault/db-prod \
  -- env
```

The child receives secret fields as environment variables. Avoid commands that print the complete environment in production; `env` is shown only to demonstrate the interface.

## Audit and revoke

```bash
tdc fs-vault list-audit-events \
  --secret-name db-prod \
  --agent-id deploy-agent \
  --since 24h \
  --limit 20

tdc fs-vault delete-grant \
  --grant-id "<grant-id>" \
  --revoked-by operator \
  --reason rotated
```

Revocation prevents new authorized operations. It cannot erase secret values a process already read.

## Mount a read-only vault

On macOS or Linux with FUSE support:

```bash
mkdir -p /path/to/vault
tdc fs-vault mount-vault \
  --mount-path /path/to/vault \
  --vault-token "$TDC_VAULT_TOKEN"
```

The mount is read-only. `--foreground` keeps it attached to the terminal, and `--ready-timeout` changes the background readiness wait.

Unmount:

```bash
tdc fs-vault unmount-vault --mount-path /path/to/vault
```

Unmount also supports `--timeout`, `--force`, and `--ignore-absent`. Vault mount is unavailable on Windows and requires FUSE support; direct `read-secret` and `run-with-secret` do not require a mount.

## Security guidance

- Give an agent the narrowest field scope and shortest practical TTL.
- Prefer `run-with-secret` over writing plaintext to disk.
- Do not store delegated tokens in tdc config or operation logs.
- Stop processes using a vault mount before unmounting.
- Revoke a grant after the task finishes.

## What's next

- [Delegate Secrets to an Agent](/ai/tdc/examples/tdc-vault-agent-secrets-example.md)
- [tdc Regions, Security, and Limitations](/ai/tdc/reference/tdc-regions-security-and-limitations.md)
