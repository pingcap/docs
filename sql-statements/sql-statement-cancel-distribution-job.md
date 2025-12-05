---
title: CANCEL DISTRIBUTION JOB
summary: TiDB 中 CANCEL DISTRIBUTION JOB 的用法概述。
---

# CANCEL DISTRIBUTION JOB <span class="version-mark">New in v8.5.4</span>

`CANCEL DISTRIBUTION JOB` 语句用于取消通过 [`DISTRIBUTE TABLE`](/sql-statements/sql-statement-distribute-table.md) 语句在 TiDB 中创建的 Region 调度任务。

<CustomContent platform="tidb-cloud">

> **Note:**
>
> 该功能在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。

</CustomContent>

## 语法

```ebnf+diagram
CancelDistributionJobsStmt ::=
    'CANCEL' 'DISTRIBUTION' 'JOB' JobID
```

## 示例

以下示例取消 ID 为 `1` 的分布式任务：

```sql
CANCEL DISTRIBUTION JOB 1;
```

输出如下：

```
Query OK, 0 rows affected (0.01 sec)
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 参考

* [`DISTRIBUTE TABLE`](/sql-statements/sql-statement-distribute-table.md)
* [`SHOW DISTRIBUTION JOBS`](/sql-statements/sql-statement-show-distribution-jobs.md)