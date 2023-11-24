---
title: SET RESOURCE GROUP
summary: An overview of the usage of SET RESOURCE GROUP in the TiDB database.
---

# リソースグループの設定 {#set-resource-group}

`SET RESOURCE GROUP`は、現在のセッションのリソース グループを設定するために使用されます。

> **注記：**
>
> この機能は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターでは使用できません。

## あらすじ {#synopsis}

**SetResourceGroupStmt:**

```ebnf+diagram
SetResourceGroupStmt ::=
   "SET" "RESOURCE" "GROUP" ResourceGroupName

ResourceGroupName ::=
   Identifier
```

## 例 {#examples}

ユーザー`user1`を作成し、2 つのリソース グループ`rg1`と`rg2`を作成し、ユーザー`user1`をリソース グループ`rg1`にバインドします。

```sql
CREATE USER 'user1';
CREATE RESOURCE GROUP 'rg1' RU_PER_SEC = 1000;
ALTER USER 'user1' RESOURCE GROUP `rg1`;
```

`user1`を使用してログインし、現在のユーザーにバインドされているリソース グループを表示します。

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

`SET RESOURCE GROUP`を実行して、デフォルトのリソース グループを使用する現在のセッションを指定します。

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

MySQL は[リソースグループの設定](https://dev.mysql.com/doc/refman/8.0/en/set-resource-group.html)もサポートします。ただし、受け入れられるパラメータは TiDB とは異なります。互換性がありません。

## こちらも参照 {#see-also}

-   [リソースグループの作成](/sql-statements/sql-statement-create-resource-group.md)
-   [リソースグループを削除](/sql-statements/sql-statement-drop-resource-group.md)
-   [リソースグループの変更](/sql-statements/sql-statement-alter-resource-group.md)
-   [リソース制御](/tidb-resource-control.md)
