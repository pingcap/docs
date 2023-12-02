---
title: TIKV_REGION_STATUS
summary: Learn the `TIKV_REGION_STATUS` information_schema table.
---

# TIKV_REGION_STATUS {#tikv-region-status}

`TIKV_REGION_STATUS`の表は、リージョンID、開始および終了の Key-Value、読み取りおよび書き込みトラフィックなど、PD の API を介した TiKV リージョンの基本情報を示しています。

> **注記：**
>
> このテーブルは[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターでは使用できません。

```sql
USE information_schema;
DESC tikv_region_status;
```

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
| EPOCH_CONF_VER            | bigint(21)  | YES  |      | NULL    |       |
| EPOCH_VERSION             | bigint(21)  | YES  |      | NULL    |       |
| WRITTEN_BYTES             | bigint(21)  | YES  |      | NULL    |       |
| READ_BYTES                | bigint(21)  | YES  |      | NULL    |       |
| APPROXIMATE_SIZE          | bigint(21)  | YES  |      | NULL    |       |
| APPROXIMATE_KEYS          | bigint(21)  | YES  |      | NULL    |       |
| REPLICATIONSTATUS_STATE   | varchar(64) | YES  |      | NULL    |       |
| REPLICATIONSTATUS_STATEID | bigint(21)  | YES  |      | NULL    |       |
+---------------------------+-------------+------+------+---------+-------+
17 rows in set (0.00 sec)
```

`TIKV_REGION_STATUS`の表の列の説明は次のとおりです。

-   `REGION_ID` :リージョンの ID。
-   `START_KEY` :リージョンの開始キーの値。
-   `END_KEY` :リージョンの終了キーの値。
-   `TABLE_ID` :リージョンが属するテーブルの ID。
-   `DB_NAME` : `TABLE_ID`が属するデータベースの名前。
-   `TABLE_NAME` :リージョンが属するテーブルの名前。
-   `IS_INDEX` :リージョンデータがインデックスであるかどうか。 0 はインデックスではないことを意味し、1 はインデックスであることを意味します。現在のリージョンにテーブル データとインデックス データの両方が含まれている場合、複数のレコード行が存在し、 `IS_INDEX`はそれぞれ 0 と 1 になります。
-   `INDEX_ID` :リージョンが属するインデックスの ID。 `IS_INDEX`が 0 の場合、この列の値は NULL になります。
-   `INDEX_NAME` :リージョンが属するインデックスの名前。 `IS_INDEX`が 0 の場合、この列の値は NULL になります。
-   `EPOCH_CONF_VER` :リージョン構成のバージョン番号。バージョン番号は、ピアが追加または削除されると増加します。
-   `EPOCH_VERSION` :リージョンの現在のバージョン番号。バージョン番号は、リージョンが分割または結合されると増加します。
-   `WRITTEN_BYTES` :リージョンに書き込まれるデータの量 (バイト)。
-   `READ_BYTES` :リージョンから読み取られたデータの量 (バイト)。
-   `APPROXIMATE_SIZE` :リージョンのおおよそのデータ サイズ (MB)。
-   `APPROXIMATE_KEYS` :リージョン内のキーのおおよその数。
-   `REPLICATIONSTATUS_STATE` :リージョンの現在のレプリケーション ステータス。ステータスは`UNKNOWN` 、 `SIMPLE_MAJORITY` 、または`INTEGRITY_OVER_LABEL`です。
-   `REPLICATIONSTATUS_STATEID` : `REPLICATIONSTATUS_STATE`に対応する識別子。

また、 `EPOCH_CONF_VER` 、 `WRITTEN_BYTES`および`READ_BYTES`列に対する`ORDER BY X LIMIT Y`操作を介して、 pd-ctl で`top confver` 、 `top read` 、および`top write`操作を実装することもできます。

次の SQL ステートメントを使用して、書き込みデータが最も多い上位 3 つのリージョンをクエリできます。

```sql
SELECT * FROM tikv_region_status ORDER BY written_bytes DESC LIMIT 3;
```
