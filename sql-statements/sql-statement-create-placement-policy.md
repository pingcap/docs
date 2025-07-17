---
title: CREATE PLACEMENT POLICY
summary: 在 TiDB 中使用 CREATE PLACEMENT POLICY。
---

# CREATE PLACEMENT POLICY

`CREATE PLACEMENT POLICY` 用于创建一个命名的放置策略，之后可以将其分配给表、分区或数据库模式。

> **Note:**
>
> 该功能在 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

## Synopsis

```ebnf+diagram
CreatePolicyStmt ::=
    "CREATE" "PLACEMENT" "POLICY" IfNotExists PolicyName PlacementOptionList

PolicyName ::=
    Identifier

PlacementOptionList ::=
    PlacementOption
|   PlacementOptionList PlacementOption
|   PlacementOptionList ',' PlacementOption

PlacementOption ::=
    CommonPlacementOption
|   SugarPlacementOption
|   AdvancedPlacementOption

CommonPlacementOption ::=
    "FOLLOWERS" EqOpt LengthNum

SugarPlacementOption ::=
    "PRIMARY_REGION" EqOpt stringLit
|   "REGIONS" EqOpt stringLit
|   "SCHEDULE" EqOpt stringLit

AdvancedPlacementOption ::=
    "LEARNERS" EqOpt LengthNum
|   "CONSTRAINTS" EqOpt stringLit
|   "LEADER_CONSTRAINTS" EqOpt stringLit
|   "FOLLOWER_CONSTRAINTS" EqOpt stringLit
|   "LEARNER_CONSTRAINTS" EqOpt stringLit
|   "SURVIVAL_PREFERENCES" EqOpt stringLit
```

## Examples

> **Note:**
>
> 要了解你的集群中可用的区域，请参见 [`SHOW PLACEMENT LABELS`](/sql-statements/sql-statement-show-placement-labels.md)。
>
> 如果没有看到任何可用区域，可能是你的 TiKV 安装没有正确设置标签。

```sql
CREATE PLACEMENT POLICY p1 PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4;
CREATE TABLE t1 (a INT) PLACEMENT POLICY=p1;
SHOW CREATE PLACEMENT POLICY p1;
```

```
Query OK, 0 rows affected (0.08 sec)

Query OK, 0 rows affected (0.10 sec)

+--------+---------------------------------------------------------------------------------------------------+
| Policy | Create Policy                                                                                     |
+--------+---------------------------------------------------------------------------------------------------+
| p1     | CREATE PLACEMENT POLICY `p1` PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4 |
+--------+---------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## MySQL compatibility

该语句是 TiDB 对 MySQL 语法的扩展。

## See also

* [Placement Rules in SQL](/placement-rules-in-sql.md)
* [SHOW PLACEMENT](/sql-statements/sql-statement-show-placement.md)
* [ALTER PLACEMENT POLICY](/sql-statements/sql-statement-alter-placement-policy.md)
* [DROP PLACEMENT POLICY](/sql-statements/sql-statement-drop-placement-policy.md)