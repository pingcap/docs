---
title: TIKV_STORE_STATUS
summary: 表`TIKV_STORE_STATUS`は、PDのAPIを介してTiKVノードの基本情報を示します。列には、ストアのID、アドレス、状態、容量、リーダー数などが含まれます。このテーブルはTiDBサーバーレスクラスターでは使用できません。
---

# TIKV_STORE_STATUS {#tikv-store-status}

表`TIKV_STORE_STATUS`は、クラスターに割り当てられた ID、アドレスとポート、ステータス、容量、現在のノードのリージョンリーダーの数など、PD の API を介した TiKV ノードの基本情報を示しています。

> **注記：**
>
> このテーブルは[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターでは使用できません。

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

`TIKV_STORE_STATUS`の表の列の説明は次のとおりです。

-   `STORE_ID` : ストアのID。
-   `ADDRESS` : ストアのアドレス。
-   `STORE_STATE` : Store 状態の識別子。 `STORE_STATE_NAME`に対応します。
-   `STORE_STATE_NAME` : ストア状態の名前。名前は`Up` 、 `Offline` 、または`Tombstone`です。
-   `LABEL` : ストアに設定されたラベル。
-   `VERSION` : ストアのバージョン番号。
-   `CAPACITY` : ストアのstorage容量。
-   `AVAILABLE` : ストアの残りのstorage容量。
-   `LEADER_COUNT` : ストア上のリーダーの数。
-   `LEADER_WEIGHT` : ストアのリーダーの重み。
-   `LEADER_SCORE` : ストアのリーダースコア。
-   `LEADER_SIZE` : ストア上のすべてのリーダーのおおよその合計データ サイズ (MB)。
-   `REGION_COUNT` : ストア上のリージョンの数。
-   `REGION_WEIGHT` : ストアのリージョンの重み。
-   `REGION_SCORE` : ストアのリージョンスコア。
-   `REGION_SIZE` : ストア上のすべてのリージョンのおおよその合計データ サイズ (MB)。
-   `START_TS` : ストアが開始されたときのタイムスタンプ。
-   `LAST_HEARTBEAT_TS` : ストアによって送信された最後のハートビートのタイムスタンプ。
-   `UPTIME` : ストアが開始されてからの合計時間。
