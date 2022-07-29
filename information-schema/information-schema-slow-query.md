---
title: SLOW_QUERY
summary: Learn the `SLOW_QUERY` information_schema table.
---

# SLOW_QUERY {#slow-query}

`SLOW_QUERY`テーブルは、現在のノードの低速クエリ情報を提供します。これは、TiDB低速ログファイルの解析結果です。表の列名は、低速ログのフィールド名に対応しています。

<CustomContent platform="tidb">

このテーブルを使用して問題のあるステートメントを特定し、クエリのパフォーマンスを向上させる方法については、 [遅いクエリログドキュメント](/identify-slow-queries.md)を参照してください。

</CustomContent>

{{< copyable "" >}}

```sql
USE information_schema;
DESC slow_query;
```

```
+---------------------------+---------------------+------+------+---------+-------+
| Field                     | Type                | Null | Key  | Default | Extra |
+---------------------------+---------------------+------+------+---------+-------+
| Time                      | timestamp(6)        | YES  |      | NULL    |       |
| Txn_start_ts              | bigint(20) unsigned | YES  |      | NULL    |       |
| User                      | varchar(64)         | YES  |      | NULL    |       |
| Host                      | varchar(64)         | YES  |      | NULL    |       |
| Conn_ID                   | bigint(20) unsigned | YES  |      | NULL    |       |
| Query_time                | double              | YES  |      | NULL    |       |
| Parse_time                | double              | YES  |      | NULL    |       |
| Compile_time              | double              | YES  |      | NULL    |       |
| Rewrite_time              | double              | YES  |      | NULL    |       |
| Preproc_subqueries        | bigint(20) unsigned | YES  |      | NULL    |       |
| Preproc_subqueries_time   | double              | YES  |      | NULL    |       |
| Optimize_time             | double              | YES  |      | NULL    |       |
| Wait_TS                   | double              | YES  |      | NULL    |       |
| Prewrite_time             | double              | YES  |      | NULL    |       |
| Wait_prewrite_binlog_time | double              | YES  |      | NULL    |       |
| Commit_time               | double              | YES  |      | NULL    |       |
| Get_commit_ts_time        | double              | YES  |      | NULL    |       |
| Commit_backoff_time       | double              | YES  |      | NULL    |       |
| Backoff_types             | varchar(64)         | YES  |      | NULL    |       |
| Resolve_lock_time         | double              | YES  |      | NULL    |       |
| Local_latch_wait_time     | double              | YES  |      | NULL    |       |
| Write_keys                | bigint(22)          | YES  |      | NULL    |       |
| Write_size                | bigint(22)          | YES  |      | NULL    |       |
| Prewrite_region           | bigint(22)          | YES  |      | NULL    |       |
| Txn_retry                 | bigint(22)          | YES  |      | NULL    |       |
| Cop_time                  | double              | YES  |      | NULL    |       |
| Process_time              | double              | YES  |      | NULL    |       |
| Wait_time                 | double              | YES  |      | NULL    |       |
| Backoff_time              | double              | YES  |      | NULL    |       |
| LockKeys_time             | double              | YES  |      | NULL    |       |
| Request_count             | bigint(20) unsigned | YES  |      | NULL    |       |
| Total_keys                | bigint(20) unsigned | YES  |      | NULL    |       |
| Process_keys              | bigint(20) unsigned | YES  |      | NULL    |       |
| DB                        | varchar(64)         | YES  |      | NULL    |       |
| Index_names               | varchar(100)        | YES  |      | NULL    |       |
| Is_internal               | tinyint(1)          | YES  |      | NULL    |       |
| Digest                    | varchar(64)         | YES  |      | NULL    |       |
| Stats                     | varchar(512)        | YES  |      | NULL    |       |
| Cop_proc_avg              | double              | YES  |      | NULL    |       |
| Cop_proc_p90              | double              | YES  |      | NULL    |       |
| Cop_proc_max              | double              | YES  |      | NULL    |       |
| Cop_proc_addr             | varchar(64)         | YES  |      | NULL    |       |
| Cop_wait_avg              | double              | YES  |      | NULL    |       |
| Cop_wait_p90              | double              | YES  |      | NULL    |       |
| Cop_wait_max              | double              | YES  |      | NULL    |       |
| Cop_wait_addr             | varchar(64)         | YES  |      | NULL    |       |
| Mem_max                   | bigint(20)          | YES  |      | NULL    |       |
| Disk_max                  | bigint(20)          | YES  |      | NULL    |       |
| Succ                      | tinyint(1)          | YES  |      | NULL    |       |
| Plan_from_cache           | tinyint(1)          | YES  |      | NULL    |       |
| Plan                      | longblob            | YES  |      | NULL    |       |
| Plan_digest               | varchar(128)        | YES  |      | NULL    |       |
| Prev_stmt                 | longblob            | YES  |      | NULL    |       |
| Query                     | longblob            | YES  |      | NULL    |       |
+---------------------------+---------------------+------+------+---------+-------+
54 rows in set (0.00 sec)
```

## CLUSTER_SLOW_QUERYテーブル {#cluster-slow-query-table}

`CLUSTER_SLOW_QUERY`テーブルは、クラスタのすべてのノードの低速クエリ情報を提供します。これは、TiDB低速ログファイルの解析結果です。 `CLUSTER_SLOW_QUERY`テーブルは`SLOW_QUERY`と同じように使用できます。 `CLUSTER_SLOW_QUERY`テーブルのテーブルスキーマは、 `INSTANCE`列が`CLUSTER_SLOW_QUERY`に追加されるという点で、 `SLOW_QUERY`テーブルのテーブルスキーマとは異なります。 `INSTANCE`列は、低速クエリの行情報のTiDBノードアドレスを表します。

<CustomContent platform="tidb">

このテーブルを使用して問題のあるステートメントを特定し、クエリのパフォーマンスを向上させる方法については、 [遅いクエリログドキュメント](/identify-slow-queries.md)を参照してください。

</CustomContent>

{{< copyable "" >}}

```sql
desc cluster_slow_query;
```

```sql
+---------------------------+---------------------+------+------+---------+-------+
| Field                     | Type                | Null | Key  | Default | Extra |
+---------------------------+---------------------+------+------+---------+-------+
| INSTANCE                  | varchar(64)         | YES  |      | NULL    |       |
| Time                      | timestamp(6)        | YES  |      | NULL    |       |
| Txn_start_ts              | bigint(20) unsigned | YES  |      | NULL    |       |
| User                      | varchar(64)         | YES  |      | NULL    |       |
| Host                      | varchar(64)         | YES  |      | NULL    |       |
| Conn_ID                   | bigint(20) unsigned | YES  |      | NULL    |       |
| Query_time                | double              | YES  |      | NULL    |       |
| Parse_time                | double              | YES  |      | NULL    |       |
| Compile_time              | double              | YES  |      | NULL    |       |
| Rewrite_time              | double              | YES  |      | NULL    |       |
| Preproc_subqueries        | bigint(20) unsigned | YES  |      | NULL    |       |
| Preproc_subqueries_time   | double              | YES  |      | NULL    |       |
| Optimize_time             | double              | YES  |      | NULL    |       |
| Wait_TS                   | double              | YES  |      | NULL    |       |
| Prewrite_time             | double              | YES  |      | NULL    |       |
| Wait_prewrite_binlog_time | double              | YES  |      | NULL    |       |
| Commit_time               | double              | YES  |      | NULL    |       |
| Get_commit_ts_time        | double              | YES  |      | NULL    |       |
| Commit_backoff_time       | double              | YES  |      | NULL    |       |
| Backoff_types             | varchar(64)         | YES  |      | NULL    |       |
| Resolve_lock_time         | double              | YES  |      | NULL    |       |
| Local_latch_wait_time     | double              | YES  |      | NULL    |       |
| Write_keys                | bigint(22)          | YES  |      | NULL    |       |
| Write_size                | bigint(22)          | YES  |      | NULL    |       |
| Prewrite_region           | bigint(22)          | YES  |      | NULL    |       |
| Txn_retry                 | bigint(22)          | YES  |      | NULL    |       |
| Cop_time                  | double              | YES  |      | NULL    |       |
| Process_time              | double              | YES  |      | NULL    |       |
| Wait_time                 | double              | YES  |      | NULL    |       |
| Backoff_time              | double              | YES  |      | NULL    |       |
| LockKeys_time             | double              | YES  |      | NULL    |       |
| Request_count             | bigint(20) unsigned | YES  |      | NULL    |       |
| Total_keys                | bigint(20) unsigned | YES  |      | NULL    |       |
| Process_keys              | bigint(20) unsigned | YES  |      | NULL    |       |
| DB                        | varchar(64)         | YES  |      | NULL    |       |
| Index_names               | varchar(100)        | YES  |      | NULL    |       |
| Is_internal               | tinyint(1)          | YES  |      | NULL    |       |
| Digest                    | varchar(64)         | YES  |      | NULL    |       |
| Stats                     | varchar(512)        | YES  |      | NULL    |       |
| Cop_proc_avg              | double              | YES  |      | NULL    |       |
| Cop_proc_p90              | double              | YES  |      | NULL    |       |
| Cop_proc_max              | double              | YES  |      | NULL    |       |
| Cop_proc_addr             | varchar(64)         | YES  |      | NULL    |       |
| Cop_wait_avg              | double              | YES  |      | NULL    |       |
| Cop_wait_p90              | double              | YES  |      | NULL    |       |
| Cop_wait_max              | double              | YES  |      | NULL    |       |
| Cop_wait_addr             | varchar(64)         | YES  |      | NULL    |       |
| Mem_max                   | bigint(20)          | YES  |      | NULL    |       |
| Disk_max                  | bigint(20)          | YES  |      | NULL    |       |
| Succ                      | tinyint(1)          | YES  |      | NULL    |       |
| Plan_from_cache           | tinyint(1)          | YES  |      | NULL    |       |
| Plan                      | longblob            | YES  |      | NULL    |       |
| Plan_digest               | varchar(128)        | YES  |      | NULL    |       |
| Prev_stmt                 | longblob            | YES  |      | NULL    |       |
| Query                     | longblob            | YES  |      | NULL    |       |
+---------------------------+---------------------+------+------+---------+-------+
55 rows in set (0.00 sec)
```

クラスタシステムテーブルが照会されると、TiDBはすべてのノードからデータを取得するのではなく、関連する計算を他のノードにプッシュダウンします。実行計画は次のとおりです。

{{< copyable "" >}}

```sql
desc SELECT count(*) FROM cluster_slow_query WHERE user = 'u1';
```

```
+--------------------------+----------+-----------+--------------------------+------------------------------------------------------+
| id                       | estRows  | task      | access object            | operator info                                        |
+--------------------------+----------+-----------+--------------------------+------------------------------------------------------+
| StreamAgg_20             | 1.00     | root      |                          | funcs:count(Column#53)->Column#51                    |
| └─TableReader_21         | 1.00     | root      |                          | data:StreamAgg_9                                     |
|   └─StreamAgg_9          | 1.00     | cop[tidb] |                          | funcs:count(1)->Column#53                            |
|     └─Selection_19       | 10.00    | cop[tidb] |                          | eq(information_schema.cluster_slow_query.user, "u1") |
|       └─TableFullScan_18 | 10000.00 | cop[tidb] | table:CLUSTER_SLOW_QUERY | keep order:false, stats:pseudo                       |
+--------------------------+----------+-----------+--------------------------+------------------------------------------------------+
```

上記の実行プランでは、 `user = u1`の条件が他の（ `cop` ）TiDBノードにプッシュダウンされ、集計演算子もプッシュダウンされます（グラフの`StreamAgg`演算子）。

現在、システムテーブルの統計が収集されていないため、一部の集計演算子をプッシュダウンできず、実行が遅くなることがあります。この場合、SQL HINTを手動で指定して、集計演算子をプッシュダウンできます。例えば：

{{< copyable "" >}}

```sql
SELECT /*+ AGG_TO_COP() */ count(*) FROM cluster_slow_query GROUP BY user;
```
