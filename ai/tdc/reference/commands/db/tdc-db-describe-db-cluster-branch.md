---
title: tdc db describe-db-cluster-branch
summary: Describe a branch for a TiDB Cloud Starter cluster.
---

# tdc db describe-db-cluster-branch

Describes one branch by cluster ID and branch ID.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc db describe-db-cluster-branch
    --db-cluster-branch-id <string>
    --db-cluster-id <string>
    [--help]
    [--version]
    [--view <string>]
    [--debug]
    [--output <string>]
    [--profile <string>]
    [--query <string>]
    [--region <string>]
```

For global flags such as `--profile`, `--region`, `--output`, and `--query`, see [tdc CLI Reference](/ai/tdc/reference/tdc-cli-reference.md).

## Examples

```shell
tdc db describe-db-cluster-branch --db-cluster-id "<cluster-id>" --db-cluster-branch-id "<branch-id>"
tdc db describe-db-cluster-branch --db-cluster-id "<cluster-id>" --db-cluster-branch-id "<branch-id>" --view FULL
```
