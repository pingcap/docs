---
title: 创建表
summary: 了解表创建中的定义、规则和指南。
---

# 创建表

本文档介绍如何使用 SQL 语句创建表以及相关的最佳实践。提供一个基于 TiDB 的 [Bookshop](/develop/dev-guide-bookshop-schema-design.md) 应用示例，以说明最佳实践。

## 在开始之前

在阅读本文档之前，请确保已完成以下任务：

- [构建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md)。
- 阅读 [Schema 设计概述](/develop/dev-guide-schema-design-overview.md)。
- [创建数据库](/develop/dev-guide-create-database.md)。

## 什么是表

[表](/develop/dev-guide-schema-design-overview.md#table) 是 TiDB 集群中的一个逻辑对象，属于 [数据库](/develop/dev-guide-schema-design-overview.md#database) 的子集。它用于存储由 SQL 语句传送的数据。表以行和列的形式保存数据记录。一个表至少有一列。如果定义了 n 列，则每一行数据的字段与这 n 列完全相同。

## 给表命名

创建表的第一步是为你的表命名。不要使用无意义的名字，否则将来会给自己或同事带来极大的困扰。建议遵循你所在公司或组织的表命名规范。

`CREATE TABLE` 语句通常采用以下形式：

```sql
CREATE TABLE {table_name} ( {elements} );
```

**参数说明**

- `{table_name}`：要创建的表名。
- `{elements}`：用逗号分隔的表元素列表，例如列定义和主键定义。

假设你需要在 `bookshop` 数据库中创建一个存储用户信息的表。

注意，目前还不能执行以下 SQL 语句，因为还没有添加任何列。

```sql
CREATE TABLE `bookshop`.`users` (
);
```

## 定义列

**列**是表的子集。每个表至少有一列。列为表提供结构，将每一行中的值划分为单个数据类型的小单元。

列定义通常采用以下格式。

```
{column_name} {data_type} {column_qualification}
```

**参数说明**

- `{column_name}`：列名。
- `{data_type}`：列的 [数据类型](/data-type-overview.md)。
- `{column_qualification}`：列的限定条件，例如 **列级约束** 或 [生成列](/generated-columns.md) 子句。

你可以为 `users` 表添加一些列，例如唯一标识符 `id`、`balance` 和 `nickname`。

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint,
  `nickname` varchar(100),
  `balance` decimal(15,2)
);
```

在上述语句中，定义了一个名为 `id` 的字段，类型为 [bigint](/data-type-numeric.md#bigint-type)，用于表示唯一的用户标识符。这意味着所有用户标识符都应为 `bigint` 类型。

然后，定义了一个名为 `nickname` 的字段，类型为 [varchar](/data-type-string.md#varchar-type)，长度限制为 100 个字符。这意味着用户的昵称使用 `varchar` 类型，且不超过 100 个字符。

最后，添加了一个名为 `balance` 的字段，类型为 [decimal](/data-type-numeric.md#decimal-type)，精度为 `15`，小数位数为 `2`。**精度**表示字段中的总位数，**小数位数**表示小数点后的位数。例如，`decimal(5,2)` 表示精度为 `5`，小数位为 `2`，范围从 `-999.99` 到 `999.99`。`decimal(6,1)` 表示精度为 `6`，小数位为 `1`，范围从 `-99999.9` 到 `99999.9`。**decimal** 是一种 [定点类型](/data-type-numeric.md#fixed-point-types)，可以用来存储精确的数字。在需要精确数字的场景（例如用户属性相关）中，务必使用 **decimal** 类型。

TiDB 支持多种其他列数据类型，包括 [整数类型](/data-type-numeric.md#integer-types)、[浮点类型](/data-type-numeric.md#floating-point-types)、[定点类型](/data-type-numeric.md#fixed-point-types)、[日期和时间类型](/data-type-date-and-time.md) 以及 [枚举类型](/data-type-string.md#enum-type)。你可以参考支持的列 [数据类型](/data-type-overview.md)，选择符合你存储需求的类型。

为了让表结构更复杂一些，可以定义一个 `books` 表，作为 `bookshop` 数据的核心。`books` 表包含书籍的 ID、标题、类型（例如，杂志、小说、生活、艺术）、库存、价格和出版日期等字段。

```sql
CREATE TABLE `bookshop`.`books` (
  `id` bigint NOT NULL,
  `title` varchar(100),
  `type` enum('Magazine', 'Novel', 'Life', 'Arts', 'Comics', 'Education & Reference', 'Humanities & Social Sciences', 'Science & Technology', 'Kids', 'Sports'),
  `published_at` datetime,
  `stock` int,
  `price` decimal(15,2)
);
```

此表包含比 `users` 表更多的数据类型。

- [int](/data-type-numeric.md#integer-types)：建议使用合适大小的类型，避免占用过多存储空间，影响性能（类型范围过大）或导致数据溢出（类型范围过小）。
- [datetime](/data-type-date-and-time.md)：**datetime** 类型可用于存储时间值。
- [enum](/data-type-string.md#enum-type)：enum 类型可用于存储有限的值集。

## 选择主键

[主键](/constraints.md#primary-key) 是表中的一列或多列，其值唯一标识表中的一行。

> **注意：**
>
> TiDB 中的 **primary key** 默认定义与 [InnoDB](https://dev.mysql.com/doc/refman/8.0/en/innodb-storage-engine.html)（MySQL 的常用存储引擎）不同。
>
> - 在 **InnoDB** 中：**primary key** 是唯一的、非空的，并且是 **索引簇**。
>
> - 在 TiDB 中：**primary key** 是唯一的且非空的，但不保证是 **簇索引**。相反，`CLUSTERED` / `NONCLUSTERED` 关键字额外控制 **primary key** 是否为 **簇索引**。如果未指定关键字，则由系统变量 `@@global.tidb_enable_clustered_index` 控制，如 [簇索引](https://docs.pingcap.com/tidb/stable/clustered-indexes) 所述。

**primary key** 在 `CREATE TABLE` 语句中定义。 [primary key 约束](/constraints.md#primary-key) 要求所有受约束的列不能包含 NULL 值。

可以创建没有 **primary key** 或使用非整数 **primary key** 的表。在这种情况下，TiDB 会自动创建一个 `_tidb_rowid` 作为 **隐式主键**。由于 `_tidb_rowid` 是单调递增的，可能在写入密集场景中引发写入热点。因此，如果你的应用写入量大，建议使用 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md) 和 [`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions) 参数进行数据分片。但这可能会导致读取放大，因此需要权衡。

当表的 **primary key** 是 [整数类型](/data-type-numeric.md#integer-types) 且使用 `AUTO_INCREMENT` 时，无法通过 `SHARD_ROW_ID_BITS` 避免热点。如果需要避免热点且不需要连续递增的主键，可以使用 [`AUTO_RANDOM`](/auto-random.md) 替代 `AUTO_INCREMENT`，以消除行 ID 的连续性。

<CustomContent platform="tidb">

关于如何处理热点问题的更多信息，请参考 [排查热点问题](/troubleshoot-hot-spot-issues.md)。

</CustomContent>

遵循 [选择主键的指南](#guidelines-to-follow-when-selecting-primary-key)，以下示例展示了在 `users` 表中定义 `AUTO_RANDOM` 主键。

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM,
  `balance` decimal(15,2),
  `nickname` varchar(100),
  PRIMARY KEY (`id`)
);
```

## 是否为簇索引

TiDB 从 v5.0 开始支持 [簇索引](/clustered-indexes.md)。此功能控制含有主键的表中数据的存储方式。它使 TiDB 能够以某种方式组织表，从而提升特定查询的性能。

“簇”在此处指数据的存储组织方式，而不是一组协作的数据库服务器。一些数据库管理系统将簇索引表称为索引组织表（IOT）。

目前，TiDB 中 **_含有主键_** 的表分为以下两类：

- `NONCLUSTERED`：表的主键为非簇索引。在非簇索引的表中，行数据的键由 TiDB 内部隐式分配的 `_tidb_rowid` 组成。由于主键本质上是唯一索引，非簇索引的表需要至少两个键值对来存储一行：
    - `_tidb_rowid`（键） - 行数据（值）
    - 主键数据（键） - `_tidb_rowid`（值）
- `CLUSTERED`：表的主键为簇索引。在簇索引的表中，行数据的键由用户提供的主键数据组成。因此，簇索引的表只需要一个键值对来存储一行：
    - 主键数据（键） - 行数据（值）

如 [选择主键](#select-primary-key) 所述，**簇索引** 在 TiDB 中通过 `CLUSTERED` 和 `NONCLUSTERED` 关键字控制。

> **注意：**
>
> TiDB 仅支持通过表的 `PRIMARY KEY` 进行簇索引。启用簇索引后，术语 _the_ `PRIMARY KEY` 和 _the clustered index_ 可能会交替使用。`PRIMARY KEY` 指约束（逻辑属性），而簇索引描述数据存储的物理实现。

遵循 [选择簇索引的指南](#guidelines-to-follow-when-selecting-clustered-index)，以下示例创建了一个 `ratings` 表，表示 `book` 被 `users` 评分的关系，使用 `book_id` 和 `user_id` 组成复合主键，并在该 **主键** 上建立 **簇索引**。

```sql
CREATE TABLE `bookshop`.`ratings` (
  `book_id` bigint,
  `user_id` bigint,
  `score` tinyint,
  `rated_at` datetime,
  PRIMARY KEY (`book_id`,`user_id`) CLUSTERED
);
```

## 添加列约束

除了 [主键约束](#select-primary-key)，TiDB 还支持其他 **列约束**，如 [NOT NULL](/constraints.md#not-null) 约束、[UNIQUE KEY](/constraints.md#unique-key) 约束，以及 `DEFAULT`。完整的约束请参考 [TiDB 约束](/constraints.md) 文档。

### 设置默认值

要为列设置默认值，使用 `DEFAULT` 约束。默认值允许你在插入数据时不为每列指定值。

可以结合 [支持的 SQL 函数](/functions-and-operators/functions-and-operators-overview.md) 使用 `DEFAULT`，将默认值的计算从应用层转移到数据库层，从而节省应用资源。计算所用资源不会消失，而是转移到 TiDB 集群中。常见的用法是插入当前时间。以下示例在 `ratings` 表中设置默认值：

```sql
CREATE TABLE `bookshop`.`ratings` (
  `book_id` bigint,
  `user_id` bigint,
  `score` tinyint,
  `rated_at` datetime DEFAULT NOW(),
  PRIMARY KEY (`book_id`,`user_id`) CLUSTERED
);
```

此外，如果在数据更新时也希望自动填充当前时间，可以使用以下语句（但只有与当前时间相关的表达式可以在 `ON UPDATE` 后填写）：

```sql
CREATE TABLE `bookshop`.`ratings` (
  `book_id` bigint,
  `user_id` bigint,
  `score` tinyint,
  `rated_at` datetime DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`book_id`,`user_id`) CLUSTERED
);
```

关于不同数据类型的默认值的更多信息，请参见 [默认值](/data-type-default-values.md)。

### 防止重复值

如果需要防止列中出现重复值，可以使用 `UNIQUE` 约束。

例如，为确保用户的昵称唯一，可以将 `users` 表的创建 SQL 改写为：

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM,
  `balance` decimal(15,2),
  `nickname` varchar(100) UNIQUE,
  PRIMARY KEY (`id`)
);
```

尝试在 `users` 表中插入相同的 `nickname` 时，会返回错误。

### 防止空值

如果需要防止列中出现 NULL 值，可以使用 `NOT NULL` 约束。

以用户昵称为例。为了确保昵称不仅唯一，而且非空，可以将创建 `users` 表的 SQL 改写为：

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM,
  `balance` decimal(15,2),
  `nickname` varchar(100) UNIQUE NOT NULL,
  PRIMARY KEY (`id`)
);
```

## 使用 HTAP 功能

<CustomContent platform="tidb">

> **注意：**
>
> 本指南提供的步骤 **_仅_** 适用于测试环境的快速启动。对于生产环境，请参考 [探索 HTAP](/explore-htap.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 本指南提供的步骤 **_仅_** 适用于快速启动。更多指引请参考 [使用 TiFlash 的 HTAP 集群](/tiflash/tiflash-overview.md)。

</CustomContent>

假设你希望对 `ratings` 表进行 OLAP 分析，例如，查询 **某本书的评分是否与评分时间有显著相关性**，以分析用户对书的评分是否客观。你需要查询整个 `score` 和 `rated_at` 字段。这对于纯 OLTP 数据库来说是资源密集型操作。或者，你可以使用一些 ETL 或其他数据同步工具，将 OLTP 数据导出到专门的 OLAP 数据库进行分析。

在这种场景下，TiDB 作为支持 OLTP 和 OLAP 的 **HTAP（Hybrid Transactional and Analytical Processing）** 数据库，是理想的一站式解决方案。

### 复制列数据

<CustomContent platform="tidb">

目前，TiDB 支持两种数据分析引擎，**TiFlash** 和 **TiSpark**。对于大数据场景（100 T 及以上），推荐使用 **TiFlash MPP** 作为 HTAP 的主要方案，**TiSpark** 作为补充方案。

想了解更多 TiDB HTAP 功能，请参考： [TiDB HTAP 快速入门指南](/quick-start-with-htap.md) 和 [探索 HTAP](/explore-htap.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

想了解更多 TiDB HTAP 功能，请参阅：[TiDB Cloud HTAP 快速入门](/tidb-cloud/tidb-cloud-htap-quickstart.md) 和 [使用 TiFlash 的 HTAP 集群](/tiflash/tiflash-overview.md)。

</CustomContent>

在此示例中，已选择 [TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview) 作为 `bookshop` 数据库的数据分析引擎。

TiFlash 部署后不会自动复制数据，因此需要手动指定要复制的表：

```sql
ALTER TABLE {table_name} SET TIFLASH REPLICA {count};
```

**参数说明**

- `{table_name}`：表名。
- `{count}`：复制副本数。如果为 0，则删除复制副本。

**TiFlash** 会开始复制表。当执行查询时，TiDB 会根据成本自动选择 TiKV（行存）或 TiFlash（列存）进行查询。也可以手动指定查询是否使用 **TiFlash** 副本。详细操作请参考 [使用 TiDB 读取 TiFlash 副本](/tiflash/use-tidb-to-read-tiflash.md)。

### 使用 HTAP 功能的示例

将 `ratings` 表开启 1 个 TiFlash 副本：

```sql
ALTER TABLE `bookshop`.`ratings` SET TIFLASH REPLICA 1;
```

> **注意：**
>
> 如果你的集群没有 **TiFlash** 节点，此 SQL 语句会报错：`1105 - the tiflash replica count: 1 should be less than the total tiflash server count: 0`。你可以使用 [构建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-tidb-cloud-cluster) 来创建包含 **TiFlash** 的 {{{ .starter }}} 集群。

然后，你可以执行以下查询：

```sql
SELECT HOUR(`rated_at`), AVG(`score`) FROM `bookshop`.`ratings` GROUP BY HOUR(`rated_at`);
```

你也可以执行 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 来查看此语句是否使用了 **TiFlash**：

```sql
EXPLAIN ANALYZE SELECT HOUR(`rated_at`), AVG(`score`) FROM `bookshop`.`ratings` GROUP BY HOUR(`rated_at`);
```

运行结果示例：

```plaintext
+-----------------------------+-----------+---------+--------------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------+----------+------+
| id                          | estRows   | actRows | task         | access object | execution info                                                                                                                                                                                                                                                                                                                                                       | operator info                                                                                                                                  | memory   | disk |
+-----------------------------+-----------+---------+--------------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------+----------+------+
| Projection_4                | 299821.99 | 24      | root         |               | time:60.8ms, loops:6, Concurrency:5                                                                                                                                                                                                                                                                                                                                  | hour(cast(bookshop.ratings.rated_at, time))->Column#6, Column#5                                                                                | 17.7 KB  | N/A  |
| └─HashAgg_5                 | 299821.99 | 24      | root         |               | time:60.7ms, loops:6, partial_worker:{wall_time:60.660079ms, concurrency:5, task_num:293, tot_wait:262.536669ms, tot_exec:40.171833ms, tot_time:302.827753ms, max:60.636886ms, p95:60.636886ms}, final_worker:{wall_time:60.701437ms, concurrency:5, task_num:25, tot_wait:303.114278ms, tot_exec:176.564µs, tot_time:303.297475ms, max:60.69326ms, p95:60.69326ms}  | group by:Column#10, funcs:avg(Column#8)->Column#5, funcs:firstrow(Column#9)->bookshop.ratings.rated_at                                         | 714.0 KB | N/A  |
|   └─Projection_15           | 300000.00 | 300000  | root         |               | time:58.5ms, loops:294, Concurrency:5                                                                                                                                                                                                                                                                                                                                | cast(bookshop.ratings.score, decimal(8,4) BINARY)->Column#8, bookshop.ratings.rated_at, hour(cast(bookshop.ratings.rated_at, time))->Column#10 | 366.2 KB | N/A  |
|     └─TableReader_10        | 300000.00 | 300000  | root         |               | time:43.5ms, loops:294, cop_task: {num: 1, max: 43.1ms, proc_keys: 0, rpc_num: 1, rpc_time: 43ms, copr_cache_hit_ratio: 0.00}                                                                                                                                                                                                                                        | data:TableFullScan_9                                                                                                                           | 4.58 MB  | N/A  |
|       └─TableFullScan_9     | 300000.00 | 300000  | cop[tiflash] | table:ratings | tiflash_task:{time:5.98ms, loops:8, threads:1}, tiflash_scan:{dtfile:{total_scanned_packs:45, total_skipped_packs:1, total_scanned_rows:368640, total_skipped_rows:8192, total_rs_index_load_time: 1ms, total_read_time: 1ms},total_create_snapshot_time:1ms}                                                                                                        | keep order:false                                                                                                                               | N/A      | N/A  |
+-----------------------------+-----------+---------+--------------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------+----------+------+
```

当字段 `cop[tiflash]` 出现时，表示任务由 **TiFlash** 处理。

## 执行 `CREATE TABLE` 语句

按照上述规则创建完所有表后，我们的 [数据库初始化](/develop/dev-guide-bookshop-schema-design.md#database-initialization-script-dbinitsql) 脚本应如下所示。如需详细查看表信息，请参考 [表的描述](/develop/dev-guide-bookshop-schema-design.md#description-of-the-tables)。

将数据库初始化脚本命名为 `init.sql` 并保存，可以执行以下命令初始化数据库。

```shell
mysql
    -u root \
    -h {host} \
    -P {port} \
    -p {password} \
    < init.sql
```

使用 [`SHOW TABLES`](/sql-statements/sql-statement-show-tables.md#show-full-tables) 查看 `bookshop` 数据库下的所有表。

```sql
SHOW TABLES IN `bookshop`;
```

运行结果：

```
+--------------------+
| Tables_in_bookshop |
+--------------------+
| authors            |
| book_authors       |
| books              |
| orders             |
| ratings            |
| users              |
+--------------------+
```

## 创建表时的指南

本节提供创建表时需要遵循的指南。

### 命名表的指南

- 使用**完全限定**的表名（例如，`CREATE TABLE {database_name}. {table_name}`）。如果不指定数据库名，TiDB 会使用你在 **SQL 会话** 中的当前数据库。如果没有使用 `USE {databasename};` 指定数据库，TiDB 会返回错误。
- 使用有意义的表名。例如，若需要创建用户表，可以用 `user`、`t_user`、`users`，或遵循你所在公司或组织的命名规范。如果没有命名规范，可以参考 [表命名规范](/develop/dev-guide-object-naming-guidelines.md#table-naming-convention)。不要使用诸如 `t1`、`table1` 这样的名字。
- 多个单词用下划线分隔，建议名字长度不超过 32 个字符。
- 为不同业务模块的表创建单独的 `DATABASE`，并添加相应注释。

### 定义列的指南

- 查看支持的 [数据类型](/data-type-overview.md)，根据数据类型限制组织你的数据。为列选择合适的类型。
- 查看 [选择主键的指南](#guidelines-to-follow-when-selecting-primary-key)，决定是否使用主键列。
- 查看 [选择簇索引的指南](#guidelines-to-follow-when-selecting-clustered-index)，决定是否指定 **簇索引**。
- 查看 [添加列约束](#add-column-constraints)，决定是否为列添加约束。
- 使用有意义的列名。建议遵循你所在公司或组织的表命名规范。如果没有，可以参考 [列命名规范](/develop/dev-guide-object-naming-guidelines.md#column-naming-convention)。

### 选择主键的指南

- 在表中定义 **主键** 或 **唯一索引**。
- 尽量选择有意义的 **列** 作为 **主键**。
- 出于性能考虑，避免存储过宽的表。建议表字段数不超过 `60`，单行数据总大小不超过 `64K`。过多的数据长度应拆分到其他表。
- 不建议使用复杂数据类型。
- 对于需要连接的字段，确保数据类型一致，避免隐式转换。
- 避免在单一单调数据列上定义 **主键**。如果使用单一单调数据列（如带 `AUTO_INCREMENT` 属性的列）作为 **主键**，可能影响写入性能。建议使用 `AUTO_RANDOM` 替代 `AUTO_INCREMENT`，以避免主键的连续递增特性。
- 如果在写入密集场景中确实需要在单调数据列上建立索引，不要将其作为 **主键**，而是使用 `AUTO_RANDOM` 创建 **主键**，或结合 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md) 和 [`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions) 进行数据分片。

### 选择簇索引的指南

- 遵循 [选择主键的指南](#guidelines-to-follow-when-selecting-primary-key) 来构建 **簇索引**。
- 相较于非簇索引的表，簇索引表在以下场景中具有更高的性能和吞吐量优势：
    - 插入数据时，簇索引减少一次网络写入索引数据。
    - 查询条件只涉及主键时，簇索引减少一次网络读取索引数据。
    - 范围查询只涉及主键时，簇索引减少多次网络读取。
    - 仅涉及主键前缀的等值或范围条件查询，簇索引减少多次网络读取。
- 另一方面，簇索引表可能存在以下问题：
    - 当插入大量值接近的主键时，可能出现写入热点。请遵循 [选择主键的指南](#guidelines-to-follow-when-selecting-primary-key)。
    - 如果主键数据类型大于 64 位，且存在多个二级索引，可能占用更多存储空间。

- 关于 [控制是否使用簇索引的默认行为](/clustered-indexes.md#create-a-table-with-clustered-indexes)，可以显式指定是否使用簇索引，而不是依赖系统变量 `@@global.tidb_enable_clustered_index` 和配置 `alter-primary-key`。

### 执行 `CREATE TABLE` 语句的指南

- 不建议使用客户端驱动或 ORM 进行数据库 schema 变更。建议使用 [MySQL 客户端](https://dev.mysql.com/doc/refman/8.0/en/mysql.html) 或 GUI 客户端进行 schema 变更。在本文档中，大部分场景使用 **MySQL 客户端**传入 SQL 文件进行 schema 变更。
- 遵循 SQL 开发 [创建和删除表的规范](/develop/dev-guide-sql-development-specification.md#create-and-delete-tables)。建议将建表和删除语句封装在业务应用中，加入判断逻辑。

## 还有一步

注意，本文中创建的所有表都没有包含二级索引。如需添加二级索引的指南，请参考 [创建二级索引](/develop/dev-guide-create-secondary-indexes.md)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>