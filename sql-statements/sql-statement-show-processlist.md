---
title: SHOW [FULL] PROCESSLIST | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW [FULL] PROCESSLIST for the TiDB database.
---

# SHOW [FULL] PROCESSLIST

This statement lists the current sessions connected to the same TiDB server. The `Info` column contains the query text, which will be truncated unless the optional keyword `FULL` is specified.

## Synopsis

```ebnf+diagram
ShowProcesslistStmt ::=
    "SHOW" "FULL"? "PROCESSLIST"
```

## Examples

```sql
mysql> SHOW PROCESSLIST;
+------+------+-----------------+------+---------+------+------------+------------------+
| Id   | User | Host            | db   | Command | Time | State      | Info             |
+------+------+-----------------+------+---------+------+------------+------------------+
|    5 | root | 127.0.0.1:45970 | test | Query   |    0 | autocommit | SHOW PROCESSLIST |
+------+------+-----------------+------+---------+------+------------+------------------+
1 rows in set (0.00 sec)
```

## MySQL compatibility

* The `State` column in TiDB is non-descriptive. Representing state as a single value is more complex in TiDB, since queries are executed in parallel and each goroutine will have a different state at any one time.

## See also

* [KILL \[TIDB\]](/sql-statements/sql-statement-kill.md)
* [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md)
