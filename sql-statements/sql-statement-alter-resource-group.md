---
title: ALTER RESOURCE GROUP
summary: Learn the usage of ALTER RESOURCE GROUP in TiDB.
---

# リソースグループの変更 {#alter-resource-group}

`ALTER RESOURCE GROUP`ステートメントは、データベース内のリソース グループを変更するために使用されます。

> **注記：**
>
> この機能は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターでは使用できません。

## あらすじ {#synopsis}

```ebnf+diagram
AlterResourceGroupStmt ::=
   "ALTER" "RESOURCE" "GROUP" IfExists ResourceGroupName ResourceGroupOptionList

IfExists ::=
    ('IF' 'EXISTS')?

ResourceGroupName ::=
   Identifier

ResourceGroupOptionList ::=
    DirectResourceGroupOption
|   ResourceGroupOptionList DirectResourceGroupOption
|   ResourceGroupOptionList ',' DirectResourceGroupOption

DirectResourceGroupOption ::=
    "RU_PER_SEC" EqOpt stringLit
|   "PRIORITY" EqOpt ResourceGroupPriorityOption
|   "BURSTABLE"
ResourceGroupPriorityOption ::=
    LOW
|   MEDIUM
|   HIGH

```

TiDB は次の`DirectResourceGroupOption`サポートします。ここで[リクエストユニット (RU)](/tidb-resource-control.md#what-is-request-unit-ru) 、CPU、IO、およびその他のシステム リソースに対する TiDB 内の統合抽象化ユニットです。

| オプション        | 説明                                                                                     | 例                                                                  |
| ------------ | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| `RU_PER_SEC` | 1 秒あたりの RU バックフィルの速度                                                                   | `RU_PER_SEC = 500` 、このリソース グループが 1 秒あたり 500 RU でバックフィルされていることを示します |
| `PRIORITY`   | TiKV 上で処理されるタスクの絶対的な優先度                                                                | `PRIORITY = HIGH`優先度が高いことを示します。指定しない場合、デフォルト値は`MEDIUM`です。          |
| `BURSTABLE`  | `BURSTABLE`属性が設定されている場合、TiDB は、クォータを超過したときに、対応するリソース グループが利用可能なシステム リソースを使用することを許可します。 |                                                                    |

> **注記：**
>
> `ALTER RESOURCE GROUP`ステートメントは、グローバル変数[`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660) `ON`に設定されている場合にのみ実行できます。

## 例 {#examples}

`rg1`という名前のリソース グループを作成し、そのプロパティを変更します。

```sql
DROP RESOURCE GROUP IF EXISTS rg1;
```

    Query OK, 0 rows affected (0.22 sec)

```sql
CREATE RESOURCE GROUP IF NOT EXISTS rg1
  RU_PER_SEC = 100
  BURSTABLE;
```

```sql
Query OK, 0 rows affected (0.08 sec)
```

```sql
SELECT * FROM information_schema.resource_groups WHERE NAME ='rg1';
+------+------------+----------+-----------+
| NAME | RU_PER_SEC | PRIORITY | BURSTABLE |
+------+------------+----------+-----------+
| rg1  |       100  | MEDIUM   | YES       |
+------+------------+----------+-----------+
1 rows in set (1.30 sec)
```

```sql
ALTER RESOURCE GROUP rg1
  RU_PER_SEC = 200
  PRIORITY = LOW;
```

```sql
Query OK, 0 rows affected (0.08 sec)
```

```sql
SELECT * FROM information_schema.resource_groups WHERE NAME ='rg1';
```

```sql
+------+------------+----------+-----------+
| NAME | RU_PER_SEC | PRIORITY | BURSTABLE |
+------+------------+----------+-----------+
| rg1  |       200  | LOW      | NO        |
+------+------------+----------+-----------+
1 rows in set (1.30 sec)
```

## MySQLの互換性 {#mysql-compatibility}

MySQL は[リソースグループの変更](https://dev.mysql.com/doc/refman/8.0/en/alter-resource-group.html)もサポートします。ただし、受け入れられるパラメータが TiDB とは異なるため、互換性はありません。

## こちらも参照 {#see-also}

-   [リソースグループを削除](/sql-statements/sql-statement-drop-resource-group.md)
-   [リソースグループの作成](/sql-statements/sql-statement-create-resource-group.md)
-   [リクエストユニット(RU)](/tidb-resource-control.md#what-is-request-unit-ru)
