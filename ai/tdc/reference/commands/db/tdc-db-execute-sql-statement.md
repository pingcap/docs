---
title: tdc db execute-sql-statement
summary: Execute one SQL statement against a TiDB Cloud Starter cluster.
---

# tdc db execute-sql-statement

Executes exactly one SQL statement. Read-write is the default role; explicit role selection is recommended.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc db execute-sql-statement
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
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Run a read-only query

```bash
tdc db execute-sql-statement --db-cluster-id "<cluster-id>" --read-only --sql "SELECT 1" --output text
```

### Run an administrative statement

```bash
tdc db execute-sql-statement --db-cluster-id "<cluster-id>" --admin --sql "CREATE DATABASE IF NOT EXISTS app"
```
