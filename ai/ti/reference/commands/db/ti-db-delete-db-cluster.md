---
title: ti db delete-db-cluster
summary: Delete a TiDB Cloud Starter cluster.
---

# ti db delete-db-cluster

Deletes one Starter cluster. `--wait` waits until deletion is observable. The command verifies the service plan before sending the delete request and rejects non-Starter or unverifiable clusters without sending `DELETE`.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

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
- `--wait`: Wait until the deleted cluster reaches `DELETED` or is no longer accessible.

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
