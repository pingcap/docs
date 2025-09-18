---
title: 垃圾回收配置
summary: 了解 GC 配置参数。
---

# 垃圾回收配置

你可以通过以下系统变量配置垃圾回收（GC）：

* [`tidb_gc_enable`](/system-variables.md#tidb_gc_enable-new-in-v50)：控制是否为 TiKV 启用垃圾回收。
* [`tidb_gc_run_interval`](/system-variables.md#tidb_gc_run_interval-new-in-v50)：指定 GC 的运行间隔。
* [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)：指定每次 GC 保留数据的时间上限。
* [`tidb_gc_concurrency`](/system-variables.md#tidb_gc_concurrency-new-in-v50)：指定 GC 的 [Resolve Locks](/garbage-collection-overview.md#resolve-locks) 步骤中线程的数量。
* [`tidb_gc_scan_lock_mode`](/system-variables.md#tidb_gc_scan_lock_mode-new-in-v50)：指定 GC 的 Resolve Locks 步骤中扫描锁的方式。
* [`tidb_gc_max_wait_time`](/system-variables.md#tidb_gc_max_wait_time-new-in-v610)：指定活跃事务阻塞 GC safe point 的最长时间。

关于如何修改系统变量的值，详见 [系统变量](/system-variables.md)。

## GC I/O 限制

<CustomContent platform="tidb-cloud">

> **Note:**
>
> 本节仅适用于 TiDB 自建集群。TiDB Cloud 默认没有 GC I/O 限制。

</CustomContent>

TiKV 支持 GC I/O 限制。你可以通过配置 `gc.max-write-bytes-per-sec` 来限制每秒 GC worker 的写入量，从而减少对正常请求的影响。

`0` 表示禁用此功能。

你可以使用 tikv-ctl 动态修改该配置：

```bash
tikv-ctl --host=ip:port modify-tikv-config -n gc.max-write-bytes-per-sec -v 10MB
```

## TiDB 5.0 的变更

在 TiDB 早期版本中，垃圾回收通过 `mysql.tidb` 系统表进行配置。虽然对该表的修改仍然受支持，但推荐使用提供的系统变量进行配置。这样可以确保配置变更能够被校验，并防止出现意外行为（[#20655](https://github.com/pingcap/tidb/issues/20655)）。

`CENTRAL` 垃圾回收模式已不再支持。将自动使用 `DISTRIBUTED` GC 模式（自 TiDB 3.0 起为默认模式）。该模式更高效，因为 TiDB 不再需要向每个 TiKV region 发送请求来触发垃圾回收。

关于早期版本的变更信息，请通过左侧菜单的 _TIDB 版本选择器_ 查看本文件的历史版本。

## TiDB 6.1.0 的变更

在 TiDB v6.1.0 之前，TiDB 中的事务不会影响 GC safe point。从 v6.1.0 开始，TiDB 在计算 GC safe point 时会考虑事务的 startTS，以解决待访问数据已被清理的问题。如果事务持续时间过长，safe point 会被长时间阻塞，影响应用性能。

在 TiDB v6.1.0 中，引入了系统变量 [`tidb_gc_max_wait_time`](/system-variables.md#tidb_gc_max_wait_time-new-in-v610) 用于控制活跃事务阻塞 GC safe point 的最长时间。超过该值后，GC safe point 会被强制推进。

### Compaction Filter 中的 GC

基于 `DISTRIBUTED` GC 模式，Compaction Filter 中的 GC 机制利用 RocksDB 的 compaction 过程，而不是单独的 GC worker 线程来执行 GC。该新 GC 机制有助于避免 GC 带来的额外磁盘读取。同时，在清理过期数据后，能够避免大量残留的 tombstone 标记，从而提升顺序扫描性能。

<CustomContent platform="tidb-cloud">

> **Note:**
>
> 以下 TiKV 配置修改示例仅适用于 TiDB 自建集群。对于 TiDB Cloud，Compaction Filter 中的 GC 机制默认已启用。

</CustomContent>

以下示例展示了如何在 TiKV 配置文件中启用该机制：

```toml
[gc]
enable-compaction-filter = true
```

你也可以通过动态修改配置来启用该 GC 机制。示例如下：

```sql
show config where type = 'tikv' and name like '%enable-compaction-filter%';
```

```sql
+------+-------------------+-----------------------------+-------+
| Type | Instance          | Name                        | Value |
+------+-------------------+-----------------------------+-------+
| tikv | 172.16.5.37:20163 | gc.enable-compaction-filter | false |
| tikv | 172.16.5.36:20163 | gc.enable-compaction-filter | false |
| tikv | 172.16.5.35:20163 | gc.enable-compaction-filter | false |
+------+-------------------+-----------------------------+-------+
```

```sql
set config tikv gc.enable-compaction-filter = true;
show config where type = 'tikv' and name like '%enable-compaction-filter%';
```

```sql
+------+-------------------+-----------------------------+-------+
| Type | Instance          | Name                        | Value |
+------+-------------------+-----------------------------+-------+
| tikv | 172.16.5.37:20163 | gc.enable-compaction-filter | true  |
| tikv | 172.16.5.36:20163 | gc.enable-compaction-filter | true  |
| tikv | 172.16.5.35:20163 | gc.enable-compaction-filter | true  |
+------+-------------------+-----------------------------+-------+
```

<CustomContent platform="tidb">

> **Note:**
>
> 使用 Compaction Filter 机制时，GC 进度可能会延迟，进而影响 TiKV 的扫描性能。如果你的业务包含大量 coprocessor 请求，并且在 [**TiKV-Details > Coprocessor Detail**](/grafana-tikv-dashboard.md#coprocessor-detail) 面板中观察到 **Total Ops Details** 下的 `next()` 或 `prev()` 调用次数明显超过 `processed_keys` 调用次数的三倍，可以采取以下措施：
> 
> - 对于 v7.1.3 之前的 TiDB 版本，建议关闭 Compaction Filter 以加快 GC。
> - 对于 v7.1.3 到 v7.5.6 版本，TiDB 会根据每个 Region 的冗余版本数量 [`region-compact-min-redundant-rows`](/tikv-configuration-file.md#region-compact-min-redundant-rows-new-in-v710) 和冗余版本百分比 [`region-compact-redundant-rows-percent`](/tikv-configuration-file.md#region-compact-redundant-rows-percent-new-in-v710) 自动触发 compaction 以提升 Compaction Filter GC 性能。此时建议调整这些配置项，而不是关闭 Compaction Filter。
> - 从 v7.5.7 起，[`region-compact-min-redundant-rows`](/tikv-configuration-file.md#region-compact-min-redundant-rows-new-in-v710) 和 [`region-compact-redundant-rows-percent`](/tikv-configuration-file.md#region-compact-redundant-rows-percent-new-in-v710) 已废弃。TiDB 现在会根据 [`gc.auto-compaction.redundant-rows-threshold`](/tikv-configuration-file.md#redundant-rows-threshold-new-in-v757) 和 [`gc.auto-compaction.redundant-rows-percent-threshold`](/tikv-configuration-file.md#redundant-rows-percent-threshold-new-in-v757) 自动触发 compaction。此时建议调整这些配置项，而不是关闭 Compaction Filter。

</CustomContent>