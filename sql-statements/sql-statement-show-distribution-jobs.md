---
title: SHOW DISTRIBUTION JOBS
summary: TiDBデータベースにおけるSHOW DISTRIBUTION JOBSの使用方法の概要。
---

# 配布ジョブの表示<span class="version-mark">（v8.5.4の新機能）</span> {#show-distribution-jobs-span-class-version-mark-new-in-v8-5-4-span}

`SHOW DISTRIBUTION JOBS`ステートメントは、現在実行中のリージョン配布ジョブをすべて表示します。

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この機能は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスではご利用いただけません。

</CustomContent>

## あらすじ {#synopsis}

```ebnf+diagram
ShowDistributionJobsStmt ::=
    "SHOW" "DISTRIBUTION" "JOBS"
```

## 例 {#examples}

現在実行中のリージョン配布ジョブをすべて表示します。

```sql
SHOW DISTRIBUTION JOBS;
```

    +--------+----------+-------+----------------+--------+----------------+-----------+---------------------+---------------------+---------------------+
    | Job_ID | Database | Table | Partition_List | Engine | Rule           | Status    | Create_Time         | Start_Time          | Finish_Time         |
    +--------+----------+-------+----------------+--------+----------------+-----------+---------------------+---------------------+---------------------+
    |    100 | test     | t1    | NULL           | tikv   | leader-scatter | finished  | 2025-04-24 16:09:55 | 2025-04-24 16:09:55 | 2025-04-24 17:09:59 |
    |    101 | test     | t2    | NULL           | tikv   | learner-scatter| cancelled | 2025-05-08 15:33:29 | 2025-05-08 15:33:29 | 2025-05-08 15:33:37 |
    |    102 | test     | t5    | p1,p2          | tikv   | peer-scatter   | cancelled | 2025-05-21 15:32:44 | 2025-05-21 15:32:47 | 2025-05-21 15:32:47 |
    +--------+----------+-------+----------------+--------+----------------+-----------+---------------------+---------------------+---------------------+

## MySQLとの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文に対するTiDBの拡張機能です。

## 関連項目 {#see-also}

-   [`DISTRIBUTE TABLE`](/sql-statements/sql-statement-distribute-table.md)
-   [`SHOW TABLE DISTRIBUTION`](/sql-statements/sql-statement-show-table-distribution.md)
-   [`CANCEL DISTRIBUTION JOB`](/sql-statements/sql-statement-cancel-distribution-job.md)
