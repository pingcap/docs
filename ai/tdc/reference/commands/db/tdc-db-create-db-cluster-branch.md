---
title: tdc db create-db-cluster-branch
summary: Create a branch for a TiDB Cloud Starter cluster.
---

# tdc db create-db-cluster-branch

Creates a branch for one Starter cluster. `--wait` waits for the branch to become `ACTIVE`.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc db create-db-cluster-branch
    --db-cluster-branch-name <string>
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
tdc db create-db-cluster-branch --db-cluster-id "<cluster-id>" --db-cluster-branch-name dev --wait
tdc db create-db-cluster-branch --db-cluster-id "<cluster-id>" --db-cluster-branch-name preview --dry-run
```
