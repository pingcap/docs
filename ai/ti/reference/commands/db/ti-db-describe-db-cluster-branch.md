---
title: ti db describe-db-cluster-branch
summary: Describe a branch for a TiDB Cloud Starter cluster.
---

# ti db describe-db-cluster-branch

Describes one branch by cluster ID and branch ID. The command verifies that the parent cluster is Starter before reading the branch.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti db describe-db-cluster-branch
  --db-cluster-branch-id <string>
  --db-cluster-id <string>
  [--help]
  [--version]
  [--view <string>]
```

## Options

- `--db-cluster-branch-id <string>`: Starter DB cluster branch ID. \[required]
- `--db-cluster-id <string>`: Starter DB cluster ID. \[required]
- `--help`: Display help information.
- `--version`: Display version information.
- `--view <string>`: Detail level: `BASIC` or `FULL`.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Describe a branch:

    ```bash
    # Return full lifecycle and connection details for one branch.
    ti db describe-db-cluster-branch --db-cluster-id "<cluster-id>" --db-cluster-branch-id "<branch-id>" --view FULL
    ```

## Related documentation

- [TiDB Cloud Starter CLI Command Reference](/ai/ti/reference/ti-starter-database.md)
