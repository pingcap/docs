---
title: TiDB 4.0.14 Release Notes
---

# TiDB 4.0.14 Release Notes

Release date: July 22, 2021

TiDB version: 4.0.14

## Compatibility Changes

+ TiDB

    - Change the default value of `tidb_multi_statement_mode` from `WARN` to `OFF` in v4.0. It is recommended to use the multi-statement feature of your client library instead. See [the documentation on `tidb_multi_statement_mode`](/system-variables.md#tidb_multi_statement_mode-new-in-v4011) for details. [#25749](https://github.com/pingcap/tidb/pull/25749)
    - Upgrade Grafana dashboard from v6.1.16 to v7.5.7 to solve two security vulnerabilities. See the [Grafana blog post](https://grafana.com/blog/2020/06/03/grafana-6.7.4-and-7.0.2-released-with-important-security-fix/) for details.
    - Change the default value of the `tidb_stmt_summary_max_stmt_count` variable from `200` to `3000` [#25872](https://github.com/pingcap/tidb/pull/25872)

+ TiKV

    - Change the default value of `merge-check-tick-interval` from `10` to `2` to speed up the Region merge process [#9676](https://github.com/tikv/tikv/pull/9676)

## Feature Enhancements

+ TiKV

    - Add a metric to monitor the number of pending PD heartbeats, which helps locate the issue of slow PD threads [#10008](https://github.com/tikv/tikv/pull/10008)
    - Support using the virtual-host addressing mode to make BR support the S3-compatible storage [#10242](https://github.com/tikv/tikv/pull/10242)

+ TiDB Dashboard

    - Support OIDC SSO. By setting the OIDC-compatible SSO services (such as Okta and Auth0), users can log into TiDB Dashboard without entering the SQL password. [#960](https://github.com/pingcap/tidb-dashboard/pull/960)
    - Add the **Debug API** UI, which is an alternative method to the command line to call several common TiDB and PD internal APIs for advanced debugging. [#927](https://github.com/pingcap/tidb-dashboard/pull/927)

## Improvements

+ TiDB

    ?- Change the lock records into put record for the index keys using `point get` or `batch point get` for `UPDATE` reads [#26223](https://github.com/pingcap/tidb/pull/26223)
    - Support the MySQL system variable `init_connect` and its associated features [#26031](https://github.com/pingcap/tidb/pull/26031)
    - Support the stable result mode to make the query results more stable [#26003](https://github.com/pingcap/tidb/pull/26003)
    - Support pushing down the built-in function `json_unquote()` to TiKV [#25721](https://github.com/pingcap/tidb/pull/25721)
    - Make the SQL Plan Management (SPM) not affected by the character set [#23295](https://github.com/pingcap/tidb/pull/23295)

+ TiKV

    - Shutdown the status server first to make sure that the client can correctly check the shutdown status [#10504](https://github.com/tikv/tikv/pull/10504)
    - Always respond to stale peers to make sure that these peers are cleared quicker [#10400](https://github.com/tikv/tikv/pull/10400)
    - Limit the TiCDC sink's memory consumption [#10147](https://github.com/tikv/tikv/pull/10147)
    - When a Region is too large, use the even split to speed up the split process [#10275](https://github.com/tikv/tikv/pull/10275)

+ PD

    - Reduce the conflicts among multiple schedulers that run at the same time [#3858](https://github.com/pingcap/pd/pull/3858) [#3854](https://github.com/tikv/pd/pull/3854)

+ TiDB Dashboard

    - Update TiDB Dashboard to v2021.07.17.1 [#3882](https://github.com/pingcap/pd/pull/3882)
    - Support sharing the current session as a read-only session to avoid further modification to it [#960](https://github.com/pingcap/tidb-dashboard/pull/960)

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

    - Fix the issue that the `SELECT` result is incompatible with MySQL when joining a subquery with a `WHERE` clause evaluated to `false` [#24865](https://github.com/pingcap/tidb/issues/24865)
    - Fix the calculation error of the `ifnull` function that occurs when the argument is the `ENUM` or `SET` type [#24944](https://github.com/pingcap/tidb/issues/24944)
    - Fix the wrong aggregate pruning in some cases [#26033](https://github.com/pingcap/tidb/pull/26033)
    - Fix the incorrect result of the merge join operation that might occur when the column is the `SET` type [#26032](https://github.com/pingcap/tidb/pull/26032)
    - Fix the issue that TiDB returns wrong results for cartesian join [#25665](https://github.com/pingcap/tidb/pull/25665)
    - Fix the panic issue that occurs when `SELECT ... FOR UPDATE` works on a join operation and the join uses a partitioned table [#25501](https://github.com/pingcap/tidb/pull/25501)
    - Fix the issue that the cached `prepared` plan is incorrectly used for `point get` [#24764](https://github.com/pingcap/tidb/pull/24764)
    - Fix the issue that the `LOAD DATA` statement can abnormally import non-utf8 data [#26142](https://github.com/pingcap/tidb/pull/26142)
    - Fix a potential memory leak issue that occurs when accessing the statistics via an HTTP API [#24650](https://github.com/pingcap/tidb/pull/24650)
    - Fix a security issue that occurs when executing the `ALTER USER` statement [#25347](https://github.com/pingcap/tidb/pull/25347)
    - Fix the bug that `TIKV_REGION_PEERS` table did not have the correct `DOWN` status. [#24918](https://github.com/pingcap/tidb/pull/24918)
    - Fix the issue that invalid strings are not truncated when parsing `DateTime` [#22260](https://github.com/pingcap/tidb/pull/22260)
    - Fix the issue that the `select into outfile` statement might have no result when the column type is `YEAR` [#22185](https://github.com/pingcap/tidb/pull/22185)

+ TiKV

    - Fix the issue that the duration calculation might panic on certain platforms [#10572](https://github.com/tikv/tikv/pull/10572)
    - Fix the wrong function that casts `DOUBLE` to `DOUBLE` [#25200](https://github.com/pingcap/tidb/issues/25200)
    - Fix the issue that the panic log might be lost when using the async logger [#8998](https://github.com/tikv/tikv/issues/8998)
    - Fix the panic issue that occurs when building a snapshot twice if encryption is enabled [#10462](https://github.com/tikv/tikv/pull/10462)
    - Fix the wrong arguments type of the `json_unquote()` function in the coprocessor [#10176](https://github.com/tikv/tikv/issues/10176)
    - Fix the issues of suspicious warnings during shutdown and the non-deterministic response from Raftstore [#10395](https://github.com/tikv/tikv/pull/10395)
    - Fix the issue of backup threads leak [#10360](https://github.com/tikv/tikv/pull/10360)
    - Fix the issue that Region split might panic and corrupt the metadata if the split process is too slow and Region merge is on-going [#9584](https://github.com/tikv/tikv/pull/9584)
    - Fix the issue that the Region heartbeats prevent TiKV from splitting large Regions in some situation [#10274](https://github.com/tikv/tikv/pull/10274)
    - Fix the wrong statistics caused by the format inconsistency of CM Sketch between TiKV and TiDB [#10433](https://github.com/tikv/tikv/pull/10433)
    - Fix the wrong statistics of the `apply wait duration` metric [#9966](https://github.com/tikv/tikv/pull/9966)
    - Fix the "Missing Blob" error after using `delete_files_in_range` in Titan [#10232](https://github.com/tikv/tikv/pull/10232)

+ PD

    - Fix a bug that the scheduler might reappear after executing the delete operation [#3825](https://github.com/pingcap/pd/pull/3825)
    - Fix the data race issue that might occur when the scheduler is started before the temporary configuration is loaded [#3773](https://github.com/pingcap/pd/pull/3773)
    - Fix a PD panic issue that might occur during the Region scattering operation [#3761](https://github.com/pingcap/pd/pull/3761)
    - Fix the issue that the priority of some operators is not set correctly [#3703](https://github.com/pingcap/pd/pull/3703)
    - Fix a PD panic issue that might occur when deleting the `evict-leader` scheduler from a non-existent store [#3680](https://github.com/pingcap/pd/pull/3680)
    - Fix the issue that the PD Leader re-election is slow when there are many stores [#3697](https://github.com/tikv/pd/issues/3697)

+ TiDB Dashboard

    - Fix the issue that the **Profiling** UI cannot profile all TiDB instances [#944](https://github.com/pingcap/tidb-dashboard/pull/944)
    - Fix the issue that the **Statements** UI does not display "Plan Count" [#939](https://github.com/pingcap/tidb-dashboard/pull/939)
    - Fix the issue that the **Slow Query** UI might display the "unknown field" error after cluster upgrade [#930](https://github.com/pingcap/tidb-dashboard/pull/930)

+ TiFlash

    - Fix the potential panic issue that occurs when compiling DAG requests
    - Fix the panic issue that occurs when the read load is heavy
    - Fix the issue that TiFlash keeps restarting because of the split failure in column storage
    - Fix a potential bug that TiFlash cannot delete the delta data
    - Fix the incorrect results that occur when cloning the shared delta index concurrently
    - Fix a bug that TiFlash fails to restart in the case of incomplete data
    - Fix the issue that the old dm files cannot be removed automatically
    - Fix the panic issue that occurs when executing the `SUBSTRING` function with specific arguments
    - Fix the issue of incorrect results when casting the `INTEGER` type to the `TIME` type

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
