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
    [--debug]
    [--output <string>]
    [--profile <string>]
    [--query <string>]
    [--region <string>]
```

For global flags such as `--profile`, `--region`, `--output`, and `--query`, see [tdc CLI Reference](/ai/tdc/reference/tdc-cli-reference.md).

## Examples

```shell
tdc db update-db-cluster --db-cluster-id "<cluster-id>" --db-cluster-name app-db-v2
tdc db update-db-cluster --db-cluster-id "<cluster-id>" --monthly-spending-limit-usd-cents 1000 --dry-run
```
