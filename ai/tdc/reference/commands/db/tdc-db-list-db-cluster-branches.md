---
title: tdc db list-db-cluster-branches
summary: List branches for a TiDB Cloud Starter cluster.
---

# tdc db list-db-cluster-branches

Lists branches for one Starter cluster, with optional pagination. The command verifies that the parent cluster is Starter before listing branches.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `tdc` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc db list-db-cluster-branches
  --db-cluster-id <string>
  [--help]
  [--page-size <int32>]
  [--page-token <string>]
  [--version]
```

## Options

- `--db-cluster-id <string>`: Starter DB cluster ID. \[required]
- `--help`: Display help information.
- `--page-size <int32>`: Number of branches to request; 0 uses the API default.
- `--page-token <string>`: Page token returned by a previous list-db-cluster-branches call.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

- List cluster branches:

    ```bash
    # Return all branches that belong to the selected Starter cluster.
    tdc db list-db-cluster-branches --db-cluster-id "<cluster-id>"
    ```

## Related documentation

- [TiDB Cloud Starter CLI Command Reference](/ai/tdc/reference/tdc-starter-database.md)
