---
title: ADMIN CANCEL DDL | TiDB SQL Statement Reference
summary: An overview of the usage of ADMIN CANCEL DDL for the TiDB database.
category: reference
---

# ADMIN CANCEL DDL

The `ADMIN CANCEL DDL` statement allows you to cancel a running DDL job. The `job_id` can be found by running [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md).

The `ADMIN CANCEL DDL` statement also allows you to cancel a DDL job that is committed but not yet completed executing. After the cancellation, the SQL statement that executes the DDL job returns the `ERROR 8214 (HY000): Cancelled DDL job` error. If you cancel a DDL job that has already been completed, you will see the `DDL Job:90 not found` error in the `RESULT` column, which indicates that the job has been removed from the DDL waiting queue.

## Synopsis

```ebnf+diagram
AdminCancelDDLStmt ::=
    'ADMIN' 'CANCEL' 'DDL' 'JOBS' NumList 

NumList ::=
    Int64Num ( ',' Int64Num )*
```

## Examples

To cancel the currently running DDL jobs and return whether the corresponding jobs are successfully cancelled, use `ADMIN CANCEL DDL JOBS`:

```sql
ADMIN CANCEL DDL JOBS job_id [, job_id] ...;
```

If the operation fails to cancel the jobs, specific reasons are displayed.

> **Note:**
>
> - Before v6.2.0, only this operation can cancel DDL jobs, and all other operations and environment changes (such as machine restart and cluster restart) cannot cancel these jobs. Starting from v6.2.0, [`KILL`](/sql-statements/sql-statement-kill.md) statements can also be used to cancel ongoing DDL jobs by killing them. 
> - This operation can cancel multiple DDL jobs at the same time. You can get the ID of DDL jobs using the [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md) statement.
> - If the jobs you want to cancel are finished, the cancellation operation fails.

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [`ADMIN SHOW DDL [JOBS|JOB QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)
