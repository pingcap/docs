---
title: tdc db delete-db-cluster-branch
summary: Delete a branch from a TiDB Cloud Starter cluster.
---

# tdc db delete-db-cluster-branch

Deletes one branch from a Starter cluster.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc db delete-db-cluster-branch
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
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Preview branch deletion

```bash
tdc db delete-db-cluster-branch --db-cluster-id "<cluster-id>" --db-cluster-branch-id "<branch-id>" --dry-run
```

### Delete a branch

```bash
tdc db delete-db-cluster-branch --db-cluster-id "<cluster-id>" --db-cluster-branch-id "<branch-id>"
```
