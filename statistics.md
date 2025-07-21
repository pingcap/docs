---
title: 统计介绍
summary: 了解统计信息如何收集表级和列级信息。
---

# 统计介绍 {#introduction-to-statistics}

TiDB 使用统计信息作为优化器的输入，用于估算 SQL 语句中每个执行计划步骤处理的行数。优化器会估算每个可用计划的成本，包括 [索引访问](/choose-index.md) 和表连接的序列，并为每个可用计划生成一个成本值。然后，优化器选择总成本最低的执行计划。

## 收集统计信息 {#collect-statistics}

本节描述两种收集统计信息的方法：自动更新和手动收集。

### 自动更新 {#automatic-update}

对于 [`INSERT`](/sql-statements/sql-statement-insert.md)、[`DELETE`](/sql-statements/sql-statement-delete.md) 或 [`UPDATE`](/sql-statements/sql-statement-update.md) 语句，TiDB 会自动更新统计信息中的行数和修改行数。

<CustomContent platform="tidb">

TiDB 定期持久化更新信息，更新周期为 20 * [`stats-lease`](/tidb-configuration-file.md#stats-lease)。`stats-lease` 的默认值为 `3s`。如果你将其值设为 `0`，TiDB 将停止自动更新统计信息。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB 每 60 秒持久化一次更新信息。

</CustomContent>

根据表的变更行数，TiDB 会自动调度 [`ANALYZE`](/sql-statements/sql-statement-analyze-table.md) 来收集这些表的统计信息。这由以下系统变量控制。

| 系统变量 | 默认值 | 描述 |
| --- | --- | --- |
| [`tidb_auto_analyze_concurrency`](/system-variables.md#tidb_auto_analyze_concurrency-new-in-v840) | `1` | TiDB 集群中自动分析操作的并发数。 |
| [`tidb_auto_analyze_end_time`](/system-variables.md#tidb_auto_analyze_end_time) | `23:59 +0000` | 一天中 TiDB 可以执行自动更新的结束时间。 |
| [`tidb_auto_analyze_partition_batch_size`](/system-variables.md#tidb_auto_analyze_partition_batch_size-new-in-v640) | `8192` | TiDB 在分析分区表（即自动更新分区表统计信息）时，自动分析的分区数量。 |
| [`tidb_auto_analyze_ratio`](/system-variables.md#tidb_auto_analyze_ratio) | `0.5` | 自动更新的阈值。 |
| [`tidb_auto_analyze_start_time`](/system-variables.md#tidb_auto_analyze_start_time) | `00:00 +0000` | 一天中 TiDB 可以执行自动更新的开始时间。 |
| [`tidb_enable_auto_analyze`](/system-variables.md#tidb_enable_auto_analyze-new-in-v610) | `ON` | 控制 TiDB 是否自动执行 `ANALYZE`。 |
| [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800) | `ON` | 控制是否启用优先队列调度自动统计任务。当启用时，TiDB 优先收集对性能影响较大的表的统计信息，例如新创建的索引和分区变更的分区表。此外，TiDB 会优先处理健康评分较低的表，将其排在队列前列。 |
| [`tidb_enable_stats_owner`](/system-variables.md#tidb_enable_stats_owner-new-in-v840) | `ON` | 控制对应的 TiDB 实例是否可以运行自动统计更新任务。 |
| [`tidb_max_auto_analyze_time`](/system-variables.md#tidb_max_auto_analyze_time-new-in-v610) | `43200`（12 小时） | 自动 `ANALYZE` 任务的最大执行时间，单位为秒。 |

当表中 `tbl` 的修改行数与总行数的比值大于 `tidb_auto_analyze_ratio`，且当前时间在 `tidb_auto_analyze_start_time` 和 `tidb_auto_analyze_end_time` 之间时，TiDB 会在后台执行 `ANALYZE TABLE tbl` 语句，自动更新该表的统计信息。

为了避免频繁修改小表数据触发自动更新，当表的行数少于 1000 行时，修改不会触发自动更新。你可以使用 `SHOW STATS_META` 语句查看表中的行数。

> **注意：**
>
> 目前，自动更新不会记录手动 `ANALYZE` 时输入的配置项。因此，当你使用 [`WITH`](/sql-statements/sql-statement-analyze-table.md) 语法控制 `ANALYZE` 的采集行为时，需要手动设置调度任务以收集统计信息。

### 手动收集 {#manual-collection}

目前，TiDB 以全量收集的方式收集统计信息。你可以执行 `ANALYZE TABLE` 语句进行统计信息的收集。

可以使用以下语法进行全量收集。

-   收集 `TableNameList` 中所有表的统计信息：

    ```sql
    ANALYZE TABLE TableNameList [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

-   `WITH NUM BUCKETS` 指定生成的直方图的最大桶数。

-   `WITH NUM TOPN` 指定生成的 `TOPN` 的最大数量。

-   `WITH NUM CMSKETCH DEPTH` 指定 CM Sketch 的深度。

-   `WITH NUM CMSKETCH WIDTH` 指定 CM Sketch 的宽度。

-   `WITH NUM SAMPLES` 指定采样次数。

-   `WITH FLOAT_NUM SAMPLERATE` 指定采样率。

`WITH NUM SAMPLES` 和 `WITH FLOAT_NUM SAMPLERATE` 分别对应两种不同的采样算法。

详细说明请参见 [Histograms](#histogram)、[Top-N](#top-n) 和 [CMSketch](#count-min-sketch)（Count-Min Sketch）。关于 `SAMPLES`/`SAMPLERATE`，请参见 [Improve collection performance](#improve-collection-performance)。

关于持久化配置以便重复使用的信息，参见 [Persist `ANALYZE` configurations](#persist-analyze-configurations)。

## 统计信息的类型 {#types-of-statistics}

本节介绍三种统计信息：直方图、Count-Min Sketch 和 Top-N。

### 直方图 {#histogram}

直方图统计信息被优化器用来估算区间或范围谓词的选择性，也可能用于估算某列中不同值的数量，以便在统计版本 2 中估算相等/IN 谓词（详见 [Versions of Statistics](#versions-of-statistics)）。

直方图是数据分布的近似表示。它将整个值域划分为一系列桶，并用简单的数据描述每个桶，例如落在该桶中的值的数量。在 TiDB 中，为每个表的特定列创建等深度直方图。等深度直方图可用于估算区间查询。

这里的“等深度”意味着每个桶中的值数量尽可能相等。例如，对于给定集合 {1.6, 1.9, 1.9, 2.0, 2.4, 2.6, 2.7, 2.7, 2.8, 2.9, 3.4, 3.5}，你希望生成 4 个桶。等深度直方图如下。它包含四个桶 [1.6, 1.9]、[2.0, 2.6]、[2.7, 2.8] 和 [2.9, 3.5]。桶深为 3。

![Equal-depth Histogram Example](/media/statistics-1.png)

关于决定直方图桶数上限的参数的详细信息，参见 [Manual Collection](#manual-collection)。桶数越多，直方图的精度越高；但同时会占用更多内存资源。你可以根据实际场景适当调整。

### Count-Min Sketch {#count-min-sketch}

> **注意：**
>
> Count-Min Sketch 仅在统计版本 1 中用于相等/IN 谓词的选择性估算。在版本 2 中，改用直方图统计信息，原因在于管理 Count-Min Sketch 以避免碰撞存在挑战（详见下文讨论）。

Count-Min Sketch 是一种哈希结构。当处理等值查询如 `a = 1` 或 `IN` 查询（例如，`a IN (1, 2, 3)`）时，TiDB 使用此数据结构进行估算。

由于 Count-Min Sketch 是哈希结构，可能会发生哈希碰撞。在 [`EXPLAIN`](/sql-statements/sql-statement-explain.md) 语句中，如果估算的等值查询结果与实际值偏差较大，可以认为较大的值和较小的值被哈希到了一起。此时，可以采取以下措施避免哈希碰撞：

-   修改 `WITH NUM TOPN` 参数。TiDB 将高频（Top x）数据单独存储，其他数据存储在 Count-Min Sketch 中。因此，为了防止较大的值和较小的值被哈希到一起，可以增加 `WITH NUM TOPN` 的值。TiDB 的默认值为 20，最大值为 1024。关于此参数的更多信息，参见 [Manual collection](#manual-collection)。
-   修改两个参数 `WITH NUM CMSKETCH DEPTH` 和 `WITH NUM CMSKETCH WIDTH`。这两个参数影响哈希桶的数量和碰撞概率。可以根据实际场景适当增大这两个参数的值，以降低碰撞概率，但会增加统计信息的内存占用。TiDB 中，`WITH NUM CMSKETCH DEPTH` 的默认值为 5，`WITH NUM CMSKETCH WIDTH` 的默认值为 2048。关于这两个参数的详细信息，参见 [Manual collection](#manual-collection)。

### Top-N {#top-n}

Top-N 值是指在某列或索引中出现频次最高的前 N 个值。Top-N 统计信息通常被称为频率统计或数据偏斜。

TiDB 记录 Top-N 值及其出现次数。这里的 `N` 由 `WITH NUM TOPN` 参数控制。默认值为 20，表示收集最频繁的前 20 个值。最大值为 1024。关于此参数的详细信息，参见 [Manual collection](#manual-collection)。

## 选择性统计信息收集 {#selective-statistics-collection}

本节介绍如何有选择性地收集统计信息。

### 收集索引的统计信息 {#collect-statistics-on-indexes}

要收集 `TableName` 中所有索引的统计信息，使用以下语法：

```sql
ANALYZE TABLE TableName INDEX [IndexNameList] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
```

当 `IndexNameList` 为空时，此语法会收集 `TableName` 中所有索引的统计信息。

> **注意：**
>
> 为确保统计信息前后保持一致，当 `tidb_analyze_version` 为 `2` 时，此语法会收集索引列和所有索引的统计信息。

### 收集部分列的统计信息 {#collect-statistics-on-some-columns}

在 TiDB 执行 SQL 语句时，优化器在大多数情况下只使用部分列的统计信息。例如，出现在 `WHERE`、`JOIN`、`ORDER BY` 和 `GROUP BY` 子句中的列。这些列被称为谓词列。

如果表有许多列，收集所有列的统计信息会带来较大开销。为减少开销，你可以只收集特定列（你选择的列）或供优化器使用的 `PREDICATE COLUMNS` 的统计信息。若要持久化任何列子集的列列表以便未来重复使用，参见 [Persist column configurations](#persist-column-configurations)。

> **注意：**
>
> -   仅在 [`tidb_analyze_version = 2`](/system-variables.md#tidb_analyze_version-new-in-v510) 时，收集谓词列的统计信息才适用。
> -   从 TiDB v7.2.0 开始，TiDB 还引入了 [`tidb_analyze_skip_column_types`](/system-variables.md#tidb_analyze_skip_column_types-new-in-v720) 系统变量，指示在执行 `ANALYZE` 收集统计信息时跳过哪些类型的列。该系统变量仅在 `tidb_analyze_version = 2` 时适用。

-   若要对特定列收集统计信息，使用以下语法：

    ```sql
    ANALYZE TABLE TableName COLUMNS ColumnNameList [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

    语法中的 `ColumnNameList` 指定目标列的名称列表。如果需要指定多个列，用逗号 `,` 分隔。例如，`ANALYZE table t columns a, b`。除了对特定表的特定列收集统计信息外，此语法还会同时收集该表中索引列和所有索引的统计信息。

-   若要对 `PREDICATE COLUMNS` 收集统计信息，使用以下语法：

    ```sql
    ANALYZE TABLE TableName PREDICATE COLUMNS [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

    <CustomContent platform="tidb">

    TiDB 会每 100 * [`stats-lease`](/tidb-configuration-file.md#stats-lease) 将 `PREDICATE COLUMNS` 信息写入 [`mysql.column_stats_usage`](/mysql-schema/mysql-schema.md#statistics-system-tables) 系统表。

    </CustomContent>

    <CustomContent platform="tidb-cloud">

    TiDB 会每 300 秒将 `PREDICATE COLUMNS` 信息写入 [`mysql.column_stats_usage`](/mysql-schema/mysql-schema.md#statistics-system-tables) 系统表。

    </CustomContent>

    除了收集特定表中 `PREDICATE COLUMNS` 的统计信息外，此语法还会同时收集索引列和所有索引的统计信息。

    > **注意：**
    >
    > -   如果 [`mysql.column_stats_usage`](/mysql-schema/mysql-schema.md#statistics-system-tables) 系统表中没有记录该表的任何 `PREDICATE COLUMNS`，则上述语法会收集索引列和所有索引的统计信息。
    > -   被排除在收集之外的列（无论是手动列出还是使用 `PREDICATE COLUMNS`）不会被覆盖统计信息。当执行新类型的 SQL 查询时，优化器会使用旧的统计信息（如果存在），或者在列从未收集统计信息时使用伪列统计信息。下一次使用 `PREDICATE COLUMNS` 进行的 `ANALYZE` 会重新收集这些列的统计信息。

-   若要收集所有列和索引的统计信息，使用以下语法：

    ```sql
    ANALYZE TABLE TableName ALL COLUMNS [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

### 收集分区的统计信息 {#collect-statistics-on-partitions}

-   要收集 `TableName` 中所有分区 `PartitionNameList` 的统计信息，使用以下语法：

    ```sql
    ANALYZE TABLE TableName PARTITION PartitionNameList [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

-   要收集 `TableName` 中所有分区 `PartitionNameList` 的索引统计信息，使用以下语法：

    ```sql
    ANALYZE TABLE TableName PARTITION PartitionNameList INDEX [IndexNameList] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

-   如果你只需要对某些分区的某些列进行 [收集统计信息](/statistics.md#collect-statistics-on-some-columns)，可以使用以下语法：

    ```sql
    ANALYZE TABLE TableName PARTITION PartitionNameList [COLUMNS ColumnNameList|PREDICATE COLUMNS|ALL COLUMNS] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

#### 在动态修剪模式下收集分区表的统计信息 {#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode}

在 [动态修剪模式](/partitioned-table.md#dynamic-pruning-mode)（自 v6.3.0 起为默认模式）下访问分区表时，TiDB 会收集表级统计信息，即分区表的全局统计信息。目前，全球统计信息是由所有分区的统计信息聚合而成。在动态修剪模式下，任何分区的统计信息更新都可能触发该表的全局统计信息更新。

如果某些分区的统计信息为空，或某些列的统计信息在某些分区中缺失，则统计信息的收集行为由 [`tidb_skip_missing_partition_stats`](/system-variables.md#tidb_skip_missing_partition_stats-new-in-v730) 变量控制：

-   当触发全局统计信息更新且 [`tidb_skip_missing_partition_stats`](/system-variables.md#tidb_skip_missing_partition_stats-new-in-v730) 为 `OFF` 时：

    -   如果某些分区没有统计信息（如新分区从未分析过），则会中断全局统计信息的生成，并显示警告信息，提示没有分区的统计信息。

    -   如果某些分区中的某些列没有统计信息（在这些分区中分析的列不同），在聚合这些列的统计信息时会中断全局统计信息的生成，并显示警告信息，提示某些列在特定分区中缺失。

-   当触发全局统计信息更新且 [`tidb_skip_missing_partition_stats`](/system-variables.md#tidb_skip_missing_partition_stats-new-in-v730) 为 `ON` 时：

    -   如果某些分区的所有或部分列的统计信息缺失，TiDB 会在生成全局统计信息时跳过这些缺失的分区统计信息，从而不影响全局统计信息的生成。

在动态修剪模式下，分区和表的 `ANALYZE` 配置应保持一致。因此，如果你在执行 `ANALYZE TABLE TableName PARTITION PartitionNameList` 语句时指定了 `COLUMNS` 配置，或在 `WITH` 后指定了 `OPTIONS` 配置，TiDB 会忽略它们并发出警告。

## 提升采集性能 {#improve-collection-performance}

> **注意：**
>
> -   TiDB 中 `ANALYZE TABLE` 的执行时间可能比 MySQL 或 InnoDB 更长。在 InnoDB 中，只采样少量页面，而 TiDB 默认会完全重建一套全面的统计信息。

TiDB 提供两种方式提升统计信息采集的性能：

-   只对部分列进行统计信息采集。详见 [Collecting statistics on some columns](#collect-statistics-on-some-columns)。
-   采样。

### 统计采样 {#statistics-sampling}

采样通过 `ANALYZE` 语句的两个不同选项实现，每个对应一种不同的采集算法：

-   `WITH NUM SAMPLES` 指定采样集的大小，在 TiDB 中采用蓄水池采样法（reservoir sampling）。当表很大时，不建议使用此方法收集统计信息，因为蓄水池采样的中间结果集包含冗余结果，会增加内存等资源压力。
-   `WITH FLOAT_NUM SAMPLERATE` 是在 v5.3.0 引入的采样方法。其值范围为 `(0, 1]`，表示采样率。TiDB 采用伯努利采样（Bernoulli sampling）实现，更适合采样较大表，且在采集效率和资源使用方面表现更优。

在 v5.3.0 之前，TiDB 使用蓄水池采样法收集统计信息。从 v5.3.0 起，TiDB 版本 2 的统计信息默认采用伯努利采样法。若要重新使用蓄水池采样法，可以使用 `WITH NUM SAMPLES` 语句。

当前采样率基于自适应算法计算。当你可以通过 [`SHOW STATS_META`](/sql-statements/sql-statement-show-stats-meta.md) 观察到表中的行数时，可以用此行数计算对应 10 万行的采样率。如果无法观察到此数字，可以用 [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md) 结果中 `APPROXIMATE_KEYS` 列的所有值之和作为参考，计算采样率。

> **注意：**
>
> 通常，`STATS_META` 比 `APPROXIMATE_KEYS` 更可靠。但当 `STATS_META` 的结果远小于 `APPROXIMATE_KEYS` 时，建议使用 `APPROXIMATE_KEYS` 来计算采样率。

### 统计信息的内存配额 {#the-memory-quota-for-collecting-statistics}

> **警告：**
>
> 目前，`ANALYZE` 的内存配额是实验性功能，生产环境中统计信息的内存统计可能不准确。

自 TiDB v6.1.0 起，你可以使用系统变量 [`tidb_mem_quota_analyze`](/system-variables.md#tidb_mem_quota_analyze-new-in-v610) 来控制 TiDB 中收集统计信息的内存配额。

在配置 `tidb_mem_quota_analyze` 时，应考虑集群的数据规模。当使用默认采样率时，主要考虑列数、列值大小和 TiDB 的内存配置。配置最大值和最小值时，建议参考如下：

> **注意：**
>
> 以下建议仅供参考，实际配置应根据具体场景调整。

-   最小值：应大于 TiDB 从行数最多的表收集统计信息时的最大内存使用量。大致参考：使用默认配置从 20 列的表收集统计信息时，最大内存约为 800 MiB；从 160 列的表收集时，最大内存约为 5 GiB。
-   最大值：应小于 TiDB 不收集统计信息时的可用内存。

## 持久化 `ANALYZE` 配置 {#persist-analyze-configurations}

自 v5.4.0 起，TiDB 支持持久化部分 `ANALYZE` 配置。通过此功能，可以方便地在未来重复使用已有的配置。

支持持久化的 `ANALYZE` 配置如下表：

| 配置项 | 对应的 `ANALYZE` 语法 |
| --- | --- |
| 直方图桶数 | `WITH NUM BUCKETS` |
| Top-N 数量 | `WITH NUM TOPN` |
| 采样次数 | `WITH NUM SAMPLES` |
| 采样率 | `WITH FLOATNUM SAMPLERATE` |
| `ANALYZE` 列类型 | AnalyzeColumnOption ::= ( 'ALL COLUMNS' | 'PREDICATE COLUMNS' | 'COLUMNS' ColumnNameList ) |
| `ANALYZE` 列 | ColumnNameList ::= Identifier ( ',' Identifier )* |

### 启用 `ANALYZE` 配置持久化 {#enable-analyze-configuration-persistence}

<CustomContent platform="tidb">

`ANALYZE` 配置持久化功能默认启用（系统变量 `tidb_analyze_version` 为 `2`，`tidb_persist_analyze_options` 默认为 `ON`）。

</CustomContent>

<CustomContent platform="tidb-cloud">

`ANALYZE` 配置持久化功能默认禁用。若要启用此功能，确保系统变量 `tidb_persist_analyze_options` 为 `ON`，并将 `tidb_analyze_version` 设置为 `2`。

</CustomContent>

你可以在手动执行 `ANALYZE` 语句时，利用此功能记录所指定的持久化配置。一旦记录，TiDB 在自动更新统计信息或你手动收集统计信息（未指定配置）时，会按照已记录的配置进行。

若要查询某个表的持久化配置（用于自动分析操作），可以使用以下 SQL：

```sql
SELECT sample_num, sample_rate, buckets, topn, column_choice, column_ids FROM mysql.analyze_options opt JOIN information_schema.tables tbl ON opt.table_id = tbl.tidb_table_id WHERE tbl.table_schema = '{db_name}' AND tbl.table_name = '{table_name}';
```

TiDB 会用最新 `ANALYZE` 语句指定的配置覆盖之前的持久化配置。例如，执行 `ANALYZE TABLE t WITH 200 TOPN;` 后，会将 Top-N 设置为 200。随后执行 `ANALYZE TABLE t WITH 0.1 SAMPLERATE;` 时，既会保持 Top-N 为 200，又会设置采样率为 0.1，效果类似于 `ANALYZE TABLE t WITH 200 TOPN, 0.1 SAMPLERATE;`。

### 禁用 `ANALYZE` 配置持久化 {#disable-analyze-configuration-persistence}

要禁用 `ANALYZE` 配置持久化功能，可以将系统变量 `tidb_persist_analyze_options` 设置为 `OFF`。由于此功能不适用于 `tidb_analyze_version = 1`，设置 `tidb_analyze_version = 1` 也会禁用此功能。

禁用后，TiDB 不会清除已持久化的配置记录。因此，如果你再次启用此功能，TiDB 仍会使用之前记录的配置进行统计信息收集。

> **注意：**
>
> 重新启用 `ANALYZE` 配置持久化后，如果之前的持久化配置不再适用最新数据，你需要手动执行 `ANALYZE` 并指定新的持久化配置。

### 持久化列配置 {#persist-column-configurations}

如果你希望在 `ANALYZE` 语句中持久化列配置（包括 `COLUMNS ColumnNameList`、`PREDICATE COLUMNS` 和 `ALL COLUMNS`），请将系统变量 `tidb_persist_analyze_options` 设置为 `ON`，以启用 [ANALYZE 配置持久化](#persist-analyze-configurations) 功能。启用后：

-   当 TiDB 自动收集统计信息或你手动执行 `ANALYZE` 时未指定列配置，TiDB 会继续使用之前持久化的配置。
-   当你多次手动执行带列配置的 `ANALYZE` 时，TiDB 会用最新的配置覆盖之前的持久化配置。

你可以使用 [`SHOW COLUMN_STATS_USAGE`](/sql-statements/sql-statement-show-column-stats-usage.md) 查看已收集统计信息的列。

以下示例中，执行 `ANALYZE TABLE t PREDICATE COLUMNS;` 后，TiDB 会对列 `b`、`c` 和 `d` 进行统计，其中列 `b` 为 `PREDICATE COLUMN`，列 `c` 和 `d` 为索引列。

```sql
CREATE TABLE t (a INT, b INT, c INT, d INT, INDEX idx_c_d(c, d));
Query OK, 0 rows affected (0.00 sec)

-- 优化器在此查询中使用列 b 的统计信息。
SELECT * FROM t WHERE b > 1;
Empty set (0.00 sec)

-- 等待一段时间（100 * stats-lease），TiDB 会将收集到的 `PREDICATE COLUMNS` 写入 mysql.column_stats_usage。
-- 指定 `last_used_at IS NOT NULL` 以显示 TiDB 收集的 `PREDICATE COLUMNS`。
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

-- 指定 `last_analyzed_at IS NOT NULL` 以显示已收集统计信息的列。
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

## 统计信息的版本 {#versions-of-statistics}

系统变量 [`tidb_analyze_version`](/system-variables.md#tidb_analyze_version-new-in-v510) 控制 TiDB 收集的统计信息。目前支持两个版本：`tidb_analyze_version = 1` 和 `tidb_analyze_version = 2`。

-   对于 TiDB 自托管版本，从 v5.3.0 起，默认值由 `1` 改为 `2`。
-   对于 TiDB 云版本，从 v6.5.0 起，默认值由 `1` 改为 `2`。
-   如果你的集群是从早期版本升级而来，升级后 `tidb_analyze_version` 的默认值不会改变。

推荐使用版本 2，并会持续增强，最终完全取代版本 1。相比版本 1，版本 2 改善了对大数据量统计信息的准确性。版本 2 还通过去除对谓词选择性估算中 Count-Min Sketch 统计的需求，以及支持只对部分列自动采集，提升了采集性能（详见 [Collecting statistics on some columns](#collect-statistics-on-some-columns)）。

以下表列出每个版本收集的统计信息，用于优化器估算的对比：

| 信息 | 版本 1 | 版本 2 |
| --- | --- | --- |
| 表中的总行数 | ⎷ | ⎷ |
| 相等/IN 谓词估算 | ⎷（列/索引 Top-N & Count-Min Sketch） | ⎷（列/索引 Top-N & Histogram） |
| 区间谓词估算 | ⎷（列/索引 Top-N & Histogram） | ⎷（列/索引 Top-N & Histogram） |
| `NULL` 谓词估算 | ⎷ | ⎷ |
| 列的平均长度 | ⎷ | ⎷ |
| 索引的平均长度 | ⎷ | ⎷ |

### 在统计版本之间切换 {#switch-between-statistics-versions}

建议确保所有表/索引（及分区）都使用相同版本的统计信息。推荐使用版本 2，但不建议在没有充分理由（如当前版本存在问题）时在两个版本之间切换。切换可能会导致一段时间内没有统计信息可用，影响优化器的执行计划选择。

切换的理由可能包括——在版本 1 中，由于哈希碰撞，可能导致相等/IN 谓词估算不准确（详见 [Count-Min Sketch](#count-min-sketch)）。解决方案列在该节中。或者，将 `tidb_analyze_version` 设置为 `2`，重新对所有对象执行 `ANALYZE` 也是一种方案。在版本 2 的早期版本中，`ANALYZE` 后存在内存溢出的风险。此问题已解决，但最初的解决方案是将 `tidb_analyze_version` 设为 `1`，然后重新对所有对象执行 `ANALYZE`。

准备在版本切换前的 `ANALYZE`：

-   如果手动执行 `ANALYZE`，请逐个分析所有需要分析的表。

    ```sql
    SELECT DISTINCT(CONCAT('ANALYZE TABLE ', table_schema, '.', table_name, ';'))
    FROM information_schema.tables JOIN mysql.stats_histograms
    ON table_id = tidb_table_id
    WHERE stats_ver = 2;
    ```

-   如果 TiDB 自动执行 `ANALYZE`，因为开启了自动分析，请执行以下语句，生成 [`DROP STATS`](/sql-statements/sql-statement-drop-stats.md) 语句：

    ```sql
    SELECT DISTINCT(CONCAT('DROP STATS ', table_schema, '.', table_name, ';'))
    FROM information_schema.tables JOIN mysql.stats_histograms
    ON table_id = tidb_table_id
    WHERE stats_ver = 2;
    ```

-   如果上述语句的结果过长，无法复制粘贴，可以导出到临时文本文件，然后从文件执行：

    ```sql
    SELECT DISTINCT ... INTO OUTFILE '/tmp/sql.txt';
    mysql -h ${TiDB_IP} -u user -P ${TIDB_PORT} ... < '/tmp/sql.txt'
    ```

## 查看统计信息 {#view-statistics}

你可以使用以下语句查看 `ANALYZE` 状态和统计信息。

### <code>ANALYZE</code> 状态 {#code-analyze-code-state}

执行 `ANALYZE` 语句时，可以使用 [`SHOW ANALYZE STATUS`](/sql-statements/sql-statement-show-analyze-status.md) 查看当前 `ANALYZE` 的状态。

从 TiDB v6.1.0 起，`SHOW ANALYZE STATUS` 支持显示集群级任务。即使重启 TiDB，也可以通过此语句查看重启前的任务记录。v6.1.0 之前，`SHOW ANALYZE STATUS` 仅能显示实例级任务，任务记录在重启后会被清除。

`SHOW ANALYZE STATUS` 只显示最新的任务记录。从 v6.1.0 起，可以通过系统表 `mysql.analyze_jobs` 查看最近 7 天内的历史任务。

当 [`tidb_mem_quota_analyze`](/system-variables.md#tidb_mem_quota_analyze-new-in-v610) 被设置，且后台运行的自动 `ANALYZE` 任务占用的内存超过此阈值时，任务会被重试。你可以在 `SHOW ANALYZE STATUS` 的输出中看到失败和重试的任务。

当 [`tidb_max_auto_analyze_time`](/system-variables.md#tidb_max_auto_analyze_time-new-in-v610) 大于 0，且后台运行的自动 `ANALYZE` 任务耗时超过此阈值时，任务会被终止。

```sql
mysql> SHOW ANALYZE STATUS [ShowLikeOrWhere];
+--------------+------------+----------------+-------------------------------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------------------------------------------------------------------------|
| Table_schema | Table_name | Partition_name | Job_info                                                                                  | Processed_rows | Start_time          | End_time            | State    | Fail_reason                                                                   |
+--------------+------------+----------------+-------------------------------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------------------------------------------------------------------------|
| test         | sbtest1    |                | retry auto analyze table all columns with 100 topn, 0.055 samplerate                      |        2000000 | 2022-05-07 16:41:09 | 2022-05-07 16:41:20 | finished | NULL                                                                          |
| test         | sbtest1    |                | auto analyze table all columns with 100 topn, 0.5 samplerate                              |              0 | 2022-05-07 16:40:50 | 2022-05-07 16:41:09 | failed   | analyze panic due to memory quota exceeds, please try with smaller samplerate |
```

### 表的元数据 {#metadata-of-tables}

你可以使用 [`SHOW STATS_META`](/sql-statements/sql-statement-show-stats-meta.md) 查看表的总行数和已更新的行数。

### 表的健康状态 {#health-state-of-tables}

你可以使用 [`SHOW STATS_HEALTHY`](/sql-statements/sql-statement-show-stats-healthy.md) 查看表的健康状态，并大致估算统计信息的准确性。当 `modify_count` >= `row_count` 时，健康状态为 0；当 `modify_count` < `row_count` 时，健康状态为 (1 - `modify_count`/`row_count`) * 100。

### 列的元数据 {#metadata-of-columns}

你可以使用 [`SHOW STATS_HISTOGRAMS`](/sql-statements/sql-statement-show-stats-histograms.md) 查看所有列中不同值的数量和 `NULL` 的数量。

### 直方图的桶 {#buckets-of-histogram}

你可以使用 [`SHOW STATS_BUCKETS`](/sql-statements/sql-statement-show-stats-buckets.md) 查看直方图的每个桶。

### Top-N 信息 {#top-n-information}

你可以使用 [`SHOW STATS_TOPN`](/sql-statements/sql-statement-show-stats-topn.md) 查看 TiDB 当前收集的 Top-N 信息。

## 删除统计信息 {#delete-statistics}

你可以运行 [`DROP STATS`](/sql-statements/sql-statement-drop-stats.md) 语句删除统计信息。

## 加载统计信息 {#load-statistics}

> **注意：**
>
> 目前，TiDB 不支持在 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群中加载统计信息。

默认情况下，TiDB 根据列统计信息的大小采用不同的加载策略：

-   对于占用内存较少的统计信息（如 count、distinctCount 和 nullCount），只要列数据更新，TiDB 会自动将对应的统计信息加载到内存中，用于 SQL 优化阶段。
-   对于占用内存较大的统计信息（如直方图、TopN 和 Count-Min Sketch），为了保证 SQL 执行性能，TiDB 会按需异步加载统计信息。以直方图为例，只有在优化器使用某列的直方图统计信息时，才会将其加载到内存。按需异步加载不会影响 SQL 执行性能，但可能导致统计信息不完整，从而影响优化。

自 v5.4.0 起，TiDB 引入了同步加载统计信息的功能。该功能允许 TiDB 在执行 SQL 语句时同步加载大尺寸统计信息（如直方图、TopN 和 Count-Min Sketch），以提升统计信息的完整性。

要启用此功能，可以将系统变量 [`tidb_stats_load_sync_wait`](/system-variables.md#tidb_stats_load_sync_wait-new-in-v540) 设置为一个超时时间（毫秒），SQL 优化最多等待此时间以同步加载完整的列统计信息。该变量的默认值为 `100`，表示启用此功能。

<CustomContent platform="tidb">

启用同步加载统计信息后，你还可以进一步配置此功能：

-   若要控制 SQL 优化等待超时后的行为，修改系统变量 [`tidb_stats_load_pseudo_timeout`](/system-variables.md#tidb_stats_load_pseudo_timeout-new-in-v540)。默认值为 `ON`，表示超时后，SQL 优化不会使用任何列的直方图、TopN 或 CMSketch 统计信息。若设置为 `OFF`，超时后，SQL 执行会失败。
-   若要限制同步加载统计信息的最大列数，修改 TiDB 配置文件中的 [`stats-load-concurrency`] 选项。自 v8.2.0 起，默认值为 `0`，表示 TiDB 会根据服务器配置自动调整并发数。
-   若要限制同步加载统计信息的最大列请求缓存数，修改 TiDB 配置文件中的 [`stats-load-queue-size`] 选项。默认值为 `1000`。

在 TiDB 启动过程中，统计信息未完全加载前执行的 SQL 语句可能会导致执行计划不理想，从而影响性能。为避免此类问题，TiDB v7.1.0 引入了 [`force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v657-and-v710) 配置参数。启用后，TiDB 在启动时会控制是否在统计信息初始化完成后才提供服务。自 v7.2.0 起，该参数默认启用。

自 v7.1.0 起，TiDB 还引入了 [`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710)，用于轻量级统计初始化。

-   当 `lite-init-stats` 取值为 `true` 时，统计初始化不会将索引或列的直方图、TopN 和 Count-Min Sketch 加载到内存。
-   当 `lite-init-stats` 取值为 `false` 时，统计初始化会将索引和主键的直方图、TopN 和 Count-Min Sketch 加载到内存，但不会加载非主键列的直方图、TopN 和 Count-Min Sketch。优化器在需要特定索引或列的直方图、TopN 和 Count-Min Sketch 时，会同步或异步加载所需的统计信息。

`lite-init-stats` 的默认值为 `true`，表示启用轻量级统计初始化。设置为 `true` 可以加快统计初始化速度，减少 TiDB 的内存占用，避免不必要的统计信息加载。

</CustomContent>

<CustomContent platform="tidb-cloud">

启用同步加载统计信息后，你可以通过修改系统变量 [`tidb_stats_load_pseudo_timeout`](/system-variables.md#tidb_stats_load_pseudo_timeout-new-in-v540) 来控制 TiDB 在等待超时时的行为。默认值为 `ON`，表示超时后，SQL 优化不会使用任何列的直方图、TopN 或 CMSketch 统计信息。

</CustomContent>

## 导出与导入统计信息 {#export-and-import-statistics}

本节介绍如何导出和导入统计信息。

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 本节内容不适用于 TiDB 云。

</CustomContent>

### 导出统计信息 {#export-statistics}

导出统计信息的接口如下：

-   获取 `${db_name}` 数据库中 `${table_name}` 表的 JSON 格式统计信息：

        http://${tidb-server-ip}:${tidb-server-status-port}/stats/dump/${db_name}/${table_name}

    例如：

    ```shell
    curl -s http://127.0.0.1:10080/stats/dump/test/t1 -o /tmp/t1.json
    ```

-   获取 `${db_name}` 数据库中 `${table_name}` 表在特定时间点的 JSON 格式统计信息：

        http://${tidb-server-ip}:${tidb-server-status-port}/stats/dump/${db_name}/${table_name}/${yyyyMMddHHmmss}

### 导入统计信息 {#import-statistics}

> **注意：**
>
> 启动 MySQL 客户端时，请使用 `--local-infile=1` 选项。

导入的统计信息通常指通过导出接口获得的 JSON 文件。

可以使用 [`LOAD STATS`](/sql-statements/sql-statement-load-stats.md) 语句加载统计信息。

例如：

```sql
LOAD STATS 'file_name';
```

`file_name` 为待导入的统计信息文件名。

## 锁定统计信息 {#lock-statistics}

自 v6.5.0 起，TiDB 支持锁定统计信息。锁定某个表或分区的统计信息后，该表的统计信息将无法被修改，也不能对其执行 `ANALYZE`。例如：

创建表 `t`，插入数据。当表 `t` 的统计信息未被锁定时，可以成功执行 `ANALYZE`。

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

锁定表 `t` 的统计信息并执行 `ANALYZE`，会显示警告，提示跳过了该表。

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

此外，还可以使用 [`LOCK STATS`](/sql-statements/sql-statement-lock-stats.md) 来锁定分区的统计信息。例如：

创建分区表 `t`，插入数据。当分区 `p1` 的统计信息未被锁定时，可以成功执行 `ANALYZE`。

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

锁定分区 `p1` 的统计信息并执行 `ANALYZE`，会显示警告，提示跳过了分区 `p1`。

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
