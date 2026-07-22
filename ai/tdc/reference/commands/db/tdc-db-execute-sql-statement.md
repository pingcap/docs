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
    [--debug]
    [--output <string>]
    [--profile <string>]
    [--query <string>]
    [--region <string>]
```

For global flags such as `--profile`, `--region`, `--output`, and `--query`, see [tdc CLI Reference](/ai/tdc/reference/tdc-cli-reference.md).

## Examples

```shell
tdc db execute-sql-statement --db-cluster-id "<cluster-id>" --read-only --sql "SELECT 1" --output text
tdc db execute-sql-statement --db-cluster-id "<cluster-id>" --admin --sql "CREATE DATABASE IF NOT EXISTS app"
```
