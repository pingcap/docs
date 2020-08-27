---
title: Modify Configuration Online
summary: Learn how to change the cluster configuration online.
aliases: ['/docs/dev/dynamic-config/']
---

# Modify Configuration Online

This document describes how to modify the cluster configuration online.

> **Note:**
>
> This feature is experimental. It is **NOT** recommended to use this feature in the production environment.

You can update the configuration of components (including TiDB, TiKV, and PD) online using SQL statements, without restarting the cluster components. Currently, the method of changing TiDB instance configuration is different from that of changing configuration of other components (such TiKV and PD).

## Common Operations

This section describes the common operations of modifying configuration online.

### View instance configuration

To view the configuration of all instances in the cluster, use the `show config` statement. The result is as follows:

{{< copyable "sql" >}}

```sql
show config;
```

```sql
+------+-----------------+-----------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Type | Instance        | Name                                                      | Value                                                                                                                                                                                                                                                                            |
+------+-----------------+-----------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| tidb | 127.0.0.1:4001  | advertise-address                                         | 127.0.0.1                                                                                                                                                                                                                                                                        |
| tidb | 127.0.0.1:4001  | alter-primary-key                                         | false                                                                                                                                                                                                                                                                            |
| tidb | 127.0.0.1:4001  | binlog.binlog-socket                                      |                                                                                                                                                                                                                                                                                  |
| tidb | 127.0.0.1:4001  | binlog.enable                                             | false                                                                                                                                                                                                                                                                            |
| tidb | 127.0.0.1:4001  | binlog.ignore-error                                       | false                                                                                                                                                                                                                                                                            |
| tidb | 127.0.0.1:4001  | binlog.strategy                                           | range                                                                                                                                                                                                                                                                            |
| tidb | 127.0.0.1:4001  | binlog.write-timeout                                      | 15s                                                                                                                                                                                                                                                                              |
| tidb | 127.0.0.1:4001  | check-mb4-value-in-utf8                                   | true                                                                                                                                                                                                                                                                             |

...
```

You can filter the result by fields. For example:

{{< copyable "sql" >}}

```sql
show config where type='tidb'
show config where instance in (...)
show config where name like '%log%'
show config where type='tikv' and name='log-level'
```

### Modify TiKV configuration online

> **Note:**
>
> - After changing TiKV configuration items online, the TiKV configuration file is automatically updated. However, you also need to modify the corresponding configuration items by executing `tiup edit-config`; otherwise, operations such as `upgrade` and `reload` will overwrite your changes. For details of modifying configuration items, refer to [Modify configuration using TiUP](/maintain-tidb-using-tiup.md#modify-the-configuration).
> - After executing `tiup edit-config`, you do not need to execute `tiup reload`.

When using the `set config` statement, you can modify the configuration of a single instance or of all instances according to the instance address or the component type.

- Modify the configuration of all TiKV instances:

    {{< copyable "sql" >}}

    ```sql
    set config tikv log.level="info"
    ```

- Modify the configuration of a single TiKV instance:

    {{< copyable "sql" >}}

    ```sql
    set config "127.0.0.1:20180" log.level="info"
    ```

If the modification is successful, `Query OK` is returned:

```sql
Query OK, 0 rows affected (0.01 sec)
```

If an error occurs during the batch modification, a warning is returned:

{{< copyable "sql" >}}

```sql
set config tikv log-level='warn';
```

```sql
Query OK, 0 rows affected, 1 warning (0.04 sec)
```

{{< copyable "sql" >}}

```sql
show warnings;
```

```sql
+---------+------+---------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                       |
+---------+------+---------------------------------------------------------------------------------------------------------------+
| Warning | 1105 | bad request to http://127.0.0.1:20180/config: fail to update, error: "config log-level can not be changed" |
+---------+------+---------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

The batch modification does not guarantee atomicity. The modification might succeed on some instances, while failing on others. If you modify the configuration of the entire TiKV cluster using `set tikv key=val`, your modification might fail on some instances. You can use `show warnings` to check the result.

If some modifications fail, you need to re-execute the corresponding statement or modify each failed instance. If some TiKV instances cannot be accessed due to network issues or machine failure, modify these instances after they are recovered.

If a configuration item is successfully modified, the result is persisted in the configuration file, which will prevail in the subsequent operations. The names of some configuration items might conflict with TiDB reserved words, such as `limit` and `key`. For these configuration items, use backtick `` ` `` to enclose them. For example, `` `raftstore.raft-log-gc-size-limit` ``.

The following TiKV configuration items can be modified online:

| Configuration item | Description |
| :--- | :--- |
| `raftstore.sync-log` | Determines whether to sync data and logs for persistent storage |
| `raftstore.raft-entry-max-size` | The maximum size of a single log |
| `raftstore.raft-log-gc-tick-interval` | The time interval at which the polling task of deleting Raft logs is scheduled |
| `raftstore.raft-log-gc-threshold` | The soft limit on the maximum allowable number of residual Raft logs |
| `raftstore.raft-log-gc-count-limit` | The hard limit on the allowable number of residual Raft logs |
| `raftstore.raft-log-gc-size-limit` | The hard limit on the allowable size of residual Raft logs |
| `raftstore.raft-entry-cache-life-time` | The maximum remaining time allowed for the log cache in memory |
| `raftstore.raft-reject-transfer-leader-duration` | Determines the smallest duration that a Leader is transferred to a newly added node |
| `raftstore.split-region-check-tick-interval` | The time interval at which to check whether the Region split is needed |
| `raftstore.region-split-check-diff` | The maximum value by which the Region data is allowed to exceed before Region split |
| `raftstore.region-compact-check-interval` | The time interval at which to check whether it is necessary to manually trigger RocksDB compaction |
| `raftstore.region-compact-check-step` | The number of Regions checked at one time for each round of manual compaction |
| `raftstore.region-compact-min-tombstones` | The number of tombstones required to trigger RocksDB compaction |
| `raftstore.region-compact-tombstones-percent` | The proportion of tombstone required to trigger RocksDB compaction |
| `raftstore.pd-heartbeat-tick-interval` | The time interval at which a Region's heartbeat to PD is triggered |
| `raftstore.pd-store-heartbeat-tick-interval` | The time interval at which a store's heartbeat to PD is triggered |
| `raftstore.snap-mgr-gc-tick-interval` | The time interval at which the recycle of expired snapshot files is triggered |
| `raftstore.snap-gc-timeout` | The longest time for which a snapshot file is saved |
| `raftstore.lock-cf-compact-interval` | The time interval at which TiKV triggers a manual compaction for the Lock Column Family |
| `raftstore.lock-cf-compact-bytes-threshold` | The size at which TiKV triggers a manual compaction for the Lock Column Family |
| `raftstore.messages-per-tick` | The maximum number of messages processed per batch |
| `raftstore.max-peer-down-duration` | The longest inactive duration allowed for a peer |
| `raftstore.max-leader-missing-duration` | The longest duration allowed for a peer to be without a leader. If this value is exceeded, the peer verifies with PD whether it has been deleted. |
| `raftstore.abnormal-leader-missing-duration` | The normal duration allowed for a peer to be without a leader. If this value is exceeded, the peer is seen as abnormal and marked in metrics and logs. |
| `raftstore.peer-stale-state-check-interval` | The time interval to check whether a peer is without a leader |
| `raftstore.consistency-check-interval` | The time interval to check consistency |
| `raftstore.raft-store-max-leader-lease` | The longest trusted period of a Raft leader |
| `raftstore.allow-remove-leader` | Determines whether to allow deleting the main switch |
| `raftstore.merge-check-tick-interval` | The time interval for merge check |
| `raftstore.cleanup-import-sst-interval` | The time interval to check expired SST files |
| `raftstore.local-read-batch-size` | The maximum number of read requests processed in one batch |
| `raftstore.hibernate-timeout` | The shortest wait duration before entering hibernation upon start. Within this duration, TiKV does not hibernate (not released). |
| `coprocessor.split-region-on-table` | Enables to split Region by table |
| `coprocessor.batch-split-limit` | The threshold of Region split in batches |
| `coprocessor.region-max-size` | The maximum size of a Region |
| `coprocessor.region-split-size` | The size of the newly split Region |
| `coprocessor.region-max-keys` | The maximum number of keys allowed in a Region |
| `coprocessor.region-split-keys` | The number of keys in the newly split Region |
| `pessimistic-txn.wait-for-lock-timeout` | The longest duration that a pessimistic transaction waits for the lock |
| `pessimistic-txn.wake-up-delay-duration` | The duration after which a pessimistic transaction is woken up |
| `pessimistic-txn.pipelined` | Whether to enable the pipelined pessimistic locking process |
| `gc.ratio-threshold` | The threshold at which Region GC is skipped (the number of GC versions/the number of keys) |
| `gc.batch-keys` | The number of keys processed in one batch |
| `gc.max-write-bytes-per-sec` | The maximum bytes that can be written into RocksDB per second |
| `gc.enable-compaction-filter` | Whether to enable compaction filter |
| `gc.compaction-filter-skip-version-check` | Whether to skip the cluster version check of compaction filter (not released) |
| `{db-name}.max-total-wal-size` | The maximum size of total WAL |
| `{db-name}.max-background-jobs` | The number of background threads in RocksDB |
| `{db-name}.max-open-files` | The total number of files that RocksDB can open |
| `{db-name}.compaction-readahead-size` | The size of `readahead` during compaction |
| `{db-name}.bytes-per-sync` | The rate at which OS incrementally synchronizes files to disk while these files are being written asynchronously |
| `{db-name}.wal-bytes-per-sync` | The rate at which OS incrementally synchronizes WAL files to disk while the WAL files are being written |
| `{db-name}.writable-file-max-buffer-size` | The maximum buffer size used in WritableFileWrite |
| `{db-name}.{cf-name}.block-cache-size` | The cache size of a block |
| `{db-name}.{cf-name}.write-buffer-size` | The size of a memtable |
| `{db-name}.{cf-name}.max-write-buffer-number` | The maximum number of memtables |
| `{db-name}.{cf-name}.max-bytes-for-level-base` | The maximum number of bytes at base level (L1) |
| `{db-name}.{cf-name}.target-file-size-base` | The size of the target file at base level |
| `{db-name}.{cf-name}.level0-file-num-compaction-trigger` | The maximum number of files at L0 that trigger compaction |
| `{db-name}.{cf-name}.level0-slowdown-writes-trigger` | The maximum number of files at L0 that trigger write stall |
| `{db-name}.{cf-name}.level0-stop-writes-trigger` | The maximum number of files at L0 that completely block write |
| `{db-name}.{cf-name}.max-compaction-bytes` | The maximum number of bytes written into disk per compaction |
| `{db-name}.{cf-name}.max-bytes-for-level-multiplier` | The default amplification multiple for each layer |
| `{db-name}.{cf-name}.disable-auto-compactions` | Enables or disables automatic compaction |
| `{db-name}.{cf-name}.soft-pending-compaction-bytes-limit` | The soft limit on the pending compaction bytes |
| `{db-name}.{cf-name}.hard-pending-compaction-bytes-limit` | The hard limit on the pending compaction bytes |
| `{db-name}.{cf-name}.titan.blob-run-mode` | The mode of processing blob files |
| `storage.block-cache.capacity` | The size of shared block cache (supported since v4.0.3) |
| `backup.num-threads` | The number of backup threads (supported since v4.0.3) |
| `split.qps-threshold` | The threshold to execute `load-base-split` on a Region. If the read QPS is higher than this value for 10 consecutive seconds, this Region should be split. |
| `split.split-balance-score` | The parameter of `load-base-split`, which ensures the load of the two split Regions is as balanced as possible |
| `split.split-contained-score` | The parameter of `load-base-split`, which reduces the cross-Region visits after split as much as possible |

In the table above, parameters with the `{db-name}` or `{db-name}.{cf-name}` prefix are configurations related to RocksDB. The optional values of `db-name` are `rocksdb` and `raftdb`.

- When `db-name` is `rocksdb`, the optional values of `cf-name` are `defaultcf`, `writecf`, `lockcf`, and `raftcf`.
- When `db-name` is `raftdb`, the value of `cf-name` can be `defaultcf`.

For detailed parameter description, refer to [TiKV Configuration File](/tikv-configuration-file.md).

### Modify PD configuration online

Currently, PD does not support the separate configuration for each instance. All PD instances share the same configuration.

You can modify the PD configurations using the following statement:

{{< copyable "sql" >}}

```sql
set config pd log.level="info"
```

If the modification is successful, `Query OK` is returned:

```sql
Query OK, 0 rows affected (0.01 sec)
```

If a configuration item is successfully modified, the result is persisted in etcd instead of in the configuration file; the configuration in etcd will prevail in the subsequent operations. The names of some configuration items might conflict with TiDB reserved words. For these configuration items, use backtick `` ` `` to enclose them. For example, `` `schedule.leader-schedule-limit` ``.

The following PD configuration items can be modified online:

| Configuration item | Description |
| :--- | :--- |
| `log.level` | The log level |
| `cluster-version` | The cluster version |
| `schedule.max-merge-region-size` | Controls the size limit of `Region Merge` (in MB) |
| `schedule.max-merge-region-keys` | Specifies the maximum numbers of the `Region Merge` keys |
| `schedule.patrol-region-interval` | Determines the frequency at which `replicaChecker` checks the health state of a Region |
| `schedule.split-merge-interval` | Determines the time interval of performing split and merge operations on the same Region |
| `schedule.max-snapshot-count` | Determines the maximum number of snapshots that a single store can send or receive at the same time |
| `schedule.max-pending-peer-count` | Determines the maximum number of pending peers in a single store |
| `schedule.max-store-down-time` | The downtime after which PD judges that the disconnected store can not be recovered |
| `schedule.leader-schedule-policy` | Determines the policy of Leader scheduling |
| `schedule.leader-schedule-limit` | The number of Leader scheduling tasks performed at the same time |
| `schedule.region-schedule-limit` | The number of Region scheduling tasks performed at the same time |
| `schedule.replica-schedule-limit` | The number of Replica scheduling tasks performed at the same time |
| `schedule.merge-schedule-limit` | The number of the `Region Merge` scheduling tasks performed at the same time |
| `schedule.hot-region-schedule-limit` | The number of hot Region scheduling tasks performed at the same time |
| `schedule.hot-region-cache-hits-threshold` | Determines the threshold at which a Region is considered a hot spot |
| `schedule.high-space-ratio` | The threshold ratio below which the capacity of the store is sufficient |
| `schedule.low-space-ratio` | The threshold ratio above which the capacity of the store is insufficient |
| `schedule.tolerant-size-ratio` | Controls the `balance` buffer size|
| `schedule.enable-remove-down-replica` | Determines whether to enable the feature that automatically removes `DownReplica` |
| `schedule.enable-replace-offline-replica` | Determines whether to enable the feature that migrates `OfflineReplica` |
| `schedule.enable-make-up-replica` | Determines whether to enable the feature that automatically supplements replicas |
| `schedule.enable-remove-extra-replica` | Determines whether to enable the feature that removes extra replicas |
| `schedule.enable-location-replacement` | Determines whether to enable isolation level check |
| `schedule.enable-cross-table-merge` | Determines whether to enable cross-table merge |
| `schedule.enable-one-way-merge` | Enables one-way merge, which only allows merging with the next adjacent Region |
| `replication.max-replicas` | Sets the maximum number of replicas |
| `replication.location-labels` | The topology information of a TiKV cluster |
| `replication.enable-placement-rules` | Enables Placement Rules |
| `replication.strictly-match-label` | Enables the label check |
| `pd-server.use-region-storage` | Enables independent Region storage |
| `pd-server.max-gap-reset-ts` | Sets the maximum interval of resetting timestamp (BR) |
| `pd-server.key-type` | Sets the cluster key type |
| `pd-server.metric-storage` | Sets the storage address of the cluster metrics |
| `pd-server.dashboard-address` | Sets the dashboard address |
| `replication-mode.replication-mode` | Sets the backup mode |

For detailed parameter description, refer to [PD Configuration File](/pd-configuration-file.md).

### Modify TiDB configuration online

Currently, the method of changing TiDB configuration is different from that of changing TiKV and PD configurations. You can modify TiDB configuration by using [SQL variables](/system-variables.md).

The following example shows how to modify `slow-threshold` online by using the `tidb_slow_log_threshold` variable. The default value of `slow-threshold` is 200 ms. You can set it to 200 ms by using `tidb_slow_log_threshold`.

{{< copyable "sql" >}}

```sql
set tidb_slow_log_threshold = 200;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

{{< copyable "sql" >}}

```sql
select @@tidb_slow_log_threshold;
```

```sql
+---------------------------+
| @@tidb_slow_log_threshold |
+---------------------------+
| 200                       |
+---------------------------+
1 row in set (0.00 sec)
```

The following TiDB configuration items can be modified online:

| Configuration item | SQL variable | Description |
| :--- | :--- |
| `mem-quota-query` | `tidb_mem_quota_query` | The memory usage limit of a query |
| `log.enable-slow-log` | `tidb_enable_slow_log` | Whether to enable slow log |
| `log.slow-threshold` | `tidb_slow_log_threshold` | The threshold of slow log |
| `log.expensive-threshold` | `tidb_expensive_query_time_threshold` | The threshold of a expensive query |
