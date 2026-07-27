---
title: tdc db describe-db-cluster
summary: Describe a TiDB Cloud Starter cluster.
---

# tdc db describe-db-cluster

Describes one Starter cluster. Use `--view FULL` to request expanded fields.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `tdc` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc db describe-db-cluster
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

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

- Describe a cluster:

    ```bash
    # Return the cluster state, placement, and connection metadata.
    tdc db describe-db-cluster --db-cluster-id "<cluster-id>" --view FULL
    ```

## Related documentation

- [TiDB Cloud Starter CLI Command Reference](/ai/tdc/reference/tdc-starter-database.md)
