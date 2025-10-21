---
title: Create TiFlash Replicas
summary: Learn how to create TiFlash replicas.
---

# Create TiFlash Replicas

This document introduces how to create TiFlash replicas for tables and for databases, and set available zones for replica scheduling.

## Create TiFlash replicas for tables

After TiFlash is connected to the TiKV cluster, data replication by default does not begin. You can send a DDL statement to TiDB through a MySQL client to create a TiFlash replica for a specific table:

```sql
ALTER TABLE table_name SET TIFLASH REPLICA count;
```

The parameter of the above command is described as follows:

- `count` indicates the number of replicas. When the value is `0`, the replica is deleted.

> **Note:**
>
> For a [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) cluster, the `count` of TiFlash replicas can only be `2`. If you set it to `1`, it will be automatically adjusted to `2` for execution. If you set it to a number larger than 2, you will get an error about the replica count.

If you execute multiple DDL statements on the same table, only the last statement is ensured to take effect. In the following example, two DDL statements are executed on the table `tpch50`, but only the second statement (to delete the replica) takes effect.

Create two replicas for the table:

```sql
ALTER TABLE `tpch50`.`lineitem` SET TIFLASH REPLICA 2;
```

Delete the replica:

```sql
ALTER TABLE `tpch50`.`lineitem` SET TIFLASH REPLICA 0;
```

**Notes:**

* If the table `t` is replicated to TiFlash through the above DDL statements, the table created using the following statement will also be automatically replicated to TiFlash:

    ```sql
    CREATE TABLE table_name like t;
    ```

* For versions earlier than v4.0.6, if you create the TiFlash replica before using TiDB Lightning to import the data, the data import will fail. You must import data to the table before creating the TiFlash replica for the table.

* If TiDB and TiDB Lightning are both v4.0.6 or later, no matter a table has TiFlash replica(s) or not, you can import data to that table using TiDB Lightning. Note that this might slow the TiDB Lightning procedure, which depends on the NIC bandwidth on the lightning host, the CPU and disk load of the TiFlash node, and the number of TiFlash replicas.

* It is recommended that you do not replicate more than 1,000 tables because this lowers the PD scheduling performance. This limit will be removed in later versions.

* In v5.1 and later versions, setting the replicas for the system tables is no longer supported. Before upgrading the cluster, you need to clear the replicas of the relevant system tables. Otherwise, you cannot modify the replica settings of the system tables after you upgrade the cluster to a later version.

* Currently, when you use TiCDC to replicate tables to a downstream TiDB cluster, creating TiFlash replicas for the tables is not supported, which means that TiCDC does not support replicating TiFlash-related DDL statements, such as:

    * `ALTER TABLE table_name SET TIFLASH REPLICA count;`
    * `ALTER DATABASE db_name SET TIFLASH REPLICA count;`

### Check replication progress

You can check the status of the TiFlash replicas of a specific table using the following statement. The table is specified using the `WHERE` clause. If you remove the `WHERE` clause, you will check the replica status of all tables.

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>' and TABLE_NAME = '<table_name>';
```

In the result of above statement:

* `AVAILABLE` indicates whether the TiFlash replicas of this table are available or not. `1` means available and `0` means unavailable. Once the replicas become available, this status does not change. If you use DDL statements to modify the number of replicas, the replication status will be recalculated.
* `PROGRESS` means the progress of the replication. The value is between `0.0` and `1.0`. `1` means at least one replica is replicated.

## Create TiFlash replicas for databases

Similar to creating TiFlash replicas for tables, you can send a DDL statement to TiDB through a MySQL client to create a TiFlash replica for all tables in a specific database:

```sql
ALTER DATABASE db_name SET TIFLASH REPLICA count;
```

In this statement, `count` indicates the number of replicas. When you set it to `0`, replicas are deleted.

Examples:

- Create two replicas for all tables in the database `tpch50`:

    ```sql
    ALTER DATABASE `tpch50` SET TIFLASH REPLICA 2;
    ```

- Delete TiFlash replicas created for the database `tpch50`:

    ```sql
    ALTER DATABASE `tpch50` SET TIFLASH REPLICA 0;
    ```

> **Note:**
>
> - This statement actually performs a series of DDL operations, which are resource-intensive. If the statement is interrupted during the execution, executed operations are not rolled back and unexecuted operations do not continue.
>
> - After executing the statement, do not set the number of TiFlash replicas or perform DDL operations on this database until **all tables in this database are replicated**. Otherwise, unexpected results might occur, which include:
>     - If you set the number of TiFlash replicas to 2 and then change the number to 1 before all tables in the database are replicated, the final number of TiFlash replicas of all the tables is not necessarily 1 or 2.
>     - After executing the statement, if you create tables in this database before the completion of the statement execution, TiFlash replicas **might or might not** be created for these new tables.
>     - After executing the statement, if you add indexes for tables in the database before the completion of the statement execution, the statement might hang and resume only after the indexes are added.
>
> - If you create tables in this database **after** the completion of the statement execution, TiFlash replicas are not created automatically for these new tables.
>
> - This statement skips system tables, views, temporary tables, and tables with character sets not supported by TiFlash.

> - You can control the number of tables allowed to remain unavailable during execution by setting the [`tidb_batch_pending_tiflash_count`](/system-variables.md#tidb_batch_pending_tiflash_count-new-in-v60) system variable. Lowering this value helps reduce the pressure on the cluster during replication. Note that this limit is not real-time, so it is still possible for the number of unavailable tables to exceed the limit after the setting is applied.

### Check replication progress

Similar to creating TiFlash replicas for tables, successful execution of the DDL statement does not mean the completion of replication. You can execute the following SQL statement to check the progress of replication on target tables:

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>';
```

To check tables without TiFlash replicas in the database, you can execute the following SQL statement:

```sql
SELECT TABLE_NAME FROM information_schema.tables where TABLE_SCHEMA = "<db_name>" and TABLE_NAME not in (SELECT TABLE_NAME FROM information_schema.tiflash_replica where TABLE_SCHEMA = "<db_name>");
```

## Speed up TiFlash replication

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This section is not applicable to TiDB Cloud.

</CustomContent>

The TiDB cluster triggers the TiFlash replica replication process when you perform any of the following operations:

* Add TiFlash replicas for a table.
* Add a new TiFlash instance, causing PD to schedule the TiFlash replicas from original instances to the new TiFlash instance.

During this process, each TiKV instance performs a full table scan and sends a snapshot of the scanned data to TiFlash to create the replica. By default, to minimize the impact on TiKV and TiFlash production workloads, TiFlash adds replicas at a slower rate and uses fewer resources. If your TiKV and TiFlash nodes have sufficient CPU and disk I/O resources, you can accelerate TiFlash replication by performing the following steps.

1. Temporarily increase the snapshot write speed limit for each TiKV and TiFlash instance by using the [Dynamic Config SQL statement](https://docs.pingcap.com/tidb/stable/dynamic-config):

    ```sql
    -- The default value for both configurations are 100MiB, i.e. the maximum disk bandwidth used for writing snapshots is no more than 100MiB/s.
    SET CONFIG tikv `server.snap-io-max-bytes-per-sec` = '300MiB';
    SET CONFIG tiflash `raftstore-proxy.server.snap-io-max-bytes-per-sec` = '300MiB';
    ```

    After executing these SQL statements, the configuration changes take effect immediately without restarting the cluster. However, since the replication speed is still restricted by the PD limit globally, you cannot observe the acceleration for now.

2. Use [PD Control](https://docs.pingcap.com/tidb/stable/pd-control) to progressively ease the replica scheduling speed limit.

    The default new replica speed limit is 30, which means approximately 30 Regions add or remove TiFlash replicas on one TiFlash instance every minute. Executing the following command will adjust the limit to 60 for all TiFlash instances, which doubles the original speed:

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 60 add-peer
    ```

    > In the preceding command, you need to replace `v<CLUSTER_VERSION>` with the actual cluster version, such as `v8.5.0` and `<PD_ADDRESS>:2379` with the address of any PD node. For example:
    >
    > ```shell
    > tiup ctl:v8.5.0 pd -u http://192.168.1.4:2379 store limit all engine tiflash 60 add-peer
    > ```

    If the cluster contains many Regions on the old TiFlash nodes, PD needs to rebalance them to the new TiFlash nodes. You need to adjust the `remove-peer` limit accordingly.

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 60 remove-peer
    ```

    Within a few minutes, you will observe a significant increase in CPU and disk IO resource usage of the TiFlash nodes, and TiFlash creates replicas faster. At the same time, the TiKV nodes' CPU and disk IO resource usage increases as well.

    If the TiKV and TiFlash nodes still have spare resources at this point and the latency of your online service does not increase significantly, you can further ease the limit, for example, triple the original speed:

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 90 add-peer
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 90 remove-peer
    ```

3. After the TiFlash replication is complete, revert to the default configuration to reduce the impact on online services.

    Execute the following PD Control command to restore the default replica scheduling speed limit:

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 30 add-peer
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 30 remove-peer
    ```

    Execute the following SQL statements to restore the default snapshot write speed limit:

    ```sql
    SET CONFIG tikv `server.snap-io-max-bytes-per-sec` = '100MiB';
    SET CONFIG tiflash `raftstore-proxy.server.snap-io-max-bytes-per-sec` = '100MiB';
    ```

## Set available zones

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This section is not applicable to TiDB Cloud.

</CustomContent>

When configuring replicas, if you need to distribute TiFlash replicas to multiple data centers for disaster recovery, you can configure available zones by following the steps below:

1. Specify labels for TiFlash nodes in the cluster configuration file.

    ```
    tiflash_servers:
      - host: 172.16.5.81
          logger.level: "info"
        learner_config:
          server.labels:
            zone: "z1"
      - host: 172.16.5.82
        config:
          logger.level: "info"
        learner_config:
          server.labels:
            zone: "z1"
      - host: 172.16.5.85
        config:
          logger.level: "info"
        learner_config:
          server.labels:
            zone: "z2"
    ```

    Note that the `flash.proxy.labels` configuration in earlier versions cannot handle special characters in the available zone name correctly. It is recommended to use the `server.labels` in `learner_config` to configure the name of an available zone.

2. After starting a cluster, specify the number of TiFlash replicas for high availability. The syntax is as follows:

    ```sql
    ALTER TABLE table_name SET TIFLASH REPLICA count;
    ```

    For example:

    ```sql
    ALTER TABLE t SET TIFLASH REPLICA 2;
    ```

3. PD schedules the replicas of the table `t` to different availability zones based on the `server.labels` in the TiFlash node's `learner_config` and the number (`count`) of the table's replicas, ensuring availability. For more information, see [Schedule Replicas by Topology Labels](https://docs.pingcap.com/tidb/stable/schedule-replicas-by-topology-labels/). You can use the following SQL statement to verify the distribution of a table's Regions across TiFlash nodes:

    ```sql
    -- Non-partitioned table
    SELECT table_id, p.store_id, address, COUNT(p.region_id) 
    FROM
      information_schema.tikv_region_status r,
      information_schema.tikv_region_peers p,
      information_schema.tikv_store_status s
    WHERE
      r.db_name = 'test' 
      AND r.table_name = 'table_to_check'
      AND r.region_id = p.region_id 
      AND p.store_id = s.store_id
      AND JSON_EXTRACT(s.label, '$[0].value') = 'tiflash'
    GROUP BY table_id, p.store_id, address;

    -- Partitioned table
    SELECT table_id, r.partition_name, p.store_id, address, COUNT(p.region_id)
    FROM
      information_schema.tikv_region_status r,
      information_schema.tikv_region_peers p,
      information_schema.tikv_store_status s
    WHERE 
      r.db_name = 'test' 
      AND r.table_name = 'table_to_check' 
      AND r.partition_name LIKE 'p202312%'
      AND r.region_id = p.region_id 
      AND p.store_id = s.store_id
      AND JSON_EXTRACT(s.label, '$[0].value') = 'tiflash'
    GROUP BY table_id, r.partition_name, p.store_id, address
    ORDER BY table_id, r.partition_name, p.store_id;
    ```

<CustomContent platform="tidb">

For more information about scheduling replicas by using labels, see [Schedule Replicas by Topology Labels](/schedule-replicas-by-topology-labels.md), [Multiple Data Centers in One City Deployment](/multi-data-centers-in-one-city-deployment.md), and [Three Data Centers in Two Cities Deployment](/three-data-centers-in-two-cities-deployment.md).

TiFlash supports configuring the replica selection strategy for different zones. For more information, see [`tiflash_replica_read`](/system-variables.md#tiflash_replica_read-new-in-v730).

</CustomContent>

> **Note:**
>
> In the syntax `ALTER TABLE table_name SET TIFLASH REPLICA count LOCATION LABELS location_labels;`, if you specify multiple labels for `location_labels`, TiDB cannot parse them correctly to set placement rules. Therefore, do not use `LOCATION LABELS` to configure TiFlash replicas.
