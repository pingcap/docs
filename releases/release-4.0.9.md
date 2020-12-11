---
title: TiDB 4.0.9 Release Notes
---

# TiDB 4.0.9 Release Notes

Release date: December 10, 2020

TiDB version: 4.0.9

## Compatibility changes

+ TiDB

    - Deprecate the `enable-streaming` configuration [#21055](https://github.com/pingcap/tidb/pull/21055)

## New Features

+ TiFlash

    - Support storing the latest data of the storage engine on multiple disks (experimental)

## Improvements

+ TiDB

    - Avoid the (index) merge join heuristically when converting equal conditions to other conditions [#21146](https://github.com/pingcap/tidb/pull/21146)
    - Differentiate the types of user variables [#21107](https://github.com/pingcap/tidb/pull/21107)
    - Support setting the `GOGC` variable in the configuration file [#20922](https://github.com/pingcap/tidb/pull/20922)
    - Make the dumped binary time (`Timestamp` and `Datetime`) more compatible with MySQL [#21135](https://github.com/pingcap/tidb/pull/21135)
    - Provide an error message for statements that use the `LOCK IN SHARE MODE` syntax [#21005](https://github.com/pingcap/tidb/pull/21005)
    - Avoid outputting unnecessary warnings or errors when folding constants in shortcut-able expressions [#21040](https://github.com/pingcap/tidb/pull/21040)
    - Raise an error when preparing the `LOAD DATA` statement [#21199](https://github.com/pingcap/tidb/pull/21199)
    - Ignore the size attribute of the integer zero-fill when changing the column types [#20986](https://github.com/pingcap/tidb/pull/20986)
    - Add the executor-related runtime information of DML statements in the result of `EXPLAIN ANALYZE` [#21066](https://github.com/pingcap/tidb/pull/21066)
    - Disallow multiple updates on the primary key in a singe SQL statements [#21113](https://github.com/pingcap/tidb/pull/21113)
    - Add a monitoring metric for the connection idle time [#21301](https://github.com/pingcap/tidb/pull/21301)

+ TiKV

    - Add the tag to trace the source of the `split` command [#8936](https://github.com/tikv/tikv/pull/8936)
    - Support dynamically changing the `pessimistic-txn.pipelined` configuration [#9100](https://github.com/tikv/tikv/pull/9100)
    - Reduce the impact on performance when running Backup & Restore and TiDB Lightning [#9098](https://github.com/tikv/tikv/pull/9098)
    - Add monitoring metrics for the ingesting SST errors [#9096](https://github.com/tikv/tikv/pull/9096)
    - Prevent hibernation when there are still peers catching up with logs [#9093](https://github.com/tikv/tikv/pull/9093)
    - Increase the success rate of the pipelined pessimistic locking [#9086](https://github.com/tikv/tikv/pull/9086)
    - Change the default value of `apply-max-batch-size` and `store-max-batch-size` to `1024` [#9020](https://github.com/tikv/tikv/pull/9020)
    - Add the `max-background-flushes` configuration item [#8947](https://github.com/tikv/tikv/pull/8947)
    - Enable the unified read pool for the storage module by default [#8887](https://github.com/tikv/tikv/pull/8887)
    - Add a check to avoid corruption caused by the RocksDB block cache error [#9029](https://github.com/tikv/tikv/pull/9029)
    - Disable `force-consistency-checks` by default to improve performance [#9029](https://github.com/tikv/tikv/pull/9029)

+ PD

    - Check TiKV cluster version when a TiKV stores become tombstone [#3213](https://github.com/pingcap/pd/pull/3213)
    - Disallow the TiKV store of a lower version to change from `Tombstone` back to `Up` [#3206](https://github.com/pingcap/pd/pull/3206)
    - Update Dashboard to `v2020.11.26.1` [#3219](https://github.com/pingcap/pd/pull/3219)

+ TiFlash

    - Reduce the latency of replica reads
    - Refine TiFlash's error message
    - Limit the memory usage of cache data under huge volume data
    - Add a metric for the number of handling coprocessor tasks

+ Tools

    + Backup & Restore (BR)

        - BR no longer accepts --checksum false in command line, which did not disable checksum. The correct usage always include the = sign: --checksum=false [#588](https://github.com/pingcap/br/pull/588)
        - Support change PD configuration temporary [#596](https://github.com/pingcap/br/pull/596)
        - Support analyze table after restore [#622](https://github.com/pingcap/br/pull/622)
        - Retry for read index not ready and proposal in merging mode [#626](https://github.com/pingcap/br/pull/626)

    + TiCDC

        - Metrics: add alert for tikv hibernate Regions [#1120](https://github.com/pingcap/ticdc/pull/1120)
        - Reduce memory usage in schema storage by avoiding table info replication [#1127](https://github.com/pingcap/ticdc/pull/1127)

    + Dumpling

        - Retry dumping on failed chunks [#182](https://github.com/pingcap/dumpling/pull/182)
        - Support configuring both -F and -r arguments at the same time [#177](https://github.com/pingcap/dumpling/pull/177)
        - Exclude system databases in --filter parameter by default [#194](https://github.com/pingcap/dumpling/pull/194)
        - Support --transactional-consistency parameter and support rebuild mysql connections during retry [#199](https://github.com/pingcap/dumpling/pull/199)

    + TiDB Lightning

        - Filter out all system schemas by default [#459](https://github.com/pingcap/tidb-lightning/pull/459)
        - Support set a default value for auto random primary key for local/importer backend [#457](https://github.com/pingcap/tidb-lightning/pull/457)
        - Use range properties to make range split more precise with local backend [#422](https://github.com/pingcap/tidb-lightning/pull/422)
        - `tikv-importer.region-split-size`, `mydumper.read-block-size`, `mydumper.batch-size` and `mydumper.max-region-size` can now accept human-readable format in the form "2.5 GiB" [#471](https://github.com/pingcap/tidb-lightning/pull/471)

    + TiDB Binlog

        - Exit Drainer process with non-zero code if upstream PD is down or apply DDL/DML to downstream failed [#1012](https://github.com/pingcap/tidb-binlog/pull/1012)

## Bug Fixes

+ TiDB

    - Fix incorrect results when using a prefix index with OR condition [#21287](https://github.com/pingcap/tidb/pull/21287)
    - Fix a bug that causes panic when `retry` is enabled [#21285](https://github.com/pingcap/tidb/pull/21285)
    - Fix a bug of partition definition checking. The value comparison should be in accord with column type [#21273](https://github.com/pingcap/tidb/pull/21273)
    - Fix a bug of partition table's partition column values type check [#21136](https://github.com/pingcap/tidb/pull/21136)
    - Fix a bug that hash type partition does not check partition name is unique [#21257](https://github.com/pingcap/tidb/pull/21257)
    - Fix insert value into hash partition table which not int [#21238](https://github.com/pingcap/tidb/pull/21238)
    - Fix unexpected error when `INSERT` meets index join in some cases [#21249](https://github.com/pingcap/tidb/pull/21249)
    - Fix bigint unsigned column value in CASE WHEN operator is converted to bigint signed [#21236](https://github.com/pingcap/tidb/pull/21236)
    - Fix a bug that index-hash-join and index-merge-join does not consider collation [#21219](https://github.com/pingcap/tidb/pull/21219)
    - Fix a bug that partition table does not consider collation in `create table` and `select` sentence [#21181](https://github.com/pingcap/tidb/pull/21181)
    - Fix issue of the query result of slow_query might miss some rows [#21211](https://github.com/pingcap/tidb/pull/21211)
    - `DELETE` might not delete data correctly when the database name is not in pure lower representation [#21206](https://github.com/pingcap/tidb/pull/21206)
    - Fix a bug causes schema change after DML [#21050](https://github.com/pingcap/tidb/pull/21050)
    - Fix the bug that can not query the coalesced column when use using-join [#21021](https://github.com/pingcap/tidb/pull/21021)
    - Fix wrong results for some semi-join queries [#21019](https://github.com/pingcap/tidb/pull/21019)
    - Fix table lock for update statement [#21002](https://github.com/pingcap/tidb/pull/21002)
    - Fix stack overflow when building recursive view [#21001](https://github.com/pingcap/tidb/pull/21001)
    - Fix unexpected results when do merge join on outer join [#20954](https://github.com/pingcap/tidb/pull/20954)
    - Fix the issue that sometimes a transaction that has an undetermined result might be treated as failed [#20925](https://github.com/pingcap/tidb/pull/20925)
    - Fix issue `explain for connection` cannot show the last query plan [#21315](https://github.com/pingcap/tidb/pull/21315)
    - Fix the issue that when Index Merge is used in a transaction with RC isolation level, the result might be incorrect [#21253](https://github.com/pingcap/tidb/pull/21253)
    - Fix auto-id allocation failed because of the transaction's write-conflict retry [#21079](https://github.com/pingcap/tidb/pull/21079)
    - Fix The JSON Data can not import to TiDB correctly by `load data` [#21074](https://github.com/pingcap/tidb/pull/21074)
    - Set correct default value for new added enum column [#20998](https://github.com/pingcap/tidb/pull/20998)
    - Expression: keep the original data type when doing date arithmetic operations [#21176](https://github.com/pingcap/tidb/pull/21176)
    - Fix the wrong point get plan generation in fast plan code path [#21244](https://github.com/pingcap/tidb/pull/21244)

+ TiKV

    - Fix a bug that Coprocessor might return wrong result when there are more than 255 columns [#9131](https://github.com/tikv/tikv/pull/9131)
    - Fix an issue that Region merge might cause data loss during network partition [#9108](https://github.com/tikv/tikv/pull/9108)
    - Fix a bug might cause analyze statement panic when using the latin1 character set [#9082](https://github.com/tikv/tikv/pull/9082)
    - Fix cast decimal as time expr get wrong result when deal with numbers argument [#9031](https://github.com/tikv/tikv/pull/9031)
    - Fix the bug that lightning fails to ingest sst files to TiKV with importer/local backend when TDE is enabled [#8995](https://github.com/tikv/tikv/pull/8995)
    - Config: fix invalid advertise-status-addr [#9036](https://github.com/tikv/tikv/pull/9036)
    - Fix the issue that reports a key-exist error when a key is locked and deleted by a committed transaction. [#8930](https://github.com/tikv/tikv/pull/8930)

+ PD

    - Fix the issue that the leader role does not take effect when using the replacement rule in some cases [#3208](https://github.com/pingcap/pd/pull/3208)
    - Fix the bug that `trace-region-flow` will be accidentally changed to `false` [#3120](https://github.com/pingcap/pd/pull/3120)
    - Fix a bug that service safe points with infinite TTL might disappear [#3143](https://github.com/pingcap/pd/pull/3143)

+ TiFlash

    - Fix the problem that `INFORMATION_SCHEMA.CLUSTER_HARDWARE` might contain information about disks not in use
    - Fix the issue that the memory consumption statistic of Delta Cache is smaller than actual the usage
    - Fix memory leak about thread info statistics

+ Tools

    + Backup & Restore (BR)

        - Fix special characters in S3 secret access keys [#617](https://github.com/pingcap/br/pull/617)

    + TiCDC

        - Fix the bug that multiple owners could exist when owner campaign key is deleted [#1104](https://github.com/pingcap/ticdc/pull/1104)

    + Dumpling

        - Fix the problem that dumpling might get blocked when its connection to database server is closed [#190](https://github.com/pingcap/dumpling/pull/190)

    + TiDB Lightning

        - Fix a bug about encoding data with wrong field information [#437](https://github.com/pingcap/tidb-lightning/pull/437)
        - Fix a bug that GC life time ttl does not take effect [#448](https://github.com/pingcap/tidb-lightning/pull/448)
        - Fix a bug that causes panic when manually stops TiDB Lightning import in Local-backend mode [#484](https://github.com/pingcap/tidb-lightning/pull/484)
