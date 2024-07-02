---
title: PREPARE | TiDB SQL Statement Reference
summary: An overview of the usage of PREPARE for the TiDB database.
---

# PREPARE

The `PREPARE` statement provides an SQL interface to server-side prepared statements.

## Synopsis

```ebnf+diagram
PreparedStmt ::=
    'PREPARE' Identifier 'FROM' PrepareSQL

PrepareSQL ::=
    stringLit
|   UserVariable
```

> **Note:**
>
> For each `PREPARE` statement, the maximum number of placeholders is 65535.

To limit the number of `PREPARE` statements in the current TiDB instance, you can use the [`max_prepared_stmt_count`](/system-variables.md#max_prepared_stmt_count) system variable.

## Examples

```sql
mysql> PREPARE mystmt FROM 'SELECT ? as num FROM DUAL';
Query OK, 0 rows affected (0.00 sec)

mysql> SET @number = 5;
Query OK, 0 rows affected (0.00 sec)

mysql> EXECUTE mystmt USING @number;
+------+
| num  |
+------+
| 5    |
+------+
1 row in set (0.00 sec)

mysql> DEALLOCATE PREPARE mystmt;
Query OK, 0 rows affected (0.00 sec)
```

## MySQL compatibility

The `PREPARE` statement in TiDB is fully compatible with MySQL. If you find any compatibility differences, [report a bug](https://docs.pingcap.com/tidb/stable/support).

## See also

* [EXECUTE](/sql-statements/sql-statement-execute.md)
* [DEALLOCATE](/sql-statements/sql-statement-deallocate.md)
