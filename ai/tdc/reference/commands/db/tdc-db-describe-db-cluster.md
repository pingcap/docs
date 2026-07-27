---
title: tdc db describe-db-cluster
summary: Describe a TiDB Cloud Starter cluster.
---

# tdc db describe-db-cluster

Describes one Starter cluster. Use `--view FULL` to request expanded fields.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

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
- `--version`: Display tdc version information.
- `--view <string>`: Detail level: `BASIC` or `FULL`.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Describe a cluster

```bash
tdc db describe-db-cluster --db-cluster-id "<cluster-id>"
```

### Show full cluster details

```bash
tdc db describe-db-cluster --db-cluster-id "<cluster-id>" --view FULL
```
