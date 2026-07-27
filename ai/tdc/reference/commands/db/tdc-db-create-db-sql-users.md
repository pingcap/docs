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
```

## Options

- `--db-cluster-id <string>`: Starter DB cluster ID. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--help`: Display help information.
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Preview SQL user creation

```bash
tdc db create-db-sql-users --db-cluster-id "<cluster-id>" --dry-run
```

### Create read-only, read-write, and admin SQL users

```bash
tdc db create-db-sql-users --db-cluster-id "<cluster-id>"
```
