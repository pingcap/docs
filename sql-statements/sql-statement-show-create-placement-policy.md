---
title: SHOW CREATE PLACEMENT POLICY
summary: The usage of SHOW CREATE PLACEMENT POLICY in TiDB.
---

# プレースメントポリシーの作成を表示 {#show-create-placement-policy}

`SHOW CREATE PLACEMENT POLICY`は、配置ポリシーの定義を示すために使用されます。これを使用して、配置ポリシーの現在の定義を確認し、別のTiDBクラスタで再作成できます。

## あらすじ {#synopsis}

```ebnf+diagram
ShowCreatePlacementPolicyStmt ::=
    "SHOW" "CREATE" "PLACEMENT" "POLICY" PolicyName

PolicyName ::=
    Identifier
```

## 例 {#examples}

{{< copyable "" >}}

```sql
CREATE PLACEMENT POLICY p1 PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4;
CREATE TABLE t1 (a INT) PLACEMENT POLICY=p1;
SHOW CREATE PLACEMENT POLICY p1\G;
```

```
Query OK, 0 rows affected (0.08 sec)

Query OK, 0 rows affected (0.10 sec)

***************************[ 1. row ]***************************
Policy        | p1
Create Policy | CREATE PLACEMENT POLICY `p1` PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4
1 row in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文のTiDB拡張です。

## も参照してください {#see-also}

-   [SQLの配置ルール](/placement-rules-in-sql.md)
-   [配置を表示](/sql-statements/sql-statement-show-placement.md)
-   [プレースメントポリシーを作成する](/sql-statements/sql-statement-create-placement-policy.md)
-   [配置ポリシーの変更](/sql-statements/sql-statement-alter-placement-policy.md)
-   [ドロッププレースメントポリシー](/sql-statements/sql-statement-drop-placement-policy.md)
