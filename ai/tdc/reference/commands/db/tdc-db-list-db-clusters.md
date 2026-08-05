---
title: tdc db list-db-clusters
summary: List TiDB Cloud Starter clusters.
---

# tdc db list-db-clusters

Lists verified Starter clusters in the effective region with optional pagination, filtering, ordering, and JMESPath projection. Cross-region, non-Starter, and unverifiable clusters are omitted. The command preserves `next_page_token` after filtering and omits the server `total_size`, which can include resources outside the verified result.

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
    # Return Starter clusters in the profile's configured region as structured JSON.
    tdc db list-db-clusters
    ```

- List clusters in another region:

    ```bash
    # Override the region for this invocation without changing the profile.
    tdc --region aws-us-west-2 db list-db-clusters
    ```

- Select cluster fields:

    ```bash
    # Reduce the result to IDs, names, and lifecycle states.
    tdc db list-db-clusters --query 'clusters[].{id:id,name:display_name,state:state}'
    ```

The effective region resolves from global `--region`, then `TDC_REGION_CODE`, then the selected profile's `region_code`. User-supplied `--filter` expressions are combined with this mandatory region scope and cannot expand the result to other regions.

## Related documentation

- [TiDB Cloud Starter CLI Command Reference](/ai/tdc/reference/tdc-starter-database.md)
