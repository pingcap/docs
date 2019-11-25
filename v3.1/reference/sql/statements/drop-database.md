---
title: DROP DATABASE | TiDB SQL Statement Reference
summary: An overview of the usage of DROP DATABASE for the TiDB database.
category: reference
---

# DROP DATABASE

The `DROP DATABASE` statement permanently removes a specified database schema, and all of the tables and views that were created inside. User privileges that are associated with the dropped database remain unaffected.

## Synopsis

**DropDatabaseStmt:**

![DropDatabaseStmt](/media/sqlgram-v3.0/DropDatabaseStmt.png)

**DatabaseSym:**

![DatabaseSym](/media/sqlgram-v3.0/DatabaseSym.png)

**IfExists:**

![IfExists](/media/sqlgram-v3.0/IfExists.png)

**DBName:**

![DBName](/media/sqlgram-v3.0/DBName.png)

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

This statement is understood to be fully compatible with MySQL. Any compatibility differences should be [reported via an issue](/v3.1/report-issue.md) on GitHub.

## See also

* [CREATE DATABASE](/v3.1/reference/sql/statements/create-database.md)
* [ALTER DATABASE](/v3.1/reference/sql/statements/alter-database.md)
