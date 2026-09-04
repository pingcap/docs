---
title: ti db list-db-clusters
summary: List TiDB Cloud Starter clusters.
---

# ti db list-db-clusters

Lists verified Starter clusters in the effective region with pagination, filtering, ordering, and JMESPath projection. The required `--db-cluster-type` must be `starter`. Cross-region, non-Starter, and unverifiable clusters are omitted. The command incrementally fills each result page from TiDB Cloud API pages and returns an opaque ti `next_page_token`; it omits the server `total_size`, which can include resources outside the verified result.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti db list-db-clusters
  --db-cluster-type <string>
  [--filter <string>]
  [--help]
  [--order-by <string>]
  [--page-size <int32>]
  [--page-token <string>]
  [--version]
```

## Options

- `--db-cluster-type <string>`: DB cluster type; must be `starter`. \[required]
- `--filter <string>`: Starter API filter expression.
- `--help`: Display help information.
- `--order-by <string>`: Starter API orderBy expression.
- `--page-size <int32>`: Number of verified clusters to return; 0 returns 10 and the maximum is 1000.
- `--page-token <string>`: Opaque ti page token returned by a previous compatible list-db-clusters call.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- List clusters:

    ```bash
    # Return Starter clusters in the profile's configured region as structured JSON.
    ti db list-db-clusters --db-cluster-type starter
    ```

- List clusters in another region:

    ```bash
    # Override the region for this invocation without changing the profile.
    ti --region aws-us-west-2 db list-db-clusters --db-cluster-type starter
    ```

- Select cluster fields:

    ```bash
    # Reduce the result to IDs, names, and lifecycle states.
    ti db list-db-clusters --db-cluster-type starter --query 'clusters[].{id:id,name:display_name,state:state}'
    ```

The effective region resolves from global `--region`, then `TI_REGION_CODE`, then the selected profile's `region_code`. User-supplied `--filter` expressions are combined with this mandatory region scope and cannot expand the result to other regions. A page token can be reused only with the same profile, cluster type, region, filter, and ordering. If its replay page changed, restart the listing without `--page-token`.

## Related documentation

- [TiDB Cloud Starter CLI Command Reference](/ai/ti/reference/ti-starter-database.md)
