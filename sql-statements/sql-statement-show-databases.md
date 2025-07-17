---
title: SHOW DATABASES | TiDB SQL 语句参考
summary: 关于 TiDB 数据库中 SHOW DATABASES 的用法概述。
---

# SHOW DATABASES

此语句显示当前用户有权限访问的数据库列表。当前用户没有访问权限的数据库将不会显示在列表中。`information_schema` 数据库始终会在数据库列表中优先显示。

`SHOW SCHEMAS` 是此语句的别名。

## 概要

```ebnf+diagram
ShowDatabasesStmt ::=
    "SHOW" "DATABASES" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
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

mysql> CREATE DATABASE mynewdb;
Query OK, 0 rows affected (0.10 sec)

mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| INFORMATION_SCHEMA |
| PERFORMANCE_SCHEMA |
| mynewdb            |
| mysql              |
| test               |
+--------------------+
5 rows in set (0.00 sec)
```

## MySQL 兼容性

TiDB 中的 `SHOW DATABASES` 语句与 MySQL 完全兼容。如果你发现任何兼容性差异，[请报告一个 bug](https://docs.pingcap.com/tidb/stable/support)。

## 相关链接

* [SHOW SCHEMAS](/sql-statements/sql-statement-show-schemas.md)
* [DROP DATABASE](/sql-statements/sql-statement-drop-database.md)
* [CREATE DATABASE](/sql-statements/sql-statement-create-database.md)
* [`INFORMATION_SCHEMA.SCHEMATA`](/information-schema/information-schema-schemata.md)