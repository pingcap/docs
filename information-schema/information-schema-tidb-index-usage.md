---
title: TIDB_INDEX_USAGE
summary: Learn the `TIDB_INDEX_USAGE` INFORMATION_SCHEMA table.
---

# TIDB_INDEX_USAGE

<CustomContent platform="tidb">

Starting from v8.0.0, TiDB provides the `TIDB_INDEX_USAGE` table. You can use `TIDB_INDEX_USAGE` to get the usage statistics of all indexes on the current TiDB node. By default, TiDB collects these index usage statistics during SQL statement execution. You can disable this feature by turning off the [`instance.tidb_enable_collect_execution_info`](/tidb-configuration-file.md#tidb_enable_collect_execution_info) configuration item or the [`tidb_enable_collect_execution_info`](/system-variables.md#tidb_enable_collect_execution_info) system variable.

</CustomContent>

<CustomContent platform="tidb-cloud">

Starting from v8.0.0, TiDB provides the `TIDB_INDEX_USAGE` table. You can use `TIDB_INDEX_USAGE` to get the usage statistics of all indexes on the current TiDB node. By default, TiDB collects these index usage statistics during SQL statement execution. You can disable this feature by turning off the [`instance.tidb_enable_collect_execution_info`](https://docs.pingcap.com/tidb/v8.0/tidb-configuration-file#tidb_enable_collect_execution_info) configuration item or the [`tidb_enable_collect_execution_info`](/system-variables.md#tidb_enable_collect_execution_info) system variable.

</CustomContent>

```sql
USE INFORMATION_SCHEMA;
DESC TIDB_INDEX_USAGE;
```

```sql
+--------------------------+-------------+------+------+---------+-------+
| Field                    | Type        | Null | Key  | Default | Extra |
+--------------------------+-------------+------+------+---------+-------+
| TABLE_SCHEMA             | varchar(64) | YES  |      | NULL    |       |
| TABLE_NAME               | varchar(64) | YES  |      | NULL    |       |
| INDEX_NAME               | varchar(64) | YES  |      | NULL    |       |
| QUERY_TOTAL              | bigint(21)  | YES  |      | NULL    |       |
| KV_REQ_TOTAL             | bigint(21)  | YES  |      | NULL    |       |
| ROWS_ACCESS_TOTAL        | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_0      | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_0_1    | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_1_10   | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_10_20  | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_20_50  | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_50_100 | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_100    | bigint(21)  | YES  |      | NULL    |       |
| LAST_ACCESS_TIME         | datetime    | YES  |      | NULL    |       |
+--------------------------+-------------+------+------+---------+-------+
14 rows in set (0.00 sec)
```

The columns in the `TIDB_INDEX_USAGE` table are as follows:

* `TABLE_SCHEMA`: The name of the database to which the table containing the index belongs.
* `TABLE_NAME`: The name of the table containing the index.
* `INDEX_NAME`: The name of the index.
* `QUERY_TOTAL`: The total number of statements accessing the index.
* `KV_REQ_TOTAL`: The total number of KV requests generated when accessing the index.
* `ROWS_ACCESS_TOTAL`: The total number of rows scanned when accessing the index.
* `PERCENTAGE_ACCESS_0`: The number of times the row access ratio (the percentage of accessed rows out of the total number of rows in the table) is 0.
* `PERCENTAGE_ACCESS_0_1`: The number of times the row access ratio is between 0% and 1%.
* `PERCENTAGE_ACCESS_1_10`: The number of times the row access ratio is between 1% and 10%.
* `PERCENTAGE_ACCESS_10_20`: The number of times the row access ratio is between 10% and 20%.
* `PERCENTAGE_ACCESS_20_50`: The number of times the row access ratio is between 20% and 50%.
* `PERCENTAGE_ACCESS_50_100`: The number of times the row access ratio is between 50% and 100%.
* `PERCENTAGE_ACCESS_100`: The number of times the row access ratio is 100%.
* `LAST_ACCESS_TIME`: The time of the most recent access to the index.

## CLUSTER_TIDB_INDEX_USAGE

The `TIDB_INDEX_USAGE` table only provides usage statistics of all indexes on a single TiDB node. To obtain the index usage statistics on all TiDB nodes in the cluster, you need to query the `CLUSTER_TIDB_INDEX_USAGE` table.

Compared with the `TIDB_INDEX_USAGE` table, the query result of the `CLUSTER_TIDB_INDEX_USAGE` table includes an additional `INSTANCE` field. This field displays the IP address and port of each node in the cluster, which helps you distinguish the statistics across different nodes.

```sql
USE INFORMATION_SCHEMA;
DESC CLUSTER_TIDB_INDEX_USAGE;
```

The output is as follows:

```sql
+--------------------------+-------------+------+------+---------+-------+
| Field                    | Type        | Null | Key  | Default | Extra |
+--------------------------+-------------+------+------+---------+-------+
| INSTANCE                 | varchar(64) | YES  |      | NULL    |       |
| TABLE_SCHEMA             | varchar(64) | YES  |      | NULL    |       |
| TABLE_NAME               | varchar(64) | YES  |      | NULL    |       |
| INDEX_NAME               | varchar(64) | YES  |      | NULL    |       |
| QUERY_TOTAL              | bigint(21)  | YES  |      | NULL    |       |
| KV_REQ_TOTAL             | bigint(21)  | YES  |      | NULL    |       |
| ROWS_ACCESS_TOTAL        | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_0      | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_0_1    | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_1_10   | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_10_20  | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_20_50  | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_50_100 | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_100    | bigint(21)  | YES  |      | NULL    |       |
| LAST_ACCESS_TIME         | datetime    | YES  |      | NULL    |       |
+--------------------------+-------------+------+------+---------+-------+
15 rows in set (0.00 sec)
```

## Limitations

- The data in the `TIDB_INDEX_USAGE` table might be delayed by up to 5 minutes.
- After TiDB restarts, the data in the `TIDB_INDEX_USAGE` table is cleared.
- TiDB records index usage for a table only when the table has valid statistics.

## Read more

- [`sys.schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md)