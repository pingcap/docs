---
title: TIKV_STORE_STATUS
summary: Learn the `TIKV_STORE_STATUS` information_schema table.
---

# TIKV_STORE_STATUS {#tikv-store-status}

`TIKV_STORE_STATUS`の表は、クラスタに割り当てられたID、アドレスとポート、ステータス、容量、現在のノードのリージョンリーダーの数など、PDのAPIを介したTiKVノードの基本情報を示しています。

{{< copyable "" >}}

```sql
USE information_schema;
DESC tikv_store_status;
```

```sql
+-------------------+-------------+------+------+---------+-------+
| Field             | Type        | Null | Key  | Default | Extra |
+-------------------+-------------+------+------+---------+-------+
| STORE_ID          | bigint(21)  | YES  |      | NULL    |       |
| ADDRESS           | varchar(64) | YES  |      | NULL    |       |
| STORE_STATE       | bigint(21)  | YES  |      | NULL    |       |
| STORE_STATE_NAME  | varchar(64) | YES  |      | NULL    |       |
| LABEL             | json        | YES  |      | NULL    |       |
| VERSION           | varchar(64) | YES  |      | NULL    |       |
| CAPACITY          | varchar(64) | YES  |      | NULL    |       |
| AVAILABLE         | varchar(64) | YES  |      | NULL    |       |
| LEADER_COUNT      | bigint(21)  | YES  |      | NULL    |       |
| LEADER_WEIGHT     | double      | YES  |      | NULL    |       |
| LEADER_SCORE      | double      | YES  |      | NULL    |       |
| LEADER_SIZE       | bigint(21)  | YES  |      | NULL    |       |
| REGION_COUNT      | bigint(21)  | YES  |      | NULL    |       |
| REGION_WEIGHT     | double      | YES  |      | NULL    |       |
| REGION_SCORE      | double      | YES  |      | NULL    |       |
| REGION_SIZE       | bigint(21)  | YES  |      | NULL    |       |
| START_TS          | datetime    | YES  |      | NULL    |       |
| LAST_HEARTBEAT_TS | datetime    | YES  |      | NULL    |       |
| UPTIME            | varchar(64) | YES  |      | NULL    |       |
+-------------------+-------------+------+------+---------+-------+
19 rows in set (0.00 sec)
```

`TIKV_STORE_STATUS`表の列の説明は次のとおりです。

-   `STORE_ID` ：ストアのID。
-   `ADDRESS` ：ストアのアドレス。
-   `STORE_STATE` ：ストア状態の識別子`STORE_STATE_NAME`に対応します。
-   `STORE_STATE_NAME` ：ストア状態の名前。名前は`Up` 、または`Offline` `Tombstone` 。
-   `LABEL` ：ストアに設定されたラベル。
-   `VERSION` ：ストアのバージョン番号。
-   `CAPACITY` ：ストアのストレージ容量。
-   `AVAILABLE` ：ストアの残りのストレージスペース。
-   `LEADER_COUNT` ：ストアのリーダーの数。
-   `LEADER_WEIGHT` ：ストアのリーダーの重み。
-   `LEADER_SCORE` ：ストアのリーダースコア。
-   `LEADER_SIZE` ：ストア上のすべてのリーダーのおおよその合計データサイズ（MB）。
-   `REGION_COUNT` ：ストア上のリージョンの数。
-   `REGION_WEIGHT` ：ストアのリージョンの重み。
-   `REGION_SCORE` ：ストアのリージョンスコア。
-   `REGION_SIZE` ：ストア上のすべてのリージョンのおおよその合計データサイズ（MB）。
-   `START_TS` ：ストアが開始されたときのタイムスタンプ。
-   `LAST_HEARTBEAT_TS` ：ストアから送信された最後のハートビートのタイムスタンプ。
-   `UPTIME` ：ストアが開始してからの合計時間。
