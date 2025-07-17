---
title: RENAME TABLE | TiDB SQL Statement Reference
summary: 关于在 TiDB 数据库中使用 RENAME TABLE 的概述。
---

# RENAME TABLE

此语句用于重命名现有的表和视图，支持一次重命名多个表以及跨数据库重命名。

## 语法概要

```ebnf+diagram
RenameTableStmt ::=
    'RENAME' 'TABLE' TableToTable ( ',' TableToTable )*

TableToTable ::=
    TableName 'TO' TableName
```

## 示例

```sql
CREATE TABLE t1 (a int);
```

```
Query OK, 0 rows affected (0.12 sec)
```

```sql
SHOW TABLES;
```

```
+----------------+
| Tables_in_test |
+----------------+
| t1             |
+----------------+
1 row in set (0.00 sec)
```

```sql
RENAME TABLE t1 TO t2;
```

```
Query OK, 0 rows affected (0.08 sec)
```

```sql
SHOW TABLES;
```

```
+----------------+
| Tables_in_test |
+----------------+
| t2             |
+----------------+
1 row in set (0.00 sec)
```

以下示例演示如何在跨数据库的情况下重命名多个表，假设数据库 `db1`、`db2`、`db3` 和 `db4` 已经存在，且表 `db1.t1` 和 `db3.t3` 已存在：

```sql
RENAME TABLE db1.t1 To db2.t2, db3.t3 To db4.t4;
```

```
Query OK, 0 rows affected (0.08 sec)
```

```sql
USE db1; SHOW TABLES;
```

```
Database changed
Empty set (0.00 sec)
```

```sql
USE db2; SHOW TABLES;
```

```
Database changed
+---------------+
| Tables_in_db2 |
+---------------+
| t2            |
+---------------+
1 row in set (0.00 sec)
```

```sql
USE db3; SHOW TABLES;
```

```
Database changed
Empty set (0.00 sec)
```

```sql
USE db4; SHOW TABLES;
```

```
Database changed
+---------------+
| Tables_in_db4 |
+---------------+
| t4            |
+---------------+
1 row in set (0.00 sec)
```

原子重命名可以用来交换表，确保在操作过程中表不会出现不存在的瞬间。

```sql
CREATE TABLE t1(id int PRIMARY KEY);
```

```
Query OK, 0 rows affected (0.04 sec)
```

```sql
CREATE TABLE t1_new(id int PRIMARY KEY, n CHAR(0));
```

```
Query OK, 0 rows affected (0.04 sec)
```

```sql
RENAME TABLE t1 TO t1_old, t1_new TO t1;
```

```
Query OK, 0 rows affected (0.07 sec)
```

```sql
SHOW CREATE TABLE t1\G
```

```
*************************** 1. row ***************************
       Table: t1
Create Table: CREATE TABLE `t1` (
  `id` int NOT NULL,
  `n` char(0) DEFAULT NULL,
  PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
1 row in set (0.00 sec)
```

## MySQL 兼容性

TiDB 中的 `RENAME TABLE` 语句与 MySQL 完全兼容。如果你发现任何兼容性差异，请 [报告一个 bug](https://docs.pingcap.com/tidb/stable/support)。

## 相关链接

* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [SHOW TABLES](/sql-statements/sql-statement-show-tables.md)
* [ALTER TABLE](/sql-statements/sql-statement-alter-table.md)