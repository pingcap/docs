---
title: Delegate TiDB Cloud Filesystem Vault Secrets to an Agent
summary: Store a secret, grant one field to an agent, inject it into a process, audit access, and revoke the grant.
---

# Delegate TiDB Cloud Filesystem Vault Secrets to an Agent

This workflow gives an agent temporary access to one secret field without sharing the Filesystem owner token or the complete secret. Use it when an agent needs a credential for one task but should not retain that value in a prompt, `.env` file, or sandbox image.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## How it works

The Filesystem owner stores the secret once and creates a short-lived grant scoped to the required field. The agent receives only the delegated vault token and can inject the allowed value into a child process. The owner can inspect audit events and revoke the grant without rotating or exposing the Filesystem owner credential.

## Why use this approach

Ordinary environment variables and files can deliver a secret, but they do not create a scoped, expiring delegation or an access audit trail. Sharing the Filesystem owner token also grants broader access than one secret field requires. A separate cloud secret manager can provide similar controls, but it requires another identity, policy, and integration path for every sandbox.

## Prerequisites

- Select a Filesystem with owner access.
- Install `jq`.
- Store the source secret value in a protected file.

## Step 1. Create a secret

```bash
ti fs-vault create-secret \
  --secret-name service-demo \
  --field ENDPOINT=https://service.example \
  --field API_TOKEN=@./api-token.txt
```

## Step 2. Create a narrow grant

```bash
umask 077
set -o noclobber
ti fs-vault create-grant \
  --agent-id example-agent \
  --scope service-demo/ENDPOINT \
  --permission read \
  --ttl 10m \
  --label-hint example > ./vault-grant.json
set +o noclobber

export TI_VAULT_TOKEN="$(jq -r '.token' ./vault-grant.json)"
export GRANT_ID="$(jq -r '.grant_id' ./vault-grant.json)"
```

The protected file captures both one-time values without printing the token. Store the token in a secret manager and retain `GRANT_ID` so that you can revoke the grant.

## Step 3. Use the delegated field

```bash
ti fs-vault read-secret \
  --secret-name service-demo \
  --field ENDPOINT \
  --format raw
```

Inject the allowed fields into a command:

```bash
ti fs-vault run-with-secret \
  --secret-path /n/vault/service-demo \
  -- sh -c 'test -n "$ENDPOINT"'
```

The `/n/vault/` prefix identifies the Vault namespace for commands that accept a full secret path; `service-demo` refers to the secret created in Step 1. `run-with-secret` reads the permitted fields, sets them as environment variables in the child process, and then runs the command after `--`. This test exits successfully when `ENDPOINT` is present without printing its value. Do not use commands that print all environment values.

## Step 4. Audit and revoke

```bash
ti fs-vault list-audit-events \
  --secret-name service-demo \
  --agent-id example-agent \
  --limit 20

ti fs-vault delete-grant \
  --grant-id "$GRANT_ID" \
  --revoked-by operator \
  --reason task-complete
```

Unset the local token:

```bash
unset TI_VAULT_TOKEN
```

## Cleanup

```bash
ti fs-vault delete-secret --secret-name service-demo
rm -f ./api-token.txt ./vault-grant.json
```

## Security and operational notes

- Scope grants to the smallest set of fields and shortest useful TTL.
- A revoked token cannot authorize new reads, but it cannot erase a value already read by a process.
- Avoid secret flags because process listings and shell history can retain them.

## What's next

- [TiDB Cloud Filesystem Vault CLI Command Reference](/ai/ti/reference/ti-filesystem-vault.md)
- [TiDB Cloud CLI Regions, Security, and Limitations](/ai/ti/reference/ti-regions-security-and-limitations.md)
