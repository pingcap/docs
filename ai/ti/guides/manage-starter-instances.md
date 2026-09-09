---
title: Manage TiDB Cloud Starter Instances
summary: Learn how to use TiDB Cloud CLI to create and manage Starter instances, branches, SQL users, connections, and SQL statements.
---

# Manage TiDB Cloud Starter Instances

This document describes how to use `ti db` commands in the TiDB Cloud CLI to manage TiDB Cloud Starter instances, branches, and SQL access from a terminal or automation workflow.

## Prerequisites

- [Install and configure TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md).
- Configure a profile with credentials that can access TiDB Cloud Starter.

## Create a TiDB Cloud Starter instance

Create a TiDB Cloud Starter instance and wait until it becomes active:

```shell
ti db create-db-cluster --db-cluster-type starter --db-cluster-name app-db --wait
```

## List instances

List TiDB Cloud Starter instances in the effective region:

```shell
ti db list-db-clusters --db-cluster-type starter --output text
```

To get information about a TiDB Cloud Starter instance, pass its ID to [`describe-db-cluster`](/ai/ti/reference/commands/db/ti-db-describe-db-cluster.md).

## Manage branches

Create a development branch from an instance:

```shell
ti db create-db-cluster-branch \
  --db-cluster-id "<instance-id>" \
  --db-cluster-branch-name dev \
  --wait
```

Use the branch list, description, and deletion commands to manage its lifecycle. For their complete options, see the [`ti db` command reference](/ai/ti/reference/ti-starter-database.md).

## Configure SQL access

Create or repair the read-only, read-write, and admin SQL users for an instance:

```shell
ti db create-db-sql-users --db-cluster-id "<instance-id>"
```

Format the stored credentials for an application:

```shell
ti db format-db-connection-string \
  --db-cluster-id "<instance-id>" \
  --read-only \
  --format env
```

## Execute SQL

Execute one statement with an explicit SQL role:

```shell
ti db execute-sql-statement \
  --db-cluster-id "<instance-id>" \
  --read-only \
  --sql "SELECT 1"
```

For a workflow that separates read-only, read-write, and administrative operations, see [Query TiDB Cloud Starter with Explicit SQL Roles](/ai/ti/reference/ti-query-sql-with-roles-example.md).

## Delete an instance

When you no longer need the instance, delete it and wait until the deletion is observable:

```shell
ti db delete-db-cluster --db-cluster-id "<instance-id>" --wait
```

## What's next

- [TiDB Cloud Starter CLI Command Reference](/ai/ti/reference/ti-starter-database.md)
- [Run a Daily TiDB Cloud CLI Workflow](/ai/ti/reference/ti-daily-workflow-example.md)
