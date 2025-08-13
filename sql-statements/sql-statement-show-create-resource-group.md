---
title: SHOW CREATE RESOURCE GROUP
summary: TiDB での SHOW CREATE RESOURCE GROUP の使用方法を学習します。
---

# リソースグループの作成を表示 {#show-create-resource-group}

`SHOW CREATE RESOURCE GROUP`ステートメントを使用して、リソース グループの現在の定義を表示できます。

> **注記：**
>
> この機能は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では利用できません。

## 概要 {#synopsis}

```ebnf+diagram
ShowCreateResourceGroupStmt ::=
    "SHOW" "CREATE" "RESOURCE" "GROUP" ResourceGroupName

ResourceGroupName ::=
    Identifier
|   "DEFAULT"
```

## 例 {#examples}

リソース グループ`rg1`を作成します。

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

## 参照 {#see-also}

-   [TiDB リソース制御](/tidb-resource-control-ru-groups.md)
-   [リソースグループの作成](/sql-statements/sql-statement-alter-resource-group.md)
-   [リソースグループの変更](/sql-statements/sql-statement-alter-resource-group.md)
-   [リソースグループの削除](/sql-statements/sql-statement-drop-resource-group.md)
