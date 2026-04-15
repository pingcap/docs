---
title: SHOW CREATE PLACEMENT POLICY
summary: TiDBにおけるSHOW CREATE PLACEMENT POLICYの使用方法。
---

# 表示・作成・配置ポリシー {#show-create-placement-policy}

`SHOW CREATE PLACEMENT POLICY`配置ポリシーの定義を表示するために使用されます。これを使用すると、現在の配置ポリシーの定義を確認し、別の TiDB クラスタでそれを再現できます。

> **注記：**
>
> この機能は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスではご利用いただけません。

## あらすじ {#synopsis}

```ebnf+diagram
ShowCreatePlacementPolicyStmt ::=
    "SHOW" "CREATE" "PLACEMENT" "POLICY" PolicyName

PolicyName ::=
    Identifier
```

## 例 {#examples}

```sql
CREATE PLACEMENT POLICY p1 PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4;
CREATE TABLE t1 (a INT) PLACEMENT POLICY=p1;
SHOW CREATE PLACEMENT POLICY p1\G
```

    Query OK, 0 rows affected (0.08 sec)

    Query OK, 0 rows affected (0.10 sec)

    ***************************[ 1. row ]***************************
    Policy        | p1
    Create Policy | CREATE PLACEMENT POLICY `p1` PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4
    1 row in set (0.00 sec)

## MySQLとの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文に対するTiDBの拡張機能です。

## 関連項目 {#see-also}

-   [SQLにおける配置ルール](/placement-rules-in-sql.md)
-   [番組掲載](/sql-statements/sql-statement-show-placement.md)
-   [配置ポリシーを作成する](/sql-statements/sql-statement-create-placement-policy.md)
-   [配置方針の変更](/sql-statements/sql-statement-alter-placement-policy.md)
-   [ドロップ配置ポリシー](/sql-statements/sql-statement-drop-placement-policy.md)
