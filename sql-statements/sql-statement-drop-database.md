---
title: DROP DATABASE | TiDB SQL 语句参考
summary: 关于 TiDB 数据库中 DROP DATABASE 的用法概述。
---

# DROP DATABASE

`DROP DATABASE` 语句会永久删除指定的数据库架构，以及在其中创建的所有表和视图。与被删除数据库相关联的用户权限不会受到影响。

## 概要

```ebnf+diagram
DropDatabaseStmt ::=
    'DROP' 'DATABASE' IfExists DBName

IfExists ::= ( 'IF' 'EXISTS' )?
```

## 示例

```sql
mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| INFORMATION_SCHEMA |
| PERFORMANCE_SCHEMA |
| mysql              |
| test               |
+--------------------+
4 rows in set (0.00 sec)

mysql> DROP DATABASE test;
Query OK, 0 rows affected (0.25 sec)

mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| INFORMATION_SCHEMA |
| PERFORMANCE_SCHEMA |
| mysql              |
+--------------------+
3 rows in set (0.00 sec)
```

## MySQL 兼容性

TiDB 中的 `DROP DATABASE` 语句与 MySQL 完全兼容。如果你发现任何兼容性差异，[请报告一个 bug](https://docs.pingcap.com/tidb/stable/support)。

## 相关链接

* [CREATE DATABASE](/sql-statements/sql-statement-create-database.md)
* [ALTER DATABASE](/sql-statements/sql-statement-alter-database.md)