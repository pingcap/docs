---
title: RESOURCE_GROUPS
summary: RESOURCE_GROUPS` information_schema テーブルについて学習します。
---

# リソースグループ {#resource-groups}

`RESOURCE_GROUPS`表には、すべてのリソース グループに関する情報が表示されます。詳細については、 [リソース制御を使用してリソースの分離を実現する](/tidb-resource-control.md)参照してください。

> **注記：**
>
> このテーブルは[TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)クラスターでは使用できません。

```sql
USE information_schema;
DESC resource_groups;
```

```sql
+------------+-------------+------+------+---------+-------+
| Field      | Type        | Null | Key  | Default | Extra |
+------------+-------------+------+------+---------+-------+
| NAME       | varchar(32) | NO   |      | NULL    |       |
| RU_PER_SEC | bigint(21)  | YES  |      | NULL    |       |
| PRIORITY   | varchar(6)  | YES  |      | NULL    |       |
| BURSTABLE  | varchar(3)  | YES  |      | NULL    |       |
+------------+-------------+------+------+---------+-------+
3 rows in set (0.00 sec)
```

## 例 {#examples}

```sql
SELECT * FROM information_schema.resource_groups; -- View all resource groups. TiDB has a `default` resource group.
```

```sql
+---------+------------+----------+-----------+
| NAME    | RU_PER_SEC | PRIORITY | BURSTABLE |
+---------+------------+----------+-----------+
| default | UNLIMITED  | MEDIUM   | YES       |
+---------+------------+----------+-----------+
```

```sql
CREATE RESOURCE GROUP rg1 RU_PER_SEC=1000; -- Create a resource group `rg1`
```

```sql
Query OK, 0 rows affected (0.34 sec)
```

```sql
SHOW CREATE RESOURCE GROUP rg1; -- Show the definition of the `rg1` resource group
```

```sql
+----------------+---------------------------------------------------------------+
| Resource_Group | Create Resource Group                                         |
+----------------+---------------------------------------------------------------+
| rg1            | CREATE RESOURCE GROUP `rg1` RU_PER_SEC=1000 PRIORITY="MEDIUM" |
+----------------+---------------------------------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT * FROM information_schema.resource_groups WHERE NAME = 'rg1'; -- View the resource groups `rg1`
```

```sql
+------+------------+----------+-----------+-------------+
| NAME | RU_PER_SEC | PRIORITY | BURSTABLE | QUERY_LIMIT |
+------+------------+----------+-----------+-------------+
| rg1  | 1000       | MEDIUM   | NO        | NULL        |
+------+------------+----------+-----------+-------------+
1 row in set (0.00 sec)
```

`RESOURCE_GROUPS`の表の列の説明は次のとおりです。

-   `NAME` : リソース グループの名前。
-   `RU_PER_SEC` : リソース グループのバックフィル速度。単位は RU/秒で、RU は[リクエストユニット](/tidb-resource-control.md#what-is-request-unit-ru)意味します。
-   `PRIORITY` : TiKV で処理されるタスクの絶対的な優先度。 `PRIORITY`設定に従って、さまざまなリソースがスケジュールされます。 `PRIORITY`が高いタスクが最初にスケジュールされます。 `PRIORITY`が同じリソース グループの場合、タスクは`RU_PER_SEC`構成に従って比例してスケジュールされます。 `PRIORITY`が指定されていない場合、デフォルトの優先度は`MEDIUM`です。
-   `BURSTABLE` : リソース グループが利用可能なシステム リソースを過剰に使用することを許可するかどうか。

> **注記：**
>
> TiDB は、クラスターの初期化中に`default`リソース グループを自動的に作成します。このリソース グループの場合、デフォルト値は`RU_PER_SEC`で、 `UNLIMITED` ( `INT`タイプの最大値である`2147483647`に相当) であり、 `BURSTABLE`モードです。どのリソース グループにもバインドされていないすべてのリクエストは、この`default`リソース グループに自動的にバインドされます。別のリソース グループに新しい構成を作成する場合は、必要に応じて`default`リソース グループの構成を変更することをお勧めします。
