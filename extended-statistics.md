---
title: Extended Statistics 介绍
summary: 学习如何使用扩展统计信息来指导优化器。
---

# Extended Statistics 介绍

TiDB 可以收集以下两种类型的统计信息。本文档描述了如何使用扩展统计信息来指导优化器。在阅读本文档之前，建议你先阅读 [Statistics 介绍](/statistics.md)。

- 基本统计：如直方图和 Count-Min Sketch 等统计信息，主要关注单个列。它们对于优化器估算查询成本至关重要。详情请参见 [Statistics 介绍](/statistics.md)。
- 扩展统计：关注指定列之间的数据相关性，当查询列存在相关性时，帮助优化器更准确地估算查询成本。

当手动或自动执行 `ANALYZE` 语句时，TiDB 默认只收集基本统计信息，不收集扩展统计信息。这是因为扩展统计信息仅在特定场景下用于优化器估算，且收集它们会带来额外的开销。

扩展统计信息默认是禁用的。若要收集扩展统计信息，首先需要启用扩展统计功能，然后逐个创建所需的扩展统计对象。对象创建后，下次执行 `ANALYZE` 语句时，TiDB 会同时收集创建对象的基本统计信息和对应的扩展统计信息。

> **Warning:**
>
> 该功能为实验性功能。不建议在生产环境中使用。此功能可能在未通知的情况下被更改或移除。如发现 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。

## 限制

在以下场景中不会收集扩展统计信息：

- 仅对索引进行统计信息收集
- 使用 `ANALYZE INCREMENTAL` 命令进行统计信息收集
- 系统变量 `tidb_enable_fast_analyze` 设置为 `true` 时进行统计信息收集

## 常用操作

### 启用扩展统计

将系统变量 `tidb_enable_extended_stats` 设置为 `ON`：

```sql
SET GLOBAL tidb_enable_extended_stats = ON;
```

该变量的默认值为 `OFF`。此设置适用于所有扩展统计对象。

### 创建扩展统计对象

扩展统计对象的创建不是一次性任务。你需要为每个扩展统计对象重复创建操作。

使用 SQL 语句 `ALTER TABLE ADD STATS_EXTENDED` 来创建扩展统计对象，语法如下：

```sql
ALTER TABLE table_name ADD STATS_EXTENDED IF NOT EXISTS stats_name stats_type(column_name, column_name...);
```

在语法中，可以指定表名、统计信息名称、统计类型和扩展统计对象的列名。

- `table_name` 指定要收集扩展统计的表名。
- `stats_name` 指定统计对象的名称，必须在每个表中唯一。
- `stats_type` 指定统计类型，目前只支持相关性（correlation）类型。
- `column_name` 指定列组，可能包含多个列，目前最多支持两个列名。

<details>
<summary> How it works</summary>

为了提升访问性能，每个 TiDB 节点在系统表 `mysql.stats_extended` 中维护扩展统计信息的缓存。创建扩展统计对象后，下次执行 `ANALYZE` 时，TiDB 会在系统表 `mysql.stats_extended` 中存在对应对象时，收集扩展统计信息。

`mysql.stats_extended` 表中的每一行有一个 `version` 列。每当一行被更新，`version` 的值就会增加。这样，TiDB 逐步将表加载到内存中，而不是一次性全部加载。

TiDB 会定期加载 `mysql.stats_extended`，以确保缓存与表中的数据保持一致。

> **Warning:**
>
> **不建议** 直接操作 `mysql.stats_extended` 系统表，否则会导致不同 TiDB 节点上的缓存不一致。
>
> 如果误操作了该表，可以在每个 TiDB 节点执行以下语句，清除当前缓存并重新加载 `mysql.stats_extended` 表：
>
> ```sql
> ADMIN RELOAD STATS_EXTENDED;
> ```

</details>

### 删除扩展统计对象

删除扩展统计对象，可以使用以下语句：

```sql
ALTER TABLE table_name DROP STATS_EXTENDED stats_name;
```

<details>
<summary>How it works</summary>

执行该语句后，TiDB 会将 `mysql.stats_extended` 中对应对象的 `status` 列的值标记为 `2`，而不是直接删除对象。

其他 TiDB 节点会读取此变化，并在其内存缓存中删除对应对象。后台的垃圾回收机制最终会删除该对象。

> **Warning:**
>
> **不建议** 直接操作 `mysql.stats_extended` 系统表，否则会导致不同 TiDB 节点上的缓存不一致。
>
> 如果误操作了该表，可以在每个 TiDB 节点执行以下语句，清除当前缓存并重新加载 `mysql.stats_extended` 表：
>
> ```sql
> ADMIN RELOAD STATS_EXTENDED;
> ```

</details>

### 导出和导入扩展统计

导出或导入扩展统计的方法与基本统计信息的导出导入相同。详情请参见 [Statistics 介绍 - 导入导出统计信息](/statistics.md#export-and-import-statistics)。

## 相关性类型扩展统计的使用示例

目前，TiDB 仅支持相关性（correlation）类型的扩展统计信息。该类型用于估算范围查询的行数，并优化索引选择。以下示例展示了如何使用相关性类型的扩展统计信息估算范围查询的行数。

### 第一步：定义表

定义表 `t` 如下：

```sql
CREATE TABLE t(col1 INT, col2 INT, KEY(col1), KEY(col2));
```

假设表 `t` 的 `col1` 和 `col2` 在行序中都遵循单调递增约束。这意味着 `col1` 和 `col2` 的值在顺序上严格相关，相关系数为 `1`。

### 第二步：执行不使用扩展统计的示例查询

执行以下不使用扩展统计的查询：

```sql
SELECT * FROM t WHERE col1 > 1 ORDER BY col2 LIMIT 1;
```

对于上述查询，TiDB 优化器有以下几种访问表 `t` 的方案：

- 使用 `col1` 上的索引访问表 `t`，然后按 `col2` 排序以计算 `Top-1`。
- 使用 `col2` 上的索引，找到满足 `col1 > 1` 的第一行。此访问方式的成本主要取决于 TiDB 在 `col2` 顺序扫描时过滤掉的行数。

没有扩展统计信息时，TiDB 优化器假设 `col1` 和 `col2` 独立，这会导致**估算误差较大**。

### 第三步：启用扩展统计信息

将 `tidb_enable_extended_stats` 设置为 `ON`，并为 `col1` 和 `col2` 创建扩展统计对象：

```sql
ALTER TABLE t ADD STATS_EXTENDED s1 correlation(col1, col2);
```

在创建对象后执行 `ANALYZE`，TiDB 会计算表 `t` 中 `col1` 和 `col2` 的 [Pearson 相关系数](https://en.wikipedia.org/wiki/Pearson_correlation_coefficient)，并将对象写入 `mysql.stats_extended` 表。

### 第四步：观察扩展统计带来的差异

在 TiDB 获取到相关性扩展统计后，优化器可以更精确地估算扫描的行数。

此时，对于 [第二步：执行不使用扩展统计的示例查询](#第二步：执行不使用扩展统计的示例查询)，`col1` 和 `col2` 在顺序上严格相关。如果 TiDB 使用 `col2` 上的索引访问表 `t`，找到满足 `col1 > 1` 的第一行，优化器会将行数估算转化为如下查询：

```sql
SELECT * FROM t WHERE col1 <= 1 OR col1 IS NULL;
```

上述查询的结果加一即为最终的行数估算。这样，就避免了假设独立带来的**估算误差**。

如果相关系数（此例为 `1`）小于系统变量 `tidb_opt_correlation_threshold` 的值，优化器会采用假设独立的方式进行估算，但会在 heuristically 增加估算结果。`tidb_opt_correlation_exp_factor` 的值越大，估算结果越大。相关系数的绝对值越大，估算结果也越大。