---
title: Manage Vault Secrets for a File System
summary: Learn how to store and rotate Vault secrets, grant temporary access to specific fields, use them in processes, and revoke access.
aliases: ['/ai/manage-filesystem-vault-secrets']
---

# Manage Vault Secrets for a File System

Use the file system Vault to store credentials and grant temporary access to the fields an application or agent needs. A delegated workflow can read those fields, inject them into a process, or access them through a read-only mount. The owner can audit and revoke access.

## Prerequisites

Before you begin:

- [Install TiDB Cloud CLI](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli).
- Have access to a test file system without an existing `db-prod` secret.
- Use Bash or Zsh. Keep the owner's shell open so that the cleanup steps can use the temporary directory created below.
- Make the file system and its owner token available to `ti`. See [Access an Existing File System](/tidb-cloud-filesystem/access-filesystem.md).

An owner token is used to create and replace secrets, create and revoke grants, and view audit events. A delegated Vault token provides only the secret access allowed by its grant.

Treat both owner tokens and delegated Vault tokens as credentials. Do not expose them in logs, source control, shared terminal output, or command-line arguments.

## Create a secret

A Vault secret can contain multiple named fields. For example, a database secret might contain a connection URL and a password.

Prepare a temporary directory containing a sample password. Use test values for this walkthrough:

```shell
umask 077
secret_dir="$(mktemp -d)"
printf '%s' 'example-password' > "$secret_dir/PASSWORD"
```

Create a secret named `db-prod`:

```shell
ti fs-vault create-secret \
  --secret-name db-prod \
  --field DB_URL=mysql://example \
  --field "PASSWORD=@$secret_dir/PASSWORD"
```

The `@` prefix tells `ti` to read the field value from the local file.

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

To rotate `DB_URL`, add its replacement value to the temporary directory. Keep the `PASSWORD` file so that the replacement retains that field:

```shell
printf '%s' 'mysql://example-new' > "$secret_dir/DB_URL"
ti fs-vault replace-secret \
  --secret-path /n/vault/db-prod \
  --from-directory "$secret_dir"
```

Each file in the directory becomes a field in the replacement secret. Any existing field that is not included in the directory is not retained.

Keep these local files out of source control and remove them when they are no longer needed. For details, see the [`replace-secret` reference](/ai/ti/reference/ti-fs-vault-replace-secret.md).

## Delegate limited access

Instead of sharing the file system owner token, create a short-lived grant for only the secret fields that another user, application, or agent needs.

For example, the following grant allows `deploy-agent` to read only the `DB_URL` field for 10 minutes:

```shell
ti fs-vault create-grant \
  --agent-id deploy-agent \
  --scope db-prod/DB_URL \
  --permission read \
  --ttl 10m
```

The command returns a delegated Vault token and a grant ID. Give the delegated token only to the workflow that needs the secret, and retain the grant ID so that you can revoke the grant before it expires if necessary.

In a separate environment that uses the delegated secret, make the token available as `TI_VAULT_TOKEN`. Also set `TI_FS_FILE_SYSTEM_ID` to the file system ID and `TI_REGION_CODE` to its region code. The delegated Vault token alone does not identify the file system. Avoid putting the token directly in a command-line argument because command arguments can appear in shell history or process listings.

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

## Mount secrets as read-only files

If an application expects credentials as files instead of environment variables, you can optionally expose permitted Vault fields through a read-only FUSE mount on Linux or macOS.

Use this option before revoking the grant and while its token is still valid. For delegated access, make the token available as `TI_VAULT_TOKEN`, with the file system ID and region set as described above. Then create a local mount directory and mount the Vault:

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

## Audit and revoke access

Back in the owner's environment, review recent access to `db-prod` by `deploy-agent`:

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

## Clean up the example

After unmounting and revoking the example grant, delete the test secret and the temporary files:

```shell
ti fs-vault delete-secret --secret-name db-prod
rm "$secret_dir/DB_URL" "$secret_dir/PASSWORD"
rmdir "$secret_dir"
```

## Security recommendations

- Grant access only to the secret fields required by the workflow and use the shortest practical TTL.
- Prefer `run-with-secret` when an application can receive credentials through environment variables.
- Do not expose owner or delegated tokens in logs, source control, or command-line arguments.
- Revoke grants when their tasks finish or access is no longer needed.

## What's next

- [Delegate File System Vault Secrets to an Agent](/ai/ti/guides/ti-vault-agent-secrets-example.md)
- [TiDB Cloud Filesystem Vault CLI Command Reference](/ai/ti/reference/ti-filesystem-vault.md)
