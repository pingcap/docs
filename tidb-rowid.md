---
title: _tidb_rowid
summary: 了解 `_tidb_rowid` 是什么、何时可用以及如何安全地使用它。
---

# `_tidb_rowid`

`_tidb_rowid` 是 TiDB 自动生成的隐藏系统列。对于不使用聚簇索引的表，它充当表的内部行 ID。你不能在表结构中声明或修改此列，但当表使用 `_tidb_rowid` 作为其内部行 ID 时，可以在 SQL 中引用它。

在当前实现中，`_tidb_rowid` 是一个由 TiDB 自动管理的额外 `BIGINT NOT NULL` 列。

> **Warning:**
>
> - 不要在所有情况下都假设 `_tidb_rowid` 是全局唯一的。对于不使用聚簇索引的分区表，执行 `ALTER TABLE ... EXCHANGE PARTITION` 可能会导致不同分区之间出现重复的 `_tidb_rowid` 值。
> - 如果你需要稳定的唯一标识符，应定义并使用显式主键，而不是依赖 `_tidb_rowid`。

## `_tidb_rowid` 何时可用 {#when-tidb-rowid-is-available}

当表不使用聚簇主键作为唯一行标识符时，TiDB 会使用 `_tidb_rowid` 来标识每一行。实际来说，这意味着以下类型的表会使用 `_tidb_rowid`：

- 没有主键的表
- 主键被显式定义为 `NONCLUSTERED` 的表

对于使用聚簇索引的表，`_tidb_rowid` 不可用（即主键被定义为 `CLUSTERED` 的表，无论它是单列主键还是组合主键）。

以下示例展示了其中的区别：

```sql
CREATE TABLE t1 (a INT, b VARCHAR(20));
CREATE TABLE t2 (id BIGINT PRIMARY KEY NONCLUSTERED, a INT);
CREATE TABLE t3 (id BIGINT PRIMARY KEY CLUSTERED, a INT);
```

对于 `t1` 和 `t2`，你可以查询 `_tidb_rowid`，因为这些表不使用聚簇索引作为行标识符：

```sql
SELECT _tidb_rowid, a, b FROM t1;
SELECT _tidb_rowid, id, a FROM t2;
```

对于 `t3`，`_tidb_rowid` 不可用，因为聚簇主键已经是行标识符：

```sql
SELECT _tidb_rowid, id, a FROM t3;
```

```sql
ERROR 1054 (42S22): Unknown column '_tidb_rowid' in 'field list'
```

## 读取 `_tidb_rowid` {#read-tidb-rowid}

对于使用 `_tidb_rowid` 的表，你可以在 `SELECT` 语句中查询 `_tidb_rowid`。这对于分页、故障排查和批处理等任务很有帮助。

示例：

```sql
CREATE TABLE t (a INT, b VARCHAR(20));
INSERT INTO t VALUES (1, 'x'), (2, 'y');

SELECT _tidb_rowid, a, b FROM t ORDER BY _tidb_rowid;
```

```sql
+-------------+---+---+
| _tidb_rowid | a | b |
+-------------+---+---+
|           1 | 1 | x |
|           2 | 2 | y |
+-------------+---+---+
```

要查看 TiDB 接下来将为行 ID 分配的值，请使用 `SHOW TABLE ... NEXT_ROW_ID`：

```sql
SHOW TABLE t NEXT_ROW_ID;
```

```sql
+-----------------------+------------+-------------+--------------------+-------------+
| DB_NAME               | TABLE_NAME | COLUMN_NAME | NEXT_GLOBAL_ROW_ID | ID_TYPE     |
+-----------------------+------------+-------------+--------------------+-------------+
| update_doc_rowid_test | t          | _tidb_rowid |              30001 | _TIDB_ROWID |
+-----------------------+------------+-------------+--------------------+-------------+
```

## 写入 `_tidb_rowid` {#write-tidb-rowid}

默认情况下，TiDB 不允许通过 `INSERT`、`REPLACE` 或 `UPDATE` 语句直接写入 `_tidb_rowid`。

```sql
INSERT INTO t(_tidb_rowid, a, b) VALUES (101, 4, 'w');
```

```sql
ERROR 1105 (HY000): insert, update and replace statements for _tidb_rowid are not supported
```

如果你需要在数据导入或迁移期间保留原始行 ID，请先启用 [`tidb_opt_write_row_id`](/system-variables.md#tidb_opt_write_row_id) 系统变量：

```sql
SET @@tidb_opt_write_row_id = ON;
INSERT INTO t(_tidb_rowid, a, b) VALUES (100, 3, 'z');
SET @@tidb_opt_write_row_id = OFF;

SELECT _tidb_rowid, a, b FROM t WHERE _tidb_rowid = 100;
```

```sql
+-------------+---+---+
| _tidb_rowid | a | b |
+-------------+---+---+
|         100 | 3 | z |
+-------------+---+---+
```

> **Warning:**
>
> `tidb_opt_write_row_id` 适用于导入和迁移场景。不建议将其用于常规应用写入。

## 限制 {#restrictions}

- 你不能创建名为 `_tidb_rowid` 的用户列。
- 你不能将现有用户列重命名为 `_tidb_rowid`。
- `_tidb_rowid` 是 TiDB 的内部列。不要将其视为业务主键或长期标识符。
- 对于非聚簇分区表，不能保证 `_tidb_rowid` 的值在各分区之间唯一。执行 `EXCHANGE PARTITION` 后，不同分区中可能包含具有相同 `_tidb_rowid` 值的行。
- `_tidb_rowid` 是否存在取决于表结构。对于带有聚簇索引的表，请使用主键作为行标识符。

## 解决热点问题 {#address-hotspot-issues}

对于使用 `_tidb_rowid` 的表，TiDB 默认按递增顺序分配行 ID。在写入密集型工作负载中，这可能会造成写入热点。

为缓解此问题（针对依赖 `_tidb_rowid` 作为行 ID 的表），可以考虑使用 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md) 更均匀地分布行 ID，并在必要时使用 [`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions) 预先拆分 Regions。

示例：

```sql
CREATE TABLE t (
    id BIGINT PRIMARY KEY NONCLUSTERED,
    c INT
) SHARD_ROW_ID_BITS = 4;
```

`SHARD_ROW_ID_BITS` 仅适用于使用 `_tidb_rowid` 的表，不适用于带有聚簇索引的表。

## 相关语句和变量 {#related-statements-and-variables}

- [`SHOW TABLE NEXT_ROW_ID`](/sql-statements/sql-statement-show-table-next-rowid.md)：显示 TiDB 接下来将分配的行 ID
- [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)：对隐式行 ID 进行分片以减少热点
- [`Clustered Indexes`](/clustered-indexes.md)：说明表何时使用主键而不是 `_tidb_rowid`
- [`tidb_opt_write_row_id`](/system-variables.md#tidb_opt_write_row_id)：控制是否允许写入 `_tidb_rowid`

## 另请参阅 {#see-also}

- [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)
- [`AUTO_INCREMENT`](/auto-increment.md)
- [Non-transactional DML](/non-transactional-dml.md)