---
title: CREATE PLACEMENT POLICY
summary: TiDB での CREATE PLACEMENT POLICY の使用法。
---

# 配置ポリシーの作成 {#create-placement-policy}

`CREATE PLACEMENT POLICY` 、後でテーブル、パーティション、またはデータベース スキーマに割り当てることができる名前付き配置ポリシーを作成するために使用されます。

> **注記：**
>
> この機能は[{{{ .スターター }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)クラスターでは利用できません。

## 概要 {#synopsis}

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
> クラスターで使用可能なリージョンを確認するには、 [`SHOW PLACEMENT LABELS`](/sql-statements/sql-statement-show-placement-labels.md)参照してください。
>
> 利用可能なリージョンが表示されない場合は、TiKV インストールでラベルが正しく設定されていない可能性があります。

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

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [SQLの配置ルール](/placement-rules-in-sql.md)
-   [表示配置](/sql-statements/sql-statement-show-placement.md)
-   [配置ポリシーの変更](/sql-statements/sql-statement-alter-placement-policy.md)
-   [ドロップ配置ポリシー](/sql-statements/sql-statement-drop-placement-policy.md)
