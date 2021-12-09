---
title: TiDB 4.0.16 Release Notes
---

# TiDB 4.0.16 Release Notes

Release Date: December 10, 2021

TiDB version: 4.0.16

## Compatibility changes

+ TiKV

    - When casting an invalid utf8 string to real, try to truncate the utf8 prefix instead of returning an error [#11466](https://github.com/tikv/tikv/issues/11466)

+ Tools

    + TiCDC

        - Change the default value of Kafka Sink `max-message-bytes` to 1 MB [#2962](https://github.com/pingcap/ticdc/issues/2962)
        - Change the default value of Kafka Sink `partition-num` to 3 [#3337](https://github.com/pingcap/ticdc/issues/3337)

## Improvements

+ TiKV

    - sst_importer: Reduce the space usage when using BR-Restore or Lightning-Local-backend by using zstd compression in SSTs  [#11469](https://github.com/tikv/tikv/issues/11469)

+ Tools

    + Backup & Restore (BR)

        - Improve the robustness for restoring [#27421](https://github.com/pingcap/tidb/issues/27421)

    + TiCDC

        - Add a rate limiter to limit the EtcdWorker tick frequency [#3112](https://github.com/pingcap/ticdc/issues/3112)
        - Optimize rate limit control when TiKV reloads. Fix congestion in gPRC, which may cause slow initialization [#3110](https://github.com/pingcap/ticdc/issues/3110)
        - Ignore the global flag of the changefeed update command [#2803](https://github.com/pingcap/ticdc/issues/2803)
        - Prohibit operating TiCDC clusters across major and minor versions [#3352](https://github.com/pingcap/ticdc/issues/3352)

## Bug fixes

+ TiDB

    - Fix the query panic caused by overflow in the statistics module when converting a range to points for cost estimation [#23625](https://github.com/pingcap/tidb/issues/23625)
    - Fix wrong results of the control functions (such as `IF` and `CASE WHEN`) when using the `ENUM` type data as parameters of such functions [#23114](https://github.com/pingcap/tidb/issues/23114)
    - Fix inconsistent results of the `GREATEST` function when setting `tidb_enable_vectorized_expression` to `on` or `off` [#29434](https://github.com/pingcap/tidb/issues/29434)
    - Fix the panic when applying index join on prefix indexes in some cases [#24547](https://github.com/pingcap/tidb/issues/24547)
    - Fix the issue that planner might cache invalid plans for `join` in some cases [#28087](https://github.com/pingcap/tidb/issues/28087)
    - Fix a bug that TiDB cannot insert `null` into a non-null column when `sql_mode` is empty [#11648](https://github.com/pingcap/tidb/issues/11648)
    - Fix the wrong result type of the `GREATEST` and`LEAST` functions [#29019](https://github.com/pingcap/tidb/issues/29019)
    - Fix the `privilege check fail` error when performing the `grant` and `revoke` operations to grant global level privileges [#29675](https://github.com/pingcap/tidb/issues/29675)
    - Fix the panic when using the `CASE WHEN` function on the `ENUM` data type [#29357](https://github.com/pingcap/tidb/issues/29357)
    - Fix wrong results of the `microsecond` function in vectorized expressions [#29244](https://github.com/pingcap/tidb/issues/29244)
    - (dup) Fix wrong results of the `hour` function in vectorized expression [#28643](https://github.com/pingcap/tidb/issues/28643)
    - Fix the issue that optimistic transaction conflicts might cause transactions blocking each other [#11148](https://github.com/tikv/tikv/issues/11148)
    - Fix the issue of incomplete log information from the `auto analyz` result [#29188](https://github.com/pingcap/tidb/issues/29188)
    - Fix an issue that `NO_ZERO_IN_DATE` does not work on the default values [#26766](https://github.com/pingcap/tidb/issues/26766)
    - Fix the issue that the Coprocessor Cache panel in Grafana does not display metrics. Now, Grafana displays the number of `hits`/`miss`/`evict`. [#26338](https://github.com/pingcap/tidb/issues/26338)
    - Fix the issue that concurrently truncating the same partition hangs DDL [#26229](https://github.com/pingcap/tidb/issues/26229)
    - Fix the issue that when the `CONCAT` function has a negative float type argument, the last digit of the argument number is chopped in the result  [#29417](https://github.com/pingcap/tidb/issues/29417)
    - Fix the issue of an extra column in the query result when `NATURAL JOIN` is used to join multiple tables [#29481](https://github.com/pingcap/tidb/issues/29481)
    - Fix the issue that `TopN` is wrongly pushed down to `indexPlan` when `IndexScan` is using a prefix index [#29711](https://github.com/pingcap/tidb/issues/29711)
    - Fix the issue that retrying transactions with `DOUBLE` type auto-increment columns causes data error [#29892](https://github.com/pingcap/tidb/issues/29892)

+ TiKV

    - Fix panic in rare conditions when merge, conf change and snapshot happen at the same time [#11475](https://github.com/tikv/tikv/issues/11475)
    - Make negative sign as false when decimal divide result is zero [#29586](https://github.com/pingcap/tidb/issues/29586)
    - Fix incorrect by-instance gRPC average duration [#11299](https://github.com/tikv/tikv/issues/11299)
    - Fix CDC panic due to missing downstream [#11123](https://github.com/tikv/tikv/issues/11123)
    - (dup) Fix the issue that the Raft connection is broken when the channel is full [#11047](https://github.com/tikv/tikv/issues/11047)
    - Fix Max/Min bug when comparing signed and unsigned int64 [#10158](https://github.com/tikv/tikv/issues/10158)
    - (dup) Fix the issue that CDC adds scan retries frequently due to the Congest error [#11082](https://github.com/tikv/tikv/issues/11082)

+ PD

    - Fix panic issue after TiKV node scales in [#4344](https://github.com/tikv/pd/issues/4344)
    - (dup) Fix slow leader election caused by stucked region syncer [#3936](https://github.com/tikv/pd/issues/3936)
    - (dup) Fix the issue that evict-leader might leave leaders when the cluster has down peers [#4093](https://github.com/tikv/pd/issues/4093)

+ TiFlash

    - Fix the issue that TiFlash fails to start up on some platforms due to the absence of library `nsl`

+ Tools
    
    + TiDB Binlog
        
        - Fix the bug that Drainer exits when transporting a transaction greater than 1 GB [#1078](https://github.com/pingcap/tidb-binlog/pull/1078)
    
    + TiCDC

        - Fix the negative value error in the changefeed checkpoint lag [#3010](https://github.com/pingcap/ticdc/issues/3010)
        - Fix OOM in container environments [#1798](https://github.com/pingcap/ticdc/issues/1798)
        - Fix the TiCDC replication interruption issue when multiple TiKVs crash or during a forced restart [#3288](https://github.com/pingcap/ticdc/issues/3288)
        - Fix the memory leak issue after processing DDLs [#3174](https://github.com/pingcap/ticdc/issues/3174)
        - Fix the issue that changefeed does not fail fast enough when the ErrGCTTLExceeded error occurs [#3111](https://github.com/pingcap/ticdc/issues/3111)
        - (dup) Fix the issue that TiCDC replication task might terminate when the upstream TiDB instance unexpectedly exits [#3061](https://github.com/pingcap/ticdc/issues/3061)
        - (dup) Fix the issue that TiCDC process might panic when TiKV sends duplicate requests to the same Region [#2386](https://github.com/pingcap/ticdc/issues/2386)
        - (dup) Fix the issue that the volume of Kafka messages generated by TiCDC is not constrained by `max-message-size` [#2962](https://github.com/pingcap/ticdc/issues/2962)
        - Fix the issue that `tikv_cdc_min_resolved_ts_no_change_for_1m` keeps alerting when there is no changefeed [#11017](https://github.com/tikv/tikv/issues/11017)
        - (dup) Fix the issue that TiCDC sync task might pause when an error occurs during writing a Kafka message [#2978](https://github.com/pingcap/ticdc/issues/2978)
        - (dup) Fix the issue that some partitioned tables without valid indexes might be ignored when `force-replicate` is enabled [#2834](https://github.com/pingcap/ticdc/issues/2834)
        - Fix the memory leak issue when creating a new changefeed [#2389](https://github.com/pingcap/ticdc/issues/2389)
        - Fix the issue that Sink skips the flush operation when reporting resolved ts [#3503](https://github.com/pingcap/ticdc/issues/3503)
        - (dup) Fix the issue that scanning stock data might fail due to TiKV performing GC when scanning stock data takes too long [#2470](https://github.com/pingcap/ticdc/issues/2470)
