---
title: ti db list-db-cluster-branches
summary: List branches for a TiDB Cloud Starter cluster.
---

# ti db list-db-cluster-branches

Lists branches for one TiDB Cloud Starter instance, with optional pagination. The command verifies that the parent cluster is Starter before listing branches.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Syntax

```text
ti db list-db-cluster-branches
  --db-cluster-id <string>
  [--help]
  [--page-size <int32>]
  [--page-token <string>]
  [--version]
```

## Options

- `--db-cluster-id <string>`: Starter DB cluster ID. \[required]
- `--help`: Display help information.
- `--page-size <int32>`: Number of branches to request. If omitted or set to `0`, the API returns at most `10`. The API maximum is `100`; values greater than `100` are set to `100`.
- `--page-token <string>`: Page token returned by a previous list-db-cluster-branches call.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- List cluster branches:

    ```bash
    # Return all branches that belong to the selected TiDB Cloud Starter instance.
    ti db list-db-cluster-branches --db-cluster-id "<cluster-id>"
    ```

## Related documentation

- [TiDB Cloud Starter CLI Command Reference](/ai/ti/reference/ti-starter-database.md)
