---
title: CANCEL IMPORT
summary: An overview of the usage of CANCEL IMPORT in TiDB.
---

# CANCEL IMPORT

The `CANCEL IMPORT` statement is used to cancel a data import job created in TiDB.

## Required privileges

To cancel a data import job, you need to be the creator of the job or have the `SUPER` privilege.

## Synopsis

```ebnf+diagram
CancelImportJobsStmt ::=
    'CANCEL' 'IMPORT' 'JOB' JobID
```

## Example

```sql
CANCEL IMPORT JOB 1;
```

```
Query OK, 0 rows affected (0.01 sec)
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [IMPORT INTO](/sql-statements/sql-statement-import-into.md)
* [SHOW IMPORT JOB](/sql-statements/sql-statement-show-import-job.md)
