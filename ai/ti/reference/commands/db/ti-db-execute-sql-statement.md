---
title: ti db execute-sql-statement
summary: Execute one SQL statement against a TiDB Cloud Starter cluster.
---

# ti db execute-sql-statement

Executes exactly one SQL statement. Read-write is the default role; explicit role selection is recommended. The command verifies that the cluster is Starter before loading credentials or sending an HTTPS or MySQL request.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti db execute-sql-statement
  --db-cluster-id <string>
  --sql <string>
  [--admin]
  [--database <string>]
  [--help]
  [--read-only]
  [--read-write]
  [--transport <string>]
  [--version]
```

## Options

- `--db-cluster-id <string>`: Starter DB cluster ID. \[required]
- `--sql <string>`: One SQL statement to execute. \[required]
- `--admin`: Use prepared admin DB SQL credentials.
- `--database <string>`: Database/default schema name.
- `--help`: Display help information.
- `--read-only`: Use prepared `read_only` DB SQL credentials.
- `--read-write`: Use prepared `read_write` DB SQL credentials.
- `--transport <string>`: SQL execution transport: `https` or `mysql`. \[default: https]
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Run a statement with the default read-write role:

    ```bash
    # Use the default prepared role for normal application reads and writes.
    ti db execute-sql-statement --db-cluster-id "<cluster-id>" --sql "INSERT INTO app.events(message) VALUES ('ready')"
    ```

- Run a read-only query:

    ```bash
    # Prevent the statement from using read-write or admin credentials.
    ti db execute-sql-statement --db-cluster-id "<cluster-id>" --read-only --sql "SELECT 1 AS ready" --output text
    ```

- Run an administrative statement:

    ```bash
    # Use the admin role for schema creation or privilege management.
    ti db execute-sql-statement --db-cluster-id "<cluster-id>" --admin --sql "CREATE DATABASE IF NOT EXISTS app"
    ```

- Use the MySQL fallback transport:

    ```bash
    # Open a one-shot MySQL connection when the HTTPS SQL API is unsuitable.
    ti db execute-sql-statement --db-cluster-id "<cluster-id>" --transport mysql --sql "SELECT CURRENT_TIMESTAMP"
    ```

## Related documentation

- [TiDB Cloud Starter CLI Command Reference](/ai/ti/reference/ti-starter-database.md)
