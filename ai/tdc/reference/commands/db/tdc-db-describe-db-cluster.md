---
title: tdc db describe-db-cluster
summary: Describe a TiDB Cloud Starter cluster.
---

# tdc db describe-db-cluster

Describes one Starter cluster. Use `--view FULL` to request expanded fields.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc db describe-db-cluster
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
tdc db describe-db-cluster --db-cluster-id "<cluster-id>"
tdc db describe-db-cluster --db-cluster-id "<cluster-id>" --view FULL
```
