---
title: SHOW PLACEMENT
summary: SHOW PLACEMENT 在 TiDB 中的用法。
---

# SHOW PLACEMENT

`SHOW PLACEMENT` 汇总了所有来自 placement policy 的放置选项，并以规范形式展示。

> **Note:**
>
> 此功能在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。

该语句返回的结果集中，`Scheduling_State` 字段表示 Placement Driver（PD）在调度放置规则时的当前进度：

* `PENDING`：PD 尚未开始调度放置规则。这可能表示放置规则在语义上是正确的，但当前集群无法满足。例如，如果 `FOLLOWERS=4`，但只有 3 个 TiKV 节点可作为 follower。
* `INPROGRESS`：PD 正在调度放置规则。
* `SCHEDULED`：PD 已成功调度放置规则。

## 语法

```ebnf+diagram
ShowStmt ::=
    "SHOW" "PLACEMENT" ShowLikeOrWhere?
```

## 示例

```sql
CREATE PLACEMENT POLICY p1 PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4;
CREATE TABLE t1 (a INT) PLACEMENT POLICY=p1;
SHOW PLACEMENT;
```

```
Query OK, 0 rows affected (0.01 sec)

Query OK, 0 rows affected (0.00 sec)

+---------------+----------------------------------------------------------------------+------------------+
| Target        | Placement                                                            | Scheduling_State |
+---------------+----------------------------------------------------------------------+------------------+
| POLICY p1     | PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4 | NULL             |
| DATABASE test | PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4 | INPROGRESS       |
| TABLE test.t1 | PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4 | INPROGRESS       |
+---------------+----------------------------------------------------------------------+------------------+
4 rows in set (0.00 sec)
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [Placement Rules in SQL](/placement-rules-in-sql.md)
* [SHOW PLACEMENT FOR](/sql-statements/sql-statement-show-placement-for.md)
* [CREATE PLACEMENT POLICY](/sql-statements/sql-statement-create-placement-policy.md)