---
title: TiDB Cloud Starter CLI Command Reference
summary: Reference every `ti db` command for Starter instances, branches, SQL users, connection strings, and SQL execution.
---

# TiDB Cloud Starter CLI Command Reference

Use `ti db` to manage TiDB Cloud Starter instances, branches, and SQL access. The CLI rejects instance-scoped operations when the target is not a TiDB Cloud Starter instance or its service plan cannot be verified.

A branch is a separate TiDB Cloud Starter instance that contains a diverged copy of data from its parent instance. Use branches to test changes in isolation without affecting the parent. For more information, see [TiDB Cloud Branching](/tidb-cloud/branch-overview.md).

## Commands

| Command | Description |
|---|---|
| [`create-db-cluster`](/ai/ti/reference/ti-db-create-db-cluster.md) | Creates a TiDB Cloud Starter instance. |
| [`list-db-clusters`](/ai/ti/reference/ti-db-list-db-clusters.md) | Lists Starter instances in the effective region. |
| [`describe-db-cluster`](/ai/ti/reference/ti-db-describe-db-cluster.md) | Describes a TiDB Cloud Starter instance. |
| [`update-db-cluster`](/ai/ti/reference/ti-db-update-db-cluster.md) | Updates a TiDB Cloud Starter instance. |
| [`delete-db-cluster`](/ai/ti/reference/ti-db-delete-db-cluster.md) | Deletes a TiDB Cloud Starter instance. |
| [`create-db-cluster-branch`](/ai/ti/reference/ti-db-create-db-cluster-branch.md) | Creates a branch for a TiDB Cloud Starter instance. |
| [`list-db-cluster-branches`](/ai/ti/reference/ti-db-list-db-cluster-branches.md) | Lists branches for a TiDB Cloud Starter instance. |
| [`describe-db-cluster-branch`](/ai/ti/reference/ti-db-describe-db-cluster-branch.md) | Describes a branch for a TiDB Cloud Starter instance. |
| [`delete-db-cluster-branch`](/ai/ti/reference/ti-db-delete-db-cluster-branch.md) | Deletes a branch from a TiDB Cloud Starter instance. |
| [`create-db-sql-users`](/ai/ti/reference/ti-db-create-db-sql-users.md) | Creates or repairs role-based SQL users. |
| [`format-db-connection-string`](/ai/ti/reference/ti-db-format-db-connection-string.md) | Formats stored SQL credentials as a connection string. |
| [`execute-sql-statement`](/ai/ti/reference/ti-db-execute-sql-statement.md) | Executes one SQL statement. |

## See also

- [Manage TiDB Cloud Starter Instances](/ai/ti/guides/manage-starter-instances.md)
- [Query TiDB Cloud Starter with Explicit SQL Roles](/ai/ti/guides/ti-query-sql-with-roles-example.md)
