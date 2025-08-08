---
title: SLOW_QUERY
summary: SLOW_QUERY` INFORMATION_SCHEMA テーブルについて学習します。
---

# 遅いクエリ {#slow-query}

<CustomContent platform="tidb">

`SLOW_QUERY`テーブルは、TiDB [遅いログファイル](/tidb-configuration-file.md#slow-query-file)の解析結果である、現在のノードのスロークエリ情報を提供します。テーブル内の列名は、スローログ内のフィールド名に対応しています。

</CustomContent>

<CustomContent platform="tidb-cloud">

`SLOW_QUERY`テーブルは、TiDB [遅いログファイル](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#slow-query-file)の解析結果である、現在のノードのスロークエリ情報を提供します。テーブル内の列名は、スローログ内のフィールド名に対応しています。

</CustomContent>

> **注記：**
>
> このテーブルは[TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)クラスターでは使用できません。

<CustomContent platform="tidb">

この表を使用して問題のあるステートメントを識別し、クエリのパフォーマンスを向上させる方法については、 [スロークエリログドキュメント](/identify-slow-queries.md)参照してください。

</CustomContent>

```sql
USE INFORMATION_SCHEMA;
DESC SLOW_QUERY;
```

出力は次のようになります。

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

`Query`列目のステートメントの最大長は、 [`tidb_stmt_summary_max_sql_length`](/system-variables.md#tidb_stmt_summary_max_sql_length-new-in-v40)システム変数によって制限されます。

## CLUSTER_SLOW_QUERY テーブル {#cluster-slow-query-table}

`CLUSTER_SLOW_QUERY`テーブル`CLUSTER_SLOW_QUERY` 、クラスター内のすべてのノードのスロークエリ情報を提供します。これは、TiDBスローログファイルの解析結果です。3 テーブルは`CLUSTER_SLOW_QUERY` `SLOW_QUERY`と同じように使用できます。7 テーブルのテーブルスキーマは、 `CLUSTER_SLOW_QUERY`列に`INSTANCE`列が追加されている点で`SLOW_QUERY`テーブルと異なります。15 `INSTANCE`は、スロークエリの行情報の TiDB ノードアドレスを表します。

> **注記：**
>
> このテーブルは[TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)クラスターでは使用できません。

<CustomContent platform="tidb">

この表を使用して問題のあるステートメントを識別し、クエリのパフォーマンスを向上させる方法については、 [スロークエリログドキュメント](/identify-slow-queries.md)参照してください。

</CustomContent>

```sql
DESC CLUSTER_SLOW_QUERY;
```

出力は次のようになります。

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

クラスタシステムテーブルへのクエリ実行時、TiDBはすべてのノードからデータを取得するのではなく、関連する計算を他のノードにプッシュダウンします。実行プランは以下のとおりです。

```sql
DESC SELECT COUNT(*) FROM CLUSTER_SLOW_QUERY WHERE user = 'u1';
```

出力は次のようになります。

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

上記の実行プランでは、 `user = u1`条件が他の（ `cop` ）TiDBノードにプッシュダウンされ、集計演算子もプッシュダウンされます（グラフの`StreamAgg`の演算子）。

現在、システムテーブルの統計情報が収集されていないため、一部の集計演算子をプッシュダウンできず、実行速度が低下することがあります。このような場合は、SQL HINTを手動で指定して、集計演算子をプッシュダウンすることができます。例：

```sql
SELECT /*+ AGG_TO_COP() */ COUNT(*) FROM CLUSTER_SLOW_QUERY GROUP BY user;
```

## 実行情報をビュー {#view-execution-information}

`SLOW_QUERY`テーブルで[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)クエリを実行すると、データベースがスロークエリ情報を取得する方法に関する詳細な情報を取得できます。ただし、 `CLUSTER_SLOW_QUERY`テーブルで`EXPLAIN ANALYZE`を実行しても、この情報は取得でき**ません**。

例：

```sql
EXPLAIN ANALYZE SELECT * FROM INFORMATION_SCHEMA.SLOW_QUERY LIMIT 1\G
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

出力では、セクション`execution info`の次のフィールド (読みやすいようにフォーマットされています) を確認します。

    initialize: 55.5µs,
    read_file: 1.21ms,
    parse_log: {
      time:4.11ms,
      concurrency:15
    },
    total_file: 1,
    read_file: 1,
    read_size: 4.06 MB

| 分野                      | 説明                                                                                                            |
| ----------------------- | ------------------------------------------------------------------------------------------------------------- |
| `initialize`            | 初期化にかかった時間                                                                                                    |
| `read_file`             | 遅いログファイルの読み取りにかかった時間                                                                                          |
| `parse_log.time`        | スローログファイルの解析にかかった時間                                                                                           |
| `parse_log.concurrency` | スローログファイルの解析の同時実行性（ [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency)に設定） |
| `total_file`            | スローログファイルの合計数                                                                                                 |
| `read_file`             | 読み取られる遅いログファイルの数                                                                                              |
| `read_size`             | ログファイルから読み取られたバイト数                                                                                            |
