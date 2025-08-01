---
title: Troubleshoot a TiFlash Cluster
summary: Learn common operations when you troubleshoot a TiFlash cluster.
---

# Troubleshoot a TiFlash Cluster

This section describes some commonly encountered issues when using TiFlash, the reasons, and the solutions.

## TiFlash fails to start

TiFlash might fail to start properly due to various reasons. You can troubleshoot the issue step by step using the following approach:

1. Check whether your system is CentOS 8.

    CentOS 8 does not include the `libnsl.so` system library by default, which might cause TiFlash to fail to start. You can install it manually using the following command:

    ```shell
    dnf install libnsl
    ```

2. Check your system's `ulimit` parameter setting.

    ```shell
    ulimit -n 1000000
    ```

3. Use the PD Control tool to check whether there is any TiFlash instance that failed to go offline on the node (same IP and Port) and force the instance(s) to go offline. For detailed steps, refer to [Scale in a TiFlash cluster](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster).

4. Check whether the CPU supports SIMD instructions.

    Starting from v6.3, deploying TiFlash on Linux AMD64 architecture requires a CPU that supports the AVX2 instruction set. Verify this by ensuring that `grep avx2 /proc/cpuinfo` produces output. For Linux ARM64 architecture, the CPU must support the ARMv8 instruction set architecture. Verify this by ensuring that `grep 'crc32' /proc/cpuinfo | grep 'asimd'` produces output.

    If you encounter this issue when deploying on a virtual machine, try changing the VM's CPU architecture to Haswell and then redeploy TiFlash.

If the preceding methods cannot resolve your issue, collect the TiFlash log files and [get support](/support.md) from PingCAP or the community.

## Some queries return the `Region Unavailable` error

If the workload on TiFlash is too heavy and it causes that TiFlash data replication falls behind, some queries might return the `Region Unavailable` error.

In this case, you can balance the workload by [adding more TiFlash nodes](/scale-tidb-using-tiup.md#scale-out-a-tiflash-cluster).

## Data file corruption

To handle data file corruption, follow these steps:

1. Refer to [Take a TiFlash node down](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster) to take the corresponding TiFlash node down.
2. Delete the related data of the TiFlash node.
3. Redeploy the TiFlash node in the cluster.

## Removing TiFlash nodes is slow

To address this issue, follow these steps:

1. Check whether any table has more TiFlash replicas than the number of TiFlash nodes available after the cluster scale-in:

    ```sql
    SELECT * FROM information_schema.tiflash_replica WHERE REPLICA_COUNT > 'tobe_left_nodes';
    ```

    `tobe_left_nodes` is the number of TiFlash nodes after the scale-in.

    If the query result is not empty, you need to modify the number of TiFlash replicas for the corresponding tables. This is because, when the number of TiFlash replicas exceeds the number of TiFlash nodes after the scale-in, PD will not move Region peers away from the TiFlash nodes to be removed, causing the removal of these TiFlash nodes to fail.

2. In scenarios where all TiFlash nodes need to be removed from a cluster, if the `INFORMATION_SCHEMA.TIFLASH_REPLICA` table shows that there are no TiFlash replicas in the cluster but removing TiFlash nodes still fails, check whether you have recently executed `DROP TABLE <db-name>.<table-name>` or `DROP DATABASE <db-name>` operations.

    For tables or databases with TiFlash replicas, after executing `DROP TABLE <db-name>.<table-name>` or `DROP DATABASE <db-name>`, TiDB does not immediately delete the TiFlash replication rules for the corresponding tables in PD. Instead, it waits until the corresponding tables meet the garbage collection (GC) conditions before deleting these replication rules. After GC is complete, the corresponding TiFlash nodes can be successfully removed.

    To remove data replication rules of TiFlash manually before the GC conditions are met, you can do the following:

    > **Note:**
    >
    > After manually removing TiFlash replication rules for a table, if you perform `RECOVER TABLE`, `FLASHBACK TABLE`, or `FLASHBACK DATABASE` operations on this table, the TiFlash replicas of this table will not be restored.

    1. View all data replication rules related to TiFlash in the current PD instance:

        ```shell
        curl http://<pd_ip>:<pd_port>/pd/api/v1/config/rules/group/tiflash
        ```

        ```
        [
          {
            "group_id": "tiflash",
            "id": "table-45-r",
            "override": true,
            "start_key": "7480000000000000FF2D5F720000000000FA",
            "end_key": "7480000000000000FF2E00000000000000F8",
            "role": "learner",
            "count": 1,
            "label_constraints": [
              {
                "key": "engine",
                "op": "in",
                "values": [
                  "tiflash"
                ]
              }
            ]
          }
        ]
        ```

    2. Remove all data replication rules related to TiFlash. Take the rule whose `id` is `table-45-r` as an example. Delete it by the following command:

        ```shell
        curl -v -X DELETE http://<pd_ip>:<pd_port>/pd/api/v1/config/rule/tiflash/table-45-r
        ```

## TiFlash analysis is slow

If a statement contains operators or functions not supported in the MPP mode, TiDB does not select the MPP mode. Therefore, the analysis of the statement is slow. In this case, you can execute the `EXPLAIN` statement to check for operators or functions not supported in the MPP mode.

```sql
create table t(a datetime);
alter table t set tiflash replica 1;
insert into t values('2022-01-13');
set @@session.tidb_enforce_mpp=1;
explain select count(*) from t where subtime(a, '12:00:00') > '2022-01-01' group by a;
show warnings;
```

In this example, the warning message shows that TiDB does not select the MPP mode because TiDB 5.4 and earlier versions do not support the `subtime` function.

```
+---------+------+-----------------------------------------------------------------------------+
| Level   | Code | Message                                                                     |
+---------+------+-----------------------------------------------------------------------------+
| Warning | 1105 | Scalar function 'subtime'(signature: SubDatetimeAndString, return type: datetime) is not supported to push down to tiflash now.       |
+---------+------+-----------------------------------------------------------------------------+
```

## TiFlash replica is always unavailable

After the TiDB cluster is deployed, if the TiFlash replicas consistently fail to be created, or if the TiFlash replicas are initially created normally but all or some tables fail to be created after a period of time, you can do the following to troubleshoot the issue:

1. Check whether the [Placement Rules](/configure-placement-rules.md) feature of PD is enabled. Starting from v5.0, this feature is enabled by default:

    ```shell
    echo 'config show replication' | /path/to/pd-ctl -u http://${pd-ip}:${pd-port}
    ```

    - If `true` is returned, go to the next step.
    - If `false` is returned, [enable the Placement Rules feature](/configure-placement-rules.md#enable-placement-rules) and go to the next step.

2. Check whether the TiFlash process is working normally by checking the **UpTime** metric on the **TiFlash-Summary** Grafana panel.

3. Check whether the connection between TiFlash and PD is normal.

    ```shell
    tiup ctl:nightly pd -u http://${pd-ip}:${pd-port} store
    ```

    The TiFlash's `store.labels` includes the information such as `{"key": "engine", "value": "tiflash"}`. You can check this information to confirm a TiFlash instance.

4. Check whether the `count` of Placement Rule with the `default` ID is correct:

    ```shell
    tiup ctl:nightly pd -u http://${pd-ip}:${pd-port} config placement-rules show | grep -C 10 default
    ```

    - If the value of `count` is smaller than or equal to the number of TiKV nodes in the cluster, go to the next step.
    - If the value of `count` is greater than the number of TiKV nodes in the cluster. For example, if there is only one TiKV node in the testing cluster while the `count` is `3`, then PD will not add any Region peer to the TiFlash node. To address this issue, change `count` to an integer smaller than or equal to the number of TiKV nodes in the cluster.

    > **Note:**
    >
    > The default value of `count` is `3`. In production environments, the value is usually smaller than the number of TiKV nodes. In test environments, if it is acceptable to have only one Region replica, you can set the value to `1`.

    ```shell
        curl -X POST -d '{
            "group_id": "pd",
            "id": "default",
            "start_key": "",
            "end_key": "",
            "role": "voter",
            "count": 3,
            "location_labels": [
            "host"
            ]
        }' <http://172.16.x.xxx:2379/pd/api/v1/config/rule>
    ```

5. Check the remaining disk space percentage on the TiFlash nodes. 

    When the disk usage of a TiFlash node exceeds the [`low-space-ratio`](/pd-configuration-file.md#low-space-ratio) setting (default: `0.8`), PD stops scheduling new data to that node to prevent disk exhaustion. If all TiFlash nodes have insufficient free disk space, PD cannot schedule new Region peers to TiFlash, causing replicas to remain unavailable (that is, progress < 1).

    - If the disk usage reaches or exceeds `low-space-ratio`, it indicates insufficient disk space. In this case, take one or more of the following actions:

        - Modify the value of `low-space-ratio` to allow the PD to resume scheduling Regions to the TiFlash node until it reaches the new threshold. 

            ```
            tiup ctl:nightly pd -u http://${pd-ip}:${pd-port} config set low-space-ratio 0.9
            ```

        - Scale out new TiFlash nodes. PD will automatically balance Regions across TiFlash nodes and resume scheduling Regions to TiFlash nodes with enough disk space.

        - Remove unnecessary files from the TiFlash node disk, such as the logging files, and the `space_placeholder_file` file in the `${data}/flash/` directory. If necessary, set `storage.reserve-space` in `tiflash-learner.toml` to `0MB` at the same time to temporarily resume TiFlash service.

    If the disk usage is less than the value of `low-space-ratio`, it indicates normal disk space availability. Proceed to the next step.

6. Check whether there is any `down peer`. 

    Remaining down peers might cause the replication to get stuck. Run the following command to check whether there is any `down peer`. 
    
    ```shell
    pd-ctl region check-down-peer
    ```
    
    If any, run the following command to remove it.

    ```shell
    pd-ctl operator add remove-peer <region-id> <tiflash-store-id>
    ```

If all the preceding checks pass but the issue persists, follow the instructions in [Data is not replicated to TiFlash](#data-is-not-replicated-to-tiflash) to identify which component or data replication process is experiencing issues.

## Data is not replicated to TiFlash

After deploying a TiFlash node and starting replication by executing `ALTER TABLE ... SET TIFLASH REPLICA ...`, no data is replicated to it. In this case, you can identify and address the problem by performing the following steps:

1. Check whether the replication is successful by running `ALTER TABLE ... SET TIFLASH REPLICA ...<num>` and check the output.

    - If the query is blocked, run the `SELECT * FROM information_schema.tiflash_replica` statement to check whether TiFlash replicas have been created.
        - Check whether the DDL statement is executed as expected through [`ADMIN SHOW DDL`](/sql-statements/sql-statement-admin-show-ddl.md). Check for other DDL statements (such as `ADD INDEX`) that might block altering TiFlash replica statement being executed.
        - Check whether any DML statement is executed on the same table through [`SHOW PROCESSLIST`](/sql-statements/sql-statement-show-processlist.md) that blocks altering TiFlash replica statement being executed.
    - Wait for the blocking statements to complete or be canceled, then try setting the TiFlash replica again. If no issues occur, proceed to the next step.

2. Check whether TiFlash Region replication runs correctly.

   Query the [`information_schema.tiflash_replica`](/information-schema/information-schema-tiflash-replica.md) table to check whether the `PROGRESS` field, which indicates the TiFlash replica replication progress, is changing. Alternatively, search for the keyword `Tiflash replica is not available` in the `tidb.log` file to review related logs and the corresponding `progress` values.

   - If the replication progress changes, it indicates TiFlash replication is functioning normally, but potentially at a slow pace. Refer to [Data replication is slow](#data-replication-is-slow) for optimization configurations.
   - If the replication progress does not change, TiFlash replication is abnormal. Go to the next step.

3. Check whether TiDB has successfully created any placement rule for the table.

    Search the logs of TiDB DDL Owner and check whether TiDB has notified PD to add placement rules. 
    
    - For non-partitioned tables, search `ConfigureTiFlashPDForTable`. 
    - For partitioned tables, search `ConfigureTiFlashPDForPartitions`.

    - If the keyword is found, go to the next step.
    - If not found, collect logs of the corresponding component to [get support](/support.md).

4. Check whether PD has configured any placement rule for tables.

    Run the following command to view all TiFlash placement rules on the current PD.
    
    ```shell
    curl http://<pd-ip>:<pd-port>/pd/api/v1/config/rules/group/tiflash
    ```

    - If a rule with the ID format `table-<table_id>-r` exists, the PD has configured a placement rule successfully. Go to the next step.
    - If such a rule does not exist, collect logs of the corresponding component to [get support](/support.md).

5. Check whether the PD schedules properly.

    Search the `pd.log` file for the `table-<table_id>-r` keyword and scheduling logs like `add operator`. Alternatively, check whether there are `add-rule-peer` operator on the **Operator/Schedule operator create** of PD Dashboard on Grafana. You can also check the value **Scheduler/Patrol Region time** on the PD Dashboard on Grafana. **Patrol Region time** reflects the duration for PD to scan all Regions and generate scheduling operations. A high value might cause delays in scheduling.

    - If the `pd.log` contains the keyword `table-<table_id>-r` along with `add operator` scheduling logs, or if the duration values on the **Scheduler/Patrol Region time** panel appear normal, it indicates that PD scheduling is functioning properly.
    - If no `add-rule-peer` scheduling logs are found, or the **Patrol Region time** is more than 30 minutes, the PD does not schedule properly or is scheduling slowly. Collect the TiDB, PD, and TiFlash log files to [get support](/support.md).

If the preceding methods cannot resolve your issue, collect the TiDB, PD, and TiFlash log files, and [get support](/support.md) from PingCAP or the community.

## Data replication is slow

The causes vary. You can address the problem by performing the following steps.

1. Follow the [Speed up TiFlash replication](/tiflash/create-tiflash-replicas.md#speed-up-tiflash-replication) to accelerate replication.

2. Adjust the load on TiFlash.

    Excessively high load on TiFlash can also result in slow replication. You can check the load of TiFlash indicators on the **TiFlash-Summary** panel on Grafana:

    - `Applying snapshots Count`: `TiFlash-summary` > `raft` > `Applying snapshots Count`
    - `Snapshot Predecode Duration`: `TiFlash-summary` > `raft` > `Snapshot Predecode Duration`
    - `Snapshot Flush Duration`: `TiFlash-summary` > `raft` > `Snapshot Flush Duration`
    - `Write Stall Duration`: `TiFlash-summary` > `Storage Write Stall` > `Write Stall Duration`
    - `generate snapshot CPU`: `TiFlash-Proxy-Details` > `Thread CPU` > `Region task worker pre-handle/generate snapshot CPU`

    Based on your service priorities, adjust the load accordingly to achieve optimal performance.
