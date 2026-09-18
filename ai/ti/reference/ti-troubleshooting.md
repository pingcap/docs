---
title: Troubleshoot TiDB Cloud CLI
summary: Learn how to diagnose TiDB Cloud CLI API authentication, Starter quota, SQL credential, and interrupted-command failures safely.
---

# Troubleshoot TiDB Cloud CLI

Use this reference to diagnose CLI authentication, Starter, SQL, and interrupted-command failures. For Filesystem tokens, regions, companion processes, and mounts, see [Troubleshoot TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-troubleshooting.md). Add `--debug` only when needed; review redacted output before sharing it.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## API authentication fails

Symptoms include missing credentials, Digest authentication failure, or permission denied.

Check that both environment values are set together:

```bash
test -n "$TIDB_CLOUD_PUBLIC_KEY"
test -n "$TIDB_CLOUD_PRIVATE_KEY"
```

If you intend to use saved credentials, unset both variables and verify the profile:

```bash
unset TIDB_CLOUD_PUBLIC_KEY TIDB_CLOUD_PRIVATE_KEY
ti db list-db-clusters --db-cluster-type starter --profile default
```

An API key can authenticate successfully but still lack the permission declared by a command. Use a key with the access required by that operation. `ti configure` validates and stores local values without contacting TiDB Cloud, so credential failures first appear on a remote command.

## Starter creation reaches quota

Quota and capacity errors can mean the organization has reached its free Starter limit. List existing Starter resources before creating another:

```bash
ti db list-db-clusters --db-cluster-type starter --output text
```

Never delete an unrelated resource to make automation pass. A Starter spending limit can require configured billing.

## SQL credentials are missing

Prepare or repair users for the exact cluster:

```bash
ti db create-db-sql-users --db-cluster-id "<cluster-id>"
```

Then retry with an explicit role:

```bash
ti db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --read-only \
  --sql "SELECT 1"
```

Deleting `~/.ti/db_users/<cluster-id>/credentials` removes local passwords. Run the create/repair command rather than inventing credentials.

## An interrupted command leaves resources

List resources and identify only those created by your workflow. Use describe before delete:

```bash
ti db describe-db-cluster --db-cluster-id "<cluster-id>"
ti fs describe-file-system --file-system-id "<file-system-id>"
```

Preview supported cleanup:

```bash
ti db delete-db-cluster --db-cluster-id "<cluster-id>" --dry-run
ti fs delete-file-system \
  --file-system-id "<file-system-id>" \
  --dry-run
```

## Report a problem

Include the TiDB Cloud CLI version, OS and architecture, command name, stable error code, and redacted logs. Never include API keys, FS or vault tokens, DB passwords, SQL containing private data, or file contents. Report issues at [github.com/tidbcloud/ti-cli/issues](https://github.com/tidbcloud/ti-cli/issues).
