---
title: ti db create-db-cluster-branch
summary: Create a branch for a TiDB Cloud Starter cluster.
---

# ti db create-db-cluster-branch

Creates a branch for one Starter cluster. `--wait` waits for the branch to become `ACTIVE`. The command verifies that the parent cluster is Starter before creating the branch.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti db create-db-cluster-branch
  --db-cluster-branch-name <string>
  --db-cluster-id <string>
  [--dry-run]
  [--help]
  [--version]
  [--wait]
```

## Options

- `--db-cluster-branch-name <string>`: Starter DB cluster branch display name. \[required]
- `--db-cluster-id <string>`: Starter DB cluster ID. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--help`: Display help information.
- `--version`: Display version information.
- `--wait`: Wait until the created branch becomes `ACTIVE` before returning.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Create a branch and wait until it is active:

    ```bash
    # Wait until the new database branch can accept connections.
    ti db create-db-cluster-branch --db-cluster-id "<cluster-id>" --db-cluster-branch-name dev --wait
    ```

- Preview branch creation:

    ```bash
    # Validate the parent cluster and branch request without creating it.
    ti db create-db-cluster-branch --db-cluster-id "<cluster-id>" --db-cluster-branch-name preview --dry-run
    ```

## Related documentation

- [TiDB Cloud Starter CLI Command Reference](/ai/ti/reference/ti-starter-database.md)
