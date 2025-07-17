---
title: Cached Tables
summary: 了解 TiDB 中的 cached table 功能，该功能用于很少更新的小型热点表，以提升读取性能。
---

# Cached Tables

在 v6.0.0 版本中，TiDB 引入了用于频繁访问但很少更新的小型热点表的 cached table 功能。启用该功能后，整个表的数据会加载到 TiDB 服务器的内存中，TiDB 直接从内存中获取表数据，而无需访问 TiKV，从而提升读取性能。

本文档描述了 cached table 的使用场景、示例以及与其他 TiDB 功能的兼容性限制。

## 使用场景

cached table 功能适用于具有以下特征的表：

- 表的数据量较小，例如小于 4 MiB。
- 表为只读或很少更新，例如每分钟写入请求（QPS）少于 10 次。
- 表被频繁访问，且希望获得更好的读取性能，例如在直接从 TiKV 读取时遇到小表的热点。

当表的数据量较小但访问频繁时，数据集中在 TiKV 的某个 Region 上，形成热点 Region，从而影响性能。因此，cached table 的典型使用场景包括：

- 配置表，应用程序从中读取配置信息。
- 金融行业中的汇率表。这些表每天只更新一次，但不是实时更新。
- 银行网点或网络信息表，这些表很少更新。

以配置表为例，当应用重启时，配置信息会加载到所有连接中，导致较高的读取延迟。此时，可以通过使用 cached table 功能解决此问题。

## 示例

本节通过示例介绍 cached table 的使用。

### 将普通表设置为 cached table

假设存在一张表 `users`：

```sql
CREATE TABLE users (
    id BIGINT,
    name VARCHAR(100),
    PRIMARY KEY(id)
);
```

要将此表设置为 cached table，使用 `ALTER TABLE` 语句：

```sql
ALTER TABLE users CACHE;
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

### 验证 cached table

使用 `SHOW CREATE TABLE` 语句验证表是否为 cached table。如果是，返回结果中会包含 `CACHED ON` 属性：

```sql
SHOW CREATE TABLE users;
```

```sql
+-------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                                                                                                                                               |
+-------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| users | CREATE TABLE `users` (
  `id` bigint NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin /* CACHED ON */ |
+-------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

从 cached table 读取数据后，TiDB 会将数据加载到内存中。你可以使用 [`TRACE`](/sql-statements/sql-statement-trace.md) 语句检查数据是否已加载到内存。当缓存未加载时，返回结果中会包含 `regionRequest.SendReqCtx` 属性，表示 TiDB 从 TiKV 读取数据。

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

再次执行 [`TRACE`](/sql-statements/sql-statement-trace.md)，返回结果中不再包含 `regionRequest.SendReqCtx` 属性，表示 TiDB 不再从 TiKV 读取数据，而是从内存中读取。

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

注意，cached table 使用 `UnionScan` 操作符，因此可以通过 `explain` 查看 cached table 的执行计划，看到 `UnionScan`：

```sql
+-------------------------+---------+-----------+---------------+--------------------------------+
| id                      | estRows | task      | access object | operator info                  |
+-------------------------+---------+-----------+---------------+--------------------------------+
| UnionScan_5             | 1.00    | root      |               |                                |
| └─TableReader_7         | 1.00    | root      |               | data:TableFullScan_6           |
|   └─TableFullScan_6     | 1.00    | cop[tikv] | table:users   | keep order:false, stats:pseudo |
+-------------------------+---------+-----------+---------------+--------------------------------+
```

### 向 cached table 写入数据

cached table 支持写入数据。例如，可以向 `users` 表插入一条记录：

```sql
INSERT INTO users(id, name) VALUES(1001, 'Davis');
```

```sql
Query OK, 1 row affected (0.00 sec)
```

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
> 当你向 cached table 插入数据时，可能会出现二级写入延迟。延迟由全局环境变量 [`tidb_table_cache_lease`](/system-variables.md#tidb_table_cache_lease-new-in-v600) 控制。你可以根据应用的接受程度决定是否使用 cached table 功能。例如，在只读场景中，可以增加 `tidb_table_cache_lease` 的值：
>
> ```sql
> set @@global.tidb_table_cache_lease = 10;
> ```
>
> cached table 的写入延迟较高，因为该功能通过复杂机制实现，需要为每个缓存设置租约。当存在多个 TiDB 实例时，一个实例不知道其他实例是否已缓存数据。如果某个实例直接修改表数据，其他实例会读取旧的缓存数据。为了确保正确性，cached table 采用租约机制，确保在租约到期前数据不被修改。这也是导致写入延迟较高的原因。

cached table 的元数据存储在 `mysql.table_cache_meta` 表中。该表记录所有 cached table 的 ID、当前锁状态（`lock_type`）以及锁租约信息（`lease`）。此表仅在 TiDB 内部使用，不建议修改，否则可能导致意外错误。

```sql
SHOW CREATE TABLE mysql.table_cache_meta\G
*************************** 1. row ***************************
       Table: table_cache_meta
Create Table: CREATE TABLE `table_cache_meta` (
  `tid` bigint NOT NULL DEFAULT '0',
  `lock_type` enum('NONE','READ','INTEND','WRITE') NOT NULL DEFAULT 'NONE',
  `lease` bigint NOT NULL DEFAULT '0',
  `oldReadLease` bigint NOT NULL DEFAULT '0',
  PRIMARY KEY (`tid`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
1 row in set (0.00 sec)
```

### 将 cached table 恢复为普通表

> **Note:**
>
> 在 cached table 上执行 DDL 语句会失败。在执行 DDL 之前，需要先移除缓存属性，将 cached table 恢复为普通表。

```sql
TRUNCATE TABLE users;
```

```sql
ERROR 8242 (HY000): 'Truncate Table' is unsupported on cache tables.
```

```sql
mysql> ALTER TABLE users ADD INDEX k_id(id);
```

```sql
ERROR 8242 (HY000): 'Alter Table' is unsupported on cache tables.
```

要将 cached table 恢复为普通表，使用 `ALTER TABLE t NOCACHE`：

```sql
ALTER TABLE users NOCACHE;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

## cached table 的大小限制

cached table 仅适用于小型表场景，因为 TiDB 会将整个表的数据加载到内存中，缓存数据在修改后会失效，需要重新加载。

目前，TiDB 中 cached table 的大小限制为 64 MiB。如果表数据超过 64 MiB，执行 `ALTER TABLE t CACHE` 会失败。

## 与其他 TiDB 功能的兼容性限制

cached table **不支持** 以下功能：

- 对分区表执行 `ALTER TABLE t ADD PARTITION` 操作不支持。
- 对临时表执行 `ALTER TABLE t CACHE` 操作不支持。
- 对视图执行 `ALTER TABLE t CACHE` 操作不支持。
- 不支持 Stale Read。
- 不支持对 cached table 进行直接 DDL 操作。需要先使用 `ALTER TABLE t NOCACHE` 将其恢复为普通表，再进行 DDL 操作。

cached table **不能** 在以下场景中使用：

- 设置系统变量 `tidb_snapshot` 以读取历史数据。
- 在修改过程中，缓存数据会变得无效，直到数据重新加载。

## 与 TiDB 迁移工具的兼容性

cached table 是 TiDB 对 MySQL 语法的扩展。只有 TiDB 能识别 `ALTER TABLE ... CACHE` 语句。TiDB 迁移工具 **不支持** cached table，包括 Backup & Restore (BR)、TiCDC 和 Dumpling。这些工具会将 cached table 视为普通表。

也就是说，当 cached table 被备份和还原后，会变成普通表。如果下游集群是不同的 TiDB 集群，且希望继续使用 cached table 功能，可以在下游集群手动启用 cached table，通过执行 `ALTER TABLE ... CACHE` 来实现。

## 参见

* [ALTER TABLE](/sql-statements/sql-statement-alter-table.md)
* [System Variables](/system-variables.md)