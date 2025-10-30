---
title: TIKV_REGION_PEERS
summary: 了解 `TIKV_REGION_PEERS` INFORMATION_SCHEMA 表。
---

# TIKV_REGION_PEERS

`TIKV_REGION_PEERS` 表展示了 TiKV 中单个 Region 节点的详细信息，例如该节点是否为 learner 或 leader。

> **Note:**
>
> 该表在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。

```sql
USE INFORMATION_SCHEMA;
DESC TIKV_REGION_PEERS;
```

输出如下：

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

例如，你可以使用以下 SQL 语句，查询 `WRITTEN_BYTES` 最大的前 3 个 Region 的具体 TiKV 地址：

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

`TIKV_REGION_PEERS` 表中的字段说明如下：

* REGION_ID：Region 的 ID。
* PEER_ID：Region 副本的 ID。
* STORE_ID：该 Region 所在 TiKV 实例的 ID。
* IS_LEARNER：该副本是否为 learner。
* IS_LEADER：该副本是否为 leader。
* STATUS：副本的状态：
    * PENDING：暂时不可用。
    * DOWN：已下线并已转换。该副本不再提供服务。
    * NORMAL：正常运行。
* DOWN_SECONDS：下线持续的时间，单位为秒。