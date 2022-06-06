---
title: CREATE PLACEMENT POLICY
summary: The usage of CREATE PLACEMENT POLICY in TiDB.
---

# プレースメントポリシーを作成する {#create-placement-policy}

> **警告：**
>
> SQLの配置ルールは実験的機能です。 GAの前に構文が変更される可能性があり、バグもある可能性があります。
>
> リスクを理解している場合は、 `SET GLOBAL tidb_enable_alter_placement = 1;`を実行することでこの実験機能を有効にできます。

`CREATE PLACEMENT POLICY`は、後でテーブル、パーティション、またはデータベーススキーマに割り当てることができる名前付き配置ポリシーを作成するために使用されます。

## あらすじ {#synopsis}

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

## 例 {#examples}

> **ノート：**
>
> クラスタで使用可能なリージョンを確認するには、 [`SHOW PLACEMENT LABELS`](/sql-statements/sql-statement-show-placement-labels.md)を参照してください。
>
> 使用可能なリージョンが表示されない場合は、TiKVインストールでラベルが正しく設定されていない可能性があります。

{{< copyable "" >}}

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

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文のTiDB拡張です。

## も参照してください {#see-also}

-   [SQLの配置ルール](/placement-rules-in-sql.md)
-   [配置を表示](/sql-statements/sql-statement-show-placement.md)
-   [配置ポリシーの変更](/sql-statements/sql-statement-alter-placement-policy.md)
-   [ドロッププレースメントポリシー](/sql-statements/sql-statement-drop-placement-policy.md)
