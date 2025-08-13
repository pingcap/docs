---
title: DROP RESOURCE GROUP
summary: TiDB での DROP RESOURCE GROUP の使用方法を学習します。
---

# リソースグループの削除 {#drop-resource-group}

`DROP RESOURCE GROUP`ステートメントを使用してリソース グループを削除できます。

> **注記：**
>
> この機能は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では利用できません。

## 概要 {#synopsis}

```ebnf+diagram
DropResourceGroupStmt ::=
    "DROP" "RESOURCE" "GROUP" IfExists ResourceGroupName

IfExists ::=
    ('IF' 'EXISTS')?

ResourceGroupName ::=
    Identifier
|   "DEFAULT"
```

> **注記：**
>
> -   `DROP RESOURCE GROUP`ステートメントは、グローバル変数[`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660) `ON`に設定されている場合にのみ実行できます。
> -   `default`リソース グループは予約されており、削除できません。

## 例 {#examples}

`rg1`という名前のリソース グループを削除します。

```sql
DROP RESOURCE GROUP IF EXISTS rg1;
```

```sql
Query OK, 0 rows affected (0.22 sec)
```

```sql
CREATE RESOURCE GROUP IF NOT EXISTS rg1 RU_PER_SEC = 500 BURSTABLE;
```

```sql
Query OK, 0 rows affected (0.08 sec)
```

```sql
SELECT * FROM information_schema.resource_groups WHERE NAME ='rg1';
```

```sql
+------+------------+----------+-----------+-------------+
| NAME | RU_PER_SEC | PRIORITY | BURSTABLE | QUERY_LIMIT |
+------+------------+----------+-----------+-------------+
| rg1  | 500        | MEDIUM   | YES       | NULL        |
+------+------------+----------+-----------+-------------+
1 row in set (0.01 sec)
```

```sql
DROP RESOURCE GROUP IF EXISTS rg1;
```

```sql
Query OK, 1 rows affected (0.09 sec)
```

    SELECT * FROM information_schema.resource_groups WHERE NAME ='rg1';

```sql
Empty set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

MySQL も[リソースグループの削除](https://dev.mysql.com/doc/refman/8.0/en/drop-resource-group.html)サポートしていますが、 TiDB は`FORCE`パラメータをサポートしていません。

## 参照 {#see-also}

-   [リソースグループの変更](/sql-statements/sql-statement-alter-resource-group.md)
-   [リソースグループの作成](/sql-statements/sql-statement-create-resource-group.md)
-   [リクエストユニット（RU）](/tidb-resource-control-ru-groups.md#what-is-request-unit-ru)
