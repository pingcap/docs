---
title: TiDB 5.0.6 Release Notes
category: Releases
---



# TiDB 5.0.6 Release Notes

Release Date: December 21, 2021

TiDB version: 5.0.6

## __unsorted

+ PingCAP/TiDB

    - This is a fix for grant global level case in v4.0 and v5.0 [#30161](https://github.com/pingcap/tidb/pull/30161)
    - Fix an issue that adding index panics by chance. [#30125](https://github.com/pingcap/tidb/pull/30125)
    - fix wrong result type for greatest/least [#29912](https://github.com/pingcap/tidb/pull/29912)
    - Prevent conflicted optimistic transactions from locking each other. [#29776](https://github.com/pingcap/tidb/pull/29776)
    - config: fix the bug that enforce-mpp *config item* is useless in v5.0.4 [#29637](https://github.com/pingcap/tidb/pull/29637)
    - Fix panic for caseWhen function with enum type [#29509](https://github.com/pingcap/tidb/pull/29509)
    - Fix wrong result of microsecond function in vectorized [#29385](https://github.com/pingcap/tidb/pull/29385)
    - Fix incomplete log information about auto analyze. [#29228](https://github.com/pingcap/tidb/pull/29228)
    - Fix wrong result of hour function in vectorized expression [#28871](https://github.com/pingcap/tidb/pull/28871)
    - Fix unexpected error like `tidb_cast to Int32 is not supported` when unsupported cast is pushed down to TiFlash [#28651](https://github.com/pingcap/tidb/pull/28651)
    - Fix bug that mpp node availability detect does not work in some corner cases [#28287](https://github.com/pingcap/tidb/pull/28287)
    - sessionctx: fix data-race bug when alloc task id [#28284](https://github.com/pingcap/tidb/pull/28284)
    - Fix index out of bound bug when empty dual table is remove for mpp query [#28278](https://github.com/pingcap/tidb/pull/28278)
    - Avoid false positive error log about `invalid cop task execution summaries length` when running MPP query. [#28262](https://github.com/pingcap/tidb/pull/28262)
    - Fixed a bug that causes TiDB panic when inserting invalid date value concurrently. [#28198](https://github.com/pingcap/tidb/pull/28198)
    - Fix `can not found column in Schema column` error for mpp queries [#28147](https://github.com/pingcap/tidb/pull/28147)
    - Fix a bug that TiDB may crash when TiFlash is shutting down. [#28138](https://github.com/pingcap/tidb/pull/28138)
    - None. [#27927](https://github.com/pingcap/tidb/pull/27927)


+ TiKV/TiKV

    - Fix resolved ts lag increased after stoping a tikv [#11538](https://github.com/tikv/tikv/pull/11538)
    - Fix connection abort when too many raft entries are batched into one messages [#11532](https://github.com/tikv/tikv/pull/11532)
    - Fix panic in rare conditions when merge, conf change and snapshot happen at the same time [#11510](https://github.com/tikv/tikv/pull/11510)
    - Fix the issue that reverse scan can't detect memory locks and may read stale data. [#11453](https://github.com/tikv/tikv/pull/11453)
    - Fix GC scan effectiveness to avoid OOM [#11419](https://github.com/tikv/tikv/pull/11419)
    - None. [#11381](https://github.com/tikv/tikv/pull/11381)
    - fix negative sign when decimal divide to zero [#11333](https://github.com/tikv/tikv/pull/11333)
    - Fix incorrect by-instance gRPC average duration. [#11327](https://github.com/tikv/tikv/pull/11327)
    - move verify_checksum to import-thread from apply-thread. [#11257](https://github.com/tikv/tikv/pull/11257)
    - Fix label leaking of thread metrics [#11201](https://github.com/tikv/tikv/pull/11201)
    - Fix CDC panic due to missing downstream. [#11136](https://github.com/tikv/tikv/pull/11136)
    - Fix frequent CDC incremental scan retry due to `Congest` error. [#11090](https://github.com/tikv/tikv/pull/11090)
    - fix channel full could break the raft connection [#11070](https://github.com/tikv/tikv/pull/11070)
    - Hide untouched storage commands' metrics in grafana dashboard [#11001](https://github.com/tikv/tikv/pull/11001)
    - Do not delete import files during Lightning import. [#10740](https://github.com/tikv/tikv/pull/10740)
    - copr: fix Max/Min bug when comparing signed and unsigned int64 [#10617](https://github.com/tikv/tikv/pull/10617)
    - - fix follower meta corruption in rare cases with more than 4 replicas [#10500](https://github.com/tikv/tikv/pull/10500)
    - ```release-note [#10361](https://github.com/tikv/tikv/pull/10361)
    - copr cast invalid utf8 string to real bug fix [#9871](https://github.com/tikv/tikv/pull/9871)


+ PingCAP/TiFlash

    - Fix potential data inconsistency when widen pk column type if pk is handle [#3572](https://github.com/pingcap/tics/pull/3572)
    - Fix the bug that results of `where <string>` is wrong because it will be converted to int type. [#3477](https://github.com/pingcap/tics/pull/3477)
    - Fix tiflash randomly crash when a mpp query is killed. [#3448](https://github.com/pingcap/tics/pull/3448)
    - Fix the issue of unexpected error that `Unexpected type of column: Nullable(Nothing)` [#3376](https://github.com/pingcap/tics/pull/3376)
    -  [#2349](https://github.com/pingcap/tics/pull/2349)


+ PD

    - fix the problem that the hot cache cannot be emptied when the interval is less than 60 [#4432](https://github.com/tikv/pd/pull/4432)
    - None. [#4288](https://github.com/tikv/pd/pull/4288)
    - speed scheduler exit [#4201](https://github.com/tikv/pd/pull/4201)
    - allow empty region to be scheduled and use a sperate tolerance config in scatter range scheduler [#4116](https://github.com/tikv/pd/pull/4116)


+ Tools

    + PingCAP/BR

        - Increase the robustness for restoring. [#1438](https://github.com/pingcap/br/pull/1438)
        - ```release-note [#1436](https://github.com/pingcap/br/pull/1436)
        - Expression index and index depending on virtual generated columns are now valid. Previously these indices are broken when importing through Lightning local or importer backend. [#1419](https://github.com/pingcap/br/pull/1419)
        - fix the bug that the average speed isn't accurate in backup and restore [#1411](https://github.com/pingcap/br/pull/1411)


    + PingCAP/Dumpling

        - fix the bug that dumpling gets very slow when dumping composite primary/unique key tables. [#399](https://github.com/pingcap/dumpling/pull/399)


    + PingCAP/TiCDC

        - None (not released yet) [#4000](https://github.com/pingcap/tiflow/pull/4000)
        - ```release-note [#3922](https://github.com/pingcap/tiflow/pull/3922)
        - Fix timezone related error that cause cdc server can't run in some RHEL release version (6.8, 6.9 etc). [#3908](https://github.com/pingcap/tiflow/pull/3908)
        - Fix mounter default date value not support [#3856](https://github.com/pingcap/tiflow/pull/3856)
        - Reduce log "synchronize is taking too long, report a bug" in some cases. [#3797](https://github.com/pingcap/tiflow/pull/3797)
        - Fix the problem that old value is not forced on automatically in Canal and Maxwell protocols [#3780](https://github.com/pingcap/tiflow/pull/3780)
        - `None`. [#3762](https://github.com/pingcap/tiflow/pull/3762)
        - The Avro sink was updated to handle JSON columns [#3651](https://github.com/pingcap/tiflow/pull/3651)
        - Please add a release note.
If you don't think this PR needs a release note then fill it with `None`. [#3566](https://github.com/pingcap/tiflow/pull/3566)
        - fix changefeed checkpoint lag negative value error [#3533](https://github.com/pingcap/tiflow/pull/3533)
        - Fix OOM in container environments. [#3441](https://github.com/pingcap/tiflow/pull/3441)
        - Please add a release note.
If you don't think this PR needs a release note then fill it with `None`. [#3391](https://github.com/pingcap/tiflow/pull/3391)
        - Show changefeed checkepoint catch-up ETA in metrics. [#3314](https://github.com/pingcap/tiflow/pull/3314)
        - Fix a bug that TiCDC could meet replication interruption when multiple TiKVs crash or forcing restart. [#3291](https://github.com/pingcap/tiflow/pull/3291)
        - Fix memory leak after processing DDLs. [#3275](https://github.com/pingcap/tiflow/pull/3275)
        - Please add a release note.
If you don't think this PR needs a release note then fill it with `None`. [#3268](https://github.com/pingcap/tiflow/pull/3268)
        - `None`. [#3211](https://github.com/pingcap/tiflow/pull/3211)
        - Please add a release note.
If you don't think this PR needs a release note then fill it with `None`. [#3177](https://github.com/pingcap/tiflow/pull/3177)
        - bugfix: fix changefeed does not fast fail when occur ErrGCTTLExceeded error. [#3135](https://github.com/pingcap/tiflow/pull/3135)
        - Optimize the rate limit control when TiKV reloads and fix the congestion in gPRC, which may cause slow initialization phase. [#3132](https://github.com/pingcap/tiflow/pull/3132)
        - change Kafka sink default `MaxMessageBytes` to 1MB. [#3107](https://github.com/pingcap/tiflow/pull/3107)
        - fix the bug that fallback resolvedTs event  will block the progress of resolve lock when occur region merging [#3100](https://github.com/pingcap/tiflow/pull/3100)
        - Close gPRC stream and re-create it when meeting `ErrPrewriteNotMatch` to avoid duplicated request error [#3091](https://github.com/pingcap/tiflow/pull/3091)
        - fix kafka sink can not send message due to constraint by `max-message-size` option. [#3047](https://github.com/pingcap/tiflow/pull/3047)
        - Nond [#3043](https://github.com/pingcap/tiflow/pull/3043)
        - Add metrics to observe incremental scan remaining time [#3033](https://github.com/pingcap/tiflow/pull/3033)
        - Fix tikv_cdc_min_resolved_ts_no_change_for_1m keep firing when there is no changefeed. [#3024](https://github.com/pingcap/tiflow/pull/3024)
        - Fix possible deadlocking when Kafka producer reports an error. [#3016](https://github.com/pingcap/tiflow/pull/3016)
        - Release new owner and processor implementation to release-5.0.
Highly available model and core modules refactoring.(ref: https://github.com/pingcap/ticdc/pull/1927) [#2946](https://github.com/pingcap/tiflow/pull/2946)
        - `None`. [#2918](https://github.com/pingcap/tiflow/pull/2918)
        - ignore the global flag for changefeed update command. [#2876](https://github.com/pingcap/tiflow/pull/2876)
        - Fix dml is not replicated after adding partition in partition table without valid index [#2864](https://github.com/pingcap/tiflow/pull/2864)
        - Extend creating service gc safepoint ttl to 1 hr to support creating changefeeds that needs long initialization time. [#2852](https://github.com/pingcap/tiflow/pull/2852)
        - Fix json encoding could panic when processing a string type value in some cases. [#2782](https://github.com/pingcap/tiflow/pull/2782)
        - Fixed a bug in DDL handling when the owner restarts. [#2610](https://github.com/pingcap/tiflow/pull/2610)
        - Fix the bug that table is not replicated when it changes from ineligible to eligible by DDL [#1488](https://github.com/pingcap/tiflow/pull/1488)


## Bug Fixes

+ PingCAP/TiDB

    - ```release-note [#30881](https://github.com/pingcap/tidb/pull/30881)
    - Fix wrong result for control function with enum type. [#30857](https://github.com/pingcap/tidb/pull/30857)
    - bugfix: concat(ifnull(time(3)) returns different results from MySQL [#30830](https://github.com/pingcap/tidb/pull/30830)
    - Fix wrong result of greatest/least Function. [#30791](https://github.com/pingcap/tidb/pull/30791)
    - Fix the bug that sql got cancel if including json column joins char column. [#30778](https://github.com/pingcap/tidb/pull/30778)
    - Fix the data inconsistency caused by incorrect usage of lazy existence check and untouch key optimization. [#30533](https://github.com/pingcap/tidb/pull/30533)
    - Fix the problem that window function may return different results when using transaction or not. [#30389](https://github.com/pingcap/tidb/pull/30389)
    - Fix wrong flen for CastAsString funtion [#30055](https://github.com/pingcap/tidb/pull/30055)
    - ```release-note [#30049](https://github.com/pingcap/tidb/pull/30049)
    - expression: Fix the issue that length information is wrong when converting Decimal to String [#30014](https://github.com/pingcap/tidb/pull/30014)
    - expression: fix different results for greatest when vectorized is off. [#29917](https://github.com/pingcap/tidb/pull/29917)
    - planner: fix the issue that planner may cache invalid plans for joins in some cases [#28445](https://github.com/pingcap/tidb/pull/28445)
    - Keep the original join schema in predicate pushdown [#28295](https://github.com/pingcap/tidb/pull/28295)


+ PingCAP/TiFlash

    - Align unix_timestamp behavior with TiDB and mysql when input is earlier than 1970-01-01 00:00:01 UTC [#3622](https://github.com/pingcap/tics/pull/3622)
    - fix the issue that comparison between Decimal may cause overflow and report `Can't compare`. [#3366](https://github.com/pingcap/tics/pull/3366)
    - Fix the issue of unexpected error that `3rd arguments of function substringUTF8 must be constants.` [#3266](https://github.com/pingcap/tics/pull/3266)
    - Fix the issue that TiFlash fails to start up under platform without library `nsl` [#3205](https://github.com/pingcap/tics/pull/3205)
    - ```release-note [#2701](https://github.com/pingcap/tics/pull/2701)
    - Fix problem that TiDB Dashboard can not display disk information of TiFlash correctly in some situations. [#2397](https://github.com/pingcap/tics/pull/2397)


+ PD

    - Fix panic issue after TiKV node scales in [#4379](https://github.com/tikv/pd/pull/4379)
    - Fix the issue that operator can get blocked due to down store [#4367](https://github.com/tikv/pd/pull/4367)
    - Fix the issue that PD may not elect leader as soon as leader step down [#4218](https://github.com/tikv/pd/pull/4218)
    - `evict-leader-scheduler` supports schedule the regions with unhealthy peers. [#4130](https://github.com/tikv/pd/pull/4130)


