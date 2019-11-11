---
title: ALTER TABLE | TiDB SQL Statement Reference
summary: An overview of the usage of ALTER TABLE for the TiDB database.
category: reference
---

# ALTER TABLE

This statement modifies an existing table to conform to a new table structure. The statement `ALTER TABLE` can be used to:

* [`ADD`](/v3.1/reference/sql/statements/add-index.md), [`DROP`](/v3.1/reference/sql/statements/drop-index.md), or [`RENAME`](/v3.1/reference/sql/statements/rename-index.md) indexes
* [`ADD`](/v3.1/reference/sql/statements/add-column.md), [`DROP`](/v3.1/reference/sql/statements/drop-column.md), [`MODIFY`](/v3.1/reference/sql/statements/modify-column.md) or [`CHANGE`](/v3.1/reference/sql/statements/change-column.md) columns

## Synopsis

**AlterTableStmt:**

![AlterTableStmt](/media/sqlgram-v3.0/AlterTableStmt.png)

**TableName:**

![TableName](/media/sqlgram-v3.0/TableName.png)

**AlterTableSpec:**

![AlterTableSpec](/media/sqlgram-v3.0/AlterTableSpec.png)

## Examples

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY auto_increment, c1 INT NOT NULL);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.03 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
+---------------------+----------+------+-------------------------------------------------------------+
| id                  | count    | task | operator info                                               |
+---------------------+----------+------+-------------------------------------------------------------+
| TableReader_7       | 10.00    | root | data:Selection_6                                            |
| └─Selection_6       | 10.00    | cop  | eq(test.t1.c1, 3)                                           |
|   └─TableScan_5     | 10000.00 | cop  | table:t1, range:[-inf,+inf], keep order:false, stats:pseudo |
+---------------------+----------+------+-------------------------------------------------------------+
3 rows in set (0.00 sec)

mysql> ALTER TABLE t1 ADD INDEX (c1);
Query OK, 0 rows affected (0.30 sec)

mysql> EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
+-------------------+-------+------+-----------------------------------------------------------------+
| id                | count | task | operator info                                                   |
+-------------------+-------+------+-----------------------------------------------------------------+
| IndexReader_6     | 10.00 | root | index:IndexScan_5                                               |
| └─IndexScan_5     | 10.00 | cop  | table:t1, index:c1, range:[3,3], keep order:false, stats:pseudo |
+-------------------+-------+------+-----------------------------------------------------------------+
2 rows in set (0.00 sec)
```

## MySQL compatibility

* All of the data types except spatial types are supported.
* `FULLTEXT`, `HASH` and `SPATIAL` indexes are not supported.

## See also

* [ADD COLUMN](/v3.1/reference/sql/statements/add-column.md)
* [DROP COLUMN](/v3.1/reference/sql/statements/drop-column.md)
* [ADD INDEX](/v3.1/reference/sql/statements/add-index.md)
* [DROP INDEX](/v3.1/reference/sql/statements/drop-index.md)
* [RENAME INDEX](/v3.1/reference/sql/statements/rename-index.md)
* [CREATE TABLE](/v3.1/reference/sql/statements/create-table.md)
* [DROP TABLE](/v3.1/reference/sql/statements/drop-table.md)
* [SHOW CREATE TABLE](/v3.1/reference/sql/statements/show-create-table.md)
