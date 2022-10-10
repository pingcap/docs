---
title: TiDB 5.4.3 Release Notes
---

# TiDB 5.4.3 Release Notes

Release date: x x, 2022

TiDB version: 5.4.3

## Compatibility changes

## Improvements

+ TiDB **TW: @TomShawn**

    <!--sql-infra **owner: @zimulala**-->

    <!--execution **owner: @zanmato1984**-->

    <!--transaction **owner: @cfzjywxk**-->

    <!--planner **owner: @winoros**-->

    <!--diagnosis **owner: @mornyx**-->

+ TiKV **owner: @tabokie, TW: @Oreoxmt**

    - Support configuring RocksDB write stall settings with values smaller than flow control thresholds [#13467](https://github.com/tikv/tikv/issues/13467)
    - (dup) Support configuring the `unreachable_backoff` item to avoid Raftstore broadcasting too many messages after one peer becomes unreachable [#13054](https://github.com/tikv/tikv/issues/13054)

+ PD **owner: @nolouch, TW: @Oreoxmt**

+ TiFlash **TW: @shichun-0415**

+ Tools

    + TiDB Lightning **owner: @niubell, TW: @ran-huang**

        - (dup) Optimize Scatter Region to batch mode to improve the stability of the Scatter Region process [#33618](https://github.com/pingcap/tidb/issues/33618)

    + TiDB Data Migration (DM) **owner: @niubell, TW: @ran-huang**

    + TiCDC **owner: @nongfushanquan, TW: @shichun-0415**

        - (dup) Reduce performance overhead caused by runtime context switching in multi-Region scenarios [#5610](https://github.com/pingcap/tiflow/issues/5610)

    + Backup & Restore (BR) **owner: @3pointer**

    + Dumpling **owner: @niubell, TW: @ran-huang**

    + TiDB Binlog

## Bug fixes

+ TiDB **TW: @TomShawn**

    <!--sql-infra **owner: @zimulala**-->
    - (dup) Fix the incorrect output of `SHOW CREATE PLACEMENT POLICY` [#37526](https://github.com/pingcap/tidb/issues/37526)
    - (dup) Fix the issue that some DDL statements might be stuck for a period after the PD node of a cluster is replaced [#33908](https://github.com/pingcap/tidb/issues/33908)
    - (dup) Fix the issue that `KILL TIDB` cannot take effect immediately on idle connections [#24031](https://github.com/pingcap/tidb/issues/24031)
    - Fix the issue that TiDB gets the incorrect result of `DATA_TYPE` and `COLUMN_TYPE` columns when executing the `SHOW COLUMNS` statement [#36496](https://github.com/pingcap/tidb/issues/36496)
    - (dup) Fix the issue that when TiDB Binlog is enabled, executing the `ALTER SEQUENCE` statement might cause a wrong metadata version and cause Drainer to exit [#36276](https://github.com/pingcap/tidb/issues/36276)

    <!--execution **owner: @zanmato1984**-->

    - (dup) Fix the issue that the `UNION` operator might return unexpected empty result [#36903](https://github.com/pingcap/tidb/issues/36903)
    - (dup) Fix the wrong result that occurs when enabling dynamic mode in partitioned tables for TiFlash [#37254](https://github.com/pingcap/tidb/issues/37254)
    - (dup) Fix the issue that `INL_HASH_JOIN` might hang when used with `LIMIT` [#35638](https://github.com/pingcap/tidb/issues/35638)
    - (dup) Fix the issue that TiDB might return the `invalid memory address or nil pointer dereference` error when executing the `SHOW WARNINGS` statement [#31569](https://github.com/pingcap/tidb/issues/31569)

    <!--transaction **owner: @cfzjywxk**-->

    - Fix `invalid transaction` error when doing stale read in RC isolation level [#30872](https://github.com/pingcap/tidb/issues/30872)
    - (dup) Fix the issue that the `EXPLAIN ANALYZE` statement with DML executors might return result before the transaction commit finishes [#37373](https://github.com/pingcap/tidb/issues/37373)
    - (dup) Fix the issue of the `data and columnID count not match` error that occurs when inserting duplicated values with TiDB Binlog enabled [#33608](https://github.com/pingcap/tidb/issues/33608)

    <!--planner **owner: @winoros**-->

    - (dup) Fix the issue that in the static partition prune mode, SQL statements with an aggregate condition might return wrong result when the table is empty [#35295](https://github.com/pingcap/tidb/issues/35295)
    - (dup) Fix the issue that TiDB might panic when executing the `UPDATE` statement [#32311](https://github.com/pingcap/tidb/issues/32311)
    - (dup) Fix the issue of wrong query result because the `UnionScan` operator cannot maintain the order [#33175](https://github.com/pingcap/tidb/issues/33175)
    - (dup) Fix the issue that the UPDATE statements incorrectly eliminate the projection in some cases, which causes the `Can't find column` error  [#37568](https://github.com/pingcap/tidb/issues/37568)
    - (dup) Fix the issue that partitioned tables cannot fully use indexes to scan data in some cases [#33966](https://github.com/pingcap/tidb/issues/33966)
    - Fix the issue that the `EXECUTE` might throw an unexpected error in specific scenarios [#37187](https://github.com/pingcap/tidb/issues/37187)
    - Fix the issue that TiDB might get wrong results when using a `BIT` type index and enabling the prepared plan cache [#33067](https://github.com/pingcap/tidb/issues/33067)

    <!--diagnosis **owner: @mornyx**-->

+ TiKV **owner: @tabokie, TW: @Oreoxmt**

    - Fix the issue that causes permission denied when TiKV gets an error from the web identity provider and fails back to the default provider [#13122](https://github.com/tikv/tikv/issues/13122)
    - (dup) Fix the issue that the PD client might cause deadlocks [#13191](https://github.com/tikv/tikv/issues/13191)
    - (dup) Fix the issue that PD does not reconnect to TiKV after the Region heartbeat is interrupted [#12934](https://github.com/tikv/tikv/issues/12934)
    - (dup) Fix the issue that Regions might be overlapped if Raftstore is busy [#13160](https://github.com/tikv/tikv/issues/13160)

+ PD **owner: @nolouch, TW: @Oreoxmt**

    - Fix the issue that PD could not handle dashboard proxy requests correctly [#5321](https://github.com/tikv/pd/issues/5321)
    - (dup) Fix the issue that a removed tombstone store appears again after the PD leader transfer ​​[#4941](https://github.com/tikv/pd/issues/4941)
    - (dup) Fix the issue that the TiFlash learner replica might not be created [#5401](https://github.com/tikv/pd/issues/5401)

+ TiFlash **TW: @shichun-0415**

    <!--compute **owner: @zanmato1984**-->

    - (dup) Fix the issue that the `format` function might return a `Data truncated` error [#4891](https://github.com/pingcap/tiflash/issues/4891)
    - (dup) Fix the issue that TiFlash might crash due to an error in parallel aggregation [#5356](https://github.com/pingcap/tiflash/issues/5356)

    <!--storage **owner: @flowbehappy**-->

    - (dup) Fix the panic that occurs after creating the primary index with a column containing the `NULL` value [#5859](https://github.com/pingcap/tiflash/issues/5859)

+ Tools

    + TiDB Lightning **owner: @niubell, TW: @ran-huang**

        - Fix the issue of BigInt auto_increment column out of range error [#27397](https://github.com/pingcap/tidb/issues/27937)
        - (dup) Fix the issue that de-duplication might cause TiDB Lightning to panic in extreme cases [#34163](https://github.com/pingcap/tidb/issues/34163)
        - (dup) Fix the issue that TiDB Lightning does not support columns starting with slash, number, or non-ascii characters in Parquet files [#36980](https://github.com/pingcap/tidb/issues/36980)
        - (dup) Fix the issue that TiDB Lightning fails to connect to TiDB when TiDB uses an IPv6 host [#35880](https://github.com/pingcap/tidb/issues/35880)

    + TiDB Data Migration (DM) **owner: @niubell, TW: @ran-huang**

        - (dup) Fix the issue that DM Worker might get stuck when getting DB Conn [#3733](https://github.com/pingcap/tiflow/issues/3733)
        - (dup) Fix the issue that DM reports the `Specified key was too long` error [#5315](https://github.com/pingcap/tiflow/issues/5315)
        - (dup) Fix the issue that latin1 data might be corrupted during replication [#7028](https://github.com/pingcap/tiflow/issues/7028)
        - (dup) Fix the issue that DM fails to start when TiDB uses an IPv6 host [#6249](https://github.com/pingcap/tiflow/issues/6249)
        - (dup) Fix the issue of possible data race in `query-status` [#4811](https://github.com/pingcap/tiflow/issues/4811)
        - (dup) Fix goroutine leak when relay meets an error [#6193](https://github.com/pingcap/tiflow/issues/6193)

    + TiCDC **owner: @nongfushanquan, TW: @shichun-0415**

        - (dup) Fix the TiCDC panic issue when you set `enable-old-value = false` [#6198](https://github.com/pingcap/tiflow/issues/6198)

    + Backup & Restore (BR) **owner: @3pointer, TW: @shichun-0415**

        - (dup) Fix the issue that might lead to backup and restoration failure if special characters exist in the authorization key of external storage [#37469](https://github.com/pingcap/tidb/issues/37469)
        - (dup) Fix the issue that the regions are not balanced because the concurrency is set too large during the restoration [#37549](https://github.com/pingcap/tidb/issues/37549)

    + Dumpling **owner: @niubell, TW: @ran-huang**

        - (dup) Fix the issue that GetDSN does not support IPv6 [#36112](https://github.com/pingcap/tidb/issues/36112)

    + TiDB Binlog
