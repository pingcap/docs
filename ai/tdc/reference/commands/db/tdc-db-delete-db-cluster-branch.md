---
title: tdc db delete-db-cluster-branch
summary: Delete a branch from a TiDB Cloud Starter cluster.
---

# tdc db delete-db-cluster-branch

Deletes one branch from a Starter cluster.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc db delete-db-cluster-branch
    --db-cluster-branch-id <string>
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
tdc db delete-db-cluster-branch --db-cluster-id "<cluster-id>" --db-cluster-branch-id "<branch-id>" --dry-run
tdc db delete-db-cluster-branch --db-cluster-id "<cluster-id>" --db-cluster-branch-id "<branch-id>"
```
