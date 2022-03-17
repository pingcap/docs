---
title: Table Cache
summary: Learn the table cache feature in TiDB, which is used for rarely-updated hotspot small tables to improve read performance.
---

# Table Cache

TiDB 在 v6.0.0 版本中引入了缓存表功能。该功能适用于频繁被访问且很少被修改的热点小表，即把整张表的数据加载到 TiDB 服务器的内存中，直接从内存中获取表数据，避免从 TiKV 获取表数据，从而提升读性能。

In v6.0.0, TiDB introduces the table feature for frequently accessed but rarely updated small hotspot tables. When this feature is used, the data of an entire table is loaded into the memory of the TiDB server, and TiDB directly gets the table data from the memory without accessing TiKV, which improves the read performance.

本文介绍了 TiDB 缓存表的使用场景、使用示例、与其他 TiDB 功能的兼容性限制。

This document describes the usage scenarios of table cache, the examples, and the compatibility restrictions with other TiDB features.

## 使用场景

## Usage scenarios

TiDB 缓存表功能适用于以下特点的表：

The table cache feature is suitable for tables with the following features:

- 表的数据量不大
- 只读表，或者几乎很少修改
- 表的访问很频繁，期望有更好的读性能

- The data volume is small.
- The table is read-only, or is rarely updated.
- The table is frequently accessed, and you expect a better read performance.

当表的数据量不大，访问又特别频繁的情况下，数据会集中在 TiKV 一个 Region 上，形成热点，从而影响性能。因此，TiDB 缓存表的典型使用场景如下：

When the data volume of the table is small but the data is frequently accessed, the data is concentrated on a Region in TiKV and makes it a hotspot Region, which affects the performance. Therefore, the typical usage scenarios of table cache are as follows:

- 配置表，业务通过该表读取配置信息
- 金融场景中的存储汇率的表，该表不会实时更新，每天只更新一次
- 银行分行或者网点信息表，该表很少新增记录项

- Configuration tables, through which applications read the configuration information.
- The tables of exchange rates in the financial sector, which is updated only once a day and not in real time.
- Bank branch or network information tables, which is rarely updated.

以配置表为例，当业务重启的瞬间，全部连接一起加载配置，会造成较高的数据库读延迟。如果使用了缓存表，则可以解决这样的问题。

Taking configuration tables as an example, when the application restarts, the configuration information is loaded in all connections, which causes a high read latency. You can solve this problem by using the table cache feature.

### 使用示例

## Examples

本节通过示例介绍缓存表的使用方法。

This section describes the usage of table cache by examples.

#### 将普通表设为缓存表

#### Set a normal table to a table cache

假设已存在普通表 `users`:

Suppose that there is a table `users`:

{{< copyable "sql" >}}

```sql
CREATE TABLE users (
    id BIGINT,
    name VARCHAR(100),
    PRIMARY KEY(id)
);
```

通过 `ALTER TABLE` 语句，可以将这张表设置成缓存表：

By using the `ALTER TABLE` statement, you can set this table to a table cache:

{{< copyable "sql" >}}

```sql
ALTER TABLE users CACHE;
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

#### 验证是否为缓存表

#### Verify a table cache

要验证一张表是否为缓存表，使用 `SHOW CREATE TABLE` 语句。如果为缓存表，返回结果中会带有 `CACHED ON` 属性：

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

从缓存表读取数据后，TiDB 会将数据加载到内存中。你可使用 `trace` 语句查看 TiDB 是否已将数据加载到内存中。当缓存还未加载时，语句的返回结果会出现 `regionRequest.SendReqCtx`，表示 TiDB 从 TiKV 读取了数据。

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

而再次执行 `trace`，返回结果中不再有 `regionRequest.SendReqCtx`，表示 TiDB 已经不再从 TiKV 读取数据，而是直接从内存中读取：

After executing `trace` again, the returned result does not contain the `regionRequest.SendReqCtx` attribute, which indicates that TiDB no longer reads data from TiKV, but instead reads data from memory.

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

注意，读取缓存表会使用 `UnionScan` 算子，所以通过 `explain` 查看缓存表的执行计划时，可能会在结果中看到 `UnionScan`：

Note that the `UnionScan` operator is used to read the table cache, so you will see `UnionScan` in the execution plan of the table cache using `explain`:

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

#### 往缓存表写入数据

#### Write data to table cache

缓存表支持写入数据。例如，往 `users` 表中插入一条记录：

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
> When you insert data to a table cache, second-level write latency might occur. The latency is controlled by the global environment variable [`tidb_table_cache_lease`](/system-variables.md#tidb_table_cache_lease-new-in-v600). You can consider whether the latency is acceptable based on your application, and decide whether to use the table cache. For example, for a read-only scenario, you can increase the value of `tidb_table_cache_lease`:
>
> {{< copyable "sql" >}}
>
> ```sql
> set @@global.tidb_table_cache_lease = 10;
> ```
>
> 缓存表的写入延时高是受到实现的限制。存在多个 TiDB 实例时，一个 TiDB 实例并不知道其它的 TiDB 实例是否缓存了数据，如果该实例直接修改了表数据，而其它 TiDB 实例依然读取旧的缓存数据，就会读到错误的结果。为了保证数据正确性，缓存表的实现使用了一套基于 lease 的复杂机制：读操作在缓存数据同时，还会对于缓存设置一个有效期，也就是 lease。在 lease 过期之前，无法对数据执行修改操作。因为修改操作必须等待 lease 过期，所以会出现写入延迟。
> The write latency of table cache is high because it is implemented with a complex mechanism that requires a lease to be set for each cache. When there are multiple TiDB instances, one instance does not know whether the other instances have cached data. If an instance modifies the table data directly, the other instances will read the old cache data. To ensure correctness, the table cache implementation uses a lease mechanism to ensure that the data is not modified before the lease expires. That is why the write latency is high.

#### 将缓存表恢复为普通表

#### Recover table cache to normal table

> **Note:**
>
> 对缓存表执行 DDL 语句会失败。若要对缓存表执行 DDL 语句，需要先去掉缓存属性，将缓存表设回普通表后，才能对其执行 DDL 语句。
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

使用 `ALTER TABLE t NOCACHE` 语句可以将缓存表恢复成普通表：

To recover a table cache to a normal table, use `ALTER TABLE t NOCACHE`:

{{< copyable "sql" >}}

```sql
ALTER TABLE users NOCACHE
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

## 缓存表大小限制

## Size limit of table cache

由于 TiDB 将整张缓存表的数据加载到 TiDB 进程的内存中，并且执行修改操作后缓存会失效，需要重新加载，所以 TiDB 缓存表只适用于表比较小的场景。

目前 TiDB 对于每张缓存表的大小限制为 64 MB。如果表的数据超过了 64 MB，执行 `ALTER TABLE t CACHE` 会失败。

The table cache is only suitable to scenarios with small tables, because TiDB loads the data of an entire table into memory, and the cached data becomes invalid after modification and needs to be reloaded.

Currently, the size limit of the table cache is 64 MB in TiDB. If the table data exceeds 64 MB, executing `ALTER TABLE t CACHE` will fail.

## 与其他 TiDB 功能的兼容性限制

## Compatibility restrictions with other TiDB features

以下是缓存表不支持的功能：

The table cache **DOES NOT** support the following features:

- 不支持对分区表执行 `ALTER TABLE t CACHE` 操作
- Performing the `ALTER TABLE t ADD PARTITION` operation on partitioned tables is not supported.
- 不支持对临时表执行 `ALTER TABLE t CACHE` 操作
- Performing the `ALTER TABLE t CACHE` operation on temporary tables is not supported.
- 不支持对视图执行 `ALTER TABLE t CACHE` 操作
- Performing the `ALTER TABLE t CACHE` operation on views is not supported.
- 不支持 Stale Read 功能
- Stale Read is not supported.
- 不支持对缓存表直接做 DDL 操作，需要先通过 `ALTER TABLE t NOCACHE` 将缓存表改回普通表后再进行 DDL 操作。
- Direct DDL operations on a table cache are not supported. You need to set the table cache back to a normal table first by using `ALTER TABLE t NOCACHE` before performing DDL operations.

以下是缓存表无法使用缓存的场景：
The table cache **CANNOT** be used in the following scenarios:

- 设置系统变量 `tidb_snapshot` 读取历史数据
- Setting the system variable `tidb_snapshot` to read historical data.
- 执行修改操作期间，已有缓存会失效，直到数据被再次加载
- During modification, the cached data becomes invalid until the data is reloaded.

## TiDB 生态工具兼容性

## Compatibility with TiDB ecosystem tools

缓存表并不是标准的 MySQL 功能，而是 TiDB 扩展。只有 TiDB 能识别 `ALTER TABLE CACHE` 语句。所有的 TiDB 生态工具均不支持缓存表功能，包括 Backup & Restore (BR)、TiCDC、Dumpling 等组件，它们会将缓存表当作普通表处理。

Table cache is not a standard MySQL feature but a TiDB extension. Only TiDB can recognize the `ALTER TABLE CACHE` statement. **NO** TiDB ecosystem tools support table cache, including Backup & Restore (BR), TiCDC, and Dumpling. They treat table cache as a normal table.

这意味着，备份恢复一张缓存表时，它会变成一张普通表。如果下游集群是另一套 TiDB 集群并且你希望继续使用缓存表功能，可以对下游集群中的表执行 `ALTER TABLE CACHE` 手动开启缓存表功能。

That is to say, when a table cache is backed up and restored, it becomes a normal table. If the downstream cluster is a different TiDB cluster and you want to continue using the table cache feature, you can manually enable the table cache on the downstream cluster by executing `ALTER TABLE CACHE` on the downstream table.

## See also

* [ALTER TABLE](/sql-statements/sql-statement-alter-table.md)
* [System Variables](/system-variables.md)
