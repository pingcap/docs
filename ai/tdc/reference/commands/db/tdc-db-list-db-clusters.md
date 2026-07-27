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
```

## Options

- `--filter <string>`: Starter API filter expression.
- `--help`: Display help information.
- `--order-by <string>`: Starter API orderBy expression.
- `--page-size <int32>`: Number of clusters to request; 0 uses the API default.
- `--page-token <string>`: Page token returned by a previous list-db-clusters call.
- `--skip <int32>`: Number of clusters to skip.
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### List clusters as text

```bash
tdc db list-db-clusters --output text
```

### Return selected cluster fields

```bash
tdc db list-db-clusters --query 'clusters[].{id:id,name:display_name,state:state}'
```
