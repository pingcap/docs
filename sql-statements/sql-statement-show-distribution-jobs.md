---
title: SHOW DISTRIBUTION JOBS
summary: An overview of the usage of SHOW DISTRIBUTION JOBS for the TiDB database.
---

# SHOW DISTRIBUTION JOBS

The `SHOW DISTRIBUTION JOBS` statement shows all current Region distribution jobs.

## Syntax

```ebnf+diagram
ShowDistributionJobsStmt ::=
    "SHOW" "DISTRIBUTION" "JOBS"
```

## Examples

Show all current Region distribution jobs:

```sql
SHOW DISTRIBUTION JOBS;
```

```
+---------+------------+------------+-----------------+------------+-----------+----------+-------------+---------------+
| JOB_ID  |  DB_NAME   | TABLE_NAME | PARTITION_NAMES | ENGINE_TYPE | ROLE_TYPE | STATUS  | CREATE_USER | CREATE_TIME   |
+---------+------------+------------+-----------------+------------+-----------+--------+---------------+---------------+
|    1    |   db_1     |    t1      |                 | TIKV       | LEADER    | RUNNING  | ADMIN       | 20240712      |
|    2    |   db_1     |    t2      |                 | TIFLASH    | LEARNER   | FINISHED | ADMIN       | 20240715      |
|    3    |   db_1     |    t3      |                 | TiKV       | VOTER     | STOPPED  | ADMIN       | 20240713      |
|    4    |   db_1     |    t4      |                 | TIFLASH    | LEARNER   | FINISHED | ADMIN       | 20240713      |
+---------+------------+------------+-----------------+------------+-----------+----------+-------------+---------------+
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

- [`DISTRIBUTE TABLE`](/sql-statements/sql-statement-distribute-table.md)
- [`SHOW TABLE DISTRIBUTION`](/sql-statements/sql-statement-show-table-distribution.md)