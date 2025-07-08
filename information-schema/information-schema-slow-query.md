---
title: SLOW_QUERY
summary: Learn the `SLOW_QUERY` INFORMATION_SCHEMA table.
---

# SLOW_QUERY

<CustomContent platform="tidb">

The `SLOW_QUERY` table provides the slow query information of the current node, which is the parsing result of the TiDB [slow log file](/tidb-configuration-file.md#slow-query-file). The column names in the table are corresponding to the field names in the slow log.

</CustomContent>

<CustomContent platform="tidb-cloud">

The `SLOW_QUERY` table provides the slow query information of the current node, which is the parsing result of the TiDB [slow log file](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#slow-query-file). The column names in the table are corresponding to the field names in the slow log.

</CustomContent>

> **Note:**
>
> This table is not available on [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) clusters.

<CustomContent platform="tidb">

For how to use this table to identify problematic statements and improve query performance, see [Slow Query Log Document](/identify-slow-queries.md).

</CustomContent>

```sql
USE INFORMATION_SCHEMA;
DESC SLOW_QUERY;
```

The output is as follows:

```sql
+-------------------------------+---------------------+------+------+---------+-------+
| Field                         | Type                | Null | Key  | Default | Extra |
+-------------------------------+---------------------+------+------+---------+-------+
| Time                          | timestamp(6)        | NO   | PRI  | NULL    |       |
| Txn_start_ts                  | bigint(20) unsigned | YES  |      | NULL    |       |
| User                          | varchar(64)         | YES  |      | NULL    |       |
| Host                          | varchar(64)         | YES  |      | NULL    |       |
| Conn_ID                       | bigint(20) unsigned | YES  |      | NULL    |       |
| Session_alias                 | varchar(64)         | YES  |      | NULL    |       |
| Exec_retry_count              | bigint(20) unsigned | YES  |      | NULL    |       |
| Exec_retry_time               | double              | YES  |      | NULL    |       |
| Query_time                    | double              | YES  |      | NULL    |       |
| Parse_time                    | double              | YES  |      | NULL    |       |
| Compile_time                  | double              | YES  |      | NULL    |       |
| Rewrite_time                  | double              | YES  |      | NULL    |       |
| Preproc_subqueries            | bigint(20) unsigned | YES  |      | NULL    |       |
| Preproc_subqueries_time       | double              | YES  |      | NULL    |       |
| Optimize_time                 | double              | YES  |      | NULL    |       |
| Wait_TS                       | double              | YES  |      | NULL    |       |
| Prewrite_time                 | double              | YES  |      | NULL    |       |
| Wait_prewrite_binlog_time     | double              | YES  |      | NULL    |       |
| Commit_time                   | double              | YES  |      | NULL    |       |
| Get_commit_ts_time            | double              | YES  |      | NULL    |       |
| Commit_backoff_time           | double              | YES  |      | NULL    |       |
| Backoff_types                 | varchar(64)         | YES  |      | NULL    |       |
| Resolve_lock_time             | double              | YES  |      | NULL    |       |
| Local_latch_wait_time         | double              | YES  |      | NULL    |       |
| Write_keys                    | bigint(22)          | YES  |      | NULL    |       |
| Write_size                    | bigint(22)          | YES  |      | NULL    |       |
| Prewrite_region               | bigint(22)          | YES  |      | NULL    |       |
| Txn_retry                     | bigint(22)          | YES  |      | NULL    |       |
| Cop_time                      | double              | YES  |      | NULL    |       |
| Process_time                  | double              | YES  |      | NULL    |       |
| Wait_time                     | double              | YES  |      | NULL    |       |
| Backoff_time                  | double              | YES  |      | NULL    |       |
| LockKeys_time                 | double              | YES  |      | NULL    |       |
| Request_count                 | bigint(20) unsigned | YES  |      | NULL    |       |
| Total_keys                    | bigint(20) unsigned | YES  |      | NULL    |       |
| Process_keys                  | bigint(20) unsigned | YES  |      | NULL    |       |
| Rocksdb_delete_skipped_count  | bigint(20) unsigned | YES  |      | NULL    |       |
| Rocksdb_key_skipped_count     | bigint(20) unsigned | YES  |      | NULL    |       |
| Rocksdb_block_cache_hit_count | bigint(20) unsigned | YES  |      | NULL    |       |
| Rocksdb_block_read_count      | bigint(20) unsigned | YES  |      | NULL    |       |
| Rocksdb_block_read_byte       | bigint(20) unsigned | YES  |      | NULL    |       |
| DB                            | varchar(64)         | YES  |      | NULL    |       |
| Index_names                   | varchar(100)        | YES  |      | NULL    |       |
| Is_internal                   | tinyint(1)          | YES  |      | NULL    |       |
| Digest                        | varchar(64)         | YES  |      | NULL    |       |
| Stats                         | varchar(512)        | YES  |      | NULL    |       |
| Cop_proc_avg                  | double              | YES  |      | NULL    |       |
| Cop_proc_p90                  | double              | YES  |      | NULL    |       |
| Cop_proc_max                  | double              | YES  |      | NULL    |       |
| Cop_proc_addr                 | varchar(64)         | YES  |      | NULL    |       |
| Cop_wait_avg                  | double              | YES  |      | NULL    |       |
| Cop_wait_p90                  | double              | YES  |      | NULL    |       |
| Cop_wait_max                  | double              | YES  |      | NULL    |       |
| Cop_wait_addr                 | varchar(64)         | YES  |      | NULL    |       |
| Mem_max                       | bigint(20)          | YES  |      | NULL    |       |
| Disk_max                      | bigint(20)          | YES  |      | NULL    |       |
| KV_total                      | double              | YES  |      | NULL    |       |
| PD_total                      | double              | YES  |      | NULL    |       |
| Backoff_total                 | double              | YES  |      | NULL    |       |
| Write_sql_response_total      | double              | YES  |      | NULL    |       |
| Result_rows                   | bigint(22)          | YES  |      | NULL    |       |
| Warnings                      | longtext            | YES  |      | NULL    |       |
| Backoff_Detail                | varchar(4096)       | YES  |      | NULL    |       |
| Prepared                      | tinyint(1)          | YES  |      | NULL    |       |
| Succ                          | tinyint(1)          | YES  |      | NULL    |       |
| IsExplicitTxn                 | tinyint(1)          | YES  |      | NULL    |       |
| IsWriteCacheTable             | tinyint(1)          | YES  |      | NULL    |       |
| Plan_from_cache               | tinyint(1)          | YES  |      | NULL    |       |
| Plan_from_binding             | tinyint(1)          | YES  |      | NULL    |       |
| Has_more_results              | tinyint(1)          | YES  |      | NULL    |       |
| Resource_group                | varchar(64)         | YES  |      | NULL    |       |
| Request_unit_read             | double              | YES  |      | NULL    |       |
| Request_unit_write            | double              | YES  |      | NULL    |       |
| Time_queued_by_rc             | double              | YES  |      | NULL    |       |
| Tidb_cpu_time                 | double              | YES  |      | NULL    |       |
| Tikv_cpu_time                 | double              | YES  |      | NULL    |       |
| Plan                          | longtext            | YES  |      | NULL    |       |
| Plan_digest                   | varchar(128)        | YES  |      | NULL    |       |
| Binary_plan                   | longtext            | YES  |      | NULL    |       |
| Prev_stmt                     | longtext            | YES  |      | NULL    |       |
| Query                         | longtext            | YES  |      | NULL    |       |
+-------------------------------+---------------------+------+------+---------+-------+
81 rows in set (0.00 sec)
```

The maximum statement length of the `Query` column is limited by the [`tidb_stmt_summary_max_sql_length`](/system-variables.md#tidb_stmt_summary_max_sql_length-new-in-v40) system variable.

## CLUSTER_SLOW_QUERY table

The `CLUSTER_SLOW_QUERY` table provides the slow query information of all nodes in the cluster, which is the parsing result of the TiDB slow log files. You can use the `CLUSTER_SLOW_QUERY` table the way you do with `SLOW_QUERY`. The table schema of the `CLUSTER_SLOW_QUERY` table differs from that of the `SLOW_QUERY` table in that an `INSTANCE` column is added to `CLUSTER_SLOW_QUERY`. The `INSTANCE` column represents the TiDB node address of the row information on the slow query.

> **Note:**
>
> This table is not available on [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) clusters.

<CustomContent platform="tidb">

For how to use this table to identify problematic statements and improve query performance, see [Slow Query Log Document](/identify-slow-queries.md).

</CustomContent>

```sql
DESC CLUSTER_SLOW_QUERY;
```

The output is as follows:

```sql
+-------------------------------+---------------------+------+------+---------+-------+
| Field                         | Type                | Null | Key  | Default | Extra |
+-------------------------------+---------------------+------+------+---------+-------+
| INSTANCE                      | varchar(64)         | YES  |      | NULL    |       |
| Time                          | timestamp(6)        | NO   | PRI  | NULL    |       |
| Txn_start_ts                  | bigint(20) unsigned | YES  |      | NULL    |       |
| User                          | varchar(64)         | YES  |      | NULL    |       |
| Host                          | varchar(64)         | YES  |      | NULL    |       |
| Conn_ID                       | bigint(20) unsigned | YES  |      | NULL    |       |
| Session_alias                 | varchar(64)         | YES  |      | NULL    |       |
| Exec_retry_count              | bigint(20) unsigned | YES  |      | NULL    |       |
| Exec_retry_time               | double              | YES  |      | NULL    |       |
| Query_time                    | double              | YES  |      | NULL    |       |
| Parse_time                    | double              | YES  |      | NULL    |       |
| Compile_time                  | double              | YES  |      | NULL    |       |
| Rewrite_time                  | double              | YES  |      | NULL    |       |
| Preproc_subqueries            | bigint(20) unsigned | YES  |      | NULL    |       |
| Preproc_subqueries_time       | double              | YES  |      | NULL    |       |
| Optimize_time                 | double              | YES  |      | NULL    |       |
| Wait_TS                       | double              | YES  |      | NULL    |       |
| Prewrite_time                 | double              | YES  |      | NULL    |       |
| Wait_prewrite_binlog_time     | double              | YES  |      | NULL    |       |
| Commit_time                   | double              | YES  |      | NULL    |       |
| Get_commit_ts_time            | double              | YES  |      | NULL    |       |
| Commit_backoff_time           | double              | YES  |      | NULL    |       |
| Backoff_types                 | varchar(64)         | YES  |      | NULL    |       |
| Resolve_lock_time             | double              | YES  |      | NULL    |       |
| Local_latch_wait_time         | double              | YES  |      | NULL    |       |
| Write_keys                    | bigint(22)          | YES  |      | NULL    |       |
| Write_size                    | bigint(22)          | YES  |      | NULL    |       |
| Prewrite_region               | bigint(22)          | YES  |      | NULL    |       |
| Txn_retry                     | bigint(22)          | YES  |      | NULL    |       |
| Cop_time                      | double              | YES  |      | NULL    |       |
| Process_time                  | double              | YES  |      | NULL    |       |
| Wait_time                     | double              | YES  |      | NULL    |       |
| Backoff_time                  | double              | YES  |      | NULL    |       |
| LockKeys_time                 | double              | YES  |      | NULL    |       |
| Request_count                 | bigint(20) unsigned | YES  |      | NULL    |       |
| Total_keys                    | bigint(20) unsigned | YES  |      | NULL    |       |
| Process_keys                  | bigint(20) unsigned | YES  |      | NULL    |       |
| Rocksdb_delete_skipped_count  | bigint(20) unsigned | YES  |      | NULL    |       |
| Rocksdb_key_skipped_count     | bigint(20) unsigned | YES  |      | NULL    |       |
| Rocksdb_block_cache_hit_count | bigint(20) unsigned | YES  |      | NULL    |       |
| Rocksdb_block_read_count      | bigint(20) unsigned | YES  |      | NULL    |       |
| Rocksdb_block_read_byte       | bigint(20) unsigned | YES  |      | NULL    |       |
| DB                            | varchar(64)         | YES  |      | NULL    |       |
| Index_names                   | varchar(100)        | YES  |      | NULL    |       |
| Is_internal                   | tinyint(1)          | YES  |      | NULL    |       |
| Digest                        | varchar(64)         | YES  |      | NULL    |       |
| Stats                         | varchar(512)        | YES  |      | NULL    |       |
| Cop_proc_avg                  | double              | YES  |      | NULL    |       |
| Cop_proc_p90                  | double              | YES  |      | NULL    |       |
| Cop_proc_max                  | double              | YES  |      | NULL    |       |
| Cop_proc_addr                 | varchar(64)         | YES  |      | NULL    |       |
| Cop_wait_avg                  | double              | YES  |      | NULL    |       |
| Cop_wait_p90                  | double              | YES  |      | NULL    |       |
| Cop_wait_max                  | double              | YES  |      | NULL    |       |
| Cop_wait_addr                 | varchar(64)         | YES  |      | NULL    |       |
| Mem_max                       | bigint(20)          | YES  |      | NULL    |       |
| Disk_max                      | bigint(20)          | YES  |      | NULL    |       |
| KV_total                      | double              | YES  |      | NULL    |       |
| PD_total                      | double              | YES  |      | NULL    |       |
| Backoff_total                 | double              | YES  |      | NULL    |       |
| Write_sql_response_total      | double              | YES  |      | NULL    |       |
| Result_rows                   | bigint(22)          | YES  |      | NULL    |       |
| Warnings                      | longtext            | YES  |      | NULL    |       |
| Backoff_Detail                | varchar(4096)       | YES  |      | NULL    |       |
| Prepared                      | tinyint(1)          | YES  |      | NULL    |       |
| Succ                          | tinyint(1)          | YES  |      | NULL    |       |
| IsExplicitTxn                 | tinyint(1)          | YES  |      | NULL    |       |
| IsWriteCacheTable             | tinyint(1)          | YES  |      | NULL    |       |
| Plan_from_cache               | tinyint(1)          | YES  |      | NULL    |       |
| Plan_from_binding             | tinyint(1)          | YES  |      | NULL    |       |
| Has_more_results              | tinyint(1)          | YES  |      | NULL    |       |
| Resource_group                | varchar(64)         | YES  |      | NULL    |       |
| Request_unit_read             | double              | YES  |      | NULL    |       |
| Request_unit_write            | double              | YES  |      | NULL    |       |
| Time_queued_by_rc             | double              | YES  |      | NULL    |       |
| Tidb_cpu_time                 | double              | YES  |      | NULL    |       |
| Tikv_cpu_time                 | double              | YES  |      | NULL    |       |
| Plan                          | longtext            | YES  |      | NULL    |       |
| Plan_digest                   | varchar(128)        | YES  |      | NULL    |       |
| Binary_plan                   | longtext            | YES  |      | NULL    |       |
| Prev_stmt                     | longtext            | YES  |      | NULL    |       |
| Query                         | longtext            | YES  |      | NULL    |       |
+-------------------------------+---------------------+------+------+---------+-------+
82 rows in set (0.00 sec)
```

When the cluster system table is queried, TiDB does not obtain data from all nodes, but pushes down the related calculation to other nodes. The execution plan is as follows:

```sql
DESC SELECT COUNT(*) FROM CLUSTER_SLOW_QUERY WHERE user = 'u1';
```

The output is as follows:

```sql
+----------------------------+----------+-----------+--------------------------+------------------------------------------------------+
| id                         | estRows  | task      | access object            | operator info                                        |
+----------------------------+----------+-----------+--------------------------+------------------------------------------------------+
| StreamAgg_7                | 1.00     | root      |                          | funcs:count(1)->Column#75                            |
| └─TableReader_13           | 10.00    | root      |                          | data:Selection_12                                    |
|   └─Selection_12           | 10.00    | cop[tidb] |                          | eq(INFORMATION_SCHEMA.cluster_slow_query.user, "u1") |
|     └─TableFullScan_11     | 10000.00 | cop[tidb] | table:CLUSTER_SLOW_QUERY | keep order:false, stats:pseudo                       |
+----------------------------+----------+-----------+--------------------------+------------------------------------------------------+
4 rows in set (0.00 sec)
```

In the preceding execution plan, the `user = u1` condition is pushed down to other (`cop`) TiDB nodes, and the aggregate operator is also pushed down (the `StreamAgg` operator in the graph).

Currently, because statistics of the system tables are not collected, sometimes some aggregation operators cannot be pushed down, which results in slow execution. In this case, you can manually specify the SQL HINT to push down the aggregation operators. For example:

```sql
SELECT /*+ AGG_TO_COP() */ COUNT(*) FROM CLUSTER_SLOW_QUERY GROUP BY user;
```

## View execution information

By running an [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) query on the `SLOW_QUERY` table, you can get detailed information about how the database fetches the slow query information. However, this information is **not** available when you run `EXPLAIN ANALYZE` on the `CLUSTER_SLOW_QUERY` table.

Example:

```sql
EXPLAIN ANALYZE SELECT * FROM INFORMATION_SCHEMA.SLOW_QUERY LIMIT 1\G
```

```
*************************** 1. row ***************************
            id: Limit_7
       estRows: 1.00
       actRows: 1
          task: root
 access object: 
execution info: time:3.46ms, loops:2, RU:0.000000
 operator info: offset:0, count:1
        memory: N/A
          disk: N/A
*************************** 2. row ***************************
            id: └─MemTableScan_10
       estRows: 10000.00
       actRows: 64
          task: root
 access object: table:SLOW_QUERY
execution info: time:3.45ms, loops:1, initialize: 55.5µs, read_file: 1.21ms, parse_log: {time:4.11ms, concurrency:15}, total_file: 1, read_file: 1, read_size: 4.06 MB
 operator info: only search in the current 'tidb-slow.log' file
        memory: 1.26 MB
          disk: N/A
2 rows in set (0.01 sec)
```

In the output, check the following fields (formatted for readability) in the `execution info` section:

```
initialize: 55.5µs,
read_file: 1.21ms,
parse_log: {
  time:4.11ms,
  concurrency:15
},
total_file: 1,
read_file: 1,
read_size: 4.06 MB
```

| Field | Description |
|---|---|
| `initialize` | Time spent initializing |
| `read_file` | Time spent reading the slow log file |
| `parse_log.time` | Time spent parsing the slow log file |
| `parse_log.concurrency` | Concurrency for parsing the slow log file (set by [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency)) |
| `total_file` | Total number of slow log files |
| `read_file` | Number of slow log files that are read |
| `read_size` | Bytes read from the log file |
