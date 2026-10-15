---
title: Run a Daily TiDB Cloud CLI Workflow
summary: Inspect resources, manage a TiDB Cloud Starter instance and file system, check for TiDB Cloud CLI updates, and clean up resources.
---

# Run a Daily TiDB Cloud CLI Workflow

This example follows a typical operator workflow across TiDB Cloud Starter and TiDB Cloud Filesystem.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Prerequisites

- Install `ti` and run `ti configure`.
- Ensure your organization has capacity for one TiDB Cloud Starter instance and one file system.

## Step 1. Inspect current resources

```bash
ti db list-db-clusters --db-cluster-type starter --output text
ti fs list-file-systems --output text
```

## Step 2. Create a TiDB Cloud Starter instance

```bash
ti db create-db-cluster \
  --db-cluster-type starter \
  --db-cluster-name daily-demo \
  --dry-run

export DB_CLUSTER_ID="$(ti db create-db-cluster \
  --db-cluster-type starter \
  --db-cluster-name daily-demo \
  --wait \
  --query id \
  --output text)"
```

The command saves the returned cluster ID in `DB_CLUSTER_ID`. Because `--wait` was set, the create command returns after the cluster is active. You can inspect it again later:

```bash
ti db describe-db-cluster \
  --db-cluster-id "$DB_CLUSTER_ID" \
  --output text
```

## Step 3. Verify SQL access

```bash
ti db create-db-sql-users --db-cluster-id "$DB_CLUSTER_ID"
ti db execute-sql-statement \
  --db-cluster-id "$DB_CLUSTER_ID" \
  --read-only \
  --sql "SELECT CURRENT_TIMESTAMP AS checked_at" \
  --output text
```

## Step 4. Create and use a file system

```bash
export TI_FS_FILE_SYSTEM_ID="$(ti fs create-file-system \
  --wait \
  --query file_system_id \
  --output text)"

printf 'daily workflow\n' | ti fs copy-file \
  --from-stdin \
  --to-remote /notes/today.txt

ti fs list-files \
  --path /notes \
  --output text
```

The file in `/notes/today.txt` verifies that the explicitly selected resource is usable.

## Step 5. Check for updates

Check whether a newer version is available without changing the installed version:

```bash
ti update --check
```

Preview an update:

```bash
ti update --dry-run
```

If another workflow has an active file system or Vault mount, stop writers and unmount it before applying the update so that `ti` and the file system runtime are updated together. For instructions, see [Update TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md#update-tidb-cloud-cli).

Apply the update when appropriate:

```bash
ti update
```

## Cleanup

```bash
ti fs delete-file-system \
  --file-system-id "$TI_FS_FILE_SYSTEM_ID"

ti db delete-db-cluster \
  --db-cluster-id "$DB_CLUSTER_ID"
```

> **Note:**
>
> Deleting local TiDB Cloud CLI configuration does not delete remote resources.

## Security notes

- Do not echo file system tokens or formatted database connection strings.
- Use unique automation prefixes and delete only resources created by that run.
- Preview destructive operations with `--dry-run`.

## What's next

- [TiDB Cloud Starter CLI Command Reference](/ai/ti/reference/ti-starter-database.md)
- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
