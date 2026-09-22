---
title: Manage TiDB Cloud Filesystem Vault Secrets
summary: Learn how to store and rotate secrets, delegate temporary access, inject secrets into processes, audit and revoke access, and optionally mount secrets as read-only files.
aliases: ['/ai/manage-filesystem-vault-secrets']
---

# Manage TiDB Cloud Filesystem Vault Secrets

Use TiDB Cloud Filesystem Vault when an application, automation, or agent needs credentials or other sensitive values, but you do not want to store those values in regular Filesystem files or give the workflow broad access to the Filesystem.

With Vault, a trusted owner can store a secret once and grant access to only the secret or field that a user, application, or agent needs, for a limited time. The delegated workflow can then read the permitted value, inject it into a process, or access it through a read-only mount. The owner can audit the access and revoke the grant when it is no longer needed.

This guide shows you how to store and rotate secrets, delegate limited access, use delegated secrets, audit and revoke access, and optionally mount secrets as files.

## Prerequisites

Before you begin:

- [Install TiDB Cloud CLI](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli).
- Have access to an existing TiDB Cloud Filesystem.
- Make the Filesystem and its owner token available to `ti`. See [Access an Existing TiDB Cloud Filesystem](/tidb-cloud-filesystem/access-filesystem.md).

An owner token is used to create and replace secrets, create and revoke grants, and view audit events. A delegated Vault token provides only the secret access allowed by its grant.

Treat both owner tokens and delegated Vault tokens as credentials. Do not expose them in logs, source control, shared terminal output, or command-line arguments.

## Create a secret

A Vault secret can contain multiple named fields. For example, a database secret might contain a connection URL and a password.

Create a secret named `db-prod`:

```shell
ti fs-vault create-secret \
  --secret-name db-prod \
  --field DB_URL=mysql://example \
  --field PASSWORD=@./password.txt
```

In `PASSWORD=@./password.txt`, the `@` prefix tells `ti` to read the field value from the local file instead of treating the file path as the value.

Some Vault commands identify a secret by name, such as `db-prod`. Commands that operate on a specific secret path, such as `replace-secret` and `run-with-secret`, use its full Vault path instead. For example, the Vault path of `db-prod` is `/n/vault/db-prod`.

### Read a secret value

`read-secret` returns plaintext secret values. Use it only when you need the value directly, and make sure its output is not written to logs or other unintended destinations.

For example, to read only the `DB_URL` field:

```shell
ti fs-vault read-secret \
  --secret-name db-prod \
  --field DB_URL \
  --format raw
```

When an application needs the secret, prefer [injecting it into the process](#inject-a-secret-into-a-process) instead of reading and handling the plaintext value yourself.

## Rotate a secret

`replace-secret` replaces all fields in the secret, not just the field whose value changed.

To rotate `DB_URL`, create a local directory containing the new `DB_URL` value and the current `PASSWORD` value that you want to keep:

```text
./secret-fields/
├── DB_URL
└── PASSWORD
```

Then replace the secret:

```shell
ti fs-vault replace-secret \
  --secret-path /n/vault/db-prod \
  --from-directory ./secret-fields
```

Each file in the directory becomes a field in the replacement secret. Any existing field that is not included in the directory is not retained.

Keep these local files out of source control and remove them when they are no longer needed. For details, see the [`replace-secret` reference](/ai/ti/reference/ti-fs-vault-replace-secret.md).

## Delegate limited access

Instead of sharing the Filesystem owner token, create a short-lived grant for only the secret fields that another user, application, or agent needs.

For example, the following grant allows `deploy-agent` to read only the `DB_URL` field for 10 minutes:

```shell
ti fs-vault create-grant \
  --agent-id deploy-agent \
  --scope db-prod/DB_URL \
  --permission read \
  --ttl 10m
```

The command returns a delegated Vault token and a grant ID. Give the delegated token only to the workflow that needs the secret, and retain the grant ID so that you can revoke the grant before it expires if necessary.

In the environment that uses the delegated secret, make the token available as `TI_VAULT_TOKEN`. Also set `TI_FS_FILE_SYSTEM_ID` to the Filesystem ID and `TI_REGION_CODE` to its region code. The delegated Vault token alone does not identify the Filesystem. Avoid putting the token directly in a command-line argument because command arguments can appear in shell history or process listings.

## Inject a secret into a process

If an application can receive credentials through environment variables, use `run-with-secret` to make the permitted secret fields available only to the child process:

```shell
ti fs-vault run-with-secret \
  --secret-path /n/vault/db-prod \
  -- <command>
```

Each permitted secret field becomes an environment variable with the same name. With the `db-prod/DB_URL` grant in this example, `ti` injects `DB_URL` into the child process, but does not inject `PASSWORD`.

The Vault credential used by `ti` is not passed to the child process. This lets the application use the secret without writing its plaintext value to a file.

Field names used with `run-with-secret` must match `[A-Z_][A-Z0-9_]*`. Use uppercase environment-variable-style field names for secrets that you plan to inject into a process.

## Audit and revoke access

To review recent access to `db-prod` by `deploy-agent`, run:

```shell
ti fs-vault list-audit-events \
  --secret-name db-prod \
  --agent-id deploy-agent \
  --since 24h \
  --limit 20
```

When the delegated access is no longer needed, revoke the grant using the grant ID returned by `create-grant`:

```shell
ti fs-vault delete-grant \
  --grant-id "<grant-id>" \
  --revoked-by operator \
  --reason task-complete
```

Revoking a grant prevents the delegated token from authorizing new operations. It cannot remove a secret value that a process has already read.

## Mount secrets as read-only files

If an application expects credentials as files instead of environment variables, you can optionally expose permitted Vault fields through a read-only FUSE mount on Linux or macOS.

For delegated access, first make the delegated Vault token available as `TI_VAULT_TOKEN`. Then create a local mount directory and mount the Vault:

```shell
mkdir -p /path/to/vault

ti fs-vault mount-vault \
  --mount-path /path/to/vault
```

The permitted secret fields are available as files under the mount path. For example:

```text
/path/to/vault/db-prod/DB_URL
```

Processes that can access the mount can read the permitted secret values, so keep access to the mount limited to the intended workload.

Before unmounting, stop processes that are using the mounted secrets:

```shell
ti fs-vault unmount-vault \
  --mount-path /path/to/vault
```

Vault mounts require FUSE and are not available on Windows. Direct secret reads and `run-with-secret` do not require a mount.

## Security recommendations

- Grant access only to the secret fields required by the workflow and use the shortest practical TTL.
- Prefer `run-with-secret` when an application can receive credentials through environment variables.
- Do not expose owner or delegated tokens in logs, source control, or command-line arguments.
- Revoke grants when their tasks finish or access is no longer needed.

## What's next

- [Delegate TiDB Cloud Filesystem Vault Secrets to an Agent](/ai/ti/guides/ti-vault-agent-secrets-example.md)
- [TiDB Cloud Filesystem Vault CLI Command Reference](/ai/ti/reference/ti-filesystem-vault.md)
