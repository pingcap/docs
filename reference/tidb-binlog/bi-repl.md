---
title: Bidirectional Replication Between TiDB Clusters
category: reference
---

# Bidirectional Replication Between TiDB Clusters

This document describes how to replicate the data of one TiDB cluster to another TiDB cluster, how the replication works, how to enable the bidirectional replication, and how to replicate DDL operations.

## User scenario

If you need to replicate data between two TiDB clusters, you can use TiDB Binlog for such operation. For example, to replicate the data of cluster A to cluster B, and replicate the data of cluster B to cluster A.

> **Note:**
>
> The data written to these two clusters is conflict-free, which means that the primary key or the rows of the unique index of the same table in the two cluster will not be modified.

The user scenario is shown as below:

![Architect](/media/binlog/bi-repl1.jpg)

## Implementations

![Mark Table](/media/binlog/bi-repl2.png)

If the bidirectional replication is enabled between cluster A and cluster B, the data written to cluster A will be replicated to cluster B, and then this part of written data will continue to be replicated back to cluster A, which will cause an infinite loop replication. From the figure above, you can see that during the data replication, Drainer marks the binlog, and filters out the marked binlog to avoid such loop replication. The detailed implementation process is described as follows:

1. Start the TiDB Binlog replication for each of the two clusters.
2. When the transaction to be replicated passes through the Drainer of cluster A, this Drainer adds the [`_drainer_repl_mark` table](#mark-table) to the transaction, writes this DML event update to the mark table, and replicate this transaction to cluster B.
3. Cluster B returns a binlog event with the `_drainer_repl_mark` mark table to cluster A. The Drainer of cluster B identifies the mark table with the DML event when parsing the binlog event, and give up replicating this binlog event to cluster A.

The replication process from cluster B to cluster A is the same as above. The two clusters can be upstream and downstream of each other.

> **Note:**
>
> * When updating the `_drainer_repl_mark` mark table, there must be data changes to generate binlogs.
> * DDL operations have nothing like transactions, so you need to use the one-way replication method to replicate DDL operations from one cluster to another. See [Replicate DDL operations](#replicate-ddl-operations) for detail.

Drainer can use a unique ID for each connection downstream to avoid conflicts. `channel_id` is used to indicate a channel for bidirectional replication. The two clusters should have the same configuration (with the same value) for bidirectional replication.

If you have added or deleted columns in the upstream, there might be more or fewer columns of the data to be replicated to the downstream. Drainer allows this situation by ignoring the added column values or by writing default values to the deleted columns.

## Mark table

The `_drainer_repl_mark` mark table has the following structure:

{{< copyable "sql" >}}

```sql
CREATE TABLE `_drainer_repl_mark` (
  `id` bigint(20) NOT NULL,
  `channel_id` bigint(20) NOT NULL DEFAULT '0',
  `val` bigint(20) DEFAULT '0',
  `channel_info` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`,`channel_id`)
);
```

Drainer use the following SQL statement to update `_drainer_repl_mark`, which ensures data change and the generation of binlog:

{{< copyable "sql" >}}

```sql
update drainer_repl_mark set val = val + 1 where id = ? && channel_id = ?;
```

## Replicate DDL operations

Because Drainer cannot add the mark table to DDL operations, you can only use the one-way replication method to replicate DDL operations.

DDL replication is enabled from cluster A to cluster B, and at the same time disabled from cluster B to cluster A. All DDL operations are performed on cluster A.

> **Note:**
>
> DDL operations cannot be executed on two clusters at the same time. When a DDL operation is executed, if there are DML operations at the same time or the DML binlog is not replicated, the upstream and downstream table structures of the DML replication might be inconsistent.

## Configure and enable bidirectional replication

For bidirectional replication between cluster A and cluster B, assume that the DDL operation is executed on cluster A. On the replication path from cluster A to cluster B, add the following configuration to Drainer:

{{< copyable "" >}}

```toml
[syncer]
loopback-control = true
channel-id = 1 # Configure the same ID for both clusters in this replication.
sync-ddl = true # DDL replication is needed.

[syncer.to]
# 1 means SyncFullColumn and 2 means SyncPartialColumn.
# If set to SyncPartialColumn, Drainer will allow the downstream table
# structure to have more or fewer columns than the data currently being replicated
# And remove the STRICT_TRANS_TABLES of the SQL mode to allow fewer columns, and insert zero values downstream.
sync-mode = 2

# Ignores the checkpoint table.
[[syncer.ignore-table]]
db-name = "tidb_binlog"
tbl-name = "checkpoint"
```

On the replication path from cluster B to cluster A, add the following configuration to Drainer:

{{< copyable "" >}}

```toml
[syncer]
loopback-control = true
channel-id = 1 # Configure the same ID for both clusters in this replication.
sync-ddl = false  # DDL replication is not needed.

[syncer.to]
# 1 means SyncFullColumn and 2 means SyncPartialColumn.
# If set to SyncPartialColumn, Drainer will allow the downstream table
# structure to have more or fewer columns than the data currently being replicated
# And remove the STRICT_TRANS_TABLES of the SQL mode to allow fewer columns, and insert zero values downstream.
sync-mode = 2

# Ignores the checkpoint table.
[[syncer.ignore-table]]
db-name = "tidb_binlog"
tbl-name = "checkpoint"
```
