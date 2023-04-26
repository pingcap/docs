---
title: TIKV_STORE_STATUS
summary: Learn the `TIKV_STORE_STATUS` INFORMATION_SCHEMA table.
---

# TIKV_STORE_STATUS {#tikv-store-status}

`TIKV_STORE_STATUS`テーブルは、PD の API を介して TiKV ノードのいくつかの基本情報を示します。たとえば、クラスターに割り当てられた ID、アドレスとポート、ステータス、容量、現在のノードのリージョンリーダーの数などです。

```sql
USE INFORMATION_SCHEMA;
DESC TIKV_STORE_STATUS;
```

出力は次のとおりです。

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

`TIKV_STORE_STATUS`テーブルの列の説明は次のとおりです。

-   `STORE_ID` : ストアの ID。
-   `ADDRESS` : ストアのアドレス。
-   `STORE_STATE` : `STORE_STATE_NAME`に対応する Store 状態の識別子。
-   `STORE_STATE_NAME` : Store 状態の名前。名前は`Up` 、 `Offline` 、または`Tombstone`です。
-   `LABEL` : ストアに設定されたラベル。
-   `VERSION` : ストアのバージョン番号。
-   `CAPACITY` : ストアのstorage容量。
-   `AVAILABLE` : ストアの残りのstorage容量。
-   `LEADER_COUNT` : ストアのリーダーの数。
-   `LEADER_WEIGHT` : ストアのリーダーの重み。
-   `LEADER_SCORE` : ストアのリーダー スコア。
-   `LEADER_SIZE` : ストアにあるすべてのリーダーのおおよその合計データ サイズ (MB)。
-   `REGION_COUNT` : ストアのリージョン数。
-   `REGION_WEIGHT` : ストアのリージョンの重み。
-   `REGION_SCORE` : ストアのリージョンスコア。
-   `REGION_SIZE` : ストアのすべてのリージョンのおおよその合計データ サイズ (MB)。
-   `START_TS` : ストアが開始されたときのタイムスタンプ。
-   `LAST_HEARTBEAT_TS` : ストアによって送信された最後のハートビートのタイムスタンプ。
-   `UPTIME` : ストアが開始してからの合計時間。
