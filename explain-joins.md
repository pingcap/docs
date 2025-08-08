---
title: Explain Statements That Use Joins
summary: TiDB のEXPLAINステートメントによって返される実行プラン情報について学習します。
---

# テーブル結合を使用する文を説明する {#explain-statements-that-use-joins}

TiDBでは、SQLオプティマイザは、テーブルをどの順序で結合するか、そして特定のSQL文に対して最も効率的な結合アルゴリズムは何かを決定する必要があります。このドキュメントの例は、以下のサンプルデータに基づいています。

```sql
CREATE TABLE t1 (id BIGINT NOT NULL PRIMARY KEY auto_increment, pad1 BLOB, pad2 BLOB, pad3 BLOB, int_col INT NOT NULL DEFAULT 0);
CREATE TABLE t2 (id BIGINT NOT NULL PRIMARY KEY auto_increment, t1_id BIGINT NOT NULL, pad1 BLOB, pad2 BLOB, pad3 BLOB, INDEX(t1_id));
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM dual;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
UPDATE t1 SET int_col = 1 WHERE pad1 = (SELECT pad1 FROM t1 ORDER BY RAND() LIMIT 1);
SELECT SLEEP(1);
ANALYZE TABLE t1, t2;
```

## インデックス結合 {#index-join}

結合する必要がある行数が少ない場合（通常10,000行未満）、インデックス結合方式を使用することをお勧めします。この結合方式は、MySQLで使用される主要な結合方式と同様に機能します。次の例では、演算子`├─TableReader_29(Build)`最初にテーブル`t1`読み取ります。一致する行ごとに、TiDBはテーブル`t2`プローブします。

> **注記：**
>
> 返される実行プランにおいて、演算子`IndexJoin`および`Apply`のすべてのプローブ側子ノードについて、v6.4.0以降では`estRows`の意味がv6.4.0以前と異なります。詳細は[TiDB クエリ実行プランの概要](/explain-overview.md#understand-explain-output)参照してください。

```sql
EXPLAIN SELECT /*+ INL_JOIN(t1, t2) */ * FROM t1 INNER JOIN t2 ON t1.id = t2.t1_id;
```

```sql
+---------------------------------+----------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
| id                              | estRows  | task      | access object                | operator info                                                                                                             |
+---------------------------------+----------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
| IndexJoin_11                    | 90000.00 | root      |                              | inner join, inner:IndexLookUp_10, outer key:test.t1.id, inner key:test.t2.t1_id, equal cond:eq(test.t1.id, test.t2.t1_id) |
| ├─TableReader_29(Build)         | 71010.00 | root      |                              | data:TableFullScan_28                                                                                                     |
| │ └─TableFullScan_28            | 71010.00 | cop[tikv] | table:t1                     | keep order:false                                                                                                          |
| └─IndexLookUp_10(Probe)         | 90000.00 | root      |                              |                                                                                                                           |
|   ├─IndexRangeScan_8(Build)     | 90000.00 | cop[tikv] | table:t2, index:t1_id(t1_id) | range: decided by [eq(test.t2.t1_id, test.t1.id)], keep order:false                                                       |
|   └─TableRowIDScan_9(Probe)     | 90000.00 | cop[tikv] | table:t2                     | keep order:false                                                                                                          |
+---------------------------------+----------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
```

インデックス結合はメモリ使用量の点で効率的ですが、多数のプローブ操作が必要な場合、他の結合方法よりも実行速度が遅くなる可能性があります。次のクエリも検討してください。

```sql
SELECT * FROM t1 INNER JOIN t2 ON t1.id=t2.t1_id WHERE t1.pad1 = 'value' and t2.pad1='value';
```

内部結合操作において、TiDBは結合順序の変更を実装しており、最初に`t1`または`t2`アクセスする可能性があります。TiDBがステップ`build`適用する最初のテーブルとしてテーブル`t1`を選択し、その後、テーブル`t2`プローブする前に述語`t1.pad1 = 'value'`でフィルタリングできると仮定します。述語`t2.pad1='value'`のフィルタはテーブル`t2`の各プローブに適用されるため、他の結合方法よりも効率が低下する可能性があります。

インデックス結合は、ビルド側が小さく、プローブ側が事前にインデックス化されていて大きい場合に効果的です。次のクエリでは、インデックス結合のパフォーマンスはハッシュ結合よりも低く、SQLオプティマイザーによって選択されません。

```sql
-- DROP previously added index
ALTER TABLE t2 DROP INDEX t1_id;

EXPLAIN ANALYZE SELECT /*+ INL_JOIN(t1, t2) */  * FROM t1 INNER JOIN t2 ON t1.id = t2.t1_id WHERE t1.int_col = 1;
EXPLAIN ANALYZE SELECT /*+ HASH_JOIN(t1, t2) */  * FROM t1 INNER JOIN t2 ON t1.id = t2.t1_id WHERE t1.int_col = 1;
EXPLAIN ANALYZE SELECT * FROM t1 INNER JOIN t2 ON t1.id = t2.t1_id WHERE t1.int_col = 1;
```

```sql
+-----------------------------+----------+---------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------+---------+------+
| id                          | estRows  | actRows | task      | access object | execution info                                                                                                                                                                                                                                                                                                           | operator info                                                                                                             | memory  | disk |
+-----------------------------+----------+---------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------+---------+------+
| IndexJoin_14                | 90000.00 | 0       | root      |               | time:330.2ms, loops:1, inner:{total:72.2ms, concurrency:5, task:12, construct:58.6ms, fetch:13.5ms, build:2.12µs}, probe:26.1ms                                                                                                                                                                                          | inner join, inner:TableReader_10, outer key:test.t2.t1_id, inner key:test.t1.id, equal cond:eq(test.t2.t1_id, test.t1.id) | 88.5 MB | N/A  |
| ├─TableReader_20(Build)     | 90000.00 | 90000   | root      |               | time:307.2ms, loops:96, cop_task: {num: 24, max: 130.6ms, min: 170.9µs, avg: 33.5ms, p95: 105ms, max_proc_keys: 10687, p95_proc_keys: 9184, tot_proc: 472ms, rpc_num: 24, rpc_time: 802.4ms, copr_cache_hit_ratio: 0.62, distsql_concurrency: 15}                                                                        | data:TableFullScan_19                                                                                                     | 58.6 MB | N/A  |
| │ └─TableFullScan_19        | 90000.00 | 90000   | cop[tikv] | table:t2      | tikv_task:{proc max:34ms, min:0s, avg: 15.3ms, p80:24ms, p95:30ms, iters:181, tasks:24}, scan_detail: {total_process_keys: 69744, total_process_keys_size: 217533936, total_keys: 69753, get_snapshot_time: 701.6µs, rocksdb: {delete_skipped_count: 97368, key_skipped_count: 236847, block: {cache_hit_count: 3509}}}  | keep order:false                                                                                                          | N/A     | N/A  |
| └─TableReader_10(Probe)     | 12617.92 | 0       | root      |               | time:11.9ms, loops:12, cop_task: {num: 42, max: 848.8µs, min: 199µs, avg: 451.8µs, p95: 846.2µs, max_proc_keys: 7, p95_proc_keys: 5, rpc_num: 42, rpc_time: 18.3ms, copr_cache_hit_ratio: 0.00, distsql_concurrency: 15}                                                                                                 | data:Selection_9                                                                                                          | N/A     | N/A  |
|   └─Selection_9             | 12617.92 | 0       | cop[tikv] |               | tikv_task:{proc max:0s, min:0s, avg: 0s, p80:0s, p95:0s, iters:42, tasks:42}, scan_detail: {total_process_keys: 56, total_process_keys_size: 174608, total_keys: 77, get_snapshot_time: 727.7µs, rocksdb: {block: {cache_hit_count: 154}}}                                                                               | eq(test.t1.int_col, 1)                                                                                                    | N/A     | N/A  |
|     └─TableRangeScan_8      | 90000.00 | 56      | cop[tikv] | table:t1      | tikv_task:{proc max:0s, min:0s, avg: 0s, p80:0s, p95:0s, iters:42, tasks:42}                                                                                                                                                                                                                                             | range: decided by [test.t2.t1_id], keep order:false                                                                       | N/A     | N/A  |
+-----------------------------+----------+---------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------+---------+------+

+------------------------------+----------+---------+-----------+---------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+---------+---------+
| id                           | estRows  | actRows | task      | access object | execution info                                                                                                                                                                                                                                                                                                         | operator info                                     | memory  | disk    |
+------------------------------+----------+---------+-----------+---------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+---------+---------+
| HashJoin_20                  | 90000.00 | 0       | root      |               | time:313.6ms, loops:1, build_hash_table:{total:24.6ms, fetch:21.2ms, build:3.32ms}, probe:{concurrency:5, total:1.57s, max:313.5ms, probe:18.9ms, fetch:1.55s}                                                                                                                                                         | inner join, equal:[eq(test.t1.id, test.t2.t1_id)] | 32.0 MB | 0 Bytes |
| ├─TableReader_23(Build)      | 9955.54  | 10000   | root      |               | time:23.6ms, loops:12, cop_task: {num: 11, max: 504.6µs, min: 203.7µs, avg: 377.4µs, p95: 504.6µs, rpc_num: 11, rpc_time: 3.92ms, copr_cache_hit_ratio: 1.00, distsql_concurrency: 15}                                                                                                                                 | data:Selection_22                                 | 14.9 MB | N/A     |
| │ └─Selection_22             | 9955.54  | 10000   | cop[tikv] |               | tikv_task:{proc max:104ms, min:3ms, avg: 24.4ms, p80:33ms, p95:104ms, iters:113, tasks:11}, scan_detail: {get_snapshot_time: 241.4µs, rocksdb: {block: {}}}                                                                                                                                                            | eq(test.t1.int_col, 1)                            | N/A     | N/A     |
| │   └─TableFullScan_21       | 71010.00 | 71010   | cop[tikv] | table:t1      | tikv_task:{proc max:101ms, min:3ms, avg: 23.8ms, p80:33ms, p95:101ms, iters:113, tasks:11}                                                                                                                                                                                                                             | keep order:false                                  | N/A     | N/A     |
| └─TableReader_25(Probe)      | 90000.00 | 90000   | root      |               | time:293.7ms, loops:91, cop_task: {num: 24, max: 105.7ms, min: 210.9µs, avg: 31.4ms, p95: 103.8ms, max_proc_keys: 10687, p95_proc_keys: 9184, tot_proc: 407ms, rpc_num: 24, rpc_time: 752.2ms, copr_cache_hit_ratio: 0.62, distsql_concurrency: 15}                                                                    | data:TableFullScan_24                             | 58.6 MB | N/A     |
|   └─TableFullScan_24         | 90000.00 | 90000   | cop[tikv] | table:t2      | tikv_task:{proc max:31ms, min:0s, avg: 13ms, p80:19ms, p95:26ms, iters:181, tasks:24}, scan_detail: {total_process_keys: 69744, total_process_keys_size: 217533936, total_keys: 69753, get_snapshot_time: 637.2µs, rocksdb: {delete_skipped_count: 97368, key_skipped_count: 236847, block: {cache_hit_count: 3509}}}  | keep order:false                                  | N/A     | N/A     |
+------------------------------+----------+---------+-----------+---------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+---------+---------+

+------------------------------+----------+---------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+---------+---------+
| id                           | estRows  | actRows | task      | access object | execution info                                                                                                                                                                                                                                                                                                           | operator info                                     | memory  | disk    |
+------------------------------+----------+---------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+---------+---------+
| HashJoin_21                  | 90000.00 | 0       | root      |               | time:331.7ms, loops:1, build_hash_table:{total:32.7ms, fetch:26ms, build:6.73ms}, probe:{concurrency:5, total:1.66s, max:331.3ms, probe:16ms, fetch:1.64s}                                                                                                                                                               | inner join, equal:[eq(test.t1.id, test.t2.t1_id)] | 32.3 MB | 0 Bytes |
| ├─TableReader_26(Build)      | 9955.54  | 10000   | root      |               | time:30.4ms, loops:13, cop_task: {num: 11, max: 1.87ms, min: 844.7µs, avg: 1.29ms, p95: 1.87ms, rpc_num: 11, rpc_time: 13.5ms, copr_cache_hit_ratio: 1.00, distsql_concurrency: 15}                                                                                                                                      | data:Selection_25                                 | 12.2 MB | N/A     |
| │ └─Selection_25             | 9955.54  | 10000   | cop[tikv] |               | tikv_task:{proc max:104ms, min:3ms, avg: 24.4ms, p80:33ms, p95:104ms, iters:113, tasks:11}, scan_detail: {get_snapshot_time: 521µs, rocksdb: {block: {}}}                                                                                                                                                                | eq(test.t1.int_col, 1)                            | N/A     | N/A     |
| │   └─TableFullScan_24       | 71010.00 | 71010   | cop[tikv] | table:t1      | tikv_task:{proc max:101ms, min:3ms, avg: 23.8ms, p80:33ms, p95:101ms, iters:113, tasks:11}                                                                                                                                                                                                                               | keep order:false                                  | N/A     | N/A     |
| └─TableReader_23(Probe)      | 90000.00 | 90000   | root      |               | time:308.6ms, loops:91, cop_task: {num: 24, max: 123.3ms, min: 518.9µs, avg: 32.4ms, p95: 113.4ms, max_proc_keys: 10687, p95_proc_keys: 9184, tot_proc: 499ms, rpc_num: 24, rpc_time: 776ms, copr_cache_hit_ratio: 0.62, distsql_concurrency: 15}                                                                        | data:TableFullScan_22                             | 58.6 MB | N/A     |
|   └─TableFullScan_22         | 90000.00 | 90000   | cop[tikv] | table:t2      | tikv_task:{proc max:44ms, min:0s, avg: 16.8ms, p80:27ms, p95:40ms, iters:181, tasks:24}, scan_detail: {total_process_keys: 69744, total_process_keys_size: 217533936, total_keys: 69753, get_snapshot_time: 955.4µs, rocksdb: {delete_skipped_count: 97368, key_skipped_count: 236847, block: {cache_hit_count: 3509}}}  | keep order:false                                  | N/A     | N/A     |
+------------------------------+----------+---------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+---------+---------+
```

上記の例では、インデックス結合操作で`t1.int_col`のインデックスが不足しています。このインデックスを追加すると、操作のパフォーマンスは`0.3 sec`から`0.06 sec`に向上します。次の結果がそれを示しています。

```sql
-- Re-add index
ALTER TABLE t2 ADD INDEX (t1_id);

EXPLAIN ANALYZE SELECT /*+ INL_JOIN(t1, t2) */  * FROM t1 INNER JOIN t2 ON t1.id = t2.t1_id WHERE t1.int_col = 1;
EXPLAIN ANALYZE SELECT /*+ HASH_JOIN(t1, t2) */  * FROM t1 INNER JOIN t2 ON t1.id = t2.t1_id WHERE t1.int_col = 1;
EXPLAIN ANALYZE SELECT * FROM t1 INNER JOIN t2 ON t1.id = t2.t1_id WHERE t1.int_col = 1;
```

```sql
+----------------------------------+----------+---------+-----------+------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------+-----------+------+
| id                               | estRows  | actRows | task      | access object                | execution info                                                                                                                                                                                                                                                                                                                                                                               | operator info                                                                                                             | memory    | disk |
+----------------------------------+----------+---------+-----------+------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------+-----------+------+
| IndexJoin_12                     | 90000.00 | 0       | root      |                              | time:65.6ms, loops:1, inner:{total:129.7ms, concurrency:5, task:7, construct:7.13ms, fetch:122.5ms, build:16.4µs}, probe:2.54ms                                                                                                                                                                                                                                                              | inner join, inner:IndexLookUp_11, outer key:test.t1.id, inner key:test.t2.t1_id, equal cond:eq(test.t1.id, test.t2.t1_id) | 28.7 MB   | N/A  |
| ├─TableReader_33(Build)          | 9955.54  | 10000   | root      |                              | time:15.4ms, loops:16, cop_task: {num: 11, max: 1.52ms, min: 211.5µs, avg: 416.8µs, p95: 1.52ms, rpc_num: 11, rpc_time: 4.36ms, copr_cache_hit_ratio: 1.00, distsql_concurrency: 15}                                                                                                                                                                                                         | data:Selection_32                                                                                                         | 13.9 MB   | N/A  |
| │ └─Selection_32                 | 9955.54  | 10000   | cop[tikv] |                              | tikv_task:{proc max:104ms, min:3ms, avg: 24.4ms, p80:33ms, p95:104ms, iters:113, tasks:11}, scan_detail: {get_snapshot_time: 185µs, rocksdb: {block: {}}}                                                                                                                                                                                                                                    | eq(test.t1.int_col, 1)                                                                                                    | N/A       | N/A  |
| │   └─TableFullScan_31           | 71010.00 | 71010   | cop[tikv] | table:t1                     | tikv_task:{proc max:101ms, min:3ms, avg: 23.8ms, p80:33ms, p95:101ms, iters:113, tasks:11}                                                                                                                                                                                                                                                                                                   | keep order:false                                                                                                          | N/A       | N/A  |
| └─IndexLookUp_11(Probe)          | 90000.00 | 0       | root      |                              | time:115.6ms, loops:7                                                                                                                                                                                                                                                                                                                                                                        |                                                                                                                           | 555 Bytes | N/A  |
|   ├─IndexRangeScan_9(Build)      | 90000.00 | 0       | cop[tikv] | table:t2, index:t1_id(t1_id) | time:114.3ms, loops:7, cop_task: {num: 7, max: 42ms, min: 1.3ms, avg: 16.2ms, p95: 42ms, tot_proc: 71ms, rpc_num: 7, rpc_time: 113.2ms, copr_cache_hit_ratio: 0.29, distsql_concurrency: 15}, tikv_task:{proc max:37ms, min:0s, avg: 11.3ms, p80:20ms, p95:37ms, iters:7, tasks:7}, scan_detail: {total_keys: 9296, get_snapshot_time: 141.9µs, rocksdb: {block: {cache_hit_count: 18592}}}  | range: decided by [eq(test.t2.t1_id, test.t1.id)], keep order:false                                                       | N/A       | N/A  |
|   └─TableRowIDScan_10(Probe)     | 90000.00 | 0       | cop[tikv] | table:t2                     |                                                                                                                                                                                                                                                                                                                                                                                              | keep order:false                                                                                                          | N/A       | N/A  |
+----------------------------------+----------+---------+-----------+------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------+-----------+------+

+------------------------------+----------+---------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+---------+---------+
| id                           | estRows  | actRows | task      | access object | execution info                                                                                                                                                                                                                                                                                                             | operator info                                     | memory  | disk    |
+------------------------------+----------+---------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+---------+---------+
| HashJoin_32                  | 90000.00 | 0       | root      |               | time:320.2ms, loops:1, build_hash_table:{total:19.3ms, fetch:16.8ms, build:2.52ms}, probe:{concurrency:5, total:1.6s, max:320.1ms, probe:16.1ms, fetch:1.58s}                                                                                                                                                              | inner join, equal:[eq(test.t1.id, test.t2.t1_id)] | 32.0 MB | 0 Bytes |
| ├─TableReader_35(Build)      | 9955.54  | 10000   | root      |               | time:18.6ms, loops:12, cop_task: {num: 11, max: 713.8µs, min: 197.3µs, avg: 368.5µs, p95: 713.8µs, rpc_num: 11, rpc_time: 3.83ms, copr_cache_hit_ratio: 1.00, distsql_concurrency: 15}                                                                                                                                     | data:Selection_34                                 | 14.9 MB | N/A     |
| │ └─Selection_34             | 9955.54  | 10000   | cop[tikv] |               | tikv_task:{proc max:104ms, min:3ms, avg: 24.4ms, p80:33ms, p95:104ms, iters:113, tasks:11}, scan_detail: {get_snapshot_time: 178.9µs, rocksdb: {block: {}}}                                                                                                                                                                | eq(test.t1.int_col, 1)                            | N/A     | N/A     |
| │   └─TableFullScan_33       | 71010.00 | 71010   | cop[tikv] | table:t1      | tikv_task:{proc max:101ms, min:3ms, avg: 23.8ms, p80:33ms, p95:101ms, iters:113, tasks:11}                                                                                                                                                                                                                                 | keep order:false                                  | N/A     | N/A     |
| └─TableReader_37(Probe)      | 90000.00 | 90000   | root      |               | time:304.4ms, loops:91, cop_task: {num: 24, max: 114ms, min: 251.1µs, avg: 33.1ms, p95: 110.4ms, max_proc_keys: 10687, p95_proc_keys: 9184, tot_proc: 492ms, rpc_num: 24, rpc_time: 793ms, copr_cache_hit_ratio: 0.62, distsql_concurrency: 15}                                                                            | data:TableFullScan_36                             | 58.6 MB | N/A     |
|   └─TableFullScan_36         | 90000.00 | 90000   | cop[tikv] | table:t2      | tikv_task:{proc max:38ms, min:3ms, avg: 14.1ms, p80:23ms, p95:35ms, iters:181, tasks:24}, scan_detail: {total_process_keys: 69744, total_process_keys_size: 217533936, total_keys: 139497, get_snapshot_time: 577.2µs, rocksdb: {delete_skipped_count: 44208, key_skipped_count: 253431, block: {cache_hit_count: 3527}}}  | keep order:false                                  | N/A     | N/A     |
+------------------------------+----------+---------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+---------+---------+

+------------------------------+----------+---------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+---------+---------+
| id                           | estRows  | actRows | task      | access object | execution info                                                                                                                                                                                                                                                                                                             | operator info                                     | memory  | disk    |
+------------------------------+----------+---------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+---------+---------+
| HashJoin_33                  | 90000.00 | 0       | root      |               | time:306.3ms, loops:1, build_hash_table:{total:20.5ms, fetch:17.1ms, build:3.45ms}, probe:{concurrency:5, total:1.53s, max:305.9ms, probe:17.1ms, fetch:1.51s}                                                                                                                                                             | inner join, equal:[eq(test.t1.id, test.t2.t1_id)] | 32.0 MB | 0 Bytes |
| ├─TableReader_42(Build)      | 9955.54  | 10000   | root      |               | time:19.6ms, loops:12, cop_task: {num: 11, max: 1.07ms, min: 246.1µs, avg: 600µs, p95: 1.07ms, rpc_num: 11, rpc_time: 6.17ms, copr_cache_hit_ratio: 1.00, distsql_concurrency: 15}                                                                                                                                         | data:Selection_41                                 | 19.7 MB | N/A     |
| │ └─Selection_41             | 9955.54  | 10000   | cop[tikv] |               | tikv_task:{proc max:104ms, min:3ms, avg: 24.4ms, p80:33ms, p95:104ms, iters:113, tasks:11}, scan_detail: {get_snapshot_time: 282.9µs, rocksdb: {block: {}}}                                                                                                                                                                | eq(test.t1.int_col, 1)                            | N/A     | N/A     |
| │   └─TableFullScan_40       | 71010.00 | 71010   | cop[tikv] | table:t1      | tikv_task:{proc max:101ms, min:3ms, avg: 23.8ms, p80:33ms, p95:101ms, iters:113, tasks:11}                                                                                                                                                                                                                                 | keep order:false                                  | N/A     | N/A     |
| └─TableReader_44(Probe)      | 90000.00 | 90000   | root      |               | time:289.2ms, loops:91, cop_task: {num: 24, max: 108.2ms, min: 252.8µs, avg: 31.3ms, p95: 106.1ms, max_proc_keys: 10687, p95_proc_keys: 9184, tot_proc: 445ms, rpc_num: 24, rpc_time: 750.4ms, copr_cache_hit_ratio: 0.62, distsql_concurrency: 15}                                                                        | data:TableFullScan_43                             | 58.6 MB | N/A     |
|   └─TableFullScan_43         | 90000.00 | 90000   | cop[tikv] | table:t2      | tikv_task:{proc max:31ms, min:3ms, avg: 13.3ms, p80:24ms, p95:30ms, iters:181, tasks:24}, scan_detail: {total_process_keys: 69744, total_process_keys_size: 217533936, total_keys: 139497, get_snapshot_time: 730.2µs, rocksdb: {delete_skipped_count: 44208, key_skipped_count: 253431, block: {cache_hit_count: 3527}}}  | keep order:false                                  | N/A     | N/A     |
+------------------------------+----------+---------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+---------+---------+
```

> **注記：**
>
> 上記の例では、SQLオプティマイザはインデックス結合よりもパフォーマンスの低いハッシュ結合プランを選択します。クエリ最適化は[NP完全問題](https://en.wikipedia.org/wiki/NP-completeness)であり、最適ではないプランが選択される場合があります。頻繁に実行されるクエリの場合は、 [SQLプラン管理](/sql-plan-management.md)使用してクエリにヒントをバインドすることをお勧めします。これは、アプリケーションがTiDBに送信するクエリにヒントを挿入するよりも管理が容易です。

### インデックス結合のバリエーション {#variations-of-index-join}

ヒント[`INL_JOIN`](/optimizer-hints.md#inl_joint1_name--tl_name-)使用したインデックス結合操作では、外部テーブルに結合する前に中間結果のハッシュテーブルが作成されます。TiDBは、ヒント[`INL_HASH_JOIN`](/optimizer-hints.md#inl_hash_join)を使用した外部テーブルへのハッシュテーブルの作成もサポートしています。これらのインデックス結合の各バリエーションは、SQLオプティマイザによって自動的に選択されます。

### コンフィグレーション {#configuration}

インデックス結合のパフォーマンスは、次のシステム変数の影響を受けます。

-   [`tidb_index_join_batch_size`](/system-variables.md#tidb_index_join_batch_size) (デフォルト値: `25000` ) - `index lookup join`操作のバッチ サイズ。
-   [`tidb_index_lookup_join_concurrency`](/system-variables.md#tidb_index_lookup_join_concurrency) (デフォルト値: `4` ) - 同時インデックス検索タスクの数。

## ハッシュ結合 {#hash-join}

ハッシュ結合操作では、TiDBは結合の`Build`側のデータを読み取ってハッシュテーブルにキャッシュし、次に結合の`Probe`側のデータを読み取り、ハッシュテーブルを参照して必要な行にアクセスします。ハッシュ結合はインデックス結合よりも多くのメモリを必要としますが、結合する行数が多い場合ははるかに高速に実行されます。ハッシュ結合演算子はTiDBでマルチスレッド化されており、並列実行されます。

ハッシュ結合の例は次のとおりです。

```sql
EXPLAIN SELECT /*+ HASH_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

```sql
+-----------------------------+-----------+-----------+---------------+------------------------------------------------+
| id                          | estRows   | task      | access object | operator info                                  |
+-----------------------------+-----------+-----------+---------------+------------------------------------------------+
| HashJoin_27                 | 142020.00 | root      |               | inner join, equal:[eq(test.t1.id, test.t2.id)] |
| ├─TableReader_29(Build)     | 142020.00 | root      |               | data:TableFullScan_28                          |
| │ └─TableFullScan_28        | 142020.00 | cop[tikv] | table:t1      | keep order:false                               |
| └─TableReader_31(Probe)     | 180000.00 | root      |               | data:TableFullScan_30                          |
|   └─TableFullScan_30        | 180000.00 | cop[tikv] | table:t2      | keep order:false                               |
+-----------------------------+-----------+-----------+---------------+------------------------------------------------+
5 rows in set (0.00 sec)
```

`HashJoin_27`の実行プロセスでは、TiDB は次の操作を順番に実行します。

1.  `Build`面分のデータをメモリにキャッシュします。
2.  キャッシュされたデータに基づいて`Build`側にハッシュ テーブルを構築します。
3.  `Probe`面のデータを読み取ります。
4.  `Probe`側のデータを使用してハッシュ テーブルをプローブします。
5.  適格なデータをユーザーに返します。

結果テーブル`EXPLAIN`の`operator info`列には、クエリが内部結合か外部結合か、結合条件など、 `HashJoin_27`に関するその他の情報も記録されます。上記の例では、クエリは内部結合であり、結合条件`equal:[eq(test.t1.id, test.t2.id)]`はクエリ条件`WHERE t1.id = t2.id`と部分的に一致しています。以降の例における他の結合演算子の演算子情報も、これと同様です。

### 実行時統計 {#runtime-statistics}

[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) (デフォルト値: 1 GB) を超え、 [`tidb_enable_tmp_storage_on_oom`](/system-variables.md#tidb_enable_tmp_storage_on_oom)値が`ON` (デフォルト) の場合、TiDB は一時storageの使用を試み、ハッシュ結合の一部として使用される`Build`演算子をディスク上に作成する可能性があります。メモリ使用量などの実行時統計は、結果テーブル`EXPLAIN ANALYZE`の`execution info`に記録されます。次の例は、1 GB (デフォルト) と`tidb_mem_quota_query`の 500 MB のクォータで`EXPLAIN ANALYZE`実行した場合の出力を示しています。500 MB の場合、ディスクは一時storageとして使用されます。

```sql
EXPLAIN ANALYZE SELECT /*+ HASH_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
SET tidb_mem_quota_query=500 * 1024 * 1024;
EXPLAIN ANALYZE SELECT /*+ HASH_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

```sql
+-----------------------------+-----------+---------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------+-----------------------+---------+
| id                          | estRows   | actRows | task      | access object | execution info                                                                                                                                                                                                                                           | operator info                                  | memory                | disk    |
+-----------------------------+-----------+---------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------+-----------------------+---------+
| HashJoin_27                 | 142020.00 | 71010   | root      |               | time:647.508572ms, loops:72, build_hash_table:{total:579.254415ms, fetch:566.91012ms, build:12.344295ms}, probe:{concurrency:5, total:3.23315006s, max:647.520113ms, probe:330.884716ms, fetch:2.902265344s}                                             | inner join, equal:[eq(test.t1.id, test.t2.id)] | 209.61642456054688 MB | 0 Bytes |
| ├─TableReader_29(Build)     | 142020.00 | 71010   | root      |               | time:567.088247ms, loops:72, cop_task: {num: 2, max: 569.809411ms, min: 369.67451ms, avg: 469.74196ms, p95: 569.809411ms, max_proc_keys: 39245, p95_proc_keys: 39245, tot_proc: 400ms, rpc_num: 2, rpc_time: 939.447231ms, copr_cache_hit_ratio: 0.00}   | data:TableFullScan_28                          | 210.2100534439087 MB  | N/A     |
| │ └─TableFullScan_28        | 142020.00 | 71010   | cop[tikv] | table:t1      | proc max:64ms, min:48ms, p80:64ms, p95:64ms, iters:79, tasks:2                                                                                                                                                                                           | keep order:false                               | N/A                   | N/A     |
| └─TableReader_31(Probe)     | 180000.00 | 90000   | root      |               | time:337.233636ms, loops:91, cop_task: {num: 3, max: 569.790741ms, min: 332.758911ms, avg: 421.543165ms, p95: 569.790741ms, max_proc_keys: 31719, p95_proc_keys: 31719, tot_proc: 500ms, rpc_num: 3, rpc_time: 1.264570696s, copr_cache_hit_ratio: 0.00} | data:TableFullScan_30                          | 267.1126985549927 MB  | N/A     |
|   └─TableFullScan_30        | 180000.00 | 90000   | cop[tikv] | table:t2      | proc max:84ms, min:72ms, p80:84ms, p95:84ms, iters:102, tasks:3                                                                                                                                                                                          | keep order:false                               | N/A                   | N/A     |
+-----------------------------+-----------+---------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------+-----------------------+---------+
5 rows in set (0.65 sec)

Query OK, 0 rows affected (0.00 sec)

+-----------------------------+-----------+---------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------+-----------------------+----------------------+
| id                          | estRows   | actRows | task      | access object | execution info                                                                                                                                                                                                                                           | operator info                                  | memory                | disk                 |
+-----------------------------+-----------+---------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------+-----------------------+----------------------+
| HashJoin_27                 | 142020.00 | 71010   | root      |               | time:963.983353ms, loops:72, build_hash_table:{total:775.961447ms, fetch:503.789677ms, build:272.17177ms}, probe:{concurrency:5, total:4.805454793s, max:963.973133ms, probe:922.156835ms, fetch:3.883297958s}                                           | inner join, equal:[eq(test.t1.id, test.t2.id)] | 93.53974533081055 MB  | 210.7459259033203 MB |
| ├─TableReader_29(Build)     | 142020.00 | 71010   | root      |               | time:504.062018ms, loops:72, cop_task: {num: 2, max: 509.276857ms, min: 402.66386ms, avg: 455.970358ms, p95: 509.276857ms, max_proc_keys: 39245, p95_proc_keys: 39245, tot_proc: 384ms, rpc_num: 2, rpc_time: 911.893237ms, copr_cache_hit_ratio: 0.00}  | data:TableFullScan_28                          | 210.20934200286865 MB | N/A                  |
| │ └─TableFullScan_28        | 142020.00 | 71010   | cop[tikv] | table:t1      | proc max:88ms, min:72ms, p80:88ms, p95:88ms, iters:79, tasks:2                                                                                                                                                                                           | keep order:false                               | N/A                   | N/A                  |
| └─TableReader_31(Probe)     | 180000.00 | 90000   | root      |               | time:363.058382ms, loops:91, cop_task: {num: 3, max: 412.659191ms, min: 358.489688ms, avg: 391.463008ms, p95: 412.659191ms, max_proc_keys: 31719, p95_proc_keys: 31719, tot_proc: 484ms, rpc_num: 3, rpc_time: 1.174326746s, copr_cache_hit_ratio: 0.00} | data:TableFullScan_30                          | 267.11340618133545 MB | N/A                  |
|   └─TableFullScan_30        | 180000.00 | 90000   | cop[tikv] | table:t2      | proc max:92ms, min:64ms, p80:92ms, p95:92ms, iters:102, tasks:3                                                                                                                                                                                          | keep order:false                               | N/A                   | N/A                  |
+-----------------------------+-----------+---------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------+-----------------------+----------------------+
5 rows in set (0.98 sec)
```

### コンフィグレーション {#configuration}

ハッシュ結合のパフォーマンスは、次のシステム変数の影響を受けます。

-   [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) (デフォルト値: 1 GB) - クエリのメモリクォータを超えた場合、TiDB はメモリを節約するためにハッシュ結合の`Build`の演算子をディスクに書き出そうとします。
-   [`tidb_hash_join_concurrency`](/system-variables.md#tidb_hash_join_concurrency) (デフォルト値: `5` ) - 同時ハッシュ結合タスクの数。

### 関連する最適化 {#related-optimizations}

TiDBは、ハッシュ結合のパフォーマンスを最適化し、実行速度を大幅に向上させるランタイムフィルタ機能を提供します。具体的な最適化の使用方法については、 [ランタイムフィルター](/runtime-filter.md)参照してください。

## マージ結合 {#merge-join}

マージ結合は、結合の両側がソート順に読み込まれる場合に適用される特殊な結合です。*効率的なジッパーマージ*に似ています。結合の`Build`と`Probe`番目の両側でデータが読み込まれるため、結合操作はストリーミング操作のように機能します。マージ結合はハッシュ結合よりもはるかに少ないメモリを必要としますが、並列実行は行われません。

次に例を示します。

```sql
EXPLAIN SELECT /*+ MERGE_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

```sql
+-----------------------------+-----------+-----------+---------------+-------------------------------------------------------+
| id                          | estRows   | task      | access object | operator info                                         |
+-----------------------------+-----------+-----------+---------------+-------------------------------------------------------+
| MergeJoin_7                 | 142020.00 | root      |               | inner join, left key:test.t1.id, right key:test.t2.id |
| ├─TableReader_12(Build)     | 180000.00 | root      |               | data:TableFullScan_11                                 |
| │ └─TableFullScan_11        | 180000.00 | cop[tikv] | table:t2      | keep order:true                                       |
| └─TableReader_10(Probe)     | 142020.00 | root      |               | data:TableFullScan_9                                  |
|   └─TableFullScan_9         | 142020.00 | cop[tikv] | table:t1      | keep order:true                                       |
+-----------------------------+-----------+-----------+---------------+-------------------------------------------------------+
5 rows in set (0.00 sec)
```

マージ結合演算子の実行プロセスでは、TiDB は次の操作を実行します。

1.  Join Group のすべてのデータを`Build`側からメモリに読み込みます。
2.  `Probe`面のデータを読み取ります。
3.  `Probe`側の各データ行が`Build`側の結合グループと完全に一致するかどうかを比較します。等価条件の他に、非等価条件もあります。ここでの「一致」とは、主に非等価条件が満たされているかどうかの確認を指します。結合グループとは、すべての結合キーの中で同じ値を持つデータを指します。
