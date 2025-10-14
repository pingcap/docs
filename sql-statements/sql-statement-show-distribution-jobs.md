---
title: SHOW DISTRIBUTION JOBS
summary: An overview of the usage of SHOW DISTRIBUTION JOBS for the TiDB database.
---

# SHOW DISTRIBUTION JOBS <span class="version-mark">New in v9.0.0</span>

The `SHOW DISTRIBUTION JOBS` statement shows all current Region distribution jobs.

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This feature is not available on [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) and [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) clusters.

</CustomContent>

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
- [`SHOW TABLE DISTRIBUTION`](/sql-statements/sql-statement-show-table-distribution.md)
- [`CANCEL DISTRIBUTION JOB`](/sql-statements/sql-statement-cancel-distribution-job.md)