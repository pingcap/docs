---
title: tdc db create-db-cluster-branch
summary: Create a branch for a TiDB Cloud Starter cluster.
---

# tdc db create-db-cluster-branch

Creates a branch for one Starter cluster. `--wait` waits for the branch to become `ACTIVE`.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc db create-db-cluster-branch
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
- `--version`: Display tdc version information.
- `--wait`: Wait until the created branch becomes `ACTIVE` before returning.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Create a branch and wait until it is active

```bash
tdc db create-db-cluster-branch --db-cluster-id "<cluster-id>" --db-cluster-branch-name dev --wait
```

### Preview branch creation

```bash
tdc db create-db-cluster-branch --db-cluster-id "<cluster-id>" --db-cluster-branch-name preview --dry-run
```
