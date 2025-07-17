---
title: RENAME TABLE | TiDB SQL Statement Reference
summary: An overview of the usage of RENAME TABLE for the TiDB database.
---

# RENAME TABLE

This statement is used to rename existing tables and views, supporting renaming multiple tables at once and renaming across databases.

## Synopsis

```ebnf+diagram
RenameTableStmt ::=
    'RENAME' 'TABLE' TableToTable ( ',' TableToTable )*

TableToTable ::=
    TableName 'TO' TableName
```

## Examples

```sql
CREATE TABLE t1 (a int);
```

```
Query OK, 0 rows affected (0.12 sec)
```

```sql
SHOW TABLES;
```

```
+----------------+
| Tables_in_test |
+----------------+
| t1             |
+----------------+
1 row in set (0.00 sec)
```

```sql
RENAME TABLE t1 TO t2;
```

```
Query OK, 0 rows affected (0.08 sec)
```

```sql
SHOW TABLES;
```

```
+----------------+
| Tables_in_test |
+----------------+
| t2             |
+----------------+
1 row in set (0.00 sec)
```

The following example demonstrates how to rename multiple tables across databases, assuming that the databases `db1`, `db2`, `db3`, and `db4` already exist, and that the tables `db1.t1` and `db3.t3` already exist:

```sql
RENAME TABLE db1.t1 To db2.t2, db3.t3 To db4.t4;
```

```
Query OK, 0 rows affected (0.08 sec)
```

```sql
USE db1; SHOW TABLES;
```

```
Database changed
Empty set (0.00 sec)
```

```sql
USE db2; SHOW TABLES;
```

```
Database changed
+---------------+
| Tables_in_db2 |
+---------------+
| t2            |
+---------------+
1 row in set (0.00 sec)
```

```sql
USE db3; SHOW TABLES;
```

```
Database changed
Empty set (0.00 sec)
```

```sql
USE db4; SHOW TABLES;
```

```
Database changed
+---------------+
| Tables_in_db4 |
+---------------+
| t4            |
+---------------+
1 row in set (0.00 sec)
```

The atomic rename can be used to swap out a table without having any moment in which the table does not exist.

```sql
CREATE TABLE t1(id int PRIMARY KEY);
```

```
Query OK, 0 rows affected (0.04 sec)
```

```sql
CREATE TABLE t1_new(id int PRIMARY KEY, n CHAR(0));
````

```
Query OK, 0 rows affected (0.04 sec)
```

```sql
RENAME TABLE t1 TO t1_old, t1_new TO t1;
```

```
Query OK, 0 rows affected (0.07 sec)
```

```sql
SHOW CREATE TABLE t1\G
```

```
*************************** 1. row ***************************
       Table: t1
Create Table: CREATE TABLE `t1` (
  `id` int NOT NULL,
  `n` char(0) DEFAULT NULL,
  PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
1 row in set (0.00 sec)
```

## MySQL compatibility

The `RENAME TABLE` statement in TiDB is fully compatible with MySQL. If you find any compatibility differences, [report a bug](https://docs.pingcap.com/tidb/stable/support).

## See also

* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [SHOW TABLES](/sql-statements/sql-statement-show-tables.md)
* [ALTER TABLE](/sql-statements/sql-statement-alter-table.md)
