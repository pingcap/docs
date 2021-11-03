---
title: CREATE PLACEMENT POLICY
summary: The usage of CREATE PLACEMENT POLICY in TiDB.
---

# CREATE PLACEMENT POLICY

> **Warning:**
>
> Placement Rules in SQL is an experimental feature. Syntax may change before its final release, and there may be bugs.
> If you understand the risks, run `SET GLOBAL tidb_enable_alter_placement = 1;` to enable this experiment.

`CREATE PLACEMENT POLICY` is used to create a named placement policy that can later be assigned to tables, partitions or database schemas.

## Synopsis

```ebnf+diagram
CreatePolicyStmt ::=
    "CREATE" "PLACEMENT" "POLICY" IfNotExists PolicyName PlacementOptionList

PolicyName ::=
    Identifier

PlacementOptionList ::=
    DirectPlacementOption
|   PlacementOptionList DirectPlacementOption
|   PlacementOptionList ',' DirectPlacementOption

DirectPlacementOption ::=
    "PRIMARY_REGION" EqOpt stringLit
|   "REGIONS" EqOpt stringLit
|   "FOLLOWERS" EqOpt LengthNum
|   "VOTERS" EqOpt LengthNum
|   "LEARNERS" EqOpt LengthNum
|   "SCHEDULE" EqOpt stringLit
|   "CONSTRAINTS" EqOpt stringLit
|   "LEADER_CONSTRAINTS" EqOpt stringLit
|   "FOLLOWER_CONSTRAINTS" EqOpt stringLit
|   "VOTER_CONSTRAINTS" EqOpt stringLit
|   "LEARNER_CONSTRAINTS" EqOpt stringLit
```

## Examples

> **Note:**
>
> See [`SHOW PLACEMENT LABELS`](/sql-statements/sql-statement-show-placement-labels.md) to see which regions are available in your cluster.
> If  you do not see any available, your TiKV installation might not have labels set correctly.

{{< copyable "sql" >}}

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

This statement is a TiDB extension to MySQL syntax.

## See also

* [Placement Rules](/placement-rules.md)
* [SHOW PLACEMENT](/sql-statements/sql-statement-show-placement.md)
* [ALTER PLACEMENT POLICY](/sql-statements/sql-statement-alter-placement-policy.md)
* [DROP PLACEMENT POLICY](/sql-statements/sql-statement-drop-placement-policy.md)