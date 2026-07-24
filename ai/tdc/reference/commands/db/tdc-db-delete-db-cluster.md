---
title: tdc db delete-db-cluster
summary: Delete a TiDB Cloud Starter cluster.
---

# tdc db delete-db-cluster

Deletes one Starter cluster. `--wait` waits until deletion is observable.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc db delete-db-cluster
    --db-cluster-id <string>
    [--dry-run]
    [--help]
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
tdc db delete-db-cluster --db-cluster-id "<cluster-id>" --dry-run
tdc db delete-db-cluster --db-cluster-id "<cluster-id>" --wait
```
