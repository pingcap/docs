---
title: TiDB 3.0 Beta Release Notes
aliases: ['/docs/dev/releases/release-3.0-beta/','/docs/dev/releases/3.0beta/']
---

# TiDB 3.0 Beta Release Notes

On January 19, 2019, TiDB 3.0 Beta is released. The corresponding TiDB Ansible 3.0 Beta is also released. TiDB 3.0 Beta builds on TiDB 2.1 with an added focus in stability, the SQL optimizer, statistics, and the execution engine.

## TiDB

+ New Features
    - Support Views
    - Support Window Functions
    - Support Range Partitioning
    - Support Hash Partitioning
+ SQL Optimizer
    - Re-support the optimization rule of `AggregationElimination` [#7676](https://github.com/pingcap/tidb/pull/7676)
    - Optimize the `NOT EXISTS` subquery and convert it to Anti Semi Join [#7842](https://github.com/pingcap/tidb/pull/7842)
    - Add the `tidb_enable_cascades_planner` variable to support the new Cascades optimizer. Currently, the Cascades optimizer is not yet fully implemented and is turned off by default [#7879](https://github.com/pingcap/tidb/pull/7879)
    - Support using Index Join in transactions [#7877](https://github.com/pingcap/tidb/pull/7877)
    - Optimize the constant propagation on the Outer Join, so that the filtering conditions related to the Outer table in the Join result can be pushed down through the Outer Join to the Outer table, reducing the useless calculation of the Outer Join and improving the execution performance [#7794](https://github.com/pingcap/tidb/pull/7794)
    - Adjust the optimization rule of Projection Elimination to the position after the Aggregation Elimination, to avoid redundant `Project` operators [#7909](https://github.com/pingcap/tidb/pull/7909)
    - Optimize the `IFNULL` function and eliminate this function when the input parameter has a non-NULL attribute [#7924](https://github.com/pingcap/tidb/pull/7924)
    - Support Range for `_tidb_rowid` construction queries, to avoid full table scan and reduce cluster stress [#8047](https://github.com/pingcap/tidb/pull/8047)
    - Optimize the `IN` subquery to do the Inner Join after the aggregation, and add the `tidb_opt_insubq_to_join_and_agg` variable to control whether to enable this optimization rule and open it by default [#7531](https://github.com/pingcap/tidb/pull/7531)
    - Support using subqueries in the `DO` statement [#8343](https://github.com/pingcap/tidb/pull/8343)
    - Add the optimization rule of Outer Join elimination to reduce unnecessary table scan and Join operations and improve execution performance [#8021](https://github.com/pingcap/tidb/pull/8021)
    - Modify the Hint behavior of the `TIDB_INLJ` optimizer, and the optimizer will use the table specified in Hint as the Inner table of Index Join [#8243](https://github.com/pingcap/tidb/pull/8243)
    - Use `PointGet` in a wide range so that it can be used when the execution plan cache of the `Prepare` statement takes effect [#8108](https://github.com/pingcap/tidb/pull/8108)
    - Introduce the greedy `Join Reorder` algorithm to optimize the join order selection when joining multiple tables [#8394](https://github.com/pingcap/tidb/pull/8394)
    - Support View [#8757](https://github.com/pingcap/tidb/pull/8757)
    - Support Window Function [#8630](https://github.com/pingcap/tidb/pull/8630)
    - Return warning to the client when `TIDB_INLJ` is not in effect, to enhance usability [#9037](https://github.com/pingcap/tidb/pull/9037)
    - Support deducing the statistics for filtered data based on filtering conditions and table statistics [#7921](https://github.com/pingcap/tidb/pull/7921)
    - Improve the Partition Pruning optimization rule of Range Partition [#8885](https://github.com/pingcap/tidb/pull/8885)
+ SQL Executor
    - Optimize the `Merge Join` operator to support the empty `ON` condition [#9037](https://github.com/pingcap/tidb/pull/9037)
    - Optimize the log and print the user variables used when executing the `EXECUTE` statement [#7684](https://github.com/pingcap/tidb/pull/7684)
    - Optimize the log to print slow query information for the `COMMIT` statement [#7951](https://github.com/pingcap/tidb/pull/7951)
    - Support the `EXPLAIN ANALYZE` feature to make the SQL tuning process easier [#7827](https://github.com/pingcap/tidb/pull/7827)
    - Optimize the write performance of wide tables with many columns [#7935](https://github.com/pingcap/tidb/pull/7935)
    - Support `admin show next_row_id` [#8242](https://github.com/pingcap/tidb/pull/8242)
    - Add the `tidb_init_chunk_size` variable to control the size of the initial Chunk used by the execution engine [#8480](https://github.com/pingcap/tidb/pull/8480)
    - Improve `shard_row_id_bits` and cross-check the auto-increment ID [#8936](https://github.com/pingcap/tidb/pull/8936)
+ `Prepare` Statement
    - Prohibit adding the `Prepare` statement containing subqueries to the query plan cache to guarantee the query plan is correct when different user variables are input [#8064](https://github.com/pingcap/tidb/pull/8064)
    - Optimize the query plan cache to guarantee the plan can be cached when the statement contains non-deterministic functions [#8105](https://github.com/pingcap/tidb/pull/8105)
    - Optimize the query plan cache to guarantee the query plan of `DELETE`/`UPDATE`/`INSERT` can be cached [#8107](https://github.com/pingcap/tidb/pull/8107)
    - Optimize the query plan cache to remove the corresponding plan when executing the `DEALLOCATE` statement [#8332](https://github.com/pingcap/tidb/pull/8332)
    - Optimize the query plan cache to avoid the TiDB OOM issue caused by caching too many plans by limiting the memory usage [#8339](https://github.com/pingcap/tidb/pull/8339)
    - Optimize the `Prepare` statement to support using the `?` placeholder in the `ORDER BY`/`GROUP BY`/`LIMIT` clause [#8206](https://github.com/pingcap/tidb/pull/8206)
+ Privilege Management
    - Add the privilege check for the `ANALYZE` statement [#8486](https://github.com/pingcap/tidb/pull/8486)
    - Add the privilege check for the `USE` statement [#8414](https://github.com/pingcap/tidb/pull/8418)
    - Add the privilege check for the `SET GLOBAL` statement [#8837](https://github.com/pingcap/tidb/pull/8837)
    - Add the privilege check for the `SHOW PROCESSLIST` statement [#7858](https://github.com/pingcap/tidb/pull/7858)
+ Server
    - Support the `Trace` feature [#9029](https://github.com/pingcap/tidb/pull/9029)
    - Support the plugin framework [#8788](https://github.com/pingcap/tidb/pull/8788)
    - Support using `unix_socket` and TCP simultaneously to connect to the database [#8836](https://github.com/pingcap/tidb/pull/8836)
    - Support the `interactive_timeout` system variable [#8573](https://github.com/pingcap/tidb/pull/8573)
    - Support the `wait_timeout` system variable [#8346](https://github.com/pingcap/tidb/pull/8346)
    - Support splitting a transaction into multiple transactions based on the number of statements using the `tidb_batch_commit` variable [#8293](https://github.com/pingcap/tidb/pull/8293)
    - Support using the `ADMIN SHOW SLOW` statement to check slow logs [#7785](https://github.com/pingcap/tidb/pull/7785)
+ Compatibility
    - Support the `ALLOW_INVALID_DATES` SQL mode [#9027](https://github.com/pingcap/tidb/pull/9027)
    - Improve `LoadData` fault-tolerance for the CSV file [#9005](https://github.com/pingcap/tidb/pull/9005)
    - Support the MySQL 320 handshake protocol [#8812](https://github.com/pingcap/tidb/pull/8812)
    - Support using the unsigned `bigint` column as the auto-increment column [#8181](https://github.com/pingcap/tidb/pull/8181)
    - Support the `SHOW CREATE DATABASE IF NOT EXISTS` syntax [#8926](https://github.com/pingcap/tidb/pull/8926)
    - Abandon the predicate pushdown operation when the filtering condition contains a user variable to improve the compatibility with MySQL’s behavior of using user variables to mock the Window Function behavior [#8412](https://github.com/pingcap/tidb/pull/8412)
+ DDL
    - Support fast recovery of mistakenly deleted tables [#7937](https://github.com/pingcap/tidb/pull/7937)
    - Support adjusting the number of concurrencies of `ADD INDEX` dynamically [#8295](https://github.com/pingcap/tidb/pull/8295)
    - Support changing the character set of tables or columns to `utf8`/`utf8mb4` [#8037](https://github.com/pingcap/tidb/pull/8037)
    - Change the default character set from `utf8` to `utf8mb4` [#7965](https://github.com/pingcap/tidb/pull/7965)
    - Support Range Partition [#8011](https://github.com/pingcap/tidb/pull/8011)

## Tools

+ TiDB Lightning
    - Speed up converting SQL statements to KV pairs remarkably [#110](https://github.com/pingcap/tidb-lightning/pull/110)
    - Support batch import for a single table to improve import performance and stability [#113](https://github.com/pingcap/tidb-lightning/pull/113)

## PD

- Add `RegionStorage` to store Region metadata separately [#1237](https://github.com/pingcap/pd/pull/1237)
- Add shuffle hot Region scheduler [#1361](https://github.com/pingcap/pd/pull/1361)
- Add scheduling parameter related metrics [#1406](https://github.com/pingcap/pd/pull/1406)
- Add cluster label related metrics [#1402](https://github.com/pingcap/pd/pull/1402)
- Add the importing data simulator [#1263](https://github.com/pingcap/pd/pull/1263)
- Fix the `Watch` issue about leader election [#1396](https://github.com/pingcap/pd/pull/1396)

## TiKV

- Support distributed GC [#3179](https://github.com/tikv/tikv/pull/3179)
- Check RocksDB Level 0 files before applying snapshots to avoid Write Stall [#3606](https://github.com/tikv/tikv/pull/3606)
- Support reverse `raw_scan` and `raw_batch_scan` [#3742](https://github.com/tikv/tikv/pull/3724)
- Support using HTTP to obtain monitoring information [#3855](https://github.com/tikv/tikv/pull/3855)
- Support DST better [#3786](https://github.com/tikv/tikv/pull/3786)
- Support receiving and sending Raft messages in batch [#3931](https://github.com/tikv/tikv/pull/3913)
- Introduce a new storage engine Titan [#3985](https://github.com/tikv/tikv/pull/3985)
- Upgrade gRPC to v1.17.2 [#4023](https://github.com/tikv/tikv/pull/4023)
- Support receiving the client requests and sending replies in batch [#4043](https://github.com/tikv/tikv/pull/4043)
- Support multi-thread Apply [#4044](https://github.com/tikv/tikv/pull/4044)
- Support multi-thread Raftstore [#4066](https://github.com/tikv/tikv/pull/4066)
