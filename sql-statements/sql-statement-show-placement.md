---
title: SHOW PLACEMENT
summary: SHOW PLACEMENT 在 TiDB 中的用法。
---

# SHOW PLACEMENT

`SHOW PLACEMENT` 汇总所有来自放置策略的放置选项，并以规范的形式展示。

> **Note:**
>
> 该功能在 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

该语句返回一个结果集，其中 `Scheduling_State` 字段表示放置调度器（PD）在调度放置方面的当前进展：

* `PENDING`：PD 尚未开始调度放置。这可能表示放置规则在语义上是正确的，但目前无法被集群满足。例如，如果 `FOLLOWERS=4`，但只有 3 个 TiKV 存储节点作为候选追随者。
* `INPROGRESS`：PD 当前正在调度放置。
* `SCHEDULED`：PD 已成功调度放置。

## 概要

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

## 相关链接

* [Placement Rules in SQL](/placement-rules-in-sql.md)
* [SHOW PLACEMENT FOR](/sql-statements/sql-statement-show-placement-for.md)
* [CREATE PLACEMENT POLICY](/sql-statements/sql-statement-create-placement-policy.md)