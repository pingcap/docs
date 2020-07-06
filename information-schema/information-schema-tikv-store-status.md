---
title: TIKV_STORE_STATUS
summary: Learn the `TIKV_STORE_STATUS` information_schema table.
category: reference
---


# TIKV_STORE_STATUS

The `TIKV_STORE_STATUS` table provides the status information of all TiKV Stores.

{{< copyable "sql" >}}

```sql
use information_schema;
DESC TIKV_STORE_STATUS;
```

```
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

## TIKV\_STORE\_STATUS table

The `TIKV_STORE_STATUS` table shows some basic information of TiKV nodes via PD's API, like the ID allocated in the cluster, address and port, and status, capacity, and the number of Region leaders of the current node.

{{< copyable "sql" >}}

```sql
desc tikv_store_status\G
```

```
*************************** 1. row ***************************
       Table: TIKV_STORE_STATUS
Create Table: CREATE TABLE `TIKV_STORE_STATUS` (
  `STORE_ID` bigint(21) unsigned DEFAULT NULL,
  `ADDRESS` varchar(64) DEFAULT NULL,
  `STORE_STATE` bigint(21) unsigned DEFAULT NULL,
  `STORE_STATE_NAME` varchar(64) DEFAULT NULL,
  `LABEL` json unsigned DEFAULT NULL,
  `VERSION` varchar(64) DEFAULT NULL,
  `CAPACITY` varchar(64) DEFAULT NULL,
  `AVAILABLE` varchar(64) DEFAULT NULL,
  `LEADER_COUNT` bigint(21) unsigned DEFAULT NULL,
  `LEADER_WEIGHT` bigint(21) unsigned DEFAULT NULL,
  `LEADER_SCORE` bigint(21) unsigned DEFAULT NULL,
  `LEADER_SIZE` bigint(21) unsigned DEFAULT NULL,
  `REGION_COUNT` bigint(21) unsigned DEFAULT NULL,
  `REGION_WEIGHT` bigint(21) unsigned DEFAULT NULL,
  `REGION_SCORE` bigint(21) unsigned DEFAULT NULL,
  `REGION_SIZE` bigint(21) unsigned DEFAULT NULL,
  `START_TS` datetime unsigned DEFAULT NULL,
  `LAST_HEARTBEAT_TS` datetime unsigned DEFAULT NULL,
  `UPTIME` varchar(64) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
1 row in set (0.01 sec)
```