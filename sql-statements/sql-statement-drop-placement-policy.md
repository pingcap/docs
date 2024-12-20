---
title: DROP PLACEMENT POLICY
summary: TiDB での ALTER PLACEMENT POLICY の使用法。
---

# ドロップ配置ポリシー {#drop-placement-policy}

`DROP PLACEMENT POLICY`以前に作成された配置ポリシーを削除するために使用されます。

> **注記：**
>
> この機能は[TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)クラスターでは使用できません。

## 概要 {#synopsis}

```ebnf+diagram
DropPolicyStmt ::=
    "DROP" "PLACEMENT" "POLICY" IfExists PolicyName

PolicyName ::=
    Identifier
```

## 例 {#examples}

配置ポリシーは、どのテーブルまたはパーティションからも参照されていない場合にのみ削除できます。

```sql
CREATE PLACEMENT POLICY p1 FOLLOWERS=4;
CREATE TABLE t1 (a INT PRIMARY KEY) PLACEMENT POLICY=p1;
DROP PLACEMENT POLICY p1;  -- This statement fails because the placement policy p1 is referenced.

-- Finds which tables and partitions reference the placement policy.
SELECT table_schema, table_name FROM information_schema.tables WHERE tidb_placement_policy_name='p1';
SELECT table_schema, table_name FROM information_schema.partitions WHERE tidb_placement_policy_name='p1';

ALTER TABLE t1 PLACEMENT POLICY=default;  -- Removes the placement policy from t1.
DROP PLACEMENT POLICY p1;  -- Succeeds.
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

## MySQL 互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [SQL の配置ルール](/placement-rules-in-sql.md)
-   [表示配置](/sql-statements/sql-statement-show-placement.md)
-   [配置ポリシーの作成](/sql-statements/sql-statement-create-placement-policy.md)
-   [配置ポリシーの変更](/sql-statements/sql-statement-alter-placement-policy.md)
