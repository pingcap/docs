---
title: TIKV_REGION_PEERS
summary: Learn the `TIKV_REGION_PEERS` information_schema table.
category: reference
---

# TIKV_REGION_PEERS

The `TIKV_REGION_PEERS` table provides the peer information of all Regions.

{{< copyable "sql" >}}

```sql
use information_schema;
DESC TIKV_REGION_PEERS;
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
7 rows in set (0.00 sec)
```


## TIKV\_REGION\_PEERS table

The `TIKV_REGION_PEERS` table shows detailed information of a single Region node in TiKV, like whether it is a learner or leader.

{{< copyable "sql" >}}

```sql
desc tikv_region_peers\G
```

```
*************************** 1. row ***************************
       Table: TIKV_REGION_PEERS
Create Table: CREATE TABLE `TIKV_REGION_PEERS` (
  `REGION_ID` bigint(21) unsigned DEFAULT NULL,
  `PEER_ID` bigint(21) unsigned DEFAULT NULL,
  `STORE_ID` bigint(21) unsigned DEFAULT NULL,
  `IS_LEARNER` tinyint(1) unsigned DEFAULT NULL,
  `IS_LEADER` tinyint(1) unsigned DEFAULT NULL,
  `STATUS` varchar(10) DEFAULT NULL,
  `DOWN_SECONDS` bigint(21) unsigned DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
1 row in set (0.00 sec)
```

For example, you can query the specific TiKV addresses for the top 3 Regions with the maximum value of `WRITTEN_BYTES` using the following SQL statement:

```sql
select
   address,
   tikv.address,
   region.region_id,
from
   tikv_store_status tikv,
   tikv_region_peers peer,
   (
      select
         *
      from
         tikv_region_status region
      order by
         written_bytes desc limit 3
   )
   region
where
   region.region_id = peer.region_id
   and peer.is_leader = 1
   and peer.store_id = tikv.region_id
```

