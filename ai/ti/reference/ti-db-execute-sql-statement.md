---
title: ti db execute-sql-statement
summary: Execute one SQL statement against a TiDB Cloud Starter cluster.
---

# ti db execute-sql-statement

Executes one SQL statement against a TiDB Cloud Starter instance. The default access role is read-write; specifying a role explicitly is recommended.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

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
    # Open a direct TLS MySQL connection when the workflow requires the MySQL protocol.
    ti db execute-sql-statement --db-cluster-id "<cluster-id>" --transport mysql --sql "SELECT CURRENT_TIMESTAMP"
    ```

## Choose a transport

The default `https` transport sends the statement to the TiDB Cloud HTTPS SQL API. The `mysql` transport opens a direct TLS MySQL connection to the instance, executes the statement once, and closes the connection. Use `mysql` only when your network or workflow specifically requires the MySQL protocol.

The CLI does not automatically fall back from `https` to `mysql` or retry a statement through the other transport. This prevents a write statement from being executed twice after an ambiguous failure.

## Output

JSON output contains `fields`, `rows`, `row_count`, `rows_affected` when applicable, `last_insert_id` when applicable, `transport`, `access_mode`, and `cluster_id`. Each item in `rows` is an object keyed by column name.

With `--output text`, query results are rendered as a table with column headings and a row count. Statements that do not return rows produce a `Query OK` message with the affected-row count and, when available, the last insert ID.

## Related documentation

- [TiDB Cloud Starter CLI Command Reference](/ai/ti/reference/ti-starter-database.md)
