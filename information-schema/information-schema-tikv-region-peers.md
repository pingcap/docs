---
title: TIKV_REGION_PEERS
summary: TIKV_REGION_PEERS` INFORMATION_SCHEMA テーブルについて学習します。
---

# TIKV_REGION_PEERS {#tikv-region-peers}

`TIKV_REGION_PEERS`表には、TiKV 内の単一のリージョンノードの詳細情報 (学習者であるかリーダーであるかなど) が表示されます。

> **注記：**
>
> このテーブルはクラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では使用できません。

```sql
USE INFORMATION_SCHEMA;
DESC TIKV_REGION_PEERS;
```

出力は次のようになります。

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

たとえば、次の SQL ステートメントを使用して、最大値が`WRITTEN_BYTES`である上位 3 つのリージョンの特定の TiKV アドレスを照会できます。

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

`TIKV_REGION_PEERS`テーブル内のフィールドは次のように説明されます。

-   REGION_ID:リージョンID。
-   PEER_ID:リージョンピアの ID。
-   STORE_ID:リージョンが配置されている TiKV ストアの ID。
-   IS_LEARNER: ピアが学習者であるかどうか。
-   IS_LEADER: ピアがリーダーであるかどうか。
-   ステータス: ピアのステータス:
    -   保留中: 一時的に利用できません。
    -   DOWN: オフラインで変換済み。このピアはサービスを提供していません。
    -   正常: 正常に動作しています。
-   DOWN_SECONDS: オフラインの継続時間（秒）。
