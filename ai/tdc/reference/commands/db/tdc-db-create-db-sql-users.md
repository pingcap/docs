---
title: tdc db create-db-sql-users
summary: Create tdc-managed SQL users for a Starter cluster.
---

# tdc db create-db-sql-users

Idempotently creates or repairs the read-only, read-write, and admin SQL users managed by tdc.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc db create-db-sql-users
    --db-cluster-id <string>
    [--dry-run]
    [--help]
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
tdc db create-db-sql-users --db-cluster-id "<cluster-id>" --dry-run
tdc db create-db-sql-users --db-cluster-id "<cluster-id>"
```
