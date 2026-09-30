---
title: 配置和管理分层存储
summary: 了解如何在 TiDB Cloud Premium 或 BYOC 上配置和管理分层存储，包括 DDL、分区选择器和最佳实践。
---

# 配置和管理分层存储

本文介绍如何配置和管理低频访问（IA）存储，包括存储类设置、分区选择器以及推荐的运维实践。

> **Note:**
>
> 分层存储目前对 {{{ .premium }}} 和 {{{ .byoc }}} 处于**私有预览**阶段，且默认禁用。要使用该功能，请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md) 为你的实例启用。本文所描述的行为反映的是当前预览版的实现，可能会在正式发布（GA）前发生变化。

## 如何使用 {#how-to-use}

本节介绍如何配置和管理 IA 存储，包括存储类设置、分区选择器以及推荐的运维实践。

### 存储类支持矩阵 {#storage-class-support-matrix}

本节介绍支持的存储类取值、表类型，以及索引和相关对象的继承规则。

#### 存储类取值 {#storage-class-values}

| 值 | 含义 | 默认 |
|-|-|-|
| `Standard` | 本地热存储，完整数据保存在本地磁盘 | 是 |
| `IA` | 远程冷存储，完整数据保存在对象存储中，本地按需缓存 | 否 |

取值不区分大小写。

#### 支持的表类型 {#supported-table-types}

| 表类型 | 是否支持 IA | 说明 |
|-|-|-|
| 普通非分区表 | 支持 | 通过 `STORAGE_CLASS` 语法糖或 `ENGINE_ATTRIBUTE` |
| Range 分区 | 支持 | 必须使用 `ENGINE_ATTRIBUTE` |
| Range Columns 分区 | 支持 | 必须使用 `ENGINE_ATTRIBUTE` |
| List 分区 | 支持 | 必须使用 `ENGINE_ATTRIBUTE` |
| List Columns 分区 | 支持 | 必须使用 `ENGINE_ATTRIBUTE` |
| Hash 分区 | **不支持** | — |
| Key 分区 | **不支持** | — |

#### 索引和相关对象的存储类型继承规则 {#storage-type-inheritance-rules-for-indexes-and-related-objects}

| 对象 | 继承规则 |
|-|-|
| 普通表索引 | 与表相同 |
| 分区表 Local Index | 与所属分区相同 |
| 分区表 Global Index | 与表级设置相同 |
| TiFlash | **不遵循表存储设置** |

### 普通表 DDL {#regular-table-ddl}

本节介绍如何为普通（非分区）表配置 IA 存储。

#### 在创建时指定 {#specify-at-create-time}

语法糖（推荐）：

```sql
CREATE TABLE t_ia (
    id BIGINT PRIMARY KEY,
    created_at DATETIME NOT NULL,
    payload VARCHAR(256) NOT NULL
) ENGINE=InnoDB STORAGE_CLASS='IA';
```

`ENGINE_ATTRIBUTE` 方法：

```sql
CREATE TABLE t_ia (
    id BIGINT PRIMARY KEY
) ENGINE_ATTRIBUTE='{"storage_class":"IA"}';
```

**冲突约束**：`STORAGE_CLASS` 语法糖和 `ENGINE_ATTRIBUTE` 中的 `storage_class` **不能同时指定**，否则系统会报错并拒绝执行。

#### 修改现有表 {#modify-an-existing-table}

```sql
-- Standard → IA
ALTER TABLE t1 STORAGE_CLASS='IA';
ALTER TABLE t1 ENGINE_ATTRIBUTE='{"storage_class":"IA"}';

-- IA → Standard
ALTER TABLE t1 STORAGE_CLASS='STANDARD';
ALTER TABLE t1 ENGINE_ATTRIBUTE='{"storage_class":"STANDARD"}';
```

`ALTER` 操作会保持所有数据访问能力，在转换期间支持 SQL 读写。

### 分区表 DDL {#partitioned-table-ddl}

分区表**不支持** `STORAGE_CLASS` 语法糖，必须使用 `ENGINE_ATTRIBUTE`。

分区属性支持三种选择器类型（不能混用），以及一个表级默认值：

| 配置方法 | 语法 | 适用分区类型 | 用途 |
|-|-|-|-|
| 表级默认值 | `{"storage_class":"IA"}` | 全部 | 统一将所有分区设置为 IA |
| 按分区名 | `"names_in":["p1","p2"]` | 全部 | 指定精确的分区名称列表 |
| 按范围 | `"less_than":"2024-01-01"` | RANGE / RANGE COLUMNS | 按边界值匹配分区 |
| 按列表值 | `"values_in":["1","2"]` | LIST / LIST COLUMNS | 按列表值匹配分区 |

#### 示例 A：表级 IA，并将特定分区覆盖为 Standard {#example-a-table-level-ia-with-specific-partitions-overridden-to-standard}

```sql
CREATE TABLE orders (
    order_id BIGINT NOT NULL,
    created_at DATETIME NOT NULL,
    PRIMARY KEY (order_id, created_at)
) ENGINE_ATTRIBUTE='{
    "storage_class":[
        {"tier":"ia"},
        {"tier":"standard","names_in":["p2025","p_future"]}
    ]
}'
PARTITION BY RANGE (YEAR(created_at)) (
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

结果：p2023 / p2024 → IA，p2025 / p_future → Standard。

#### 示例 B：范围选择器 {#example-b-range-selector}

```sql
CREATE TABLE users (
    user_id BIGINT NOT NULL,
    PRIMARY KEY (user_id)
) ENGINE_ATTRIBUTE='{
    "storage_class":[
        {"tier":"ia","less_than":"2000000"}
    ]
}'
PARTITION BY RANGE (user_id) (
    PARTITION p0 VALUES LESS THAN (1000000),
    PARTITION p1 VALUES LESS THAN (2000000),
    PARTITION p2 VALUES LESS THAN (3000000),
    PARTITION p3 VALUES LESS THAN MAXVALUE
);
```

结果：p0 / p1 → IA，p2 / p3 → Standard。

#### 示例 C：列表值选择器 {#example-c-list-value-selector}

```sql
CREATE TABLE order_status_log (
    log_id BIGINT NOT NULL,
    status INT NOT NULL,
    PRIMARY KEY (log_id, status)
) ENGINE_ATTRIBUTE='{
    "storage_class":[
        {"tier":"ia","values_in":["1","2"]}
    ]
}'
PARTITION BY LIST (status) (
    PARTITION p_pending VALUES IN (1),
    PARTITION p_paid VALUES IN (2),
    PARTITION p_shipped VALUES IN (3),
    PARTITION p_completed VALUES IN (4)
);
```

结果：p_pending / p_paid → IA，p_shipped / p_completed → Standard。

#### 分区选择器规则 {#partition-selector-rules}

- **优先级**：分区级配置会**覆盖**表级配置
- **互斥性**：同一个选择器中不能同时使用多种匹配方式（例如 `"names_in"` 和 `"less_than"`），否则会报错
- **前向兼容性**：后续新增的分区（`ADD PARTITION` / `REORGANIZE PARTITION`）会根据持久化的存储类规则自动进行评估；匹配到的分区会继承相应配置

### 查看和监控 {#view-and-monitor}

```sql
-- View DDL definition
SHOW CREATE TABLE t1\G

-- View table-level storage type
SELECT TABLE_NAME, TIDB_STORAGE_CLASS
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'your_database'
  AND TABLE_NAME = 'your_table';

-- View partition-level storage type
SELECT PARTITION_NAME, TIDB_STORAGE_CLASS
FROM INFORMATION_SCHEMA.PARTITIONS
WHERE TABLE_SCHEMA = 'your_database'
  AND TABLE_NAME = 'your_table';
```

#### 监控 IA 存储空间 {#monitor-ia-storage-space}

在 TiDB Cloud 控制台中查看：

- 路径：**Overview** > **Monitoring** > **Metrics** > **Instance Overview**（或 **Overview** > **Core Metrics**）
- 新增指标：
    - `Row-based IA Storage` — IA 存储类中数据的存储空间
    - `Row-based Standard Storage` — Standard 表空间总量
- 关系：`Row-based Storage` = `Row-based IA Storage` + `Row-based Standard Storage`

> **Note:**
>
> IA 存储空间只统计表的 L1 及更深层级。memtable 和 L0 文件仍保留在本地磁盘上，不计入 IA 存储。关于原因，请参见 [LSM-Tree 写入路径](/tidb-cloud/tiered-storage-overview.md#lsm-tree-write-path)。

单表空间查询方法保持不变：

> **Note:**
>
> 此方法依赖表统计信息，可能存在较大的估算误差。它还覆盖整张表，因此结果不能直接与 `Row-based IA Storage` 对比。

```sql
SELECT TABLE_NAME,
    ROUND(DATA_LENGTH / 1024 / 1024, 2) AS Data_MB,
    ROUND(INDEX_LENGTH / 1024 / 1024, 2) AS Index_MB,
    TABLE_ROWS
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'your_database'
  AND TABLE_NAME = 'your_table'
ORDER BY (DATA_LENGTH + INDEX_LENGTH) DESC;
```

### 配置 IA 缓存级别 {#configure-the-ia-cache-level}

IA 缓存级别用于控制有多少 IA 数据会缓存在本地磁盘上。级别越高，缓存的数据越多，从而提升冷读性能，但也会增加成本。

> **Note:**
>
> - 调整 IA 缓存级别除了需要启用分层存储私有预览外，还需要单独加入 allowlist。请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md) 为你的实例启用此功能。
> - 缓存级别在底层 TiKV 物理集群级别生效，而不是在单个逻辑实例级别生效。如果多个逻辑实例共享同一个物理集群，那么在一个实例上修改缓存级别会同时影响所有这些实例。在 {{{ .premium }}} 和 {{{ .byoc }}} 上，底层 TiKV 物理集群为你独享，因此不会影响其他客户。逻辑实例级别的控制计划在未来版本中提供。

| 缓存级别 | 适用场景 |
|-|-|
| **Economy** | 冷读较少，且你希望尽量降低本地磁盘成本 |
| **Default** | 系统默认值，适用于通用工作负载 |
| **Balanced** | 在成本与冷读延时之间取得平衡 |
| **Deep** | 你的工作负载对冷读延时非常敏感 |

要修改缓存级别，请执行以下操作：

1. 在 Cloud Console 中，进入 **Overview** > **Capacity**，然后点击 **Update Capacity**。
2. 在 **Storage Acceleration** 区块中，选择一个缓存级别。
3. 在 **Summary** 面板中查看成本影响，然后点击 **Update Capacity**。

此更改无需重启即可生效，通常会在一分钟内完成。TiDB Cloud 会自动为底层资源完成配置，因此你无需检查可用空间，也无需选择扩缩容方法。资源配置可能需要一些时间。

在 {{{ .premium }}} 上，每个缓存级别都有一个 IA 存储等效系数，在计算账单时会应用到你上报的 IA 存储用量，因此级别越高成本越高。在 {{{ .byoc }}} 上，不适用任何系数：额外的本地缓存资源会在你自己的云账户中配置，并由你的云服务提供商计费。各级别对应的系数，请参见 [TiDB Cloud 计费](/tidb-cloud/tidb-cloud-billing.md)。

### 调整 IA segment 大小（仅 BYOC） {#adjust-the-ia-segment-size-byoc-only}

segment 是 TiKV 从对象存储读取并写入本地缓存的最小单位。默认大小为 1 MiB。

在 {{{ .byoc }}} 上，你可以将 TiKV 配置参数 `kvengine.ia.segment-size` 设置为 `128 KiB`、`256 KiB`、`512 KiB`、`1 MiB` 或 `2 MiB`。该参数在 {{{ .premium }}} 上不可用。

`kvengine.ia.segment-size` 仅在启动时生效。修改后，请对 TiKV 节点执行滚动重启，最好安排在业务低峰期进行。

修改 segment 大小不会重写对象存储中的任何文件。SST 文件以完整对象形式存储，并不是按 segment 组织的，因此变化的只有本地磁盘上的读取粒度和缓存粒度。重启后，随着查询到来，本地缓存会按新的粒度逐步重建。

## 可观测性 {#observability}

关于 IA 可观测性，包括存储类转换进度、`EXPLAIN ANALYZE` 字段、statement summary 和慢查询指标，以及集群级别的 IA 缓存性能面板，请参见 [分层存储可观测性](/tidb-cloud/tiered-storage-observability.md)。

## 最佳实践 {#best-practices}

本节介绍 IA 存储的推荐运维实践，包括分层策略、发布策略、写入优化、查询优化、缓存级别调优、segment 大小选择、切回注意事项以及配置稳定性。

### 分层策略：优先使用分区级 IA {#tiering-strategy-prefer-partition-level-ia}

对于分区表，**始终优先使用分区级 IA**，而不是表级 IA。这样可以更精确地控制冷热边界：

- 历史冷分区（例如 `p2023`）→ IA
- 近期热分区（例如 `p2025`）→ Standard
- 未来分区（例如 `p_future`）→ Standard

### 发布策略：从最小且最旧的分区开始 {#rollout-strategy-start-with-the-smallest-oldest-partition}

```
Step 1: Select the oldest and smallest partition → ALTER PARTITION → IA
Step 2: Observe for one full business day (at least 24h)
Step 3: Verify QPS / TPS / P99 Latency / CPU metrics show no degradation
Step 4: Set the next cold partition → IA one by one
Step 5: Repeat Steps 2-4 until all target partitions are covered
```

**不要一次性将所有分区批量设置为 IA。**

### 写入优化 {#write-optimization}

- 在应用此调优前，请在相同线程数、相同工作负载和相同分区分布下，对并发写入进行基准测试。在一个测试环境中，向 IA 分区随机写入的平均速度为 50k rows/sec，而向单个 IA 分区进行固定单线程写入的平均速度为 70k rows/sec；这些结果不能直接比较。
- 新导入的数据只有在 flush/compaction 后才会切换到 IA 模式。导入后立即执行大范围查询时，可能会遇到冷缓存。

这些数据来自测试环境，并不代表真实生产场景。你应根据自身业务测试获得准确数据。

### 查询优化 {#query-optimization}

- 建议跨 IA 分区的查询**最多覆盖 3 个分区**；超过此数量可能会导致响应时间显著下降
- 避免同时在 IA 表上并发执行 `SELECT *` 全表扫描
- 通过 `EXPLAIN ANALYZE` 和慢查询监控 IA 远程读取量，并据此进行调整

### 调优 IA 缓存级别 {#tune-the-ia-cache-level}

使用 **IA Cache Hit Rate** 面板来决定是否需要修改缓存级别：

- 如果命中率持续低于 85%，请提高缓存级别。**Balanced** 是一个合理的起点。
- 每次修改后，在再次修改之前，至少观察一个完整业务日的命中率。
- 如果命中率持续较高且你希望降低成本，可以将缓存级别下调为 **Economy**。

关于此调优循环中使用的面板和语句级指标，请参见 [分层存储可观测性](/tidb-cloud/tiered-storage-observability.md)。

### 选择 segment 大小（仅 BYOC） {#choose-the-segment-size-byoc-only}

segment 大小需要在读放大和对象存储请求数量之间进行权衡：

| segment 大小 | 每次缓存未命中的读放大 | 对象存储请求数 | 适用场景 |
|-|-|-|-|
| 小于 1 MiB | 更低 | 更高 | 面向低延时对象存储的点查询，且不关注请求成本时 |
| 1 MiB（默认） | 中等 | 中等 | 通用工作负载 |
| 大于 1 MiB | 更高 | 更低 | 具有充足网络带宽的大范围扫描 |

在修改此参数之前，请先使用你自己的工作负载进行基准测试，并在业务低峰期执行滚动重启。

### 切回注意事项 {#switch-back-considerations}

- IA → Standard 转换会从对象存储下载全部数据，产生显著的冷存储带宽使用
- 监控带宽使用情况以确保平稳运行；如有必要，**请提前联系 TiDB Cloud 团队**进行联合监控
- 转换期间，业务 SQL 读写不会受到影响，但性能（例如 QPS/TPS）可能会有轻微影响——测试环境显示低于 5%
- 开始前，请查询 `mysql.tidb_storage_class_transition_history`，并按 `state = 'COMPLETED'` 过滤你集群中过去类似转换的持续时间，以估算本次变更窗口
- 转换期间，运行 `SHOW STORAGE_CLASS TRANSITIONS` 以跟踪进度并检测卡住的转换

### 配置稳定性 {#configuration-stability}

请保持存储类设置稳定，避免在 IA 和 Standard 之间频繁切换。每次切换都会触发：

- Region 重新加载
- 对象存储数据下载或元信息重建
- IA 缓存数据刷盘

这些操作的累计成本不可忽视。

如果在上一次转换仍在进行时发起反向转换，则上一次转换会失效，且其已完成的进度会被丢弃。反转一个正在进行中的转换可能会触发额外的 Region 重新加载和数据下载。部分现有本地文件可以被复用，因此额外工作量取决于转换已进行到什么程度，以及本地仍可用的数据有多少。为减少不必要的 I/O 和资源使用，请避免在 IA 和 Standard 之间频繁切换。关于如何识别失效的转换，请参见 [分层存储可观测性](/tidb-cloud/tiered-storage-observability.md)。

这适用于表或分区的存储类。调整 IA 缓存级别则是另一种操作：它属于热更新，不会在不同存储类之间移动数据，并且可以根据你的成本和性能目标按需频繁调整。