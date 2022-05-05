---
title: Create a Table
summary: The ways, best practices, and examples for creating tables.
---

# Create a Table

This page provides a best practice guide for creating tables and an example of a [bookshop](/develop/bookshop-schema-design.md) database based on TiDB.

> **Note:**
>
> Detailed reference documentation for this `CREATE TABLE` statement, including additional examples, can be found in the [CREATE TABLE](https://docs.pingcap.com/zh/tidb/stable/sql-statement-create-table) documentation.

## Before you start

Before reading this page, you need to prepare the following:

- [Build a TiDB Cluster in TiDB Cloud(DevTier)](/develop/build-cluster-in-cloud.md).
- Read [Schema Design Overview](/develop/schema-design-overview.md).
- [Create a Database](/develop/create-database.md).

## How to create a table

[Table](/develop/schema-design-overview.md#table) is a logical object. It would stores data sent from the persistence layer of an application or from other SQL. Tables saved data records in the form of rows and columns.

To create a table, use the [CREATE TABLE](https://docs.pingcap.com/tidb/stable/sql-statement-create-table) statement and follow the best practices:

- [Naming a table](#naming-a-table)
- [Defining columns](#defining-columns)
- [Select primary key](#select-primary-key)
- [Clustered or not](#clustered-or-not)
- [Add column constraints](#add-column-constraints)
- [Using HTAP capabilities](#using-htap-capabilities)
- [Execute the `CREATE TABLE` statement](#execute-the-create-table-statement)

After reviewing each best practice, you can take a look at the examples provided in this page.

### Naming a table

Giving your table a name is the first step in creating it. We recommend that you follow your company or organization's table naming convention.

The `CREATE TABLE` statement usually takes the following form.

{{< copyable "sql" >}}

```sql
CREATE TABLE {table_name} ( {elements} );
```

|      Parameter      |                      Description                      |
| :------------: | :--------------------------------------------: |
| `{table_name}` |                      Table name                      |
|  `{elements}`  | A comma-separated list of table elements, such as column definitions, primary key definitions, etc. |

#### Best Practices for naming a table

There are some best practices to follow when naming tables:

- Use a **fully-qualified** table name (i.e., `CREATE TABLE {database_name}. {table_name}`). This is because when you do not specify a database name, TiDB will use the current database in your **SQL session**. If you do not use `USE {databasename};` to specify the database in your SQL session, TiDB will return an error.
- Use meaningful table names, for example, if you need to create a user table, you can use names: `user`, `t_user`, `users`, etc., or follow your company or organization's naming convention. If your company or organization does not have a naming convention, you can refer to the [table naming convention](/develop/object-naming-guidelines.md#table-naming-convention). Do not use such table names as: `t1`, `table1`, etc.
- Multiple words are separated by an underscore, more than 32 characters are not recommended.
- Create separate DATABASE for tables of different business modules and add comments accordingly.
- Create a separate `DATABASE` for the tables of different business modules and add comments accordingly.

#### Table naming example

Suppose you need to create a table to store the user information in the `bookshop` database.

Note that the following SQL cannot be run yet because not a single column has been added.

{{< copyable "sql" >}}

```sql
CREATE TABLE `bookshop`.`users` (
);
```

### Defining columns

**Columns** provide structure to a table by dividing the values in each row into small cells of a single data type.

Column definitions typically use the following form.

```
{column_name} {data_type} {column_qualification}
```

|      Parameter      |                      Description                      |
| :----------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|     `{column_name}`      |                                                                               Column name                                                                                |
|      `{data_type}`       | Column [data type](https://docs.pingcap.com/tidb/stable/basic-features#data-types-functions-and-operators) |
| `{column_qualification}` | Column qualifications, such as **column-level constraints** or [generated column (experimental function)](https://docs.pingcap.com/tidb/stable/generated-columns) clauses |

#### Best Practices for defining columns

There are some best practices to follow when defining columns:

- Check the [data types](https://docs.pingcap.com/tidb/stable/basic-features#data-types-functions-and-operators) of the supporting columns and organize your data according to the data type restrictions. Select the appropriate type for the data you plan to be present in the column.
- Check the [best practices](#best-practices-for-select-primary-key) and [examples](#select-primary-key-example) for selecting primary keys and decide whether to use primary key columns.
- Check [best practices](#best-practices-for-select-clustered-index) and [examples](#select-clustered-index-example) for selecting clustered indexes and decide whether to specify **clustered indexes**.
- Check [adding column constraints](#add-column-constraints) and decide whether to add constraints to the columns.
- Please use meaningful column names. we recommend that you follow your company or organization's table naming convention. If your company or organization does not have a corresponding naming convention, refer to the [column naming convention](/develop/object-naming-guidelines.md#field-naming-convention).

#### Defining columns example

We can add some columns to the `users` table, such as their unique identifier `id`, `balance` and `nickname`.

{{< copyable "sql" >}}

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint,
  `nickname` varchar(100),
  `balance` decimal(15,2)
);
```

In this case, we define a field with the name `id` and the type [bigint](https://docs.pingcap.com/tidb/stable/data-type-numeric#bigint-type). This is used to represent a unique user identifier. This means that all user identifiers should be of type `bigint`.

After that, we define a field named `nickname`, of type [varchar](https://docs.pingcap.com/tidb/stable/data-type-string#varchar-type), and not longer than 100 characters. This means that the `nicknames` of the users used `varchar` type and were not longer than `100` characters.

Finally, we added a field named `balance`, type is [decimal](https://docs.pingcap.com/tidb/stable/data-type-numeric#decimal-type), with a **precision** of `15` and a **scale** of `2`. To briefly explain the meaning of **precision** and **scale**, **precision** represents the total number of digits in the field, and **scale** represents the number of decimal places. For example: `decimal(5,2)`, i.e., with a precision of `5` and a scale of `2`, the range is `-999.99` to `999.99`. `decimal(6,1)`, i.e., with a precision of `6` and a scale of `1`, the range is `-99999.9` to `99999.9`. **decimal** is a [fixed-point types](https://docs.pingcap.com/tidb/stable/data-type-numeric#fixed-point-types), which can be used to store numbers accurately, in scenarios where accurate numbers are needed (e.g., user property-related), please **make sure** to use the **decimal** type.

TiDB supports many other column data types, including [Integer types](https://docs.pingcap.com/tidb/stable/data-type-numeric#integer-types), [Floating-point types](https://docs.pingcap.com/tidb/stable/data-type-numeric#floating-point-types), [Fixed-point types](https://docs.pingcap.com/tidb/stable/data-type-numeric#fixed-point-types), [Date and time types](https://docs.pingcap.com/tidb/stable/data-type-date-and-time), [Enum type](https://docs.pingcap.com/tidb/stable/data-type-string#enum-type), etc. You can refer to the supported column [data types](https://docs.pingcap.com/tidb/stable/basic-features#data-types-functions-and-operators) and use the **data types** that match the data you want to save in the database.

让我们稍微提升一下复杂度，例如我们会选择定义一张 `books` 表，这张表将是 `bookshop` 数据的核心。它包含书的 唯一标识、名称、书籍类型（如：杂志、动漫、教辅 等）、库存、价格、出版时间 字段。

Let's increase the complexity a little bit, for example, we will choose to define a `books` table which will be the core of the `bookshop` data. It contains fields for the book's id, title, type (e.g., Magazine, Novel, Life, Arts, etc.), stock, price, and publication date.

{{< copyable "sql" >}}

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

This table contains more data types than the `users` table.

- [int](https://docs.pingcap.com/tidb/stable/data-type-numeric#integer-types): We recommend using the right size type to aviod using too much hard disk or even affecting performance worse (too large a type range) or data overflow (too small a type range).
- [datetime](https://docs.pingcap.com/tidb/stable/data-type-date-and-time): The **datetime** type can be used to store time values.
- [enum](https://docs.pingcap.com/tidb/stable/data-type-string#enum-type): Enum type can be used to save a limited selection of values.

### Select primary key

[Primary key](https://docs.pingcap.com/tidb/stable/constraints#primary-key) is a column or group of columns, and this value, which is a combination of all **primary key columns**, is a unique identifier for a row of data.

> **注意：**
>
> TiDB 中，关于 **Primary Key** 的默认定义与 MySQL 常用存储引擎 [InnoDB](https://mariadb.com/kb/en/innodb/) 不一致。**InnoDB** 中，**Primary Key** 的语义为：唯一，不为空，**且为聚簇索引**。
>
> 而在 TiDB 中，**Primary Key** 的定义为：唯一，不为空。但主键不保证为**聚簇索引**。而是由另一组关键字 `CLUSTERED`、`NONCLUSTERED` 额外控制 **Primary Key** 是否为聚簇索引，若不指定，则由系统变量 `@@global.tidb_enable_clustered_index` 影响，具体说明请看[此文档](https://docs.pingcap.com/zh/tidb/stable/clustered-indexes)。

主键在 `CREATE TABLE` 语句中定义。[主键约束](https://docs.pingcap.com/zh/tidb/stable/constraints#%E4%B8%BB%E9%94%AE%E7%BA%A6%E6%9D%9F)要求所有受约束的列仅包含非 `NULL` 值。

一个表可以没有主键，主键也可以是非整数类型。但此时 TiDB 就会创建一个 `_tidb_rowid` 作为隐式主键。隐式主键 `_tidb_rowid` 因为其单调递增的特性，可能在大批量写入场景下会导致写入热点，如果你写入量密集，可考虑通过 [SHARD_ROW_ID_BITS](https://docs.pingcap.com/zh/tidb/stable/shard-row-id-bits) 和 [PRE_SPLIT_REGIONS](https://docs.pingcap.com/zh/tidb/stable/sql-statement-split-region#pre_split_regions) 两参数控制打散。但这可能导致读放大，请自行取舍。

表的主键为 [整数类型](https://docs.pingcap.com/zh/tidb/stable/data-type-numeric#%E6%95%B4%E6%95%B0%E7%B1%BB%E5%9E%8B) 且使用了 `AUTO_INCREMENT` 时，无法使用 `SHARD_ROW_ID_BITS` 消除热点。需解决此热点问题，且无需使用主键的连续和递增时，可使用 [AUTO_RANDOM](https://docs.pingcap.com/zh/tidb/stable/auto-random) 替换 `AUTO_INCREMENT` 属性来消除行 ID 的连续性。

更多有关热点问题的处理办法，请参考[TiDB 热点问题处理](https://docs.pingcap.com/zh/tidb/stable/troubleshoot-hot-spot-issues)。

#### Best Practices for select primary key

以下是在 TiDB 中选择主键列时需要遵循的一些最佳实践：

- 在表内定义一个主键或唯一索引。
- 尽量选择有意义的列作为主键。
- 出于为性能考虑，尽量避免存储超宽表，表字段数不建议超过 60 个，建议单行的总数据大小不要超过 64K，数据长度过大字段最好拆到另外的表。
- 不推荐使用复杂的数据类型。
- 需要 JOIN 的字段，数据类型保障绝对一致，避免隐式转换。
- 避免在单个单调数据列上定义主键。如果你使用单个单调数据列（例如：`AUTO_INCREMENT` 的列）来定义主键，有可能会对写性能产生负面影响。可能的话，使用 `AUTO_RANDOM` 替换 `AUTO_INCREMENT`（这会失去主键的连续和递增特性）。
- 如果你 **_必须_** 在单个单调数据列上创建索引，且有大量写入的话。请不要将这个单调数据列定义为主键，而是使用 `AUTO_RANDOM` 创建该表的主键，或使用 [SHARD_ROW_ID_BITS](https://docs.pingcap.com/zh/tidb/stable/shard-row-id-bits) 和 [PRE_SPLIT_REGIONS](https://docs.pingcap.com/zh/tidb/stable/sql-statement-split-region#pre_split_regions) 打散 `_tidb_rowid`。

#### Select primary key example

需遵循[主键选择的最佳实践](#主键选择的最佳实践)，我们展示在 `users` 表中定义 `AUTO_RANDOM` 主键的场景：

{{< copyable "sql" >}}

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM,
  `balance` decimal(15,2),
  `nickname` varchar(100),
  PRIMARY KEY (`id`)
);
```

### Clustered or not

[聚簇索引](https://docs.pingcap.com/zh/tidb/stable/clustered-indexes) (clustered index) 是 TiDB 从 v5.0 开始支持的特性，用于控制含有主键的表数据的存储方式。通过使用聚簇索引，TiDB 可以更好地组织数据表，从而提高某些查询的性能。有些数据库管理系统也将聚簇索引称为“索引组织表” (index-organized tables)。

目前 TiDB 中 **_含有主键_** 的表分为以下两类：

- `NONCLUSTERED`，表示该表的主键为非聚簇索引。在非聚簇索引表中，行数据的键由 TiDB 内部隐式分配的 `_tidb_rowid` 构成，而主键本质上是唯一索引，因此非聚簇索引表存储一行至少需要两个键值对，分别为：
    - `_tidb_rowid`（键）- 行数据（值）
    - 主键列数据（键） - `_tidb_rowid`（值）
- `CLUSTERED`，表示该表的主键为聚簇索引。在聚簇索引表中，行数据的键由用户给定的主键列数据构成，因此聚簇索引表存储一行至少只要一个键值对，即：
    - 主键列数据（键） - 行数据（值）

如[主键](#选择主键)中所述，聚簇索引在 TiDB 中，使用关键字 `CLUSTERED`、`NONCLUSTERED` 进行控制。

> **注意：**
>
> TiDB 仅支持根据表的主键来进行聚簇操作。聚簇索引启用时，“主键”和“聚簇索引”两个术语在一些情况下可互换使用。主键指的是约束（一种逻辑属性），而聚簇索引描述的是数据存储的物理实现。

#### Best Practices for select clustered index

以下是在 TiDB 中选择聚簇索引时需要遵循的一些最佳实践：

- 遵循 [主键选择的最佳实践](#主键选择的最佳实践)：

    聚簇索引将基于主键建立，请遵循主键选择的最佳实践，以完成聚簇索引最佳实践的基础。

- 在以下场景中，尽量使用聚簇索引，将带来性能和吞吐量的优势：

    - 插入数据时会减少一次从网络写入索引数据。
    - 等值条件查询仅涉及主键时会减少一次从网络读取数据。
    - 范围条件查询仅涉及主键时会减少多次从网络读取数据。
    - 等值或范围条件查询仅涉及主键的前缀时会减少多次从网络读取数据。

- 在以下场景中，尽量避免使用聚簇索引，将带来性能劣势：

    - 批量插入大量取值相邻的主键时，可能会产生较大的写热点问题，请遵循[主键选择的最佳实践](#主键选择的最佳实践)。
    - 当使用大于 64 位的数据类型作为主键时，可能导致表数据需要占用更多的存储空间。该现象在存在多个二级索引时尤为明显。

- 显式指定是否使用聚簇索引，而非使用系统变量 `@@global.tidb_enable_clustered_index` 及配置项 `alter-primary-key` 控制是否使用[聚簇索引的默认行为](https://docs.pingcap.com/zh/tidb/stable/clustered-indexes#%E5%88%9B%E5%BB%BA%E8%81%9A%E7%B0%87%E7%B4%A2%E5%BC%95%E8%A1%A8)。

#### Select clustered index example

需遵循[聚簇索引选择的最佳实践](#聚簇索引选择的最佳实践)，假设我们将需要建立一张 `books` 和 `users` 之间关联的表，代表用户对某书籍的评分。我们使用表名 `ratings` 来创建该表，并使用 `book_id` 和 `user_id` 构建[复合主键](https://docs.pingcap.com/zh/tidb/stable/constraints#%E4%B8%BB%E9%94%AE%E7%BA%A6%E6%9D%9F)，并在该主键上建立聚簇索引：

{{< copyable "sql" >}}

```sql
CREATE TABLE `bookshop`.`ratings` (
  `book_id` bigint,
  `user_id` bigint,
  `score` tinyint,
  `rated_at` datetime,
  PRIMARY KEY (`book_id`,`user_id`) CLUSTERED
);
```

### Add column constraints

除[主键约束](#选择主键)外，TiDB 还支持其他的列约束，如：[非空约束 `NOT NULL`](https://docs.pingcap.com/zh/tidb/stable/constraints#%E9%9D%9E%E7%A9%BA%E7%BA%A6%E6%9D%9F)、[唯一约束 `UNIQUE KEY`](https://docs.pingcap.com/zh/tidb/stable/constraints#%E5%94%AF%E4%B8%80%E7%BA%A6%E6%9D%9F)、默认值 `DEFAULT` 等。完整约束，请查看 [TiDB 约束](https://docs.pingcap.com/zh/tidb/stable/constraints)文档。

#### 填充默认值

如需在列上设置默认值，请使用 `DEFAULT` 约束。默认值将可以使你无需指定每一列的值，就可以插入数据。

你可以将 `DEFAULT` 与[支持的 SQL 函数](https://docs.pingcap.com/zh/tidb/stable/basic-features#%E6%95%B0%E6%8D%AE%E7%B1%BB%E5%9E%8B%E5%87%BD%E6%95%B0%E5%92%8C%E6%93%8D%E4%BD%9C%E7%AC%A6)结合使用，将默认值的计算移出应用层，从而节省应用层的资源（当然，计算所消耗的资源并不会凭空消失，只是被转移到了 TiDB 集群中）。常见的，我们想实现数据插入时，可默认填充默认的时间。还是使用 `rating` 作为示例，可使用以下语句：

{{< copyable "sql" >}}

```sql
CREATE TABLE `bookshop`.`ratings` (
  `book_id` bigint,
  `user_id` bigint,
  `score` tinyint,
  `rated_at` datetime DEFAULT NOW(),
  PRIMARY KEY (`book_id`,`user_id`) CLUSTERED
);
```

额外的，如果需更新时也默认填入当前时间，可使用以下语句（但 `ON UPDATE` 后仅可填入[当前时间相关语句](https://pingcap.github.io/sqlgram/#NowSymOptionFraction)，`DEFAULT` 后支持[更多选择](https://pingcap.github.io/sqlgram/#DefaultValueExpr)）：

{{< copyable "sql" >}}

```sql
CREATE TABLE `bookshop`.`ratings` (
  `book_id` bigint,
  `user_id` bigint,
  `score` tinyint,
  `rated_at` datetime DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`book_id`,`user_id`) CLUSTERED
);
```

#### 防止重复

如果你需要防止列中出现重复值，那你可以使用 `UNIQUE` 约束。

例如，你需要确保用户的昵称唯一，我们可以这样改写 `user` 表的创建 SQL：

{{< copyable "sql" >}}

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM,
  `balance` decimal(15,2),
  `nickname` varchar(100) UNIQUE,
  PRIMARY KEY (`id`)
);
```

如果你在 `user` 表中尝试插入相同的 `nickname`，将返回错误。

#### 防止空值

如果你需要防止列中出现空值，那就可以使用 `NOT NULL` 约束。

还是使用用户昵称来举例子，除了昵称唯一，我们还希望昵称不可为空，于是此处可以这样改写 `user` 表的创建 SQL：

{{< copyable "sql" >}}

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM,
  `balance` decimal(15,2),
  `nickname` varchar(100) UNIQUE NOT NULL,
  PRIMARY KEY (`id`)
);
```

### Using HTAP capabilities

> **注意：**
>
> 本指南中有关 HTAP 的步骤仅适用于快速上手体验，不适用于生产环境。如需探索 HTAP 更多功能，请参考[深入探索 HTAP](https://docs.pingcap.com/zh/tidb/stable/explore-htap)。

假设我们的 `bookshop` 应用程序，有对用户评价的 `ratings` 表进行 OLAP 分析查询的需求，例如需查询: **书籍的评分，是否和评价的时间具有显著的相关性** 的需求，用以分析用户的书籍评分是否客观。那么会要求我们查询整个 `ratings` 表中的 `score` 和 `rated_at` 字段。这对普通仅支持的 OLTP 的数据库来说，是一个非常消耗资源的操作。或者使用一些 ETL 或其他数据同步工具，将 OLTP 数据库中的数据，导出到专用的 OLAP 数据库，再进行分析。

这种场景下，TiDB 就是一个比较理想的一站式数据库解决方案，TiDB 是一个 **HTAP (Hybrid Transactional and Analytical Processing)** 数据库，同时支持 OLTP 和 OLAP 场景。

#### 同步列存数据

当前，TiDB 支持两种数据分析引擎：**TiFlash** 和 **TiSpark**。大数据场景 (100 T) 下，推荐使用 TiFlash MPP 作为 HTAP 的主要方案，TiSpark 作为补充方案。希望了解更多关于 TiDB 的 HTAP 能力，可参考以下文章：[快速上手 HTAP](https://docs.pingcap.com/zh/tidb/stable/quick-start-with-htap) 和 [深入探索 HTAP](https://docs.pingcap.com/zh/tidb/stable/explore-htap)。

我们此处选用 [TiFlash](https://docs.pingcap.com/zh/tidb/stable/tiflash-overview) 为 `bookshop` 数据库的数据分析引擎。

TiFlash 部署完成后并不会自动同步数据，而需要手动指定需要同步的表，开启同步副本仅需一行 SQL，如下所示：

{{< copyable "sql" >}}

```sql
ALTER TABLE {table_name} SET TIFLASH REPLICA {count};
```

|      Parameter      |                      Description                      |
| :------------: | :------------------------------------: |
| `{table_name}` |                  表名                  |
|   `{count}`    | 同步副本数，若为 0，则表示删除同步副本 |

随后，TiFlash 将同步该表，查询时，TiDB 将会自动基于成本优化，考虑使用 **TiKV (行存)** 或 **TiFlash (列存)** 进行数据查询。当然，除了自动的方法，你也可以直接指定查询是否使用 TiFlash 副本，使用方法可查看[使用 TiDB 读取 TiFlash](https://docs.pingcap.com/zh/tidb/stable/use-tiflash#%E4%BD%BF%E7%94%A8-tidb-%E8%AF%BB%E5%8F%96-tiflash) 文档。

#### 使用 HTAP 的示例

`ratings` 表开启 1 个 TiFlash 副本：

{{< copyable "sql" >}}

```sql
ALTER TABLE `bookshop`.`ratings` SET TIFLASH REPLICA 1;
```

> **注意：**
>
> 如果你的集群，不包含 TiFlash 节点，此 SQL 语句将会报错：`1105 - the tiflash replica count: 1 should be less than the total tiflash server count: 0` 你可以[使用 TiDB Cloud (DevTier) 构建 TiDB 集群](/develop/build-cluster-in-cloud.md#第-1-步创建免费集群) 来创建一个含有 TiFlash 的免费集群。

随后正常进行查询即可：

{{< copyable "sql" >}}

```sql
SELECT HOUR(`rated_at`), AVG(`score`) FROM `bookshop`.`ratings` GROUP BY HOUR(`rated_at`);
```

我们也可使用 [EXPLAIN ANALYZE](https://docs.pingcap.com/zh/tidb/stable/sql-statement-explain-analyze) 语句查看此语句是否使用了 TiFlash 引擎：

{{< copyable "sql" >}}

```sql
EXPLAIN ANALYZE SELECT HOUR(`rated_at`), AVG(`score`) FROM `bookshop`.`ratings` GROUP BY HOUR(`rated_at`);
```

运行结果为：

```
+-----------------------------+-----------+---------+--------------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------+----------+------+
| id                          | estRows   | actRows | task         | access object | execution info                                                                                                                                                                                                                                                                                                                                                       | operator info                                                                                                                                  | memory   | disk |
+-----------------------------+-----------+---------+--------------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------+----------+------+
| Projection_4                | 299821.99 | 24      | root         |               | time:60.8ms, loops:6, Concurrency:5                                                                                                                                                                                                                                                                                                                                  | hour(cast(bookshop.ratings.rated_at, time))->Column#6, Column#5                                                                                | 17.7 KB  | N/A  |
| └─HashAgg_5                 | 299821.99 | 24      | root         |               | time:60.7ms, loops:6, partial_worker:{wall_time:60.660079ms, concurrency:5, task_num:293, tot_wait:262.536669ms, tot_exec:40.171833ms, tot_time:302.827753ms, max:60.636886ms, p95:60.636886ms}, final_worker:{wall_time:60.701437ms, concurrency:5, task_num:25, tot_wait:303.114278ms, tot_exec:176.564µs, tot_time:303.297475ms, max:60.69326ms, p95:60.69326ms}  | group by:Column#10, funcs:avg(Column#8)->Column#5, funcs:firstrow(Column#9)->bookshop.ratings.rated_at                                         | 714.0 KB | N/A  |
|   └─Projection_15           | 300000.00 | 300000  | root         |               | time:58.5ms, loops:294, Concurrency:5                                                                                                                                                                                                                                                                                                                                | cast(bookshop.ratings.score, decimal(8,4) BINARY)->Column#8, bookshop.ratings.rated_at, hour(cast(bookshop.ratings.rated_at, time))->Column#10 | 366.2 KB | N/A  |
|     └─TableReader_10        | 300000.00 | 300000  | root         |               | time:43.5ms, loops:294, cop_task: {num: 1, max: 43.1ms, proc_keys: 0, rpc_num: 1, rpc_time: 43ms, copr_cache_hit_ratio: 0.00}                                                                                                                                                                                                                                        | data:TableFullScan_9                                                                                                                           | 4.58 MB  | N/A  |
|       └─TableFullScan_9     | 300000.00 | 300000  | cop[tiflash] | table:ratings | tiflash_task:{time:5.98ms, loops:8, threads:1}                                                                                                                                                                                                                                                                                                                       | keep order:false                                                                                                                               | N/A      | N/A  |
+-----------------------------+-----------+---------+--------------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------+----------+------+
```

在出现 `cop[tiflash]` 字样时，表示该任务发送至 TiFlash 进行处理。

### Execute the `CREATE TABLE` statement

我们定义完毕 `CREATE TABLE` 后，可以进行执行。

#### Best Practices for execute the `CREATE TABLE` statement

执行 `CREATE TABLE` 时需要遵循的一些最佳实践：

- 我们不推荐使用客户端的 Driver 或 ORM 来执行数据库模式的更改。以经验来看，作为最佳实践，我们建议使用 [MySQL 客户端](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)或使用任意你喜欢的 GUI 客户端来进行数据库模式的更改。本文档中，我们将在大多数场景下，使用 **MySQL 客户端** 传入 SQL 文件来执行数据库模式的更改。
- 遵循 SQL 开发规范中的[建表删表规范](/develop/sql-development-specification.md#建表删表规范)，建议业务应用内部封装建表删表语句增加判断逻辑。

#### Execute the `CREATE TABLE` statement example

按以上步骤创建所有表后，我们的 `dbinit.sql` 文件应该类似于[数据库初始化](/develop/bookshop-schema-design.md#数据库初始化-dbinitsql-脚本)所示。若需查看表信息详解，请参阅[数据表详解](/develop/bookshop-schema-design.md#数据表详解)。

我们可使用以下语句来执行 `dbinit.sql` 文件：

{{< copyable "shell-regular" >}}

```shell
mysql
    -u root \
    -h {host} \
    -P {port} \
    -p {password} \
    < dbinit.sql
```

需查看 `bookshop` 数据库下的所有表，可使用 [SHOW TABLES](https://docs.pingcap.com/zh/tidb/stable/sql-statement-show-tables#show-full-tables) 语句：

{{< copyable "sql" >}}

```sql
SHOW TABLES IN `bookshop`;
```

运行结果为：

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

请注意，到目前为止，我们所创建的所有表都不包含二级索引。添加二级索引的指南，请参考[创建二级索引](/develop/create-secondary-indexes.md)。
