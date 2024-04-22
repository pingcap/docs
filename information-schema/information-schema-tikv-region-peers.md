---
title: TIKV_REGION_PEERS
summary: TIKV_REGION_PEERSテーブルには、TiKVの単一リージョンノードの詳細情報が表示されます。このテーブルはTiDBサーバーレスクラスターでは使用できません。フィールドにはREGION_ID、PEER_ID、STORE_ID、IS_LEARNER、IS_LEADER、STATUS、DOWN_SECONDSが含まれます。例えば、最大値WRITTEN_BYTESで上位3つのリージョンの特定のTiKVアドレスをクエリできます。また、STATUSフィールドには保留中、下、NORMALのステータスがあります。
---

# TIKV_REGION_PEERS {#tikv-region-peers}

`TIKV_REGION_PEERS`表には、TiKV の単一リージョンノードの詳細情報 (学習者かリーダーかなど) が表示されます。

> **注記：**
>
> このテーブルは[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターでは使用できません。

```sql
USE INFORMATION_SCHEMA;
DESC TIKV_REGION_PEERS;
```

出力は次のとおりです。

```sql
+--------------+-------------+------+------+---------+-------+
| Field        | Type        | Null | Key  | Default | Extra |
+--------------+-------------+------+------+---------+-------+
| REGION_ID    | bigint(21)  | YES  |      | NULL    |       |
| PEER_ID      | bigint(21)  | YES  |      | NULL    |       |
| STORE_ID     | bigint(21)  | YES  |      | NULL    |       |
| IS_LEARNER   | tinyint(1)  | NO   |      | 0       |       |
| IS_LEADER    | tinyint(1)  | NO   |      | 0       |       |
| STATUS       | varchar(10) | YES  |      | 0       |       |
| DOWN_SECONDS | bigint(21)  | YES  |      | 0       |       |
+--------------+-------------+------+------+---------+-------+
7 rows in set (0.01 sec)
```

たとえば、次の SQL ステートメントを使用して、最大値`WRITTEN_BYTES`で上位 3 つのリージョンの特定の TiKV アドレスをクエリできます。

```sql
SELECT
  address,
  tikv.address,
  region.region_id
FROM
  TIKV_STORE_STATUS tikv,
  TIKV_REGION_PEERS peer,
  (SELECT * FROM tikv_region_status ORDER BY written_bytes DESC LIMIT 3) region
WHERE
  region.region_id = peer.region_id
  AND peer.is_leader = 1
  AND peer.store_id = tikv.store_id;
```

`TIKV_REGION_PEERS`テーブルのフィールドは次のように説明されています。

-   REGION_ID:リージョンID。
-   PEER_ID:リージョンピアの ID。
-   STORE_ID:リージョンが配置されている TiKV ストアの ID。
-   IS_LEARNER: ピアが学習者かどうか。
-   IS_LEADER: ピアがリーダーであるかどうか。
-   STATUS: ピアのステータス:
    -   保留中: 一時的に利用できません。
    -   下: オフラインで変換されました。このピアはサービスを提供しなくなりました。
    -   NORMAL：正常に動作しています。
-   DOWN_SECONDS: オフラインの継続時間 (秒単位)。
