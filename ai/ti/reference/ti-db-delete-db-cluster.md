---
title: ti db delete-db-cluster
summary: Delete a TiDB Cloud Starter cluster.
---

# ti db delete-db-cluster

Deletes a TiDB Cloud Starter instance. Use `--wait` to wait until deletion completes. This command only accepts TiDB Cloud Starter instances and rejects other cluster types.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Syntax

```text
ti db delete-db-cluster
  --db-cluster-id <string>
  [--dry-run]
  [--help]
  [--version]
  [--wait]
```

## Options

- `--db-cluster-id <string>`: Starter DB cluster ID. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--help`: Display help information.
- `--version`: Display version information.
- `--wait`: After TiDB Cloud accepts the deletion request, poll until the instance reaches `DELETED`. A subsequent `not found` or `permission denied` response is also treated as completed deletion because the instance is no longer readable.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Delete a cluster and wait for completion:

    ```bash
    # Wait until TiDB Cloud reports the cluster deleted or no longer accessible.
    ti db delete-db-cluster --db-cluster-id "<cluster-id>" --wait
    ```

- Delete a cluster asynchronously:

    ```bash
    # Return after TiDB Cloud accepts deletion while cleanup continues remotely.
    ti db delete-db-cluster --db-cluster-id "<cluster-id>"
    ```

## Related documentation

- [TiDB Cloud Starter CLI Command Reference](/ai/ti/reference/ti-starter-database.md)
