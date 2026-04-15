---
title: ALTER PLACEMENT POLICY
summary: TiDBにおけるALTER PLACEMENT POLICYの使用方法。
---

# 配置方針の変更 {#alter-placement-policy}

`ALTER PLACEMENT POLICY`は、既に作成済みの配置ポリシーを変更するために使用されます。この配置ポリシーを使用するすべてのテーブルとパーティションは自動的に更新されます。

> **注記：**
>
> この機能は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスではご利用いただけません。

`ALTER PLACEMENT POLICY`以前のポリシーを新しい定義に*置き換えます*。古いポリシーと新しいポリシー*をマージするわけ*ではありません。次の例では、 `FOLLOWERS=4`が実行されると、 `ALTER PLACEMENT POLICY`は失われます。

```sql
CREATE PLACEMENT POLICY p1 FOLLOWERS=4;
ALTER PLACEMENT POLICY p1 PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1";
```

## あらすじ {#synopsis}

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
> クラスターで使用可能なリージョンを確認するには、 [`SHOW PLACEMENT LABELS`](/sql-statements/sql-statement-show-placement-labels.md)を参照してください。
>
> 利用可能なリージョンが表示されない場合は、TiKVのインストール時にラベルが正しく設定されていない可能性があります。

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

## MySQLとの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文に対するTiDBの拡張機能です。

## 関連項目 {#see-also}

-   [SQLにおける配置ルール](/placement-rules-in-sql.md)
-   [番組掲載](/sql-statements/sql-statement-show-placement.md)
-   [配置ポリシーを作成する](/sql-statements/sql-statement-create-placement-policy.md)
-   [ドロップ配置ポリシー](/sql-statements/sql-statement-drop-placement-policy.md)
