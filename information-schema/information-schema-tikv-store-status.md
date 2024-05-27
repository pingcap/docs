---
title: TIKV_STORE_STATUS
summary: TIKV_STORE_STATUS INFORMATION_SCHEMA テーブルについて学習します。
---

# TIKV_ストアステータス {#tikv-store-status}

`TIKV_STORE_STATUS`表には、クラスターに割り当てられた ID、アドレスとポート、現在のノードのステータス、容量、リージョンリーダーの数など、PD の API 経由の TiKV ノードの基本情報が表示されます。

> **注記：**
>
> このテーブルは[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターでは使用できません。

```sql
USE INFORMATION_SCHEMA;
DESC TIKV_STORE_STATUS;
```

出力は次のようになります。

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

-   `STORE_ID` : ストアの ID。
-   `ADDRESS` : ストアのアドレス。
-   `STORE_STATE` : ストア状態の識別子`STORE_STATE_NAME`に対応します。
-   `STORE_STATE_NAME` : ストア状態の名前。名前は`Up` 、 `Offline` 、または`Tombstone`です。
-   `LABEL` : ストアに設定されたラベル。
-   `VERSION` : ストアのバージョン番号。
-   `CAPACITY` : ストアのstorage容量。
-   `AVAILABLE` : ストアの残りのstorage容量。
-   `LEADER_COUNT` : ストアのリーダーの数。
-   `LEADER_WEIGHT` : ストアのリーダーの重み。
-   `LEADER_SCORE` : ストアのリーダースコア。
-   `LEADER_SIZE` : ストア上のすべてのリーダーのおおよその合計データ サイズ (MB)。
-   `REGION_COUNT` : ストア上のリージョンの数。
-   `REGION_WEIGHT` : ストアのリージョンの重み。
-   `REGION_SCORE` : ストアのリージョンスコア。
-   `REGION_SIZE` : ストア上のすべてのリージョンのおおよその合計データ サイズ (MB)。
-   `START_TS` : ストアが開始されたときのタイムスタンプ。
-   `LAST_HEARTBEAT_TS` : ストアから送信された最後のハートビートビートのタイムスタンプ。
-   `UPTIME` : ストアが開始してからの合計時間。
