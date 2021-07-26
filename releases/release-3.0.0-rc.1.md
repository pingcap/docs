---
title: TiDB 3.0.0-rc.1 Release Notes
aliases: ['/docs/dev/releases/release-3.0.0-rc.1/','/docs/dev/releases/3.0.0-rc.1/']
---

# TiDB 3.0.0-rc.1 Release Notes

Release Date: May 10, 2019

TiDB version: 3.0.0-rc.1

TiDB Ansible version: 3.0.0-rc.1

## Overview

On May 10, 2019, TiDB 3.0.0-rc.1 is released. The corresponding TiDB Ansible version is 3.0.0-rc.1. Compared with TiDB 3.0.0-beta.1, this release has greatly improved the stability, usability, features, the SQL optimizer, statistics, and the execution engine.

## TiDB

+ SQL Optimizer
    - Improve the accuracy of cost estimates by using order correlation between columns; introduce a heuristic parameter `tidb_opt_correlation_exp_factor` to control the preference for index scans for scenarios when correlation cannot be directly used for estimation. [#9839](https://github.com/pingcap/tidb/pull/9839)
    - Match more prefix columns of the indexes when extracting access conditions of composite indexes if there are relevant columns in the filter [#10053](https://github.com/pingcap/tidb/pull/10053)
    - Use the dynamic programming algorithm to specify the execution order of join operations when the number of tables participating in the join is less than the value of `tidb_opt_join_reorder_threshold`. [#8816](https://github.com/pingcap/tidb/pull/8816)
    - Match more prefix columns of the indexes in the inner tables that build the index join when using composite indexes as the access conditions [#8471](https://github.com/pingcap/tidb/pull/8471)
    - Improve the accuracy of row count estimation for single-column indexes with NULL values [#9474](https://github.com/pingcap/tidb/pull/9474)
    - Specially handle `GROUP_CONCAT` when eliminating aggregate functions during the logical optimization phase to prevent incorrect executions [#9967](https://github.com/pingcap/tidb/pull/9967)
    - Properly push the filter down to child nodes of the join operator if the filter is a constant [#9848](https://github.com/pingcap/tidb/pull/9848)
    - Specially handle some functions such as `RAND()` when pruning columns during the logical optimization phase to prevent incompatibilities with MySQL [#10064](https://github.com/pingcap/tidb/pull/10064)
    - Support `FAST ANALYZE`, which speeds up statistics collection by sampling the region instead of scanning the entire region. This feature is controlled by the variable `tidb_enable_fast_analyze`. [#10258](https://github.com/pingcap/tidb/pull/10258)
    - Support SQL Plan Management, which ensures execution stability by performing execution plan binding for SQL statements. This feature is currently in beta and only supports bound execution plans for SELECT statements. It is not recommended to use it in the production environment. [#10284](https://github.com/pingcap/tidb/pull/10284)

+ Execution Engine
    - Support tracking and controlling memory usage in three operators - `TableReader`, `IndexReader` and `IndexLookupReader` [#10003](https://github.com/pingcap/tidb/pull/10003)
    - Support showing more information about coprocessor tasks in the slow log such as the number of tasks in coprocessor, the average/longest/90% of execution/waiting time and the addresses of the TiKVs which take the longest execution time or waiting time [#10165](https://github.com/pingcap/tidb/pull/10165)
    - Support the prepared DDL statements with no placeholders [#10144](https://github.com/pingcap/tidb/pull/10144)

+ Server
    - Only allow the DDL owner to execute bootstrap when TiDB is started [#10029](https://github.com/pingcap/tidb/pull/10029)
    - Add the variable `tidb_skip_isolation_level_check` to prevent TiDB from reporting errors when setting the transaction isolation level to SERIALIZABLE [#10065](https://github.com/pingcap/tidb/pull/10065)
    - Merge the implicit commit time and the SQL execution time in the slow log [#10294](https://github.com/pingcap/tidb/pull/10294)
        - Support for SQL Roles (RBAC Privilege Management)
        - Support `SHOW GRANT` [#10016](https://github.com/pingcap/tidb/pull/10016)
        - Support `SET DEFAULT ROLE` [#9949](https://github.com/pingcap/tidb/pull/9949)
    - Support `GRANT ROLE` [#9721](https://github.com/pingcap/tidb/pull/9721)
    - Fix the `ConnectionEvent` error from the `whitelist` plugin that makes TiDB exit [#9889](https://github.com/pingcap/tidb/pull/9889)
    - Fix the issue of mistakenly adding read-only statements to the transaction history [#9723](https://github.com/pingcap/tidb/pull/9723)
    - Improve `kill` statements to stop SQL execution  and release resources more quickly [#9844](https://github.com/pingcap/tidb/pull/9844)
    - Add a startup option `config-check` to check the validity of the configuration file [#9855](https://github.com/pingcap/tidb/pull/9855)
    - Fix the validity check of inserting NULL fields when the strict SQL mode is disabled [#10161](https://github.com/pingcap/tidb/pull/10161)

+ DDL
    - Add the `pre_split_regions` option for `CREATE TABLE` statements; this option supports pre-splitting the Table Region when creating a table to avoid write hot spots caused by lots of writes after the table creation [#10138](https://github.com/pingcap/tidb/pull/10138)
    - Optimize the execution performance of some DDL statements [#10170](https://github.com/pingcap/tidb/pull/10170)
    - Add the warning that full-text indexes are not supported for `FULLTEXT KEY` [#9821](https://github.com/pingcap/tidb/pull/9821)
    - Fix the compatibility issue for the UTF8 and UTF8MB4 charsets in the old versions of TiDB [#9820](https://github.com/pingcap/tidb/pull/9820)
    - Fix the potential bug in `shard_row_id_bits` of a table [#9868](https://github.com/pingcap/tidb/pull/9868)
    - Fix the bug that the column charset is not changed after the table charset is changed [#9790](https://github.com/pingcap/tidb/pull/9790)
    - Fix a potential bug in `SHOW COLUMN` when using `BINARY`/`BIT` as the column default value [#9897](https://github.com/pingcap/tidb/pull/9897)
    - Fix the compatibility issue in displaying `CHARSET`/`COLLATION` descriptions in the `SHOW FULL COLUMNS` statement [#10007](https://github.com/pingcap/tidb/pull/10007)
    - Fix the issue that the `SHOW COLLATIONS` statement only lists collations supported by TiDB [#10186](https://github.com/pingcap/tidb/pull/10186)

## PD

+ Upgrade ETCD [#1452](https://github.com/pingcap/pd/pull/1452)
    - Unify the log format of etcd and PD server
    - Fix the issue of failing to elect Leader by PreVote
    - Support fast dropping the “propose” and “read” requests that are to fail to avoid blocking the subsequent requests
    - Fix the deadlock issue of Lease
+ Fix the issue that a hot store makes incorrect statistics of keys [#1487](https://github.com/pingcap/pd/pull/1487)
+ Support forcibly rebuilding a PD cluster from a single PD node [#1485](https://github.com/pingcap/pd/pull/1485)
+ Fix the issue that `regionScatterer` might generate an invalid `OperatorStep` [#1482](https://github.com/pingcap/pd/pull/1482)
+ Fix the too short timeout issue of the `MergeRegion` operator [#1495](https://github.com/pingcap/pd/pull/1495)
+ Support giving high priority to hot region scheduling [#1492](https://github.com/pingcap/pd/pull/1492)
+ Add the metrics for recording the time of handling TSO requests on the PD server side [#1502](https://github.com/pingcap/pd/pull/1502)
+ Add the corresponding Store ID and Address to the metrics related to the store [#1506](https://github.com/pingcap/pd/pull/1506)
+ Support the `GetOperator` service [#1477](https://github.com/pingcap/pd/pull/1477)
+ Fix the issue that the error cannot be sent in the Heartbeat stream because the store cannot be found [#1521](https://github.com/pingcap/pd/pull/1521)

## TiKV

+ Engine
    - FIx the issue that may cause incorrect statistics on read traffic [#4436](https://github.com/tikv/tikv/pull/4436)
    - Fix the issue that may cause prefix extractor panic when deleting a range [#4503](https://github.com/tikv/tikv/pull/4503)
    - Optimize memory management to reduce memory allocation and copying for `Iterator Key Bound Option` [#4537](https://github.com/tikv/tikv/pull/4537)
    - Fix the issue that failing to consider learner log gap may in some cases cause panic [#4559](https://github.com/tikv/tikv/pull/4559)
    - Support `block cache` sharing among different `column families` [#4612](https://github.com/tikv/tikv/pull/4612)

+ Server
    - Reduce context switch overhead of  `batch commands` [#4473](https://github.com/tikv/tikv/pull/4473)
    - Check the validity of seek iterator status [#4470](https://github.com/tikv/tikv/pull/4470)

+ RaftStore
    - Support configurable `properties index distance` [#4517](https://github.com/tikv/tikv/pull/4517)

+ Coprocessor
    - Add batch index scan executor [#4419](https://github.com/tikv/tikv/pull/4419)
    - Add vectorized evaluation framework [#4322](https://github.com/tikv/tikv/pull/4322)
    - Add execution summary framework for batch executors [#4433](https://github.com/tikv/tikv/pull/4433)
    - Check the maximum column when constructing the RPN expression to avoid invalid column offset that may cause evaluation panic [#4481](https://github.com/tikv/tikv/pull/4481)
    - Add `BatchLimitExecutor` [#4469](https://github.com/tikv/tikv/pull/4469)
    - Replace the original `futures-cpupool` with `tokio-threadpool` in ReadPool to reduce context switch [#4486](https://github.com/tikv/tikv/pull/4486)
    - Add batch aggregation framework [#4533](https://github.com/tikv/tikv/pull/4533)
    - Add `BatchSelectionExecutor` [#4562](https://github.com/tikv/tikv/pull/4562)
    - Add batch aggression function `AVG` [#4570](https://github.com/tikv/tikv/pull/4570)
    - Add RPN function `LogicalAnd`[#4575](https://github.com/tikv/tikv/pull/4575)

+ Misc
    - Support `tcmalloc` as a memory allocator [#4370](https://github.com/tikv/tikv/pull/4370)

## Tools

+ TiDB Binlog
    - Fix the replication abortion issue when binlog data for the primary key column of unsigned int type is negative [#573](https://github.com/pingcap/tidb-binlog/pull/573)
    - Provide no compression option when downstream is `pb`; modify the downstream name from `pb` to `file` [#559](https://github.com/pingcap/tidb-binlog/pull/559)
    - Add the `storage.sync-log` configuration item in Pump that allows asynchronous flush on local storage [#509](https://github.com/pingcap/tidb-binlog/pull/509)
    - Support traffic compression for communications between Pump and Drainer [#495](https://github.com/pingcap/tidb-binlog/pull/495)
    - Add the `syncer.sql-mode` configuration item in Drainer to support parsing DDL queries in different sql-mode [#511](https://github.com/pingcap/tidb-binlog/pull/511)
    - Add the `syncer.ignore-table` configuration item to support filtering out tables that do not require replication [#520](https://github.com/pingcap/tidb-binlog/pull/520)

+ Lightning
    - Use row IDs or default column values to populate the column data missed in the dump file [#170](https://github.com/pingcap/tidb-lightning/pull/170)
    - Fix the bug in Importer that import success may still be returned even if part of the SST failed to be imported [#4566](https://github.com/tikv/tikv/pull/4566)
    - Support speed limit in Importer when uploading SST to TiKV [#4412](https://github.com/tikv/tikv/pull/4412)
    - Support importing tables by size to reduce impacts on the cluster brought by Checksum and Analyze for big tables, and improve the success rate for Checksum and Analyze [#156](https://github.com/pingcap/tidb-lightning/pull/156)
    - Improve Lightning’s SQL encoding performance by 50% by directly parsing data source file as types.Datum of TiDB and saving extra parsing overhead from the KV encoder [#145](https://github.com/pingcap/tidb-lightning/pull/145)
    - Change log format to [Unified Log Format](https://github.com/tikv/rfcs/blob/master/text/2018-12-19-unified-log-format.md) [#162](https://github.com/pingcap/tidb-lightning/pull/162)
    - Add some command line options for use when the configuration file is missing [#157](https://github.com/pingcap/tidb-lightning/pull/157)

+ sync-diff-inspector
    - Support checkpoint to record verification status and continue the verification from last saved point after restarting [#224](https://github.com/pingcap/tidb-tools/pull/224)
    - Add the `only-use-checksum` configuration item to check data consistency by calculating checksum [#215](https://github.com/pingcap/tidb-tools/pull/215)

## TiDB Ansible

+ Support more TiKV monitoring panels and update versions for Ansible, Grafana, and Prometheus [#727](https://github.com/pingcap/tidb-ansible/pull/727)
    - Summary dashboard for viewing cluster status
    - trouble_shooting dashboard for troubleshooting issues
    - Details dashboard for developers to analyze issues
+ Fix the bug that causes the downloading failure of TiDB Binlog of Kafka version [#730](https://github.com/pingcap/tidb-ansible/pull/730)
+ Modify version limits on supported operating systems as CentOS 7.0+ and later, and Red Hat 7.0 and later [#733](https://github.com/pingcap/tidb-ansible/pull/733)
+ Change version detection mode during the rolling update to multi-concurrent [#736](https://github.com/pingcap/tidb-ansible/pull/736)
+ Update documentation links in README [#740](https://github.com/pingcap/tidb-ansible/pull/740)
+ Remove redundant TiKV monitoring metrics; add new metrics for troubleshooting [#735](https://github.com/pingcap/tidb-ansible/pull/735)
+ Optimize `table-regions.py` script to display leader distribution by table [#739](https://github.com/pingcap/tidb-ansible/pull/739)
+ Update configuration file for Drainer [#745](https://github.com/pingcap/tidb-ansible/pull/745)
+ Optimize TiDB monitoring with new panels that display latencies by SQL categories [#747](https://github.com/pingcap/tidb-ansible/pull/747)
+ Update the Lightning configuration file and add the `tidb_lightning_ctl` script [#1e946f8](https://github.com/pingcap/tidb-ansible/commit/1e946f89908e8fd6ef84128c6da3064ddfccf6a8)
