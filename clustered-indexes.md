---
title: 聚簇索引
summary: 了解聚簇索引的概念、使用场景、用法、限制和兼容性。
---

# 聚簇索引

自 v5.0 起，TiDB 支持聚簇索引功能。该功能控制包含主键的表中数据的存储方式，使 TiDB 能够以提升特定查询性能的方式组织表数据。

此处的 _clustered_ 指的是 _数据的存储组织方式_，而不是 _一组协同工作的数据库服务器_。某些数据库管理系统将聚簇索引表称为 _索引组织表_（IOT）。

目前，TiDB 中包含主键的表分为以下两类：

- `NONCLUSTERED`：表的主键为非聚簇索引。在非聚簇索引表中，行数据的键由 TiDB 隐式分配的内部 [`_tidb_rowid`](/tidb-rowid.md) 值组成。由于主键本质上是唯一索引，非聚簇索引表存储一行数据至少需要两个键值对，分别为：
    - `_tidb_rowid`（键）- 行数据（值）
    - 主键数据（键）- `_tidb_rowid`（值）
- `CLUSTERED`：表的主键为聚簇索引。在聚簇索引表中，行数据的键由用户指定的主键数据组成。因此，聚簇索引表存储一行数据只需一个键值对，即：
    - 主键数据（键）- 行数据（值）

> **注意：**
>
> TiDB 仅支持按表的 `PRIMARY KEY` 进行聚簇。启用聚簇索引后，_the_ `PRIMARY KEY` 和 _the clustered index_ 这两个术语可能会互换使用。`PRIMARY KEY` 指的是约束（逻辑属性），而聚簇索引描述了数据存储的物理实现方式。

## 使用场景

与非聚簇索引表相比，聚簇索引表在以下场景下具有更高的性能和吞吐优势：

+ 插入数据时，聚簇索引减少了一次索引数据的网络写入。
+ 当查询等值条件仅涉及主键时，聚簇索引减少了一次索引数据的网络读取。
+ 当查询范围条件仅涉及主键时，聚簇索引减少了多次索引数据的网络读取。
+ 当查询等值或范围条件仅涉及主键前缀时，聚簇索引减少了多次索引数据的网络读取。

另一方面，聚簇索引表也存在一些劣势，如下所示：

- 当插入大量值接近的主键时，可能会出现写入热点问题。
- 如果主键的数据类型大于 64 位，尤其存在多个二级索引时，表数据会占用更多存储空间。

## 用法

### 创建带聚簇索引的表

自 TiDB v5.0 起，你可以在 `CREATE TABLE` 语句中，在 `PRIMARY KEY` 后添加非保留关键字 `CLUSTERED` 或 `NONCLUSTERED`，以指定表的主键是否为聚簇索引。例如：

```sql
CREATE TABLE t (a BIGINT PRIMARY KEY CLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT PRIMARY KEY NONCLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT KEY CLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT KEY NONCLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) CLUSTERED);
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) NONCLUSTERED);
```

注意，在列定义中，关键字 `KEY` 和 `PRIMARY KEY` 含义相同。

你也可以使用 TiDB 的 [注释语法](/comment-syntax.md) 指定主键类型。例如：

```sql
CREATE TABLE t (a BIGINT PRIMARY KEY /*T![clustered_index] CLUSTERED */, b VARCHAR(255));
CREATE TABLE t (a BIGINT PRIMARY KEY /*T![clustered_index] NONCLUSTERED */, b VARCHAR(255));
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) /*T![clustered_index] CLUSTERED */);
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) /*T![clustered_index] NONCLUSTERED */);
```

对于未显式指定 `CLUSTERED`/`NONCLUSTERED` 关键字的语句，默认行为由系统变量 [`@@global.tidb_enable_clustered_index`](/system-variables.md#tidb_enable_clustered_index-new-in-v50) 控制。该变量支持的取值如下：

- `OFF` 表示主键默认创建为非聚簇索引。
- `ON` 表示主键默认创建为聚簇索引。
- `INT_ONLY` 表示行为由配置项 `alter-primary-key` 控制。如果 `alter-primary-key` 设置为 `true`，主键默认创建为非聚簇索引；如果设置为 `false`，仅由整数型列组成的主键默认创建为聚簇索引。

`@@global.tidb_enable_clustered_index` 的默认值为 `ON`。

### 添加或删除聚簇索引

TiDB 不支持在表创建后添加或删除聚簇索引，也不支持聚簇索引与非聚簇索引之间的互相转换。例如：

```sql
ALTER TABLE t ADD PRIMARY KEY(b, a) CLUSTERED; -- 当前不支持。
ALTER TABLE t DROP PRIMARY KEY;     -- 如果主键为聚簇索引，则不支持。
ALTER TABLE t DROP INDEX `PRIMARY`; -- 如果主键为聚簇索引，则不支持。
```

### 添加或删除非聚簇索引

TiDB 支持在表创建后添加或删除非聚簇索引。你可以显式指定 `NONCLUSTERED` 关键字，也可以省略。例如：

```sql
ALTER TABLE t ADD PRIMARY KEY(b, a) NONCLUSTERED;
ALTER TABLE t ADD PRIMARY KEY(b, a); -- 如果省略关键字，主键默认为非聚簇索引。
ALTER TABLE t DROP PRIMARY KEY;
ALTER TABLE t DROP INDEX `PRIMARY`;
```

### 检查主键是否为聚簇索引

你可以通过以下方法之一检查表的主键是否为聚簇索引：

- 执行命令 `SHOW CREATE TABLE`。
- 执行命令 `SHOW INDEX FROM`。
- 查询系统表 `information_schema.tables` 中的 `TIDB_PK_TYPE` 列。

通过执行 `SHOW CREATE TABLE` 命令，可以看到 `PRIMARY KEY` 的属性是 `CLUSTERED` 还是 `NONCLUSTERED`。例如：

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

通过执行 `SHOW INDEX FROM` 命令，可以检查 `Clustered` 列的结果是否为 `YES` 或 `NO`。例如：

```sql
mysql> SHOW INDEX FROM t;
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
| Table | Non_unique | Key_name | Seq_in_index | Column_name | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment | Visible | Expression | Clustered |
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
| t     |          0 | PRIMARY  |            1 | a           | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | YES     | NULL       | YES       |
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
1 row in set (0.01 sec)
```

你还可以查询系统表 `information_schema.tables` 中的 `TIDB_PK_TYPE` 列，查看结果是 `CLUSTERED` 还是 `NONCLUSTERED`。例如：

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

目前，聚簇索引功能存在多种类型的限制，具体如下：

- 不支持且暂无支持计划的场景：
    - 聚簇索引与属性 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md) 不支持同时使用。同时，属性 [`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions) 对于非 [`AUTO_RANDOM`](/auto-random.md) 的聚簇索引表无效。
    - 不支持对聚簇索引表进行降级。如果需要降级此类表，请使用逻辑备份工具进行数据迁移。
- 尚未支持但有支持计划的场景：
    - 通过 `ALTER TABLE` 语句添加、删除或修改聚簇索引暂不支持。

如果你将聚簇索引与属性 `SHARD_ROW_ID_BITS` 同时使用，TiDB 会报如下错误：

```sql
mysql> CREATE TABLE t (a VARCHAR(255) PRIMARY KEY CLUSTERED) SHARD_ROW_ID_BITS = 3;
ERROR 8200 (HY000): Unsupported shard_row_id_bits for table with primary key as row id
```

## 兼容性

### 与早期和后续 TiDB 版本的兼容性

TiDB 支持对聚簇索引表进行升级，但不支持降级。这意味着在较高版本 TiDB 上的聚簇索引表数据无法在较低版本上使用。

聚簇索引功能在 TiDB v3.0 和 v4.0 中为部分支持。仅当以下条件全部满足时，默认启用：

- 表包含 `PRIMARY KEY`。
- `PRIMARY KEY` 仅包含一列。
- `PRIMARY KEY` 为整数型。

自 TiDB v5.0 起，聚簇索引功能对所有类型的主键均完全支持，但默认行为与 TiDB v3.0 和 v4.0 保持一致。你可以通过配置系统变量 `@@tidb_enable_clustered_index` 为 `ON` 或 `OFF` 来更改默认行为。详情参见 [创建带聚簇索引的表](#创建带聚簇索引的表)。

### 与 MySQL 的兼容性

TiDB 特有的注释语法支持将 `CLUSTERED` 和 `NONCLUSTERED` 关键字包裹在注释中。`SHOW CREATE TABLE` 的结果也包含 TiDB 特有的 SQL 注释。MySQL 数据库和早期版本的 TiDB 数据库会忽略这些注释。

### 与 TiDB 迁移工具的兼容性

聚簇索引功能仅在 v5.0 及以上版本与以下迁移工具兼容：

- 备份与恢复工具：BR、Dumpling 和 TiDB Lightning。
- 数据迁移与同步工具：DM 和 TiCDC。

但是，你无法通过 v5.0 版本的 BR 工具备份并恢复表来实现非聚簇索引表与聚簇索引表之间的互相转换，反之亦然。

### 与其他 TiDB 功能的兼容性

对于联合主键或单一非整数型主键的表，如果你将主键从非聚簇索引更改为聚簇索引，其行数据的键也会发生变化。因此，在 TiDB v5.0 之前可执行的 `SPLIT TABLE BY/BETWEEN` 语句，在 v5.0 及以上版本的 TiDB 中将不再适用。如果你希望对带聚簇索引的表使用 `SPLIT TABLE BY/BETWEEN`，则需要提供主键列的值，而不是指定整数值。示例如下：

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

属性 [`AUTO_RANDOM`](/auto-random.md) 只能用于聚簇索引，否则 TiDB 会返回如下错误：

```sql
mysql> create table t (a bigint primary key nonclustered auto_random);
ERROR 8216 (HY000): Invalid auto random: column a is not the integer primary key, or the primary key is nonclustered
```