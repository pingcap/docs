---
title: SHOW DISTRIBUTION JOBS
summary: SHOW DISTRIBUTION JOBS 在 TiDB 数据库中的用法概述。
---

# SHOW DISTRIBUTION JOBS <span class="version-mark">New in v8.5.4</span>

`SHOW DISTRIBUTION JOBS` 语句用于显示当前所有的 Region 分布作业。

<CustomContent platform="tidb-cloud">

> **Note:**
>
> 此功能在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。

</CustomContent>

## 语法

```ebnf+diagram
ShowDistributionJobsStmt ::=
    "SHOW" "DISTRIBUTION" "JOBS"
```

## 示例

显示当前所有的 Region 分布作业：

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

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

- [`DISTRIBUTE TABLE`](/sql-statements/sql-statement-distribute-table.md)
- [`SHOW TABLE DISTRIBUTION`](/sql-statements/sql-statement-show-table-distribution.md)
- [`CANCEL DISTRIBUTION JOB`](/sql-statements/sql-statement-cancel-distribution-job.md)