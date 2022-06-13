---
title: TIKV_REGION_PEERS
summary: Learn the `TIKV_REGION_PEERS` information_schema table.
---

# TIKV_REGION_PEERS {#tikv-region-peers}

`TIKV_REGION_PEERS`の表は、学習者かリーダーかなど、TiKVの単一のリージョンノードの詳細情報を示しています。

{{< copyable "" >}}

```sql
USE information_schema;
DESC tikv_region_peers;
```

```
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

たとえば、次のSQLステートメントを使用して、最大値が`WRITTEN_BYTES`の上位3つのリージョンの特定のTiKVアドレスを照会できます。

```sql
SELECT
 address,
 tikv.address,
 region.region_id
FROM
 tikv_store_status tikv,
 tikv_region_peers peer,
 (SELECT * FROM tikv_region_status ORDER BY written_bytes DESC LIMIT 3) region
WHERE
  region.region_id = peer.region_id
 AND peer.is_leader = 1
 AND peer.store_id = tikv.store_id;
```

`TIKV_REGION_PEERS`表のフィールドは次のように説明されています。

-   REGION_ID：リージョンID。
-   PEER_ID：リージョンピアのID。
-   STORE_ID：リージョンが配置されているTiKVストアのID。
-   IS_LEARNER：ピアが学習者であるかどうか。
-   IS_LEADER：ピアがリーダーであるかどうか。
-   ステータス：ピアのステータス：
    -   保留中：一時的に利用できません。
    -   DOWN：オフラインで変換されました。このピアはサービスを提供しなくなります。
    -   NORMAL：正常に動作しています。
-   DOWN_SECONDS：オフラインの期間（秒単位）。
