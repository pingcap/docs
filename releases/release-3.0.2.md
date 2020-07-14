---
title: TiDB 3.0.2 Release Notes
aliases: ['/docs/dev/releases/release-3.0.2/','/docs/dev/releases/3.0.2/']
---

# TiDB 3.0.2 Release Notes

Release date: August 7, 2019

TiDB version: 3.0.2

TiDB Ansible version: 3.0.2

## TiDB

+ SQL Optimizer
    - Fix the issue that the “Can’t find column in schema” message is reported when the same table occurs multiple times in a query and logically the query result is always empty [#11247](https://github.com/pingcap/tidb/pull/11247)
    - Fix the issue that the query plan does not meet the expectation caused by the `TIDB_INLJ` hint not working correctly in some cases (like `explain select /*+ TIDB_INLJ(t1) */ t1.b, t2.a from t t1, t t2 where t1.b = t2.a`) [#11362](https://github.com/pingcap/tidb/pull/11362)
    - Fix the issue that the column name in the query result is wrong in some cases (like `SELECT IF(1,c,c) FROM t`) [#11379](https://github.com/pingcap/tidb/pull/11379)
    - Fix the issue that some queries like `SELECT 0 LIKE 'a string'` return `TRUE` because the `LIKE` expression is implicitly converted to 0 in some cases [#11411](https://github.com/pingcap/tidb/pull/11411)
    - Support sub-queries in the `SHOW` statement, like `SHOW COLUMNS FROM tbl WHERE FIELDS IN (SELECT 'a')` [#11459](https://github.com/pingcap/tidb/pull/11459)
    - Fix the issue that the related column of the aggregate function cannot be found and an error is reported caused by the `outerJoinElimination` optimizing rule not correctly handling the column alias; improve alias parsing in the optimizing process to make optimization cover more query types [#11377](https://github.com/pingcap/tidb/pull/11377)
    - Fix the issue that no error is reported when the syntax restriction is violated in the Window function (for example, `UNBOUNDED PRECEDING` is not allowed to appear at the end of the Frame definition) [#11543](https://github.com/pingcap/tidb/pull/11543)
    - Fix the issue that `FUNCTION_NAME` is in uppercase in the `ERROR 3593 (HY000): You cannot use the window function FUNCTION_NAME in this context` error message, which causes incompatibility with MySQL [#11535](https://github.com/pingcap/tidb/pull/11535)
    - Fix the issue that the unimplemented `IGNORE NULLS` syntax in the Window function is used but no error is reported [#11593](https://github.com/pingcap/tidb/pull/11593)
    - Fix the issue that the Optimizer does not correctly estimate time equal conditions [#11512](https://github.com/pingcap/tidb/pull/11512)
    - Support updating the Top-N statistics based on the feedback information [#11507](https://github.com/pingcap/tidb/pull/11507)
+ SQL Execution Engine
    - Fix the issue that the returned value is not `NULL` when the `INSERT` function contains `NULL` in parameters [#11248](https://github.com/pingcap/tidb/pull/11248)
    - Fix the issue that the computing result might be wrong when the  partitioned table is checked by the `ADMIN CHECKSUM` operation [#11266](https://github.com/pingcap/tidb/pull/11266)
    - Fix the issue that the result might be wrong when INDEX JOIN uses the prefix index [#11246](https://github.com/pingcap/tidb/pull/11246)
    - Fix the issue that result might be wrong caused by incorrectly aligning fractions when the `DATE_ADD` function does subtraction on date numbers involving microseconds [#11288](https://github.com/pingcap/tidb/pull/11288)
    - Fix the wrong result caused by the `DATE_ADD` function incorrectly processing the negative numbers in `INTERVAL` [#11325](https://github.com/pingcap/tidb/pull/11325)
    - Fix the issue that the number of fractional digits returned by `Mod(%)`, `Multiple(*)` or `Minus(-)` is different from that in MySQL when `Mod(%)`, `Multiple(*)` or `Minus(-)` returns 0 and the number of fractional digits is large (like `select 0.000 % 0.11234500000000000000`) [#11251](https://github.com/pingcap/tidb/pull/11251)
    - Fix the issue that `NULL` with a warning is incorrectly returned when the length of the result returned by `CONCAT` and `CONCAT_WS` functions exceeds `max_allowed_packet` [#11275](https://github.com/pingcap/tidb/pull/11275)
    - Fix the issue that `NULL` with a warning is incorrectly returned when parameters in the `SUBTIME` and `ADDTIME` functions are invalid [#11337](https://github.com/pingcap/tidb/pull/11337)
    - Fix the issue that `NULL` is incorrectly returned when parameters in the `CONVERT_TZ` function are invalid [#11359](https://github.com/pingcap/tidb/pull/11359)
    - Add the `MEMORY` column to the result returned by `EXPLAIN ANALYZE` to show the memory usage of this query [#11418](https://github.com/pingcap/tidb/pull/11418)
    - Add `CARTESIAN` Join to the result of `EXPLAIN` [#11429](https://github.com/pingcap/tidb/pull/11429)
    - Fix the incorrect data of auto-increment columns of the float and double types [#11385](https://github.com/pingcap/tidb/pull/11385)
    - Fix the panic issue caused by some `nil` information when pseudo statistics are dumped [#11460](https://github.com/pingcap/tidb/pull/11460)
    - Fix the incorrect query result of `SELECT … CASE WHEN … ELSE NULL ...` caused by constant folding optimization [#11441](https://github.com/pingcap/tidb/pull/11441)
    - Fix the issue that `floatStrToIntStr` does not correctly parse the input such as `+999.9999e2` [#11473](https://github.com/pingcap/tidb/pull/11473)
    - Fix the issue that `NULL` is not returned in some cases when the result of the `DATE_ADD` and `DATE_SUB` function overflows [#11476](https://github.com/pingcap/tidb/pull/11476)
    - Fix the issue that the conversion result is different from that in MySQL if the string contains an invalid character when a long string is converted to an integer [#11469](https://github.com/pingcap/tidb/pull/11469)
    - Fix the issue that the result of the `REGEXP BINARY` function is incompatible with MySQL caused by case sensitiveness of this function [#11504](https://github.com/pingcap/tidb/pull/11504)
    - Fix the issue that an error is reported when the `GRANT ROLE` statement receives `CURRENT_ROLE`; fix the issue that the `REVOKE ROLE` statement does not correctly revoke the `mysql.default_role` privilege [#11356](https://github.com/pingcap/tidb/pull/11356)
    - Fix the display format issue of the `Incorrect datetime value` warning information when executing statements like `SELECT ADDDATE('2008-01-34', -1)` [#11447](https://github.com/pingcap/tidb/pull/11447)
    - Fix the issue that the error message reports `constant … overflows float` rather than `constant … overflows bigint` if the result overflows when a float field of the JSON data is converted to an integer [#11534](https://github.com/pingcap/tidb/pull/11534)
    - Fix the issue that the result might be wrong caused by incorrect type conversion when the `DATE_ADD` function receives `FLOAT`, `DOUBLE` and `DECIMAL` column parameters [#11527](https://github.com/pingcap/tidb/pull/11527)
    - Fix the wrong result caused by incorrectly processing the sign of the INTERVAL fraction in the `DATE_ADD` function [#11615](https://github.com/pingcap/tidb/pull/11615)
    - Fix the incorrect query result when Index Lookup Join contains the prefix index caused by `Ranger` not correctly handling the prefix index [#11565](https://github.com/pingcap/tidb/pull/11565)
    - Fix the issue that the “Incorrect arguments to NAME_CONST” message is reported if the `NAME_CONST` function is executed when the second parameter of `NAME_CONST` is a negative number [#11268](https://github.com/pingcap/tidb/pull/11268)
    - Fix the issue that the result is incompatible with MySQL when an SQL statement involves computing the current time and the value is fetched multiple times; use the same value when fetching the current time for the same SQL statement [#11394](https://github.com/pingcap/tidb/pull/11394)
    - Fix the issue that `Close` is not called for `ChildExecutor` when the `Close` of `baseExecutor` reports an error. This issue might lead to Goroutine leaks when the `KILL` statements do not take effect and `ChildExecutor` is not closed [#11576](https://github.com/pingcap/tidb/pull/11576)
+ Server
    - Fix the issue that the auto-added value is 0 instead of the current timestamp when `LOAD DATA` processes the missing `TIMESTAMP` field in the CSV file [#11250](https://github.com/pingcap/tidb/pull/11250)
    - Fix issues that the `SHOW CREATE USER` statement does not correctly check related privileges, and `USER` and `HOST` returned by `SHOW CREATE USER CURRENT_USER()` might be wrong [#11229](https://github.com/pingcap/tidb/pull/11229)
    - Fix the issue that the returned result might be wrong when `executeBatch` is used in JDBC [#11290](https://github.com/pingcap/tidb/pull/11290)
    - Reduce printing the log information of the streaming client when changing the TiKV server’s port [#11370](https://github.com/pingcap/tidb/pull/11370)
    - Optimize the logic of reconnecting the streaming client to the TiKV server so that the streaming client will not be blocked for a long time [#11372](https://github.com/pingcap/tidb/pull/11372)
    - Add `REGION_ID` in `INFORMATION_SCHEMA.TIDB_HOT_REGIONS` [#11350](https://github.com/pingcap/tidb/pull/11350)
    - Cancel the timeout duration of obtaining Region information from the PD API to ensure that obtaining Region information will not end in a failure when TiDB API `http://{TiDBIP}:10080/regions/hot` is called due to PD timeout when the number of Regions is large [#11383](https://github.com/pingcap/tidb/pull/11383)
    - Fix the issue that Region related requests do not return partitioned table-related Regions in the HTTP API [#11466](https://github.com/pingcap/tidb/pull/11466)
    - Make the following changes to reduce the probability of locking timeout caused by slow operations when the user manually validates pessimistic locking [#11521](https://github.com/pingcap/tidb/pull/11521):
        - Increase the default TTL of pessimistic locking from 30 seconds to 40 seconds
        - Increase the maximum TTL from 60 seconds to 120 seconds
        - Calculate the pessimistic locking duration from the first `LockKeys` request
    - Change the `SendRequest` function logic in the TiKV client: try to immediately connect to another peer instead of keeping waiting when the connect cannot be built [#11531](https://github.com/pingcap/tidb/pull/11531)
    - Optimize the Region cache: label the removed store as invalid when a store is moved while another store goes online with a same address, to update the store information in the cache as soon as possible [#11567](https://github.com/pingcap/tidb/pull/11567)
    - Add the Region ID to the result returned by the `http://{TiDB_ADDRESS:TIDB_IP}/mvcc/key/{db}/{table}/{handle}` API [#11557](https://github.com/pingcap/tidb/pull/11557)
    - Fix the issue that Scatter Table does not work caused by the Scatter Table API not escaping the Range key [#11298](https://github.com/pingcap/tidb/pull/11298)
    - Optimize the Region cache: label the store where the Region exists as invalid when the correspondent store is inaccessible, to avoid reduced query performance caused by accessing this store [#11498](https://github.com/pingcap/tidb/pull/11498)
    - Fix the error that the table schema can still be obtained through the HTTP API after dropping the database with the same name multiple times [#11585](https://github.com/pingcap/tidb/pull/11585)
+ DDL
    - Fix the issue that an error occurs when a non-string column with a zero length is being indexed [#11214](https://github.com/pingcap/tidb/pull/11214)
    - Disallow modifying the columns with foreign key constraints and full-text indexes (Note: TiDB still supports foreign key constraints and full-text indexes in syntax) [#11274](https://github.com/pingcap/tidb/pull/11274)
    - Fix the issue that the index offset of the column might be wrong because the position changed by the `ALTER TABLE` statement and the default value of the column are used concurrently [#11346](https://github.com/pingcap/tidb/pull/11346)
    - Fix two issues that occur when parsing JSON files:
        - `int64` is used as the intermediate parsing result of `uint64` in `ConvertJSONToFloat`, which leads to the precision overflow error [#11433](https://github.com/pingcap/tidb/pull/11433)
        - `int64` is used as the intermediate parsing result of `uint64` in `ConvertJSONToInt`, which leads to the precision overflow error [#11551](https://github.com/pingcap/tidb/pull/11551)
    - Disallow dropping indexes on the auto-increment column to avoid that the auto-increment column might get an incorrect result [#11399](https://github.com/pingcap/tidb/pull/11399)
    - Fix the following issues [#11492](https://github.com/pingcap/tidb/pull/11492):
        - The character set and the collation of the column are not consistent when explicitly specifying the collation but not the character set
        - The error is not correctly reported when there is a conflict between the character set and the collation that are specified by `ALTER TABLE … MODIFY COLUMN`
        - Incompatibility with MySQL when using `ALTER TABLE … MODIFY COLUMN` to specify character sets and collations multiple times
    - Add the trace details of the subquery to the result of the `TRACE` query [#11458](https://github.com/pingcap/tidb/pull/11458)
    - Optimize the performance of executing `ADMIN CHECK TABLE` and greatly reduce its execution time [#11547](https://github.com/pingcap/tidb/pull/11547)
    - Add the result returned by `SPLIT TABLE … REGIONS/INDEX` and make `TOTAL_SPLIT_REGION` and `SCATTER_FINISH_RATIO` display the number of Regions that have been split successfully before timeout in the result [#11484](https://github.com/pingcap/tidb/pull/11484)
    - Fix the issue that the precision displayed by statements like `SHOW CREATE TABLE` is incomplete when `ON UPDATE CURRENT_TIMESTAMP` is the column attribute and the float precision is specified [#11591](https://github.com/pingcap/tidb/pull/11591)
    - Fix the issue that the index result of the column cannot be correctly calculated when the expression of a virtual generated column contains another virtual generated column [#11475](https://github.com/pingcap/tidb/pull/11475)
    - Fix the issue that the minus sign cannot be added after `VALUE LESS THAN` in the `ALTER TABLE … ADD PARTITION …` statement [#11581](https://github.com/pingcap/tidb/pull/11581)
+ Monitor
    - Fix the issue that data is not collected and reported because the `TiKVTxnCmdCounter` monitoring metric is not registered [#11316](https://github.com/pingcap/tidb/pull/11316)
    - Add the `BindUsageCounter`, `BindTotalGauge` and `BindMemoryUsage` monitoring metrics for the Bind Info [#11467](https://github.com/pingcap/tidb/pull/11467)

## TiKV

- Fix the bug that TiKV panics if the Raft log is not written in time [#5160](https://github.com/tikv/tikv/pull/5160)
- Fix the bug that the panic information is not written into the log file after TiKV panics [#5198](https://github.com/tikv/tikv/pull/5198)
- Fix the bug that the Insert operation might be incorrectly performed in the pessimistic transaction [#5203](https://github.com/tikv/tikv/pull/5203)
- Lower the output level of some logs that require no manual intervention to INFO [#5193](https://github.com/tikv/tikv/pull/5193)
- Improve the accuracy of monitoring the storage engine size [#5200](https://github.com/tikv/tikv/pull/5200)
- Improve the accuracy of the Region size in tikv-ctl [#5195](https://github.com/tikv/tikv/pull/5195)
- Improve the performance of the deadlock detector for pessimistic locking [#5192](https://github.com/tikv/tikv/pull/5192)
- Improve the performance of GC in the Titan storage engine [#5197](https://github.com/tikv/tikv/pull/5197)

## PD

- Fix the bug that the Scatter Region scheduler cannot work [#1642](https://github.com/pingcap/pd/pull/1642)
- Fix the bug that the merge Region operation cannot be performed in pd-ctl [#1653](https://github.com/pingcap/pd/pull/1653)
- Fix the bug that the remove-tombstone operation cannot be performed in pd-ctl [#1651](https://github.com/pingcap/pd/pull/1651)
- Fix the issue that the Region overlapping with the key scope cannot be found when performing the scan Region operation [#1648](https://github.com/pingcap/pd/pull/1648)
- Add the retrying mechanism to make sure that the members are added successfully in PD [#1643](https://github.com/pingcap/pd/pull/1643)

## Tools

TiDB Binlog

- Add the configuration item check feature when starting, which will stop the Binlog service and report an error when an invalid item is found [#687](https://github.com/pingcap/tidb-binlog/pull/687)
- Add the `node-id` configuration in Drainer to specify a specific logic used by Drainer [#684](https://github.com/pingcap/tidb-binlog/pull/684)

TiDB Lightning

- Fix the issue that `tikv_gc_life_time` fails to be changed back to its original value when 2 checksums are running at the same time [#218](https://github.com/pingcap/tidb-lightning/pull/218)
- Add the configuration item check feature when starting, which will stop the Binlog service and report an error when an invalid item is found [#217](https://github.com/pingcap/tidb-lightning/pull/217)

## TiDB Ansible

- Fix the unit error that the Disk Performance monitor treats seconds as milliseconds [#840](https://github.com/pingcap/tidb-ansible/pull/840)
- Add the `log4j` configuration file in Spark [#841](https://github.com/pingcap/tidb-ansible/pull/841)
- Fix the issue that the Prometheus configuration file is generated in the wrong format when Binlog is enabled and Kafka or ZooKeeper is configured [#844](https://github.com/pingcap/tidb-ansible/pull/844)
- Fix the issue that the `pessimistic-txn` configuration parameter is left out in the generated TiDB configuration file [#850](https://github.com/pingcap/tidb-ansible/pull/850)
- Add and optimize metrics on the TiDB Dashboard [#853](https://github.com/pingcap/tidb-ansible/pull/853)
- Add descriptions for each monitoring item on the TiDB Dashboard [#854](https://github.com/pingcap/tidb-ansible/pull/854)
- Add the TiDB Summary Dashboard to better view the cluster status and troubleshoot issues [#855](https://github.com/pingcap/tidb-ansible/pull/855)
- Update the Allocator Stats monitoring item on the TiKV Dashboard [#857](https://github.com/pingcap/tidb-ansible/pull/857)
- Fix the unit error in the Node Exporter’s alerting expression [#860](https://github.com/pingcap/tidb-ansible/pull/860)
- Upgrade the TiSpark jar package to v2.1.2 [#862](https://github.com/pingcap/tidb-ansible/pull/862)
- Update the descriptions of the Ansible Task feature [#867](https://github.com/pingcap/tidb-ansible/pull/867)
- Update the expression of the local reader requests monitoring item on the TiDB Dashboard [#874](https://github.com/pingcap/tidb-ansible/pull/874)
- Update the expression of the TiKV Memory monitoring item on the Overview Dashboard, and fix the issue of wrongly displayed monitoring [#879](https://github.com/pingcap/tidb-ansible/pull/879)
- Remove the Binlog support in the Kafka mode [#878](https://github.com/pingcap/tidb-ansible/pull/878)
- Fix the issue that PD fails to transfer the Leader when executing the `rolling_update.yml` operation [#887](https://github.com/pingcap/tidb-ansible/pull/887)
