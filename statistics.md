---
title: 统计信息简介
summary: 学习统计信息如何收集表级和列级信息。
---

# 统计信息简介

TiDB 使用统计信息作为优化器的输入，用于估算 SQL 语句每个执行计划步骤中处理的行数。优化器会估算每个可用执行计划的成本，包括 [索引访问](/choose-index.md) 和表连接的顺序，并为每个可用计划生成一个成本值。然后，优化器选择总体成本最低的执行计划。

## 收集统计信息

本节介绍两种收集统计信息的方式：自动更新和手动收集。

### 自动更新

对于 [`INSERT`](/sql-statements/sql-statement-insert.md)、[`DELETE`](/sql-statements/sql-statement-delete.md) 或 [`UPDATE`](/sql-statements/sql-statement-update.md) 语句，TiDB 会自动更新统计信息中的行数和已修改行数。

<CustomContent platform="tidb">

TiDB 会定期持久化更新信息，更新周期为 20 * [`stats-lease`](/tidb-configuration-file.md#stats-lease)。`stats-lease` 的默认值为 `3s`。如果你将该值设置为 `0`，TiDB 将停止自动更新统计信息。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB 每 60 秒持久化一次更新信息。

</CustomContent>

根据表的数据变更量，TiDB 会自动调度 [`ANALYZE`](/sql-statements/sql-statement-analyze-table.md) 对这些表收集统计信息。该行为由以下系统变量控制。

|  系统变量 | 默认值 | 描述 |
|---|---|---|
| [`tidb_auto_analyze_concurrency`](/system-variables.md#tidb_auto_analyze_concurrency-new-in-v840) | `1` | TiDB 集群内自动分析操作的并发度。 |
| [`tidb_auto_analyze_end_time`](/system-variables.md#tidb_auto_analyze_end_time)   | `23:59 +0000` | TiDB 可执行自动更新的每日结束时间。 |
| [`tidb_auto_analyze_partition_batch_size`](/system-variables.md#tidb_auto_analyze_partition_batch_size-new-in-v640) | `8192` | TiDB 在分析分区表时（即自动更新分区表统计信息时）自动分析的分区数。 |
| [`tidb_auto_analyze_ratio`](/system-variables.md#tidb_auto_analyze_ratio) | `0.5` | 自动更新的阈值。 |
| [`tidb_auto_analyze_start_time`](/system-variables.md#tidb_auto_analyze_start_time) | `00:00 +0000` | TiDB 可执行自动更新的每日开始时间。 |
| [`tidb_enable_auto_analyze`](/system-variables.md#tidb_enable_auto_analyze-new-in-v610) | `ON` | 控制 TiDB 是否自动执行 `ANALYZE`。 |
| [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800) | `ON` | 控制是否启用优先队列调度自动收集统计信息的任务。启用后，TiDB 优先为更有价值的表收集统计信息，如新建索引和分区发生变更的分区表。此外，TiDB 会优先处理健康度较低的表，将其排在队列前面。 |
| [`tidb_enable_stats_owner`](/system-variables.md#tidb_enable_stats_owner-new-in-v840) | `ON` | 控制对应的 TiDB 实例是否可以运行自动统计信息更新任务。 |
| [`tidb_max_auto_analyze_time`](/system-variables.md#tidb_max_auto_analyze_time-new-in-v610) | `43200`（12 小时） | 自动 `ANALYZE` 任务的最大执行时间，单位为秒。 |

当表中 `tbl` 的已修改行数与总行数的比值大于 `tidb_auto_analyze_ratio`，且当前时间在 `tidb_auto_analyze_start_time` 和 `tidb_auto_analyze_end_time` 之间时，TiDB 会在后台执行 `ANALYZE TABLE tbl` 语句，自动更新该表的统计信息。

为避免频繁修改小表数据时频繁触发自动更新，当表的行数小于 1000 时，TiDB 不会因修改而触发自动更新。你可以使用 `SHOW STATS_META` 语句查看表的行数。

> **注意：**
>
> 目前，自动更新不会记录手动 `ANALYZE` 时输入的配置项。因此，当你使用 [`WITH`](/sql-statements/sql-statement-analyze-table.md) 语法控制 `ANALYZE` 的收集行为时，需要手动设置定时任务收集统计信息。

### 手动收集

目前，TiDB 以全量方式收集统计信息。你可以执行 `ANALYZE TABLE` 语句来收集统计信息。

你可以使用以下语法进行全量收集。

+ 收集 `TableNameList` 中所有表的统计信息：

    ```sql
    ANALYZE TABLE TableNameList [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

+ `WITH NUM BUCKETS` 指定生成直方图的最大桶数。
+ `WITH NUM TOPN` 指定生成的 `TOPN` 的最大数量。
+ `WITH NUM CMSKETCH DEPTH` 指定 CM Sketch 的深度。
+ `WITH NUM CMSKETCH WIDTH` 指定 CM Sketch 的宽度。
+ `WITH NUM SAMPLES` 指定样本数量。
+ `WITH FLOAT_NUM SAMPLERATE` 指定采样率。

`WITH NUM SAMPLES` 和 `WITH FLOAT_NUM SAMPLERATE` 分别对应两种不同的采样算法。

详细说明请参见 [直方图](#histogram)、[Top-N](#top-n) 和 [CMSketch](#count-min-sketch)（Count-Min Sketch）。关于 `SAMPLES`/`SAMPLERATE`，参见 [提升收集性能](#improve-collection-performance)。

关于持久化选项以便复用的信息，参见 [持久化 `ANALYZE` 配置](#persist-analyze-configurations)。

## 统计信息类型

本节介绍三种统计信息类型：直方图、Count-Min Sketch 和 Top-N。

### 直方图

直方图统计信息被优化器用于估算区间或范围谓词的选择性，也可能用于统计信息版本 2 中估算等值/IN 谓词时确定列中不同值的数量（参见 [统计信息版本](#versions-of-statistics)）。

直方图是一种对数据分布的近似表示。它将整个取值范围划分为一系列桶，并用简单的数据描述每个桶，例如落入该桶的值的数量。在 TiDB 中，会为每个表的特定列创建等深直方图。等深直方图可用于估算区间查询。

这里的“等深”指的是每个桶中落入的值的数量尽可能相等。例如，对于集合 {1.6, 1.9, 1.9, 2.0, 2.4, 2.6, 2.7, 2.7, 2.8, 2.9, 3.4, 3.5}，如果要生成 4 个桶，则等深直方图为 [1.6, 1.9]、[2.0, 2.6]、[2.7, 2.8]、[2.9, 3.5]，每个桶的深度为 3。

![等深直方图示例](/media/statistics-1.png)

关于决定直方图桶数上限的参数，参见 [手动收集](#manual-collection)。桶数越多，直方图的精度越高；但更高的精度会消耗更多内存资源。你可以根据实际场景适当调整该值。

### Count-Min Sketch

> **注意：**
>
> Count-Min Sketch 仅在统计信息版本 1 中用于等值/IN 谓词选择性估算。在版本 2 中，由于管理 Count-Min Sketch 以避免哈希冲突存在挑战，已改用直方图统计信息。

Count-Min Sketch 是一种哈希结构。在处理如 `a = 1` 的等值查询或 `IN` 查询（如 `a IN (1, 2, 3)`）时，TiDB 使用该数据结构进行估算。

由于 Count-Min Sketch 是哈希结构，可能会发生哈希冲突。在 [`EXPLAIN`](/sql-statements/sql-statement-explain.md) 语句中，如果等值查询的估算值与实际值偏差很大，可能是因为大值和小值被哈希到了一起。此时，你可以通过以下方式避免哈希冲突：

- 修改 `WITH NUM TOPN` 参数。TiDB 会将高频（前 x 个）数据单独存储，其余数据存储在 Count-Min Sketch 中。因此，为防止大值和小值被哈希到一起，可以增大 `WITH NUM TOPN` 的值。在 TiDB 中，默认值为 20，最大值为 1024。关于该参数的更多信息，参见 [手动收集](#manual-collection)。
- 修改 `WITH NUM CMSKETCH DEPTH` 和 `WITH NUM CMSKETCH WIDTH` 两个参数。二者均影响哈希桶数量和冲突概率。你可以根据实际场景适当增大这两个参数的值，以降低哈希冲突概率，但会增加统计信息的内存占用。在 TiDB 中，`WITH NUM CMSKETCH DEPTH` 默认值为 5，`WITH NUM CMSKETCH WIDTH` 默认值为 2048。关于这两个参数的更多信息，参见 [手动收集](#manual-collection)。

### Top-N

Top-N 值是指某一列或索引中出现次数最多的前 N 个值。Top-N 统计信息通常也称为频率统计或数据倾斜。

TiDB 会记录 Top-N 值及其出现次数。`N` 由 `WITH NUM TOPN` 参数控制，默认值为 20，即收集出现频率最高的前 20 个值。最大值为 1024。关于该参数的详细信息，参见 [手动收集](#manual-collection)。

## 选择性统计信息收集

本节介绍如何有选择地收集统计信息。

### 收集索引统计信息

要收集 `TableName` 中 `IndexNameList` 所有索引的统计信息，可使用以下语法：

```sql
ANALYZE TABLE TableName INDEX [IndexNameList] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
```

当 `IndexNameList` 为空时，该语法会收集 `TableName` 中所有索引的统计信息。

> **注意：**
>
> 为保证收集前后统计信息一致，当 `tidb_analyze_version` 为 `2` 时，该语法会收集索引列及所有索引的统计信息。

### 收集部分列的统计信息

在执行 SQL 语句时，优化器大多数情况下只会用到部分列的统计信息。例如，出现在 `WHERE`、`JOIN`、`ORDER BY` 和 `GROUP BY` 子句中的列，这些列称为谓词列（predicate columns）。

如果表中列很多，收集所有列的统计信息会带来较大开销。为降低开销，你可以只为特定列（自定义选择）或 `PREDICATE COLUMNS`（谓词列）收集统计信息，以供优化器使用。若需持久化任意子集列的列表以便后续复用，参见 [持久化列配置](#persist-column-configurations)。

> **注意：**
>
> - 仅在 [`tidb_analyze_version = 2`](/system-variables.md#tidb_analyze_version-new-in-v510) 时，才支持收集谓词列的统计信息。
> - 从 TiDB v7.2.0 起，TiDB 引入了 [`tidb_analyze_skip_column_types`](/system-variables.md#tidb_analyze_skip_column_types-new-in-v720) 系统变量，用于指定在执行 `ANALYZE` 命令收集统计信息时跳过哪些类型的列。该变量仅适用于 `tidb_analyze_version = 2`。

- 若要收集指定列的统计信息，使用以下语法：

    ```sql
    ANALYZE TABLE TableName COLUMNS ColumnNameList [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

    其中，`ColumnNameList` 指定目标列名列表。若需指定多个列名，使用英文逗号 `,` 分隔。例如：`ANALYZE table t columns a, b`。该语法除了收集指定表中指定列的统计信息外，还会同时收集该表的索引列及所有索引的统计信息。

- 若要收集 `PREDICATE COLUMNS` 的统计信息，使用以下语法：

    ```sql
    ANALYZE TABLE TableName PREDICATE COLUMNS [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

    <CustomContent platform="tidb">

    TiDB 每 100 * [`stats-lease`](/tidb-configuration-file.md#stats-lease) 会将 `PREDICATE COLUMNS` 信息写入 [`mysql.column_stats_usage`](/mysql-schema/mysql-schema.md#statistics-system-tables) 系统表。

    </CustomContent>

    <CustomContent platform="tidb-cloud">

    TiDB 每 300 秒会将 `PREDICATE COLUMNS` 信息写入 [`mysql.column_stats_usage`](/mysql-schema/mysql-schema.md#statistics-system-tables) 系统表。

    </CustomContent>

    除了收集指定表的 `PREDICATE COLUMNS` 统计信息外，该语法还会同时收集该表的索引列及所有索引的统计信息。

    > **注意：**
    >
    > - 如果 [`mysql.column_stats_usage`](/mysql-schema/mysql-schema.md#statistics-system-tables) 系统表中未记录该表的任何 `PREDICATE COLUMNS`，则上述语法会收集该表的索引列及所有索引的统计信息。
    > - 被排除在收集之外的列（无论是手动指定列还是使用 `PREDICATE COLUMNS`）不会被覆盖其统计信息。当执行新类型的 SQL 查询时，优化器会使用这些列的旧统计信息（若存在），或使用伪列统计信息（若从未收集过统计信息）。下次使用 `PREDICATE COLUMNS` 执行 ANALYZE 时，会收集这些列的统计信息。

- 若要收集所有列及索引的统计信息，使用以下语法：

    ```sql
    ANALYZE TABLE TableName ALL COLUMNS [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

### 收集分区统计信息

- 若要收集 `TableName` 中 `PartitionNameList` 所有分区的统计信息，使用以下语法：

    ```sql
    ANALYZE TABLE TableName PARTITION PartitionNameList [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

- 若要收集 `TableName` 中 `PartitionNameList` 所有分区的索引统计信息，使用以下语法：

    ```sql
    ANALYZE TABLE TableName PARTITION PartitionNameList INDEX [IndexNameList] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

- 如果你只需[收集部分分区的部分列统计信息](/statistics.md#collect-statistics-on-some-columns)，使用以下语法：

    ```sql
    ANALYZE TABLE TableName PARTITION PartitionNameList [COLUMNS ColumnNameList|PREDICATE COLUMNS|ALL COLUMNS] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

#### 动态裁剪模式下收集分区表统计信息

在 [动态裁剪模式](/partitioned-table.md#dynamic-pruning-mode)（自 v6.3.0 起为默认）下访问分区表时，TiDB 会收集表级统计信息，即分区表的全局统计信息。目前，全局统计信息是从所有分区的统计信息聚合而来。在动态裁剪模式下，表中任一分区的统计信息更新都可能触发该表全局统计信息的更新。

如果部分分区的统计信息为空，或部分分区缺少某些列的统计信息，则收集行为由 [`tidb_skip_missing_partition_stats`](/system-variables.md#tidb_skip_missing_partition_stats-new-in-v730) 变量控制：

- 当触发全局统计信息更新且 [`tidb_skip_missing_partition_stats`](/system-variables.md#tidb_skip_missing_partition_stats-new-in-v730) 为 `OFF` 时：

    - 若部分分区无统计信息（如新建分区从未分析过），全局统计信息生成会中断，并显示警告，提示分区无统计信息。

    - 若部分分区缺少某些列的统计信息（这些分区分析时指定了不同的列），在聚合这些列的统计信息时，全局统计信息生成会中断，并显示警告，提示部分分区缺少某些列的统计信息。

- 当触发全局统计信息更新且 [`tidb_skip_missing_partition_stats`](/system-variables.md#tidb_skip_missing_partition_stats-new-in-v730) 为 `ON` 时：

    - 若部分分区缺少全部或部分列的统计信息，TiDB 在生成全局统计信息时会跳过这些缺失的分区统计信息，不影响全局统计信息的生成。

在动态裁剪模式下，分区和表的 `ANALYZE` 配置应保持一致。因此，如果你在 `ANALYZE TABLE TableName PARTITION PartitionNameList` 语句后指定了 `COLUMNS` 配置，或在 `WITH` 后指定了 `OPTIONS` 配置，TiDB 会忽略这些配置并返回警告。

## 提升收集性能

> **注意：**
>
> - TiDB 中 `ANALYZE TABLE` 的执行时间可能比 MySQL 或 InnoDB 更长。在 InnoDB 中，仅对少量页面进行采样，而 TiDB 默认会完全重建一套全面的统计信息。

TiDB 提供两种方式提升统计信息收集性能：

- 只收集部分列的统计信息。参见 [收集部分列的统计信息](#collect-statistics-on-some-columns)。
- 采样。

### 统计信息采样

采样可通过 `ANALYZE` 语句的两个不同选项实现，每个选项对应不同的收集算法：

- `WITH NUM SAMPLES` 指定采样集大小，在 TiDB 中实现为蓄水池采样法。当表较大时，不建议使用该方法收集统计信息。因为蓄水池采样的中间结果集包含冗余结果，会对内存等资源造成额外压力。
- `WITH FLOAT_NUM SAMPLERATE` 是 v5.3.0 引入的采样方法，取值范围为 `(0, 1]`，指定采样率。在 TiDB 中实现为伯努利采样，更适合大表采样，在收集效率和资源使用上表现更优。

v5.3.0 之前，TiDB 使用蓄水池采样法收集统计信息。自 v5.3.0 起，TiDB 统计信息版本 2 默认使用伯努利采样法。若需继续使用蓄水池采样法，可使用 `WITH NUM SAMPLES` 语句。

当前采样率基于自适应算法计算。当你可以通过 [`SHOW STATS_META`](/sql-statements/sql-statement-show-stats-meta.md) 观察到表的行数时，可以用该行数计算对应 100,000 行的采样率。如果无法观察到该行数，可以用 [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md) 结果中 `APPROXIMATE_KEYS` 列的所有值之和作为参考，计算采样率。

> **注意：**
>
> 通常，`STATS_META` 比 `APPROXIMATE_KEYS` 更可靠。但当 `STATS_META` 结果远小于 `APPROXIMATE_KEYS` 时，建议用 `APPROXIMATE_KEYS` 计算采样率。

### 收集统计信息的内存配额

> **警告：**
>
> 目前，`ANALYZE` 内存配额为实验特性，生产环境下内存统计可能不准确。

自 TiDB v6.1.0 起，你可以通过系统变量 [`tidb_mem_quota_analyze`](/system-variables.md#tidb_mem_quota_analyze-new-in-v610) 控制 TiDB 收集统计信息时的内存配额。

设置 `tidb_mem_quota_analyze` 时，应结合集群数据量综合考虑。使用默认采样率时，主要考虑列数、列值大小和 TiDB 的内存配置。配置最大值和最小值时可参考以下建议：

> **注意：**
>
> 以下建议仅供参考，具体值需结合实际场景配置。

- 最小值：应大于 TiDB 收集列数最多的表时的最大内存使用量。大致参考：默认配置下，TiDB 收集 20 列的表时最大内存约 800 MiB；收集 160 列的表时最大内存约 5 GiB。
- 最大值：应小于 TiDB 未收集统计信息时的可用内存。

## 持久化 ANALYZE 配置

自 v5.4.0 起，TiDB 支持持久化部分 `ANALYZE` 配置。通过该特性，可以方便地复用现有配置进行后续统计信息收集。

支持持久化的 `ANALYZE` 配置如下：

| 配置项 | 对应 ANALYZE 语法 |
| --- | --- |
| 直方图桶数 | `WITH NUM BUCKETS` |
| Top-N 数量  | `WITH NUM TOPN` |
| 样本数量 | `WITH NUM SAMPLES` |
| 采样率 | `WITH FLOATNUM SAMPLERATE` |
| `ANALYZE` 列类型 | AnalyzeColumnOption ::= ( 'ALL COLUMNS' \| 'PREDICATE COLUMNS' \| 'COLUMNS' ColumnNameList ) |
| `ANALYZE` 列 | ColumnNameList ::= Identifier ( ',' Identifier )* |

### 启用 ANALYZE 配置持久化

<CustomContent platform="tidb">

`ANALYZE` 配置持久化特性默认开启（系统变量 `tidb_analyze_version` 默认为 `2`，`tidb_persist_analyze_options` 默认为 `ON`）。

</CustomContent>

<CustomContent platform="tidb-cloud">

`ANALYZE` 配置持久化特性默认关闭。若需启用该特性，请确保系统变量 `tidb_persist_analyze_options` 为 `ON`，并将系统变量 `tidb_analyze_version` 设置为 `2`。

</CustomContent>

你可以通过该特性，在手动执行 `ANALYZE` 语句时记录指定的持久化配置。记录后，下次 TiDB 自动更新统计信息或你手动收集统计信息时未指定这些配置，TiDB 会按照已记录的配置收集统计信息。

要查询某张表用于自动分析操作的持久化配置，可执行以下 SQL 语句：

```sql
SELECT sample_num, sample_rate, buckets, topn, column_choice, column_ids FROM mysql.analyze_options opt JOIN information_schema.tables tbl ON opt.table_id = tbl.tidb_table_id WHERE tbl.table_schema = '{db_name}' AND tbl.table_name = '{table_name}';
```

TiDB 会用最新一次 `ANALYZE` 语句指定的新配置覆盖之前记录的持久化配置。例如，执行 `ANALYZE TABLE t WITH 200 TOPN;` 后，`ANALYZE` 语句会设置 top 200 的值。随后执行 `ANALYZE TABLE t WITH 0.1 SAMPLERATE;`，则自动 `ANALYZE` 语句会同时设置 top 200 和采样率 0.1，等同于 `ANALYZE TABLE t WITH 200 TOPN, 0.1 SAMPLERATE;`。

### 关闭 ANALYZE 配置持久化

若需关闭 `ANALYZE` 配置持久化特性，将系统变量 `tidb_persist_analyze_options` 设置为 `OFF`。由于 `ANALYZE` 配置持久化特性不适用于 `tidb_analyze_version = 1`，将 `tidb_analyze_version` 设置为 `1` 也可关闭该特性。

关闭 `ANALYZE` 配置持久化特性后，TiDB 不会清除已持久化的配置记录。因此，若你再次启用该特性，TiDB 会继续使用之前记录的持久化配置收集统计信息。

> **注意：**
>
> 再次启用 `ANALYZE` 配置持久化特性时，若之前记录的持久化配置已不适用于最新数据，你需要手动执行 `ANALYZE` 语句并指定新的持久化配置。

### 持久化列配置

如果你希望持久化 `ANALYZE` 语句中的列配置（包括 `COLUMNS ColumnNameList`、`PREDICATE COLUMNS` 和 `ALL COLUMNS`），请将系统变量 `tidb_persist_analyze_options` 设置为 `ON`，以启用 [ANALYZE 配置持久化](#persist-analyze-configurations) 特性。启用后：

- 当 TiDB 自动收集统计信息，或你手动执行 `ANALYZE` 语句但未指定列配置时，TiDB 会继续使用之前持久化的配置收集统计信息。
- 当你多次手动执行带有列配置的 `ANALYZE` 语句时，TiDB 会用最新一次 `ANALYZE` 语句指定的新配置覆盖之前记录的持久化配置。

要定位已收集统计信息的 `PREDICATE COLUMNS` 和列，可使用 [`SHOW COLUMN_STATS_USAGE`](/sql-statements/sql-statement-show-column-stats-usage.md) 语句。

如下示例，在执行 `ANALYZE TABLE t PREDICATE COLUMNS;` 后，TiDB 会收集列 `b`、`c` 和 `d` 的统计信息，其中 `b` 为谓词列，`c` 和 `d` 为索引列。

```sql
CREATE TABLE t (a INT, b INT, c INT, d INT, INDEX idx_c_d(c, d));
Query OK, 0 rows affected (0.00 sec)

-- 优化器在该查询中会使用列 b 的统计信息。
SELECT * FROM t WHERE b > 1;
Empty set (0.00 sec)

-- 等待一段时间（100 * stats-lease）后，TiDB 会将收集到的 `PREDICATE COLUMNS` 写入 mysql.column_stats_usage。
-- 指定 `last_used_at IS NOT NULL` 可显示 TiDB 收集到的 `PREDICATE COLUMNS`。
SHOW COLUMN_STATS_USAGE
WHERE db_name = 'test' AND table_name = 't' AND last_used_at IS NOT NULL;
+---------+------------+----------------+-------------+---------------------+------------------+
| Db_name | Table_name | Partition_name | Column_name | Last_used_at        | Last_analyzed_at |
+---------+------------+----------------+-------------+---------------------+------------------+
| test    | t          |                | b           | 2022-01-05 17:21:33 | NULL             |
+---------+------------+----------------+-------------+---------------------+------------------+
1 row in set (0.00 sec)

ANALYZE TABLE t PREDICATE COLUMNS;
Query OK, 0 rows affected, 1 warning (0.03 sec)

-- 指定 `last_analyzed_at IS NOT NULL` 可显示已收集统计信息的列。
SHOW COLUMN_STATS_USAGE
WHERE db_name = 'test' AND table_name = 't' AND last_analyzed_at IS NOT NULL;
+---------+------------+----------------+-------------+---------------------+---------------------+
| Db_name | Table_name | Partition_name | Column_name | Last_used_at        | Last_analyzed_at    |
+---------+------------+----------------+-------------+---------------------+---------------------+
| test    | t          |                | b           | 2022-01-05 17:21:33 | 2022-01-05 17:23:06 |
| test    | t          |                | c           | NULL                | 2022-01-05 17:23:06 |
| test    | t          |                | d           | NULL                | 2022-01-05 17:23:06 |
+---------+------------+----------------+-------------+---------------------+---------------------+
3 rows in set (0.00 sec)
```

## 统计信息版本

[`tidb_analyze_version`](/system-variables.md#tidb_analyze_version-new-in-v510) 变量控制 TiDB 收集的统计信息。目前支持两种统计信息版本：`tidb_analyze_version = 1` 和 `tidb_analyze_version = 2`。

- 对于 TiDB 自建版，该变量的默认值自 v5.3.0 起由 `1` 变为 `2`。
- 对于 TiDB Cloud，该变量的默认值自 v6.5.0 起由 `1` 变为 `2`。
- 如果你的集群由早期版本升级而来，升级后 `tidb_analyze_version` 的默认值不会改变。

推荐使用版本 2，且后续会持续增强，最终完全替代版本 1。与版本 1 相比，版本 2 在大数据量下提升了统计信息的准确性，并通过移除 Count-Min Sketch 统计信息收集（用于谓词选择性估算）提升了收集性能，同时支持仅对选定列自动收集（参见 [收集部分列的统计信息](#collect-statistics-on-some-columns)）。

下表列出了每个版本为优化器估算收集的信息：

| 信息 | 版本 1 | 版本 2|
| --- | --- | ---|
| 表的总行数 | ⎷ | ⎷ |
| 等值/IN 谓词估算 | ⎷（列/索引 Top-N & Count-Min Sketch） | ⎷（列/索引 Top-N & 直方图） |
| 范围谓词估算 | ⎷（列/索引 Top-N & 直方图） | ⎷（列/索引 Top-N & 直方图） |
| `NULL` 谓词估算 | ⎷ | ⎷ |
| 列的平均长度 | ⎷ | ⎷ |
| 索引的平均长度 | ⎷ | ⎷ |

### 切换统计信息版本

建议确保所有表/索引（及分区）均使用同一版本的统计信息收集。推荐使用版本 2，但不建议无正当理由随意切换版本。切换版本期间，若所有表尚未用新版本分析，可能会出现一段时间内无统计信息，影响优化器的执行计划选择。

常见的切换理由包括：在版本 1 下，因收集 Count-Min Sketch 统计信息时哈希冲突导致等值/IN 谓词估算不准确。解决方案见 [Count-Min Sketch](#count-min-sketch) 一节。或者，将 `tidb_analyze_version` 设为 2 并对所有对象重新执行 `ANALYZE` 也是一种解决方案。在版本 2 的早期发布中，`ANALYZE` 后存在内存溢出的风险。该问题已修复，但当时的解决方法是将 `tidb_analyze_version` 设为 1 并对所有对象重新执行 `ANALYZE`。

切换版本前的 `ANALYZE` 准备：

- 若手动执行 `ANALYZE` 语句，请手动分析所有需分析的表。

    ```sql
    SELECT DISTINCT(CONCAT('ANALYZE TABLE ', table_schema, '.', table_name, ';'))
    FROM information_schema.tables JOIN mysql.stats_histograms
    ON table_id = tidb_table_id
    WHERE stats_ver = 2;
    ```

- 若 TiDB 自动执行 `ANALYZE` 语句（已启用自动分析），可执行以下语句生成 [`DROP STATS`](/sql-statements/sql-statement-drop-stats.md) 语句：

    ```sql
    SELECT DISTINCT(CONCAT('DROP STATS ', table_schema, '.', table_name, ';'))
    FROM information_schema.tables JOIN mysql.stats_histograms
    ON table_id = tidb_table_id
    WHERE stats_ver = 2;
    ```

- 若上述语句结果过长无法复制粘贴，可将结果导出到临时文本文件，再从文件中执行：

    ```sql
    SELECT DISTINCT ... INTO OUTFILE '/tmp/sql.txt';
    mysql -h ${TiDB_IP} -u user -P ${TIDB_PORT} ... < '/tmp/sql.txt'
    ```

## 查看统计信息

你可以通过以下语句查看 `ANALYZE` 状态和统计信息。

### `ANALYZE` 状态

执行 `ANALYZE` 语句时，可通过 [`SHOW ANALYZE STATUS`](/sql-statements/sql-statement-show-analyze-status.md) 查看当前 `ANALYZE` 状态。

自 TiDB v6.1.0 起，`SHOW ANALYZE STATUS` 支持显示集群级任务。即使 TiDB 重启后，仍可通过该语句查看重启前的任务记录。TiDB v6.1.0 之前，`SHOW ANALYZE STATUS` 仅能显示实例级任务，且重启后任务记录会被清除。

`SHOW ANALYZE STATUS` 仅显示最近的任务记录。自 TiDB v6.1.0 起，你可以通过系统表 `mysql.analyze_jobs` 查看最近 7 天的历史任务。

当设置了 [`tidb_mem_quota_analyze`](/system-variables.md#tidb_mem_quota_analyze-new-in-v610)，且后台自动 `ANALYZE` 任务使用内存超出该阈值时，任务会被重试。你可以在 `SHOW ANALYZE STATUS` 输出中看到失败和重试的任务。

当 [`tidb_max_auto_analyze_time`](/system-variables.md#tidb_max_auto_analyze_time-new-in-v610) 大于 0，且后台自动 `ANALYZE` 任务执行时间超出该阈值时，任务会被终止。

```sql
mysql> SHOW ANALYZE STATUS [ShowLikeOrWhere];
+--------------+------------+----------------+-------------------------------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------------------------------------------------------------------------|
| Table_schema | Table_name | Partition_name | Job_info                                                                                  | Processed_rows | Start_time          | End_time            | State    | Fail_reason                                                                   |
+--------------+------------+----------------+-------------------------------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------------------------------------------------------------------------|
| test         | sbtest1    |                | retry auto analyze table all columns with 100 topn, 0.055 samplerate                      |        2000000 | 2022-05-07 16:41:09 | 2022-05-07 16:41:20 | finished | NULL                                                                          |
| test         | sbtest1    |                | auto analyze table all columns with 100 topn, 0.5 samplerate                              |              0 | 2022-05-07 16:40:50 | 2022-05-07 16:41:09 | failed   | analyze panic due to memory quota exceeds, please try with smaller samplerate |
```

### 表的元数据

你可以使用 [`SHOW STATS_META`](/sql-statements/sql-statement-show-stats-meta.md) 语句查看总行数和已更新行数。

### 表的健康状态

你可以使用 [`SHOW STATS_HEALTHY`](/sql-statements/sql-statement-show-stats-healthy.md) 语句检查表的健康状态，并大致估算统计信息的准确性。当 `modify_count` >= `row_count` 时，健康度为 0；当 `modify_count` < `row_count` 时，健康度为 (1 - `modify_count`/`row_count`) * 100。

### 列的元数据

你可以使用 [`SHOW STATS_HISTOGRAMS`](/sql-statements/sql-statement-show-stats-histograms.md) 语句查看所有列的不同值数量和 `NULL` 数量。

### 直方图的桶

你可以使用 [`SHOW STATS_BUCKETS`](/sql-statements/sql-statement-show-stats-buckets.md) 语句查看直方图的每个桶。

### Top-N 信息

你可以使用 [`SHOW STATS_TOPN`](/sql-statements/sql-statement-show-stats-topn.md) 语句查看 TiDB 当前收集到的 Top-N 信息。

## 删除统计信息

你可以通过 [`DROP STATS`](/sql-statements/sql-statement-drop-stats.md) 语句删除统计信息。

## 加载统计信息

> **注意：**
>
> 加载统计信息不适用于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群。

默认情况下，TiDB 会根据列统计信息的大小采用不同的加载方式：

- 对于占用内存较小的统计信息（如 count、distinctCount 和 nullCount），只要列数据有更新，TiDB 会自动将对应统计信息加载到内存中，供 SQL 优化阶段使用。
- 对于占用内存较大的统计信息（如直方图、TopN 和 Count-Min Sketch），为保证 SQL 执行性能，TiDB 会按需异步加载这些统计信息。例如，直方图统计信息只有在优化器需要使用某列的直方图时，才会将其加载到内存。按需异步加载不会影响 SQL 执行性能，但可能导致 SQL 优化时统计信息不完整。

自 v5.4.0 起，TiDB 引入了同步加载统计信息特性。该特性允许 TiDB 在执行 SQL 语句时，将大体积统计信息（如直方图、TopN 和 Count-Min Sketch）同步加载到内存，从而提升 SQL 优化时统计信息的完整性。

要启用该特性，请将 [`tidb_stats_load_sync_wait`](/system-variables.md#tidb_stats_load_sync_wait-new-in-v540) 系统变量设置为 SQL 优化可等待同步加载完整列统计信息的超时时间（毫秒）。该变量默认值为 `100`，表示已启用该特性。

<CustomContent platform="tidb">

启用同步加载统计信息特性后，你还可以进一步配置如下：

- 若要控制 SQL 优化等待超时后的行为，可修改 [`tidb_stats_load_pseudo_timeout`](/system-variables.md#tidb_stats_load_pseudo_timeout-new-in-v540) 系统变量。该变量默认值为 `ON`，表示超时后 SQL 优化过程不会使用任何列的直方图、TopN 或 CMSketch 统计信息。若设为 `OFF`，超时后 SQL 执行失败。
- 若要指定同步加载统计信息特性可并发处理的最大列数，可修改 TiDB 配置文件中的 [`stats-load-concurrency`](/tidb-configuration-file.md#stats-load-concurrency-new-in-v540) 选项。自 v8.2.0 起，默认值为 `0`，表示 TiDB 会根据服务器配置自动调整并发度。
- 若要指定同步加载统计信息特性可缓存的最大列请求数，可修改 TiDB 配置文件中的 [`stats-load-queue-size`](/tidb-configuration-file.md#stats-load-queue-size-new-in-v540) 选项。默认值为 `1000`。

TiDB 启动期间，在初始统计信息尚未完全加载前执行的 SQL 语句，可能会生成次优的执行计划，导致性能问题。为避免此类问题，TiDB v7.1.0 引入了配置参数 [`force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v657-and-v710)。通过该选项，你可以控制 TiDB 是否在统计信息初始化完成后才提供服务。自 v7.2.0 起，该参数默认启用。

自 v7.1.0 起，TiDB 引入了 [`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710) 轻量级统计信息初始化。

- 当 `lite-init-stats` 为 `true` 时，统计信息初始化不会将任何索引或列的直方图、TopN 或 Count-Min Sketch 加载到内存。
- 当 `lite-init-stats` 为 `false` 时，统计信息初始化会将索引和主键的直方图、TopN 和 Count-Min Sketch 加载到内存，但不会加载非主键列的直方图、TopN 或 Count-Min Sketch。当优化器需要某个索引或列的直方图、TopN 和 Count-Min Sketch 时，会同步或异步加载所需统计信息。

`lite-init-stats` 默认值为 `true`，即启用轻量级统计信息初始化。将 `lite-init-stats` 设为 `true` 可加快统计信息初始化速度，并通过避免不必要的统计信息加载降低 TiDB 内存占用。

</CustomContent>

<CustomContent platform="tidb-cloud">

启用同步加载统计信息特性后，你可以通过修改 [`tidb_stats_load_pseudo_timeout`](/system-variables.md#tidb_stats_load_pseudo_timeout-new-in-v540) 系统变量控制 SQL 优化等待超时后的行为。该变量默认值为 `ON`，表示超时后 SQL 优化过程不会使用任何列的直方图、TopN 或 CMSketch 统计信息。若设为 `OFF`，超时后 SQL 执行失败。

</CustomContent>

## 导出与导入统计信息

本节介绍如何导出和导入统计信息。

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 本节内容不适用于 TiDB Cloud。

</CustomContent>

### 导出统计信息

导出统计信息的接口如下：

+ 获取 `${db_name}` 数据库中 `${table_name}` 表的 JSON 格式统计信息：

    ```
    http://${tidb-server-ip}:${tidb-server-status-port}/stats/dump/${db_name}/${table_name}
    ```

    例如：

    ```shell
    curl -s http://127.0.0.1:10080/stats/dump/test/t1 -o /tmp/t1.json
    ```

+ 获取 `${db_name}` 数据库中 `${table_name}` 表在指定时间点的 JSON 格式统计信息：

    ```
    http://${tidb-server-ip}:${tidb-server-status-port}/stats/dump/${db_name}/${table_name}/${yyyyMMddHHmmss}
    ```

### 导入统计信息

> **注意：**
>
> 启动 MySQL 客户端时，请使用 `--local-infile=1` 选项。

通常，导入的统计信息指的是通过导出接口获得的 JSON 文件。

加载统计信息可通过 [`LOAD STATS`](/sql-statements/sql-statement-load-stats.md) 语句完成。

例如：

```sql
LOAD STATS 'file_name';
```

`file_name` 为待导入的统计信息文件名。

## 锁定统计信息

自 v6.5.0 起，TiDB 支持锁定统计信息。表或分区的统计信息被锁定后，该表的统计信息无法被修改，且无法对该表执行 `ANALYZE` 语句。例如：

创建表 `t` 并插入数据。当表 `t` 的统计信息未被锁定时，可以成功执行 `ANALYZE` 语句。

```sql
mysql> CREATE TABLE t(a INT, b INT);
Query OK, 0 rows affected (0.03 sec)

mysql> INSERT INTO t VALUES (1,2), (3,4), (5,6), (7,8);
Query OK, 4 rows affected (0.00 sec)
Records: 4  Duplicates: 0  Warnings: 0

mysql> ANALYZE TABLE t;
Query OK, 0 rows affected, 1 warning (0.02 sec)

mysql> SHOW WARNINGS;
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Level | Code | Message                                                                                                                                                                                                               |
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Note  | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t, reason to use this rate is "Row count in stats_meta is much smaller compared with the row count got by PD, use min(1, 15000/4) as the sample-rate=1" |
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

锁定表 `t` 的统计信息后执行 `ANALYZE`，警告信息显示 `ANALYZE` 语句已跳过表 `t`。

```sql
mysql> LOCK STATS t;
Query OK, 0 rows affected (0.00 sec)

mysql> SHOW STATS_LOCKED;
+---------+------------+----------------+--------+
| Db_name | Table_name | Partition_name | Status |
+---------+------------+----------------+--------+
| test    | t          |                | locked |
+---------+------------+----------------+--------+
1 row in set (0.01 sec)

mysql> ANALYZE TABLE t;
Query OK, 0 rows affected, 2 warnings (0.00 sec)

mysql> SHOW WARNINGS;
+---------+------+-----------------------------------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                                                 |
+---------+------+-----------------------------------------------------------------------------------------------------------------------------------------+
| Note    | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t, reason to use this rate is "use min(1, 110000/8) as the sample-rate=1" |
| Warning | 1105 | skip analyze locked table: test.t                                                                                                       |
+---------+------+-----------------------------------------------------------------------------------------------------------------------------------------+
2 rows in set (0.00 sec)
```

解锁表 `t` 的统计信息后，可以再次成功执行 `ANALYZE`。

```sql
mysql> UNLOCK STATS t;
Query OK, 0 rows affected (0.01 sec)

mysql> ANALYZE TABLE t;
Query OK, 0 rows affected, 1 warning (0.03 sec)

mysql> SHOW WARNINGS;
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------+
| Level | Code | Message                                                                                                                                 |
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------+
| Note  | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t, reason to use this rate is "use min(1, 110000/8) as the sample-rate=1" |
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

此外，你还可以通过 [`LOCK STATS`](/sql-statements/sql-statement-lock-stats.md) 锁定分区的统计信息。例如：

创建分区表 `t` 并插入数据。当分区 `p1` 的统计信息未被锁定时，可以成功执行 `ANALYZE` 语句。

```sql
mysql> CREATE TABLE t(a INT, b INT) PARTITION BY RANGE (a) (PARTITION p0 VALUES LESS THAN (10), PARTITION p1 VALUES LESS THAN (20), PARTITION p2 VALUES LESS THAN (30));
Query OK, 0 rows affected (0.03 sec)

mysql> INSERT INTO t VALUES (1,2), (3,4), (5,6), (7,8);
Query OK, 4 rows affected (0.00 sec)
Records: 4  Duplicates: 0  Warnings: 0

mysql> ANALYZE TABLE t;
Query OK, 0 rows affected, 6 warning (0.02 sec)

mysql> SHOW WARNINGS;
+---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                                                                                                                                              |
+---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Warning | 1105 | disable dynamic pruning due to t has no global stats                                                                                                                                                                                 |
| Note    | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t's partition p0, reason to use this rate is "Row count in stats_meta is much smaller compared with the row count got by PD, use min(1, 15000/4) as the sample-rate=1" |
| Warning | 1105 | disable dynamic pruning due to t has no global stats                                                                                                                                                                                 |
| Note    | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t's partition p1, reason to use this rate is "TiDB assumes that the table is empty, use sample-rate=1"                                                                 |
| Warning | 1105 | disable dynamic pruning due to t has no global stats                                                                                                                                                                                 |
| Note    | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t's partition p2, reason to use this rate is "TiDB assumes that the table is empty, use sample-rate=1"                                                                 |
+---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
6 rows in set (0.01 sec)
```

锁定分区 `p1` 的统计信息后执行 `ANALYZE`，警告信息显示 `ANALYZE` 语句已跳过分区 `p1`。

```sql
mysql> LOCK STATS t PARTITION p1;
Query OK, 0 rows affected (0.00 sec)

mysql> SHOW STATS_LOCKED;
+---------+------------+----------------+--------+
| Db_name | Table_name | Partition_name | Status |
+---------+------------+----------------+--------+
| test    | t          | p1             | locked |
+---------+------------+----------------+--------+
1 row in set (0.00 sec)

mysql> ANALYZE TABLE t PARTITION p1;
Query OK, 0 rows affected, 2 warnings (0.01 sec)

mysql> SHOW WARNINGS;
+---------+------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                                                                              |
+---------+------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Note    | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t's partition p1, reason to use this rate is "TiDB assumes that the table is empty, use sample-rate=1" |
| Warning | 1105 | skip analyze locked table: test.t partition (p1)                                                                                                                     |
+---------+------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
2 rows in set (0.00 sec)
```

解锁分区 `p1` 的统计信息后，可以再次成功执行 `ANALYZE`。

```sql
mysql> UNLOCK STATS t PARTITION p1;
Query OK, 0 rows affected (0.00 sec)

mysql> ANALYZE TABLE t PARTITION p1;
Query OK, 0 rows affected, 1 warning (0.01 sec)

mysql> SHOW WARNINGS;
+-------+------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Level | Code | Message                                                                                                                                                              |
+-------+------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Note  | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t's partition p1, reason to use this rate is "TiDB assumes that the table is empty, use sample-rate=1" |
+-------+------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

### 锁定统计信息的行为

* 若锁定分区表的统计信息，则该分区表所有分区的统计信息均被锁定。
* 若截断表或分区，则表或分区的统计信息锁会被释放。

下表描述了锁定统计信息的行为：

| | 删除整张表 | 截断整张表 | 截断分区 | 新建分区 | 删除分区 | 重组分区 | 交换分区 |
|----------------------------|------------|----------------------------------------------------------------|----------------------------------------------------------------|----------------|----------------------------------------------|----------------------------------------------|--------------------------|
| 非分区表被锁定 | 锁失效 | 锁失效，因 TiDB 删除旧表，锁信息也被删除 | / | / | / | / | / |
| 分区表且整表被锁定 | 锁失效 | 锁失效，因 TiDB 删除旧表，锁信息也被删除 | 旧分区锁信息失效，新分区自动加锁 | 新分区自动加锁 | 被删除分区锁信息清除，整表锁继续生效 | 被删除分区锁信息清除，新分区自动加锁 | 锁信息转移到交换表，新分区自动加锁 |
| 分区表且仅部分分区被锁定 | 锁失效 | 锁失效，因 TiDB 删除旧表，锁信息也被删除 | 锁失效，因 TiDB 删除旧表，锁信息也被删除 | / | 被删除分区锁信息清除 | 被删除分区锁信息清除 | 锁信息转移到交换表 |

## 管理 `ANALYZE` 任务与并发度

本节介绍如何终止后台 `ANALYZE` 任务及控制 `ANALYZE` 并发度。

### 终止后台 `ANALYZE` 任务

自 TiDB v6.0 起，TiDB 支持使用 `KILL` 语句终止后台运行的 `ANALYZE` 任务。如果你发现后台 `ANALYZE` 任务消耗大量资源影响业务，可以按以下步骤终止该任务：

1. 执行以下 SQL 语句：

    ```sql
    SHOW ANALYZE STATUS
    ```

    通过结果中的 `instance` 列和 `process_id` 列，可以获取后台 `ANALYZE` 任务所在 TiDB 实例地址及任务 `ID`。

2. 终止正在后台运行的 `ANALYZE` 任务。

    <CustomContent platform="tidb">

    - 若 [`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-new-in-v610) 为 `true`（默认 `true`），可直接执行 `KILL TIDB ${id};`，其中 `${id}` 为上一步获取的后台 `ANALYZE` 任务的 `ID`。
    - 若 `enable-global-kill` 为 `false`，需使用客户端连接到正在执行后台 `ANALYZE` 任务的 TiDB 实例，然后执行 `KILL TIDB ${id};`。若使用客户端连接到其他 TiDB 实例，或客户端与 TiDB 集群间有代理，则 `KILL` 语句无法终止后台 `ANALYZE` 任务。

    </CustomContent>

    <CustomContent platform="tidb-cloud">

    若需终止 `ANALYZE` 任务，可执行 `KILL TIDB ${id};`，其中 `${id}` 为上一步获取的后台 `ANALYZE` 任务的 `ID`。

    </CustomContent>

更多关于 `KILL` 语句的信息，参见 [`KILL`](/sql-statements/sql-statement-kill.md)。

### 控制 `ANALYZE` 并发度

执行 `ANALYZE` 语句时，你可以通过系统变量调整并发度，以控制其对系统的影响。

相关系统变量的关系如下图所示：

![analyze_concurrency](/media/analyze_concurrency.png)

`tidb_build_stats_concurrency`、`tidb_build_sampling_stats_concurrency` 和 `tidb_analyze_partition_concurrency` 之间为上下游关系，如上图所示。实际总并发度为：`tidb_build_stats_concurrency` * (`tidb_build_sampling_stats_concurrency` + `tidb_analyze_partition_concurrency`)。修改这些变量时需同时考虑各自的取值。建议按 `tidb_analyze_partition_concurrency`、`tidb_build_sampling_stats_concurrency`、`tidb_build_stats_concurrency` 的顺序逐一调整，并观察对系统的影响。三者值越大，对系统资源消耗越大。

#### `tidb_build_stats_concurrency`

执行 `ANALYZE` 语句时，任务会被拆分为多个小任务。每个小任务仅处理一个列或索引的统计信息。你可以通过 [`tidb_build_stats_concurrency`](/system-variables.md#tidb_build_stats_concurrency) 变量控制同时运行的小任务数。默认值为 `2`。v7.4.0 及更早版本默认值为 `4`。

#### `tidb_build_sampling_stats_concurrency`

分析普通列时，可通过 [`tidb_build_sampling_stats_concurrency`](/system-variables.md#tidb_build_sampling_stats_concurrency-new-in-v750) 控制采样任务的并发度。默认值为 `2`。

#### `tidb_analyze_partition_concurrency`

执行 `ANALYZE` 语句时，可通过 [`tidb_analyze_partition_concurrency`](/system-variables.md#tidb_analyze_partition_concurrency) 控制分区表读写统计信息的并发度。默认值为 `2`。v7.4.0 及更早版本默认值为 `1`。

#### `tidb_distsql_scan_concurrency`

分析普通列时，可通过 [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency) 变量控制一次读取的 Region 数量。默认值为 `15`。注意，修改该值会影响查询性能，请谨慎调整。

#### `tidb_index_serial_scan_concurrency`

分析索引列时，可通过 [`tidb_index_serial_scan_concurrency`](/system-variables.md#tidb_index_serial_scan_concurrency) 变量控制一次读取的 Region 数量。默认值为 `1`。注意，修改该值会影响查询性能，请谨慎调整。

## 另请参阅

<CustomContent platform="tidb">

* [LOAD STATS](/sql-statements/sql-statement-load-stats.md)
* [DROP STATS](/sql-statements/sql-statement-drop-stats.md)
* [LOCK STATS](/sql-statements/sql-statement-lock-stats.md)
* [UNLOCK STATS](/sql-statements/sql-statement-unlock-stats.md)
* [SHOW STATS_LOCKED](/sql-statements/sql-statement-show-stats-locked.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

* [LOAD STATS](/sql-statements/sql-statement-load-stats.md)
* [LOCK STATS](/sql-statements/sql-statement-lock-stats.md)
* [UNLOCK STATS](/sql-statements/sql-statement-unlock-stats.md)
* [SHOW STATS_LOCKED](/sql-statements/sql-statement-show-stats-locked.md)

</CustomContent>
