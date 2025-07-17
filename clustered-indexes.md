---
title: Clustered Indexes
summary: 了解聚簇索引的概念、用户场景、用法、限制和兼容性。
---

# Clustered Indexes

TiDB 从 v5.0 版本开始支持聚簇索引功能。该功能控制包含主键的表中数据的存储方式。它赋予 TiDB 以组织表的能力，从而可以提升某些查询的性能。

在此上下文中，_clustered_ 一词指的是 _数据存储的组织方式_，而不是 _一组协同工作的数据库服务器_。一些数据库管理系统将聚簇索引表称为 _index-organized tables_（IOT）。

目前，TiDB 中包含主键的表被划分为以下两类：

- `NONCLUSTERED`：表的主键是非聚簇索引。在具有非聚簇索引的表中，行数据的键由 TiDB 隐式分配的内部 `_tidb_rowid` 组成。由于主键本质上是唯一索引，具有非聚簇索引的表存储一行数据需要至少两个键值对，分别是：
    - `_tidb_rowid`（键） - 行数据（值）
    - 主键数据（键） - `_tidb_rowid`（值）
- `CLUSTERED`：表的主键是聚簇索引。在具有聚簇索引的表中，行数据的键由用户提供的主键数据组成。因此，具有聚簇索引的表只需一个键值对即可存储一行数据，即：
    - 主键数据（键） - 行数据（值）

> **Note:**
>
> TiDB 仅支持通过表的 `PRIMARY KEY` 进行聚簇。启用聚簇索引后，_the_ `PRIMARY KEY` 和 _the clustered index_ 这两个术语可能会交替使用。`PRIMARY KEY` 指的是约束（逻辑属性），而聚簇索引描述的是数据存储的物理实现。

## 用户场景

与具有非聚簇索引的表相比，具有聚簇索引的表在以下场景中提供更高的性能和吞吐量优势：

+ 插入数据时，聚簇索引减少了一次网络索引数据的写入。
+ 当查询条件相等且只涉及主键时，聚簇索引减少了一次网络索引数据的读取。
+ 当范围条件查询只涉及主键时，聚簇索引减少了多次网络索引数据的读取。
+ 当查询条件相等或范围条件只涉及主键前缀时，聚簇索引减少了多次网络索引数据的读取。

另一方面，具有聚簇索引的表也存在一些缺点。请参见以下内容：

- 当插入大量值接近的主键时，可能会出现写入热点问题。
- 如果主键的数据类型大于 64 位，尤其是在存在多个二级索引的情况下，表数据会占用更多存储空间。

## 用法

### 创建带有聚簇索引的表

自 TiDB v5.0 起，你可以在 `CREATE TABLE` 语句中，在 `PRIMARY KEY` 后添加非保留关键字 `CLUSTERED` 或 `NONCLUSTERED`，以指定表的主键是否为聚簇索引。例如：

```sql
CREATE TABLE t (a BIGINT PRIMARY KEY CLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT PRIMARY KEY NONCLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT KEY CLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT KEY NONCLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) CLUSTERED);
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) NONCLUSTERED);
```

注意，`KEY` 和 `PRIMARY KEY` 在列定义中具有相同的含义。

你也可以在 TiDB 中使用 [comment 语法](/comment-syntax.md) 来指定主键的类型。例如：

```sql
CREATE TABLE t (a BIGINT PRIMARY KEY /*T![clustered_index] CLUSTERED */, b VARCHAR(255));
CREATE TABLE t (a BIGINT PRIMARY KEY /*T![clustered_index] NONCLUSTERED */, b VARCHAR(255));
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) /*T![clustered_index] CLUSTERED */);
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) /*T![clustered_index] NONCLUSTERED */);
```

对于未显式指定 `CLUSTERED`/`NONCLUSTERED` 关键字的语句，默认行为由系统变量 [`@@global.tidb_enable_clustered_index`](/system-variables.md#tidb_enable_clustered_index-new-in-v50) 控制。支持的取值如下：

- `OFF` 表示默认创建主键为非聚簇索引。
- `ON` 表示默认创建主键为聚簇索引。
- `INT_ONLY` 表示行为由配置项 `alter-primary-key` 控制。如果 `alter-primary-key` 设置为 `true`，则默认创建非聚簇索引的主键；如果设置为 `false`，则只有由整数列组成的主键会被创建为聚簇索引。

系统变量 `@@global.tidb_enable_clustered_index` 的默认值为 `ON`。

### 添加或删除聚簇索引

TiDB 不支持在表创建后添加或删除聚簇索引，也不支持聚簇索引与非聚簇索引之间的相互转换。例如：

```sql
ALTER TABLE t ADD PRIMARY KEY(b, a) CLUSTERED; -- 目前不支持。
ALTER TABLE t DROP PRIMARY KEY;     -- 如果主键是聚簇索引，则不支持。
ALTER TABLE t DROP INDEX `PRIMARY`; -- 如果主键是聚簇索引，则不支持。
```

### 添加或删除非聚簇索引

TiDB 支持在表创建后添加或删除非聚簇索引。可以显式指定关键字 `NONCLUSTERED`，也可以省略。例如：

```sql
ALTER TABLE t ADD PRIMARY KEY(b, a) NONCLUSTERED;
ALTER TABLE t ADD PRIMARY KEY(b, a); -- 省略关键字时，主键默认为非聚簇索引。
ALTER TABLE t DROP PRIMARY KEY;
ALTER TABLE t DROP INDEX `PRIMARY`;
```

### 查询主键是否为聚簇索引

你可以通过以下方法之一检查表的主键是否为聚簇索引：

- 执行命令 `SHOW CREATE TABLE`。
- 执行命令 `SHOW INDEX FROM`。
- 查询系统表 `information_schema.tables` 中的 `TIDB_PK_TYPE` 列。

通过运行 `SHOW CREATE TABLE`，可以看到 `PRIMARY KEY` 的属性是 `CLUSTERED` 还是 `NONCLUSTERED`。例如：

```sql
mysql> SHOW CREATE TABLE t;
+-------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                                                                                                                      |
+-------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| t     | CREATE TABLE `t` (
  `a` bigint NOT NULL,
  `b` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`a`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+-------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.01 sec)
```

通过运行 `SHOW INDEX FROM`，可以检查 `Clustered` 列的结果是否显示为 `YES` 或 `NO`。例如：

```sql
mysql> SHOW INDEX FROM t;
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
| Table | Non_unique | Key_name | Seq_in_index | Column_name | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment | Visible | Expression | Clustered |
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
| t     |          0 | PRIMARY  |            1 | a           | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | YES     | NULL       | YES       |
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
1 row in set (0.01 sec)
```

你也可以查询系统表 `information_schema.tables` 中的 `TIDB_PK_TYPE` 列，判断结果是否为 `CLUSTERED` 或 `NONCLUSTERED`。例如：

```sql
mysql> SELECT TIDB_PK_TYPE FROM information_schema.tables WHERE table_schema = 'test' AND table_name = 't';
+--------------+
| TIDB_PK_TYPE |
+--------------+
| CLUSTERED    |
+--------------+
1 row in set (0.03 sec)
```

## 限制

目前，聚簇索引功能存在若干限制。请参见以下内容：

- 不支持且不在支持计划中的场景：
    - 不支持将聚簇索引与属性 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md) 一起使用。同时，属性 [`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions) 不对非 [`AUTO_RANDOM`](/auto-random.md) 的聚簇索引表生效。
    - 不支持对具有聚簇索引的表进行降级。如果需要降级此类表，请使用逻辑备份工具迁移数据。
- 尚未支持但在支持计划中的场景：
    - 不支持使用 `ALTER TABLE` 语句添加、删除或修改聚簇索引。

如果你将聚簇索引与属性 `SHARD_ROW_ID_BITS` 一起使用，TiDB 会报错：

```sql
mysql> CREATE TABLE t (a VARCHAR(255) PRIMARY KEY CLUSTERED) SHARD_ROW_ID_BITS = 3;
ERROR 8200 (HY000): Unsupported shard_row_id_bits for table with primary key as row id
```

## 兼容性

### 与早期及后续版本的 TiDB 兼容性

TiDB 支持升级带有聚簇索引的表，但不支持降级此类表，也就是说，后续版本中带有聚簇索引的表中的数据在早期版本中不可用。

聚簇索引功能在 TiDB v3.0 和 v4.0 中部分支持。满足以下全部条件时，默认启用：

- 表包含 `PRIMARY KEY`。
- `PRIMARY KEY` 仅由一列组成。
- `PRIMARY KEY` 为 `INTEGER`。

自 TiDB v5.0 起，聚簇索引功能对所有类型的主键都已完全支持，但默认行为与 TiDB v3.0 和 v4.0 保持一致。若要更改默认行为，可以将系统变量 `@@tidb_enable_clustered_index` 设置为 `ON` 或 `OFF`。更多详情请参见 [Create a table with clustered indexes](#create-a-table-with-clustered-indexes)。

### 与 MySQL 的兼容性

TiDB 特定的注释语法支持将关键字 `CLUSTERED` 和 `NONCLUSTERED` 包裹在注释中。`SHOW CREATE TABLE` 的结果也包含 TiDB 特定的 SQL 注释。早期版本的 MySQL 和 TiDB 数据库会忽略这些注释。

### 与 TiDB 迁移工具的兼容性

聚簇索引功能仅与 v5.0 及更高版本中的以下迁移工具兼容：

- 备份与还原工具：BR、Dumpling 和 TiDB Lightning。
- 数据迁移与复制工具：DM 和 TiCDC。

但你不能通过使用 v5.0 版本的 BR 工具备份和还原表，来实现非聚簇索引表向聚簇索引表的转换，反之亦然。

### 与其他 TiDB 功能的兼容性

对于具有组合主键或单一非整数主键的表，如果你将主键从非聚簇索引更改为聚簇索引，其行数据的索引也会发生变化。因此，在 TiDB v5.0 之前版本中可执行的 `SPLIT TABLE BY/BETWEEN` 语句在 v5.0 及之后的版本中不再适用。如果你想使用 `SPLIT TABLE BY/BETWEEN` 来拆分带有聚簇索引的表，需要提供主键列的值，而不是指定整数值。示例如下：

```sql
mysql> create table t (a int, b varchar(255), primary key(a, b) clustered);
Query OK, 0 rows affected (0.01 sec)
mysql> split table t between (0) and (1000000) regions 5;
ERROR 1105 (HY000): Split table region lower value count should be 2
mysql> split table t by (0), (50000), (100000);
ERROR 1136 (21S01): Column count doesn't match value count at row 0
mysql> split table t between (0, 'aaa') and (1000000, 'zzz') regions 5;
+--------------------+----------------------+
| TOTAL_SPLIT_REGION | SCATTER_FINISH_RATIO |
+--------------------+----------------------+
|                  4 |                    1 |
+--------------------+----------------------+
1 row in set (0.00 sec)
mysql> split table t by (0, ''), (50000, ''), (100000, '');
+--------------------+----------------------+
| TOTAL_SPLIT_REGION | SCATTER_FINISH_RATIO |
+--------------------+----------------------+
|                  3 |                    1 |
+--------------------+----------------------+
1 row in set (0.01 sec)
```

属性 [`AUTO_RANDOM`](/auto-random.md) 只能用于聚簇索引，否则 TiDB 会返回以下错误：

```sql
mysql> create table t (a bigint primary key nonclustered auto_random);
ERROR 8216 (HY000): Invalid auto random: column a is not the integer primary key, or the primary key is nonclustered
```