---
title: tdc db format-db-connection-string
summary: Format a connection string for a tdc-managed SQL user.
---

# tdc db format-db-connection-string

Formats stored SQL credentials for read-write, read-only, or admin access.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc db format-db-connection-string
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
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Format a read-write MySQL URI

```bash
tdc db format-db-connection-string --db-cluster-id "<cluster-id>" --read-write --format mysql-uri
```

### Format read-only dotenv variables

```bash
tdc db format-db-connection-string --db-cluster-id "<cluster-id>" --read-only --format env --env-prefix TIDB_
```
