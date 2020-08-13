---
title: Compatibility with MySQL
summary: Learn about the compatibility of TiDB with MySQL, and the unsupported and different features.
aliases: ['/docs/v3.1/mysql-compatibility/','/docs/v3.1/reference/mysql-compatibility/']
---

# Compatibility with MySQL

TiDB supports both the MySQL wire protocol and the majority of its syntax. This means that you can use your existing MySQL connectors and clients, and your existing applications can often be migrated to TiDB without changing any application code.

Currently TiDB Server advertises itself as MySQL 5.7 and works with most MySQL database tools such as PHPMyAdmin, Navicat, MySQL Workbench, mysqldump, and Mydumper/myloader.

However, some features of MySQL are not supported. This could be because there is now a better way to solve the problem (such as XML functions superceded by JSON), or a lack of current demand versus effort required (such as stored procedures and functions). Some features might also be difficult to implement as a distributed system.

> **Note:**
>
> This page refers to general differences between MySQL and TiDB. Refer to the dedicated pages for [Security](/security-compatibility-with-mysql.md) and [Pessimistic Transaction Model](/pessimistic-transaction.md#difference-with-mysql-innodb) compatibility.

## Unsupported features

+ Stored procedures and functions
+ Triggers
+ Events
+ User-defined functions
+ `FOREIGN KEY` constraints
+ `FULLTEXT`/`SPATIAL` functions and indexes
+ Character sets other than `utf8`, `utf8mb4`, `ascii`, `latin1` and `binary`
+ Collations other than `BINARY`
+ Add/drop primary key
+ SYS schema
+ Optimizer trace
+ XML Functions
+ X-Protocol
+ Savepoints
+ Column-level privileges
+ `XA` syntax (TiDB uses a two-phase commit internally, but this is not exposed via an SQL interface)
+ `CREATE TABLE tblName AS SELECT stmt` syntax
+ `CREATE TEMPORARY TABLE` syntax
+ `CHECK TABLE` syntax
+ `CHECKSUM TABLE` syntax
+ `SELECT INTO FILE` syntax
+ `GET_LOCK` and `RELEASE_LOCK` functions

## Features that are different from MySQL

### Auto-increment ID

In TiDB, auto-increment columns are only guaranteed to be unique and incremental on a single TiDB server, but they are *not* guaranteed to be incremental among multiple TiDB servers or allocated sequentially. Currently, TiDB allocates IDs in batches. If you insert data on multiple TiDB servers at the same time, the allocated IDs are not continuous. You can use the `tidb_allow_remove_auto_inc` system variable to enable or disable deleting the `AUTO_INCREMENT` attribute of a column. The syntax for deleting this column attribute is `alter table modify` or `alter table change`.

> **Note:**
>
> If you use auto-increment IDs in a cluster with multiple tidb-server instances, do not mix default values and custom values. Otherwise, an error might occur in the following situation.

Assume that you have a table with the auto-increment ID:

{{< copyable "sql" >}}

```sql
CREATE TABLE t(id int unique key AUTO_INCREMENT, c int);
```

The principle of the auto-increment ID in TiDB is that each tidb-server instance caches a section of ID values (currently 30000 IDs are cached) for allocation and fetches the next section after this section is used up.

Assume that the cluster contains two tidb-server instances, namely Instance A and Instance B. Instance A caches the auto-increment ID of [1, 30000], while Instance B caches the auto-increment ID of [30001, 60000].

The operations are executed as follows:

1. The client issues the `INSERT INTO t VALUES (1, 1)` statement to Instance B which sets the `id` to 1 and the statement is executed successfully.
2. The client issues the `INSERT INTO t (c) (1)` statement to Instance A. This statement does not specify the value of `id`, so Instance A allocates the value. Currently, Instances A caches the auto-increment ID of [1, 30000], so it allocates the `id` value to 1 and adds 1 to the local counter. However, at this time the data with the `id` of 1 already exists in the cluster, therefore it reports `Duplicated Error`.

Also, starting with TiDB 3.0.4, TiDB supports using the system variable `tidb_allow_remove_auto_inc` to control whether the `AUTO_INCREMENT` property of a column is allowed to be removed by executing  `ALTER TABLE MODIFY` or `ALTER TABLE CHANGE` statements. It is not allowed by default.

> **Note:**
>
> If the primary key is not specified, TiDB uses the `_tibd_rowid` column to identify rows. The values of the `_tibd_rowid` column and the auto-increment column (if there is) are assigned by the same allocator. If the auto-increment column is specified as the primary key, then TiDB uses this column to identify rows. Therefore, there might be the following situations.

```sql
mysql> create table t(id int unique key AUTO_INCREMENT);
Query OK, 0 rows affected (0.05 sec)

mysql> insert into t values(),(),();
Query OK, 3 rows affected (0.00 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql> select _tidb_rowid, id from t;
+-------------+------+
| _tidb_rowid | id   |
+-------------+------+
|           4 |    1 |
|           5 |    2 |
|           6 |    3 |
+-------------+------+
3 rows in set (0.01 sec)
```

In early versions, the cache size of auto-increment IDs in TiDB is transparent to users. Since v3.0.14, v3.1.2, and v4.0.rc-2, the `AUTO_ID_CACHE` table option has been introduced to allow users to customize the cache size of auto-increment IDs to be allocated. This cache size might be consumed by both auto-increment columns and `_tidb_rowid`. In addition, if the length of continuous IDs needed for an `INSERT` statement exceeds the value set by `AUTO_ID_CACHE`, TiDB will properly increase the cache size so that this insertion can be executed successfully.

### Performance schema

Performance schema tables return empty results in TiDB. TiDB uses a combination of [Prometheus and Grafana](/monitor-a-tidb-cluster.md) for performance metrics instead.

TiDB supports the `events_statements_summary_by_digest` table from TiDB 3.0.4. For more information, see [Statement Summary Table](/statement-summary-tables.md).

### Query Execution Plan

The output format of Query Execution Plan (`EXPLAIN`/`EXPLAIN FOR`) in TiDB is greatly different from that in MySQL. Besides, the output content and the privileges setting of `EXPLAIN FOR` are not the same as those of MySQL. See [Understand the Query Execution Plan](/query-execution-plan.md) for more details.

### Built-in functions

TiDB supports most of the MySQL built-in functions, but not all. See [TiDB SQL Grammar](https://pingcap.github.io/sqlgram/#functioncallkeyword) for the supported functions.

### DDL

In TiDB DDL does not block reads or writes to tables while in operation. However, some restrictions currently apply to DDL changes:

+ Add Index:
    - Does not support creating multiple indexes at the same time.
    - Does not support the `VISIBLE/INVISIBLE` index.
    - Adding an index on a generated column via `ALTER TABLE` is not supported.
    - Other Index Type (HASH/BTREE/RTREE) is supported in syntax, but not applicable.
+ Add Column:
    - Does not support creating multiple columns at the same time.
    - Does not support setting a column as the `PRIMARY KEY`, or creating a unique index, or specifying `AUTO_INCREMENT` while adding it.
+ Drop Column: Does not support dropping the `PRIMARY KEY` column or index column.
+ Change/Modify Column:
    - Does not support lossy changes, such as from `BIGINT` to `INTEGER` or `VARCHAR(255)` to `VARCHAR(10)`.
    - Does not support modifying the precision of `DECIMAL` data types.
    - Does not support changing the `UNSIGNED` attribute.
    - Only supports changing the `CHARACTER SET` attribute from `utf8` to `utf8mb4`.
+ `LOCK [=] {DEFAULT|NONE|SHARED|EXCLUSIVE}`: the syntax is supported, but is not applicable to TiDB. All DDL changes that are supported do not lock the table.
+ `ALGORITHM [=] {DEFAULT|INSTANT|INPLACE|COPY}`: the syntax for `ALGORITHM=INSTANT` and `ALGORITHM=INPLACE` is fully supported, but it works differently from MySQL because some operations that are `INPLACE` in MySQL are `INSTANT` in TiDB. The syntax `ALGORITHM=COPY` is not applicable to TIDB and returns a warning.
+ Multiple operations cannot be completed in a single `ALTER TABLE` statement. For example, it's not possible to add multiple columns or indexes in a single statement.

+ The following Table Options are not supported in syntax:
    - `WITH/WITHOUT VALIDATION`
    - `SECONDARY_LOAD/SECONDARY_UNLOAD`
    - `CHECK/DROP CHECK`
    - `STATS_AUTO_RECALC/STATS_SAMPLE_PAGES`
    - `SECONDARY_ENGINE`
    - `ENCRYPTION`

+ The following Table Partition syntaxes are not supported:
    - `PARTITION BY LIST`
    - `PARTITION BY KEY`
    - `SUBPARTITION`
    - `{CHECK|EXCHANGE|TRUNCATE|OPTIMIZE|REPAIR|IMPORT|DISCARD|REBUILD|REORGANIZE} PARTITION`

For more information, see [Online Schema Changes](/key-features.md#online-schema-changes).

### Analyze table

[`ANALYZE TABLE`](/statistics.md#manual-collection) works differently in TiDB than in MySQL, in that it is a relatively lightweight and short-lived operation in MySQL/InnoDB, while in TiDB it completely rebuilds the statistics for a table and can take much longer to complete.

### Views

Views in TiDB are currently non-insertable and non-updatable.

### Storage engines

For compatibility reasons, TiDB supports the syntax to create tables with alternative storage engines. Metadata commands describe tables as being of engine InnoDB:

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (a INT) ENGINE=MyISAM;
```

```
Query OK, 0 rows affected (0.14 sec)
```

{{< copyable "sql" >}}

```sql
SHOW CREATE TABLE t1;
```

```
*************************** 1. row ***************************
       Table: t1
Create Table: CREATE TABLE `t1` (
  `a` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
1 row in set (0.00 sec)
```

Architecturally, TiDB does support a similar storage engine abstraction to MySQL, and user tables are created in the engine specified by the [`--store`](/command-line-flags-for-tidb-configuration.md#--store) option used when you start tidb-server (typically `tikv`).

### SQL modes

TiDB supports most [SQL modes](/sql-mode.md):

- The compatibility modes, such as `ORACLE` and `POSTGRESQL` are parsed but ignored. Compatibility modes are deprecated in MySQL 5.7 and removed in MySQL 8.0.
- The `ONLY_FULL_GROUP_BY` mode has minor [semantic differences](/functions-and-operators/aggregate-group-by-functions.md#differences-from-mysql) from MySQL 5.7.
- The `NO_DIR_IN_CREATE` and `NO_ENGINE_SUBSTITUTION` SQL modes in MySQL are accepted for compatibility, but are not applicable to TiDB.

### Version-specific comments

TiDB executes all MySQL version-specific comments, regardless of the version they apply to. For example, the comment `/*!90000 */` would instruct a MySQL server less than 9.0 to not execute code. In TiDB this code will always be executed:

```sql
mysql 8.0.16> SELECT /*!90000 "I should not run", */ "I should run" FROM dual;
+--------------+
| I should run |
+--------------+
| I should run |
+--------------+
1 row in set (0.00 sec)

tidb> SELECT /*!90000 "I should not run", */ "I should run" FROM dual;
+------------------+--------------+
| I should not run | I should run |
+------------------+--------------+
| I should not run | I should run |
+------------------+--------------+
1 row in set (0.00 sec)
```

### Default differences

- Default character set:
    - The default value in TiDB is `utf8mb4`.
    - The default value in MySQL 5.7 is `latin1`, but changes to `utf8mb4` in MySQL 8.0.
- Default collation:
    - The default collation of `utf8mb4` in TiDB is `utf8mb4_bin`.
    - The default collation of `utf8mb4` in MySQL 5.7 is `utf8mb4_general_ci`, but changes to `utf8mb4_0900_ai_ci` in MySQL 8.0.
    - You can use the [`SHOW CHARACTER SET`](/sql-statements/sql-statement-show-character-set.md) statement to check the default collations of all character sets.
- Default value of `foreign_key_checks`:
    - The default value in TiDB is `OFF` and currently TiDB only supports `OFF`.
    - The default value in MySQL 5.7 is `ON`.
- Default SQL mode:
    - The default SQL mode in TiDB includes these modes: `ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION`.
    - The default SQL mode in MySQL:
        - The default SQL mode in MySQL 5.7 is the same as TiDB.
        - The default SQL mode in MySQL 8.0 includes these modes: `ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION`.
- Default value of `lower_case_table_names`:
    - The default value in TiDB is 2 and currently TiDB only supports 2.
    - The default value in MySQL:
        - On Linux: 0
        - On Windows: 1
        - On macOS: 2
- Default value of `explicit_defaults_for_timestamp`:
    - The default value in TiDB is `ON` and currently TiDB only supports `ON`.
    - The default value in MySQL:
        - For MySQL 5.7: `OFF`
        - For MySQL 8.0: `ON`

### Date and Time

#### Named timezone

TiDB supports named timezones such as `America/Los_Angeles` without having to load the [time zone information tables](https://dev.mysql.com/doc/refman/8.0/en/time-zone-support.html#time-zone-installation) as in MySQL.

Because they are built-in, named time zones in TiDB might behave slightly differently to MySQL, and cannot be modified. For example, in TiDB the names are case-sensitive [#8087](https://github.com/pingcap/tidb/issues/8087).

> **Note:**
>
> TiKV calculates time-related expressions that can be pushed down to it. This calculation uses the built-in time zone rule and does not depend on the time zone rule installed in the system. If the time zone rule installed in the system does not match the version of the built-in time zone rule in TiKV, the time data that can be inserted might result in a statement error in a few cases.
>
> For example, if the tzdata 2018a time zone rule is installed in the system, the time `1988-04-17 02:00:00` can be inserted into TiDB of the 3.0.0-rc.1 version when the time zone is set to Asia/Shanghai or the time zone is set to the local time zone and the local time zone is Asia/Shanghai. But reading this record might result in a statement error because this time does not exist in the Asia/Shanghai time zone according to the tzdata 2018i time zone rule used by TiKV 3.0.0-rc.1. Daylight saving time is one hour late.
>
> The named timezone rules in TiKV of two versions are as follows:
>
> - 3.0.0 RC.1 and later: [tzdata 2018i](https://github.com/eggert/tz/tree/2018i)
> - 2.1.0 RC.1 and later: [tzdata 2018e](https://github.com/eggert/tz/tree/2018e)

#### Zero month and zero day

It is not recommended to unset the `NO_ZERO_DATE` and `NO_ZERO_IN_DATE` SQL modes, which are enabled by default in TiDB as in MySQL. While TiDB supports operating with these modes disabled, the TiKV coprocessor does not. Executing certain statements that push down date and time processing functions to TiKV might result in a statement error.

#### Handling of space at the end of string line

Currently, when inserting data, TiDB keeps the space at the end of the line for the `VARCHAR` type, and truncate the space for the `CHAR` type. In case there is no index, TiDB behaves exactly the same as MySQL. 

If there is a `UNIQUE` index on the `VARCHAR` data, MySQL truncates the space at the end of the `VARCHAR` line before determining whether the data is duplicated, which is similar to the processing of the `CHAR` type, while TiDB keeps the space.

When making a comparison, MySQL first truncates the constant and the space at the end of the column, while TiDB keeps them to enable exact comparison.

### Type system differences

The following column types are supported by MySQL, but not by TiDB:

+ FLOAT4/FLOAT8
+ FIXED (alias for DECIMAL)
+ SERIAL (alias for BIGINT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE)
+ SQL_TSI_* (including SQL_TSI_YEAR, SQL_TSI_MONTH, SQL_TSI_WEEK, SQL_TSI_DAY, SQL_TSI_HOUR, SQL_TSI_MINUTE and SQL_TSI_SECOND)
