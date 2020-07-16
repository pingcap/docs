---
title: TiDB 3.0.1 Release Notes
aliases: ['/docs/dev/releases/release-3.0.1/','/docs/dev/releases/3.0.1/']
---

# TiDB 3.0.1 Release Notes

Release date: July 16, 2019

TiDB version: 3.0.1

TiDB Ansible version: 3.0.1

## TiDB

+ Add support for the `MAX_EXECUTION_TIME` feature [#11026](https://github.com/pingcap/tidb/pull/11026)
+ Add the `tidb_wait_split_region_finish_backoff` session variable to control the backoff time of splitting Regions [#11166](https://github.com/pingcap/tidb/pull/11166)
+ Support automatically adjusting the incremental gap allocated by auto-increment IDs based on the load, and the auto-adjustment scope of the incremental gap is 1000~2000000 [#11006](https://github.com/pingcap/tidb/pull/11006)
+ Add the `ADMIN PLUGINS ENABLE`/`ADMIN PLUGINS DISABLE` SQL statement to dynamically enable or disable plugins [#11157](https://github.com/pingcap/tidb/pull/11157)
+ Add the session connection information in the Audit plugin [#11013](https://github.com/pingcap/tidb/pull/11013)
+ Change the default behavior during the period of splitting Regions to wait for PD to finish scheduling [#11166](https://github.com/pingcap/tidb/pull/11166)
+ Prohibit Window Functions from being cached in Prepare Plan Cache to avoid incorrect results in some cases [#11048](https://github.com/pingcap/tidb/pull/11048)
+ Prohibit `ALTER` statements from modifying the definition of stored generated columns [#11068](https://github.com/pingcap/tidb/pull/11068)
+ Disallow changing virtual generated columns to stored generated columns [#11068](https://github.com/pingcap/tidb/pull/11068)
+ Disallow changing the generated column expression with indexes [#11068](https://github.com/pingcap/tidb/pull/11068)
+ Support compiling TiDB on the ARM64 architecture [#11150](https://github.com/pingcap/tidb/pull/11150)
+ Support modifying the collation of a database or a table, but the character set of the database/table has to be UTF-8 or utf8mb4 [#11086](https://github.com/pingcap/tidb/pull/11086)
+ Fix the issue that an error is reported when the `SELECT` subquery in the `UPDATE … SELECT` statement fails to parse the column in the `UPDATE` expression and the column is wrongly pruned [#11252](https://github.com/pingcap/tidb/pull/11252)
+ Fix the panic issue that happens when a column is queried on multiple times and the returned result is NULL during point queries [#11226](https://github.com/pingcap/tidb/pull/11226)
+ Fix the data race issue caused by non-thread safe `rand.Rand` when using the `RAND` function [#11169](https://github.com/pingcap/tidb/pull/11169)
+ Fix the bug that the memory usage of a SQL statement exceeds the threshold but the execution of this statement is not canceled in some cases when `oom-action="cancel"` is configured, and the returned result is incorrect [#11004](https://github.com/pingcap/tidb/pull/11004)
+ Fix the issue that `SHOW PROCESSLIST` shows that the memory usage is not `0` because the memory usage of MemTracker was not correctly cleaned [#10970](https://github.com/pingcap/tidb/pull/10970)
+ Fix the bug that the result of comparing integers and non-integers is not correct in some cases [#11194](https://github.com/pingcap/tidb/pull/11194)
+ Fix the bug that the query result is not correct when the query on table partitions contains a predicate in explicit transactions [#11196](https://github.com/pingcap/tidb/pull/11196)
+ Fix the DDL job panic issue because `infoHandle` might be `NULL` [#11022](https://github.com/pingcap/tidb/pull/11022)
+ Fix the issue that the query result is not correct because the queried column is not referenced in the subquery and is then wrongly pruned when running a nested aggregation query [#11020](https://github.com/pingcap/tidb/pull/11020)
+ Fix the issue that the `Sleep` function does not respond to the `KILL` statement in time [#11028](https://github.com/pingcap/tidb/pull/11028)
+ Fix the issue that the `DB` and `INFO` columns shown by the `SHOW PROCESSLIST` command are incompatible with MySQL [#11003](https://github.com/pingcap/tidb/pull/11003)
+ Fix the system panic issue caused by the `FLUSH PRIVILEGES` statement when `skip-grant-table=true` is configured [#11027](https://github.com/pingcap/tidb/pull/11027)
+ Fix the issue that the primary key statistics collected by `FAST ANALYZE` are not correct when the table primary key is an `UNSIGNED` integer [#11099](https://github.com/pingcap/tidb/pull/11099)
+ Fix the issue that the “invalid key” error is reported by the `FAST ANALYZE` statement in some cases [#11098](https://github.com/pingcap/tidb/pull/11098)
+ Fix the issue that the precision shown by the `SHOW CREATE TABLE` statement is incomplete when `CURRENT_TIMESTAMP` is used as the default value of the column and the float precision is specified [#11088](https://github.com/pingcap/tidb/pull/11088)
+ Fix the issue that the function name is not in lowercase when window functions report an error to make it compatible with MySQL [#11118](https://github.com/pingcap/tidb/pull/11118)
+ Fix the issue that TiDB fails to connect to TiKV and thus cannot provide service after the background thread of TiKV Client Batch gRPC panics [#11101](https://github.com/pingcap/tidb/pull/11101)
+ Fix the issue that the variable is set incorrectly by `SetVar` because of the shallow copy of the string [#11044](https://github.com/pingcap/tidb/pull/11044)
+ Fix the issue that the execution fails and an error is reported when the `INSERT … ON DUPLICATE` statement is applied on table partitions [#11231](https://github.com/pingcap/tidb/pull/11231)
+ Pessimistic locking (experimental feature)
    - Fix the issue that an incorrect result is returned because of the invalid lock on the row when point queries are run using the pessimistic locking and the returned data is empty [#10976](https://github.com/pingcap/tidb/pull/10976)
    - Fix the issue that the query result is not correct because `SELECT … FOR UPDATE` does not use the correct TSO when using the pessimistic locking in the query [#11015](https://github.com/pingcap/tidb/pull/11015)
    - Change the detection behavior from immediate conflict detection to waiting when an optimistic transaction meets a pessimistic lock to avoid worsening the lock conflict [#11051](https://github.com/pingcap/tidb/pull/11051)

## TiKV

- Add the statistics of the size of blob files in statistics information [#5060](https://github.com/tikv/tikv/pull/5060)
- Fix the core dump issue caused by the incorrectly cleaned memory resources when the process exits [#5053](https://github.com/tikv/tikv/pull/5053)
- Add all monitoring metrics related to the Titan engine [#4772](https://github.com/tikv/tikv/pull/4772), [#4836](https://github.com/tikv/tikv/pull/4836)
- Add the number of open file handles for Titan when counting the number of open file handles to avoid the issue that no file handle is available because of inaccurate statistics of file handles [#5026](https://github.com/tikv/tikv/pull/5026)
- Set `blob_run_mode` to decide whether to enable the Titan engine on a specific CF [#4991](https://github.com/tikv/tikv/pull/4991)
- Fix the issue that the read operations cannot get the commit information of pessimistic transactions [#5067](https://github.com/tikv/tikv/pull/5067)
- Add the `blob-run-mode` configuration parameter to control the running mode of the Titan engine, and its value can be `normal`, `read-only` or `fallback` [#4865](https://github.com/tikv/tikv/pull/4865)
- Improve the performance of detecting deadlocks [#5089](https://github.com/tikv/tikv/pull/5089)

## PD

- Fix the issue that the scheduling limit is automatically adjusted to 0 when PD schedules hot Regions [#1552](https://github.com/pingcap/pd/pull/1552)
- Add the `enable-grpc-gateway` configuration option to enable the gRPC gateway feature of etcd [#1596](https://github.com/pingcap/pd/pull/1596)
- Add `store-balance-rate`, `hot-region-schedule-limit` and other statistics related to scheduler configuration [#1601](https://github.com/pingcap/pd/pull/1601)
- Optimize the hot Region scheduling strategy and skip the Regions that lack replicas during scheduling to prevent multiple replicas from being scheduled to the same IDC [#1609](https://github.com/pingcap/pd/pull/1609)
- Optimize the Region merge processing logic and support giving priority to merging the Regions with smaller sizes to speed up Region merging [#1613](https://github.com/pingcap/pd/pull/1613)
- Adjust the default limit of hot Region scheduling in a single time to 64 to prevent too many scheduling tasks from occupying system resources and impacting performance [#1616](https://github.com/pingcap/pd/pull/1616)
- Optimize the Region scheduling strategy and support giving high priority to scheduling Regions in the `Pending` status [#1617](https://github.com/pingcap/pd/pull/1617)
- Fix the issue that `random-merge` and `admin-merge-region` operators cannot be added [#1634](https://github.com/pingcap/pd/pull/1634)
- Adjust the format of the Region key in the log to hexadecimal notation to make it easier to view [#1639](https://github.com/pingcap/pd/pull/1639)

## Tools

TiDB Binlog

- Optimize the Pump GC strategy and remove the restriction that the unconsumed binlog cannot be cleaned to make sure that the resources are not occupied for a  long time [#646](https://github.com/pingcap/tidb-binlog/pull/646)

TiDB Lightning

- Fix the import error that happens when the column names specified by the SQL dump are not in lowercase [#210](https://github.com/pingcap/tidb-lightning/pull/210)

## TiDB Ansible

- Add the precheck feature for the ansible command and its `jmespath` and `jinja2` dependency packages [#803](https://github.com/pingcap/tidb-ansible/pull/803), [#813](https://github.com/pingcap/tidb-ansible/pull/813)
- Add the `stop-write-at-available-space` parameter (10 GiB by default) in Pump to stop writing binlog files in Pump when the available disk space is less than the parameter value [#806](https://github.com/pingcap/tidb-ansible/pull/806)
- Update the I/O monitoring items in the TiKV monitoring information and make them compatible with the monitoring components of the new version [#820](https://github.com/pingcap/tidb-ansible/pull/820)
- Update the PD monitoring information, and fix the anomaly that Disk Latency is empty in the disk performance dashboard [#817](https://github.com/pingcap/tidb-ansible/pull/817)
- Add monitoring items for Titan in the TiKV details dashboard [#824](https://github.com/pingcap/tidb-ansible/pull/824)
