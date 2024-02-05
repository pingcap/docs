---
title: TIDB_INDEX_USAGE
summary: Learn the `TIDB_INDEX_USAGE` information_schema table.
---

# TIDB_INDEX_USAGE

`TIDB_INDEX_USAGE` records the access statistics of all indexes on the current node.

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC tidb_index_usage;
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
* `PERCENTAGE_ACCESS_0`: The number of times the access ratio of rows to the total number of rows in the table is 0.
* `PERCENTAGE_ACCESS_0_1`: The number of times the access ratio of rows to the total number of rows in the table is between 0% and 1%.
* `PERCENTAGE_ACCESS_1_10`: The number of times the access ratio of rows to the total number of rows in the table is between 1% and 10%.
* `PERCENTAGE_ACCESS_10_20`: The number of times the access ratio of rows to the total number of rows in the table is between 10% and 20%.
* `PERCENTAGE_ACCESS_20_50`: The number of times the access ratio of rows to the total number of rows in the table is between 20% and 50%.
* `PERCENTAGE_ACCESS_50_100`: The number of times the access ratio of rows to the total number of rows in the table is between 50% and 100%.
* `PERCENTAGE_ACCESS_100`: The number of times the access ratio of rows to the total number of rows in the table is 100%.
* `LAST_ACCESS_TIME`: The time when the index was last accessed.

# Limitations

- The data in the `TIDB_INDEX_USAGE` table may be delayed by up to 5 minutes.
- After TiDB restarts, the data in the `TIDB_INDEX_USAGE` table is cleared.
