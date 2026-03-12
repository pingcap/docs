---
title: Cluster Key
---

This page provides a comprehensive overview of cluster key operations in Databend, organized by functionality for easy reference.

## Cluster Key Management

| Command | Description |
|---------|-------------|
| [SET CLUSTER KEY](dml-set-cluster-key.md) | Creates or replaces a cluster key for a table |
| [ALTER CLUSTER KEY](dml-alter-cluster-key.md) | Modifies an existing cluster key |
| [DROP CLUSTER KEY](dml-drop-cluster-key.md) | Removes a cluster key from a table |
| [RECLUSTER TABLE](dml-recluster-table.md) | Reorganizes table data based on the cluster key |

## Related Topics

- [Cluster Key](/guides/performance/cluster-key)

:::note
Cluster keys in Databend are used to physically organize data in tables to improve query performance by co-locating related data.
:::