---
title: TIDB_HOT_REGIONS
summary: Learn the `TIDB_HOT_REGIONS` information_schema table.
---

# TIDB_HOT_REGIONS

The `TIDB_HOT_REGIONS` table provides information about hotspot Regions.

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC tidb_hot_regions;
```

```
+----------------+-------------+------+------+---------+-------+
| Field          | Type        | Null | Key  | Default | Extra |
+----------------+-------------+------+------+---------+-------+
| TABLE_ID       | bigint(21)  | YES  |      | NULL    |       |
| INDEX_ID       | bigint(21)  | YES  |      | NULL    |       |
| DB_NAME        | varchar(64) | YES  |      | NULL    |       |
| TABLE_NAME     | varchar(64) | YES  |      | NULL    |       |
| INDEX_NAME     | varchar(64) | YES  |      | NULL    |       |
| REGION_ID      | bigint(21)  | YES  |      | NULL    |       |
| TYPE           | varchar(64) | YES  |      | NULL    |       |
| MAX_HOT_DEGREE | bigint(21)  | YES  |      | NULL    |       |
| REGION_COUNT   | bigint(21)  | YES  |      | NULL    |       |
| FLOW_BYTES     | bigint(21)  | YES  |      | NULL    |       |
+----------------+-------------+------+------+---------+-------+
10 rows in set (0.00 sec)
```

The description of columns in the `TIDB_HOT_REGIONS` table is as follows:

* `TABLE_ID`: ID of located.
* `INDEX_ID`: ID of the table in which the hot Region is the index in which the hot Region is located.
* `DB_NAME`: The database name of the object in which the hot Region is located.
* `TABLE_NAME`: The name of the table in which the hot Region is located.
* `INDEX_NAME`: The name of the index in which the hot Region is located.
* `REGION_ID`: ID of the hot Region.
* `TYPE`: The type of the hot Region.
* `MAX_HOT_DEGREE`: The maximum hot degree of the Region.
* `REGION_COUNT`: The number of Regions in the instance. 
* `FLOW_BYTES`: The number of bytes written and read in the Region.
