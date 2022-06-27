---
title: TiDB 5.4.2 Release Notes
---

# TiDB 5.4.2 Release Notes

Release Date: xx xx, 2022

TiDB version: 5.4.2

## __unsorted

+ PingCAP/TiDB

    - ```release-note [#35695](https://github.com/pingcap/tidb/pull/35695)
    - ```release-note [#35561](https://github.com/pingcap/tidb/pull/35561)
    - ```release-note [#35464](https://github.com/pingcap/tidb/pull/35464)
    - ```release-note [#35385](https://github.com/pingcap/tidb/pull/35385)
    - ```release-note [#35353](https://github.com/pingcap/tidb/pull/35353)
    - ```release-note [#34983](https://github.com/pingcap/tidb/pull/34983)
    - ```release-note [#34955](https://github.com/pingcap/tidb/pull/34955)
    - ```release-note [#34693](https://github.com/pingcap/tidb/pull/34693)
    - ```release-note [#34638](https://github.com/pingcap/tidb/pull/34638)
    - ```release-note [#34378](https://github.com/pingcap/tidb/pull/34378)
    - lightning: split and scatter regions in batches [#34258](https://github.com/pingcap/tidb/pull/34258)
    - ```release-note [#34081](https://github.com/pingcap/tidb/pull/34081)
    - Fix a bug that caused BR get stuck when restore meets some unrecoverable error. [#33268](https://github.com/pingcap/tidb/pull/33268)


+ TiKV/TiKV

    - Fix the issue of unexpected `panic` on analyzed statistics when `max_sample_size` is set to `0`. [#12906](https://github.com/tikv/tikv/pull/12906)
    - resolved_ts: fix shutdown panic [#12881](https://github.com/tikv/tikv/pull/12881)
    - Fix possible panic when source peer catch up logs by snapshot in merge [#12873](https://github.com/tikv/tikv/pull/12873)
    - Fix potential panic when a peer is being split and destroyed at the same time [#12863](https://github.com/tikv/tikv/pull/12863)
    - Reload TLS certificate automatically when it changes. [#12856](https://github.com/tikv/tikv/pull/12856)
    - Fix bug which causes frequent pd client reconnection [#12833](https://github.com/tikv/tikv/pull/12833)
    - Report bad health status if raftstore stops working. [#12818](https://github.com/tikv/tikv/pull/12818)
    - Fix a wrong check in datetime when the datetime has a fraction and 'Z' [#12746](https://github.com/tikv/tikv/pull/12746)
    - Fix tikv crash when conv empty string [#12693](https://github.com/tikv/tikv/pull/12693)
    - Fix possible duplicate commit record in async-commit pessimistic transactions. [#12654](https://github.com/tikv/tikv/pull/12654)
    - Use `posix_fallocate` for space reservation. [#12553](https://github.com/tikv/tikv/pull/12553)
    - Fix a bug that sometimes generates a message with zero store id when doing follower read [#12530](https://github.com/tikv/tikv/pull/12530)
    - Please add a release note.

Please refer to [Release Notes Language Style Guide](https://pingcap.github.io/tidb-dev-guide/contribute-to-tidb/release-notes-style-guide.html) to write a quality release note.

If you don't think this PR needs a release note then fill it with None.
If this PR will be picked to release branch, then a release note is probably required. [#12502](https://github.com/tikv/tikv/pull/12502)
    - fix race between split check and destroy [#12406](https://github.com/tikv/tikv/pull/12406)
    - Fix logic of error string match in `bad-ssts`. [#12150](https://github.com/tikv/tikv/pull/12150)
    - Pass leader transferee to cdc observer to reduce TiCDC latency spike. [#12137](https://github.com/tikv/tikv/pull/12137)


+ PD

    - Fix the issue that the status code of `not leader` is sometimes wrong [#5218](https://github.com/tikv/pd/pull/5218)
    - server: disable swagger server [#5176](https://github.com/tikv/pd/pull/5176)
    - Fix the issue that the hot region may cause panic due to no leader [#5004](https://github.com/tikv/pd/pull/5004)
    - Fix the issue that scheduling cannot immediately start after PD leader transfers [#4970](https://github.com/tikv/pd/pull/4970)
    - Fix the corner case that may cause TSO fallback. [#4892](https://github.com/tikv/pd/pull/4892)


+ Tools

    + PingCAP/TiCDC

        - Fix data loss when upstream transaction conflicts during cdc reconnection [#5829](https://github.com/pingcap/tiflow/pull/5829)
        - Fix a bug in redo log manager that flush log executed before writing logs [#5629](https://github.com/pingcap/tiflow/pull/5629)
        - Fix a bug that resolved ts moves too fast when part of tables are not maintained redo writer. [#5618](https://github.com/pingcap/tiflow/pull/5618)
        - Add uuid suffix to redo log file name to prevent name conflict, which may cause data loss. [#5614](https://github.com/pingcap/tiflow/pull/5614)
        - Fix data loss when upstream transaction conflicts during cdc reconnection
Fix replication interruption due to leader missing by extending region retry duration
Fix min resolved ts/checkpoint table ID metrics [#5542](https://github.com/pingcap/tiflow/pull/5542)
        - `Fix a bug that mysql sink may save a wrong checkpointTs`. [#5437](https://github.com/pingcap/tiflow/pull/5437)
        - Fix a bug that after auto resume, DM will use more disk space. [#5415](https://github.com/pingcap/tiflow/pull/5415)
        - `Add support for region-label to enable meta-region isolation` [#5354](https://github.com/pingcap/tiflow/pull/5354)
        - Fix a bug that may causes goroutine leak in http server. [#5346](https://github.com/pingcap/tiflow/pull/5346)
        - Fix DM can't replicate uppercase tables when the task has case-sensitive: false [#5309](https://github.com/pingcap/tiflow/pull/5309)
        - `None` [#5172](https://github.com/pingcap/tiflow/pull/5172)
        - `None`. [#4869](https://github.com/pingcap/tiflow/pull/4869)

## Compatibility change(s)

## Improvements

## Bug Fixes

+ PingCAP/TiDB

    - ```release-note [#34737](https://github.com/pingcap/tidb/pull/34737)


+ PingCAP/TiFlash

    - Fix the TiFlash crash issue that occurs after dropping a column of a table with clustered indexes under some situations. [#5191](https://github.com/pingcap/tiflash/pull/5191)
    - Fix potential wrong result after a lot of insert and delete operations [#4968](https://github.com/pingcap/tiflash/pull/4968)


