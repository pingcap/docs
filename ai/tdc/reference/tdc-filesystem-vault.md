---
title: tdc fs-vault Command Reference
summary: Reference every tdc fs-vault command for secrets, grants, audit events, process injection, and read-only mounts.
---

# tdc fs-vault Command Reference

`tdc fs-vault` stores structured secrets and delegates limited, expiring access to agents. Owner operations use the Filesystem owner credential; delegated reads use a vault token scoped to selected secrets or fields.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Command tree

```text
tdc fs-vault
├── create-secret
├── replace-secret
├── read-secret
├── list-secrets
├── delete-secret
├── create-grant
├── delete-grant
├── list-audit-events
├── run-with-secret
├── mount-vault
└── unmount-vault
```

| Command | Purpose and key inputs | Example |
| --- | --- | --- |
| `create-secret` | Creates a structured secret from repeatable literal, file, or stdin fields. | `tdc fs-vault create-secret --secret-name db-prod --field PASSWORD=@./password.txt` |
| `replace-secret` | Replaces all fields from files in one directory. | `tdc fs-vault replace-secret --secret-path /n/vault/db-prod --from-directory ./secret-fields` |
| `read-secret` | Reads all fields or one field as structured, raw, or environment output. | `tdc fs-vault read-secret --secret-name db-prod --field DB_URL --format raw` |
| `list-secrets` | Lists secrets visible to the active owner or delegated credential. | `tdc fs-vault list-secrets` |
| `delete-secret` | Deletes one owner-visible secret. | `tdc fs-vault delete-secret --secret-name db-prod` |
| `create-grant` | Creates a scoped, expiring delegated token for one agent. | `tdc fs-vault create-grant --agent-id deploy-agent --scope db-prod/DB_URL --permission read --ttl 10m` |
| `delete-grant` | Revokes one grant by ID. | `tdc fs-vault delete-grant --grant-id "<grant-id>" --reason completed` |
| `list-audit-events` | Lists vault access events using secret, agent, time, and limit filters. | `tdc fs-vault list-audit-events --secret-name db-prod --limit 20` |
| `run-with-secret` | Runs a child command with secret fields injected as environment variables. | `tdc fs-vault run-with-secret --secret-path /n/vault/db-prod -- ./deploy.sh` |
| `mount-vault` | Mounts delegated readable fields as a local read-only FUSE filesystem. | `tdc fs-vault mount-vault --mount-path /path/to/vault --vault-token "$TDC_VAULT_TOKEN"` |
| `unmount-vault` | Unmounts a local vault mount. | `tdc fs-vault unmount-vault --mount-path /path/to/vault` |

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

- [Delegate Secrets to an Agent](/ai/tdc/reference/tdc-vault-agent-secrets-example.md)
- [tdc Regions, Security, and Limitations](/ai/tdc/reference/tdc-regions-security-and-limitations.md)
