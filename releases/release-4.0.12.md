---
title: TiDB 4.0.12 Release Notes
---

# TiDB 4.0.12 Release Notes

Release date: March 31, 2021

TiDB version: 4.0.12

## New Features

+ TiFlash

    - Add tools to check exact tiflash replica status for online rolling update [#1512](https://github.com/pingcap/tics/pull/1512)

## Improvements

+ TiFlash

    - Allow omitting deprecated "users.*" settings in the configuration file of TiFlash [#1535](https://github.com/pingcap/tics/pull/1535)
    - Reduce the size of TiFlash binary file [#1414](https://github.com/pingcap/tics/pull/1414)

## Bug Fixes

+ PD

    - Save to the region cache when pending-peers or down-peers change [#3471](https://github.com/pingcap/pd/pull/3471)
    - Checker: prevent the regions in split-cache from becoming the target of merge [#3459](https://github.com/pingcap/pd/pull/3459)

+ TiFlash

    - Fix the issue that binary type column's default value containing leading zero bytes is trimmed and does not contain padded tailing zero bytes [#1571](https://github.com/pingcap/tics/pull/1571)
    - Fix the bug that TiFlash fail to sync schema if the database name contains special character [#1559](https://github.com/pingcap/tics/pull/1559)
    - Use an adaptive aggressive GC strategy to avoid OOM [#1553](https://github.com/pingcap/tics/pull/1553)
    - Fix wrong result of IN function [#1532](https://github.com/pingcap/tics/pull/1532)
    - Fix the bug that opened file count shown in Grafana is high [#1503](https://github.com/pingcap/tics/pull/1503)
    - Support timestamp literal in dag requeset [#1501](https://github.com/pingcap/tics/pull/1501)
    - Fix potential segmentation fault in TiFlash [#1491](https://github.com/pingcap/tics/pull/1491)
    - Fix problem CastStringAsInt may produce wrong result. [#1481](https://github.com/pingcap/tics/pull/1481)
    - Fix a bug that the `like` function may return wrong result [#1461](https://github.com/pingcap/tics/pull/1461)

+ Tools

    - Backup & Restore (BR)

        - Fix the bug that lightning generated ts may be to large or small that query may return incorrect result. [#860](https://github.com/pingcap/br/pull/860)
        - No release note (it's not released yet.) [#854](https://github.com/pingcap/br/pull/854)
        - Fix the bug that importer may ignore write rows error if open engine returns `file exists` error [#848](https://github.com/pingcap/br/pull/848)

## 请判断下面未分类 note，对下面 note 进行分类并移动到以上三个分类部分中

+ TiKV

    - Fix missing space when casting json to string in TiKV coprocessor [#9666](https://github.com/tikv/tikv/pull/9666)
    - Change the default `leader-transfer-max-log-lag` to 128 to increase the success rate of leader transfer [#9605](https://github.com/tikv/tikv/pull/9605)

+ PD

    - Fix the bug that the isolation level is wrong when the store lacks label [#3474](https://github.com/pingcap/pd/pull/3474)

+ Tools

    - BR

        - Reduce memory usage during backup. [#886](https://github.com/pingcap/br/pull/886)
        - Added configurations `tikv-importer.engine-mem-cache-size` and `tikv-importer.local-writer-mem-cache-size` to tune between memory usage and performance. [#866](https://github.com/pingcap/br/pull/866)
        - BR would log `HTTP_PROXY` and `HTTPS_PROXY` now. [#827](https://github.com/pingcap/br/pull/827)
        - Add cluster_version and br_version info in backupmeta [#803](https://github.com/pingcap/br/pull/803)
        - Check TiDB cluster version before running TiDB-Lightning to avoid unexpected errors. [#787](https://github.com/pingcap/br/pull/787)
        - Improve backup performance when there are many tables. [#745](https://github.com/pingcap/br/pull/745)

    - TiCDC

        - Fix a data loss bug when capture restarts due to network issue, and some table on it is scheduled at the same time. [#1523](https://github.com/pingcap/ticdc/pull/1523)
        - Add double confirm when creating or resuming changefeed with `start-ts` or `checkpoint-ts` 1 day before current ts. [#1499](https://github.com/pingcap/ticdc/pull/1499)
        - No release note, the bug is never released [#1475](https://github.com/pingcap/ticdc/pull/1475)
        - Fix a resolved ts event disorder problems caused by concurrency [#1472](https://github.com/pingcap/ticdc/pull/1472)
        - No release note, this bug is never released [#1470](https://github.com/pingcap/ticdc/pull/1470)
