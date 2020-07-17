---
title: TiDB 3.0.4 Release Notes
aliases: ['/docs/dev/releases/release-3.0.4/','/docs/dev/releases/3.0.4/']
---

# TiDB 3.0.4 Release Notes

Release date: October 8, 2019

TiDB version: 3.0.4

TiDB Ansible version: 3.0.4

- New features
    - Add the `performance_schema.events_statements_summary_by_digest` system table to troubleshoot performance issues at the SQL level
    - Add the `WHERE` clause in TiDB’s `SHOW TABLE REGIONS` syntax
    - Add the `worker-count` and `txn-batch` configuration items in Reparo to control the recovery speed
- Improvements
    - Support batch Region split command and empty split command in TiKV to improve split performance
    - Support double linked list for RocksDB in TiKV to improve performance of reverse scan
    - Add two perf tools `iosnoop` and `funcslower` in TiDB Ansible to better diagnose the cluster state
    - Optimize the output of slow query logs in TiDB by deleting redundant fields
- Changed behaviors
    - Update the default value of `txn-local-latches.enable` to `false` to disable the default behavior of checking conflicts of local transactions in TiDB
    - Add the `tidb_txn_mode` system variable of global scope in TiDB and allow using the pessimistic lock; note that TiDB still adopts the optimistic lock by default
    - Replace the `Index_ids` field in TiDB slow query logs with `Index_names` to improve the usability of slow query logs
    - Add the `split-region-max-num` parameter in the TiDB configuration file to modify the maximum number of Regions allowed in the `SPLIT TABLE` syntax
    - Return the `Out Of Memory Quota` error instead of disconnecting the link when a SQL execution exceeds the memory limit
    - Disallow dropping the `AUTO_INCREMENT` attribute of columns in TiDB to avoid misoperations. To drop this attribute, change the `tidb_allow_remove_auto_inc` system variable
- Fixed issues
    - Fix the issue that the uncommented TiDB-specific syntax `PRE_SPLIT_REGIONS` might cause errors in the downstream database during data replication
    - Fix the issue in TiDB that the slow query logs are incorrect when getting the result of `PREPARE` + `EXECUTE` by using the cursor
    - Fix the issue in PD that adjacent small Regions cannot be merged
    - Fix the issue in TiKV that file descriptor leak in idle clusters might cause TiKV processes to exit abnormally when the processes run for a long time
- Contributors

    Our thanks go to the following contributors from the community for helping this release:
    - [sduzh](https://github.com/sduzh)
    - [lizhenda](https://github.com/lizhenda)

## TiDB

- SQL Optimizer
    - Fix the issue that invalid query ranges might be resulted when splitted by feedback [#12170](https://github.com/pingcap/tidb/pull/12170)
    - Display the returned error of the `SHOW STATS_BUCKETS` statement in hexadecimal rather than return errors when the result contains invalid Keys [#12094](https://github.com/pingcap/tidb/pull/12094)
    - Fix the issue that when a query contains the `SLEEP` function (for example, `select 1 from (select sleep(1)) t;)`), column pruning causes invalid `sleep(1)` during query [#11953](https://github.com/pingcap/tidb/pull/11953)
    - Use index scan to lower IO when a query only concerns the number of columns rather than the table data [#12112](https://github.com/pingcap/tidb/pull/12112)
    - Do not use any index when no index is specified in `use index()` to be compatible with MySQL [#12100](https://github.com/pingcap/tidb/pull/12100)
    - Strictly limit the number of `TopN` records in the `CMSketch` statistics to fix the issue that the `ANALYZE` statement fails because the statement count exceeds TiDB’s limit on the size of a transaction [#11914](https://github.com/pingcap/tidb/pull/11914)
    - Fix the error occurred when converting the subqueries contained in the `Update` statement [#12483](https://github.com/pingcap/tidb/pull/12483)
    - Optimize execution performance of the `select ... limit ... offset ...` statement by pushing the Limit operator down to the `IndexLookUpReader` execution logic [#12378](https://github.com/pingcap/tidb/pull/12378)
- SQL Execution Engine
    - Print the SQL statement in the log when the `PREPARED` statement is incorrectly executed [#12191](https://github.com/pingcap/tidb/pull/12191)
    - Support partition pruning when the `UNIX_TIMESTAMP` function is used to implement partitioning [#12169](https://github.com/pingcap/tidb/pull/12169)
    - Fix the issue that no error is reported when `AUTO_INCREMENT` incorrectly allocates `MAX int64` and `MAX uint64` [#12162](https://github.com/pingcap/tidb/pull/12162)
    - Add the `WHERE` clause in the `SHOW TABLE … REGIONS` and `SHOW TABLE .. INDEX … REGIONS` syntaxes [#12123](https://github.com/pingcap/tidb/pull/12123)
    - Return the `Out Of Memory Quota` error instead of disconnecting the link when a SQL execution exceeds the memory limit [#12127](https://github.com/pingcap/tidb/pull/12127)
    - Fix the issue that incorrect result is returned when `JSON_UNQUOTE` function handles JSON text [#11955](https://github.com/pingcap/tidb/pull/11955)
    - Fix the issue that `LAST INSERT ID` is incorrect when assigning values to the `AUTO_INCREMENT` column in the first row (for example, `insert into t (pk, c) values (1, 2), (NULL, 3)`) [#12002](https://github.com/pingcap/tidb/pull/12002)
    - Fix the issue that the `GROUPBY` parsing rule is incorrect in the `PREPARE` statement [#12351](https://github.com/pingcap/tidb/pull/12351)
    - Fix the issue that the privilege check is incorrect in the point queries [#12340](https://github.com/pingcap/tidb/pull/12340)
    - Fix the issue that the duration by `sql_type` for the `PREPARE` statement is not shown in the monitoring record [#12331](https://github.com/pingcap/tidb/pull/12331)
    - Support using aliases for tables in the point queries (for example, `select * from t tmp where a = "aa"`) [#12282](https://github.com/pingcap/tidb/pull/12282)
    - Fix the error occurred when not handling negative values as unsigned when inserting negative numbers into BIT type columns  [#12423](https://github.com/pingcap/tidb/pull/12423)
    - Fix the incorrectly rounding of time (for example, `2019-09-11 11:17:47.999999666` should be rounded to `2019-09-11 11:17:48`.) [#12258](https://github.com/pingcap/tidb/pull/12258)
    - Refine the usage of expression blacklist (for example, `<` is equivalent to `It`.) [#11975](https://github.com/pingcap/tidb/pull/11975)
    - Add the database prefix to the message of non-existing function error (for example, `[expression:1305]FUNCTION test.std_samp does not exist`) [#12111](https://github.com/pingcap/tidb/pull/12111)
- Server
    - Add the `Prev_stmt` field in slow query logs to output the previous statement when the last statement is `COMMIT` [#12180](https://github.com/pingcap/tidb/pull/12180)
    - Optimize the output of slow query logs by deleting redundant fields [#12144](https://github.com/pingcap/tidb/pull/12144)
    - Update the default value of `txn-local-latches.enable` to `false` to disable the default behavior of checking conflicts of local transactions in TiDB [#12095](https://github.com/pingcap/tidb/pull/12095)
    - Replace the `Index_ids` field in TiDB slow query logs with `Index_names` to improve the usability of slow query logs [#12061](https://github.com/pingcap/tidb/pull/12061)
    - Add the `tidb_txn_mode` system variable of global scope in TiDB and allow using pessimistic lock [#12049](https://github.com/pingcap/tidb/pull/12049)
    - Add the `Backoff` field in the slow query logs to record the Backoff information in the commit phase of 2PC [#12335](https://github.com/pingcap/tidb/pull/12335)
    - Fix the issue that the slow query logs are incorrect when getting the result of `PREPARE` + `EXECUTE` by using the cursor (for example, `PREPARE stmt1FROM SELECT * FROM t WHERE a > ?; EXECUTE stmt1 USING @variable`) [#12392](https://github.com/pingcap/tidb/pull/12392)
    - Support `tidb_enable_stmt_summary`. When this feature is enabled, TiDB counts the SQL statements and the result can be queried by using the system table `performance_schema.events_statements_summary_by_digest` [#12308](https://github.com/pingcap/tidb/pull/12308)
    - Adjust the level of some logs in tikv-client (for example, change the  log level of `batchRecvLoop fails` from `ERROR` to `INFO`) [#12383](https://github.com/pingcap/tidb/pull/12383)
- DDL
    - Add the `tidb_allow_remove_auto_inc` variable. Dropping the `AUTO INCREMENT` attribute of the column is disabled by default [#12145](https://github.com/pingcap/tidb/pull/12145)
    - Fix the issue that the uncommented TiDB-specific syntax `PRE_SPLIT_REGIONS` might cause errors in the downstream database during data replication [#12120](https://github.com/pingcap/tidb/pull/12120)
    - Add the `split-region-max-num` variable in the configuration file so that the maximum allowable number of Regions is adjustable [#12097](https://github.com/pingcap/tidb/pull/12079)
    - Support splitting a Region into multiple Regions and fix the timeout issue during Region scatterings [#12343](https://github.com/pingcap/tidb/pull/12343)
    - Fix the issue that the `drop index` statement fails when the index that contains an `AUTO_INCREMENT` column referenced by two indexes [#12344](https://github.com/pingcap/tidb/pull/12344)
- Monitor
    - Add the `connection_transient_failure_count` monitoring metrics to count the number of gRPC connection errors in `tikvclient` [#12093](https://github.com/pingcap/tidb/pull/12093)

## TiKV

- Raftstore
    - Fix the issue that Raftstore inaccurately counts the number of keys in empty Regions [#5414](https://github.com/tikv/tikv/pull/5414)
    - Support double linked list for RocksDB to improve the performance of reverse scan [#5368](https://github.com/tikv/tikv/pull/5368)
    - Support batch Region split command and empty split command to improve split performance [#5470](https://github.com/tikv/tikv/pull/5470)
- Server
    - Fix the issue that the output format of the `-V` command is not consistent with the format of 2.X [#5501](https://github.com/tikv/tikv/pull/5501)
    - Upgrade Titan to the latest version in the 3.0 branch [#5517](https://github.com/tikv/tikv/pull/5517)
    - Upgrade grpcio to v0.4.5 [#5523](https://github.com/tikv/tikv/pull/5523)
    - Fix the issue of gRPC coredump and support shared memory to avoid OOM [#5524](https://github.com/tikv/tikv/pull/5524)
    - Fix the issue in TiKV that file descriptor leak in idle clusters might cause TiKV processes to exit abnormally when the processes run for a long time [#5567](https://github.com/tikv/tikv/pull/5567)
- Storage
    - Support the `txn_heart_beat` API to make the pessimistic lock in TiDB consistent with that in MySQL as much as possible [#5507](https://github.com/tikv/tikv/pull/5507)
    - Fix the issue that the performance of point queries is low in some situations [#5495](https://github.com/tikv/tikv/pull/5495) [#5463](https://github.com/tikv/tikv/pull/5463)

## PD

- Fix the issue that adjacent small Regions cannot be merged [#1726](https://github.com/pingcap/pd/pull/1726)
- Fix the issue that the TLS enabling parameter in `pd-ctl` is invalid [#1738](https://github.com/pingcap/pd/pull/1738)
- Fix the thread-safety issue that the PD operator is accidentally removed [#1734](https://github.com/pingcap/pd/pull/1734)
- Support TLS for Region syncer [#1739](https://github.com/pingcap/pd/pull/1739)

## Tools

- TiDB Binlog
    - Add the `worker-count` and `txn-batch` configuration items in Reparo to control the recovery speed [#746](https://github.com/pingcap/tidb-binlog/pull/746)
    - Optimize the memory usage of Drainer to enhance the efficiency of simultaneous execution [#737](https://github.com/pingcap/tidb-binlog/pull/737)
- TiDB Lightning
    - Fix the issue that re-importing data from checkpoint might cause TiDB Lightning to panic [#237](https://github.com/pingcap/tidb-lightning/pull/237)
    - Optimize the algorithm of `AUTO_INCREMENT` to reduce the risk of overflowing `AUTO_INCREMENT` columns [#227](https://github.com/pingcap/tidb-lightning/pull/227)

## TiDB Ansible

- Upgrade TiSpark to v2.2.0 [#926](https://github.com/pingcap/tidb-ansible/pull/926)
- Update the default value of the TiDB configuration item `pessimistic_txn` to `true` [#933](https://github.com/pingcap/tidb-ansible/pull/933)
- Add more system-level monitoring metrics to `node_exporter` [#938](https://github.com/pingcap/tidb-ansible/pull/938)
- Add two perf tools `iosnoop` and `funcslower` in TiDB Ansible to better diagnose the cluster state [#946](https://github.com/pingcap/tidb-ansible/pull/946)
- Replace the raw module to shell module to address the long waiting time in such situations as the password expires [#949](https://github.com/pingcap/tidb-ansible/pull/949)
- Update the default value of the TiDB configuration item `txn_local_latches` to `false`
- Optimize the monitoring metrics and alert rules of Grafana dashboard [#962](https://github.com/pingcap/tidb-ansible/pull/962) [#963](https://github.com/pingcap/tidb-ansible/pull/963) [#969](https://github.com/pingcap/tidb-ansible/pull/963)
- Check the configuration file before the deployment and upgrade [#934](https://github.com/pingcap/tidb-ansible/pull/934) [#972](https://github.com/pingcap/tidb-ansible/pull/972)
