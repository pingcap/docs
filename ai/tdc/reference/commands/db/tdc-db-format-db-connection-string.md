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
    [--debug]
    [--output <string>]
    [--profile <string>]
    [--query <string>]
    [--region <string>]
```

For global flags such as `--profile`, `--region`, `--output`, and `--query`, see [tdc CLI Reference](/ai/tdc/reference/tdc-cli-reference.md).

## Examples

```shell
tdc db format-db-connection-string --db-cluster-id "<cluster-id>" --read-write --format mysql-uri
tdc db format-db-connection-string --db-cluster-id "<cluster-id>" --read-only --format env --env-prefix TIDB_
```
