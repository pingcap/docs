---
title: tdc db create-db-cluster
summary: Create a TiDB Cloud Starter cluster.
---

# tdc db create-db-cluster

Creates a Starter cluster. The required `--db-cluster-type` must be `starter`; there is no implicit type. `--wait` waits for the cluster to become `ACTIVE`. Project selection uses an explicit `--project-id`, then the configured virtual project, then the TiDB Cloud account default. The TiDB Cloud CLI validates the returned service plan; if verification fails after creation is accepted, it reports the cluster ID and retains the cluster for inspection.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `tdc` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc db create-db-cluster
  --db-cluster-name <string>
  --db-cluster-type <string>
  [--dry-run]
  [--help]
  [--monthly-spending-limit-usd-cents <int32>]
  [--project-id <string>]
  [--version]
  [--wait]
```

## Options

- `--db-cluster-name <string>`: Starter DB cluster display name. \[required]
- `--db-cluster-type <string>`: DB cluster type; must be `starter`. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--help`: Display help information.
- `--monthly-spending-limit-usd-cents <int32>`: Monthly spending limit in USD cents; omit to use the API default.
- `--project-id <string>`: TiDB Cloud project ID. Overrides the configured and account defaults.
- `--version`: Display version information.
- `--wait`: Wait until the created cluster becomes `ACTIVE` before returning.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

- Create a cluster and wait until it is active:

    ```bash
    # Wait until the new Starter cluster reaches the ACTIVE state.
    tdc db create-db-cluster --db-cluster-type starter --db-cluster-name app-db --wait
    ```

- Create a cluster asynchronously:

    ```bash
    # Return after TiDB Cloud accepts creation so another process can poll the cluster.
    tdc db create-db-cluster --db-cluster-type starter --db-cluster-name background-db
    ```

- Preview cluster creation:

    ```bash
    # Validate the request and resolved defaults without creating a cluster.
    tdc db create-db-cluster --db-cluster-type starter --db-cluster-name app-db --dry-run
    ```

- Create a cluster in an explicit project:

    ```bash
    # Override the configured virtual project for this cluster.
    tdc db create-db-cluster --db-cluster-type starter --db-cluster-name project-db --project-id "<project-id>" --wait
    ```

- Set a monthly spending limit:

    ```bash
    # Create a paid Starter cluster with a monthly limit expressed in US dollar cents.
    tdc db create-db-cluster --db-cluster-type starter --db-cluster-name production-db --monthly-spending-limit-usd-cents 1000 --wait
    ```

## Related documentation

- [TiDB Cloud Starter CLI Command Reference](/ai/tdc/reference/tdc-starter-database.md)
