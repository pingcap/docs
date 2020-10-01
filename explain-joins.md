---
title: Explain Statements Using Joins
summary: Learn about the execution plan information returned by the `EXPLAIN` statement in TiDB.
---

# Explain Statements Using Joins

In TiDB, the SQL Optimizer needs to decide which order tables should be joined in, and what is the most efficient join algorithm for a particular SQL statement. The examples are based on the following sample data:

{{< copyable "sql" >}}

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

## Index Join

If the estimated rows that need to be joined is small (typically less than 10000 rows), using the Index Join method is preferable. This method of join works similar to the primary method of join used in MySQL. In the following example, the operator `├─TableReader_28(Build)` first reads the table `t1`. For each row that matches, TiDB will probe the table `t2`:

{{< copyable "sql" >}}

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

Index join is efficient in memory usage, but may be slower to execute than other join methods when a large number of probe operations are required. Consider also the following query:

```sql
SELECT * FROM t1 INNER JOIN t2 ON t1.id=t2.t1_id WHERE t1.pad1 = 'value' and t2.pad1='value';
```

On an inner join, TiDB will apply join reordering and might access either `t1` or `t2` first. Assuming that TiDB selects `t1` as the first table to apply the `Build` step, it will be able to filter on the predicate `t1.col = 'value'` before probing the table `t2`. The filter for the predicate `t2.col='value'` will be applied on each probe of table `t2`, which may be less efficient than other join methods.

Index Join is effective if the build side is small and the probe side is pre-indexed and large. Consider the following query where the index join performs much better than the hash join:

{{< copyable "sql" >}}

```sql
EXPLAIN ANALYZE SELECT /*+ INL_JOIN(t1, t2) */  * FROM t1 INNER JOIN t2 ON t1.id = t2.t1_id WHERE t1.int_col = 1;
EXPLAIN ANALYZE SELECT /*+ HASH_JOIN(t1, t2) */  * FROM t1 INNER JOIN t2 ON t1.id = t2.t1_id WHERE t1.int_col = 1;
```

```sql
+---------------------------------+----------+---------+-----------+------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------+-----------------------+------+
| id                              | estRows  | actRows | task      | access object                | execution info                                                                                                                                                                                                                                                                               | operator info                                                                   | memory                | disk |
+---------------------------------+----------+---------+-----------+------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------+-----------------------+------+
| IndexJoin_11                    | 90000.00 | 0       | root      |                              | time:161.402922ms, loops:1, inner:{total:85.680156ms, concurrency:5, task:7, construct:3.42369ms, fetch:82.249596ms, build:1.32µs}, probe:953.935µs                                                                                                                                          | inner join, inner:IndexLookUp_10, outer key:test.t1.id, inner key:test.t2.t1_id | 29.730140686035156 MB | N/A  |
| ├─TableReader_32(Build)         | 71.01    | 10000   | root      |                              | time:143.807836ms, loops:13, cop_task: {num: 3, max: 92.101568ms, min: 48.32769ms, avg: 65.810308ms, p95: 92.101568ms, max_proc_keys: 31724, p95_proc_keys: 31724, tot_proc: 156ms, tot_wait: 4ms, rpc_num: 4, rpc_time: 197.761264ms, copr_cache_hit_ratio: 0.00}, backoff{regionMiss: 2ms} | data:Selection_31                                                               | 29.679648399353027 MB | N/A  |
| │ └─Selection_31                | 71.01    | 10000   | cop[tikv] |                              | proc max:56ms, min:36ms, p80:56ms, p95:56ms, iters:83, tasks:3                                                                                                                                                                                                                               | eq(test.t1.int_col, 1)                                                          | N/A                   | N/A  |
| │   └─TableFullScan_30          | 71010.00 | 71010   | cop[tikv] | table:t1                     | proc max:56ms, min:36ms, p80:56ms, p95:56ms, iters:83, tasks:3                                                                                                                                                                                                                               | keep order:false                                                                | N/A                   | N/A  |
| └─IndexLookUp_10(Probe)         | 1267.43  | 0       | root      |                              | time:78.36754ms, loops:7, cop_task: {num: 7, max: 14.541893ms, min: 2.914102ms, avg: 10.445675ms, p95: 14.541893ms, tot_proc: 56ms, tot_wait: 12ms, rpc_num: 8, rpc_time: 73.424356ms, copr_cache_hit_ratio: 0.00}                                                                           |                                                                                 | 458 Bytes             | N/A  |
|   ├─IndexRangeScan_8(Build)     | 1267.43  | 0       | cop[tikv] | table:t2, index:t1_id(t1_id) | proc max:12ms, min:0s, p80:12ms, p95:12ms, iters:7, tasks:7                                                                                                                                                                                                                                  | range: decided by [eq(test.t2.t1_id, test.t1.id)], keep order:false             | N/A                   | N/A  |
|   └─TableRowIDScan_9(Probe)     | 1267.43  | 0       | cop[tikv] | table:t2                     | time:0ns, loops:0                                                                                                                                                                                                                                                                            | keep order:false                                                                | N/A                   | N/A  |
+---------------------------------+----------+---------+-----------+------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------+-----------------------+------+
7 rows in set (0.12 sec)

+------------------------------+----------+---------+-----------+---------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+-----------------------+---------+
| id                           | estRows  | actRows | task      | access object | execution info                                                                                                                                                                                                                                                          | operator info                                     | memory                | disk    |
+------------------------------+----------+---------+-----------+---------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+-----------------------+---------+
| HashJoin_31                  | 90000.00 | 0       | root      |               | time:444.850751ms, loops:1, build_hash_table:{total:141.104584ms, fetch:138.713119ms, build:2.391465ms}, probe:{concurrency:5, total:2.2238735s, max:444.802992ms, probe:6.031399ms, fetch:2.217842101s}                                                                | inner join, equal:[eq(test.t1.id, test.t2.t1_id)] | 29.746952056884766 MB | 0 Bytes |
| ├─TableReader_34(Build)      | 71.01    | 10000   | root      |               | time:138.980527ms, loops:11, cop_task: {num: 3, max: 138.702269ms, min: 85.011941ms, avg: 106.410859ms, p95: 138.702269ms, max_proc_keys: 31724, p95_proc_keys: 31724, tot_proc: 256ms, rpc_num: 3, rpc_time: 319.170518ms, copr_cache_hit_ratio: 0.00}                 | data:Selection_33                                 | 18.458189964294434 MB | N/A     |
| │ └─Selection_33             | 71.01    | 10000   | cop[tikv] |               | proc max:96ms, min:40ms, p80:96ms, p95:96ms, iters:83, tasks:3                                                                                                                                                                                                          | eq(test.t1.int_col, 1)                            | N/A                   | N/A     |
| │   └─TableFullScan_32       | 71010.00 | 71010   | cop[tikv] | table:t1      | proc max:96ms, min:40ms, p80:96ms, p95:96ms, iters:83, tasks:3                                                                                                                                                                                                          | keep order:false                                  | N/A                   | N/A     |
| └─TableReader_36(Probe)      | 90000.00 | 90000   | root      |               | time:443.457881ms, loops:90, cop_task: {num: 3, max: 443.829268ms, min: 312.204258ms, avg: 372.765158ms, p95: 443.829268ms, max_proc_keys: 31712, p95_proc_keys: 31712, tot_proc: 580ms, tot_wait: 4ms, rpc_num: 3, rpc_time: 1.118223204s, copr_cache_hit_ratio: 0.00} | data:TableFullScan_35                             | 182.62188053131104 MB | N/A     |
|   └─TableFullScan_35         | 90000.00 | 90000   | cop[tikv] | table:t2      | proc max:112ms, min:92ms, p80:112ms, p95:112ms, iters:102, tasks:3                                                                                                                                                                                                      | keep order:false                                  | N/A                   | N/A     |
+------------------------------+----------+---------+-----------+---------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+-----------------------+---------+
6 rows in set (0.37 sec)
```

If the index on `t1.int_col` is not available, the hash join execution plan remains the same. However, the plan changes for the Index Join and performance is reduced:

{{< copyable "sql" >}}

```sql
ALTER TABLE t2 DROP INDEX t1_id; # drop the index
EXPLAIN ANALYZE SELECT /*+ INL_JOIN(t1, t2) */  * FROM t1 INNER JOIN t2 ON t1.id = t2.t1_id WHERE t1.int_col = 1;
EXPLAIN ANALYZE SELECT /*+ HASH_JOIN(t1, t2) */  * FROM t1 INNER JOIN t2 ON t1.id = t2.t1_id WHERE t1.int_col = 1;
ALTER TABLE t2 ADD INDEX (t1_id); # Re-add the index
```

```sql
Query OK, 0 rows affected (0.28 sec)

+-----------------------------+-----------+---------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------+-----------------------+------+
| id                          | estRows   | actRows | task      | access object | execution info                                                                                                                                                                                                                                           | operator info                                                                  | memory                | disk |
+-----------------------------+-----------+---------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------+-----------------------+------+
| IndexJoin_13                | 180000.00 | 0       | root      |               | time:306.660606ms, loops:1, inner:{total:94.469824ms, concurrency:5, task:12, construct:24.068036ms, fetch:70.386118ms, build:3.56µs}, probe:8.044327ms                                                                                                  | inner join, inner:TableReader_9, outer key:test.t2.t1_id, inner key:test.t1.id | 267.4683485031128 MB  | N/A  |
| ├─TableReader_19(Build)     | 180000.00 | 90000   | root      |               | time:265.456563ms, loops:95, cop_task: {num: 3, max: 289.969456ms, min: 263.177148ms, avg: 274.494282ms, p95: 289.969456ms, max_proc_keys: 31712, p95_proc_keys: 31712, tot_proc: 344ms, rpc_num: 3, rpc_time: 823.426838ms, copr_cache_hit_ratio: 0.00} | data:TableFullScan_18                                                          | 182.62185955047607 MB | N/A  |
| │ └─TableFullScan_18        | 180000.00 | 90000   | cop[tikv] | table:t2      | proc max:52ms, min:40ms, p80:52ms, p95:52ms, iters:102, tasks:3                                                                                                                                                                                          | keep order:false                                                               | N/A                   | N/A  |
| └─TableReader_9(Probe)      | 0.14      | 0       | root      |               | time:68.863176ms, loops:12, cop_task: {num: 15, max: 27.789032ms, min: 194.999µs, avg: 4.613536ms, p95: 27.789032ms, max_proc_keys: 3, p95_proc_keys: 3, rpc_num: 15, rpc_time: 68.906182ms, copr_cache_hit_ratio: 0.00}                                 | data:Selection_8                                                               | N/A                   | N/A  |
|   └─Selection_8             | 0.14      | 0       | cop[tikv] |               | proc max:0s, min:0s, p80:0s, p95:0s, iters:15, tasks:15                                                                                                                                                                                                  | eq(test.t1.int_col, 1)                                                         | N/A                   | N/A  |
|     └─TableRangeScan_7      | 1.00      | 24      | cop[tikv] | table:t1      | proc max:0s, min:0s, p80:0s, p95:0s, iters:15, tasks:15                                                                                                                                                                                                  | range: decided by [test.t2.t1_id], keep order:false                            | N/A                   | N/A  |
+-----------------------------+-----------+---------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------+-----------------------+------+
6 rows in set (0.31 sec)

+------------------------------+-----------+---------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+-----------------------+---------+
| id                           | estRows   | actRows | task      | access object | execution info                                                                                                                                                                                                                                           | operator info                                     | memory                | disk    |
+------------------------------+-----------+---------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+-----------------------+---------+
| HashJoin_19                  | 180000.00 | 0       | root      |               | time:358.337597ms, loops:1, build_hash_table:{total:147.96025ms, fetch:146.205311ms, build:1.754939ms}, probe:{concurrency:5, total:1.791287915s, max:358.288747ms, probe:13.101709ms, fetch:1.778186206s}                                               | inner join, equal:[eq(test.t1.id, test.t2.t1_id)] | 29.746952056884766 MB | 0 Bytes |
| ├─TableReader_22(Build)      | 20000.00  | 10000   | root      |               | time:146.262389ms, loops:11, cop_task: {num: 3, max: 145.767323ms, min: 73.050062ms, avg: 104.982029ms, p95: 145.767323ms, max_proc_keys: 31724, p95_proc_keys: 31724, tot_proc: 256ms, rpc_num: 3, rpc_time: 314.898089ms, copr_cache_hit_ratio: 0.00}  | data:Selection_21                                 | 18.457707405090332 MB | N/A     |
| │ └─Selection_21             | 20000.00  | 10000   | cop[tikv] |               | proc max:104ms, min:28ms, p80:104ms, p95:104ms, iters:83, tasks:3                                                                                                                                                                                        | eq(test.t1.int_col, 1)                            | N/A                   | N/A     |
| │   └─TableFullScan_20       | 142020.00 | 71010   | cop[tikv] | table:t1      | proc max:104ms, min:28ms, p80:104ms, p95:104ms, iters:83, tasks:3                                                                                                                                                                                        | keep order:false                                  | N/A                   | N/A     |
| └─TableReader_24(Probe)      | 180000.00 | 90000   | root      |               | time:356.586006ms, loops:90, cop_task: {num: 3, max: 357.264333ms, min: 301.721986ms, avg: 326.268422ms, p95: 357.264333ms, max_proc_keys: 31712, p95_proc_keys: 31712, tot_proc: 536ms, rpc_num: 3, rpc_time: 978.759747ms, copr_cache_hit_ratio: 0.00} | data:TableFullScan_23                             | 178.60922050476074 MB | N/A     |
|   └─TableFullScan_23         | 180000.00 | 90000   | cop[tikv] | table:t2      | proc max:100ms, min:88ms, p80:100ms, p95:100ms, iters:102, tasks:3                                                                                                                                                                                       | keep order:false                                  | N/A                   | N/A     |
+------------------------------+-----------+---------+-----------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+-----------------------+---------+
6 rows in set (0.36 sec)

Query OK, 0 rows affected (3.16 sec)
```

### Variations of Index Join

An index join using the hint [`INL_JOIN`](/optimizer-hints.md#inl_joint1_name--tl_name-) will create a hash table of the intermediate results before joining on the outer table. TiDB also supports creating a hash table on the outer table with the hint [`INL_HASH_JOIN`](/optimizer-hints.md#inl_hash_join). If the column sets on the inner table match the columns of the outer table, the [`INL_MERGE_JOIN`](/optimizer-hints.md#inl_merge_join) index join can apply. Each of these variations of Index Join will be automatically selected by the SQL Optimizer.

### Configuration

Index Join performance is influenced by the following system variables:

* [`tidb_index_join_batch_size`](/system-variables.md#tidb_index_join_batch_size) (default: 25000) - the batch size of index lookup operations.
* [`tidb_index_lookup_join_concurrency`](/system-variables.md#tidb_index_lookup_join_concurrency) (default: 4) - the number of concurrent index lookup tasks.

## Hash Join

A hash join reads and caches the data on the `Build` side of the join in a hash table, and then reads the data on the `Probe` side of the join, probing the hash table to access required rows. Hash joins require more memory to execute than Index Joins, but execute much faster when there are a lot of rows that need to be joined. The Hash Join operator is multi-threaded in TiDB, and executes in parallel.

An example Hash Join is as follows:

{{< copyable "sql" >}}

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

The execution process of `Hash Join` is as follows:

1. Cache the data of the `Build` side in memory.
2. Construct a Hash Table on the `Build` side based on the cached data.
3. Read the data at the `Probe` side.
4. Use the data of the `Probe` side to probe the Hash Table.
5. Return qualified data to the user.

The operator info column in the `explain` table also records other information about `Hash Join`, including whether the query is Inner Join or Outer Join, and what are the conditions of Join. In the above example, the query is an Inner Join, where the Join condition `equal:[eq(test.t1.id, test.t2.id)]` partly corresponds with the query statement `WHERE t1.id = t2.id`. The operator info of the other Join operators in the following examples is similar to this one.

### Runtime Statistics

If [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) (default: 1GB) is exceeded, TiDB will attempt to use temporary storage provided that `oom-use-tmp-storage=TRUE` (default). This means that the `Build` operator used as part of the hash join might be created on disk. Runtime statistics, such as memory usage are visible in the `execution info` of `EXPLAIN ANALYZE`. The following example shows the output of `EXPLAIN ANALYZE` with a 1GB (default) `tidb_mem_quota_query` quota, and a 500MB quota. At 500MB disk is used for temporary storage:

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

### Configuration

Hash Join performance is influenced by the following system variables:

* [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) (default: 1GB) - if the memory quota for a query is exceeded, TiDB will attempt to spill the `Build` operator of a hash join to disk to save memory.
* [`tidb_hash_join_concurrency`](/system-variables.md#tidb_hash_join_concurrency) (default: 5) - the number of concurrent hash join tasks.

## Merge Join

Merge join is a special sort of join that applies when both sides of the join are read in sorted order. It can be described as similar to an _efficient zipper merge_, in that as data is read on both the `Build` and the `Probe` side of the join it can be compared as a streaming operation. Merge joins require far less memory than hash join, but do not execute in parallel.

The following is an example:

{{< copyable "sql" >}}

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

The execution of the `Merge Join` operator is as follows:

1. Read all the data of a Join Group from the `Build` side into the memory
2. Read the data of the `Probe` side.
3. Compare whether each row of data on the `Probe` side matches a complete Join Group on the `Build` side. Apart from equivalent conditions, there are non-equivalent conditions. Here "match" mainly refers to checking whether non-equivalent conditions are met. Join Group refers to the data with the same value among all Join Keys.
