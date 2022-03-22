---
title: Table Cache
summary: Learn the table cache feature in TiDB, which is used for rarely-updated hotspot small tables to improve read performance.
---

# Table Cache

In v6.0.0, TiDB introduces the table cache feature for frequently accessed but rarely updated small hotspot tables. When this feature is used, the data of an entire table is loaded into the memory of the TiDB server, and TiDB directly gets the table data from the memory without accessing TiKV, which improves the read performance.

This document describes the usage scenarios of table cache, the examples, and the compatibility restrictions with other TiDB features.

## Usage scenarios

The table cache feature is suitable for tables with the following characteristics:

- The data volume of the table is small.
- The table is read-only, or is rarely updated.
- The table is frequently accessed, and you expect a better read performance.

When the data volume of the table is small but the data is frequently accessed, the data is concentrated on a Region in TiKV and makes it a hotspot Region, which affects the performance. Therefore, the typical usage scenarios of table cache are as follows:

- 配置表，业务通过该表读取配置信息
- 金融场景中的存储汇率的表，该表不会实时更新，每天只更新一次
- 银行分行或者网点信息表，该表很少新增记录项

- Configuration tables, from which applications read the configuration information.
- The tables of exchange rates in the financial sector, which is updated only once a day and not in real time.
- Bank branch or network information tables, which is rarely updated.

Taking configuration tables as an example, when the application restarts, the configuration information is loaded in all connections, which causes a high read latency. You can solve this problem by using the table cache feature.

## Examples

This section describes the usage of table cache by examples.

#### Set a normal table to a table cache

Suppose that there is a table `users`:

{{< copyable "sql" >}}

```sql
CREATE TABLE users (
    id BIGINT,
    name VARCHAR(100),
    PRIMARY KEY(id)
);
```

By using the `ALTER TABLE` statement, you can set this table to a table cache:

{{< copyable "sql" >}}

```sql
ALTER TABLE users CACHE;
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

#### Verify a table cache

To verify a table cache, use the `SHOW CREATE TABLE` statement. If the table is cached, the returned result contains the `CACHED ON` attribute:

{{< copyable "sql" >}}

```sql
SHOW CREATE TABLE users;
```

```sql
+-------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                                                                                                                                               |
+-------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| users | CREATE TABLE `users` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin /* CACHED ON */ |
+-------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

After reading data from table cache, TiDB loads the data in memory. You can use the `trace` statement to check whether the data is loaded into memory. When the cache is not loaded, the returned result contains the `regionRequest.SendReqCtx` attribute, which indicates that TiDB reads data from TiKV.

{{< copyable "sql" >}}

```sql
TRACE SELECT * FROM users;
```

```sql
+------------------------------------------------+-----------------+------------+
| operation                                      | startTS         | duration   |
+------------------------------------------------+-----------------+------------+
| trace                                          | 17:47:39.969980 | 827.73µs   |
|   ├─session.ExecuteStmt                        | 17:47:39.969986 | 413.31µs   |
|   │ ├─executor.Compile                         | 17:47:39.969993 | 198.29µs   |
|   │ └─session.runStmt                          | 17:47:39.970221 | 157.252µs  |
|   │   └─TableReaderExecutor.Open               | 17:47:39.970294 | 47.068µs   |
|   │     └─distsql.Select                       | 17:47:39.970312 | 24.729µs   |
|   │       └─regionRequest.SendReqCtx           | 17:47:39.970454 | 189.601µs  |
|   ├─*executor.UnionScanExec.Next               | 17:47:39.970407 | 353.073µs  |
|   │ ├─*executor.TableReaderExecutor.Next       | 17:47:39.970411 | 301.106µs  |
|   │ └─*executor.TableReaderExecutor.Next       | 17:47:39.970746 | 6.57µs     |
|   └─*executor.UnionScanExec.Next               | 17:47:39.970772 | 17.589µs   |
|     └─*executor.TableReaderExecutor.Next       | 17:47:39.970776 | 6.59µs     |
+------------------------------------------------+-----------------+------------+
12 rows in set (0.01 sec)
```

After executing `trace` again, the returned result no longer contains the `regionRequest.SendReqCtx` attribute, which indicates that TiDB no longer reads data from TiKV, but instead reads data from the memory.

{{< copyable "sql" >}}

```sql
+----------------------------------------+-----------------+------------+
| operation                              | startTS         | duration   |
+----------------------------------------+-----------------+------------+
| trace                                  | 17:47:40.533888 | 453.547µs  |
|   ├─session.ExecuteStmt                | 17:47:40.533894 | 402.341µs  |
|   │ ├─executor.Compile                 | 17:47:40.533903 | 205.54µs   |
|   │ └─session.runStmt                  | 17:47:40.534141 | 132.084µs  |
|   │   └─TableReaderExecutor.Open       | 17:47:40.534202 | 14.749µs   |
|   ├─*executor.UnionScanExec.Next       | 17:47:40.534306 | 3.21µs     |
|   └─*executor.UnionScanExec.Next       | 17:47:40.534316 | 1.219µs    |
+----------------------------------------+-----------------+------------+
7 rows in set (0.00 sec)
```

Note that the `UnionScan` operator is used to read the table cache, so you can see `UnionScan` in the execution plan of the table cache:

{{< copyable "sql" >}}

```sql
+-------------------------+---------+-----------+---------------+--------------------------------+
| id                      | estRows | task      | access object | operator info                  |
+-------------------------+---------+-----------+---------------+--------------------------------+
| UnionScan_5             | 1.00    | root      |               |                                |
| └─TableReader_7         | 1.00    | root      |               | data:TableFullScan_6           |
|   └─TableFullScan_6     | 1.00    | cop[tikv] | table:users   | keep order:false, stats:pseudo |
+-------------------------+---------+-----------+---------------+--------------------------------+
3 rows in set (0.00 sec)
```

#### Write data to table cache

Table cache supports data writes. For example, you can insert a record into the `users` table:

{{< copyable "sql" >}}

```sql
INSERT INTO users(id, name) VALUES(1001, 'Davis');
```

```sql
Query OK, 1 row affected (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM users;
```

```sql
+------+-------+
| id   | name  |
+------+-------+
| 1001 | Davis |
+------+-------+
1 row in set (0.00 sec)
```

> **Note:**
>
> When you insert data to a table cache, second-level write latency might occur. The latency is controlled by the global environment variable [`tidb_table_cache_lease`](/system-variables.md#tidb_table_cache_lease-new-in-v600). You can consider whether the latency is acceptable based on your application, and decide whether to use the table cache. For example, in a read-only scenario, you can increase the value of `tidb_table_cache_lease`:
>
> {{< copyable "sql" >}}
>
> ```sql
> set @@global.tidb_table_cache_lease = 10;
> ```
>
> The write latency of table cache is high because it is implemented with a complex mechanism that requires a lease to be set for each cache. When there are multiple TiDB instances, one instance does not know whether the other instances have cached data. If an instance modifies the table data directly, the other instances will read the old cache data. To ensure correctness, the table cache implementation uses a lease mechanism to ensure that the data is not modified before the lease expires. That is why the write latency is high.

#### Recover table cache to normal table

> **Note:**
>
> Executing DDL statements on a table cache will fail. Before executing DDL statements on a table cache, you need to remove the cache attribute first and set the table cache back to a normal table.

{{< copyable "sql" >}}

```sql
TRUNCATE TABLE users;
```

```sql
ERROR 8242 (HY000): 'Truncate Table' is unsupported on cache tables.
```

{{< copyable "sql" >}}

```sql
mysql> ALTER TABLE users ADD INDEX k_id(id);
```

```sql
ERROR 8242 (HY000): 'Alter Table' is unsupported on cache tables.
```

To recover a table cache to a normal table, use `ALTER TABLE t NOCACHE`:

{{< copyable "sql" >}}

```sql
ALTER TABLE users NOCACHE
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

## Size limit of table cache

The table cache is only suitable to scenarios with small tables, because TiDB loads the data of an entire table into memory, and the cached data becomes invalid after modification and needs to be reloaded.

Currently, the size limit of the table cache is 64 MB in TiDB. If the table data exceeds 64 MB, executing `ALTER TABLE t CACHE` will fail.

## Compatibility restrictions with other TiDB features

以下是缓存表不支持的功能：

The table cache **DOES NOT** support the following features:

- Performing the `ALTER TABLE t ADD PARTITION` operation on partitioned tables is not supported.
- Performing the `ALTER TABLE t CACHE` operation on temporary tables is not supported.
- Performing the `ALTER TABLE t CACHE` operation on views is not supported.
- Stale Read is not supported.
- Direct DDL operations on a table cache are not supported. You need to set the table cache back to a normal table first by using `ALTER TABLE t NOCACHE` before performing DDL operations.

The table cache **CANNOT** be used in the following scenarios:

- Setting the system variable `tidb_snapshot` to read historical data.
- During modification, the cached data becomes invalid until the data is reloaded.

## Compatibility with TiDB ecosystem tools

缓存表并不是标准的 MySQL 功能，而是 TiDB 扩展。只有 TiDB 能识别 `ALTER TABLE CACHE` 语句。所有的 TiDB 生态工具均不支持缓存表功能，包括 Backup & Restore (BR)、TiCDC、Dumpling 等组件，它们会将缓存表当作普通表处理。

Table cache is not a standard MySQL feature but a TiDB extension. Only TiDB can recognize the `ALTER TABLE CACHE` statement. TiDB ecosystem tools **DOES NOT** support table cache, including Backup & Restore (BR), TiCDC, and Dumpling. They treat table cache as a normal table.

That is to say, when a table cache is backed up and restored, it becomes a normal table. If the downstream cluster is a different TiDB cluster and you want to continue using the table cache feature, you can manually enable the table cache on the downstream cluster by executing `ALTER TABLE CACHE` on the downstream table.

## See also

* [ALTER TABLE](/sql-statements/sql-statement-alter-table.md)
* [System Variables](/system-variables.md)
