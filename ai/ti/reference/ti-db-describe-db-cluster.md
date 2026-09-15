---
title: ti db describe-db-cluster
summary: Describe a TiDB Cloud Starter cluster.
---

# ti db describe-db-cluster

Gets information about a TiDB Cloud Starter instance. The default `BASIC` view returns basic instance information. Use `--view FULL` to request the complete details available from the TiDB Cloud API. The command rejects the cluster if its API metadata does not verify it as Starter.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Syntax

```text
ti db describe-db-cluster
  --db-cluster-id <string>
  [--help]
  [--version]
  [--view <string>]
```

## Options

- `--db-cluster-id <string>`: Starter DB cluster ID. \[required]
- `--help`: Display help information.
- `--version`: Display version information.
- `--view <string>`: Detail level: `BASIC` or `FULL`. If omitted, the TiDB Cloud API uses `BASIC`.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Get information about a TiDB Cloud Starter instance:

    ```bash
    # Return the instance state, placement, and connection metadata.
    ti db describe-db-cluster --db-cluster-id "<cluster-id>" --view FULL
    ```

## Related documentation

- [TiDB Cloud Starter CLI Command Reference](/ai/ti/reference/ti-starter-database.md)
