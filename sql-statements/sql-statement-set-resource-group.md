---
title: SET RESOURCE GROUP
summary: TiDBデータベースにおけるSET RESOURCE GROUPの使用方法の概要。
---

# リソースグループを設定する {#set-resource-group}

`SET RESOURCE GROUP`現在のセッションのリソース グループを設定するために使用されます。

> **注記：**
>
> この機能は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスではご利用いただけません。

## あらすじ {#synopsis}

**SetResourceGroupStmt:**

```ebnf+diagram
SetResourceGroupStmt ::=
    "SET" "RESOURCE" "GROUP" ResourceGroupName

ResourceGroupName ::=
    Identifier
|   "DEFAULT"
```

## 特権 {#privilege}

このステートメントを実行するには、以下の構成と権限が必要です。

1.  システム変数[`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660)は`ON`に設定されています。
2.  システム変数[`tidb_resource_control_strict_mode`](/system-variables.md#tidb_resource_control_strict_mode-new-in-v820) `ON`に設定されている場合、 `SUPER`または`RESOURCE_GROUP_ADMIN`または`RESOURCE_GROUP_USER`の権限が必要です。 `OFF`に設定されている場合、これらの権限は不要です。

## 例 {#examples}

ユーザー`user1`を作成し、2 つのリソース グループ`rg1`と`rg2`を作成し、ユーザー`user1`をリソース グループ`rg1`にバインドします。

```sql
CREATE USER 'user1';
CREATE RESOURCE GROUP 'rg1' RU_PER_SEC = 1000;
ALTER USER 'user1' RESOURCE GROUP `rg1`;
```

`user1`を使用してログインし、現在のユーザーに紐づけられたリソース グループを表示します。

```sql
SELECT CURRENT_RESOURCE_GROUP();
```

    +--------------------------+
    | CURRENT_RESOURCE_GROUP() |
    +--------------------------+
    | rg1                      |
    +--------------------------+
    1 row in set (0.00 sec)

`SET RESOURCE GROUP`を実行して、現在のセッションのリソース グループを`rg2`に設定します。

```sql
SET RESOURCE GROUP `rg2`;
SELECT CURRENT_RESOURCE_GROUP();
```

    +--------------------------+
    | CURRENT_RESOURCE_GROUP() |
    +--------------------------+
    | rg2                      |
    +--------------------------+
    1 row in set (0.00 sec)

`SET RESOURCE GROUP`を実行して、現在のセッションでデフォルトのリソース グループを使用するように指定します。

```sql
SET RESOURCE GROUP `default`;
SELECT CURRENT_RESOURCE_GROUP();
```

```sql
+--------------------------+
| CURRENT_RESOURCE_GROUP() |
+--------------------------+
| default                  |
+--------------------------+
1 row in set (0.00 sec)
```

## MySQLとの互換性 {#mysql-compatibility}

MySQL は[リソースグループを設定する](https://dev.mysql.com/doc/refman/8.0/en/set-resource-group.html)もサポートしています。ただし、受け入れられるパラメータは TiDB とは異なります。互換性がありません。

## 関連項目 {#see-also}

-   [リソースグループを作成する](/sql-statements/sql-statement-create-resource-group.md)
-   [リソースグループを削除する](/sql-statements/sql-statement-drop-resource-group.md)
-   [アルター・リソース・グループ](/sql-statements/sql-statement-alter-resource-group.md)
-   [リソース制御](/tidb-resource-control-ru-groups.md)
