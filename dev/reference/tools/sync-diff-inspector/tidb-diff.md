---
title: Data Check for TiDB Upstream and Downstream Clusters
summary: Learn how to check data for TiDB upstream and downstream clusters.
category: tools
---

# Data Check for TiDB Upstream and Downstream Clusters

You can use TiDB Binlog to build upstream and downstream clusters of TiDB. When Drainer replicates data to TiDB, saving the checkpoint also has the TSO mapping relationship between the upstream and downstream saved as `ts-map`. To check data between the upstream and downstream, configure `snapshot` in sync-diff-inspector.

## Step 1: obtain `ts-map`

To obtain `ts-map`, execute the following SQL statement in the downstream TiDB cluster:

```sql
mysql> select * from tidb_binlog.checkpoint;
+---------------------+---------------------------------------------------------------------------------------------------------+
| clusterID           | checkPoint                                                                                              |
+---------------------+---------------------------------------------------------------------------------------------------------+
| 6711243465327639221 | {"commitTS":409622383615541249,"ts-map":{"master-ts":409621863377928194,"slave-ts":409621863377928345}} |
+---------------------+---------------------------------------------------------------------------------------------------------+
```

## Step 2: configure snapshot

Configure the snapshot information of the upstream and downstream databases using the `ts-map` information obtained in the previous step.

```toml
######################### Databases config #########################

# Configuration of the instance in the source database
[[source-db]]
    host = "127.0.0.1"
    port = 4000
    user = "root"
    password = "123456"
    # The ID of the instance in the source database, the unique identifier of a database instance
    instance-id = "source-1"
    # Use the snapshot function of TiDB, corresponding to the master-ts in ts-map
    snapshot = "409621863377928194"

# Configuration of the instance in the target database
[target-db]
    host = "127.0.0.1"
    port = 4001
    user = "root"
    password = "123456"
    # Use the snapshot function of TiDB, corresponding to the slave-ts in ts-map
    snapshot = "409621863377928345"
```

> **Note:**
>
> - Set the `db-type` of Drainer to `tidb` to ensure that `ts-map` is saved in the checkpoint.
> - Modify the Garbage Collection (GC) time of TiKV to ensure that the historical data corresponding to snapshot is not collected by GC during the data check. It is recommended that you modify the GC time to 1 hour and recover the setting after the check.
