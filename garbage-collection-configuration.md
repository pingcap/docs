---
title: 垃圾回收配置
summary: 了解 GC 配置参数。
---

# 垃圾回收配置

你可以使用以下系统变量来配置垃圾回收（GC）：

* [`tidb_gc_enable`](/system-variables.md#tidb_gc_enable-new-in-v50): 控制是否启用 TiKV 的垃圾回收。
* [`tidb_gc_run_interval`](/system-variables.md#tidb_gc_run_interval-new-in-v50): 指定 GC 的间隔时间。
* [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50): 指定每次 GC 保留数据的时间限制。
* [`tidb_gc_concurrency`](/system-variables.md#tidb_gc_concurrency-new-in-v50): 指定 GC 中 [Resolve Locks](/garbage-collection-overview.md#resolve-locks) 步骤的线程数。
* [`tidb_gc_scan_lock_mode`](/system-variables.md#tidb_gc_scan_lock_mode-new-in-v50): 指定在 GC 的 Resolve Locks 步骤中扫描锁的方式。
* [`tidb_gc_max_wait_time`](/system-variables.md#tidb_gc_max_wait_time-new-in-v610): 指定活跃事务阻塞 GC 安全点的最大时间。

关于如何修改系统变量的值的更多信息，请参见 [System variables](/system-variables.md)。

## GC I/O 限制

<CustomContent platform="tidb-cloud">

> **Note:**
>
> 本节内容仅适用于 TiDB Self-Managed。TiDB Cloud 默认没有 GC I/O 限制。

</CustomContent>

TiKV 支持 GC I/O 限制。你可以配置 `gc.max-write-bytes-per-sec` 来限制每个 GC 线程每秒的写入量，从而减少对正常请求的影响。

`0` 表示禁用此功能。

你可以通过 tikv-ctl 动态修改此配置：

```bash
tikv-ctl --host=ip:port modify-tikv-config -n gc.max-write-bytes-per-sec -v 10MB
```

## TiDB 5.0 版本的变化

在之前的 TiDB 版本中，垃圾回收通过 `mysql.tidb` 系统表进行配置。虽然仍然支持对该表的更改，但建议使用提供的系统变量。这有助于确保配置的任何更改都能被验证，并防止出现意外行为（[#20655](https://github.com/pingcap/tidb/issues/20655)）。

`CENTRAL` 垃圾回收模式不再支持。将自动使用 `DISTRIBUTED` GC 模式（自 TiDB 3.0 起为默认模式）。此模式更高效，因为 TiDB 不再需要向每个 TiKV 区域发送请求以触发垃圾回收。

关于之前版本的变更信息，请使用左侧菜单中的 _TIDB 版本选择器_ 查看早期版本的文档。

## TiDB 6.1.0 版本的变化

在 TiDB v6.1.0 之前，TiDB 中的事务不会影响 GC 安全点。从 v6.1.0 开始，TiDB 会在计算 GC 安全点时考虑事务的 startTS，以解决访问数据已被清除的问题。如果事务时间过长，安全点会被长时间阻塞，从而影响应用性能。

在 TiDB v6.1.0 中，新增了系统变量 [`tidb_gc_max_wait_time`](/system-variables.md#tidb_gc_max_wait_time-new-in-v610)，用以控制活跃事务阻塞 GC 安全点的最大时间。超过该值后，GC 安全点会被强制前移。

### GC in Compaction Filter

基于 `DISTRIBUTED` GC 模式，Compaction Filter 中的 GC 机制采用 RocksDB 的压缩过程，而不是单独的 GC 工作线程，来执行 GC。这一新机制有助于避免因 GC 导致的额外磁盘读取。同时，在清理过时数据后，也能避免大量残留的 tombstone 标记，从而提升顺序扫描性能。

<CustomContent platform="tidb-cloud">

> **Note:**
>
> 以下修改 TiKV 配置的示例仅适用于 TiDB Self-Managed。对于 TiDB Cloud，Compaction Filter 中的 GC 机制默认已启用。

</CustomContent>

以下示例展示如何在 TiKV 配置文件中启用该机制：

```toml
[gc]
enable-compaction-filter = true
```

你也可以通过动态修改配置来启用此机制。示例如下：

```sql
show config where type = 'tikv' and name like '%enable-compaction-filter%';
```

```sql
set config tikv gc.enable-compaction-filter = true;
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