---
title: TIFLASH_REPLICA
summary: Learn the `TIFLASH_REPLICA` information_schema table.
---

# TIFLASH_REPLICA

The `TIFLASH_REPLICA` table provides information about TiFlash replicas available.

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC tiflash_replica;
```

```
+-----------------+-------------+------+------+---------+-------+
| Field           | Type        | Null | Key  | Default | Extra |
+-----------------+-------------+------+------+---------+-------+
| TABLE_SCHEMA    | varchar(64) | YES  |      | NULL    |       |
| TABLE_NAME      | varchar(64) | YES  |      | NULL    |       |
| TABLE_ID        | bigint(21)  | YES  |      | NULL    |       |
| REPLICA_COUNT   | bigint(64)  | YES  |      | NULL    |       |
| LOCATION_LABELS | varchar(64) | YES  |      | NULL    |       |
| AVAILABLE       | tinyint(1)  | YES  |      | NULL    |       |
| PROGRESS        | double      | YES  |      | NULL    |       |
+-----------------+-------------+------+------+---------+-------+
7 rows in set (0.01 sec)
```

Fields in the `TIFLASH_REPLICA` table are described as follows:

- `TABLE_SCHEMA`: the name of the database to which the table belongs.
- `TABLE_NAME`: the name of the table.
- `TABLE_ID`: the internal ID of the table, which is unique within a TiDB cluster.
- `REPLICA_COUNT`: the number of TiFlash replicas.
- `LOCATION_LABELS`: the LocationLabelList that is set when a TiFlash replica is created.
- `AVAILABLE`: indicates whether to support querying TiFlash. If the value is `1`, TiDB optimizer will intelligently choose to push down queries to TiKV or TiFlash based on query cost. If the value is `0`, TiDB will not push down queries to TiFlash.
- `PROGRESS`: the replication progress of TiFlash replicas, with a precision of minutes. If `PROGRESS` is less than 1, it means the TiFlash replica is lagging behind TiKV, and the query will probably fail due to timeout of waiting for data replication.
- `TABLE_MODE`: indicates whether TiFlash enables [FastScan](/develop/dev-guide-use-fastscan.md). `Normal` means FastScan is disabled, and `Fast` means FastScan is enabled.