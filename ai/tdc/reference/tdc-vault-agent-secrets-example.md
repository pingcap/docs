---
title: Delegate Filesystem Vault Secrets to an Agent
summary: Store a secret, grant one field to an agent, inject it into a process, audit access, and revoke the grant.
---

# Delegate Filesystem Vault Secrets to an Agent

This example gives an agent temporary access to one secret field without sharing the Filesystem owner token or the complete secret.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## The agent problem

An agent might need one API endpoint or token to complete a short task. Putting the complete secret in a prompt, `.env` file, or sandbox image exposes it beyond the process and lifetime that need it. Sharing the Filesystem owner token also grants much more access than one secret field requires.

## Why ordinary environment variables and files are not enough

Environment variables and files can deliver a secret, but they do not create a scoped, expiring delegation or an access audit trail. A separate cloud secret manager can provide those controls, but it requires another identity, policy, and integration path for every sandbox.

## How tdc changes the workflow

The Filesystem owner stores the secret once and creates a short-lived grant scoped to the required field. The agent receives only the delegated vault token and can inject the allowed value into a child process. The owner can inspect audit events and revoke the grant without rotating or exposing the Filesystem owner credential.

## Prerequisites

- Select a Filesystem with owner access.
- Store the source secret value in a protected file.

## Step 1. Create a secret

```bash
tdc fs-vault create-secret \
  --secret-name service-demo \
  --field ENDPOINT=https://service.example \
  --field API_TOKEN=@./api-token.txt
```

## Step 2. Create a narrow grant

```bash
export TDC_VAULT_TOKEN="$(tdc fs-vault create-grant \
  --agent-id example-agent \
  --scope service-demo/ENDPOINT \
  --permission read \
  --ttl 10m \
  --label-hint example \
  --token-only)"
```

Record the returned grant ID from the structured create result in a real workflow. The token is captured and not printed.

## Step 3. Use the delegated field

```bash
tdc fs-vault read-secret \
  --secret-name service-demo \
  --field ENDPOINT \
  --format raw
```

Inject the allowed fields into a command:

```bash
tdc fs-vault run-with-secret \
  --secret-path /n/vault/service-demo \
  -- sh -c 'test -n "$ENDPOINT"'
```

The process exits successfully when the permitted field is present. Do not use commands that print all environment values.

## Step 4. Audit and revoke

```bash
tdc fs-vault list-audit-events \
  --secret-name service-demo \
  --agent-id example-agent \
  --limit 20

tdc fs-vault delete-grant \
  --grant-id "<grant-id>" \
  --revoked-by operator \
  --reason task-complete
```

Unset the local token:

```bash
unset TDC_VAULT_TOKEN
```

## Cleanup

```bash
tdc fs-vault delete-secret --secret-name service-demo
rm -f ./api-token.txt
```

## Security notes

- Scope grants to the smallest set of fields and shortest useful TTL.
- A revoked token cannot authorize new reads, but it cannot erase a value already read by a process.
- Avoid secret flags because process listings and shell history can retain them.

## What's next

- [tdc fs-vault Command Reference](/ai/tdc/reference/tdc-filesystem-vault.md)
- [tdc Regions, Security, and Limitations](/ai/tdc/reference/tdc-regions-security-and-limitations.md)
