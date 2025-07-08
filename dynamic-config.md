---
title: 动态修改配置
summary: 学习如何动态修改集群配置。
---

# 动态修改配置

本文档描述了如何动态修改集群配置。

你可以使用 SQL 语句在不重启集群组件的情况下，动态更新组件（包括 TiDB、TiKV 和 PD）的配置。目前，修改 TiDB 实例配置的方法与修改其他组件（如 TiKV 和 PD）的方法不同。

> **Note:**
>
> 该功能仅适用于 TiDB 自托管版本，不支持 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)。对于 TiDB Cloud，你需要联系 [TiDB Cloud Support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support) 来修改配置。

## 常用操作

本节介绍动态修改配置的常用操作。

### 查看实例配置

要查看集群中所有实例的配置，使用 `show config` 语句。结果如下：


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

### 动态修改 TiKV 配置

> **Note:**
>
> - 动态修改 TiKV 配置项后，TiKV 配置文件会自动更新，但你还需要通过执行 `tiup edit-config` 来修改对应的配置项，否则 `upgrade` 和 `reload` 等操作会覆盖你的更改。关于修改配置项的详细操作，请参考 [使用 TiUP 修改配置](/maintain-tidb-using-tiup.md#modify-the-configuration)。
> - 执行 `tiup edit-config` 后，无需再执行 `tiup reload`。

使用 `set config` 语句时，可以根据实例地址或组件类型，修改单个实例或所有实例的配置。

- 修改所有 TiKV 实例的配置：

> **Note:**
>
> 建议用反引号 `` ` `` 包裹变量名。


```sql
set config tikv `split.qps-threshold`=1000;
```

- 修改单个 TiKV 实例的配置：

    
    ```sql
    set config "127.0.0.1:20180" `split.qps-threshold`=1000;
    ```

如果修改成功，会返回 `Query OK`：

```sql
Query OK, 0 rows affected (0.01 sec)
```

如果在批量修改过程中发生错误，会返回警告信息：


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

批量修改不保证原子性，可能在部分实例成功，部分失败。如果你使用 `set tikv key=val` 修改整个 TiKV 集群的配置，可能会在某些实例上失败。你可以通过 `show warnings` 查看结果。

如果部分修改失败，需要重新执行对应的语句或逐个修改失败的实例。如果某些 TiKV 实例因网络问题或机器故障无法访问，待其恢复后再进行修改。

配置项成功修改后，结果会被持久化到配置文件中，后续操作会以此为准。有些配置项的名称可能与 TiDB 保留字冲突，例如 `limit` 和 `key`。对于这些配置项，使用反引号 `` ` `` 包裹，例如 `` `raftstore.raft-log-gc-size-limit` ``。

以下 TiKV 配置项可以动态修改：

| 配置项 | 描述 |
| :--- | :--- |
| log.level | 日志级别。 |
| `raftstore.raft-max-inflight-msgs` | 要确认的 Raft 日志数。如果超过此数，Raft 状态机会减慢日志发送速度。 |
| `raftstore.raft-log-gc-tick-interval` | 定期调度删除 Raft 日志的轮询任务时间间隔 |
| `raftstore.raft-log-gc-threshold` | Raft 日志残留最大允许数量的软限制 |
| `raftstore.raft-log-gc-count-limit` | Raft 日志残留最大允许数量的硬限制 |
| `raftstore.raft-log-gc-size-limit` | Raft 日志残留最大允许大小的硬限制 |
| `raftstore.raft-max-size-per-msg` | 单个消息包允许生成的软限制大小 |
| `raftstore.raft-entry-max-size` | 单个 Raft 日志最大尺寸的硬限制 |
| `raftstore.raft-entry-cache-life-time` | 日志缓存的最大剩余时间 |
| `raftstore.max-apply-unpersisted-log-limit` | 已提交但未持久化的 Raft 日志最大应用数 |
| `raftstore.split-region-check-tick-interval` | 检查是否需要 Region 拆分的时间间隔 |
| `raftstore.region-split-check-diff` | 允许超出 Region 数据最大值的最大差值，超过则进行 Region 拆分 |
| `raftstore.region-compact-check-interval` | 检查是否需要手动触发 RocksDB 压缩的时间间隔 |
| `raftstore.region-compact-check-step` | 每轮手动压缩检查的 Region 数量 |
| `raftstore.region-compact-min-tombstones` | 触发 RocksDB 压缩所需的墓碑数量 |
| `raftstore.region-compact-tombstones-percent` | 触发 RocksDB 压缩所需墓碑比例 |
| `raftstore.pd-heartbeat-tick-interval` | 触发 Region 向 PD 发送心跳的时间间隔 |
| `raftstore.pd-store-heartbeat-tick-interval` | 触发存储向 PD 发送心跳的时间间隔 |
| `raftstore.snap-mgr-gc-tick-interval` | 触发过期快照文件回收的时间间隔 |
| `raftstore.snap-gc-timeout` | 快照文件保存的最长时间 |
| `raftstore.lock-cf-compact-interval` | TiKV 触发 Lock Column Family 手动压缩的时间间隔 |
| `raftstore.lock-cf-compact-bytes-threshold` | TiKV 触发 Lock Column Family 手动压缩的大小阈值 |
| `raftstore.messages-per-tick` | 每批处理的最大消息数 |
| `raftstore.max-peer-down-duration` | 允许的最大 Peer 不活跃时间 |
| `raftstore.max-leader-missing-duration` | Peer 无 Leader 的最长时间，超出后会向 PD 校验是否已被删除 |
| `raftstore.abnormal-leader-missing-duration` | Peer 无 Leader 的正常最长时间，超出后会在指标和日志中标记为异常 |
| `raftstore.peer-stale-state-check-interval` | 检查 Peer 是否无 Leader 的时间间隔 |
| `raftstore.consistency-check-interval` | 检查一致性的时间间隔（**不建议**，因为与 TiDB 的垃圾回收不兼容） |
| `raftstore.raft-store-max-leader-lease` | Raft Leader 的最长信任期 |
| `raftstore.merge-check-tick-interval` | 合并检测的时间间隔 |
| `raftstore.cleanup-import-sst-interval` | 检查过期 SST 文件的时间间隔 |
| `raftstore.local-read-batch-size` | 一次处理的最大读请求数 |
| `raftstore.apply-yield-write-size` | Apply 线程每轮对一个 FSM 写入的最大字节数 |
| `raftstore.hibernate-timeout` | 启动后进入休眠的最短等待时间，期间 TiKV 不会休眠（不释放） |
| `raftstore.apply-pool-size` | 刷写数据到磁盘的线程池大小，即 Apply 线程池的大小 |
| `raftstore.store-pool-size` | 处理 Raft 的线程池大小，即 Raftstore 线程池的大小 |
| `raftstore.apply-max-batch-size` | Raft 状态机批量处理写请求的最大数量 |
| `raftstore.store-max-batch-size` | Raft 状态机批量处理写入日志到磁盘的最大数量 |
| `raftstore.store-io-pool-size` | 处理 Raft I/O 任务的线程数，也是 StoreWriter 线程池的大小（**不要**将此值从非零改为 0 或反之） |
| `raftstore.periodic-full-compact-start-max-cpu` | TiKV 在启用全量压缩时的 CPU 使用阈值 |
| `readpool.unified.max-thread-count` | 统一处理读请求的线程池最大线程数，即 UnifyReadPool 线程池的大小 |
| `readpool.unified.max-tasks-per-worker` | 单个线程在统一读池中允许的最大任务数，超出会返回 `Server Is Busy` 错误 |
| `readpool.unified.auto-adjust-pool-size` | 是否自动调整 UnifyReadPool 线程池大小 |
| `coprocessor.split-region-on-table` | 是否启用按表拆分 Region |
| `coprocessor.batch-split-limit` | 批量拆分 Region 的阈值 |
| `coprocessor.region-max-size` | Region 的最大尺寸 |
| `coprocessor.region-split-size` | 新拆分 Region 的尺寸 |
| `coprocessor.region-max-keys` | Region 允许的最大键数 |
| `coprocessor.region-split-keys` | 新拆分 Region 的键数 |
| `pessimistic-txn.wait-for-lock-timeout` | 悲观事务等待锁的最长时间 |
| `pessimistic-txn.wake-up-delay-duration` | 悲观事务唤醒的延迟时间 |
| `pessimistic-txn.pipelined` | 是否启用管道式悲观锁 |
| `pessimistic-txn.in-memory` | 是否启用内存悲观锁 |
| `quota.foreground-cpu-time` | TiKV 前台处理读写请求的 CPU 资源软限制 |
| `quota.foreground-write-bandwidth` | 前台事务写入数据的带宽软限制 |
| `quota.foreground-read-bandwidth` | 前台事务和协处理器读取数据的带宽软限制 |
| `quota.background-cpu-time` | TiKV 后台处理读写请求的 CPU 资源软限制 |
| `quota.background-write-bandwidth` | 后台事务写入数据的带宽软限制 |
| `quota.background-read-bandwidth` | 后台事务和协处理器读取数据的带宽软限制 |
| `quota.enable-auto-tune` | 是否启用配额的自动调优。启用后，TiKV 会根据实例负载动态调整后台请求的配额。 |
| `quota.max-delay-duration` | 单个读写请求在前台被强制等待的最长时间 |
| `gc.ratio-threshold` | 跳过 Region GC 的阈值（GC 版本数/键数） |
| `gc.batch-keys` | 一批处理的键数 |
| `gc.max-write-bytes-per-sec` | 每秒写入 RocksDB 的最大字节数 |
| `gc.enable-compaction-filter` | 是否启用压缩过滤器 |
| `gc.compaction-filter-skip-version-check` | 是否跳过压缩过滤器的集群版本检查（未发布） |
| `{db-name}.max-total-wal-size` | WAL 总大小的最大值 |
| `{db-name}.max-background-jobs` | RocksDB 后台线程数 |
| `{db-name}.max-background-flushes` | RocksDB 刷新线程的最大数量 |
| `{db-name}.max-open-files` | RocksDB 可打开的最大文件数 |
| `{db-name}.compaction-readahead-size` | 压缩时的 readahead 大小 |
| `{db-name}.bytes-per-sync` | 文件异步写入时操作系统逐步同步到磁盘的速率 |
| `{db-name}.wal-bytes-per-sync` | WAL 文件写入时操作系统逐步同步到磁盘的速率 |
| `{db-name}.writable-file-max-buffer-size` | WritableFileWrite 使用的最大缓冲区大小 |
| `{db-name}.{cf-name}.block-cache-size` | 块缓存的大小 |
| `{db-name}.{cf-name}.write-buffer-size` | memtable 的大小 |
| `{db-name}.{cf-name}.max-write-buffer-number` | memtable 的最大数量 |
| `{db-name}.{cf-name}.max-bytes-for-level-base` | 基层（L1）最大字节数 |
| `{db-name}.{cf-name}.target-file-size-base` | 基层目标文件大小 |
| `{db-name}.{cf-name}.level0-file-num-compaction-trigger` | 触发压缩的 L0 文件最大数量 |
| `{db-name}.{cf-name}.level0-slowdown-writes-trigger` | 触发写入阻塞的 L0 文件最大数量 |
| `{db-name}.{cf-name}.level0-stop-writes-trigger` | 完全阻塞写入的 L0 文件最大数量 |
| `{db-name}.{cf-name}.max-compaction-bytes` | 每次压缩写入磁盘的最大字节数 |
| `{db-name}.{cf-name}.max-bytes-for-level-multiplier` | 每层的默认放大倍数 |
| `{db-name}.{cf-name}.disable-auto-compactions` | 是否启用自动压缩 |
| `{db-name}.{cf-name}.soft-pending-compaction-bytes-limit` | 软限制待压缩字节数 |
| `{db-name}.{cf-name}.hard-pending-compaction-bytes-limit` | 硬限制待压缩字节数 |
| `{db-name}.{cf-name}.titan.blob-run-mode` | Titan 文件处理模式 |
| `{db-name}.{cf-name}.titan.min-blob-size` | Titan 存储阈值，值达到此值时存入 Titan Blob 文件 |
| `{db-name}.{cf-name}.titan.blob-file-compression` | Titan Blob 文件的压缩算法 |
| `{db-name}.{cf-name}.titan.discardable-ratio` | Titan 数据文件中垃圾数据比例阈值，超过则触发 GC |
| `server.grpc-memory-pool-quota` | gRPC 使用的内存限制 |
| `server.max-grpc-send-msg-len` | gRPC 允许的最大消息长度 |
| `server.snap-io-max-bytes-per-sec` | 处理快照时的最大磁盘带宽 |
| `server.concurrent-send-snap-limit` | 同时发送的快照最大数量 |
| `server.concurrent-recv-snap-limit` | 同时接收的快照最大数量 |
| `server.raft-msg-max-batch-size` | 单个 gRPC 消息中包含的最大 Raft 消息数 |
| `server.simplify-metrics`        | 是否简化采样监控指标                   |
| `storage.block-cache.capacity` | 共享块缓存的大小（支持 v4.0.3 及以上版本） |
| `storage.scheduler-worker-pool-size` | 调度器线程池中的线程数 |
| `import.num-threads` | 处理恢复或导入 RPC 请求的线程数（从 v8.1.2 开始支持动态修改） |
| `backup.num-threads` | 备份线程数（支持 v4.0.3 及以上版本） |
| `split.qps-threshold` | 执行 `load-base-split` 的请求 QPS 阈值。如果 Region 的读请求 QPS 连续 10 秒超过此值，则进行拆分。|
| `split.byte-threshold` | 执行 `load-base-split` 的字节数阈值。如果 Region 的读请求流量连续 10 秒超过此值，则进行拆分。 |
| `split.region-cpu-overload-threshold-ratio` | 执行 `load-base-split` 的 CPU 使用率阈值。如果 Region 的统一读池 CPU 使用率连续 10 秒超过此值，则进行拆分（支持 v6.2.0 及以上版本） |
| `split.split-balance-score` | `load-base-split` 的参数，确保拆分后两个 Region 的负载尽可能平衡。值越小越平衡，但设置过小可能导致拆分失败。 |
| `split.split-contained-score` | `load-base-split` 的参数，值越小，Region 拆分后跨 Region 访问越少。 |
| `cdc.min-ts-interval` | 传递 Resolved TS 的时间间隔 |
| `cdc.old-value-cache-memory-quota` | TiCDC 旧值条目占用的最大内存 |
| `cdc.sink-memory-quota` | TiCDC 数据变更事件占用的最大内存 |
| `cdc.incremental-scan-speed-limit` | 历史数据增量扫描速度上限 |
| `cdc.incremental-scan-concurrency` | 历史数据增量扫描任务的最大并发数 |

在上表中，带有 `{db-name}` 或 `{db-name}.{cf-name}` 前缀的参数是 RocksDB 相关配置。`db-name` 的可选值为 `rocksdb` 和 `raftdb`。

- 当 `db-name` 为 `rocksdb` 时，`cf-name` 的可选值为 `defaultcf`、`writecf`、`lockcf` 和 `raftcf`。
- 当 `db-name` 为 `raftdb` 时，`cf-name` 的值可以为 `defaultcf`。

详细参数说明请参考 [TiKV 配置文件](/tikv-configuration-file.md)。

### 动态修改 PD 配置

目前，PD 不支持每个实例的单独配置，所有 PD 实例共享相同的配置。

你可以使用以下语句修改 PD 配置：


```sql
set config pd `log.level`='info';
```

如果修改成功，会返回 `Query OK`：

```sql
Query OK, 0 rows affected (0.01 sec)
```

成功修改的配置项会被持久化到 etcd 中，后续操作以 etcd 中的配置为准。部分配置项的名称可能与 TiDB 保留字冲突，对于这些配置项，使用反引号 `` ` `` 包裹，例如 `` `schedule.leader-schedule-limit` ``。

以下 PD 配置项可以动态修改：

| 配置项 | 描述 |
| :--- | :--- |
| `log.level` | 日志级别 |
| `cluster-version` | 集群版本 |
| `schedule.max-merge-region-size` | 控制 `Region Merge` 的尺寸限制（单位：MiB） |
| `schedule.max-merge-region-keys` | 指定 `Region Merge` 的最大键数 |
| `schedule.patrol-region-interval` | 检查 Region 健康状态的频率 |
| `schedule.split-merge-interval` | 对同一 Region 执行拆分和合并操作的时间间隔 |
| `schedule.max-snapshot-count` | 单个存储同时发送或接收的最大快照数 |
| `schedule.max-pending-peer-count` | 单个存储的最大待处理 Peer 数量 |
| `schedule.max-store-down-time` | PD 判断存储断开后无法恢复的停机时间 |
| `schedule.max-store-preparing-time` | 控制存储上线的最大等待时间 |
| `schedule.leader-schedule-policy` | Leader 调度策略 |
| `schedule.leader-schedule-limit` | 同时进行的 Leader 调度任务数 |
| `schedule.region-schedule-limit` | 同时进行的 Region 调度任务数 |
| `schedule.replica-schedule-limit` | 同时进行的副本调度任务数 |
| `schedule.merge-schedule-limit` | `Region Merge` 调度任务的最大数量 |
| `schedule.hot-region-schedule-limit` | 热点 Region 调度任务的最大数量 |
| `schedule.hot-region-cache-hits-threshold` | 认为 Region 为热点的阈值 |
| `schedule.high-space-ratio` | 存储容量充足的阈值比例 |
| `schedule.low-space-ratio` | 存储容量不足的阈值比例 |
| `schedule.tolerant-size-ratio` | 控制 `balance` 缓冲区大小 |
| `schedule.enable-remove-down-replica` | 是否启用自动移除 `DownReplica` 功能 |
| `schedule.enable-replace-offline-replica` | 是否启用迁移 `OfflineReplica` 功能 |
| `schedule.enable-make-up-replica` | 是否启用自动补充副本功能 |
| `schedule.enable-remove-extra-replica` | 是否启用移除多余副本功能 |
| `schedule.enable-location-replacement` | 是否启用隔离级别检查 |
| `schedule.enable-cross-table-merge` | 是否启用跨表合并 |
| `schedule.enable-one-way-merge` | 是否启用单向合并，只允许与相邻 Region 合并 |
| `schedule.region-score-formula-version` | Region 评分公式版本控制 |
| `schedule.scheduler-max-waiting-operator` | 每个调度器中的等待操作数 |
| `schedule.enable-debug-metrics` | 是否启用调试指标 |
| `schedule.enable-joint-consensus` | 是否使用联合共识进行副本调度 |
| `schedule.hot-regions-write-interval` | PD 存储热点 Region 信息的时间间隔 |
| `schedule.hot-regions-reserved-days` | 热点 Region 信息保留天数 |
| `schedule.max-movable-hot-peer-size` | 可调度的最大 Region 大小 |
| `schedule.store-limit-version` | [store limit](/configure-store-limit.md) 的版本控制 |
| `replication.max-replicas` | 副本最大数量 |
| `replication.location-labels` | TiKV 集群的拓扑信息 |
| `replication.enable-placement-rules` | 是否启用 Placement Rules |
| `replication.strictly-match-label` | 是否启用标签匹配 |
| `replication.isolation-level` | 最小拓扑隔离级别 |
| `pd-server.use-region-storage` | 是否启用独立的 Region 存储 |
| `pd-server.max-gap-reset-ts` | 重置时间戳（BR）的最大间隔 |
| `pd-server.key-type` | 集群密钥类型 |
| `pd-server.metric-storage` | 集群指标存储地址 |
| `pd-server.dashboard-address` | 仪表盘地址 |
| `pd-server.flow-round-by-digit` | Region 流量信息的最低位数取整 |
| `pd-server.min-resolved-ts-persistence-interval` | 最小已解决时间戳持久化到 PD 的间隔 |
| `pd-server.server-memory-limit` | PD 实例的内存限制比例 |
| `pd-server.server-memory-limit-gc-trigger` | PD 触发 GC 的阈值比例 |
| `pd-server.enable-gogc-tuner` | 是否启用 GOGC 调优器 |
| `pd-server.gc-tuner-threshold` | GOGC 调优的最大内存阈值比例 |
| `relication-mode.replication-mode` | 备份模式 |
| `relication-mode.dr-auto-sync.label-key` | 区分不同 AZ 的标签键，需匹配 Placement Rules |
| `relication-mode.dr-auto-sync.primary` | 主要 AZ |
| `relication-mode.dr-auto-sync.dr` | 灾备（DR） AZ |
| `relication-mode.dr-auto-sync.primary-replicas` | 主要 AZ 中的 Voter 副本数 |
| `relication-mode.dr-auto-sync.dr-replicas` | 灾备 AZ 中的 Voter 副本数 |
| `relication-mode.dr-auto-sync.wait-store-timeout` | 网络隔离或故障时切换到异步复制模式的等待时间 |
| `relication-mode.dr-auto-sync.wait-recover-timeout` | 网络恢复后切换回 `sync-recover` 状态的等待时间 |
| `relication-mode.dr-auto-sync.pause-region-split` | 是否暂停 `async_wait` 和 `async` 状态下的 Region 拆分操作 |

详细参数说明请参考 [PD 配置文件](/pd-configuration-file.md)。

### 动态修改 TiDB 配置

目前，修改 TiDB 配置的方法与修改 TiKV 和 PD 配置的方法不同。你可以通过使用 [系统变量](/system-variables.md) 来修改 TiDB 配置。

以下示例演示如何通过 `tidb_slow_log_threshold` 变量动态修改 `slow-threshold`。

`slow-threshold` 的默认值为 300 ms。你可以使用 `tidb_slow_log_threshold` 设置为 200 ms。


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

以下 TiDB 配置项可以动态修改：

| 配置项 | SQL 变量 | 描述 |
| --- | --- | --- |
| `instance.tidb_enable_slow_log` | `tidb_enable_slow_log` | 是否启用慢日志 |
| `instance.tidb_slow_log_threshold` | `tidb_slow_log_threshold` | 慢日志阈值 |
| `instance.tidb_expensive_query_time_threshold` | `tidb_expensive_query_time_threshold` | 昂贵查询的阈值 |
| `instance.tidb_enable_collect_execution_info` | `tidb_enable_collect_execution_info` | 是否记录操作符的执行信息 |
| `instance.tidb_record_plan_in_slow_log` | `tidb_record_plan_in_slow_log` | 是否在慢日志中记录执行计划 |
| `instance.tidb_force_priority` | `tidb_force_priority` | 指定从此 TiDB 实例提交的语句的优先级 |
| `instance.max_connections` | `max_connections` | 最大允许的并发连接数 |
| `instance.tidb_enable_ddl` | `tidb_enable_ddl` | 是否允许此 TiDB 实例成为 DDL 所有者 |
| `pessimistic-txn.constraint-check-in-place-pessimistic` | `tidb_constraint_check_in_place_pessimistic` | 是否将唯一索引的唯一性约束检查延后到需要锁定索引或事务提交时 |

### 动态修改 TiFlash 配置

目前，你可以通过系统变量 [`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610) 动态修改 TiFlash 的最大并发数 `max_threads`，该变量指定 TiFlash 执行请求的最大并发数。

`tidb_max_tiflash_threads` 的默认值为 `-1`，表示此变量无效，依赖于 TiFlash 配置文件中的设置。你可以通过设置 `tidb_max_tiflash_threads` 将 `max_threads` 改为 10：


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