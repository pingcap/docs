---
title: TRUNCATE | TiDB SQL 语句参考
summary: 关于在 TiDB 数据库中使用 TRUNCATE 的概述。
---

# TRUNCATE

`TRUNCATE` 语句以非事务性的方式删除表中的所有数据。可以将 `TRUNCATE` 在语义上理解为 `DROP TABLE` + `CREATE TABLE`，与之前的定义相同。

无论是 `TRUNCATE TABLE tableName` 还是 `TRUNCATE tableName`，都是有效的语法。

## 概要

```ebnf+diagram
TruncateTableStmt ::=
    "TRUNCATE" ( "TABLE" )? TableName

TableName ::=
    (Identifier ".")? Identifier
```

## 示例

```sql
mysql> CREATE TABLE t1 (a INT NOT NULL PRIMARY KEY);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.01 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM t1;
+---+
| a |
+---+
| 1 |
| 2 |
| 3 |
| 4 |
| 5 |
+---+
5 rows in set (0.00 sec)

mysql> TRUNCATE t1;
Query OK, 0 rows affected (0.11 sec)

mysql> SELECT * FROM t1;
Empty set (0.00 sec)

mysql> INSERT INTO t1 VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.01 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> TRUNCATE TABLE t1;
Query OK, 0 rows affected (0.11 sec)
```

## MySQL 兼容性

TiDB 中的 `TRUNCATE` 语句与 MySQL 完全兼容。如果你发现任何兼容性差异，[请报告一个 bug](https://docs.pingcap.com/tidb/stable/support)。

## 相关链接

* [DROP TABLE](/sql-statements/sql-statement-drop-table.md)
* [DELETE](/sql-statements/sql-statement-delete.md)
* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [SHOW CREATE TABLE](/sql-statements/sql-statement-show-create-table.md)