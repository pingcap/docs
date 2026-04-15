---
title: TIKV_STORE_STATUS
summary: TIKV_STORE_STATUS` INFORMATION_SCHEMA テーブルについて学習してください。
---

# TIKV_STORE_STATUS {#tikv-store-status}

`TIKV_STORE_STATUS`テーブルには、PD の API を介して TiKV ノードの基本情報が表示されます。これには、クラスタに割り当てられた ID、アドレスとポート、現在のノードのステータス、容量、リージョンリーダーの数などが含まれます。

> **注記：**
>
> このテーブルは、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスでは利用できません。

```sql
USE INFORMATION_SCHEMA;
DESC TIKV_STORE_STATUS;
```

出力は以下のとおりです。

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

`TIKV_STORE_STATUS`テーブルの列の説明は以下のとおりです。

-   `STORE_ID` : ストアのID。
-   `ADDRESS` : 店舗の住所。
-   `STORE_STATE` : ストア状態の識別子。これは`STORE_STATE_NAME`に対応します。
-   `STORE_STATE_NAME` : ストア状態の名前。名前は`Up` 、 `Offline` 、または`Tombstone` 。
-   `LABEL` : ストアのラベルセット。
-   `VERSION` : ストアのバージョン番号。
-   `CAPACITY` : ストアのstorage容量。
-   `AVAILABLE` : ストアの残りのstorage容量。
-   `LEADER_COUNT` : ストアのリーダーの数。
-   `LEADER_WEIGHT` : ストアのリーダーウェイト。
-   `LEADER_SCORE` : ストアのリーダースコア。
-   `LEADER_SIZE` : ストア上のすべてのリーダーのおおよその合計データサイズ (MB)。
-   `REGION_COUNT` : ストアのリージョン数。
-   `REGION_WEIGHT` : ストアのリージョンウェイト。
-   `REGION_SCORE` : ストアのリージョンスコア。
-   `REGION_SIZE` : ストア上のすべてのリージョンのおおよその合計データサイズ (MB)。
-   `START_TS` : ストアが開始された時のタイムスタンプ。
-   `LAST_HEARTBEAT_TS` : ストアから送信された最後のハートビートのタイムスタンプ。
-   `UPTIME` : ストアが起動してからの合計時間。
