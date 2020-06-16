---
title: DROP DATABASE | TiDB SQL Statement Reference
summary: An overview of the usage of DROP DATABASE for the TiDB database.
category: reference
aliases: ['/docs/dev/reference/sql/statements/drop-database/']
---

# DROP DATABASE

The `DROP DATABASE` statement permanently removes a specified database schema, and all of the tables and views that were created inside. User privileges that are associated with the dropped database remain unaffected.

## Synopsis

**DropDatabaseStmt:**

![DropDatabaseStmt](/media/sqlgram/DropDatabaseStmt.png)

**IfExists:**

![IfExists](/media/sqlgram/IfExists.png)

## Examples

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

## MySQL compatibility

This statement is understood to be fully compatible with MySQL. Any compatibility differences should be [reported via an issue](/report-issue.md) on GitHub.

## See also

* [CREATE DATABASE](/sql-statements/sql-statement-create-database.md)
* [ALTER DATABASE](/sql-statements/sql-statement-alter-database.md)
