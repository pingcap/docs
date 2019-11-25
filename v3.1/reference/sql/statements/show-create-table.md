---
title: SHOW CREATE TABLE | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW CREATE TABLE for the TiDB database.
category: reference
---

# SHOW CREATE TABLE

This statement shows the exact statement to recreate an existing table using SQL.

## Synopsis

**ShowStmt:**

![ShowStmt](/media/sqlgram-v3.0/ShowStmt.png)

**TableName:**

![TableName](/media/sqlgram-v3.0/TableName.png)

## Examples

```sql
mysql> CREATE TABLE t1 (a INT);
Query OK, 0 rows affected (0.12 sec)

mysql> SHOW CREATE TABLE t1;
+-------+------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                               |
+-------+------------------------------------------------------------------------------------------------------------+
| t1    | CREATE TABLE `t1` (
  `a` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+-------+------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## MySQL compatibility

This statement is understood to be fully compatible with MySQL. Any compatibility differences should be [reported via an issue](/v3.1/report-issue.md) on GitHub.

## See also

* [CREATE TABLE](/v3.1/reference/sql/statements/create-table.md)
* [DROP TABLE](/v3.1/reference/sql/statements/drop-table.md)
* [SHOW TABLES](/v3.1/reference/sql/statements/show-tables.md)
* [SHOW COLUMNS FROM](/v3.1/reference/sql/statements/show-columns-from.md)
