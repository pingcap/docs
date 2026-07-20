---
title: Run a Daily tdc Workflow
summary: Inspect projects, manage a Starter cluster and Filesystem, check for tdc updates, and clean up resources.
---

# Run a Daily tdc Workflow

This example follows a typical operator workflow across TiDB Cloud Starter and TiDB Cloud Filesystem.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Prerequisites

- Install tdc and run `tdc configure`.
- Ensure your organization has capacity for one Starter cluster and one Filesystem.

## Step 1. Inspect the active account

```bash
tdc organization list-projects --output text
tdc db list-db-clusters --output text
tdc fs list-file-systems --output text
```

## Step 2. Create a Starter cluster

```bash
tdc db create-db-cluster \
  --db-cluster-name daily-demo \
  --db-cluster-type starter \
  --dry-run

tdc db create-db-cluster \
  --db-cluster-name daily-demo \
  --db-cluster-type starter
```

Record the returned cluster ID and wait until the cluster is active:

```bash
tdc db describe-db-cluster \
  --db-cluster-id "<cluster-id>" \
  --output text
```

## Step 3. Verify SQL access

```bash
tdc db create-db-sql-users --db-cluster-id "<cluster-id>"
tdc db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --read-only \
  --sql "SELECT CURRENT_TIMESTAMP AS checked_at" \
  --output text
```

## Step 4. Create and use a Filesystem

```bash
tdc fs create-file-system \
  --file-system-name daily-workspace \
  --set-default

printf 'daily workflow\n' | tdc fs copy-file \
  --from-stdin \
  --to-remote /notes/today.txt

tdc fs list-files --path /notes --output text
```

The file in `/notes/today.txt` verifies that the selected default resource is usable.

## Step 5. Check for updates

Unmount active filesystems before applying an update. A check is always non-mutating:

```bash
tdc update --check
```

Apply an update when appropriate:

```bash
tdc update --dry-run
tdc update
```

## Cleanup

```bash
tdc fs delete-file-system \
  --file-system-name daily-workspace

tdc db delete-db-cluster \
  --db-cluster-id "<cluster-id>"
```

Deleting local tdc configuration is not a substitute for deleting remote resources.

## Security notes

- Do not echo FS tokens or formatted database connection strings.
- Use unique automation prefixes and delete only resources created by that run.
- Preview destructive operations with `--dry-run`.

## What's next

- [Manage TiDB Cloud Starter Databases](/ai/tdc/guides/tdc-starter-database.md)
- [Manage TiDB Cloud Filesystem with tdc](/ai/tdc/guides/tdc-filesystem.md)
