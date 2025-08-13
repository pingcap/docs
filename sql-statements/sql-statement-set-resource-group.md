---
title: SET RESOURCE GROUP
summary: TiDB データベースでの SET RESOURCE GROUP の使用法の概要。
---

# リソースグループの設定 {#set-resource-group}

`SET RESOURCE GROUP` 、現在のセッションのリソース グループを設定するために使用されます。

> **注記：**
>
> この機能は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では利用できません。

## 概要 {#synopsis}

**リソースグループステートメントの設定:**

```ebnf+diagram
SetResourceGroupStmt ::=
    "SET" "RESOURCE" "GROUP" ResourceGroupName

ResourceGroupName ::=
    Identifier
|   "DEFAULT"
```

## 特権 {#privilege}

このステートメントを実行するには、次の構成と権限が必要です。

1.  システム変数[`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660) `ON`に設定されています。
2.  システム変数[`tidb_resource_control_strict_mode`](/system-variables.md#tidb_resource_control_strict_mode-new-in-v820) `ON`に設定されている場合、 `SUPER` 、 `RESOURCE_GROUP_ADMIN` 、または`RESOURCE_GROUP_USER`権限が必要です。 `OFF`に設定されている場合、これらの権限は必要ありません。

## 例 {#examples}

ユーザー`user1`を作成し、リソース グループ`rg1`と`rg2` 2 つのリソース グループを作成し、ユーザー`user1`リソース グループ`rg1`にバインドします。

```sql
CREATE USER 'user1';
CREATE RESOURCE GROUP 'rg1' RU_PER_SEC = 1000;
ALTER USER 'user1' RESOURCE GROUP `rg1`;
```

ログインして、現在のユーザーにバインドされているリソース グループを表示するには、 `user1`使用します。

```sql
SELECT CURRENT_RESOURCE_GROUP();
```

    +--------------------------+
    | CURRENT_RESOURCE_GROUP() |
    +--------------------------+
    | rg1                      |
    +--------------------------+
    1 row in set (0.00 sec)

`SET RESOURCE GROUP`実行して、現在のセッションのリソース グループを`rg2`に設定します。

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

現在のセッションでデフォルトのリソース グループを使用するように指定するには、 `SET RESOURCE GROUP`実行します。

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

## MySQLの互換性 {#mysql-compatibility}

MySQLも[リソースグループの設定](https://dev.mysql.com/doc/refman/8.0/en/set-resource-group.html)サポートしています。ただし、受け入れられるパラメータはTiDBとは異なります。互換性はありません。

## 参照 {#see-also}

-   [リソースグループの作成](/sql-statements/sql-statement-create-resource-group.md)
-   [リソースグループの削除](/sql-statements/sql-statement-drop-resource-group.md)
-   [リソースグループの変更](/sql-statements/sql-statement-alter-resource-group.md)
-   [リソース管理](/tidb-resource-control-ru-groups.md)
