---
title: tdc db update-db-cluster
summary: Update a TiDB Cloud Starter cluster.
---

# tdc db update-db-cluster

Updates the display name or monthly spending limit of one Starter cluster.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc db update-db-cluster
  --db-cluster-id <string>
  [--db-cluster-name <string>]
  [--dry-run]
  [--help]
  [--monthly-spending-limit-usd-cents <int32>]
  [--version]
```

## Options

- `--db-cluster-id <string>`: Starter DB cluster ID. \[required]
- `--db-cluster-name <string>`: New Starter DB cluster display name.
- `--dry-run`: Validate the request without applying changes.
- `--help`: Display help information.
- `--monthly-spending-limit-usd-cents <int32>`: Monthly spending limit in USD cents; omit to leave unchanged.
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Rename a cluster

```bash
tdc db update-db-cluster --db-cluster-id "<cluster-id>" --db-cluster-name app-db-v2
```

### Preview a spending-limit update

```bash
tdc db update-db-cluster --db-cluster-id "<cluster-id>" --monthly-spending-limit-usd-cents 1000 --dry-run
```
