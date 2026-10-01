---
title: 分层存储限制
summary: 了解 TiDB Cloud Premium 或 BYOC 上分层存储的限制、限流、兼容性以及查询性能的不确定性。
---

# 分层存储限制

本文介绍 Infrequent Access (IA) 存储当前的限制及其运维影响，包括功能约束、冷读限流、工具兼容性以及查询性能的不确定性。

> **注意：**
>
> 分层存储目前在 {{{ .premium }}} 和 {{{ .byoc }}} 中处于**私有预览**阶段，默认关闭。如需使用，请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md) 为你的实例启用。本文描述的行为反映的是当前预览版本的实现，正式可用（GA）前可能会发生变化。

## 功能限制 {#feature-limitations}

| 限制 | 说明 |
|-|-|
| Hash / Key partitions | 不能设置为 IA |
| Index-independent setting | 不能对索引单独设置 IA |
| TTL auto-tiering | 不支持基于业务字段的冷热自动分层 |
| Syntax conflict | 不能同时指定 `STORAGE_CLASS` 和 `ENGINE_ATTRIBUTE` |
| Partition selector mixing | 不能同时使用 `names_in` / `less_than` / `values_in` |
| TiFlash | 不遵循 IA；数据始终保留在本地 |
| Cache level scope | IA 缓存级别作用于底层 TiKV 物理集群级别，而不是单个逻辑实例，也不是特定表或分区。共享同一物理集群的所有逻辑实例，都会受到其中任一实例缓存级别变更的影响。逻辑实例级别的控制计划在未来版本中提供 |
| Cache level enablement | 修改 IA 缓存级别除了需要启用分层存储私有预览外，还需要单独加入 allowlist，且默认关闭。请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md) 启用 |
| Segment size adjustment | `kvengine.ia.segment-size` 只能在 {{{ .byoc }}} 上修改，并且只有在 TiKV 节点滚动重启后才会生效 |
| Cache level provisioning | 缓存级别变更会以热更新方式生效，但底层资源由 TiDB Cloud 自动配置，这可能需要一些时间 |
| Transition progress visibility | 只有当你对该表拥有 `ALL` 权限时，`INFORMATION_SCHEMA.TIKV_STORAGE_CLASS_TRANSITIONS` 中对应的行才可见。对于你无权访问的表，其对应行会被跳过且不会报错 |
| Transition progress freshness | 转换进度每 10 秒采集一次，因此 `INFORMATION_SCHEMA.TIKV_STORAGE_CLASS_TRANSITIONS` 中的值不是实时的 |

## 访问限流约束 {#access-throttling-constraints}

由于共享物理集群的对象存储带宽有限，IA 冷存储访问必须遵守以下限制：

| 约束维度 | 限制 | 原因 |
|-|-|-|
| 单条 SQL 冷读吞吐 | ≤ 100 MiB/s | 防止单个查询占用过多带宽 |
| 并发冷读总吞吐 | ≤ 1 GiB/s (≤ 10 concurrent) | 保护集群中的其他租户 |
| TiKV 单次缓存未命中加载大小 | ≤ ~3 MiB (estimated) | 来自 3 个 LSM level 的 segment |

> **注意：**
>
> 单次 TiKV 缓存未命中并不等同于单次查询缓存未命中！例如，一个查询可能涉及多个（如 1000 个）TiKV 缓存未命中。如果由 5 个 TiKV 节点来服务该查询，则每个 TiKV 平均有 200 次缓存未命中，从而导致 200 次远程冷数据查询。尽管这些请求在每个 TiKV 内部是并发的，但 200 次缓存未命中仍然会耗费很长时间，因此最终查询延时可能会非常高。

**如果你的业务涉及持续的大量冷数据访问，不建议使用 IA；请将表切回 Standard 存储。** 为了确保系统稳定性，未来的技术版本将为冷数据访问增加硬性限流。目前，你必须遵守上述约束。

你可以通过 Cloud Console → Monitoring → Diagnosis → Slow Query → Coprocessor 中的 `IA Remote Read Segment Size` 面板监控单条 SQL 的冷数据访问量。要监控整个集群的 IA 缓存行为，请使用 [分层存储可观测性](/tidb-cloud/tiered-storage-observability.md) 中介绍的 **IA Cache Performance** 面板。

## 对外围工具的影响 {#impact-on-peripheral-tools}

| 工具 | 影响 | 兼容性 |
|-|-|-|
| **TiCDC** | 逻辑数据语义不变；初始化扫描/读取旧数据时可能有更高延时；Region 变化按正常方式处理 | 兼容 |
| **BR backup & restore** | 保留存储类元信息；恢复后 IA 表继续按 IA 语义加载 | 兼容 |
| **IMPORT INTO** | 导入的数据会通过 flush/compaction 转换到 IA；导入后的大范围校验可能遇到冷缓存 | 兼容 |
| **PITR** | 保留存储类元信息；恢复后 schema manager 会重新同步 | 兼容 |

## 风险隔离机制 {#risk-isolation-mechanisms}

在为表设置 IA 后，系统会使用以下措施对 IA 表和非 IA 表进行隔离：

**Region 级别**：

- IA 表/分区占用专用 Region，并触发必要的切分
- 相邻且存储类不同的 Region 会被限制合并，以防止冷热数据混合
- 单个 Region 要么完全是 IA，要么完全是非 IA

**计算 layer**：

- Standard 表和 IA 表在计算 layer 没有隔离——TiDB 不会针对这两类表采用单独的隔离策略

**存储 layer**：

- 冷读限速

> **注意：**
>
> 共享资源（CPU、网络、本地磁盘、对象存储带宽）无法做到完全隔离。在极端情况下，大规模 IA 扫描仍可能影响其他租户。这也是设置访问限流约束的根本原因。

## 紧急恢复方法 {#emergency-recovery-methods}

如果 IA 表出现问题，你和 TiDB Cloud 团队可以使用以下方法：

| 方法 | 场景 | 优先级 | 说明 |
|-|-|-|-|
| IA → Standard switch-back | 你发现性能无法接受 | **你的首选** | 系统会将数据重新加载到本地，绕过远程路径 |
| **Flow Control (already available)** | 控制 IA 表与对象存储之间的流量 | TiDB Cloud 团队的选择 | 通过限速保护集群稳定性；由 TiDB Cloud 团队管理 |
| Contact TiDB Cloud Support | 存储类转换卡住：`DURATION` 持续增长，而 `COMPLETED_REPLICAS` 不增加或保持为 `NULL` | 必需 | 你无法自行解决卡住的转换。关于如何检测，请参见 [分层存储可观测性](/tidb-cloud/tiered-storage-observability.md) |

## IA 本地缓存与查询性能不确定性 {#ia-local-cache-and-query-performance-uncertainty}

分层存储会维护一个本地 IA 数据缓存（由 IaManager 管理），以加速对最近访问过的冷数据的重复访问。不过，需要理解以下关键事实：

- **缓存容量可调，但缓存行为仍由系统管理**：你可以在 Cloud Console 中选择 IA 缓存级别，以控制本地磁盘上缓存多少 IA 数据。但淘汰策略仍由系统管理：你不能指定哪些数据保留在缓存中，并且缓存级别作用于底层 TiKV 物理集群，而不是单个逻辑实例、表或分区。缓存命中率取决于实际访问模式：访问集中时可能超过 95%，访问分散时则可能低于 95%。
- **IA 查询响应时间是非确定性的**：当查询命中本地缓存时，性能接近 Standard 表。但当数据必须从远程对象存储加载时（缓存未命中），每次远程请求都会增加约 500ms~2s 的延时。单次 SQL 执行可能涉及多次远程加载，导致延时累积。因此，IA 表的查询响应时间不像 Standard 表那样可预测——业务侧需要据此做好规划。
- **建议：使用分区表精确控制冷数据范围**：建议使用分区表，仅将已确认低频访问的历史分区设置为 IA，同时将活跃分区保留为 Standard。这样可以将缓存不确定性限制在一个定义明确的数据范围内，而不是让整张表的查询性能都暴露在缓存未命中的风险之下。
- **增加缓存空间意味着增加成本**：更高的缓存级别会在本地磁盘上保留更多 IA 数据，从而消耗更多本地磁盘和 TiKV 资源。在 {{{ .premium }}} 上，更高的缓存级别会增加计费的 IA 存储量。在 {{{ .byoc }}} 上，额外资源会在你自己的云账户中配置，由你的云服务提供商计费，并且需要一些时间完成配置。请根据业务需求，在冷读性能与成本之间做好权衡。

**简而言之：** IA 存储通过牺牲查询性能的可预测性来降低存储成本——这是其设计上的固有权衡。建议使用分区表精确定义哪些数据属于冷数据，并将影响限制在这些数据上。如果你的业务需要可预测的查询响应时间，请将对延时敏感的数据保留在 Standard 存储中。