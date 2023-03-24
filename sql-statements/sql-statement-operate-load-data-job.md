---
title: [CANCEL|DROP] LOAD DATA
summary: An overview of the usage of [CANCEL|DROP] LOAD DATA for the TiDB database.
---

# [CANCEL|DROP] LOAD DATA

The `CANCEL LOAD DATA` statement cancels a LOAD DATA job created in the system.

The `DROP LOAD DATA` statement deletes a LOAD DATA job created in the system.

## Synopsis

```ebnf+diagram
CancelLoadDataJobsStmt ::=
    'CANCEL' 'LAOD' 'DATA' 'JOB' JobID

DropLoadDataJobsStmt ::=
    'DROP' 'LAOD' 'DATA' 'JOB' JobID
```

## Examples

```sql
CANCEL LOAD DATA JOB 1;
```

```
Query OK, 0 rows affected (0.01 sec)
```

```sql
DROP LOAD DATA JOB 1;
```

```
Query OK, 1 row affected (0.01 sec)
```

## MySQL compatibility

This statement is an extension of TiDB to MySQL syntax.

## See also

* [LOAD DATA](/sql-statements/sql-statement-load-data.md)
* [SHOW LOAD DATA](/sql-statements/sql-statement-show-load-data.md)
