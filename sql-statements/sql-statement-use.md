---
title: USE | TiDB SQL Statement Reference
summary: An overview of the usage of USE for the TiDB database.
aliases: ['/docs/v2.1/sql-statements/sql-statement-use/','/docs/v2.1/reference/sql/statements/use/']
---

# USE

The `USE` statement selects a current database for the user session.

## Synopsis

**UseStmt:**

![UseStmt](/media/sqlgram/UseStmt.png)

**DBName:**

![DBName](/media/sqlgram/DBName.png)

## Examples

```sql
mysql> USE mysql;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> SHOW TABLES;
+----------------------+
| Tables_in_mysql      |
+----------------------+
| GLOBAL_VARIABLES     |
| bind_info            |
| columns_priv         |
| db                   |
| default_roles        |
| gc_delete_range      |
| gc_delete_range_done |
| help_topic           |
| role_edges           |
| stats_buckets        |
| stats_feedback       |
| stats_histograms     |
| stats_meta           |
| tables_priv          |
| tidb                 |
| user                 |
+----------------------+
16 rows in set (0.00 sec)

mysql> CREATE DATABASE newtest;
Query OK, 0 rows affected (0.10 sec)

mysql> USE newtest;
Database changed
mysql> SHOW TABLES;
Empty set (0.00 sec)

mysql> CREATE TABLE t1 (a int);
Query OK, 0 rows affected (0.10 sec)

mysql> SHOW TABLES;
+-------------------+
| Tables_in_newtest |
+-------------------+
| t1                |
+-------------------+
1 row in set (0.00 sec)
```

## MySQL compatibility

This statement is understood to be fully compatible with MySQL. Any compatibility differences should be [reported via an issue](https://github.com/pingcap/tidb/issues/new/choose) on GitHub.

## See also

* [CREATE DATABASE](/sql-statements/sql-statement-create-database.md)
* [SHOW TABLES](/sql-statements/sql-statement-show-tables.md)
