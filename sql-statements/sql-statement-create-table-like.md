---
title: CREATE TABLE LIKE | TiDB SQL Statement Reference
summary: An overview of the usage of CREATE TABLE LIKE for the TiDB database.
category: reference
aliases: ['/docs/dev/reference/sql/statements/create-table-like/']
---

# CREATE TABLE LIKE

This statement copies the definition of an existing table, without copying any data.

## Synopsis

**CreateTableStmt:**

![CreateTableLikeStmt](/media/sqlgram/CreateTableLikeStmt.png)

**LikeTableWithOrWithoutParen:**

![LikeTableWithOrWithoutParen](/media/sqlgram/LikeTableWithOrWithoutParen.png)

## Examples

```sql
mysql> CREATE TABLE t1 (a INT NOT NULL);
Query OK, 0 rows affected (0.13 sec)

mysql> INSERT INTO t1 VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.02 sec)
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

mysql> CREATE TABLE t2 LIKE t1;
Query OK, 0 rows affected (0.10 sec)

mysql> SELECT * FROM t2;
Empty set (0.00 sec)
```

## Presplit region

The table built with `CREATE TABLE LIKE` inherits the attribute `PRE_SPLIT_REGIONS`. When creating a table, the region on the new table will be split. 
如果被复制的表定义了 `PRE_SPLIT_REGIONS` 属性，则通过 `CREATE TABLE LIKE` 语句复制的表，会继承该属性并在建表时预切分 Region。For details of `PRE_SPLIT_REGIONS`, see [`CREATE TABLE` Statement](/sql-statements/sql-statement-create-table.md)。

## MySQL compatibility

This statement is understood to be fully compatible with MySQL. Any compatibility differences should be [reported via an issue](/report-issue.md) on GitHub.

## See also

* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [SHOW CREATE TABLE](/sql-statements/sql-statement-show-create-table.md)
