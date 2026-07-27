---
title: tdc db list-db-clusters
summary: List TiDB Cloud Starter clusters.
---

# tdc db list-db-clusters

Lists Starter clusters with optional pagination, filtering, ordering, and JMESPath projection.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `tdc` — is currently in preview. Its features and command-line interface might change without prior notice.

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
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

- List clusters:

    ```bash
    # Return all visible Starter clusters as structured JSON.
    tdc db list-db-clusters
    ```

- Select cluster fields:

    ```bash
    # Reduce the result to IDs, names, and lifecycle states.
    tdc db list-db-clusters --query 'clusters[].{id:id,name:display_name,state:state}'
    ```

## Related documentation

- [TiDB Cloud Starter CLI Command Reference](/ai/tdc/reference/tdc-starter-database.md)
