---
title: ti db create-db-cluster
summary: Create a TiDB Cloud Starter cluster.
---

# ti db create-db-cluster

Creates a TiDB Cloud Starter instance. The required `--db-cluster-type` must be `starter`; there is no implicit type. `--wait` waits for the cluster to become `ACTIVE`.

The request does not select a project. TiDB Cloud assigns the instance according to its server-side project rules, and `ti` preserves any project metadata in the response. You cannot select or configure a project through `ti`.

The TiDB Cloud CLI validates the returned service plan. If verification fails after creation is accepted, `ti` reports the cluster ID and retains the instance for inspection.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

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
- `--monthly-spending-limit-usd-cents <int32>`: Monthly spending limit in USD cents. If omitted, `ti` does not send a spending limit, and TiDB Cloud applies its default rules. For details, see [Manage Spending Limit for TiDB Cloud Starter Instances](/tidb-cloud/manage-serverless-spend-limit.md).
- `--version`: Display version information.
- `--wait`: Wait until the created cluster becomes `ACTIVE` before returning.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Create a cluster and wait until it is active:

    ```bash
    # Wait until the new TiDB Cloud Starter instance reaches the ACTIVE state.
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
    # Create a paid TiDB Cloud Starter instance with a monthly limit expressed in US dollar cents.
    ti db create-db-cluster --db-cluster-type starter --db-cluster-name production-db --monthly-spending-limit-usd-cents 1000 --wait
    ```

## If post-creation verification fails

If TiDB Cloud accepts the creation request but `ti` cannot verify the returned resource as a Starter instance, note the cluster ID in the error. Inspect the retained resource with:

```bash
ti db describe-db-cluster --db-cluster-id "<cluster-id>"
```

If `ti` still cannot verify the service plan, inspect or delete the resource in the TiDB Cloud console. Do not repeat the create command until you determine whether the first request created an instance.

## Related documentation

- [TiDB Cloud Starter CLI Command Reference](/ai/ti/reference/ti-starter-database.md)
