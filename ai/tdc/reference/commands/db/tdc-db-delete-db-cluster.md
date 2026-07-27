---
title: tdc db delete-db-cluster
summary: Delete a TiDB Cloud Starter cluster.
---

# tdc db delete-db-cluster

Deletes one Starter cluster. `--wait` waits until deletion is observable.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `tdc` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc db delete-db-cluster
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

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

- Delete a cluster and wait for completion:

    ```bash
    # Wait until TiDB Cloud reports the cluster deleted or no longer accessible.
    tdc db delete-db-cluster --db-cluster-id "<cluster-id>" --wait
    ```

- Delete a cluster asynchronously:

    ```bash
    # Return after TiDB Cloud accepts deletion while cleanup continues remotely.
    tdc db delete-db-cluster --db-cluster-id "<cluster-id>"
    ```

## Related documentation

- [TiDB Cloud Starter CLI Command Reference](/ai/tdc/reference/tdc-starter-database.md)
