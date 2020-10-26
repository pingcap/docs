---
title: TiDB 4.0.8 Release Notes
---

# TiDB 4.0.8 Release Notes

Release date: October 29, 2020

TiDB version: 4.0.8

## New Features

+ TiDB

    - Support new aggregate function APPROX_PERCENTILE [#20197](https://github.com/pingcap/tidb/pull/20197)

+ Tools

    + TiCDC

        - Supports snapshot level consistency replication in time [#932](https://github.com/pingcap/ticdc/pull/932)

## Improvements

+ TiDB

    - Prioritize low selectivity indexes in the greedy search procedure of `Selectivity()` [#20154](https://github.com/pingcap/tidb/pull/20154)
    - Record more RPC runtime information in cop runtime stats [#19264](https://github.com/pingcap/tidb/pull/19264)

+ TiFlash

    - Add metrics about applying Raft logs
    - Make the min-max index more accurate if there are deleted data
    - Improved query performance under small volume data
    - Support CAST functions push down

+ Tools

    + TiCDC

        - Print statistics in MySQL sink [#1023](https://github.com/pingcap/ticdc/pull/1023)

    + Backup and Restore (BR)

        - Speed up restore by pipeline split and restore [#428](https://github.com/pingcap/br/pull/428)
        - Support restoring PD schedulers manually [#530](https://github.com/pingcap/br/pull/530)
        - Use pause instead of remove schedulers [#551](https://github.com/pingcap/br/pull/551)

    + Dumpling

        - Support writing directly to S3 [#155](https://github.com/pingcap/dumpling/pull/155)
        - Support dumping view [#158](https://github.com/pingcap/dumpling/pull/158)
        - Support dumping all generated column table [#166](https://github.com/pingcap/dumpling/pull/166)

    + TiDB Lightning

        - Support multi bytes csv delimiter and separator [#406](https://github.com/pingcap/tidb-lightning/pull/406)
        - Speed up restore by disable some pd scheduler [#408](https://github.com/pingcap/tidb-lightning/pull/408)
        - Use gc ttl api for checksum gc safepoint in v4.0 cluster [#396](https://github.com/pingcap/tidb-lightning/pull/396)

## Bug Fixes

+ TiDB

    - Fix unexpected panic when using partition tables. [#20565](https://github.com/pingcap/tidb/pull/20565)
    - Fix wrong outer join result when filter outer side using index merge join. [#20427](https://github.com/pingcap/tidb/pull/20427)
    - Fix data too long when converting to bit returns a null value [#20363](https://github.com/pingcap/tidb/pull/20363)
    - Fix corrupted default value for bit type column. [#20340](https://github.com/pingcap/tidb/pull/20340)
    - Fix overflow error when convert bit to int64 [#20312](https://github.com/pingcap/tidb/pull/20312)
    - Avoid propagate column optimization for Hybrid type. [#20297](https://github.com/pingcap/tidb/pull/20297)
    - Fix panic when storing outdated plans from plan cache [#20246](https://github.com/pingcap/tidb/pull/20246)
    - Fix a bug that `from_unixtime` + `union all` returns truncated result [#20240](https://github.com/pingcap/tidb/pull/20240)
    - Fix enum value convert to float failed [#20235](https://github.com/pingcap/tidb/pull/20235)
    - Fix panic in RegionStore.accessStore. [#20210](https://github.com/pingcap/tidb/pull/20210)
    - Fix sort result for max unsigned int in batch-point-get [#20205](https://github.com/pingcap/tidb/pull/20205)

+ TiFlash

    - Fix wrong timestamp in log message
    - Fix the issue that when deployed with multi-paths, the wrong capacity make creating TiFlash replicas failed
    - Fix the bug that TiFlash could throw errors about broken data files after the restart
    - Fix the issue that broken files may be left on disk after TiFlash crashed

+ Tools

    + TiCDC

        - Fix unexpected exit due to updating GC safepoint error [#979](https://github.com/pingcap/ticdc/pull/979)
        - Fix task status is always flushed because of incorrect mod revision cache [#1017](https://github.com/pingcap/ticdc/pull/1017)
        - Fix Maxwell empty messages [#978](https://github.com/pingcap/ticdc/pull/978)

    + Backup and Restore (BR)

        - Fix send on closed channel panic during restore [#559](https://github.com/pingcap/br/pull/559)

    + TiDB Lightning

        - Fix a bug about wrong column info [#420](https://github.com/pingcap/tidb-lightning/pull/420)
        - Fix infinity loop in retry get region in local mode [#418](https://github.com/pingcap/tidb-lightning/pull/418)

## Others

+ TiDB

    - Introduce errors documentation generator to generate errors.toml [#20564](https://github.com/pingcap/tidb/pull/20564)
    - Speed up parse slow-log when query slow_query. [#20556](https://github.com/pingcap/tidb/pull/20556)
    - When verifying potential new plans, plan binding will now wait before timing out worse plans so that more debug information can be written to the TiDB error log. [#20530](https://github.com/pingcap/tidb/pull/20530)
    - Add execution retry time in slow log and slow_query. [#20495](https://github.com/pingcap/tidb/pull/20495)
    - Add execution retry count in slow log and slow_query. [#20494](https://github.com/pingcap/tidb/pull/20494)
    - Add system table `table_storage_stats` [#20431](https://github.com/pingcap/tidb/pull/20431)
    - Add rpc runtime stats information for insert/update/replace statement. [#20430](https://github.com/pingcap/tidb/pull/20430)
    - Add executor information in `explain for connection` result. [#20384](https://github.com/pingcap/tidb/pull/20384)
    - Fix a bug that the coercibilities of enum and set are wrong. [#20364](https://github.com/pingcap/tidb/pull/20364)
    - Config: check if valid storage by simple indexing [#20342](https://github.com/pingcap/tidb/pull/20342)
    - Duplicate order by conditions are eliminated [#20333](https://github.com/pingcap/tidb/pull/20333)
    - The TiDB error log now reports client connect/disconnect activity only under debug level verbosity. [#20321](https://github.com/pingcap/tidb/pull/20321)
    - Add metrics for coprocessor cache [#20293](https://github.com/pingcap/tidb/pull/20293)
    - Fix ambiguous year conversion [#20292](https://github.com/pingcap/tidb/pull/20292)
    - Fixed an issue where the KV duration panel contains `store0` [#20260](https://github.com/pingcap/tidb/pull/20260)
    - Fix FLOAT data type: out of range data should not be inserted [#20252](https://github.com/pingcap/tidb/pull/20252)
    - Fix a bug that the generated column doesn't handle bad null value [#20216](https://github.com/pingcap/tidb/pull/20216)
    - Add pessimistic lock keys runtime information [#20199](https://github.com/pingcap/tidb/pull/20199)
    - Add two extra time-consuming sections in runtime information and trace span [#20187](https://github.com/pingcap/tidb/pull/20187)
    - Add transaction commit runtime information in slow log [#20185](https://github.com/pingcap/tidb/pull/20185)
    - Fix inaccurate error info for year column out of range. [#20170](https://github.com/pingcap/tidb/pull/20170)
    - Fix unexpected 'invalid auto-id' error in pessimistic txn retry. [#20134](https://github.com/pingcap/tidb/pull/20134)
    - Fix an issue that alter enum/set type does not check constraint [#20046](https://github.com/pingcap/tidb/pull/20046)
    - Fix cop task runtime information is wrong in the concurrent executor. [#19947](https://github.com/pingcap/tidb/pull/19947)
    - Fix cannot select session scope explicitly with unchangeable variables [#19944](https://github.com/pingcap/tidb/pull/19944)

+ TiKV

    - Error_code: re-format metafile [#8877](https://github.com/tikv/tikv/pull/8877)
    - Move counter metric processing into the scheduler worker. [#8872](https://github.com/tikv/tikv/pull/8872)
    - Fix the bug that mutex conflict of encryption makes pd-worker deal with heartbeat slow [#8869](https://github.com/tikv/tikv/pull/8869)
    - Raftstore: record the noop entry message temporarily like pending_votes [#8864](https://github.com/tikv/tikv/pull/8864)
    - Config: enable dynamically change config pessimistic-txn.pipelined [#8853](https://github.com/tikv/tikv/pull/8853)
    - Add the Fast-Tune panel page as performance assisted diagnosis [#8804](https://github.com/tikv/tikv/pull/8804)
    - Enabling profiling features by default [#8801](https://github.com/tikv/tikv/pull/8801)
    - Fix generating memory profile [#8790](https://github.com/tikv/tikv/pull/8790)
    - Fixed failure to backup database on GCS when storage class was provided. [#8763](https://github.com/tikv/tikv/pull/8763)
    - Add `security.redact-info-log` config, which redacts user data from logs [#8746](https://github.com/tikv/tikv/pull/8746)

+ PD

    - TiDB Dashboard: Fix a bug that KeyViz may panic [#3096](https://github.com/pingcap/pd/pull/3096)
    - Generate the metafile of errors [#3090](https://github.com/pingcap/pd/pull/3090)
    - Fix the bug that PD might panic if there is down store with 10 minutes [#3069](https://github.com/pingcap/pd/pull/3069)
    - Add additional info for operator [#3009](https://github.com/pingcap/pd/pull/3009)

+ TiFlash

    - Add metrics about memory usage for cop task
    - Fix bug: waiting index during learner read may cost long time if proxy can not catch up latest raft lease info
    - Add errors.toml to support standard error code
    - Fix bug: proxy write too much region state info to kv engine while replaying outdated raft log
