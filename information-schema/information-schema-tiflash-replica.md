---
title: TIFLASH_REPLICA
summary: Learn the `TIFLASH_REPLICA` information_schema table.
---

# TIFLASH_REPLICA {#tiflash-replica}

`TIFLASH_REPLICA`の表は、使用可能なTiFlashレプリカに関する情報を提供します。

{{< copyable "" >}}

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
