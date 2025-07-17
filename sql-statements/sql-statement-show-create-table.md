---
title: SHOW CREATE TABLE | TiDB SQL 语句参考
summary: 关于在 TiDB 数据库中使用 SHOW CREATE TABLE 的概述。
---

# SHOW CREATE TABLE

此语句用于显示用 SQL 重建现有表的确切语句。

## 语法简介

```ebnf+diagram
ShowCreateTableStmt ::=
    "SHOW" "CREATE" "TABLE" (SchemaName ".")? TableName
```

## 示例

```sql
mysql> CREATE TABLE t1 (a INT);
Query OK, 0 rows affected (0.12 sec)

mysql> SHOW CREATE TABLE t1\G
*************************** 1. row ***************************
       Table: t1
Create Table: CREATE TABLE `t1` (
  `a` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
1 row in set (0.00 sec)
```

## MySQL 兼容性

TiDB 中的 `SHOW CREATE TABLE` 语句与 MySQL 完全兼容。如果你发现任何兼容性差异，[请报告一个 bug](https://docs.pingcap.com/tidb/stable/support)。

## 相关链接

* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [DROP TABLE](/sql-statements/sql-statement-drop-table.md)
* [SHOW TABLES](/sql-statements/sql-statement-show-tables.md)
* [SHOW COLUMNS FROM](/sql-statements/sql-statement-show-columns-from.md)