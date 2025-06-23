---
title: CANCEL DISTRIBUTION JOB
summary: An overview of the usage of CANCEL DISTRIBUTION JOB in TiDB.
---

# CANCEL DISTRIBUTION JOB

The `CANCEL DISTRIBUTION JOB` statement is used to cancel a Region scheduling task created using the [`DISTRIBUTE TABLE`](/sql-statements/sql-statement-distribute-table.md) statement in TiDB.

## Syntax diagram

```ebnf+diagram
CancelDistributionJobsStmt ::=
    'CANCEL' 'DISTRIBUTION' 'JOB' JobID
```

## Examples

The following example cancels the distribution job with ID `1`:

```sql
CANCEL DISTRIBUTION JOB 1;
```

The output is as follows:

```
Query OK, 0 rows affected (0.01 sec)
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [`DISTRIBUTE TABLE`](/sql-statements/sql-statement-distribute-table.md)
* [`SHOW DISTRIBUTION JOBS`](/sql-statements/sql-statement-show-distribution-jobs.md)