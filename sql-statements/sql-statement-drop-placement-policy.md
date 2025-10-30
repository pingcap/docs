---
title: DROP PLACEMENT POLICY
summary: The usage of ALTER PLACEMENT POLICY in TiDB.
---

# DROP PLACEMENT POLICY

`DROP PLACEMENT POLICY` 用于删除之前创建的放置策略（placement policy）。

> **Note:**
>
> 此功能在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。

## 语法

```ebnf+diagram
DropPolicyStmt ::=
    "DROP" "PLACEMENT" "POLICY" IfExists PolicyName

PolicyName ::=
    Identifier
```

## 示例

只有当放置策略未被任何表或分区引用时，才能删除该放置策略。

```sql
CREATE PLACEMENT POLICY p1 FOLLOWERS=4;
CREATE TABLE t1 (a INT PRIMARY KEY) PLACEMENT POLICY=p1;
DROP PLACEMENT POLICY p1;  -- 此语句会失败，因为放置策略 p1 仍被引用。

-- 查询哪些表和分区引用了该放置策略。
SELECT table_schema, table_name FROM information_schema.tables WHERE tidb_placement_policy_name='p1';
SELECT table_schema, table_name FROM information_schema.partitions WHERE tidb_placement_policy_name='p1';

ALTER TABLE t1 PLACEMENT POLICY=default;  -- 从 t1 表移除放置策略。
DROP PLACEMENT POLICY p1;  -- 删除成功。
```

```sql
Query OK, 0 rows affected (0.10 sec)

Query OK, 0 rows affected (0.11 sec)

ERROR 8241 (HY000): Placement policy 'p1' is still in use

+--------------+------------+
| table_schema | table_name |
+--------------+------------+
| test         | t1         |
+--------------+------------+
1 row in set (0.00 sec)

Empty set (0.01 sec)

Query OK, 0 rows affected (0.08 sec)

Query OK, 0 rows affected (0.21 sec)
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 参见

* [Placement Rules in SQL](/placement-rules-in-sql.md)
* [SHOW PLACEMENT](/sql-statements/sql-statement-show-placement.md)
* [CREATE PLACEMENT POLICY](/sql-statements/sql-statement-create-placement-policy.md)
* [ALTER PLACEMENT POLICY](/sql-statements/sql-statement-alter-placement-policy.md)