---
title: SHOW [FULL] TABLES | TiDB SQL 语句参考
summary: 关于 TiDB 数据库中使用 SHOW [FULL] TABLES 的概述。
---

# SHOW [FULL] TABLES

此语句显示当前选中的数据库中的表和视图列表。可选的关键字 `FULL` 表示表的类型是 `BASE TABLE`、`SEQUENCE` 还是 `VIEW`。

若要显示其他数据库中的表，可以使用 `SHOW TABLES IN DatabaseName`。

## 概要

```ebnf+diagram
ShowTableStmt ::=
    "SHOW" "FULL"? "TABLES" ("FROM" Identifier | "IN" Identifier )? ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 示例

```sql
mysql> CREATE TABLE t1 (a int);
Query OK, 0 rows affected (0.12 sec)

mysql> CREATE VIEW v1 AS SELECT 1;
Query OK, 0 rows affected (0.10 sec)

mysql> SHOW TABLES;
+----------------+
| Tables_in_test |
+----------------+
| t1             |
| v1             |
+----------------+
2 rows in set (0.00 sec)

mysql> SHOW FULL TABLES;
+----------------+------------+
| Tables_in_test | Table_type |
+----------------+------------+
| t1             | BASE TABLE |
| v1             | VIEW       |
+----------------+------------+
2 rows in set (0.00 sec)

mysql> SHOW TABLES IN mysql;
+-------------------------+
| Tables_in_mysql         |
+-------------------------+
| GLOBAL_VARIABLES        |
| bind_info               |
| columns_priv            |
| db                      |
| default_roles           |
| expr_pushdown_blacklist |
| gc_delete_range         |
| gc_delete_range_done    |
| global_priv             |
| help_topic              |
| opt_rule_blacklist      |
| role_edges              |
| stats_buckets           |
| stats_feedback          |
| stats_histograms        |
| stats_meta              |
| stats_top_n             |
| tables_priv             |
| tidb                    |
| user                    |
+-------------------------+
20 rows in set (0.00 sec)
```

## MySQL 兼容性

TiDB 中的 `SHOW [FULL] TABLES` 语句与 MySQL 完全兼容。如果你发现任何兼容性差异，[请报告一个 bug](https://docs.pingcap.com/tidb/stable/support)。

## 相关链接

* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [DROP TABLE](/sql-statements/sql-statement-drop-table.md)
* [SHOW CREATE TABLE](/sql-statements/sql-statement-show-create-table.md)
* [`INFORMATION_SCHEMA.TABLES`](/information-schema/information-schema-tables.md)