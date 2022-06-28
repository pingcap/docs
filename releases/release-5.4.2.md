---
title: TiDB 5.4.2 Release Notes
---

# TiDB 5.4.2 Release Notes

Release Date: xx xx, 2022

TiDB version: 5.4.2

## __unsorted

+ PingCAP/TiDB

    <!--transaction-->
    - ```release-note [#34906](https://github.com/pingcap/tidb/issues/34906)
    - ```release-note [#35198](https://github.com/pingcap/tidb/issues/35198)

    <!--diagnosis-->
    - ```release-note [#35340](https://github.com/pingcap/tidb/issues/35340)

    <!--sql-infra-->
    - ```release-note [#34722](https://github.com/pingcap/tidb/issues/34722)
    - ```release-note [#34638](https://github.com/pingcap/tidb/pull/34638)
    - ```release-note [#33965](https://github.com/pingcap/tidb/issues/33965)

    <!--planner-->
    - ```release-note [#34613](https://github.com/pingcap/tidb/issues/34613)

+ TiKV/TiKV

    - Fix the issue of unexpected `panic` on analyzed statistics when `max_sample_size` is set to `0`. [#11192](https://github.com/tikv/tikv/issues/11192)
    - Fix the potential issue of mistakenly reporting TiKV panics when exiting TiKV [#12231](https://github.com/tikv/tikv/issues/12231)
    - Fix possible panic when source peer catch up logs by snapshot in merge [#12663](https://github.com/tikv/tikv/issues/12663)
    - Fix potential panic when a peer is being split and destroyed at the same time [#12825](https://github.com/tikv/tikv/issues/12825)
    - Reload TLS certificate automatically when it changes. [#12546](https://github.com/tikv/tikv/issues/12546)
    - Fix bug which causes frequent pd client reconnection [#12345](https://github.com/tikv/tikv/issues/12345)
    - Improve the health check to detect unavailable Raftstore, so that the TiKV client can update Region Cache in time [#12398](https://github.com/tikv/tikv/issues/12398)
    - Fix a wrong check in datetime when the datetime has a fraction and 'Z' [#12739](https://github.com/tikv/tikv/issues/12739)
    - Fix tikv crash when conv empty string [#12673](https://github.com/tikv/tikv/issues/12673)
    - Fix possible duplicate commit record in async-commit pessimistic transactions. [#12615](https://github.com/tikv/tikv/issues/12615)
    - Use `posix_fallocate` for space reservation. [#12543](https://github.com/tikv/tikv/issues/12543)
    - Fix the issue that TiKV reports the `invalid store ID 0` error when using Follower Read [#12478](https://github.com/tikv/tikv/issues/12478)
    - Fix the issue of TiKV panic caused by the race between destroying peers and batch splitting Regions [#12368](https://github.com/tikv/tikv/issues/12368)
    - Fix the issue that tikv-ctl returns an incorrect result due to its wrong string match [#12329](https://github.com/tikv/tikv/issues/12329)
    - Transfer the leadership to CDC observer to reduce latency jitter [#12111](https://github.com/tikv/tikv/issues/12111)


+ PD

    (dup: release-6.1.0.md > Bug fixes> PD)- Fix the wrong status code of `not leader` [#4797](https://github.com/tikv/pd/issues/4797)
    (dup: release-6.1.0.md > Improvements> PD)- Disable compiling swagger server by default [#4932](https://github.com/tikv/pd/issues/4932)
    - Fix the issue that the hot region may cause panic due to no leader [#5005](https://github.com/tikv/pd/issues/5005)
    (dup: release-6.1.0.md > Bug fixes> PD)- Fix the issue that scheduling cannot start immediately after the PD leader transfer [#4769](https://github.com/tikv/pd/issues/4769)
    (dup: release-6.1.0.md > Bug fixes> PD)- Fix a bug of TSO fallback in some corner cases [#4884](https://github.com/tikv/pd/issues/4884)
    (dup: release-5.4.1.md > Bug Fixes> TiDB)- Fix the error that occurs when reading from the `INFORMATION_SCHEMA.ATTRIBUTES` table by skipping the unidentifiable table attributes [#33665](https://github.com/pingcap/tidb/issues/33665)


+ Tools

    + BR

        - ```release-note [#35279](https://github.com/pingcap/tidb/issues/35279)
        - ```release-note [#34865](https://github.com/pingcap/tidb/issues/34865)
        - ```release-note [#34956](https://github.com/pingcap/tidb/issues/34956)
        - ```release-note [#34350](https://github.com/pingcap/tidb/issues/34350)
        (dup: release-6.0.0-dmr.md > Bug fixes> Tools> Backup & Restore (BR))- Fix a bug that BR gets stuck when the restore operation meets some unrecoverable errors [#33200](https://github.com/pingcap/tidb/issues/33200)

    + TiDB Lightning

        (dup: release-6.1.0.md > Improvements> Tools> TiDB Lightning)- Optimize Scatter Region to batch mode to improve the stability of the Scatter Region process [#33618](https://github.com/pingcap/tidb/issues/33618)

    + PingCAP/TiCDC

        (dup: release-6.1.0.md > Bug fixes> Tools> TiCDC)- Fix data loss that occurs in special incremental scanning scenarios [#5468](https://github.com/pingcap/tiflow/issues/5468)
        - Fix a bug in redo log manager that flush log executed before writing logs [#5486](https://github.com/pingcap/tiflow/issues/5486)
        - Fix a bug that resolved ts moves too fast when part of tables are not maintained redo writer. [#5486](https://github.com/pingcap/tiflow/issues/5486)
        - Add uuid suffix to redo log file name to prevent name conflict, which may cause data loss. [#5486](https://github.com/pingcap/tiflow/issues/5486)
        - Fix replication interruption due to leader missing by extending region retry duration
        - Fix min resolved ts/checkpoint table ID metrics [#5542](https://github.com/pingcap/tiflow/pull/5542)
        - `Fix a bug that mysql sink may save a wrong checkpointTs`. [#5107](https://github.com/pingcap/tiflow/issues/5107)
        - Fix a bug that may causes goroutine leak in http server. [#5303](https://github.com/pingcap/tiflow/issues/5303)
        - `None` [#2792](https://github.com/pingcap/tiflow/issues/2792)

    + TiDB Data Migration (DM)

        (dup: release-6.1.0.md > Bug fixes> Tools> TiDB Data Migration (DM))- Fix the issue that DM occupies more disk space after the task automatically resumes [#3734](https://github.com/pingcap/tiflow/issues/3734) [#5344](https://github.com/pingcap/tiflow/issues/5344)
        (dup: release-6.1.0.md > Bug fixes> Tools> TiDB Data Migration (DM))- Fix an issue that the uppercase table cannot be replicated when `case-sensitive: true` is not set [#5255](https://github.com/pingcap/tiflow/issues/5255)
        - `None`. [#4858](https://github.com/pingcap/tiflow/issues/4858)

## Compatibility change(s)

## Improvements

## Bug Fixes

+ PingCAP/TiDB

    <!--planner-->
    - ```release-note [#34678](https://github.com/pingcap/tidb/issues/34678)


+ PingCAP/TiFlash

    <!--storage-->
    - Fix the TiFlash crash issue that occurs after dropping a column of a table with clustered indexes under some situations. [#5154](https://github.com/pingcap/tiflash/issues/5154)
    (dup: release-6.1.0.md > Bug fixes> TiFlash)- Fix potential data inconsistency after a lot of INSERT and DELETE operations [#4956](https://github.com/pingcap/tiflash/issues/4956)
