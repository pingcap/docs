---
title: ti db describe-db-cluster
summary: Describe a TiDB Cloud Starter cluster.
---

# ti db describe-db-cluster

Describes one Starter cluster. Use `--view FULL` to request expanded fields. The command rejects the cluster if its API metadata does not verify it as Starter.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

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
- `--view <string>`: Detail level: `BASIC` or `FULL`.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Describe a cluster:

    ```bash
    # Return the cluster state, placement, and connection metadata.
    ti db describe-db-cluster --db-cluster-id "<cluster-id>" --view FULL
    ```

## Related documentation

- [TiDB Cloud Starter CLI Command Reference](/ai/ti/reference/ti-starter-database.md)
