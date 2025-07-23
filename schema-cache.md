---
title: Schema Cache
summary: TiDB 采用基于 LRU（最近最少使用）机制的 schema 缓存机制，在数据库和表数量较多的场景下，显著降低内存使用并提升性能。
---

# Schema Cache

在一些多租户场景中，可能存在数十万甚至上百万个数据库和表。将所有这些数据库和表的 schema 信息加载到内存中，不仅会消耗大量内存，还会降低访问性能。为了解决这一问题，TiDB 引入了类似于 LRU（最近最少使用）的 schema 缓存机制。只有最近访问的数据库和表的 schema 信息会被缓存到内存中。

> **Note:**
>
> 当前，该功能在 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

## 配置 schema cache

你可以通过配置系统变量 [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800) 来启用 schema 缓存功能。

## 最佳实践

- 在数据库和表数量较多（例如超过 10 万个数据库和表）或数量足够大以影响系统性能的场景下，建议启用 schema 缓存功能。
- 你可以通过观察 TiDB Dashboard 中 **Schema load** 部分下的 **Infoschema v2 Cache Operation** 子面板，监控 schema 缓存的命中率。如果命中率较低，可以增加 [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800) 的值。
- 你可以通过观察 TiDB Dashboard 中 **Schema load** 部分下的 **Infoschema v2 Cache Size** 子面板，监控当前使用的 schema 缓存大小。

<CustomContent platform="tidb">

- 建议禁用 [`performance.force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v657-and-v710)，以减少 TiDB 启动时间。
- 如果需要创建大量表（例如超过 10 万个表），建议将 [`split-table`](/tidb-configuration-file.md#split-table) 参数设置为 `false`，以减少 Regions 数量，从而降低 TiKV 的内存使用。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 建议禁用 [`performance.force-init-stats`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file/#force-init-stats-new-in-v657-and-v710)，以减少 TiDB 启动时间。
- 如果需要创建大量表（例如超过 10 万个表），建议将 [`split-table`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file/#split-table) 参数设置为 `false`，以减少 Regions 数量，从而降低 TiKV 的内存使用。

</CustomContent>

## 已知限制

在数据库和表数量较多的场景下，存在以下已知问题：

- 单个集群中的表数量不能超过 300 万。
- 如果单个集群中的表数量超过 30 万，不要将 [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-new-in-v800) 设置为 `0`，否则可能导致 TiDB 内存溢出（OOM）。
- 使用外键可能会增加集群中 DDL 操作的执行时间。
- 当表的访问不规律，例如一组表在 time1 被访问，另一组在 time2 被访问，且 `tidb_schema_cache_size` 的值较小时，schema 信息可能频繁被驱逐和缓存，导致性能波动。此功能更适合频繁访问且相对固定的数据库和表场景。
- 统计信息可能无法及时采集。
- 访问某些元数据信息可能变慢。
- 开启或关闭 schema cache 需要等待一段时间。
- 涉及枚举所有元数据信息的操作可能变慢，例如：

    - `SHOW FULL TABLES`
    - `FLASHBACK`
    - `ALTER TABLE ... SET TIFLASH MODE ...`

- 当你使用带有 [`AUTO_INCREMENT`](/auto-increment.md) 或 [`AUTO_RANDOM`](/auto-random.md) 属性的表时，较小的 schema 缓存大小可能导致这些表的元数据频繁进入和退出缓存，从而使分配的 ID 范围在未用完之前变得无效，导致 ID 跳跃。在写入密集型场景下，甚至可能耗尽 ID 范围。为减少异常 ID 分配行为并提升系统稳定性，建议采取以下措施：

    - 查看监控面板上的命中率和 schema 缓存大小，评估缓存设置是否合理。适当增加 schema 缓存大小以减少频繁驱逐。
    - 将 [`AUTO_ID_CACHE`](/auto-increment.md#auto_id_cache) 设置为 `1`，以防止 ID 跳跃。
    - 合理配置 `AUTO_RANDOM` 的 shard bits 和 reserved bits，避免 ID 范围过小。

