---
title: ti db format-db-connection-string
summary: Format a connection string for a TiDB Cloud CLI-managed SQL user.
---

# ti db format-db-connection-string

Formats stored SQL credentials for read-write, read-only, or admin access. The command verifies that the cluster is Starter before loading its local SQL credentials.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti db format-db-connection-string
  --db-cluster-id <string>
  [--admin]
  [--database <string>]
  [--env-database-url-name <string>]
  [--env-include-database-url]
  [--env-prefix <string>]
  [--format <string>]
  [--help]
  [--read-only]
  [--read-write]
  [--version]
```

## Options

- `--db-cluster-id <string>`: Starter DB cluster ID. \[required]
- `--admin`: Use prepared admin DB SQL credentials.
- `--database <string>`: Database/default schema name.
- `--env-database-url-name <string>`: Database URL variable name for `--format env`. \[default: DATABASE_URL]
- `--env-include-database-url`: Include a database URL variable with `--format env`.
- `--env-prefix <string>`: Dotenv variable prefix for `--format env`. \[default: TIDB_]
- `--format <string>`: Connection string format: `mysql-uri`, `jdbc`, `go-sql-driver`, `sqlalchemy`, or `env`. \[default: mysql-uri]
- `--help`: Display help information.
- `--read-only`: Use prepared `read_only` DB SQL credentials.
- `--read-write`: Use prepared `read_write` DB SQL credentials.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Format a read-write MySQL URI:

    ```bash
    # Use the default application role in tools that accept a MySQL URI.
    ti db format-db-connection-string --db-cluster-id "<cluster-id>" --read-write --format mysql-uri
    ```

- Format read-only dotenv variables:

    ```bash
    # Emit environment assignments for a workload that must not modify data.
    ti db format-db-connection-string --db-cluster-id "<cluster-id>" --read-only --format env --env-prefix TIDB_
    ```

- Format an admin JDBC URL:

    ```bash
    # Generate a JDBC connection value with the prepared admin credentials.
    ti db format-db-connection-string --db-cluster-id "<cluster-id>" --admin --format jdbc --database app
    ```

- Include DATABASE_URL in dotenv output:

    ```bash
    # Emit both component variables and a conventional DATABASE_URL value.
    ti db format-db-connection-string --db-cluster-id "<cluster-id>" --format env --env-include-database-url
    ```

## Related documentation

- [TiDB Cloud Starter CLI Command Reference](/ai/ti/reference/ti-starter-database.md)
