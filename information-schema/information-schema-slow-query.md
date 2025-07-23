---
title: SLOW_QUERY
summary: 了解 `SLOW_QUERY` INFORMATION_SCHEMA 表。
---

# SLOW_QUERY

<CustomContent platform="tidb">

`SLOW_QUERY` 表提供了当前节点的慢查询信息，该信息是 TiDB [slow log file](/tidb-configuration-file.md#slow-query-file) 的解析结果。表中的列名对应于慢日志中的字段名。

</CustomContent>

<CustomContent platform="tidb-cloud">

`SLOW_QUERY` 表提供了当前节点的慢查询信息，该信息是 TiDB [slow log file](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#slow-query-file) 的解析结果。表中的列名对应于慢日志中的字段名。

</CustomContent>

> **Note:**
>
> 该表在 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群中不可用。

<CustomContent platform="tidb">

关于如何使用此表识别问题语句并优化查询性能，请参见 [Slow Query Log Document](/identify-slow-queries.md)。

</CustomContent>

```sql
USE INFORMATION_SCHEMA;
DESC SLOW_QUERY;
```

输出如下：

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
82 rows in set (0.00 sec)
```

当查询集群系统表时，TiDB 不会从所有节点获取数据，而是将相关计算下推到其他节点。执行计划如下：

```sql
DESC SELECT COUNT(*) FROM CLUSTER_SLOW_QUERY WHERE user = 'u1';
```

输出如下：

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

在上述执行计划中，`user = u1` 条件被下推到其他（`cop`） TiDB 节点，聚合操作符也被下推（图中的 `StreamAgg` 操作符）。

目前，由于系统表的统计信息未被收集，有时某些聚合操作符无法下推，导致执行缓慢。在这种情况下，你可以手动指定 SQL HINT 以下推聚合操作符。例如：

```sql
SELECT /*+ AGG_TO_COP() */ COUNT(*) FROM CLUSTER_SLOW_QUERY GROUP BY user;
```

## 查看执行信息

通过对 `SLOW_QUERY` 表运行 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 查询，可以获得数据库获取慢查询信息的详细过程信息。然而，在对 `CLUSTER_SLOW_QUERY` 表运行 `EXPLAIN ANALYZE` 时，此信息**不可用**。

示例：

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

在输出中，关注 `execution info` 部分的以下字段（为可读性而格式化）：

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

| 字段 | 描述 |
|---|---|
| `initialize` | 初始化所用时间 |
| `read_file` | 读取慢日志文件所用时间 |
| `parse_log.time` | 解析慢日志文件所用时间 |
| `parse_log.concurrency` | 解析慢日志的并发数（由 [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency) 设置） |
| `total_file` | 慢日志文件总数 |
| `read_file` | 读取的慢日志文件数 |
| `read_size` | 从日志文件读取的字节数 |