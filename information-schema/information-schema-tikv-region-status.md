---
title: TIKV_REGION_STATUS
summary: TIKV_REGION_STATUS`情報スキーマテーブルについて学習してください。
---

# TIKV_REGION_STATUS {#tikv-region-status}

`TIKV_REGION_STATUS`テーブルには、PD の API を介して TiKV リージョンに関する基本的な情報が表示されます。これには、リージョンID、開始および終了キー値、読み取りおよび書き込みトラフィックなどが含まれます。

> **注記：**
>
> このテーブルは、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスでは利用できません。

```sql
USE INFORMATION_SCHEMA;
DESC TIKV_REGION_STATUS;
```

出力は以下のとおりです。

```sql
+---------------------------+-------------+------+------+---------+-------+
| Field                     | Type        | Null | Key  | Default | Extra |
+---------------------------+-------------+------+------+---------+-------+
| REGION_ID                 | bigint(21)  | YES  |      | NULL    |       |
| START_KEY                 | text        | YES  |      | NULL    |       |
| END_KEY                   | text        | YES  |      | NULL    |       |
| TABLE_ID                  | bigint(21)  | YES  |      | NULL    |       |
| DB_NAME                   | varchar(64) | YES  |      | NULL    |       |
| TABLE_NAME                | varchar(64) | YES  |      | NULL    |       |
| IS_INDEX                  | tinyint(1)  | NO   |      | 0       |       |
| INDEX_ID                  | bigint(21)  | YES  |      | NULL    |       |
| INDEX_NAME                | varchar(64) | YES  |      | NULL    |       |
| IS_PARTITION              | tinyint(1)  | NO   |      | 0       |       |
| PARTITION_ID              | bigint(21)  | YES  |      | NULL    |       |
| PARTITION_NAME            | varchar(64) | YES  |      | NULL    |       |
| EPOCH_CONF_VER            | bigint(21)  | YES  |      | NULL    |       |
| EPOCH_VERSION             | bigint(21)  | YES  |      | NULL    |       |
| WRITTEN_BYTES             | bigint(21)  | YES  |      | NULL    |       |
| READ_BYTES                | bigint(21)  | YES  |      | NULL    |       |
| APPROXIMATE_SIZE          | bigint(21)  | YES  |      | NULL    |       |
| APPROXIMATE_KEYS          | bigint(21)  | YES  |      | NULL    |       |
| REPLICATIONSTATUS_STATE   | varchar(64) | YES  |      | NULL    |       |
| REPLICATIONSTATUS_STATEID | bigint(21)  | YES  |      | NULL    |       |
+---------------------------+-------------+------+------+---------+-------+
20 rows in set (0.00 sec)
```

`TIKV_REGION_STATUS`テーブルの列の説明は以下のとおりです。

-   `REGION_ID` :リージョンの ID 。
-   `START_KEY` :リージョンの開始キーの値。
-   `END_KEY` :リージョンの終了キーの値。
-   `TABLE_ID` :リージョンが属するテーブルのID。
-   `DB_NAME` : `TABLE_ID`が属するデータベースの名前。
-   `TABLE_NAME` :リージョンが属するテーブルの名前。
-   `IS_INDEX` :リージョンデータがインデックスであるかどうか。0 はインデックスではないことを意味し、1 はインデックスであることを意味します。現在のリージョンにテーブルデータとインデックスデータの両方が含まれている場合、レコードの行が複数になり、 `IS_INDEX`はそれぞれ 0 と 1 になります。
-   `INDEX_ID` :リージョンが属するインデックスのID。 `IS_INDEX`が 0 の場合、この列の値は NULL になります。
-   `INDEX_NAME` :リージョンが属するインデックスの名前。 `IS_INDEX`が 0 の場合、この列の値は NULL になります。
-   `IS_PARTITION` :リージョンが属するテーブルがパーティション化されているかどうか。
-   `PARTITION_ID` :リージョンが属するテーブルがパーティション化されている場合、この列にはリージョンが属するパーティションの ID が表示されます。
-   `PARTITION_NAME` :リージョンが属するテーブルがパーティション化されている場合、この列にはリージョンが属するパーティションの名前が表示されます。
-   `EPOCH_CONF_VER` :リージョン構成のバージョン番号。ピアが追加または削除されると、バージョン番号が増加します。
-   `EPOCH_VERSION` :リージョンの現在のバージョン番号。リージョンが分割または統合されると、バージョン番号が増加します。
-   `WRITTEN_BYTES` :リージョンに書き込まれたデータ量（バイト）。
-   `READ_BYTES` :リージョンから読み取られたデータ量（バイト）。
-   `APPROXIMATE_SIZE` :リージョンのおおよそのデータサイズ (MB)。
-   `APPROXIMATE_KEYS` :リージョン内のキーのおおよその数。
-   `REPLICATIONSTATUS_STATE` :リージョンの現在のレプリケーション状態。状態は`UNKNOWN` 、 `SIMPLE_MAJORITY` 、または`INTEGRITY_OVER_LABEL`のいずれかになります。
-   `REPLICATIONSTATUS_STATEID` : `REPLICATIONSTATUS_STATE`に対応する識別子。

また、 `top confver` 、 `top read` 、 `top write`操作を、 `ORDER BY X LIMIT Y` `EPOCH_CONF_VER`列に対する`WRITTEN_BYTES`操作によって`READ_BYTES` 。

以下のSQL文を使用すると、書き込みデータが最も多い上位3つのリージョンを照会できます。

```sql
SELECT * FROM tikv_region_status ORDER BY written_bytes DESC LIMIT 3;
```
