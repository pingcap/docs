---
title: TiDB 4.0.14 Release Notes
---

# TiDB 4.0.14 Release Notes

Release date: July 22, 2021

TiDB version: 4.0.14

## Compatibility Changes

+ TiDB

    - For users upgrading from TiDB 4.0, the value of `tidb_multi_statement_mode` is now `OFF`. It is recommended to use the multi-statement feature of your client library instead, see the documentation on `tidb_multi_statement_mode` for additional details. [#25749](https://github.com/pingcap/tidb/pull/25749)

## Improvements

+ Tools

    + Backup & Restore (BR)

        - Refactor storage.ExternalStorage interface to support compress [#1317](https://github.com/pingcap/br/pull/1317)

## Bug Fixes

+ TiDB

    - Generate correct number of rows when all agg funcs are pruned [#26039](https://github.com/pingcap/tidb/pull/26039)
    - Executor: fix ifnull bug when arg is enum/set [#26035](https://github.com/pingcap/tidb/pull/26035)
    - Fix wrong aggregate pruning for some cases [#26033](https://github.com/pingcap/tidb/pull/26033)
    - Fix incorrect result of set type for merge join [#26032](https://github.com/pingcap/tidb/pull/26032)
    - Expression: fix IN expr critical bug [#25665](https://github.com/pingcap/tidb/pull/25665)
    - Fix panic when 'select ... for update' works on a join operation and the join uses partition table [#25501](https://github.com/pingcap/tidb/pull/25501)
    - Fix the issue point get cached plan of prepared statement is incorrectly used by in transaction point get statement. [#24764](https://github.com/pingcap/tidb/pull/24764)

+ TiFlash

    - Fix potential npe in executeTS during DAG compile [#2377](https://github.com/pingcap/tics/pull/2377)
    - Fix the panic issue that occurs when the read load is heavy [#2280](https://github.com/pingcap/tics/pull/2280)
    - Fix the issue that TiFlash nodes keep restart because of split failure. [#2218](https://github.com/pingcap/tics/pull/2218)
    - Fix the bug that TiFlash can not GC delta data under rare case [#2183](https://github.com/pingcap/tics/pull/2183)
    - Fix the potential concurrency problem when clone the shared delta index. [#2032](https://github.com/pingcap/tics/pull/2032)
    - Fix the bug that incomplete data may make TiFlash fail to restart [#2002](https://github.com/pingcap/tics/pull/2002)
    - Fix the problem that old dmfile is not removed atomically [#1924](https://github.com/pingcap/tics/pull/1924)
    - Fix the problem that TiFlash will crash when executing SUBSTRING function with specific argument [#1914](https://github.com/pingcap/tics/pull/1914)
    - Fix the issue that cast int as time function in TiFlash's coprocessor may produce wrong result [#1892](https://github.com/pingcap/tics/pull/1892)

+ Tools

    - BR

        * Fix parquet parse when parse decimal type [#1276](https://github.com/pingcap/br/pull/1276)
        * Fix the bug that lightning returns EOF error when CSV file without '\r\n' at the last line and `strict-format = true`. [#1188](https://github.com/pingcap/br/pull/1188)
        * Fix the bug that lightning rebase wrong auto_increment base when the auto_increment field type is float or double. [#1185](https://github.com/pingcap/br/pull/1185)

## 以下 note 未分类。请将以下 note 进行分类 (New feature, Improvements, Bug fixes, Compatibility Changes 四类)，并移动到上面对应的标题下。如果某条 note 为多余的，请删除。如果漏抓取了 note，请手动补充

+ TiDB

    - Fix a bug which is caused by prior bug fix PR [#26274](https://github.com/pingcap/tidb/pull/26274)
    - Change the lock record into put record for the index keys using point/batch point get for update read. [#26223](https://github.com/pingcap/tidb/pull/26223)
    - Load: fix load data with non-utf8 can succeed [#26142](https://github.com/pingcap/tidb/pull/26142)
    - TiDB now supports the mysql system variable `init_connect` and associated functionality. [#26031](https://github.com/pingcap/tidb/pull/26031)
    - Planner: support stable result mode [#26003](https://github.com/pingcap/tidb/pull/26003)
    - Enlarge the variable tidb_stmt_summary_max_stmt_count default value from 200 to 3000 [#25872](https://github.com/pingcap/tidb/pull/25872)
    - Enable the pushdown of builtin function `json_unquote()` to TiKV. [#25721](https://github.com/pingcap/tidb/pull/25721)
    - Planner: select distinct should bypass batchget [#25532](https://github.com/pingcap/tidb/pull/25532)
    - Important security issue for handling ALTER USER statements [#25347](https://github.com/pingcap/tidb/pull/25347)
    - Fix the bug that `TIKV_REGION_PEERS` table did not have the correct `DOWN` status. [#24918](https://github.com/pingcap/tidb/pull/24918)
    - Handle a potential statistic object's memory leak when HTTP api is used [#24650](https://github.com/pingcap/tidb/pull/24650)
    - Don't let SPM be affected by charset [#23295](https://github.com/pingcap/tidb/pull/23295)
    - Time: parse datatime won't truncate the reluctant string. [#22260](https://github.com/pingcap/tidb/pull/22260)
    - Fix a bug that `select into outfile` has no data with year column type [#22185](https://github.com/pingcap/tidb/pull/22185)

+ TiKV

    - ```release-note [#10572](https://github.com/tikv/tikv/pull/10572)
    - ```release-note [#10532](https://github.com/tikv/tikv/pull/10532)
    - ```release-note [#10531](https://github.com/tikv/tikv/pull/10531)
    - ```release-note [#10517](https://github.com/tikv/tikv/pull/10517)
    - ```release-note [#10504](https://github.com/tikv/tikv/pull/10504)
    - Ensure panic output is flushed to the log [#10488](https://github.com/tikv/tikv/pull/10488)
    - ```release-note [#10462](https://github.com/tikv/tikv/pull/10462)
    - ```release-note [#10433](https://github.com/tikv/tikv/pull/10433)
    - Copr: fix the wrong arguments type of json_unquote [#10425](https://github.com/tikv/tikv/pull/10425)
    - ```release-note [#10400](https://github.com/tikv/tikv/pull/10400)
    - ```release-note [#10395](https://github.com/tikv/tikv/pull/10395)
    - For release-5.0 [#10360](https://github.com/tikv/tikv/pull/10360)
    - ```release-note [#10320](https://github.com/tikv/tikv/pull/10320)
    - ```release-note [#10302](https://github.com/tikv/tikv/pull/10302)
    - ```release-note [#10291](https://github.com/tikv/tikv/pull/10291)
    - ```release-note [#10279](https://github.com/tikv/tikv/pull/10279)
    - Approximate split range evenly [#10275](https://github.com/tikv/tikv/pull/10275)
    - BR now supports S3-compatible storage using virtual-host addressing style. [#10242](https://github.com/tikv/tikv/pull/10242)
    - ```release-note [#10147](https://github.com/tikv/tikv/pull/10147)
    - Add metrics to see pending pd heartbeats number [#10008](https://github.com/tikv/tikv/pull/10008)
    - Change the default merge-check-tick-interval to 2 to speed up the retry of merge process [#9676](https://github.com/tikv/tikv/pull/9676)
    - Fix an issue that split may panic and corrupt the metadata if the split process is too slow and region merge is open. [#9584](https://github.com/tikv/tikv/pull/9584)

+ PD

    - ```release-note [#3882](https://github.com/pingcap/pd/pull/3882)
    - ```release-note [#3858](https://github.com/pingcap/pd/pull/3858)
    - ```release-note [#3854](https://github.com/pingcap/pd/pull/3854)
    - ```release-note [#3825](https://github.com/pingcap/pd/pull/3825)
    - ```release-note [#3809](https://github.com/pingcap/pd/pull/3809)
    - ```release-note [#3797](https://github.com/pingcap/pd/pull/3797)
    - ```release-note [#3790](https://github.com/pingcap/pd/pull/3790)
    - ```release-note [#3773](https://github.com/pingcap/pd/pull/3773)
    - ```release-note [#3761](https://github.com/pingcap/pd/pull/3761)
    - ```release-note [#3718](https://github.com/pingcap/pd/pull/3718)
    - ```release-note [#3703](https://github.com/pingcap/pd/pull/3703)
    - ```release-note [#3680](https://github.com/pingcap/pd/pull/3680)

+ Tools

    - BR

        * Fix the issue that restore from `mysql` schema would failed. [#1142](https://github.com/pingcap/br/pull/1142)
        * No realease note [#1131](https://github.com/pingcap/br/pull/1131)
        * Fix the issue that lightning panic due to batch kv greater than 4.0g. [#1128](https://github.com/pingcap/br/pull/1128)
        * Speed up restore by merging small backup files. [#655](https://github.com/pingcap/br/pull/655)

    - Dumpling

        * Always split TiDB v3.* tables through tidb rowid to save TiDB's memory. [#306](https://github.com/pingcap/dumpling/pull/306)
        * When using Dumpling to export to S3, we no longer require s3:ListBucket permission on the entire bucket, only the data source prefix itself. [#287](https://github.com/pingcap/dumpling/pull/287)

    - TiCDC

        * ```release-note [#2258](https://github.com/pingcap/ticdc/pull/2258)
        * ```release-note [#2215](https://github.com/pingcap/ticdc/pull/2215)
        * Fix extra partition dispatching when adding new table partition. [#2205](https://github.com/pingcap/ticdc/pull/2205)
        * Better err msg when PD endpoint missing certificate [#2184](https://github.com/pingcap/ticdc/pull/2184)
        * Add `capture-session-ttl` in cdc server config [#2169](https://github.com/pingcap/ticdc/pull/2169)
        * Fix panic when TiCDC fails to read `/proc/meminfo` [#2023](https://github.com/pingcap/ticdc/pull/2023)
        * Reduce unnecessary memory consumption [#2011](https://github.com/pingcap/ticdc/pull/2011)
        * Make sorter IO errors more user-friendly. [#1976](https://github.com/pingcap/ticdc/pull/1976)
        * Fix Unified Sorter memory consumption when tables are many. [#1957](https://github.com/pingcap/ticdc/pull/1957)
        * Fix a bug that some MySQL connection could leak after MySQL sink meets error and pauses. [#1945](https://github.com/pingcap/ticdc/pull/1945)
        * Add concurrency limit to the region incremental scan in kv client. [#1926](https://github.com/pingcap/ticdc/pull/1926)
        * Add metrics for table memory consumption [#1884](https://github.com/pingcap/ticdc/pull/1884)
        * Owner:  When tikv_gc_life_time is greater than gcttl, use tikv_gc_life_time to calculate the lower bound of gcSafePoint. [#1871](https://github.com/pingcap/ticdc/pull/1871)
        * Reduce memory malloc in sort heap to avoid too much CPU overhead. [#1862](https://github.com/pingcap/ticdc/pull/1862)
        * Fix a bug about resolved ts stopped when move a table. [#1827](https://github.com/pingcap/ticdc/pull/1827)
