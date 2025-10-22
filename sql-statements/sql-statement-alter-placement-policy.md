---
title: ALTER PLACEMENT POLICY
summary: TiDB での ALTER PLACEMENT POLICY の使用法。
---

# 配置ポリシーの変更 {#alter-placement-policy}

`ALTER PLACEMENT POLICY` 、以前に作成された既存の配置ポリシーを変更するために使用されます。この配置ポリシーを使用するすべてのテーブルとパーティションが自動的に更新されます。

> **注記：**
>
> この機能は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では利用できません。

`ALTER PLACEMENT POLICY`以前のポリシーを新しい定義に*置き換えます*。古いポリシーと新しいポリシーはマージ*され*ません。次の例では、 `ALTER PLACEMENT POLICY`実行すると`FOLLOWERS=4`失われます。

```sql
CREATE PLACEMENT POLICY p1 FOLLOWERS=4;
ALTER PLACEMENT POLICY p1 PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1";
```

## 概要 {#synopsis}

```ebnf+diagram
AlterPolicyStmt ::=
    "ALTER" "PLACEMENT" "POLICY" IfExists PolicyName PlacementOptionList

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

## 例 {#examples}

> **注記：**
>
> クラスターで使用可能なリージョンを確認するには、 [`SHOW PLACEMENT LABELS`](/sql-statements/sql-statement-show-placement-labels.md)参照してください。
>
> 利用可能なリージョンが表示されない場合は、TiKV インストールでラベルが正しく設定されていない可能性があります。

```sql
CREATE PLACEMENT POLICY p1 PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1";
CREATE TABLE t1 (i INT) PLACEMENT POLICY=p1; -- Assign policy p1 to table t1
ALTER PLACEMENT POLICY p1 PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1,us-west-2" FOLLOWERS=4; -- The rules of t1 will be updated automatically.
SHOW CREATE PLACEMENT POLICY p1\G
```

    Query OK, 0 rows affected (0.08 sec)

    Query OK, 0 rows affected (0.10 sec)

    ***************************[ 1. row ]***************************
    Policy        | p1
    Create Policy | CREATE PLACEMENT POLICY `p1` PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1,us-west-2" FOLLOWERS=4
    1 row in set (0.00 sec)

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [SQLの配置ルール](/placement-rules-in-sql.md)
-   [表示配置](/sql-statements/sql-statement-show-placement.md)
-   [配置ポリシーの作成](/sql-statements/sql-statement-create-placement-policy.md)
-   [ドロップ配置ポリシー](/sql-statements/sql-statement-drop-placement-policy.md)
