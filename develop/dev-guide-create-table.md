---
title: Create a Table
summary: The ways, best practices, and examples for creating tables.
---

# Create a Table

This page provides a best practice guide for creating tables and an example of a [bookshop](/develop/dev-guide-bookshop-schema-design.md) database based on TiDB.

> **Note:**
>
> Detailed reference documentation for this `CREATE TABLE` statement, including additional examples, can be found in the [CREATE TABLE](https://docs.pingcap.com/zh/tidb/stable/sql-statement-create-table) documentation.

## Before you start

Before reading this page, you need to prepare the following:

- [Build a TiDB Cluster in TiDB Cloud(DevTier)](/develop/dev-guide-build-cluster-in-cloud.md).
- Read [Schema Design Overview](/develop/dev-guide-schema-design-overview.md).
- [Create a Database](/develop/dev-guide-create-database.md).

## How to create a table

[Table](/develop/dev-guide-schema-design-overview.md#table) is a logical object. It would stores data sent from the persistence layer of an application or from other SQL. Tables saved data records in the form of rows and columns.

To create a table, use the [CREATE TABLE](/common/sql-statements/sql-statement-create-table.md) statement and follow the best practices:

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
- Use meaningful table names, for example, if you need to create a user table, you can use names: `user`, `t_user`, `users`, etc., or follow your company or organization's naming convention. If your company or organization does not have a naming convention, you can refer to the [table naming convention](/develop/dev-guide-object-naming-guidelines.md#table-naming-convention). Do not use such table names as: `t1`, `table1`, etc.
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
|      `{data_type}`       | Column [data type](/basic-features.md#data-types-functions-and-operators) |
| `{column_qualification}` | Column qualifications, such as **column-level constraints** or [generated column (experimental function)](/generated-columns.md) clauses |

#### Best Practices for defining columns

There are some best practices to follow when defining columns:

- Check the [data types](/basic-features.md#data-types-functions-and-operators) of the supporting columns and organize your data according to the data type restrictions. Select the appropriate type for the data you plan to be present in the column.
- Check the [best practices](#best-practices-for-select-primary-key) and [examples](#select-primary-key-example) for selecting primary keys and decide whether to use primary key columns.
- Check [best practices](#best-practices-for-select-clustered-index) and [examples](#select-clustered-index-example) for selecting clustered indexes and decide whether to specify **clustered indexes**.
- Check [adding column constraints](#add-column-constraints) and decide whether to add constraints to the columns.
- Please use meaningful column names. we recommend that you follow your company or organization's table naming convention. If your company or organization does not have a corresponding naming convention, refer to the [column naming convention](/develop/dev-guide-object-naming-guidelines.md#field-naming-convention).

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

In this case, we define a field with the name `id` and the type [bigint](/data-type-numeric.md#bigint-type). This is used to represent a unique user identifier. This means that all user identifiers should be of type `bigint`.

After that, we define a field named `nickname`, of type [varchar](/data-type-string.md#varchar-type), and not longer than 100 characters. This means that the `nicknames` of the users used `varchar` type and were not longer than `100` characters.

Finally, we added a field named `balance`, type is [decimal](/data-type-numeric.md#decimal-type), with a **precision** of `15` and a **scale** of `2`. To briefly explain the meaning of **precision** and **scale**, **precision** represents the total number of digits in the field, and **scale** represents the number of decimal places. For example: `decimal(5,2)`, i.e., with a precision of `5` and a scale of `2`, the range is `-999.99` to `999.99`. `decimal(6,1)`, i.e., with a precision of `6` and a scale of `1`, the range is `-99999.9` to `99999.9`. **decimal** is a [fixed-point types](/data-type-numeric.md#fixed-point-types), which can be used to store numbers accurately, in scenarios where accurate numbers are needed (e.g., user property-related), please **make sure** to use the **decimal** type.

TiDB supports many other column data types, including [Integer types](/data-type-numeric.md#integer-types), [Floating-point types](/data-type-numeric.md#floating-point-types), [Fixed-point types](/data-type-numeric.md#fixed-point-types), [Date and time types](/data-type-date-and-time.md), [Enum type](/data-type-string.md#enum-type), etc. You can refer to the supported column [data types](/basic-features.md#data-types-functions-and-operators) and use the **data types** that match the data you want to save in the database.

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

- [int](/data-type-numeric.md#integer-types): We recommend using the right size type to aviod using too much hard disk or even affecting performance worse (too large a type range) or data overflow (too small a type range).
- [datetime](/data-type-date-and-time.md): The **datetime** type can be used to store time values.
- [enum](/data-type-string.md#enum-type): Enum type can be used to save a limited selection of values.

### Select primary key

[Primary key](/constraints.md#primary-key) is a column or group of columns, and this value, which is a combination of all **primary key columns**, is a unique identifier for a row of data.

> **Note:**
>
> In TiDB, the default definition of **Primary Key** is different from [InnoDB](https://mariadb.com/kb/en/innodb/)(the common storage engine of MySQL). In **InnoDB**, The semantics of **Primary Key** is unique, not null, and **index clustered**.
>
> However, in TiDB, the definition of **Primary Key** is: unique, not null. But the primary key is not guaranteed to be a **clustered index**. Instead, another set of keywords `CLUSTERED` / `NONCLUSTERED` additionally controls whether the **Primary Key** is a **Clustered Index**, and if not specified, is affected by the system variable `@@global.tidb_enable_clustered_index`, as described in [this document](https://docs.pingcap.com/zh/tidb/stable/clustered-indexes).

The **primary key** is defined in the `CREATE TABLE` statement. The [primary key constraint](/constraints.md#primary-key) requires that all constrained columns contain only non-NULL values.

A table can create without **primary key**, and the **primary key** can be a non-integer type. But then TiDB creates an `_tidb_rowid` as an **implicit primary key**. The implicit primary key `_tidb_rowid`, because of its monotonically increasing nature, may cause write hotspots in write-intensive scenarios. So if your application is write-intensive, consider sharding with the [SHARD_ROW_ID_BITS](https://docs.pingcap.com/zh/tidb/stable/shard-row-id-bits) and [PRE_SPLIT_REGIONS](/common/sql-statements/sql-statement-split-region.md#pre_split_regions) parameters. However, this may lead to read amplification, so please make your own trade-off.

When the **primary key** of a table is [integer types](/data-type-numeric.md#integer-types) and `AUTO_INCREMENT` is used, hotspots cannot avoid by using `SHARD_ROW_ID_BITS`. If you need to avoid hotspots and do not need to use the primary key continuous and incremental, you can use [AUTO_RANDOM](/auto-random.md) instead of `AUTO_INCREMENT` to eliminate row ID continuous.

For more information on how to handle hotspot issues, please refer to [Troubleshoot Hotspot Issues](/troubleshoot-hot-spot-issues.md).

#### Best Practices for select primary key

There are some best practices to follow when selecting primary key columns in TiDB:

- Define a **primary key** or **unique index** within the table.
- Try to select meaningful **columns** as **primary keys**.
- For performance reasons, try to avoid storing extra-wide tables, the number of table fields is not recommended to over `60`, the total data size of a single row is not recommended to over `64K`, and fields with too much data length are best split to another table.
- It is not recommended to use complex data types.
- The fields need to **JOIN** , ensure data types absolute consistency, to avoid implicit conversion.
- Avoid defining **primary keys** on a single monotonic data column. If you use a single monotonic data column (e.g., a column of `AUTO_INCREMENT`) to define the **primary key**, there is a risk of a negative impact on write performance. If possible, use `AUTO_RANDOM` instead of `AUTO_INCREMENT` (this loses the continuous and incremental nature of the primary key).
- If you **_must_** create an index on a single monotonic data column at write-intensive scenarios. Instead of defining this monotonic data column as the **primary key**. You can use `AUTO_RANDOM` to create the **primary key** for that table, or use [SHARD_ROW_ID_BITS](/shard-row-id-bits.md) and [PRE_SPLIT_REGIONS](/common/sql-statements/sql-statement-split-region.md#pre_split_regions) to shard `_tidb_rowid`.

#### Select primary key example

Following the [Best Practices for select primary key](#best-practices-for-select-primary-key), we show a scenario where the `AUTO_RANDOM` primary key is defined in the `users` table.

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

TiDB supports the [clustered index](/clustered-indexes.md) feature since v5.0. This feature controls how data is stored in tables containing primary keys. It provides TiDB the ability to organize tables in a way that can improve the performance of certain queries.

The term clustered in this context refers to the organization of how data is stored and not a group of database servers working together. Some database management systems refer to clustered indexes as index-organized tables (IOT).

Currently, tables **_containing primary_** keys in TiDB are divided into the following two categories:

- `NONCLUSTERED`: The primary key of the table is non-clustered index. In tables with non-clustered indexes, the keys for row data consist of internal `_tidb_rowid` implicitly assigned by TiDB. Because primary keys are essentially unique indexes, tables with non-clustered indexes need at least two key-value pairs to store a row, which are:
    - `_tidb_rowid` (key) - row data (value)
    - Primary key data (key) - `_tidb_rowid` (value)
- `CLUSTERED`: The primary key of the table is clustered index. In tables with clustered indexes, the keys for row data consist of primary key data given by the user. Therefore, tables with clustered indexes need only one key-value pair to store a row, which is:
    - Primary key data (key) - row data (value)

As described in [select primary key](#select-primary-key), **clustered indexes** are controlled in TiDB using the keywords `CLUSTERED`, `NONCLUSTERED`.

> **Note:**
>
> TiDB supports clustering only by a table's `PRIMARY KEY`. With clustered indexes enabled, the terms _the_ `PRIMARY KEY` and _the clustered index_ might be used interchangeably. `PRIMARY KEY` refers to the constraint (a logical property), and clustered index describes the physical implementation of how the data is stored.

#### Best Practices for select clustered index

The following are some best practices to follow when selecting **clustered indexes** in TiDB.

- Follow the [best practices for select primary key](#best-practices-for-select-primary-key), **Clustered indexes** will be built based on **primary keys**.
- Compared to tables with non-clustered indexes, tables with clustered indexes offer greater performance and throughput advantages in the following scenarios:
    - When data is inserted, the clustered index reduces one write of the index data from the network.
    - When a query with an equivalent condition only involves the primary key, the clustered index reduces one read of index data from the network.
    - When a query with a range condition only involves the primary key, the clustered index reduces multiple reads of index data from the network.
    - When a query with an equivalent or range condition only involves the primary key prefix, the clustered index reduces multiple reads of index data from the network.
- On the other hand, tables with clustered indexes have certain disadvantages. See the following:
    - There might be write hotspot issues when inserting a large number of primary keys with close values, please follow the [best practices for select primary key](#best-practices-for-select-primary-key).
    - The table data takes up more storage space if the data type of the primary key is larger than 64 bits, especially when there are multiple secondary indexes.

- Explicitly specifying whether to use clustered indexes instead of using the system variable `@@global.tidb_enable_clustered_index` and the configuration `alter-primary-key` control the [default behavior of whether to use clustered indexes](/clustered-indexes.md#create-a-table-with-clustered-indexes).

#### Select clustered index example

Following the [best practices for select clustered index](#best-practices-for-select-clustered-index), suppose we will need to create a table with an association between `books` and `users`, representing the `ratings` of a `book` by `users`. We create the table and construct a composite primary key using `book_id` and `user_id` and create a **clustered index** on that **primary key**.

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

In addition to [primary key constraints](#select-primary-key), TiDB also supports other **column constraints** such as [NOT NULL](/constraints.md#not-null) constraint, [UNIQUE KEY](/constraints.md#unique-key) constraint, `DEFAULT`, etc. For complete constraints, please check TiDB [Constraints](/constraints.md) documentation.

#### Default value

To set a default value on a column, use the `DEFAULT` constraint. The default value will allow you to insert data without specifying a value for each column.

You can use `DEFAULT` together with [supported SQL functions](/basic-features.md#data-types-functions-and-operators) to move the calculation of defaults out of the application layer, thus saving application layer resources (of course, the resources consumed by the calculation don't just disappear into thin air, they are just moved to the TiDB cluster). Commonly, we want to implement data insertion with the default time populated by default. Again using `rating` as an example, the following statement can be used:

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

In addition, if the current time is also filled in by default when updating, the following statements can be used (but only the [current time related statements](https://pingcap.github.io/sqlgram/#NowSymOptionFraction) can be filled in after `ON UPDATE`, [more options](https://pingcap.github.io/sqlgram/#DefaultValueExpr) are supported after `DEFAULT`):

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

#### Prevent duplicate values

If you need to prevent duplicate values in a column, you can use the `UNIQUE` constraint.

For example, you need to make sure that the `nickname` of `users` is unique. We can override the creation SQL of the user table like this:

{{< copyable "sql" >}}

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM,
  `balance` decimal(15,2),
  `nickname` varchar(100) UNIQUE,
  PRIMARY KEY (`id`)
);
```

If you try to insert the same `nickname` in the `users` table, an error will be return.

#### Prevents null values

If you need to prevent null values in columns, then you can use the `NOT NULL` constraint.

Using the user nickname example again, in addition to the nickname being unique, we also want the nickname to be non-null, so here we can rewrite the `users` table creation SQL like this.

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

> **Note:**
>
> The steps provided in this guide is **_ONLY_** for quick start in the test environment. For production environments, [explore HTAP](/explore-htap.md) is recommended.

Suppose our `bookshop` application has a requirement to perform OLAP analysis on the `ratings` table of user ratings, for example, we need to query: **whether the rating of a book has a significant correlation with the time of the rating**, in order to analyze whether the user's rating of the book is objective or not. Then we are asked to query the `score` and `rated_at` fields of the entire `ratings` table. This is a very resource-intensive operation for a normal OLTP-only database. Or we can use some ETL or other data synchronization tools to export the data from OLTP database to a dedicated OLAP database for analysis.

In this scenario, TiDB is an ideal one-stop database solution. TiDB is a **HTAP (Hybrid Transactional and Analytical Processing)** database that supports both OLTP and OLAP scenarios.

#### Synchronized column-oriented data

Currently, TiDB supports two data analysis engines, **TiFlash** and **TiSpark**, and for large data scenarios (100 T), **TiFlash MPP** is recommended as the primary solution for HTAP, and **TiSpark** as a complementary solution. To learn more about TiDB HTAP capabilities, please refer to the following articles: [Quick Start Guide for TiDB HTAP](/quick-start-with-htap.md) and [Explore HTAP](/explore-htap.md).

We have chosen [TiFlash](https://docs.pingcap.com/zh/tidb/stable/tiflash-overview) as the data analysis engine for our `bookshop` database.

TiFlash does not automatically synchronize data after deployment, but you need to manually specify the tables that need to be synchronized:

{{< copyable "sql" >}}

```sql
ALTER TABLE {table_name} SET TIFLASH REPLICA {count};
```

|      Parameter      |                      Description                      |
| :------------: | :------------------------------------: |
| `{table_name}` |                  Table name                  |
|   `{count}`    | The number of synchronized copies, if 0, the synchronized copies are deleted |

**TiFlash** will then synchronize the table, and when queried, TiDB will automatically consider using TiKV (row-oriented) or TiFlash (column-oriented) for data queries based on cost optimization. Of course, in addition to the automatic approach, you can also directly specify whether the query uses a **TiFlash** copy, see [Use TiDB to read TiFlash replicas](/tiflash/use-tiflash.md#use-tidb-to-read-tiflash-replicas) for how to use it.

#### Using HTAP capabilities example

The `ratings` table opens `1` copy of TiFlash:

{{< copyable "sql" >}}

```sql
ALTER TABLE `bookshop`.`ratings` SET TIFLASH REPLICA 1;
```

> **Note:**
>
> If your cluster, does not contain **TiFlash** nodes, this SQL statement will report an error: `1105 - the tiflash replica count: 1 should be less than the total tiflash server count: 0` You can use [Build a TiDB Cluster in TiDB Cloud (DevTier)](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-free-cluster) to create a free cluster include **TiFlash**.

Subsequent queries can be carried out normally.

{{< copyable "sql" >}}

```sql
SELECT HOUR(`rated_at`), AVG(`score`) FROM `bookshop`.`ratings` GROUP BY HOUR(`rated_at`);
```

We can also use the [EXPLAIN ANALYZE](/common/sql-statements/sql-statement-explain-analyze.md) statement to see if this statement is using the **TiFlash** here:

{{< copyable "sql" >}}

```sql
EXPLAIN ANALYZE SELECT HOUR(`rated_at`), AVG(`score`) FROM `bookshop`.`ratings` GROUP BY HOUR(`rated_at`);
```

Running results:

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

When the word `cop[tiflash]` appears, it means that the task is sent to **TiFlash** for processing.

### Execute the `CREATE TABLE` statement

Once we have defined `CREATE TABLE`, we can execute it.

#### Best Practices for execute the `CREATE TABLE` statement

Some best practices to follow when executing `CREATE TABLE`：

- We do not recommend using a client-side Driver or ORM to perform database schema changes. As a best practice from experience, we recommend using a [MySQL client](https://dev.mysql.com/doc/refman/8.0/en/mysql.html) or using any GUI client you like to perform database schema changes. In this document, we will use the **MySQL client** to pass in SQL files to perform database schema changes in most scenarios.
- Following the SQL development [specification for table build and delete](/develop/dev-guide-sql-development-specification.md#specification-for-table-build-and-delete), it is recommended to wrap the build and delete statements inside the business application to add judgment logic.

#### Execute the `CREATE TABLE` statement example

After creating all the tables as above rules, our `dbinit.sql` file should look similar to the [database initialization](/develop/dev-guide-bookshop-schema-design.md#database-initialization-script-dbinitsql) shown. If you need to see the table information in detail, please refer to [Details about Table](/develop/dev-guide-bookshop-schema-design.md#details-about-table).

We can execute the dbinit.sql file with the following statements:

{{< copyable "shell-regular" >}}

```shell
mysql
    -u root \
    -h {host} \
    -P {port} \
    -p {password} \
    < dbinit.sql
```

To view all tables under the `bookshop` database, use the [SHOW TABLES](/common/sql-statements/sql-statement-show-tables.md#show-full-tables) statement.

{{< copyable "sql" >}}

```sql
SHOW TABLES IN `bookshop`;
```

Running results:

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

Please note that all the tables we have created so far do not contain secondary indexes. For a guide to adding secondary indexes, please refer to [Creating Secondary Indexes](/develop/dev-guide-create-secondary-indexes.md).
