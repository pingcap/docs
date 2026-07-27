---
title: tdc db create-db-cluster
summary: Create a TiDB Cloud Starter cluster.
---

# tdc db create-db-cluster

Creates a Starter cluster. `--db-cluster-type` defaults to `starter`, and `--wait` waits for the cluster to become `ACTIVE`.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc db create-db-cluster
  --db-cluster-name <string>
  [--db-cluster-type <string>]
  [--dry-run]
  [--help]
  [--monthly-spending-limit-usd-cents <int32>]
  [--project-id <string>]
  [--version]
  [--wait]
```

## Options

- `--db-cluster-name <string>`: Starter DB cluster display name. \[required]
- `--db-cluster-type <string>`: DB cluster type; must be `starter`. \[default: starter]
- `--dry-run`: Validate the request without applying changes.
- `--help`: Display help information.
- `--monthly-spending-limit-usd-cents <int32>`: Monthly spending limit in USD cents; omit to use the API default.
- `--project-id <string>`: TiDB Cloud project ID.
- `--version`: Display tdc version information.
- `--wait`: Wait until the created cluster becomes `ACTIVE` before returning.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Create a cluster and wait until it is active

```bash
tdc db create-db-cluster --db-cluster-name app-db --wait
```

### Preview cluster creation

```bash
tdc db create-db-cluster --db-cluster-name app-db --dry-run
```
