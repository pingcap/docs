---
title: CLUSTER_CONFIG
summary: Learn the `CLUSTER_CONFIG` information_schema table.
---

# CLUSTER_CONFIG {#cluster-config}

`CLUSTER_CONFIG`クラスタ構成テーブルを使用して、クラスタのすべてのサーバーコンポーネントの現在の構成を取得できます。これにより、TiDBの以前のリリースよりも使用が簡素化され、同様の情報を取得するには、各インスタンスのHTTPAPIエンドポイントにアクセスする必要があります。

{{< copyable "" >}}

```sql
USE information_schema;
DESC cluster_config;
```

```sql
+----------+--------------+------+------+---------+-------+
| Field    | Type         | Null | Key  | Default | Extra |
+----------+--------------+------+------+---------+-------+
| TYPE     | varchar(64)  | YES  |      | NULL    |       |
| INSTANCE | varchar(64)  | YES  |      | NULL    |       |
| KEY      | varchar(256) | YES  |      | NULL    |       |
| VALUE    | varchar(128) | YES  |      | NULL    |       |
+----------+--------------+------+------+---------+-------+
```

フィールドの説明：

-   `TYPE` ：インスタンスタイプ。オプションの値は`tidb` 、および`pd` `tikv` 。
-   `INSTANCE` ：インスタンスのサービスアドレス。
-   `KEY` ：構成アイテム名。
-   `VALUE` ：構成アイテムの値。

次の例は、 `CLUSTER_CONFIG`テーブルを使用してTiKVインスタンスの`coprocessor`構成を照会する方法を示しています。

{{< copyable "" >}}

```sql
SELECT * FROM cluster_config WHERE type='tikv' AND `key` LIKE 'coprocessor%';
```

```sql
+------+-----------------+-----------------------------------+---------+
| TYPE | INSTANCE        | KEY                               | VALUE   |
+------+-----------------+-----------------------------------+---------+
| tikv | 127.0.0.1:20165 | coprocessor.batch-split-limit     | 10      |
| tikv | 127.0.0.1:20165 | coprocessor.region-max-keys       | 1440000 |
| tikv | 127.0.0.1:20165 | coprocessor.region-max-size       | 144MiB  |
| tikv | 127.0.0.1:20165 | coprocessor.region-split-keys     | 960000  |
| tikv | 127.0.0.1:20165 | coprocessor.region-split-size     | 96MiB   |
| tikv | 127.0.0.1:20165 | coprocessor.split-region-on-table | false   |
+------+-----------------+-----------------------------------+---------+
6 rows in set (0.00 sec)
```
