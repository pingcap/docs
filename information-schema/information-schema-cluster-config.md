---
title: CLUSTER_CONFIG
summary: Learn the `CLUSTER_CONFIG` information_schema table.
---

# クラスター構成 {#cluster-config}

`CLUSTER_CONFIG`クラスター構成テーブルを使用して、クラスター内のすべてのサーバーコンポーネントの現在の構成を取得できます。これにより、同様の情報を取得するには各インスタンスの HTTP API エンドポイントにアクセスする必要があった TiDB の以前のリリースよりも使用法が簡素化されます。

> **注記：**
>
> このテーブルは TiDB セルフホスト型にのみ適用され、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)では使用できません。

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

フィールドの説明:

-   `TYPE` : インスタンスのタイプ。オプションの値は`tidb` 、 `pd` 、および`tikv`です。
-   `INSTANCE` : インスタンスのサービスアドレス。
-   `KEY` : 設定項目名。
-   `VALUE` : 設定項目の値。

次の例は、 `CLUSTER_CONFIG`テーブルを使用して TiKV インスタンスの`coprocessor`構成をクエリする方法を示しています。

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
