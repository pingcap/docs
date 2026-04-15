---
title: CREATE PLACEMENT POLICY
summary: TiDBにおけるCREATE PLACEMENT POLICYの使用方法。
---

# 配置ポリシーを作成する {#create-placement-policy}

`CREATE PLACEMENT POLICY`後でテーブル、パーティション、またはデータベーススキーマに割り当てることができる名前付き配置ポリシーを作成するために使用されます。

> **注記：**
>
> この機能は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスではご利用いただけません。

## あらすじ {#synopsis}

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

## 例 {#examples}

> **注記：**
>
> クラスターで使用可能なリージョンを確認するには、 [`SHOW PLACEMENT LABELS`](/sql-statements/sql-statement-show-placement-labels.md)を参照してください。
>
> 利用可能なリージョンが表示されない場合は、TiKVのインストール時にラベルが正しく設定されていない可能性があります。

```sql
CREATE PLACEMENT POLICY p1 PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4;
CREATE TABLE t1 (a INT) PLACEMENT POLICY=p1;
SHOW CREATE PLACEMENT POLICY p1;
```

    Query OK, 0 rows affected (0.08 sec)

    Query OK, 0 rows affected (0.10 sec)

    +--------+---------------------------------------------------------------------------------------------------+
    | Policy | Create Policy                                                                                     |
    +--------+---------------------------------------------------------------------------------------------------+
    | p1     | CREATE PLACEMENT POLICY `p1` PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4 |
    +--------+---------------------------------------------------------------------------------------------------+
    1 row in set (0.00 sec)

## MySQLとの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文に対するTiDBの拡張機能です。

## 関連項目 {#see-also}

-   [SQLにおける配置ルール](/placement-rules-in-sql.md)
-   [番組掲載](/sql-statements/sql-statement-show-placement.md)
-   [配置方針の変更](/sql-statements/sql-statement-alter-placement-policy.md)
-   [ドロップ配置ポリシー](/sql-statements/sql-statement-drop-placement-policy.md)
