---
title: ti db create-db-sql-users
summary: Create TiDB Cloud CLI-managed SQL users for a Starter cluster.
---

# ti db create-db-sql-users

Idempotently creates or repairs the read-only, read-write, and admin SQL users managed by `ti`. The command verifies that the cluster is Starter before calling SQL-user APIs or writing local credentials.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti db create-db-sql-users
  --db-cluster-id <string>
  [--dry-run]
  [--help]
  [--version]
```

## Options

- `--db-cluster-id <string>`: Starter DB cluster ID. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Create the managed SQL users:

    ```bash
    # Create or reconcile the read-only, read-write, and admin SQL users.
    ti db create-db-sql-users --db-cluster-id "<cluster-id>"
    ```

- Preview SQL user creation:

    ```bash
    # Show the three managed roles without changing SQL users or local credentials.
    ti db create-db-sql-users --db-cluster-id "<cluster-id>" --dry-run
    ```

## Related documentation

- [TiDB Cloud Starter CLI Command Reference](/ai/ti/reference/ti-starter-database.md)
