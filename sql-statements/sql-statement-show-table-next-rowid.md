---
title: SHOW TABLE NEXT_ROW_ID
summary: Learn the usage of `SHOW TABLE NEXT_ROW_ID` in TiDB.
---

# SHOW TABLE NEXT_ROW_ID

`SHOW TABLE NEXT_ROW_ID` is used to show the details of some special columns of a table, including:

* [`AUTO_INCREMENT`](/auto-increment.md) column automatically created by TiDB, namely, `_tidb_rowid` column.
* `AUTO_INCREMENT` column created by users.
* [`AUTO_RANDOM`](/auto-random.md) column created by users.
* [`SEQUENCE`](/sql-statements/sql-statement-create-sequence.md) created by users.

## Synopsis

```ebnf+diagram
ShowTableNextRowIDStmt ::=
    "SHOW" "TABLE" (SchemaName ".")? TableName "NEXT_ROW_ID"
```

## Examples

For newly created tables, `NEXT_GLOBAL_ROW_ID` is `1` because no Row ID is allocated.

```sql
CREATE TABLE t(a int);
Query OK, 0 rows affected (0.06 sec)
```

```sql
SHOW TABLE t NEXT_ROW_ID;
+---------+------------+-------------+--------------------+
| DB_NAME | TABLE_NAME | COLUMN_NAME | NEXT_GLOBAL_ROW_ID |
+---------+------------+-------------+--------------------+
| test    | t          | _tidb_rowid |                  1 |
+---------+------------+-------------+--------------------+
1 row in set (0.00 sec)
```

Data have been written to the table. The TiDB server that inserts the data allocates and caches 30000 IDs at once. Thus, NEXT_GLOBAL_ROW_ID is 30001 now. The number of IDs is controlled by [`AUTO_ID_CACHE`](/auto-increment.md#auto_id_cache).

```sql
INSERT INTO t VALUES (), (), ();
Query OK, 3 rows affected (0.02 sec)
Records: 3  Duplicates: 0  Warnings: 0
```

```sql
SHOW TABLE t NEXT_ROW_ID;
+---------+------------+-------------+--------------------+
| DB_NAME | TABLE_NAME | COLUMN_NAME | NEXT_GLOBAL_ROW_ID |
+---------+------------+-------------+--------------------+
| test    | t          | _tidb_rowid |              30001 |
+---------+------------+-------------+--------------------+
1 row in set (0.00 sec)
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [AUTO_RANDOM](/auto-random.md)
* [CREATE_SEQUENCE](/sql-statements/sql-statement-create-sequence.md)
