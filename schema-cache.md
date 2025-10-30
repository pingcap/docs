---
title: Schema Cache
summary: TiDB 采用基于 LRU（最近最少使用）机制的 schema 信息缓存，有效降低了内存占用，并在拥有大量数据库和数据表的场景下提升了性能。
---

# Schema Cache

在一些多租户场景下，可能会有数十万甚至上百万个数据库和数据表。如果将所有这些数据库和数据表的 schema 信息全部加载到内存中，不仅会消耗大量内存，还会导致访问性能下降。为了解决这个问题，TiDB 引入了类似 LRU（最近最少使用）的 schema 缓存机制。只有最近访问过的数据库和数据表的 schema 信息才会被缓存在内存中。

> **Note:**
>
> 目前，该特性不适用于 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群。

## 配置 schema 缓存

你可以通过配置系统变量 [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800) 来启用 schema 缓存特性。

## 最佳实践

- 在拥有大量数据库和数据表（例如超过 10 万个数据库和数据表）的场景，或者数据库和数据表数量足以影响系统性能时，建议开启 schema 缓存特性。
- 你可以通过 TiDB Dashboard 的 **Schema load** 部分下的 **Infoschema v2 Cache Operation** 子面板，监控 schema 缓存的命中率。如果命中率较低，可以适当增大 [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800) 的值。
- 你可以通过 TiDB Dashboard 的 **Schema load** 部分下的 **Infoschema v2 Cache Size** 子面板，监控当前 schema 缓存的实际使用大小。

<CustomContent platform="tidb">

- 建议关闭 [`performance.force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v657-and-v710) 以减少 TiDB 启动时间。
- 如果需要创建大量数据表（例如超过 10 万张表），建议将 [`split-table`](/tidb-configuration-file.md#split-table) 参数设置为 `false`，以减少 Region 数量，从而降低 TiKV 的内存占用。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 建议关闭 [`performance.force-init-stats`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file/#force-init-stats-new-in-v657-and-v710) 以减少 TiDB 启动时间。
- 如果需要创建大量数据表（例如超过 10 万张表），建议将 [`split-table`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file/#split-table) 参数设置为 `false`，以减少 Region 数量，从而降低 TiKV 的内存占用。

</CustomContent>

## 已知限制

在拥有大量数据库和数据表的场景下，存在以下已知问题：

- 单个集群中的数据表数量不能超过 300 万。
- 如果单个集群中的数据表数量超过 30 万，不要将 [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800) 的值设置为 `0`，否则可能导致 TiDB 内存溢出（OOM）。
- 使用外键可能会增加集群中 DDL 操作的执行时间。
- 当数据表被不规律访问时，例如在 time1 访问一批表，在 time2 访问另一批表，且 `tidb_schema_cache_size` 设置较小，schema 信息可能会频繁被驱逐和重新缓存，导致性能波动。该特性更适用于频繁访问的数据库和数据表相对固定的场景。
- 统计信息可能无法及时收集。
- 访问部分元数据信息可能会变慢。
- 切换 schema 缓存的开关需要等待一段时间。
- 涉及枚举所有元数据信息的操作可能会变慢，例如：

    - `SHOW FULL TABLES`
    - `FLASHBACK`
    - `ALTER TABLE ... SET TIFLASH MODE ...`

- 当你使用带有 [`AUTO_INCREMENT`](/auto-increment.md) 或 [`AUTO_RANDOM`](/auto-random.md) 属性的数据表时，较小的 schema 缓存大小可能导致这些表的元数据频繁进出缓存，从而导致分配的 ID 区间在未完全使用前失效，出现 ID 跳号。在写入压力较大的场景下，甚至可能导致 ID 区间被耗尽。为尽量减少异常的 ID 分配行为并提升系统稳定性，建议采取以下措施：

    - 通过监控面板查看 schema 缓存的命中率和大小，评估缓存设置是否合理。适当增大 schema 缓存大小，减少频繁驱逐。
    - 将 [`AUTO_ID_CACHE`](/auto-increment.md#auto_id_cache) 设置为 `1`，以避免 ID 跳号。
    - 合理配置 `AUTO_RANDOM` 的 shard bits 和 reserved bits，避免 ID 区间过小。