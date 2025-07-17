---
title: ADD COLUMN | TiDB SQL 语句参考
summary: 关于在 TiDB 数据库中使用 ADD COLUMN 的概述。
---

# ADD COLUMN

`ALTER TABLE.. ADD COLUMN` 语句在现有表中添加一列。在 TiDB 中，此操作是在线的，意味着添加列不会阻塞对表的读取或写入。

## 概要

```ebnf+diagram
AlterTableStmt
         ::= 'ALTER' 'IGNORE'? 'TABLE' TableName AddColumnSpec ( ',' AddColumnSpec )*

TableName ::=
    Identifier ('.' Identifier)?

AddColumnSpec
         ::= 'ADD' 'COLUMN' 'IF NOT EXISTS'? ColumnName ColumnType ColumnOption+ ( 'FIRST' | 'AFTER' ColumnName )?

ColumnType
         ::= NumericType
           | StringType
           | DateAndTimeType
           | 'SERIAL'

ColumnOption
         ::= 'NOT'? 'NULL'
           | 'AUTO_INCREMENT'
           | 'PRIMARY'? 'KEY' ( 'CLUSTERED' | 'NONCLUSTERED' )? ( 'GLOBAL' | 'LOCAL' )?
           | 'UNIQUE' 'KEY'? ( 'GLOBAL' | 'LOCAL' )?
           | 'DEFAULT' ( NowSymOptionFraction | SignedLiteral | NextValueForSequence )
           | 'SERIAL' 'DEFAULT' 'VALUE'
           | 'ON' 'UPDATE' NowSymOptionFraction
           | 'COMMENT' stringLit
           | ( 'CONSTRAINT' Identifier? )? 'CHECK' '(' Expression ')' ( 'NOT'? ( 'ENFORCED' | 'NULL' ) )?
           | 'GENERATED' 'ALWAYS' 'AS' '(' Expression ')' ( 'VIRTUAL' | 'STORED' )?
           | 'REFERENCES' TableName ( '(' IndexPartSpecificationList ')' )? Match? OnDeleteUpdateOpt
           | 'COLLATE' CollationName
           | 'COLUMN_FORMAT' ColumnFormat
           | 'STORAGE' StorageMedia
           | 'AUTO_RANDOM' ( '(' LengthNum ')' )?
```

## 示例

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 VALUES (NULL);
Query OK, 1 row affected (0.02 sec)

mysql> SELECT * FROM t1;
+----+
| id |
+----+
|  1 |
+----+
1 row in set (0.00 sec)

mysql> ALTER TABLE t1 ADD COLUMN c1 INT NOT NULL;
Query OK, 0 rows affected (0.28 sec)

mysql> SELECT * FROM t1;
+----+----+
| id | c1 |
+----+----+
|  1 |  0 |
+----+----+
1 row in set (0.00 sec)

mysql> ALTER TABLE t1 ADD c2 INT NOT NULL AFTER c1;
Query OK, 0 rows affected (0.28 sec)

mysql> SELECT * FROM t1;
+----+----+----+
| id | c1 | c2 |
+----+----+----+
|  1 |  0 |  0 |
+----+----+----+
1 row in set (0.00 sec)
```

## MySQL 兼容性

* 不支持将新添加的列设置为 `PRIMARY KEY`。
* 不支持将新添加的列设置为 `AUTO_INCREMENT`。
* 对生成列的添加有限制，详见：[generated column limitations](/generated-columns.md#limitations)。
* 在添加新列时，通过指定 `PRIMARY KEY` 或 `UNIQUE INDEX` 为 `GLOBAL` 来设置 [global index](/partitioned-table.md#global-indexes)，这是 TiDB 对 [partitioned tables](/partitioned-table.md) 的扩展，不兼容 MySQL。

## 相关链接

* [ADD INDEX](/sql-statements/sql-statement-add-index.md)
* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)