---
title: SHOW TABLE DISTRIBUTION
summary: An overview of the usage of SHOW TABLE DISTRIBUTION for the TiDB database.
---

# SHOW TABLE DISTRIBUTION

The `SHOW TABLE DISTRIBUTION` statement shows the Region distribution information for a specified table.

## Syntax

```ebnf+diagram
ShowTableDistributionStmt ::=
    "SHOW" "TABLE" "DISTRIBUTION" TableName

TableName ::=
    (SchemaName ".")? Identifier
```

## Examples

Show the Region distribution of the table `t1`:

```sql
SHOW TABLE DISTRIBUTION t1;
```

```
+--------+----------+-------+----------------+--------+----------------+-----------+---------------------+---------------------+---------------------+
| Job_ID | Database | Table | Partition_List | Engine | Rule           | Status    | Create_Time         | Start_Time          | Finish_Time         |
+--------+----------+-------+----------------+--------+----------------+-----------+---------------------+---------------------+---------------------+
|    100 | test     | t1    | NULL           | tikv   | leader-scatter | finished  | 2025-04-24 16:09:55 | 2025-04-24 16:09:55 | 2025-04-24 17:09:59 |
|    101 | test     | t2    | NULL           | tikv   | learner-scatter| cancelled | 2025-05-08 15:33:29 | 2025-05-08 15:33:29 | 2025-05-08 15:33:37 |
|    102 | test     | t5    | p1,p2          | tikv   | peer-scatter   | cancelled | 2025-05-21 15:32:44 | 2025-05-21 15:32:47 | 2025-05-21 15:32:47 |
+--------+----------+-------+----------------+--------+----------------+-----------+---------------------+---------------------+---------------------+
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

- [`DISTRIBUTE TABLE`](/sql-statements/sql-statement-distribute-table.md)
- [`SHOW DISTRIBUTION JOBS`](/sql-statements/sql-statement-show-distribution-jobs.md)
- [`CANCEL DISTRIBUTION JOB`](/sql-statements/sql-statement-cancel-distribution-job.md)