---
title: TiDB 4.0.14 Release Notes
---

# TiDB 4.0.14 Release Notes

Release date: July 22, 2021

TiDB version: 4.0.14

## Compatibility Changes

+ TiDB

    - Change the default value of `tidb_multi_statement_mode` from `WARN` to `OFF` in v4.0. It is recommended to use the multi-statement feature of your client library instead. See [the documentation on `tidb_multi_statement_mode`](/system-variables.md#tidb_multi_statement_mode-new-in-v4011) for details. [#25749](https://github.com/pingcap/tidb/pull/25749)
    - Upgrade Grafana dashboard from v6.1.16 to v7.5.7 to solve two security vulnerabilities. See the [Grafana post](https://grafana.com/blog/2020/06/03/grafana-6.7.4-and-7.0.2-released-with-important-security-fix/) for details.

## Improvements

+ Tools

    + Backup & Restore (BR)

        - Speed up restore by merging small backup files. [#655](https://github.com/pingcap/br/pull/655)

    + Dumpling

        - Always split TiDB v3.* tables through `_tidb_rowid` to reduce TiDB's memory use. [#306](https://github.com/pingcap/dumpling/pull/306)

    + TiCDC

        - Better error message when PD endpoint missing certificate [#2184](https://github.com/pingcap/ticdc/pull/2184)
        - Make sorter IO errors more user-friendly. [#1976](https://github.com/pingcap/ticdc/pull/1976)
        - Add concurrency limit to the region incremental scan in kv client. [#1926](https://github.com/pingcap/ticdc/pull/1926)
        - Add metrics for table memory consumption [#1884](https://github.com/pingcap/ticdc/pull/1884)

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

    - Fix the potential panic issue that occurs while compiling DAG requests
    - Fix the panic issue that occurs when read load is heavy
    - Fix the issue that TiFlash keeps restarting because of split failure in column storage
    - Fix a potential bug that TiFlash can not GC delta data
    - Fix the issue of incorrect results when cloning shared delta index concurrently
    - Fix a bug that TiFlash fails to restart because of incomplete data
    - Fix the issue that old dm files are not removed automatically
    - Fix the panic issue that occurs while executing `SUBSTRING` function with specific arguments
    - Fix the issue of incorrect results when casting the `TIME` type to the `INTEGER` type

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that data restore from the `mysql` schema might fail [#1142](https://github.com/pingcap/br/pull/1142)

    + TiDB Lightning

        - Fix parquet parse when parse decimal type [#1276](https://github.com/pingcap/br/pull/1276)
        - Fix the bug that Lightning returns EOF error when CSV file without `\r\n` at the last line and `strict-format = true` [#1188](https://github.com/pingcap/br/pull/1188)
        - Fix the bug that Lightning rebase wrong auto_increment base when the auto_increment field type is float or double [#1185](https://github.com/pingcap/br/pull/1185)
        - Fix the issue that Lightning panics due to batching KV larger than 4 GB [#1128](https://github.com/pingcap/br/pull/1128)

    + Dumpling

        - When using Dumpling to export to S3, we no longer require s3:ListBucket permission on the entire bucket, only the data source prefix itself [#287](https://github.com/pingcap/dumpling/pull/287)

    + TiCDC

        - Fix extra partition dispatching when adding new table partition [#2205](https://github.com/pingcap/ticdc/pull/2205)
        - Add `capture-session-ttl` in CDC server config [#2169](https://github.com/pingcap/ticdc/pull/2169)
        - Fix panic when TiCDC fails to read `/proc/meminfo` [#2023](https://github.com/pingcap/ticdc/pull/2023)
        - Reduce unnecessary memory consumption [#2011](https://github.com/pingcap/ticdc/pull/2011)
        - Fix Unified Sorter memory consumption when tables are many [#1957](https://github.com/pingcap/ticdc/pull/1957)
        - Fix a bug that some MySQL connection could leak after MySQL sink meets error and pauses [#1945](https://github.com/pingcap/ticdc/pull/1945)
        - Fix the issue that TiCDC changefeed cannot be created when start ts is less than current ts - gcttl [#1871](https://github.com/pingcap/ticdc/pull/1871)
        - Reduce memory malloc in sort heap to avoid too much CPU overhead [#1862](https://github.com/pingcap/ticdc/pull/1862)
        - Fix a bug about resolved ts stopped when move a table [#1827](https://github.com/pingcap/ticdc/pull/1827)

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

    - Fix duration calculation panics on certain platforms [#10572](https://github.com/tikv/tikv/pull/10572)
    - Fix wrong function cast double to double [#10532](https://github.com/tikv/tikv/pull/10532)
    - Ensure panic output is flushed to the log [#10488](https://github.com/tikv/tikv/pull/10488)
    - Avoid panic when building a snapshot twice if encryption enabled [#10462](https://github.com/tikv/tikv/pull/10462)
    - Copr: fix the wrong arguments type of json_unquote [#10425](https://github.com/tikv/tikv/pull/10425)
    - skip clearing callback during gracefully shutdown to avoid breaking ACID in some cases [#10395](https://github.com/tikv/tikv/pull/10395)
    - Fix backup threads leak [#10360](https://github.com/tikv/tikv/pull/10360)
    - Approximate split range evenly [#10275](https://github.com/tikv/tikv/pull/10275)
    - BR now supports S3-compatible storage using virtual-host addressing style. [#10242](https://github.com/tikv/tikv/pull/10242)
    - Limit CDC sink memory consumption. [#10147](https://github.com/tikv/tikv/pull/10147)
    - Add metrics to see pending pd heartbeats number [#10008](https://github.com/tikv/tikv/pull/10008)
    - Change the default merge-check-tick-interval to 2 to speed up the retry of merge process [#9676](https://github.com/tikv/tikv/pull/9676)
    - Fix an issue that split may panic and corrupt the metadata if the split process is too slow and region merge is open. [#9584](https://github.com/tikv/tikv/pull/9584)

+ PD

    - TiDB Dashboard: Add OIDC based SSO support [#3882](https://github.com/pingcap/pd/pull/3882)
    - Reduce the conflict due to multiple scheduler running in same time [#3858](https://github.com/pingcap/pd/pull/3858)
    - Fix the issue that the scheduler may appear again even if we have already executed the delete operation [#3825](https://github.com/pingcap/pd/pull/3825)
    - Update TiDB Dashboard to v2021.06.15.1 [#3797](https://github.com/pingcap/pd/pull/3797)
    - Fix the data race when the scheduler is started before loading TTL configurations [#3773](https://github.com/pingcap/pd/pull/3773)
    - Fix pd may get panic during scattering region [#3761](https://github.com/pingcap/pd/pull/3761)
    - Fix the issue that leader re-election be slow when there are many stores [#3718](https://github.com/pingcap/pd/pull/3718)
    - Fix the priority problems for some kinds of operators [#3703](https://github.com/pingcap/pd/pull/3703)
    - Fix the panic issue about remove evict leader scheduler from a nonexistent store [#3680](https://github.com/pingcap/pd/pull/3680)
