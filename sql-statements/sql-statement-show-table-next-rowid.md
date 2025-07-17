---
title: SHOW TABLE NEXT_ROW_ID
summary: 了解 TiDB 中 `SHOW TABLE NEXT_ROW_ID` 的用法。
---

# SHOW TABLE NEXT_ROW_ID

`SHOW TABLE NEXT_ROW_ID` 用于显示表的某些特殊列的详细信息，包括：

* [`AUTO_INCREMENT`](/auto-increment.md) 列，由 TiDB 自动创建，即 `_tidb_rowid` 列。
* 用户创建的 `AUTO_INCREMENT` 列。
* [`AUTO_RANDOM`](/auto-random.md) 列，由用户创建。
* [`SEQUENCE`](/sql-statements/sql-statement-create-sequence.md) 由用户创建。

## 语法

```ebnf+diagram
ShowTableNextRowIDStmt ::=
    "SHOW" "TABLE" (SchemaName ".")? TableName "NEXT_ROW_ID"
```

## 示例

对于新创建的表，`NEXT_GLOBAL_ROW_ID` 为 `1`，因为尚未分配任何行 ID。

```sql
CREATE TABLE t(a int);
Query OK, 0 rows affected (0.06 sec)
```

```sql
SHOW TABLE t NEXT_ROW_ID;
+---------+------------+-------------+--------------------+
| DB_NAME | TABLE_NAME | COLUMN_NAME | NEXT_GLOBAL_ROW_ID |
+---------+------------+-------------+--------------------+
| test    | t          | _tidb_rowid |                  1 |
+---------+------------+-------------+--------------------+
1 row in set (0.00 sec)
```

数据已写入表中。插入数据的 TiDB 服务器会一次性分配并缓存 30000 个 ID。因此，现在 `NEXT_GLOBAL_ROW_ID` 为 30001。ID 数量由 [`AUTO_ID_CACHE`](/auto-increment.md#auto_id_cache) 控制。

```sql
INSERT INTO t VALUES (), (), ();
Query OK, 3 rows affected (0.02 sec)
Records: 3  Duplicates: 0  Warnings: 0
```

```sql
SHOW TABLE t NEXT_ROW_ID;
+---------+------------+-------------+--------------------+
| DB_NAME | TABLE_NAME | COLUMN_NAME | NEXT_GLOBAL_ROW_ID |
+---------+------------+-------------+--------------------+
| test    | t          | _tidb_rowid |              30001 |
+---------+------------+-------------+--------------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 相关链接

* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [AUTO_RANDOM](/auto-random.md)
* [CREATE_SEQUENCE](/sql-statements/sql-statement-create-sequence.md)