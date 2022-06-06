---
title: ALTER PLACEMENT POLICY
summary: The usage of ALTER PLACEMENT POLICY in TiDB.
---

# 配置ポリシーの変更 {#alter-placement-policy}

> **警告：**
>
> SQLの配置ルールは実験的機能です。 GAの前に構文が変更される可能性があり、バグもある可能性があります。
>
> リスクを理解している場合は、 `SET GLOBAL tidb_enable_alter_placement = 1;`を実行することでこの実験機能を有効にできます。

`ALTER PLACEMENT POLICY`は、以前に作成された既存の配置ポリシーを変更するために使用されます。配置ポリシーを使用するすべてのテーブルとパーティションは自動的に更新されます。

## あらすじ {#synopsis}

```ebnf+diagram
AlterPolicyStmt ::=
    "ALTER" "PLACEMENT" "POLICY" IfExists PolicyName PlacementOptionList

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

## 例 {#examples}

> **ノート：**
>
> クラスタで使用可能なリージョンを確認するには、 [`SHOW PLACEMENT LABELS`](/sql-statements/sql-statement-show-placement-labels.md)を参照してください。
>
> 使用可能なリージョンが表示されない場合は、TiKVインストールでラベルが正しく設定されていない可能性があります。

{{< copyable "" >}}

```sql
CREATE PLACEMENT POLICY p1 PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1";
ALTER PLACEMENT POLICY p1 PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1,us-west-2" FOLLOWERS=4;
SHOW CREATE PLACEMENT POLICY p1\G
```

```
Query OK, 0 rows affected (0.08 sec)

Query OK, 0 rows affected (0.10 sec)

*************************** 1. row ***************************
       Policy: p1
Create Policy: CREATE PLACEMENT POLICY `p1` PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1,us-west-2" FOLLOWERS=4
1 row in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文のTiDB拡張です。

## も参照してください {#see-also}

-   [SQLの配置ルール](/placement-rules-in-sql.md)
-   [配置を表示](/sql-statements/sql-statement-show-placement.md)
-   [プレースメントポリシーを作成する](/sql-statements/sql-statement-create-placement-policy.md)
-   [ドロッププレースメントポリシー](/sql-statements/sql-statement-drop-placement-policy.md)
