---
title: Explain Statements That Use Joins
summary: Learn about the execution plan information returned by the EXPLAIN statement in TiDB.
---

# テーブル結合を使用するステートメントを説明する {#explain-statements-that-use-joins}

TiDBでは、SQLオプティマイザーは、テーブルを結合する順序と、特定のSQLステートメントに対して最も効率的な結合アルゴリズムを決定する必要があります。このドキュメントの例は、次のサンプルデータに基づいています。

{{< copyable "" >}}

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

## インデックス参加 {#index-join}

結合する必要のある推定行数が少ない場合（通常は10000行未満）、インデックス結合方式を使用することをお勧めします。この結合方法は、MySQLで使用される主要な結合方法と同様に機能します。次の例では、オペレーター`├─TableReader_28(Build)`が最初にテーブル`t1`を読み取ります。一致する行ごとに、TiDBはテーブル`t2`をプローブします。

{{< copyable "" >}}

```sql
EXPLAIN SELECT /*+ INL_JOIN(t1, t2) */ * FROM t1 INNER JOIN t2 ON t1.id = t2.t1_id;
```

```sql
+---------------------------------+-----------+-----------+------------------------------+--------------------------------------------------------------------------------+
| id                              | estRows   | task      | access object                | operator info                                                                  |
+---------------------------------+-----------+-----------+------------------------------+--------------------------------------------------------------------------------+
| IndexJoin_10                    | 180000.00 | root      |                              | inner join, inner:IndexLookUp_9, outer key:test.t1.id, inner key:test.t2.t1_id |
| ├─TableReader_28(Build)         | 142020.00 | root      |                              | data:TableFullScan_27                                                          |
| │ └─TableFullScan_27            | 142020.00 | cop[tikv] | table:t1                     | keep order:false                                                               |
| └─IndexLookUp_9(Probe)          | 1.27      | root      |                              |                                                                                |
|   ├─IndexRangeScan_7(Build)     | 1.27      | cop[tikv] | table:t2, index:t1_id(t1_id) | range: decided by [eq(test.t2.t1_id, test.t1.id)], keep order:false            |
|   └─TableRowIDScan_8(Probe)     | 1.27      | cop[tikv] | table:t2                     | keep order:false                                                               |
+---------------------------------+-----------+-----------+------------------------------+--------------------------------------------------------------------------------+
6 rows in set (0.00 sec)
```

インデックス結合はメモリ使用量が効率的ですが、多数のプローブ操作が必要な場合は、他の結合方法よりも実行が遅くなる可能性があります。次のクエリも検討してください。

```sql
SELECT * FROM t1 INNER JOIN t2 ON t1.id=t2.t1_id WHERE t1.pad1 = 'value' and t2.pad1='value';
```

内部結合操作では、TiDBは結合の並べ替えを実装し、最初に`t1`または`t2`にアクセスする場合があります。 TiDBが`build`ステップを適用する最初のテーブルとして`t1`を選択すると、TiDBはテーブル`t2`をプローブする前に、述語`t1.col = 'value'`でフィルタリングできると仮定します。述語`t2.col='value'`のフィルターは、表`t2`の各プローブに適用されます。これは、他の結合方法よりも効率が低い可能性があります。

インデックス結合は、ビルド側が小さく、プローブ側が事前にインデックス付けされていて大きい場合に効果的です。インデックス結合のパフォーマンスがハッシュ結合よりも悪く、SQLオプティマイザによって選択されない次のクエリについて考えてみます。

{{< copyable "" >}}

```sql
-- DROP previously added index
ALTER TABLE t2 DROP INDEX t1_id;

EXPLAIN ANALYZE SELECT /*+ INL_JOIN(t1, t2) */  * FROM t1 INNER JOIN t2 ON t1.id = t2.t1_id WHERE t1.int_col = 1;
EXPLAIN ANALYZE SELECT /*+ HASH_JOIN(t1, t2) */  * FROM t1 INNER JOIN t2 ON t1.id = t2.t1_id WHERE t1.int_col = 1;
EXPLAIN ANALYZE SELECT * FROM t1 INNER JOIN t2 ON t1.id = t2.t1_id WHERE t1.int_col = 1;
```

```sql
Query OK, 0 rows affected (0.29 sec)

+-----------------------------+----------+---------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------+-----------------------+------+
| id                          | estRows  | actRows | task      | access object | execution info                                                                                                                                                                                                                                                                                    | operator info                                                                  | memory                | disk |
+-----------------------------+----------+---------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------+-----------------------+------+
| IndexJoin_13                | 90000.00 | 20000   | root      |               | time:613.19955ms, loops:21, inner:{total:42.494047ms, concurrency:5, task:12, construct:33.149671ms, fetch:9.322956ms, build:8.66µs}, probe:32.435355ms                                                                                                                                           | inner join, inner:TableReader_9, outer key:test.t2.t1_id, inner key:test.t1.id | 269.63341903686523 MB | N/A  |
| ├─TableReader_19(Build)     | 90000.00 | 90000   | root      |               | time:586.613252ms, loops:95, cop_task: {num: 3, max: 205.893949ms, min: 185.051354ms, avg: 194.878702ms, p95: 205.893949ms, max_proc_keys: 31715, p95_proc_keys: 31715, tot_proc: 332ms, tot_wait: 4ms, rpc_num: 4, rpc_time: 584.907774ms, copr_cache_hit_ratio: 0.00}, backoff{regionMiss: 2ms} | data:TableFullScan_18                                                          | 182.624906539917 MB   | N/A  |
| │ └─TableFullScan_18        | 90000.00 | 90000   | cop[tikv] | table:t2      | time:0ns, loops:0, tikv_task:{proc max:72ms, min:64ms, p80:72ms, p95:72ms, iters:102, tasks:3}                                                                                                                                                                                                    | keep order:false                                                               | N/A                   | N/A  |
| └─TableReader_9(Probe)      | 0.00     | 5       | root      |               | time:8.432051ms, loops:14, cop_task: {num: 14, max: 629.805µs, min: 226.129µs, avg: 420.979µs, p95: 629.805µs, max_proc_keys: 4, p95_proc_keys: 4, rpc_num: 15, rpc_time: 5.953229ms, copr_cache_hit_ratio: 0.00}                                                                                 | data:Selection_8                                                               | N/A                   | N/A  |
|   └─Selection_8             | 0.00     | 5       | cop[tikv] |               | time:0ns, loops:0, tikv_task:{proc max:0s, min:0s, p80:0s, p95:0s, iters:14, tasks:14}                                                                                                                                                                                                            | eq(test.t1.int_col, 1)                                                         | N/A                   | N/A  |
|     └─TableRangeScan_7      | 1.00     | 25      | cop[tikv] | table:t1      | time:0ns, loops:0, tikv_task:{proc max:0s, min:0s, p80:0s, p95:0s, iters:14, tasks:14}                                                                                                                                                                                                            | range: decided by [test.t2.t1_id], keep order:false                            | N/A                   | N/A  |
+-----------------------------+----------+---------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------+-----------------------+------+
6 rows in set (0.61 sec)

+------------------------------+----------+---------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+-----------------------+---------+
| id                           | estRows  | actRows | task      | access object | execution info                                                                                                                                                                                                                                          | operator info                                     | memory                | disk    |
+------------------------------+----------+---------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+-----------------------+---------+
| HashJoin_19                  | 90000.00 | 20000   | root      |               | time:406.098528ms, loops:22, build_hash_table:{total:148.574644ms, fetch:146.843636ms, build:1.731008ms}, probe:{concurrency:5, total:2.026547436s, max:406.039309ms, probe:205.337813ms, fetch:1.821209623s}                                           | inner join, equal:[eq(test.t1.id, test.t2.t1_id)] | 30.00731658935547 MB  | 0 Bytes |
| ├─TableReader_22(Build)      | 71.01    | 10000   | root      |               | time:147.072725ms, loops:12, cop_task: {num: 3, max: 145.847743ms, min: 50.932527ms, avg: 113.009029ms, p95: 145.847743ms, max_proc_keys: 31724, p95_proc_keys: 31724, tot_proc: 284ms, rpc_num: 3, rpc_time: 338.950488ms, copr_cache_hit_ratio: 0.00} | data:Selection_21                                 | 29.679713249206543 MB | N/A     |
| │ └─Selection_21             | 71.01    | 10000   | cop[tikv] |               | time:0ns, loops:0, tikv_task:{proc max:132ms, min:48ms, p80:132ms, p95:132ms, iters:83, tasks:3}                                                                                                                                                        | eq(test.t1.int_col, 1)                            | N/A                   | N/A     |
| │   └─TableFullScan_20       | 71010.00 | 71010   | cop[tikv] | table:t1      | time:0ns, loops:0, tikv_task:{proc max:128ms, min:48ms, p80:128ms, p95:128ms, iters:83, tasks:3}                                                                                                                                                        | keep order:false                                  | N/A                   | N/A     |
| └─TableReader_24(Probe)      | 90000.00 | 90000   | root      |               | time:365.918504ms, loops:91, cop_task: {num: 3, max: 398.62145ms, min: 338.460345ms, avg: 358.732721ms, p95: 398.62145ms, max_proc_keys: 31715, p95_proc_keys: 31715, tot_proc: 536ms, rpc_num: 3, rpc_time: 1.076128895s, copr_cache_hit_ratio: 0.00}  | data:TableFullScan_23                             | 182.62489891052246 MB | N/A     |
|   └─TableFullScan_23         | 90000.00 | 90000   | cop[tikv] | table:t2      | time:0ns, loops:0, tikv_task:{proc max:100ms, min:40ms, p80:100ms, p95:100ms, iters:102, tasks:3}                                                                                                                                                       | keep order:false                                  | N/A                   | N/A     |
+------------------------------+----------+---------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+-----------------------+---------+
6 rows in set (0.41 sec)

+------------------------------+----------+---------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+-----------------------+---------+
| id                           | estRows  | actRows | task      | access object | execution info                                                                                                                                                                                                                                           | operator info                                     | memory                | disk    |
+------------------------------+----------+---------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+-----------------------+---------+
| HashJoin_20                  | 90000.00 | 20000   | root      |               | time:441.897092ms, loops:21, build_hash_table:{total:138.600864ms, fetch:136.353899ms, build:2.246965ms}, probe:{concurrency:5, total:2.207403854s, max:441.850032ms, probe:148.01937ms, fetch:2.059384484s}                                             | inner join, equal:[eq(test.t1.id, test.t2.t1_id)] | 30.00731658935547 MB  | 0 Bytes |
| ├─TableReader_25(Build)      | 71.01    | 10000   | root      |               | time:138.081807ms, loops:12, cop_task: {num: 3, max: 134.702901ms, min: 53.356202ms, avg: 93.372186ms, p95: 134.702901ms, max_proc_keys: 31724, p95_proc_keys: 31724, tot_proc: 236ms, rpc_num: 3, rpc_time: 280.017658ms, copr_cache_hit_ratio: 0.00}   | data:Selection_24                                 | 29.680171966552734 MB | N/A     |
| │ └─Selection_24             | 71.01    | 10000   | cop[tikv] |               | time:0ns, loops:0, tikv_task:{proc max:80ms, min:52ms, p80:80ms, p95:80ms, iters:83, tasks:3}                                                                                                                                                            | eq(test.t1.int_col, 1)                            | N/A                   | N/A     |
| │   └─TableFullScan_23       | 71010.00 | 71010   | cop[tikv] | table:t1      | time:0ns, loops:0, tikv_task:{proc max:80ms, min:52ms, p80:80ms, p95:80ms, iters:83, tasks:3}                                                                                                                                                            | keep order:false                                  | N/A                   | N/A     |
| └─TableReader_22(Probe)      | 90000.00 | 90000   | root      |               | time:413.560548ms, loops:91, cop_task: {num: 3, max: 432.938474ms, min: 231.263355ms, avg: 365.710741ms, p95: 432.938474ms, max_proc_keys: 31715, p95_proc_keys: 31715, tot_proc: 488ms, rpc_num: 3, rpc_time: 1.097021983s, copr_cache_hit_ratio: 0.00} | data:TableFullScan_21                             | 182.62489891052246 MB | N/A     |
|   └─TableFullScan_21         | 90000.00 | 90000   | cop[tikv] | table:t2      | time:0ns, loops:0, tikv_task:{proc max:80ms, min:80ms, p80:80ms, p95:80ms, iters:102, tasks:3}                                                                                                                                                           | keep order:false                                  | N/A                   | N/A     |
+------------------------------+----------+---------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+-----------------------+---------+
6 rows in set (0.44 sec)
```

上記の例では、インデックス結合操作で`t1.int_col`のインデックスが欠落しています。このインデックスが追加されると、次の結果が示すように、操作のパフォーマンスが`0.61 sec`から`0.14 sec`に向上します。

```sql
-- Re-add index
ALTER TABLE t2 ADD INDEX (t1_id);

EXPLAIN ANALYZE SELECT /*+ INL_JOIN(t1, t2) */  * FROM t1 INNER JOIN t2 ON t1.id = t2.t1_id WHERE t1.int_col = 1;
EXPLAIN ANALYZE SELECT /*+ HASH_JOIN(t1, t2) */  * FROM t1 INNER JOIN t2 ON t1.id = t2.t1_id WHERE t1.int_col = 1;
EXPLAIN ANALYZE SELECT * FROM t1 INNER JOIN t2 ON t1.id = t2.t1_id WHERE t1.int_col = 1;
```

```sql
Query OK, 0 rows affected (3.65 sec)

+---------------------------------+----------+---------+-----------+------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------+-----------------------+------+
| id                              | estRows  | actRows | task      | access object                | execution info                                                                                                                                                                                                                                                           | operator info                                                                   | memory                | disk |
+---------------------------------+----------+---------+-----------+------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------+-----------------------+------+
| IndexJoin_11                    | 90000.00 | 0       | root      |                              | time:136.876686ms, loops:1, inner:{total:114.948158ms, concurrency:5, task:7, construct:5.329114ms, fetch:109.610054ms, build:2.38µs}, probe:1.699799ms                                                                                                                  | inner join, inner:IndexLookUp_10, outer key:test.t1.id, inner key:test.t2.t1_id | 29.864535331726074 MB | N/A  |
| ├─TableReader_32(Build)         | 10000.00 | 10000   | root      |                              | time:95.755212ms, loops:12, cop_task: {num: 3, max: 95.652443ms, min: 30.758712ms, avg: 57.545129ms, p95: 95.652443ms, max_proc_keys: 31724, p95_proc_keys: 31724, tot_proc: 124ms, rpc_num: 3, rpc_time: 172.528417ms, copr_cache_hit_ratio: 0.00}                      | data:Selection_31                                                               | 29.679298400878906 MB | N/A  |
| │ └─Selection_31                | 10000.00 | 10000   | cop[tikv] |                              | time:0ns, loops:0, tikv_task:{proc max:44ms, min:28ms, p80:44ms, p95:44ms, iters:84, tasks:3}                                                                                                                                                                            | eq(test.t1.int_col, 1)                                                          | N/A                   | N/A  |
| │   └─TableFullScan_30          | 71010.00 | 71010   | cop[tikv] | table:t1                     | time:0ns, loops:0, tikv_task:{proc max:44ms, min:28ms, p80:44ms, p95:44ms, iters:84, tasks:3}                                                                                                                                                                            | keep order:false                                                                | N/A                   | N/A  |
| └─IndexLookUp_10(Probe)         | 9.00     | 0       | root      |                              | time:103.93801ms, loops:7                                                                                                                                                                                                                                                |                                                                                 | 2.1787109375 KB       | N/A  |
|   ├─IndexRangeScan_8(Build)     | 9.00     | 0       | cop[tikv] | table:t2, index:t1_id(t1_id) | time:0s, loops:0, cop_task: {num: 7, max: 23.969244ms, min: 12.003682ms, avg: 14.659066ms, p95: 23.969244ms, tot_proc: 100ms, rpc_num: 7, rpc_time: 102.435966ms, copr_cache_hit_ratio: 0.00}, tikv_task:{proc max:24ms, min:12ms, p80:16ms, p95:24ms, iters:7, tasks:7} | range: decided by [eq(test.t2.t1_id, test.t1.id)], keep order:false             | N/A                   | N/A  |
|   └─TableRowIDScan_9(Probe)     | 9.00     | 0       | cop[tikv] | table:t2                     | time:0ns, loops:0                                                                                                                                                                                                                                                        | keep order:false                                                                | N/A                   | N/A  |
+---------------------------------+----------+---------+-----------+------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------+-----------------------+------+
7 rows in set (0.14 sec)

+------------------------------+----------+---------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+-----------------------+---------+
| id                           | estRows  | actRows | task      | access object | execution info                                                                                                                                                                                                                                         | operator info                                     | memory                | disk    |
+------------------------------+----------+---------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+-----------------------+---------+
| HashJoin_31                  | 90000.00 | 0       | root      |               | time:402.263795ms, loops:1, build_hash_table:{total:128.467151ms, fetch:126.871282ms, build:1.595869ms}, probe:{concurrency:5, total:2.010969815s, max:402.212295ms, probe:8.924769ms, fetch:2.002045046s}                                             | inner join, equal:[eq(test.t1.id, test.t2.t1_id)] | 29.689788818359375 MB | 0 Bytes |
| ├─TableReader_34(Build)      | 10000.00 | 10000   | root      |               | time:126.765972ms, loops:11, cop_task: {num: 3, max: 126.721293ms, min: 54.375481ms, avg: 84.518849ms, p95: 126.721293ms, max_proc_keys: 31724, p95_proc_keys: 31724, tot_proc: 208ms, rpc_num: 3, rpc_time: 253.478218ms, copr_cache_hit_ratio: 0.00} | data:Selection_33                                 | 29.679292678833008 MB | N/A     |
| │ └─Selection_33             | 10000.00 | 10000   | cop[tikv] |               | time:0ns, loops:0, tikv_task:{proc max:72ms, min:56ms, p80:72ms, p95:72ms, iters:84, tasks:3}                                                                                                                                                          | eq(test.t1.int_col, 1)                            | N/A                   | N/A     |
| │   └─TableFullScan_32       | 71010.00 | 71010   | cop[tikv] | table:t1      | time:0ns, loops:0, tikv_task:{proc max:72ms, min:56ms, p80:72ms, p95:72ms, iters:84, tasks:3}                                                                                                                                                          | keep order:false                                  | N/A                   | N/A     |
| └─TableReader_36(Probe)      | 90000.00 | 90000   | root      |               | time:400.447175ms, loops:90, cop_task: {num: 3, max: 400.838264ms, min: 309.474053ms, avg: 341.01943ms, p95: 400.838264ms, max_proc_keys: 31719, p95_proc_keys: 31719, tot_proc: 528ms, rpc_num: 3, rpc_time: 1.02298055s, copr_cache_hit_ratio: 0.00} | data:TableFullScan_35                             | 182.62786674499512 MB | N/A     |
|   └─TableFullScan_35         | 90000.00 | 90000   | cop[tikv] | table:t2      | time:0ns, loops:0, tikv_task:{proc max:108ms, min:72ms, p80:108ms, p95:108ms, iters:102, tasks:3}                                                                                                                                                      | keep order:false                                  | N/A                   | N/A     |
+------------------------------+----------+---------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+-----------------------+---------+
6 rows in set (0.40 sec)

+------------------------------+----------+---------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+-----------------------+---------+
| id                           | estRows  | actRows | task      | access object | execution info                                                                                                                                                                                                                                          | operator info                                     | memory                | disk    |
+------------------------------+----------+---------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+-----------------------+---------+
| HashJoin_32                  | 90000.00 | 0       | root      |               | time:356.282882ms, loops:1, build_hash_table:{total:154.187155ms, fetch:151.259305ms, build:2.92785ms}, probe:{concurrency:5, total:1.781087041s, max:356.238312ms, probe:7.406146ms, fetch:1.773680895s}                                               | inner join, equal:[eq(test.t1.id, test.t2.t1_id)] | 29.689788818359375 MB | 0 Bytes |
| ├─TableReader_41(Build)      | 10000.00 | 10000   | root      |               | time:151.190175ms, loops:11, cop_task: {num: 3, max: 151.055697ms, min: 56.214348ms, avg: 96.70463ms, p95: 151.055697ms, max_proc_keys: 31724, p95_proc_keys: 31724, tot_proc: 240ms, rpc_num: 3, rpc_time: 290.019942ms, copr_cache_hit_ratio: 0.00}   | data:Selection_40                                 | 29.679292678833008 MB | N/A     |
| │ └─Selection_40             | 10000.00 | 10000   | cop[tikv] |               | time:0ns, loops:0, tikv_task:{proc max:80ms, min:56ms, p80:80ms, p95:80ms, iters:84, tasks:3}                                                                                                                                                           | eq(test.t1.int_col, 1)                            | N/A                   | N/A     |
| │   └─TableFullScan_39       | 71010.00 | 71010   | cop[tikv] | table:t1      | time:0ns, loops:0, tikv_task:{proc max:80ms, min:56ms, p80:80ms, p95:80ms, iters:84, tasks:3}                                                                                                                                                           | keep order:false                                  | N/A                   | N/A     |
| └─TableReader_43(Probe)      | 90000.00 | 90000   | root      |               | time:354.68523ms, loops:90, cop_task: {num: 3, max: 354.313475ms, min: 328.460762ms, avg: 345.530558ms, p95: 354.313475ms, max_proc_keys: 31719, p95_proc_keys: 31719, tot_proc: 508ms, rpc_num: 3, rpc_time: 1.036492374s, copr_cache_hit_ratio: 0.00} | data:TableFullScan_42                             | 182.62786102294922 MB | N/A     |
|   └─TableFullScan_42         | 90000.00 | 90000   | cop[tikv] | table:t2      | time:0ns, loops:0, tikv_task:{proc max:84ms, min:64ms, p80:84ms, p95:84ms, iters:102, tasks:3}                                                                                                                                                          | keep order:false                                  | N/A                   | N/A     |
+------------------------------+----------+---------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+-----------------------+---------+
6 rows in set (0.36 sec)
```

> **ノート：**
>
> 上記の例では、SQLオプティマイザーはインデックス結合よりもパフォーマンスが悪いハッシュ結合プランを選択します。クエリの最適化は[NP完全問題](https://en.wikipedia.org/wiki/NP-completeness)であり、最適ではないプランが選択される可能性があります。これが頻繁なクエリである場合は、 [SQL計画管理](/sql-plan-management.md)を使用してヒントをクエリにバインドすることをお勧めします。これは、アプリケーションがTiDBに送信するクエリにヒントを挿入するよりも管理が簡単です。

### インデックス結合のバリエーション {#variations-of-index-join}

ヒント[`INL_JOIN`](/optimizer-hints.md#inl_joint1_name--tl_name-)を使用したインデックス結合操作は、外部テーブルで結合する前に、中間結果のハッシュテーブルを作成します。 TiDBは、ヒント[`INL_HASH_JOIN`](/optimizer-hints.md#inl_hash_join)を使用して外部テーブルにハッシュテーブルを作成することもサポートしています。インデックス結合のこれらの各バリエーションは、SQLオプティマイザによって自動的に選択されます。

### Configuration / コンフィグレーション {#configuration}

インデックス結合のパフォーマンスは、次のシステム変数の影響を受けます。

-   [`tidb_index_join_batch_size`](/system-variables.md#tidb_index_join_batch_size) （デフォルト値： `25000` ） `index lookup join`の操作のバッチサイズ。
-   [`tidb_index_lookup_join_concurrency`](/system-variables.md#tidb_index_lookup_join_concurrency) （デフォルト値： `4` ）-同時インデックスルックアップタスクの数。

## ハッシュ参加 {#hash-join}

ハッシュ結合操作では、TiDBは結合の`Build`側のデータを読み取ってハッシュテーブルにキャッシュし、次に結合の`Probe`側のデータを読み取って、ハッシュテーブルをプローブして必要な行にアクセスします。ハッシュ結合は、インデックス結合よりも実行に多くのメモリを必要としますが、結合する必要のある行が多数ある場合は、はるかに高速に実行されます。ハッシュ結合演算子はTiDBでマルチスレッド化されており、並行して実行されます。

ハッシュ結合の例は次のとおりです。

{{< copyable "" >}}

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

`HashJoin_27`の実行プロセスでは、TiDBは次の操作を順番に実行します。

1.  片側のデータをメモリにキャッシュし`Build` 。
2.  キャッシュされたデータに基づいて、片側にハッシュテーブルを作成し`Build` 。
3.  片側のデータを読み取り`Probe` 。
4.  片側のデータを使用して、ハッシュテーブルを調べ`Probe` 。
5.  修飾されたデータをユーザーに返します。

`EXPLAIN`の結果テーブルの`operator info`列には、クエリが内部結合か外部結合か、結合の条件など、 `HashJoin_27`に関するその他の情報も記録されます。上記の例では、クエリは内部結合であり、結合条件`equal:[eq(test.t1.id, test.t2.id)]`はクエリ条件`WHERE t1.id = t2.id`に部分的に対応しています。次の例の他のJoin演算子の演算子情報は、これに似ています。

### 実行時統計 {#runtime-statistics}

[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) （デフォルト値：1GB）を超えると、TiDBは`oom-use-tmp-storage`の値が`true` （デフォルト）であることを条件に一時ストレージの使用を試みます。これは、ハッシュ結合の一部として使用される`Build`演算子がディスク上に作成される可能性があることを意味します。メモリ使用量などの実行時統計は、 `EXPLAIN ANALYZE`の結果テーブルの`execution info`に表示されます。次の例は、1GB（デフォルト）の`tidb_mem_quota_query`クォータと500MBクォータの`EXPLAIN ANALYZE`の出力を示しています。 500MBでは、ディスクは一時ストレージに使用されます。

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

### Configuration / コンフィグレーション {#configuration}

ハッシュ結合のパフォーマンスは、次のシステム変数の影響を受けます。

-   [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) （デフォルト値：1GB）-クエリのメモリクォータを超えた場合、TiDBはメモリを節約するためにハッシュ結合の`Build`演算子をディスクにスピルしようとします。
-   [`tidb_hash_join_concurrency`](/system-variables.md#tidb_hash_join_concurrency) （デフォルト値： `5` ）-同時ハッシュ結合タスクの数。

## マージ参加 {#merge-join}

マージ結合は、結合の両側がソートされた順序で読み取られるときに適用される特別な種類の結合です。これは、*効率的なジッパーマージ*に似ていると説明できます。データは結合の`Build`側と`Probe`側の両方で読み取られるため、結合操作はストリーミング操作のように機能します。マージ結合は、ハッシュ結合よりもはるかに少ないメモリを必要としますが、並行して実行されません。

次に例を示します。

{{< copyable "" >}}

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

マージ結合演算子の実行プロセスでは、TiDBは次の操作を実行します。

1.  参加グループのすべてのデータを片側からメモリに読み込み`Build` 。
2.  片側のデータを読み取り`Probe` 。
3.  `Probe`側のデータの各行が`Build`側の完全な参加グループと一致するかどうかを比較します。同等の条件とは別に、同等ではない条件があります。ここで「一致」とは、主に非等価条件が満たされているかどうかを確認することを指します。結合グループは、すべての結合キー間で同じ値を持つデータを参照します。
