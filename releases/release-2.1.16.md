---
title: TiDB 2.1.16 Release Notes
aliases: ['/docs/dev/releases/release-2.1.16/','/docs/dev/releases/2.1.16/']
---

# TiDB 2.1.16 Release Notes

Release date: August 15, 2019

TiDB version: 2.1.16

TiDB Ansible version: 2.1.16

## TiDB

+ SQL Optimizer
    - Fix the issue that row count is estimated inaccurately for the equal condition on the time column [#11526](https://github.com/pingcap/tidb/pull/11526)
    - Fix the issue that `TIDB_INLJ` Hint does not take effect or take effect on the specified table [#11361](https://github.com/pingcap/tidb/pull/11361)
    - Change the implementation of `NOT EXISTS` in a query from OUTER JOIN to ANTI JOIN to find a more optimized execution plan [#11291](https://github.com/pingcap/tidb/pull/11291)
    - Support subqueries within `SHOW` statements, allowing syntaxes such as `SHOW COLUMNS FROM tbl WHERE FIELDS IN (SELECT 'a')` [#11461](https://github.com/pingcap/tidb/pull/11461)
    - Fix the issue that the `SELECT … CASE WHEN … ELSE NULL ...` query gets an incorrect result caused by the constant folding optimization [#11441](https://github.com/pingcap/tidb/pull/11441)
+ SQL Execution Engine
    - Fix the issue that the `DATE_ADD` function gets a wrong result when `INTERVAL` is negative [#11616](https://github.com/pingcap/tidb/pull/11616)
    - Fix the issue that the `DATE_ADD` function might get an incorrect result because it performs type conversion wrongly when it accepts an argument of the `FLOAT`, `DOUBLE`, or `DECIMAL` type [#11628](https://github.com/pingcap/tidb/pull/11628)
    - Fix the issue that the error message is inaccurate when CAST(JSON AS SIGNED) overflows [#11562](https://github.com/pingcap/tidb/pull/11562)
    - Fix the issue that other child nodes are not closed when one child node fails to be closed and returns an error during the process of closing Executor [#11598](https://github.com/pingcap/tidb/pull/11598)
    - Support `SPLIT TABLE` statements that return the number of Regions that are successfully split and a finished percentage rather than an error when the scheduling is not finished for Region scatter before the timeout [#11487](https://github.com/pingcap/tidb/pull/11487)
    - Make `REGEXP BINARY` function case sensitive to be compatible with MySQL [#11505](https://github.com/pingcap/tidb/pull/11505)
    - Fix the issue that `NULL` is not returned correctly because the value of `YEAR` in the `DATE_ADD`/`DATE_SUB` result overflows when it is smaller than 0 or larger than 65535 [#11477](https://github.com/pingcap/tidb/pull/11477)
    - Add in the slow query table a `Succ` field that indicates whether the execution succeeds [#11412](https://github.com/pingcap/tidb/pull/11421)
    - Fix the MySQL incompatibility issue caused by fetching the current timestamp multiple times when a SQL statement involves calculations of the current time (such as `CURRENT_TIMESTAMP` or `NOW`) [#11392](https://github.com/pingcap/tidb/pull/11392)
    - Fix the issue that the AUTO_INCREMENT columns do not handle the FLOAT or DOUBLE type [#11389](https://github.com/pingcap/tidb/pull/11389)
    - Fix the issue that `NULL` is not returned correctly when the `CONVERT_TZ` function accepts an invalid argument [#11357](https://github.com/pingcap/tidb/pull/11357)
    - Fix the issue that an error is reported by the `PARTITION BY LIST` statement. (Currently only the syntax is supported; when TiDB executes the statement, a regular table is created and a prompting message is provided) [#11236](https://github.com/pingcap/tidb/pull/11236)
    - Fix the issue that `Mod(%)`, `Multiple(*)`, and `Minus(-)` operations return an inconsistent `0` result with that in MySQL when there are many decimal digits (such as `select 0.000 % 0.11234500000000000000`) [#11353](https://github.com/pingcap/tidb/pull/11353)
+ Server
    - Fix the issue that the plugin gets a `NULL` domain when `OnInit` is called back [#11426](https://github.com/pingcap/tidb/pull/11426)
    - Fix the issue that the table information in a schema can still be obtained through the HTTP interface after the schema has been deleted [#11586](https://github.com/pingcap/tidb/pull/11586)
+ DDL
    - Disallow dropping indexes on auto-increment columns to avoid incorrect results of the auto-increment columns caused by this operation [#11402](https://github.com/pingcap/tidb/pull/11402)
    - Fix the issue that the character set of the column is not correct when creating and modifying the table with different character sets and collations [#11423](https://github.com/pingcap/tidb/pull/11423)
    - Fix the issue that the column schema might get wrong when `alter table ... set default...` and another DDL statement that modifies this column are executed in parallel [#11374](https://github.com/pingcap/tidb/pull/11374)
    - Fix the issue that data fails to be backfilled when Generated Column A depends on Generated Column B and A is used to create an index [#11538](https://github.com/pingcap/tidb/pull/11538)
    - Speed up `ADMIN CHECK TABLE` operations [#11538](https://github.com/pingcap/tidb/pull/11676)

## TiKV

+ Support returning an error message when the client accesses a TiKV Region that is being closed [#4820](https://github.com/tikv/tikv/pull/4820)
+ Support reverse `raw_scan` and `raw_batch_scan` interfaces [#5148](https://github.com/tikv/tikv/pull/5148)

## Tools

+ TiDB Binlog
    - Add the `ignore-txn-commit-ts` configuration item in Drainer to skip executing some statements in a transaction [#697](https://github.com/pingcap/tidb-binlog/pull/697)
    - Add the configuration item check on startup, which stops Pump and Drainer from running and returns an error message when meeting invalid configuration items [#708](https://github.com/pingcap/tidb-binlog/pull/708)
    - Add the `node-id` configuration in Drainer to specify Drainer’s node ID [#706](https://github.com/pingcap/tidb-binlog/pull/706)
+ TiDB Lightning
    - Fix the issue that `tikv_gc_life_time` fails to be changed back to its original value when 2 checksums are running at the same time [#224](https://github.com/pingcap/tidb-lightning/pull/224)

## TiDB Ansible

+ Add the `log4j` configuration file in Spark [#842](https://github.com/pingcap/tidb-ansible/pull/842)
+ Update the tispark jar package to v2.1.2 [#863](https://github.com/pingcap/tidb-ansible/pull/863)
+ Fix the issue that the Prometheus configuration file is generated in the wrong format when TiDB Binlog uses Kafka or ZooKeeper [#845](https://github.com/pingcap/tidb-ansible/pull/845)
+ Fix the bug that PD fails to switch the Leader when executing the `rolling_update.yml` operation [#888](https://github.com/pingcap/tidb-ansible/pull/888)
+ Optimize the logic of rolling updating PD nodes - upgrade Followers first and then the Leader - to improve stability [#895](https://github.com/pingcap/tidb-ansible/pull/895)
