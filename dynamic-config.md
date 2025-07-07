---
title: 动态修改配置
summary: 学习如何动态修改集群配置。
---

# 动态修改配置

本文档描述了如何动态修改集群配置。

你可以使用SQL语句在不重启集群组件的情况下，动态更新组件（包括TiDB、TiKV和PD）的配置。目前，修改TiDB实例配置的方法与修改其他组件（如TiKV和PD）的配置方式不同。

> **Note:**
>
> 该功能仅适用于TiDB自管理版本，不支持[TIDB云](https://docs.pingcap.com/tidbcloud/)。对于TiDB云，你需要联系[TIDB云支持](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)进行配置修改。

## 常用操作

本节介绍动态修改配置的常用操作。

### 查看实例配置

要查看集群中所有实例的配置，使用`show config`语句。结果如下：


```sql
show config;
```

```sql
+------+-----------------+-----------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Type | Instance        | Name                                                      | Value                                                                                                                                                                                                                                                                            |
+------+-----------------+-----------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| tidb | 127.0.0.1:4001  | advertise-address                                         | 127.0.0.1                                                                                                                                                                                                                                                                        |
| tidb | 127.0.0.1:4001  | binlog.binlog-socket                                      |                                                                                                                                                                                                                                                                                  |
| tidb | 127.0.0.1:4001  | binlog.enable                                             | false                                                                                                                                                                                                                                                                            |
| tidb | 127.0.0.1:4001  | binlog.ignore-error                                       | false                                                                                                                                                                                                                                                                            |
| tidb | 127.0.0.1:4001  | binlog.strategy                                           | range                                                                                                                                                                                                                                                                            |
| tidb | 127.0.0.1:4001  | binlog.write-timeout                                      | 15s                                                                                                                                                                                                                                                                              |
| tidb | 127.0.0.1:4001  | check-mb4-value-in-utf8                                   | true                                                                                                                                                                                                                                                                             |

...
```

你可以通过字段过滤结果。例如：


```sql
show config where type='tidb'
show config where instance in (...)
show config where name like '%log%'
show config where type='tikv' and name='log.level'
```

### 动态修改TiKV配置

> **Note:**
>
> - 动态修改TiKV配置项后，TiKV配置文件会自动更新，但你还需要通过执行`tiup edit-config`来修改对应的配置项，否则`upgrade`和`reload`等操作会覆盖你的修改。关于配置项的修改细节，参考[使用TiUP修改配置](/maintain-tidb-using-tiup.md#modify-the-configuration)。
> - 执行`tiup edit-config`后，无需再执行`tiup reload`。

使用`set config`语句时，可以根据实例地址或组件类型，修改单个实例或所有实例的配置。

- 修改所有TiKV实例的配置：

> **Note:**
>
> 建议用反引号包裹变量名。


```sql
set config tikv `split.qps-threshold`=1000;
```

- 修改单个TiKV实例的配置：

    
```sql
set config "127.0.0.1:20180" `split.qps-threshold`=1000;
```

如果修改成功，会返回`Query OK`：

```sql
Query OK, 0 rows affected (0.01 sec)
```

如果批量修改过程中发生错误，会返回警告信息：


```sql
set config tikv `log-level`='warn';
```

```sql
Query OK, 0 rows affected, 1 warning (0.04 sec)
```

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

批量修改不保证原子性，可能在部分实例成功，部分失败。如果你用`set tikv key=val`修改整个TiKV集群的配置，可能会在某些实例失败。可以通过`show warnings`检查结果。

如果部分修改失败，需要重新执行对应的语句或逐个修改失败的实例。若某些TiKV实例因网络或机器故障无法访问，待恢复后再进行修改。

配置项成功修改后，结果会被持久化到配置文件中，后续操作会以此为准。一些配置项的名称可能与TiDB的保留字冲突，例如`limit`和`key`，对于这些配置项，需用反引号`` ` ``括起来，例如 `` `raftstore.raft-log-gc-size-limit` ``。

以下TiKV配置项支持动态修改：

| 配置项 | 描述 |
| :--- | :--- |
| log.level | 日志级别。 |
| `raftstore.raft-max-inflight-msgs` | 需要确认的Raft日志数。当超过此数时，Raft状态机会减慢日志发送速度。 |
| `raftstore.raft-log-gc-tick-interval` | 定期调度删除Raft日志的轮询任务时间间隔。 |
| `raftstore.raft-log-gc-threshold` | Raft日志残留最大软限制。 |
| `raftstore.raft-log-gc-count-limit` | Raft日志残留最大硬限制。 |
| `raftstore.raft-log-gc-size-limit` | Raft日志残留最大大小硬限制。 |
| `raftstore.raft-max-size-per-msg` | 单个消息包允许生成的最大大小软限制。 |
| `raftstore.raft-entry-max-size` | 单个Raft日志最大大小硬限制。 |
| `raftstore.raft-entry-cache-life-time` | 日志缓存的最大剩余时间。 |
| `raftstore.max-apply-unpersisted-log-limit` | 已提交但未持久化的Raft日志最大应用数。 |
| `raftstore.split-region-check-tick-interval` | 检查是否需要Region拆分的时间间隔。 |
| `raftstore.region-split-check-diff` | 允许Region数据超出最大值的最大差值，超过则触发Region拆分。 |
| `raftstore.region-compact-check-interval` | 检查是否需要手动触发RocksDB压缩的时间间隔。 |
| `raftstore.region-compact-check-step` | 每轮手动压缩检查的Region数量。 |
| `raftstore.region-compact-min-tombstones` | 触发RocksDB压缩所需的墓碑数量。 |
| `raftstore.region-compact-tombstones-percent` | 触发RocksDB压缩所需墓碑比例。 |
| `raftstore.pd-heartbeat-tick-interval` | Region向PD发送心跳的时间间隔。 |
| `raftstore.pd-store-heartbeat-tick-interval` | Store向PD发送心跳的时间间隔。 |
| `raftstore.snap-mgr-gc-tick-interval` | 触发过期快照文件回收的时间间隔。 |
| `raftstore.snap-gc-timeout` | 快照文件保存的最长时间。 |
| `raftstore.lock-cf-compact-interval` | TiKV触发Lock列族手动压缩的时间间隔。 |
| `raftstore.lock-cf-compact-bytes-threshold` | TiKV触发Lock列族手动压缩的大小阈值。 |
| `raftstore.messages-per-tick` | 每批处理的最大消息数。 |
| `raftstore.max-peer-down-duration` | 允许的最大Peer不活动时间。 |
| `raftstore.max-leader-missing-duration` | Peer无Leader的最长时间，超出后会向PD确认是否已被删除。 |
| `raftstore.abnormal-leader-missing-duration` | Peer无Leader的正常最长时间，超出后会在指标和日志中标记为异常。 |
| `raftstore.peer-stale-state-check-interval` | 检查Peer是否无Leader的时间间隔。 |
| `raftstore.consistency-check-interval` | 检查一致性的时间间隔（**不建议使用**，因为与TiDB的GC不兼容） |
| `raftstore.raft-store-max-leader-lease` | Raft Leader的最长信任期限。 |
| `raftstore.merge-check-tick-interval` | 合并检测的时间间隔。 |
| `raftstore.cleanup-import-sst-interval` | 检查过期SST文件的时间间隔。 |
| `raftstore.local-read-batch-size` | 一次处理的最大读请求数。 |
| `raftstore.apply-yield-write-size` | Apply线程每轮能写入的最大字节数（有限状态机） 。 |
| `raftstore.hibernate-timeout` | 启动后进入休眠的最短等待时间。在此时间内，TiKV不会休眠（不释放资源）。 |
| `raftstore.apply-pool-size` | 刷写数据到磁盘的线程池大小，即Apply线程池的大小。 |
| `raftstore.store-pool-size` | 处理Raft的线程池大小，即Raftstore线程池的大小。 |
| `raftstore.apply-max-batch-size` | Raft状态机以BatchSystem批量处理写请求时，最大可同时执行的Raft状态机数量。 |
| `raftstore.store-max-batch-size` | Raft状态机以BatchSystem批量处理写入日志到磁盘的请求时，最大可同时处理的Raft状态机数量。 |
| `raftstore.store-io-pool-size` | 处理Raft I/O任务的线程数，也是StoreWriter线程池的大小（**不要**将此值从非零改为0或从0改为非零） |
| `raftstore.periodic-full-compact-start-max-cpu` | TiKV启用全量压缩时的CPU使用阈值。 |
| `readpool.unified.max-thread-count` | 统一处理读请求的线程池最大线程数，即UnifyReadPool线程池的大小。 |
| `readpool.unified.max-tasks-per-worker` | 单个线程在统一读池中允许的最大任务数，超出会返回`Server Is Busy`错误。 |
| `readpool.unified.auto-adjust-pool-size` | 是否自动调整UnifyReadPool线程池大小。 |
| `coprocessor.split-region-on-table` | 是否开启按表拆分Region。 |
| `coprocessor.batch-split-limit` | Region批量拆分的阈值。 |
| `coprocessor.region-max-size` | Region的最大大小。 |
| `coprocessor.region-split-size` | 新拆分Region的大小。 |
| `coprocessor.region-max-keys` | Region允许的最大Key数。 |
| `coprocessor.region-split-keys` | 新拆分Region的Key数。 |
| `pessimistic-txn.wait-for-lock-timeout` | 悲观事务等待锁的最长时间。 |
| `pessimistic-txn.wake-up-delay-duration` | 悲观事务唤醒的延迟时间。 |
| `pessimistic-txn.pipelined` | 是否开启悲观锁的流水线处理。 |
| `pessimistic-txn.in-memory` | 是否开启悲观锁的内存模式。 |
| `quota.foreground-cpu-time` | TiKV前台处理读写请求的CPU资源软限制。 |
| `quota.foreground-write-bandwidth` | TiKV前台写入数据带宽软限制。 |
| `quota.foreground-read-bandwidth` | TiKV前台读取数据带宽软限制。 |
| `quota.background-cpu-time` | TiKV后台处理读写请求的CPU资源软限制。 |
| `quota.background-write-bandwidth` | TiKV后台写入数据带宽软限制。 |
| `quota.background-read-bandwidth` | TiKV后台读取数据带宽软限制。 |
| `quota.enable-auto-tune` | 是否开启配额的自动调优。开启后，TiKV会根据实例负载动态调整后台请求的配额。 |
| `quota.max-delay-duration` | 单个读写请求在前台被强制等待的最长时间。 |
| `gc.ratio-threshold` | 跳过Region GC的阈值（GC版本数/键数）。 |
| `gc.batch-keys` | 一批处理的键数。 |
| `gc.max-write-bytes-per-sec` | 每秒最大写入RocksDB的字节数。 |
| `gc.enable-compaction-filter` | 是否启用压缩过滤器。 |
| `gc.compaction-filter-skip-version-check` | 是否跳过压缩过滤器的集群版本检查（未发布）。 |
| `{db-name}.max-total-wal-size` | WAL总最大大小。 |
| `{db-name}.max-background-jobs` | RocksDB后台线程数。 |
| `{db-name}.max-background-flushes` | RocksDB最大刷写线程数。 |
| `{db-name}.max-open-files` | RocksDB最大打开文件数。 |
| `{db-name}.compaction-readahead-size` | 压缩时的`readahead`大小。 |
| `{db-name}.bytes-per-sync` | 文件异步写入时，操作系统逐步同步到磁盘的速率。 |
| `{db-name}.wal-bytes-per-sync` | WAL文件写入时，操作系统逐步同步到磁盘的速率。 |
| `{db-name}.writable-file-max-buffer-size` | WritableFileWrite中使用的最大缓冲区大小。 |
| `{db-name}.{cf-name}.block-cache-size` | 块缓存的大小。 |
| `{db-name}.{cf-name}.write-buffer-size` | memtable的大小。 |
| `{db-name}.{cf-name}.max-write-buffer-number` | memtable的最大数量。 |
| `{db-name}.{cf-name}.max-bytes-for-level-base` | 基层（L1）最大字节数。 |
| `{db-name}.{cf-name}.target-file-size-base` | 基层的目标文件大小。 |
| `{db-name}.{cf-name}.level0-file-num-compaction-trigger` | 触发L0压缩的最大文件数。 |
| `{db-name}.{cf-name}.level0-slowdown-writes-trigger` | 触发写入阻塞的L0最大文件数。 |
| `{db-name}.{cf-name}.level0-stop-writes-trigger` | 完全阻塞写入的L0最大文件数。 |
| `{db-name}.{cf-name}.max-compaction-bytes` | 每次压缩写入磁盘的最大字节数。 |
| `{db-name}.{cf-name}.max-bytes-for-level-multiplier` | 每层的默认放大倍数。 |
| `{db-name}.{cf-name}.disable-auto-compactions` | 是否启用自动压缩。 |
| `{db-name}.{cf-name}.soft-pending-compaction-bytes-limit` | 软限制待压缩字节数。 |
| `{db-name}.{cf-name}.hard-pending-compaction-bytes-limit` | 硬限制待压缩字节数。 |
| `{db-name}.{cf-name}.titan.blob-run-mode` | Titan Blob文件的处理模式。 |
| `{db-name}.{cf-name}.titan.min-blob-size` | Titan存储数据的阈值。值达到此阈值时，数据存入Titan Blob文件。 |
| `{db-name}.{cf-name}.titan.blob-file-compression` | Titan Blob文件的压缩算法。 |
| `{db-name}.{cf-name}.titan.discardable-ratio` | Titan数据文件中垃圾数据比例的阈值，超过则触发Titan GC。 |
| `server.grpc-memory-pool-quota` | gRPC可用的最大内存。 |
| `server.max-grpc-send-msg-len` | gRPC最大可发送消息长度。 |
| `server.snap-io-max-bytes-per-sec` | 处理快照时的最大磁盘带宽。 |
| `server.concurrent-send-snap-limit` | 同时发送快照的最大数量。 |
| `server.concurrent-recv-snap-limit` | 同时接收快照的最大数量。 |
| `server.raft-msg-max-batch-size` | 单个gRPC消息中包含的最大Raft消息数。 |
| `server.simplify-metrics`        | 是否简化采样监控指标。 |
| `storage.block-cache.capacity` | 共享块缓存的大小（支持v4.0.3及以上版本）。 |
| `storage.scheduler-worker-pool-size` | 调度器线程池中的线程数。 |
| `import.num-threads` | 处理恢复或导入RPC请求的线程数（从v8.1.2开始支持动态修改）。 |
| `backup.num-threads` | 备份线程数（支持v4.0.3及以上版本）。 |
| `split.qps-threshold` | 执行`load-base-split`的QPS阈值。如果Region的读请求QPS连续10秒超过此值，则进行拆分。 |
| `split.byte-threshold` | 执行`load-base-split`的字节数阈值。如果Region的读请求流量连续10秒超过此值，则进行拆分。 |
| `split.region-cpu-overload-threshold-ratio` | 执行`load-base-split`的Region CPU超载阈值。若Region的统一读池CPU使用率连续10秒超过此比例，则拆分（支持v6.2.0及以上）。 |
| `split.split-balance-score` | `load-base-split`的参数，确保拆分后两个Region的负载尽可能平衡。值越小越平衡，但设置过小可能导致拆分失败。 |
| `split.split-contained-score` | `load-base-split`的参数，值越小，Region拆分后跨Region访问越少。 |
| `cdc.min-ts-interval` | 解决TS转发的时间间隔。 |
| `cdc.old-value-cache-memory-quota` | TiCDC旧值条目的内存占用上限。 |
| `cdc.sink-memory-quota` | TiCDC数据变更事件的内存占用上限。 |
| `cdc.incremental-scan-speed-limit` | 历史数据增量扫描速度上限。 |
| `cdc.incremental-scan-concurrency` | 历史数据增量扫描任务的最大并发数。 |

在上表中，带有`{db-name}`或`{db-name}.{cf-name}`前缀的参数是与RocksDB相关的配置。`db-name`的可选值为`rocksdb`和`raftdb`。

- 当`db-name`为`rocksdb`时，`cf-name`的可选值为`defaultcf`、`writecf`、`lockcf`和`raftcf`。
- 当`db-name`为`raftdb`时，`cf-name`的值可以为`defaultcf`。

详细参数说明请参考[TiKV配置文件](/tikv-configuration-file.md)。

### 动态修改PD配置

目前，PD不支持每个实例的单独配置，所有PD实例共享相同的配置。

你可以使用以下语句修改PD配置：


```sql
set config pd `log.level`='info';
```

如果修改成功，会返回`Query OK`：

```sql
Query OK, 0 rows affected (0.01 sec)
```

成功修改的配置项会被持久化到etcd中，后续操作以etcd中的配置为准。部分配置项的名称可能与TiDB的保留字冲突，对于这些配置项，需用反引号`` ` ``括起来，例如 `` `schedule.leader-schedule-limit` ``。

以下PD配置项支持动态修改：

| 配置项 | 描述 |
| :--- | :--- |
| `log.level` | 日志级别。 |
| `cluster-version` | 集群版本。 |
| `schedule.max-merge-region-size` | 控制Region合并的大小限制（单位MiB）。 |
| `schedule.max-merge-region-keys` | 指定Region合并的最大Key数。 |
| `schedule.patrol-region-interval` | 检查Region健康状态的频率。 |
| `schedule.split-merge-interval` | 对同一Region执行拆分和合并操作的时间间隔。 |
| `schedule.max-snapshot-count` | 单个存储节点同时发送或接收的最大快照数。 |
| `schedule.max-pending-peer-count` | 单个存储节点的最大待处理Peer数。 |
| `schedule.max-store-down-time` | PD判断存储节点不可恢复的停机时间。 |
| `schedule.max-store-preparing-time` | 控制存储节点上线的最大等待时间。 |
| `schedule.leader-schedule-policy` | Leader调度策略。 |
| `schedule.leader-schedule-limit` | 同时进行的Leader调度任务数。 |
| `schedule.region-schedule-limit` | 同时进行的Region调度任务数。 |
| `schedule.replica-schedule-limit` | 同时进行的副本调度任务数。 |
| `schedule.merge-schedule-limit` | Region合并调度任务的最大数。 |
| `schedule.hot-region-schedule-limit` | 热Region调度任务的最大数。 |
| `schedule.hot-region-cache-hits-threshold` | 认为Region为热点的阈值。 |
| `schedule.high-space-ratio` | 存储容量充足的阈值比例。 |
| `schedule.low-space-ratio` | 存储容量不足的阈值比例。 |
| `schedule.tolerant-size-ratio` | 负载平衡缓冲区大小。 |
| `schedule.enable-remove-down-replica` | 是否启用自动移除DownReplica。 |
| `schedule.enable-replace-offline-replica` | 是否启用迁移OfflineReplica。 |
| `schedule.enable-make-up-replica` | 是否启用自动补充副本。 |
| `schedule.enable-remove-extra-replica` | 是否启用移除多余副本。 |
| `schedule.enable-location-replacement` | 是否启用隔离级别检测。 |
| `schedule.enable-cross-table-merge` | 是否启用跨表合并。 |
| `schedule.enable-one-way-merge` | 是否启用单向合并（只允许与相邻Region合并）。 |
| `schedule.region-score-formula-version` | Region评分公式版本。 |
| `schedule.scheduler-max-waiting-operator` | 每个调度器中的等待操作数。 |
| `schedule.enable-debug-metrics` | 是否启用调试指标。 |
| `schedule.enable-joint-consensus` | 是否使用联合共识进行副本调度。 |
| `schedule.hot-regions-write-interval` | PD存储热点Region信息的时间间隔。 |
| `schedule.hot-regions-reserved-days` | 热Region信息的保留天数。 |
| `schedule.max-movable-hot-peer-size` | 可调度的最大Region大小。 |
| `schedule.store-limit-version` | [store limit](/configure-store-limit.md)的版本控制。 |
| `replication.max-replicas` | 副本最大数。 |
| `replication.location-labels` | TiKV集群的拓扑信息。 |
| `replication.enable-placement-rules` | 是否启用Placement Rules。 |
| `replication.strictly-match-label` | 是否启用标签匹配。 |
| `replication.isolation-level` | TiKV集群的最小拓扑隔离级别。 |
| `pd-server.use-region-storage` | 是否启用独立Region存储。 |
| `pd-server.max-gap-reset-ts` | 设置重置时间戳（BR）的最大间隔。 |
| `pd-server.key-type` | 设置集群密钥类型。 |
| `pd-server.metric-storage` | 设置集群指标存储地址。 |
| `pd-server.dashboard-address` | 设置Dashboard地址。 |
| `pd-server.flow-round-by-digit` | 指定Region流量信息的最低位数取整。 |
| `pd-server.min-resolved-ts-persistence-interval` | 决定最小已解决时间戳持久化到PD的间隔。 |
| `pd-server.server-memory-limit` | PD实例的内存限制比例。 |
| `pd-server.server-memory-limit-gc-trigger` | PD尝试触发GC的阈值比例。 |
| `pd-server.enable-gogc-tuner` | 是否启用GOGC调优器。 |
| `pd-server.gc-tuner-threshold` | GOGC调优的最大内存阈值比例。 |
| `replication-mode.replication-mode` | 备份模式。 |
| `replication-mode.dr-auto-sync.label-key` | 区分不同AZ的标签键，需匹配Placement Rules。 |
| `replication-mode.dr-auto-sync.primary` | 主AZ。 |
| `replication-mode.dr-auto-sync.dr` | 灾备（DR）AZ。 |
| `replication-mode.dr-auto-sync.primary-replicas` | 主AZ中的Voter副本数。 |
| `replication-mode.dr-auto-sync.dr-replicas` | 灾备AZ中的Voter副本数。 |
| `replication-mode.dr-auto-sync.wait-store-timeout` | 网络隔离或故障时切换到异步复制模式的等待时间。 |
| `replication-mode.dr-auto-sync.wait-recover-timeout` | 网络恢复后切换回同步恢复状态的等待时间。 |
| `replication-mode.dr-auto-sync.pause-region-split` | 是否在`async_wait`和`async`状态下暂停Region拆分操作。 |

详细参数说明请参考[PD配置文件](/pd-configuration-file.md)。

### 动态修改TiDB配置

目前，修改TiDB配置的方法与修改TiKV和PD配置不同。你可以通过使用[系统变量](/system-variables.md)来修改TiDB配置。

以下示例演示如何通过`tidb_slow_log_threshold`变量动态修改`slow-threshold`。

`slow-threshold`的默认值为300毫秒。你可以通过`tidb_slow_log_threshold`设置为200毫秒。


```sql
set tidb_slow_log_threshold = 200;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

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

以下TiDB配置项支持动态修改：

| 配置项 | SQL变量 | 描述 |
| --- | --- | --- |
| `instance.tidb_enable_slow_log` | `tidb_enable_slow_log` | 是否启用慢日志。 |
| `instance.tidb_slow_log_threshold` | `tidb_slow_log_threshold` | 慢日志阈值。 |
| `instance.tidb_expensive_query_time_threshold` | `tidb_expensive_query_time_threshold` | 显示“昂贵查询”的阈值。 |
| `instance.tidb_enable_collect_execution_info` | `tidb_enable_collect_execution_info` | 是否记录操作符的执行信息。 |
| `instance.tidb_record_plan_in_slow_log` | `tidb_record_plan_in_slow_log` | 是否在慢日志中记录执行计划。 |
| `instance.tidb_force_priority` | `tidb_force_priority` | 指定从此TiDB实例提交的语句的优先级。 |
| `instance.max_connections` | `max_connections` | 最大允许的并发连接数。 |
| `instance.tidb_enable_ddl` | `tidb_enable_ddl` | 是否允许此TiDB实例成为DDL所有者。 |
| `pessimistic-txn.constraint-check-in-place-pessimistic` | `tidb_constraint_check_in_place_pessimistic` | 是否将唯一索引的唯一性约束检查延后到需要锁定索引或事务提交时。 |

### 动态修改TiFlash配置

目前，你可以通过系统变量[`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610)动态修改TiFlash的最大并发数`max_threads`，该变量指定TiFlash执行请求的最大并发数。

`tidb_max_tiflash_threads`的默认值为`-1`，表示无效，依赖于TiFlash配置文件中的设置。你可以将`max_threads`设置为10：


```sql
set tidb_max_tiflash_threads = 10;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

```sql
select @@tidb_max_tiflash_threads;
```

```sql
+----------------------------+
| @@tidb_max_tiflash_threads |
+----------------------------+
| 10                         |
+----------------------------+
1 row in set (0.00 sec)
```