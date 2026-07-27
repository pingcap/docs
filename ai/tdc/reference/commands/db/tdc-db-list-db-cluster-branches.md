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
```

## Options

- `--db-cluster-id <string>`: Starter DB cluster ID. \[required]
- `--help`: Display help information.
- `--page-size <int32>`: Number of branches to request; 0 uses the API default.
- `--page-token <string>`: Page token returned by a previous list-db-cluster-branches call.
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### List branches as text

```bash
tdc db list-db-cluster-branches --db-cluster-id "<cluster-id>" --output text
```

### Return branch IDs

```bash
tdc db list-db-cluster-branches --db-cluster-id "<cluster-id>" --query 'branches[].id'
```
