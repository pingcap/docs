---
title: tdc db list-db-cluster-branches
summary: List branches for a TiDB Cloud Starter cluster.
---

# tdc db list-db-cluster-branches

Lists branches for one Starter cluster, with optional pagination.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc db list-db-cluster-branches
    --db-cluster-id <string>
    [--help]
    [--page-size <int32>]
    [--page-token <string>]
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
tdc db list-db-cluster-branches --db-cluster-id "<cluster-id>" --output text
tdc db list-db-cluster-branches --db-cluster-id "<cluster-id>" --query 'branches[].id'
```
