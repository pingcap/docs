---
title: ti db delete-db-cluster-branch
summary: Delete a branch from a TiDB Cloud Starter cluster.
---

# ti db delete-db-cluster-branch

Deletes one branch from a TiDB Cloud Starter instance. The command verifies that the parent cluster is Starter before reading or deleting the branch. It returns the delete response without polling; this command does not provide a `--wait` option.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Syntax

```text
ti db delete-db-cluster-branch
  --db-cluster-branch-id <string>
  --db-cluster-id <string>
  [--dry-run]
  [--help]
  [--version]
```

## Options

- `--db-cluster-branch-id <string>`: Starter DB cluster branch ID. \[required]
- `--db-cluster-id <string>`: Starter DB cluster ID. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Delete a branch:

    ```bash
    # Delete only the selected branch from its parent TiDB Cloud Starter instance.
    ti db delete-db-cluster-branch --db-cluster-id "<cluster-id>" --db-cluster-branch-id "<branch-id>"
    ```

To verify that the branch no longer appears, run `ti db list-db-cluster-branches --db-cluster-id "<cluster-id>"`.

## Related documentation

- [TiDB Cloud Starter CLI Command Reference](/ai/ti/reference/ti-starter-database.md)
