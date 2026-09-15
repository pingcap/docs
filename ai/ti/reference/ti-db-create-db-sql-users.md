---
title: ti db create-db-sql-users
summary: Create TiDB Cloud CLI-managed SQL users for a TiDB Cloud Starter instance.
---

# ti db create-db-sql-users

Creates or repairs three `ti`-managed SQL users for a TiDB Cloud Starter instance: read-only, read-write, and admin. It stores their credentials locally so that later commands can select the appropriate user with `--read-only`, `--read-write`, or `--admin`.

These users have the following predefined access levels and built-in TiDB Cloud roles:

| `ti` access mode | TiDB Cloud built-in role | Intended use |
| --- | --- | --- |
| `read_only` | `role_readonly` | Query and verify data without modifying it |
| `read_write` | `role_readwrite` | Query and modify application data |
| `admin` | `role_admin` | Make schema changes and manage privileges |

For the TiDB Cloud role model, see [Manage Database Users and Roles](/tidb-cloud/configure-sql-users.md).

`ti` stores the generated usernames and passwords in `~/.ti/db_users/<cluster-id>/credentials`, with separate TOML sections for the three access modes. On systems that support POSIX permissions, the credentials file is readable and writable only by its owner.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

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
