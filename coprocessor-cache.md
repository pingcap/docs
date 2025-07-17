---
title: Coprocessor Cache
summary: 了解 Coprocessor Cache 的特性。
---

# Coprocessor Cache

从 v4.0 版本开始，TiDB 实例支持缓存下推到 TiKV 的计算结果（Coprocessor Cache 功能），在某些场景下可以加快计算过程。

## 配置

<CustomContent platform="tidb">

你可以通过在 TiDB 配置文件中的 `tikv-client.copr-cache` 配置项来配置 Coprocessor Cache。关于如何启用和配置 Coprocessor Cache 的详细信息，请参见 [TiDB 配置文件](/tidb-configuration-file.md#tikv-clientcopr-cache-new-in-v400)。

</CustomContent>

<CustomContent platform="tidb-cloud">

Coprocessor Cache 功能默认启用。可缓存的数据最大大小为 1000 MB。

</CustomContent>

## 特性描述

+ 当在单个 TiDB 实例上首次执行某个 SQL 语句时，执行结果不会被缓存。
+ 计算结果会被缓存到 TiDB 的内存中。如果 TiDB 实例重启，缓存将失效。
+ 该缓存不在 TiDB 实例之间共享。
+ 只缓存下推计算的结果。即使命中缓存，TiDB 仍需执行后续计算。
+ 缓存以 Region 为单位。向 Region 写入数据会导致该 Region 的缓存失效。因此，Coprocessor Cache 主要在数据变化较少的场景下生效。
+ 当下推计算请求相同时，缓存会命中。通常在以下场景中，下推计算请求相同或部分相同：
    - SQL 语句相同。例如，反复执行相同的 SQL 语句。

        在这种场景下，所有的下推计算请求是一致的，所有请求都可以使用下推计算缓存。

    - SQL 语句包含变化条件，其他部分保持一致。变化条件为表的主键或分区。

        在这种场景下，部分下推计算请求与之前的请求相同，这些请求可以使用缓存的（之前的）下推计算结果。

    - SQL 语句包含多个变化条件，其他部分保持一致。变化条件与复合索引列完全匹配。

        在这种场景下，部分下推计算请求与之前的请求相同，这些请求可以使用缓存的（之前的）下推计算结果。

+ 该特性对用户是透明的。启用或禁用该特性不会影响计算结果，只会影响 SQL 执行时间。

## 查看缓存效果

你可以通过执行 `EXPLAIN ANALYZE` 或查看 Grafana 监控面板来检查 Coprocessor Cache 的效果。

### 使用 `EXPLAIN ANALYZE`

你可以在 [Operators for accessing tables](/choose-index.md#operators-for-accessing-tables) 中通过 [`EXPLAIN ANALYZE` statement](/sql-statements/sql-statement-explain-analyze.md) 查看缓存命中率。示例如下：

```sql
EXPLAIN ANALYZE SELECT * FROM t USE INDEX(a);
+-------------------------------+-----------+---------+-----------+------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------+-----------------------+------+
| id                            | estRows   | actRows | task      | access object          | execution info                                                                                                                                                                                                                                           | operator info                  | memory                | disk |
+-------------------------------+-----------+---------+-----------+------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------+-----------------------+------+
| IndexLookUp_6                 | 262400.00 | 262400  | root      |                        | time:620.513742ms, loops:258, cop_task: {num: 4, max: 5.530817ms, min: 1.51829ms, avg: 2.70883ms, p95: 5.530817ms, max_proc_keys: 2480, p95_proc_keys: 2480, tot_proc: 1ms, tot_wait: 1ms, rpc_num: 4, rpc_time: 10.816328ms, copr_cache_hit_rate: 0.75} |                                | 6.685169219970703 MB  | N/A  |
| ├─IndexFullScan_4(Build)      | 262400.00 | 262400  | cop[tikv] | table:t, index:a(a, c) | proc max:93ms, min:1ms, p80:93ms, p95:93ms, iters:275, tasks:4                                                                                                                                                                                           | keep order:false, stats:pseudo | 1.7549400329589844 MB | N/A  |
| └─TableRowIDScan_5(Probe)     | 262400.00 | 0       | cop[tikv] | table:t                | time:0ns, loops:0                                                                                                                                                                                                                                        | keep order:false, stats:pseudo | N/A                   | N/A  |
+-------------------------------+-----------+---------+-----------+------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------+-----------------------+------+
3 rows in set (0.62 sec)
```

执行结果中的 `execution info` 列会显示 `copr_cache_hit_ratio` 信息，表示 Coprocessor Cache 的命中率。上例中的 `0.75` 表示命中率大约为 75%。

### 查看 Grafana 监控面板

在 Grafana 中，你可以在 `tidb` 命名空间下的 `distsql` 子系统中看到 **copr-cache** 面板。该面板监控整个集群中 Coprocessor Cache 的命中次数、未命中次数和缓存丢弃情况。