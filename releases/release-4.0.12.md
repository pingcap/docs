---
title: TiDB 4.0.12 Release Notes
---

# TiDB 4.0.12 Release Notes

Release date: March 31, 2021

TiDB version: 4.0.12

## New Features

+ TiFlash

    - Add tools to check exact status of `tiflash replica` for online rolling update

## Improvements

+ TiDB

    - Refine explain info for batch cop [#23164](https://github.com/pingcap/tidb/pull/23164)
    - Add warning info for exprs that can not be pushed to storage layer for explain statement. [#23020](https://github.com/pingcap/tidb/pull/23020)
    - Ddl: migrate part of ddl package code from Execute/ExecRestricted to safe API (2) [#22935](https://github.com/pingcap/tidb/pull/22935)
    - Ddl: migrate part of ddl package code from Execute/ExecRestricted to safe API (1). [#22929](https://github.com/pingcap/tidb/pull/22929)
    - Add optimization-time and wait-TS-time into the slow log [#22918](https://github.com/pingcap/tidb/pull/22918)
    - Support query partition_id from infoschema.partitions [#22489](https://github.com/pingcap/tidb/pull/22489)
    - Add 'last_plan_from_binding' to help know whether sql's plan is matched with the hints in the binding [#21430](https://github.com/pingcap/tidb/pull/21430)
    - Do not report error for prepared stmt execution if tidb_snapshot is set [#22641](https://github.com/pingcap/tidb/pull/22641)
    - Record prepare execute fail as "Failed Query OPM" in monitor [#22672](https://github.com/pingcap/tidb/pull/22672)
    - Add three format specifier for str_to_date expression [#22812](https://github.com/pingcap/tidb/pull/22812)
    - Scattering truncated tables without pre-split option [#22872](https://github.com/pingcap/tidb/pull/22872)

+ TiKV

    * Pd_client: prevent a large number of reconnections in a short time [#9879](https://github.com/tikv/tikv/pull/9879)
    * Optimize seek write for many tombstones [#9729](https://github.com/tikv/tikv/pull/9729)
    * Change the default value of `leader-transfer-max-log-lag` to 128 to increase the success rate of leader transfer [#9605](https://github.com/tikv/tikv/pull/9605)

+ PD

    - Save to the region cache when pending-peers or down-peers change [#3471](https://github.com/pingcap/pd/pull/3471)
    - Checker: prevent the regions in split-cache from becoming the target of merge [#3459](https://github.com/pingcap/pd/pull/3459)

+ TiFlash

    - Optimize configuration file and remove useless items
    - Reduce the size of TiFlash binary file
    - Use an adaptive aggressive GC strategy to reduce memory usage

+ Tools

    + TiCDC

        - Add double confirm when creating or resuming changefeed with start-ts or checkpoint-ts 1 day before current ts [#1497](https://github.com/pingcap/ticdc/pull/1497)

    + Backup & Restore (BR)

        - Log `HTTP_PROXY` and `HTTPS_PROXY`. [#827](https://github.com/pingcap/br/pull/827)
        - Improve backup performance when there are many tables. [#745](https://github.com/pingcap/br/pull/745)
        - Report error if service safe point check fails. [#826](https://github.com/pingcap/br/pull/826)
        - Add cluster_version and br_version info in backupmeta [#803](https://github.com/pingcap/br/pull/803)
        - Added retry for external storage errors. [#851](https://github.com/pingcap/br/pull/851)
        - Reduce memory usage during backup. [#886](https://github.com/pingcap/br/pull/886)

    + TiDB Lightning

        - Check TiDB cluster version before running TiDB-Lightning to avoid unexpected errors. [#787](https://github.com/pingcap/br/pull/787)
        - Fail fast when lightning meets error in engine/chunk restore and do not retry context.Cancel error. [#867](https://github.com/pingcap/br/pull/867)
        - Added configurations tikv-importer.engine-mem-cache-size and tikv-importer.local-writer-mem-cache-size to tune between memory usage and performance. [#866](https://github.com/pingcap/br/pull/866)
        - Run batch split regions in parallel for Lightning local backend. [#868](https://github.com/pingcap/br/pull/868)
        - When using Lightning to import from S3, Lightning no longer require s3:ListBucket permission on the entire bucket, only the data source prefix itself. [#919](https://github.com/pingcap/br/pull/919)
        - When resuming from checkpoint, Lightning now keeps restoring the original engines instead of starting to process some random new ones. [#924](https://github.com/pingcap/br/pull/924)

## Bug Fixes

+ TiDB

    - Fix get var expr when session var is hex literal [#23372](https://github.com/pingcap/tidb/pull/23372)
    - Fix the bug that wrong collation is used when try fast path for enum or set [#23292](https://github.com/pingcap/tidb/pull/23292)
    - Wrong result of nullif expr when used with is null expr [#23279](https://github.com/pingcap/tidb/pull/23279)
    - Statistics: fix a case that auto-analyze is triggered outside its time range [#23219](https://github.com/pingcap/tidb/pull/23219)
    - Executor: fix cast function will ignore the error for point get key construction [#23211](https://github.com/pingcap/tidb/pull/23211)
    - Fixed a bug that prevented SPM from taking effect [#23209](https://github.com/pingcap/tidb/pull/23209)
    - Fix wrong table filters for index merge plan [#23165](https://github.com/pingcap/tidb/pull/23165)
    - Fix unexpected NotNullFlag in case when expr ret type [#23135](https://github.com/pingcap/tidb/pull/23135)
    - Fix a bug that collation is not handle for text type [#23092](https://github.com/pingcap/tidb/pull/23092)
    - Fix range partition prune bug for IN expr [#23074](https://github.com/pingcap/tidb/pull/23074)
    - Fix request block forever when replace a tombstone store with the store has same IP addr [#23071](https://github.com/pingcap/tidb/pull/23071)
    - Do not ajust int when it is null and compared year [#22844](https://github.com/pingcap/tidb/pull/22844)
    - Fix load data lost connection error on tables with auto_random column [#22736](https://github.com/pingcap/tidb/pull/22736)
    - Fix ddl hang over when it meets panic in cancelling path. [#23297](https://github.com/pingcap/tidb/pull/23297)
    - Fix wrong key range of index scan when filter is comparing year column with NULL [#23104](https://github.com/pingcap/tidb/pull/23104)
    - Fix create view success but failed when using it [#23083](https://github.com/pingcap/tidb/pull/23083)

+ TiKV

    - Fix the issue that the IN expr(coprocessor) didn't handle unsigned/signed int properly [#9850](https://github.com/tikv/tikv/pull/9850)
    - Fix the issue that the ingests operation cannot reentrant. [#9779](https://github.com/tikv/tikv/pull/9779)
    - Fix the issue that the space missed when converting json to string in TiKV coprocessor [#9666](https://github.com/tikv/tikv/pull/9666)

+ PD

    - Fix the bug that the isolation level is wrong when the store lacks label [#3474](https://github.com/pingcap/pd/pull/3474)

+ TiFlash

    - Fix an issue of incorrect results when the default value of `binary` type column contains leading or tailing zero bytes
    - Fix the bug that TiFlash fail to sync schema if the name of database contains special characters
    - Fix an issue of incorrect results when handling `IN` expression with decimal values
    - Fix the bug that metrics about opened file count shown in Grafana is high
    - Fix the bug that TiFlash does not support `Timestamp` literal
    - Fix the potential crash while handling `FROM_UNIXTIME` expression
    - Fix an issue of incorrect results when casting string as integer
    - Fix a bug that `like` function may return wrong result

+ Tools

    + TiCDC

        - Fix a resolved ts event disorder problems caused by concurrency [#1464](https://github.com/pingcap/ticdc/pull/1464)
        - Fix a data loss bug when capture restarts due to network issue, and some table on it is scheduled at the same time [#1508](https://github.com/pingcap/ticdc/pull/1508)

    + Backup & Restore (BR)

        - Fix the bug that WalkDir for s3 storage returns nil if the target path is bucket name. [#773](https://github.com/pingcap/br/pull/773)
        - Fixed a bug that caused, even BR started with TLS config, the pprof endpoints won't be served with TLS [#839](https://github.com/pingcap/br/pull/839)

    + TiDB Lightning

        - Fix a bug that importer may ignore write rows error if open engine returns file exists error [#848](https://github.com/pingcap/br/pull/848)
        - Fix a bug that lightning generated ts may be to large or small that query may return incorrect result [#850](https://github.com/pingcap/br/pull/850)
        - Fix a bug that lightning unexpected exit may cause checkpoint file truncated to 0 sized [#889](https://github.com/pingcap/br/pull/889)
        - Fix a bug that chunk restore task may ignore context cancel error and causes data loss [#874](https://github.com/pingcap/br/pull/874)
