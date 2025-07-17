---
title: CREATE TABLE LIKE | TiDB SQL 语句参考
summary: 关于在 TiDB 数据库中使用 CREATE TABLE LIKE 的概述。
---

# CREATE TABLE LIKE

此语句复制现有表的定义，但不复制任何数据。

## 概述

```ebnf+diagram
CreateTableLikeStmt ::=
    'CREATE' OptTemporary 'TABLE' IfNotExists TableName LikeTableWithOrWithoutParen OnCommitOpt

OptTemporary ::=
    ( 'TEMPORARY' | ('GLOBAL' 'TEMPORARY') )?

LikeTableWithOrWithoutParen ::=
    'LIKE' TableName
|   '(' 'LIKE' TableName ')'

OnCommitOpt ::=
    ('ON' 'COMMIT' 'DELETE' 'ROWS')?
```

## 示例

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

## 预分割区域

如果被复制的表定义了 `PRE_SPLIT_REGIONS` 属性，使用 `CREATE TABLE LIKE` 语句创建的表会继承此属性，并且新表上的 Region 将会被分割。关于 `PRE_SPLIT_REGIONS` 的详细信息，请参见 [`CREATE TABLE` 语句](/sql-statements/sql-statement-create-table.md)。

## MySQL 兼容性

TiDB 中的 `CREATE TABLE LIKE` 语句与 MySQL 完全兼容。如果你发现任何兼容性差异，[请报告一个 bug](https://docs.pingcap.com/tidb/stable/support)。

## 相关链接

* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [SHOW CREATE TABLE](/sql-statements/sql-statement-show-create-table.md)
