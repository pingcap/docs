---
title: SHOW CREATE RESOURCE GROUP
summary: TiDBにおけるSHOW CREATE RESOURCE GROUPの使い方を学びましょう。
---

# リソースグループの作成と表示 {#show-create-resource-group}

`SHOW CREATE RESOURCE GROUP`ステートメントを使用すると、リソース グループの現在の定義を表示できます。

> **注記：**
>
> この機能は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスではご利用いただけません。

## あらすじ {#synopsis}

```ebnf+diagram
ShowCreateResourceGroupStmt ::=
    "SHOW" "CREATE" "RESOURCE" "GROUP" ResourceGroupName

ResourceGroupName ::=
    Identifier
|   "DEFAULT"
```

## 例 {#examples}

リソースグループ`rg1`を作成します。

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

## MySQLとの互換性 {#mysql-compatibility}

このステートメントは、MySQL 用の TiDB 拡張機能です。

## 関連項目 {#see-also}

-   [TiDBリソース制御](/tidb-resource-control-ru-groups.md)
-   [リソースグループを作成する](/sql-statements/sql-statement-alter-resource-group.md)
-   [アルター・リソース・グループ](/sql-statements/sql-statement-alter-resource-group.md)
-   [リソースグループを削除する](/sql-statements/sql-statement-drop-resource-group.md)
