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
    [--debug]
    [--output <string>]
    [--profile <string>]
    [--query <string>]
    [--region <string>]
```

For global flags such as `--profile`, `--region`, `--output`, and `--query`, see [tdc CLI Reference](/ai/tdc/reference/tdc-cli-reference.md).

## Examples

```shell
tdc db create-db-cluster --db-cluster-name app-db --wait
tdc db create-db-cluster --db-cluster-name app-db --dry-run
```
