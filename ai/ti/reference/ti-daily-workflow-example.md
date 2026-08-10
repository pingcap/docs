---
title: Run a Daily TiDB Cloud CLI Workflow
summary: Inspect projects, manage a Starter cluster and Filesystem, check for TiDB Cloud CLI updates, and clean up resources.
---

# Run a Daily TiDB Cloud CLI Workflow

This example follows a typical operator workflow across TiDB Cloud Starter and TiDB Cloud Filesystem.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Prerequisites

- Install `ti` and run `ti configure`.
- Ensure your organization has capacity for one Starter cluster and one Filesystem.

## Step 1. Inspect the active account

```bash
ti organization list-projects --output text
ti db list-db-clusters --db-cluster-type starter --output text
ti fs list-file-systems --output text
```

## Step 2. Create a Starter cluster

```bash
ti db create-db-cluster \
  --db-cluster-type starter \
  --db-cluster-name daily-demo \
  --dry-run

ti db create-db-cluster \
  --db-cluster-type starter \
  --db-cluster-name daily-demo \
  --wait
```

Record the returned cluster ID. Because `--wait` was set, the create command returns after the cluster is active. You can inspect it again later:

```bash
ti db describe-db-cluster \
  --db-cluster-id "<cluster-id>" \
  --output text
```

## Step 3. Verify SQL access

```bash
ti db create-db-sql-users --db-cluster-id "<cluster-id>"
ti db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --read-only \
  --sql "SELECT CURRENT_TIMESTAMP AS checked_at" \
  --output text
```

## Step 4. Create and use a Filesystem

```bash
ti fs create-file-system \
  --file-system-name daily-workspace

printf 'daily workflow\n' | ti fs copy-file \
  --file-system-name daily-workspace \
  --from-stdin \
  --to-remote /notes/today.txt

ti fs list-files \
  --file-system-name daily-workspace \
  --path /notes \
  --output text
```

The file in `/notes/today.txt` verifies that the explicitly selected resource is usable.

## Step 5. Check for updates

Unmount active filesystems before applying an update. A check is always non-mutating:

```bash
ti update --check
```

Apply an update when appropriate:

```bash
ti update --dry-run
ti update
```

## Cleanup

```bash
ti fs delete-file-system \
  --file-system-name daily-workspace

ti db delete-db-cluster \
  --db-cluster-id "<cluster-id>"
```

Deleting local TiDB Cloud CLI configuration is not a substitute for deleting remote resources.

## Security notes

- Do not echo FS tokens or formatted database connection strings.
- Use unique automation prefixes and delete only resources created by that run.
- Preview destructive operations with `--dry-run`.

## What's next

- [TiDB Cloud Starter CLI Command Reference](/ai/ti/reference/ti-starter-database.md)
- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
