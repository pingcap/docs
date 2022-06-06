---
title: TIKV_REGION_STATUS
summary: Learn the `TIKV_REGION_STATUS` information_schema table.
---

# TIKV_REGION_STATUS {#tikv-region-status}

`TIKV_REGION_STATUS`の表は、リージョンID、開始キー値と終了キー値、読み取りおよび書き込みトラフィックなど、PDのAPIを介したTiKVリージョンの基本情報を示しています。

{{< copyable "" >}}

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

`TIKV_REGION_STATUS`表の列の説明は次のとおりです。

-   `REGION_ID` ：リージョンのID。
-   `START_KEY` ：リージョンの開始キーの値。
-   `END_KEY` ：リージョンのエンドキーの値。
-   `TABLE_ID` ：リージョンが属するテーブルのID。
-   `DB_NAME` ： `TABLE_ID`が属するデータベースの名前。
-   `TABLE_NAME` ：リージョンが属するテーブルの名前。
-   `IS_INDEX` ：地域データがインデックスかどうか。 0はインデックスではないことを意味し、1はインデックスであることを意味します。現在のリージョンにテーブルデータとインデックスデータの両方が含まれている場合、レコードの複数の行があり、 `IS_INDEX`はそれぞれ0と1です。
-   `INDEX_ID` ：リージョンが属するインデックスのID。 `IS_INDEX`が0の場合、この列の値はNULLです。
-   `INDEX_NAME` ：リージョンが属するインデックスの名前。 `IS_INDEX`が0の場合、この列の値はNULLです。
-   `EPOCH_CONF_VER` ：リージョン構成のバージョン番号。ピアが追加または削除されると、バージョン番号が増加します。
-   `EPOCH_VERSION` ：リージョンの現在のバージョン番号。リージョンが分割またはマージされると、バージョン番号が増加します。
-   `WRITTEN_BYTES` ：リージョンに書き込まれるデータの量（バイト）。
-   `READ_BYTES` ：リージョンから読み取られたデータの量（バイト）。
-   `APPROXIMATE_SIZE` ：リージョンのおおよそのデータサイズ（MB）。
-   `APPROXIMATE_KEYS` ：リージョン内のキーのおおよその数。
-   `REPLICATIONSTATUS_STATE` ：リージョンの現在のレプリケーションステータス。ステータスは`UNKNOWN` 、または`SIMPLE_MAJORITY`の場合があり`INTEGRITY_OVER_LABEL` 。
-   `REPLICATIONSTATUS_STATEID` ： `REPLICATIONSTATUS_STATE`に対応する識別子。

また、 `ORDER BY X LIMIT Y` `WRITTEN_BYTES` `top write` `top confver` `top read`実装`READ_BYTES` `EPOCH_CONF_VER` 。

次のSQLステートメントを使用して、書き込みデータが最も多い上位3つのリージョンをクエリできます。

```sql
SELECT * FROM tikv_region_status ORDER BY written_bytes DESC LIMIT 3;
```
