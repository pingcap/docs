---
title: tdc db list-db-clusters
summary: List TiDB Cloud Starter clusters.
---

# tdc db list-db-clusters

Lists Starter clusters with optional pagination, filtering, ordering, and JMESPath projection.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc db list-db-clusters
    [--filter <string>]
    [--help]
    [--order-by <string>]
    [--page-size <int32>]
    [--page-token <string>]
    [--skip <int32>]
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
tdc db list-db-clusters --output text
tdc db list-db-clusters --query 'clusters[].{id:id,name:display_name,state:state}'
```
