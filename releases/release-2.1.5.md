---
title: TiDB 2.1.5 Release Notes
aliases: ['/docs/dev/releases/release-2.1.5/','/docs/dev/releases/2.1.5/']
---

# TiDB 2.1.5 Release Notes

On February 28, 2019, TiDB 2.1.5 is released. The corresponding TiDB Ansible 2.1.5 is also released. Compared with TiDB 2.1.4, this release has greatly improved the stability, the SQL optimizer, statistics, and the execution engine.

## TiDB

+ SQL Optimizer/Executor
    - Make `SHOW CREATE TABLE` do not print the column charset information when the charset information of a column is the same with that of a table, to improve the compatibility of `SHOW CREATE TABLE` with MySQL [#9306](https://github.com/pingcap/tidb/pull/9306)
    - Fix the panic or the wrong result of the `Sort` operator in some cases by extracting `ScalarFunc` from `Sort` to a `Projection` operator for computing to simplify the computing logic of `Sort` [#9319](https://github.com/pingcap/tidb/pull/9319)
    - Remove the sorting field with constant values in the `Sort` operator [#9335](https://github.com/pingcap/tidb/pull/9335), [#9440](https://github.com/pingcap/tidb/pull/9440)
    - Fix the data overflow issue when inserting data into an unsigned integer column [#9339](https://github.com/pingcap/tidb/pull/9339)
    - Set `cast_as_binary` to `NULL` when the length of the target binary exceeds `max_allowed_packet` [#9349](https://github.com/pingcap/tidb/pull/9349)
    - Optimize the constant folding process of `IF` and `IFNULL` [#9351](https://github.com/pingcap/tidb/pull/9351)
    - Optimize the index selection of TiDB using skyline pruning to improve the stability of simple queries [#9356](https://github.com/pingcap/tidb/pull/9356)
    - Support computing the selectivity of the `DNF` expression [#9405](https://github.com/pingcap/tidb/pull/9405)
    - Fix the wrong SQL query result of `!=ANY()` and `=ALL()` in some cases [#9403](https://github.com/pingcap/tidb/pull/9403)
    - Fix the panic or the wrong result when the Join Key types of two tables on which  the `Merge Join` operation is performed are different [#9438](https://github.com/pingcap/tidb/pull/9438)
    - Fix the issue that the result of the `RAND()` function is not compatible with MySQL [#9446](https://github.com/pingcap/tidb/pull/9446)
    - Refactor the logic of `Semi Join` processing `NULL` and the empty result set to get the correct result and improve the compatibility with MySQL [#9449](https://github.com/pingcap/tidb/pull/9449)
+ Server
    - Add the `tidb_constraint_check_in_place` system variable to check the data uniqueness constraint when executing the `INSERT` statement [#9401](https://github.com/pingcap/tidb/pull/9401)
    - Fix the issue that the value of the `tidb_force_priority` system variable is different from that set in the configuration file [#9347](https://github.com/pingcap/tidb/pull/9347)
    - Add the `current_db` field in general logs to print the name of the currently used database [#9346](https://github.com/pingcap/tidb/pull/9346)
    - Add an HTTP API of obtaining the table information with the table ID [#9408](https://github.com/pingcap/tidb/pull/9408)
    - Fix the issue that `LOAD DATA` loads incorrect data in some cases [#9414](https://github.com/pingcap/tidb/pull/9414)
    - Fix the issue that it takes a long time to build a connection between the MySQL client and TiDB in some cases [#9451](https://github.com/pingcap/tidb/pull/9451)
+ DDL
    - Fix some issues when canceling the `DROP COLUMN` operation [#9352](https://github.com/pingcap/tidb/pull/9352)
    - Fix some issues when canceling the `DROP` or `ADD` partitioned table operation [#9376](https://github.com/pingcap/tidb/pull/9376)
    - Fix the issue that `ADMIN CHECK TABLE` mistakenly reports the data index inconsistency in some cases [#9399](https://github.com/pingcap/tidb/pull/9399)
    - Fix the time zone issue of the `TIMESTAMP` default value [#9108](https://github.com/pingcap/tidb/pull/9108)

## PD

- Provide the `exclude_tombstone_stores` option in the `GetAllStores` interface to remove the Tombstone store from the returned result [#1444](https://github.com/pingcap/pd/pull/1444)

## TiKV

- Fix the issue that Importer fails to import data in some cases [#4223](https://github.com/tikv/tikv/pull/4223)
- Fix the `KeyNotInRegion` error in some cases [#4125](https://github.com/tikv/tikv/pull/4125)
- Fix the panic issue caused by Region merge in some cases [#4235](https://github.com/tikv/tikv/pull/4235)
- Add the detailed `StoreNotMatch` error message [#3885](https://github.com/tikv/tikv/pull/3885)

## Tools

+ Lightning
    - Do not report an error or exit when a Tombstone store exists in the cluster [#4223](https://github.com/tikv/tikv/pull/4223)
+ TiDB Binlog
    - Update the DDL binlog replication plan to guarantee the correctness of DDL event replication [#9304](https://github.com/pingcap/tidb/issues/9304)