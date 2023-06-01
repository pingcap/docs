---
title: SHOW CREATE RESOURCE GROUP
summary: Learn the usage of SHOW CREATE RESOURCE GROUP in TiDB.
---

# 表示 リソースグループの作成 {#show-create-resource-group}

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> この機能は[Serverless Tierクラスター](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)では使用できません。

</CustomContent>

`SHOW CREATE RESOURCE GROUP`ステートメントを使用すると、リソース グループの現在の定義を表示できます。

## あらすじ {#synopsis}

```ebnf+diagram
ShowCreateResourceGroupStmt ::=
    "SHOW" "CREATE" "RESOURCE" "GROUP" ResourceGroupName

ResourceGroupName ::=
    Identifier
```

## 例 {#examples}

リソース グループを作成します`rg1` 。

```sql
CREATE RESOURCE GROUP rg1 RU_PER_SEC=100;
Query OK, 0 rows affected (0.10 sec)
```

`rg1`の定義をビュー。

```sql
SHOW CREATE RESOURCE GROUP rg1;
***************************[ 1. row ]***************************
+----------------+------------------------------------------------------------+
| Resource_Group | Create Resource Group                                      |
+----------------+------------------------------------------------------------+
| rg1            | CREATE RESOURCE GROUP `rg1` RU_PER_SEC=100 PRIORITY=MEDIUM |
+----------------+------------------------------------------------------------+
1 row in set (0.01 sec)
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL の TiDB 拡張機能です。

## こちらも参照 {#see-also}

-   [TiDB リソース制御](/tidb-resource-control.md)
-   [リソースグループの作成](/sql-statements/sql-statement-alter-resource-group.md)
-   [リソースグループの変更](/sql-statements/sql-statement-alter-resource-group.md)
-   [リソースグループを削除](/sql-statements/sql-statement-drop-resource-group.md)
