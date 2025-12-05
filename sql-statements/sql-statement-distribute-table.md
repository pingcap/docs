---
title: DISTRIBUTE TABLE
summary: TiDB 数据库中 DISTRIBUTE TABLE 的用法概述。
---

# DISTRIBUTE TABLE <span class="version-mark">New in v8.5.4</span>

> **Warning:**
>
> 该功能为实验性功能。不建议在生产环境中使用。该功能可能会在没有提前通知的情况下更改或移除。如果你发现了 bug，可以在 GitHub 上提交一个 [issue](https://github.com/pingcap/tidb/issues)。

<CustomContent platform="tidb-cloud">

> **Note:**
>
> 该功能在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。

</CustomContent>

`DISTRIBUTE TABLE` 语句会重新分布并重新调度指定表的 Region，以实现表级别的均衡分布。执行该语句有助于防止 Region 集中在少数 TiFlash 或 TiKV 节点上，从而解决表内 Region 分布不均的问题。

## 语法

```ebnf+diagram
DistributeTableStmt ::=
    "DISTRIBUTE" "TABLE" TableName PartitionNameListOpt "RULE" EqOrAssignmentEq Identifier "ENGINE" EqOrAssignmentEq Identifier "TIMEOUT" EqOrAssignmentEq Identifier

TableName ::=
    (SchemaName ".")? Identifier

PartitionNameList ::=
    "PARTITION" "(" PartitionName ("," PartitionName)* ")"
```

## 参数说明

在使用 `DISTRIBUTE TABLE` 语句对表中的 Region 进行重新分布时，你可以指定存储引擎（如 TiFlash 或 TiKV）以及不同的 Raft 角色（如 Leader、Learner 或 Voter）以实现均衡分布。

- `RULE`：指定要均衡和调度的 Raft 角色的 Region。可选值为 `"leader-scatter"`、`"peer-scatter"` 和 `"learner-scatter"`。
- `ENGINE`：指定存储引擎。可选值为 `"tikv"` 和 `"tiflash"`。
- `TIMEOUT`：指定 scatter 操作的超时时间限制。如果 PD 在该时间内未完成 scatter，scatter 任务会自动退出。当未指定该参数时，默认值为 `"30m"`。

## 示例

在 TiKV 上重新分布表 `t1` 的 Leader 的 Region：

```sql
CREATE TABLE t1 (a INT);
...
DISTRIBUTE TABLE t1 RULE = "leader-scatter" ENGINE = "tikv" TIMEOUT = "1h";
```

```
+--------+
| JOB_ID |
+--------+
|    100 |
+--------+
```

在 TiFlash 上重新分布表 `t2` 的 Learner 的 Region：

```sql
CREATE TABLE t2 (a INT);
...
DISTRIBUTE TABLE t2 RULE = "learner-scatter" ENGINE = "tiflash";
```

```
+--------+
| JOB_ID |
+--------+
|    101 |
+--------+
```

在 TiKV 上重新分布表 `t3` 的 `p1` 和 `p2` 分区的 Peer 的 Region：

```sql
CREATE TABLE t3 ( a INT, b INT, INDEX idx(b)) PARTITION BY RANGE( a ) (
    PARTITION p1 VALUES LESS THAN (10000),
    PARTITION p2 VALUES LESS THAN (20000),
    PARTITION p3 VALUES LESS THAN (MAXVALUE) );
...
DISTRIBUTE TABLE t3 PARTITION (p1, p2) RULE = "peer-scatter" ENGINE = "tikv";
```

```
+--------+
| JOB_ID |
+--------+
|    102 |
+--------+
```

在 TiFlash 上重新分布表 `t4` 的 `p1` 和 `p2` 分区的 Learner 的 Region：

```sql
CREATE TABLE t4 ( a INT, b INT, INDEX idx(b)) PARTITION BY RANGE( a ) (
    PARTITION p1 VALUES LESS THAN (10000),
    PARTITION p2 VALUES LESS THAN (20000),
    PARTITION p3 VALUES LESS THAN (MAXVALUE) );
...
DISTRIBUTE TABLE t4 PARTITION (p1, p2) RULE = "learner-scatter" ENGINE="tiflash";
```

```
+--------+
| JOB_ID |
+--------+
|    103 |
+--------+
```

## 注意事项

当你执行 `DISTRIBUTE TABLE` 语句对表的 Region 进行重新分布时，Region 的分布结果可能会受到 PD 热点调度器的影响。重新分布后，随着时间推移，该表的 Region 分布可能会再次变得不均衡。

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

- [`SHOW DISTRIBUTION JOBS`](/sql-statements/sql-statement-show-distribution-jobs.md)
- [`SHOW TABLE DISTRIBUTION`](/sql-statements/sql-statement-show-table-distribution.md)
- [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md)
- [`CANCEL DISTRIBUTION JOB`](/sql-statements/sql-statement-cancel-distribution-job.md)