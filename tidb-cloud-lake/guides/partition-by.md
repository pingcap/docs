---
title: Fuse 表分区
summary: 了解如何在 TiDB Cloud Lake 中对 Fuse 表进行分区，以实现更快的查询裁剪和可预测的数据布局。
---

# 对 Fuse 表进行分区以实现更快的裁剪和可预测的数据布局

`PARTITION BY` 会将 Fuse 表在物理上拆分为多个分区。{{{ .lake }}} 会将不同分区值对应的 block 和 segment 分开存储，在元信息中记录分区值，并裁剪不可能匹配查询谓词的分区。

当大型表经常按时间范围、租户或 region 标识符，或其他稳定维度进行过滤时，适合使用分区。对于高基数键，请使用 `BUCKET()` 创建固定数量的哈希分区。

## 它解决了什么问题？ {#what-problem-does-it-solve}

| 问题 | 影响 | `PARTITION BY` 解决方案 |
|---------|--------|-------------------------|
| 查询只针对大表中的一小部分数据 | 必须检查无关的 segment 和 block | 分区元信息会在扫描前排除无关分区 |
| 时序数据跨越很多天或很多月 | 查询最近时间段时会读取历史数据 | 日期表达式会将数据归入时间分区 |
| 自然键具有非常高的基数 | 每个值一个分区会造成过度碎片化 | `BUCKET()` 将值映射到固定数量的哈希分区 |
| 分布式写入器产生许多小 block | 同一分区可能会在多个节点上被独立写入 | 哈希写入分布会将每个分区值路由到一个写入器 |

## 分区与聚簇 {#partitioning-vs-clustering}

`PARTITION BY` 和 `CLUSTER BY` 是互补的：

| 特性 | `PARTITION BY` | `CLUSTER BY` |
|---------|----------------|--------------|
| 物理保证 | block 和 segment 不会跨越分区边界 | 行会按顺序排列，相关值会被放置在一起 |
| 主要收益 | 分区级裁剪和隔离 | 分区内细粒度的 block 裁剪 |
| 典型基数 | 低或有上界 | 中到高 |
| 典型表达式 | `DATE_TRUNC(day, event_time)`, `region`, `BUCKET(32, customer_id)` | `event_time`, `customer_id`, `(region, event_time)` |
| 维护方式 | 由写入、变异、压实和重新聚簇保持 | 通过聚簇和重新聚簇维护 |

你可以在同一张表上同时使用两者。分区键不会成为用户可见 cluster key 的一部分：

```sql
CREATE TABLE events (
    event_time TIMESTAMP,
    tenant_id  BIGINT,
    payload    VARIANT
)
PARTITION BY (DATE_TRUNC(day, event_time))
CLUSTER BY (tenant_id, event_time);
```

## 快速设置 {#quick-setup}

创建一张按天分区的表：

```sql
CREATE TABLE events (
    event_id   BIGINT,
    event_time TIMESTAMP,
    event_type STRING
)
PARTITION BY (DATE_TRUNC(day, event_time));
```

后续所有写入都会遵循分区边界：

```sql
INSERT INTO events VALUES
    (1, '2026-07-08 10:00:00', 'login'),
    (2, '2026-07-08 18:30:00', 'purchase'),
    (3, '2026-07-09 09:15:00', 'logout');
```

这样，时间谓词就可以裁剪无关的按天分区：

```sql
EXPLAIN
SELECT *
FROM events
WHERE event_time >= TIMESTAMP '2026-07-08'
  AND event_time <  TIMESTAMP '2026-07-09';
```

在 `EXPLAIN` 输出中，比较 `partitions total` 和 `partitions scanned`，并检查 `range pruning` 统计信息。被扫描的分区越少，说明已应用分区裁剪。

## 分区策略 {#partitioning-strategies}

本节介绍在 {{{ .lake }}} 中对 Fuse 表进行分区的不同策略。

### 基于时间的分区 {#time-based-partitioning}

对时间戳或日期列应用确定性表达式：

```sql
-- Daily partitions
PARTITION BY (DATE_TRUNC(day, event_time))

-- Monthly partitions
PARTITION BY (DATE_TRUNC(month, event_time))
```

选择与常见过滤条件匹配的粒度，同时确保每个分区足够大，以避免碎片化。按天分区通常适合高吞吐事件数据；按月分区通常更适合低吞吐的历史数据。

### 标识分区 {#identity-partitioning}

当某列本身已经具有较小且稳定的取值集合时，可以直接使用该列：

```sql
CREATE TABLE regional_sales (
    region     STRING,
    order_id   BIGINT,
    order_date DATE,
    amount     DECIMAL(18, 2)
)
PARTITION BY (region);
```

适合作为标识键的包括 region、国家、租户层级，或其他有界的业务维度。避免直接按唯一 ID 分区。

### 使用 `BUCKET()` 的哈希分区 {#hash-partitioning-with-bucket}

`BUCKET(<count>, <column>)` 会以确定性方式将支持的值映射为无符号分区编号，范围为 `0` 到 `<count> - 1`。bucket 数必须是 `1` 到 `4294967295` 之间的常量整数型。

```sql
CREATE TABLE customer_events (
    customer_id BIGINT,
    event_time  TIMESTAMP,
    payload     VARIANT
)
PARTITION BY (BUCKET(32, customer_id));
```

当等值过滤针对高基数列，但为每个不同值创建一个物理分区又不切实际时，bucket 分区非常有用。

`BUCKET()` 支持的值类型包括整数型、字符串、日期和时间戳。详情请参见 [BUCKET](/tidb-cloud-lake/sql/bucket.md)。

### 复合分区 {#composite-partitioning}

列出多个表达式以形成复合分区键：

```sql
CREATE TABLE tenant_events (
    tenant_id  BIGINT,
    event_time TIMESTAMP,
    payload    VARIANT
)
PARTITION BY (
    DATE_TRUNC(month, event_time),
    BUCKET(16, tenant_id)
);
```

每个分区表达式必须且只能引用一个源列。若要按两列分区，请像上面那样使用独立表达式；像 `tenant_id + another_id` 这样的表达式无效。

## 哈希分布式写入 {#hash-distributed-writes}

对于向分区表进行分布式或高并行导入的场景，请设置 `WRITE_DISTRIBUTION_MODE = 'hash'`：

```sql
CREATE TABLE customer_events (
    customer_id BIGINT,
    event_time  TIMESTAMP,
    payload     VARIANT
)
PARTITION BY (BUCKET(32, customer_id))
WRITE_DISTRIBUTION_MODE = 'hash';
```

该模式会对计算后的分区键进行哈希，并在本地排序之前，将具有相同分区值的行路由到同一个写入器。当多个节点或管道并发写入相同分区时，它可以减少小 block 碎片。

`WRITE_DISTRIBUTION_MODE` 支持以下取值：

- `'none'`（默认）：写入前不重新分发行。
- `'hash'`：写入前按分区键重新分发行。该值要求使用 `PARTITION BY`。

哈希重分发会增加一次网络 shuffle。对于分布式或并行负载，如果改进后的 block 布局收益大于 shuffle 成本，则应启用它；对于小规模、单写入器的插入，它可能没有收益。

> **Note:**
>
> 如果没有哈希分布，未排序输入会很慢。在默认的 `WRITE_DISTRIBUTION_MODE = 'none'` 下，行会按照到达顺序写入。如果输入按行混合了不同的分区值，{{{ .lake }}} 会写出许多非常小的 block，导致负载变慢。你可以在表上设置 `WRITE_DISTRIBUTION_MODE = 'hash'`，或者按分区键对输入进行排序：
>
> ```sql
> INSERT INTO events SELECT ... FROM source ORDER BY DATE_TRUNC(day, event_time);
> ```

## 向现有表添加分区键 {#adding-a-partition-key-to-an-existing-table}

`ALTER TABLE ... PARTITION BY` 只会修改表定义。现有数据不会被重新分布，之后执行 `OPTIMIZE TABLE` 或 `RECLUSTER` 也不会重新分布这些数据。只有在变更之后写入的数据才会被分区。

| 表 | 结果 |
|---|---|
| 空表 | 推荐。之后加载的所有数据都会被分区。 |
| 有数据 | 可以成功，但现有数据不会被裁剪，并且对现有行执行 `UPDATE`、`DELETE` 或 `MERGE INTO` 会因 `serialized block contains more than one partition` 而失败。请按下文所示重写数据。 |
| 具有相同键 | 无变化。 |
| 具有不同键 | 会失败，并报错 `PARTITION BY is already defined ...; changing it is not supported`。请先删除该键。 |
| 不是 Fuse 表 | 会失败，并报错 `ALTER TABLE PARTITION BY is not supported for engine ...`。 |

**空表：**添加该键，然后加载数据。

```sql
ALTER TABLE events PARTITION BY (DATE_TRUNC(month, event_time));
INSERT INTO events SELECT * FROM source;
```

**有数据的表：**添加该键，然后重写表。请保留 `ORDER BY`；如果没有它，重写会写入非常小的数据块，速度会很慢。

```sql
ALTER TABLE events PARTITION BY (DATE_TRUNC(month, event_time));
INSERT OVERWRITE events SELECT * FROM events ORDER BY DATE_TRUNC(month, event_time);
```

**修改该键：**先删除它，再添加新键，然后重写表。

```sql
ALTER TABLE events DROP PARTITION KEY;
ALTER TABLE events PARTITION BY (DATE_TRUNC(day, event_time));
INSERT OVERWRITE events SELECT * FROM events ORDER BY DATE_TRUNC(day, event_time);
```

`DROP PARTITION KEY` 不会重写数据。它会停止分区裁剪，并将 `WRITE_DISTRIBUTION_MODE` 重置为 `'none'`。

## 修改一行的分区键值 {#updating-the-partition-key-value-of-a-row}

`UPDATE` 和 `MERGE INTO` 可以修改一行的分区键值。该行会移动到其新值对应的分区中。无需额外操作。

```sql
-- Moves the row from the September partition to the October partition.
UPDATE events SET event_time = '2026-10-05 12:00:00' WHERE event_id = 42;
```

移动一行会重写该行，因此其开销比原地修改更高。

## 表达式规则和表变更 {#expression-rules-and-table-changes}

对于 Fuse 表分区表达式：

- 每个表达式都必须是确定性的，并且只能引用一个源列。
- 对于复合分区，请使用多个表达式，而不是一个多列表达式。
- `BUCKET()` 要求存储桶数量为从 `1` 到 `4294967295` 的常量。
- 分区键引用的列不能被删除，也不能修改其数据类型。
- 重命名被引用的列时，会同步修改已存储的分区表达式。
- 内部 `partition_by` 元信息不能通过 `SET OPTIONS` 修改。
- `PARTITION BY` 支持用于 Fuse 表。其他引擎可能会实现不同的分区语法和语义。

## 最佳实践 {#best-practices}

| 实践 | 原因 |
|----------|--------------|
| 让分区表达式匹配常用过滤条件 | 使优化器能够尽早消除分区 |
| 优先选择低基数或有界基数 | 避免产生过多的小分区和元信息 |
| 对高基数等值键使用 `BUCKET()` | 使分区数量保持可预测 |
| 将分区与 cluster key 结合使用 | 在每个分区内增加细粒度裁剪 |
| 使用具有代表性的摄取并发进行测试 | 判断哈希分布写入是否能减少碎片 |
| 使用 `EXPLAIN` 进行验证 | 确认谓词能够减少 `partitions scanned` |

> **Tip:**
>
> 适合的场景：
>
> - 按天或按月过滤的事件表和日志表
> - 按租户过滤的多租户表
> - 取值范围有界的区域性或类别型数据集
> - 使用固定存储桶数量的高基数等值查找

> **Note:**
>
> **不适合分区的情况：**小表、没有稳定过滤模式的表，以及会产生大量微小分区的键，通常都无法从物理分区中获益。在这些情况下，仅使用 [cluster key](/tidb-cloud-lake/guides/cluster-key-performance.md) 可能更合适。