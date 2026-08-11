---
title: ti db create-db-cluster
summary: Create a TiDB Cloud Starter cluster.
---

# ti db create-db-cluster

Creates a Starter cluster. The required `--db-cluster-type` must be `starter`; there is no implicit type. `--wait` waits for the cluster to become `ACTIVE`. The request omits project selection and lets TiDB Cloud select its server-side default project. The TiDB Cloud CLI validates the returned service plan; if verification fails after creation is accepted, it reports the cluster ID and retains the cluster for inspection.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti db create-db-cluster
  --db-cluster-name <string>
  --db-cluster-type <string>
  [--dry-run]
  [--help]
  [--monthly-spending-limit-usd-cents <int32>]
  [--version]
  [--wait]
```

## Options

- `--db-cluster-name <string>`: Starter DB cluster display name. \[required]
- `--db-cluster-type <string>`: DB cluster type; must be `starter`. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--help`: Display help information.
- `--monthly-spending-limit-usd-cents <int32>`: Monthly spending limit in USD cents; omit to use the API default.
- `--version`: Display version information.
- `--wait`: Wait until the created cluster becomes `ACTIVE` before returning.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Create a cluster and wait until it is active:

    ```bash
    # Wait until the new Starter cluster reaches the ACTIVE state.
    ti db create-db-cluster --db-cluster-type starter --db-cluster-name app-db --wait
    ```

- Create a cluster asynchronously:

    ```bash
    # Return after TiDB Cloud accepts creation so another process can poll the cluster.
    ti db create-db-cluster --db-cluster-type starter --db-cluster-name background-db
    ```

- Preview cluster creation:

    ```bash
    # Validate the request and resolved defaults without creating a cluster.
    ti db create-db-cluster --db-cluster-type starter --db-cluster-name app-db --dry-run
    ```

- Set a monthly spending limit:

    ```bash
    # Create a paid Starter cluster with a monthly limit expressed in US dollar cents.
    ti db create-db-cluster --db-cluster-type starter --db-cluster-name production-db --monthly-spending-limit-usd-cents 1000 --wait
    ```

## Related documentation

- [TiDB Cloud Starter CLI Command Reference](/ai/ti/reference/ti-starter-database.md)
