---
title: TIKV_REGION_STATUS
summary: Learn the `TIKV_REGION_STATUS` information_schema table.
category: reference
---

# TIKV_REGION_STATUS

The `TIKV_REGION_STATUS` table provides the status information of all Regions.


{{< copyable "sql" >}}

```sql
use information_schema;
DESC TIKV_REGION_STATUS;
```

```
+---------------------------+-------------+------+------+---------+-------+
| Field                     | Type        | Null | Key  | Default | Extra |
+---------------------------+-------------+------+------+---------+-------+
| REGION_ID                 | bigint(21)  | YES  |      | NULL    |       |
| START_KEY                 | text        | YES  |      | NULL    |       |
| END_KEY                   | text        | YES  |      | NULL    |       |
| TABLE_ID                  | bigint(21)  | YES  |      | NULL    |       |
| DB_NAME                   | varchar(64) | YES  |      | NULL    |       |
| TABLE_NAME                | varchar(64) | YES  |      | NULL    |       |
| IS_INDEX                  | tinyint(1)  | NO   |      | 0       |       |
| INDEX_ID                  | bigint(21)  | YES  |      | NULL    |       |
| INDEX_NAME                | varchar(64) | YES  |      | NULL    |       |
| EPOCH_CONF_VER            | bigint(21)  | YES  |      | NULL    |       |
| EPOCH_VERSION             | bigint(21)  | YES  |      | NULL    |       |
| WRITTEN_BYTES             | bigint(21)  | YES  |      | NULL    |       |
| READ_BYTES                | bigint(21)  | YES  |      | NULL    |       |
| APPROXIMATE_SIZE          | bigint(21)  | YES  |      | NULL    |       |
| APPROXIMATE_KEYS          | bigint(21)  | YES  |      | NULL    |       |
| REPLICATIONSTATUS_STATE   | varchar(64) | YES  |      | NULL    |       |
| REPLICATIONSTATUS_STATEID | bigint(21)  | YES  |      | NULL    |       |
+---------------------------+-------------+------+------+---------+-------+
17 rows in set (0.00 sec)
```

## TIKV\_REGION\_STATUS table

The `TIKV_REGION_STATUS` table shows some basic information of TiKV Regions via PD's API, like the Region ID, starting and ending key-values, and read and write traffic.

{{< copyable "sql" >}}

```sql
desc tikv_region_status\G
```

```
*************************** 1. row ***************************
       Table: TIKV_REGION_STATUS
Create Table: CREATE TABLE `TIKV_REGION_STATUS` (
  `REGION_ID` bigint(21) unsigned DEFAULT NULL,
  `START_KEY` text DEFAULT NULL,
  `END_KEY` text DEFAULT NULL,
  `EPOCH_CONF_VER` bigint(21) unsigned DEFAULT NULL,
  `EPOCH_VERSION` bigint(21) unsigned DEFAULT NULL,
  `WRITTEN_BYTES` bigint(21) unsigned DEFAULT NULL,
  `READ_BYTES` bigint(21) unsigned DEFAULT NULL,
  `APPROXIMATE_SIZE` bigint(21) unsigned DEFAULT NULL,
  `APPROXIMATE_KEYS` bigint(21) unsigned DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
1 row in set (0.00 sec)
```

You can implement the `top confver`, `top read` and `top write` operations in pd-ctl via the `ORDER BY X LIMIT Y` operation on the `EPOCH_CONF_VER`, `WRITTEN_BYTES` and `READ_BYTES` columns.

You can query the top 3 Regions with the most write data using the following SQL statement:

```
select * from tikv_region_status order by written_bytes desc limit 3;
```