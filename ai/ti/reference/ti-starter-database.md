---
title: TiDB Cloud Starter CLI Command Reference
summary: Reference every `ti db` command for Starter instances, branches, SQL users, connection strings, and SQL execution.
---

# TiDB Cloud Starter CLI Command Reference

Use `ti db` to manage TiDB Cloud Starter instances, branches, and SQL access. The CLI rejects instance-scoped operations when the target is not a TiDB Cloud Starter instance or its service plan cannot be verified.

## Commands

| Command | Description |
|---|---|
| [`create-db-cluster`](/ai/ti/reference/commands/db/ti-db-create-db-cluster.md) | Creates a TiDB Cloud Starter instance. |
| [`list-db-clusters`](/ai/ti/reference/commands/db/ti-db-list-db-clusters.md) | Lists Starter instances in the effective region. |
| [`describe-db-cluster`](/ai/ti/reference/commands/db/ti-db-describe-db-cluster.md) | Describes a TiDB Cloud Starter instance. |
| [`update-db-cluster`](/ai/ti/reference/commands/db/ti-db-update-db-cluster.md) | Updates a TiDB Cloud Starter instance. |
| [`delete-db-cluster`](/ai/ti/reference/commands/db/ti-db-delete-db-cluster.md) | Deletes a TiDB Cloud Starter instance. |
| [`create-db-cluster-branch`](/ai/ti/reference/commands/db/ti-db-create-db-cluster-branch.md) | Creates a branch. |
| [`list-db-cluster-branches`](/ai/ti/reference/commands/db/ti-db-list-db-cluster-branches.md) | Lists branches. |
| [`describe-db-cluster-branch`](/ai/ti/reference/commands/db/ti-db-describe-db-cluster-branch.md) | Describes a branch. |
| [`delete-db-cluster-branch`](/ai/ti/reference/commands/db/ti-db-delete-db-cluster-branch.md) | Deletes a branch. |
| [`create-db-sql-users`](/ai/ti/reference/commands/db/ti-db-create-db-sql-users.md) | Creates or repairs role-based SQL users. |
| [`format-db-connection-string`](/ai/ti/reference/commands/db/ti-db-format-db-connection-string.md) | Formats stored SQL credentials as a connection string. |
| [`execute-sql-statement`](/ai/ti/reference/commands/db/ti-db-execute-sql-statement.md) | Executes one SQL statement. |

## See also

- [Manage TiDB Cloud Starter Instances](/ai/ti/guides/manage-starter-instances.md)
- [Query TiDB Cloud Starter with Explicit SQL Roles](/ai/ti/reference/ti-query-sql-with-roles-example.md)
